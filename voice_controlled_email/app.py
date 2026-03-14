from flask import send_from_directory
from flask import Flask, render_template
from mic import listen
from voice_engine import speak
from email_sender import send_email
from email_reader import read_emails
import re
import time

app = Flask(__name__)

# ---------------- EMAIL VALIDATION ----------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html", message="Click Mic and Speak")


# ---------------- PROCESS VOICE ----------------
@app.route("/process", methods=["POST"])
def process():

    speak("Welcome. Say compose to send email or say inbox to read emails.")

    command = listen()

    if command is None:
        speak("I did not hear anything.")
        return render_template("index.html", message="No voice detected")

    # ---------------- COMPOSE EMAIL ----------------
    if "compose" in command:

        speak("Please say the recipient email address.")
        to_email = listen()

        if not to_email:
            speak("Recipient not received.")
            return render_template("index.html", message="Recipient not received")

        # convert spoken format to email
        to_email = to_email.replace(" at ", "@").replace(" dot ", ".").replace(" ", "")

        if not is_valid_email(to_email):
            speak("Invalid email address.")
            return render_template("index.html", message="Invalid Email Address")

        speak("Please say the subject.")
        subject = listen()

        if not subject:
            speak("Subject not received.")
            return render_template("index.html", message="Subject not received")

        speak("Please say your message.")
        body = listen()

        if not body:
            speak("Message not received.")
            return render_template("index.html", message="Message not received")

        speak("Do you want to send the email? Say yes or no.")
        confirm = listen()

        if confirm is None:
            speak("Confirmation not received.")
            return render_template("index.html", message="Confirmation not received")

        if "yes" in confirm or "send" in confirm:
            speak("Sending email.")
            success = send_email(to_email, subject, body)

            if success:
                speak("Email sent successfully.")
                time.sleep(1)
                return render_template("index.html", message="Email Sent Successfully")
            else:
                speak("Failed to send email.")
                return render_template("index.html", message="Error Sending Email")

        else:
            speak("Email cancelled.")
            return render_template("index.html", message="Email Cancelled")

    # ---------------- READ INBOX ----------------
    elif "inbox" in command:

        speak("Reading your latest emails.")
        emails = read_emails()

        if not emails:
            speak("No emails found.")
            return render_template("index.html", message="No Emails Found")

        for sender, subject in emails:
            speak(f"Email from {sender}. Subject is {subject}")

        return render_template("index.html", message="Inbox Read Successfully")

    else:
        speak("Command not recognized.")
        return render_template("index.html", message="Invalid Command")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")