from voice_engine import speak, listen
from email_sender import send_email
from email_reader import read_emails
import time

def main():
    speak("Welcome to Voice Controlled Email System")

    while True:
        speak("Say compose email, read inbox, or exit")
        command = listen()

        if command == "":
            continue

        if "compose" in command:
            send_email()

        elif "read" in command:
            read_emails()

        elif "exit" in command:
            speak("Goodbye")
            break

        else:
            speak("Command not recognized")

        time.sleep(1)

if __name__ == "__main__":
    main()
