import imaplib
import email
from email.header import decode_header
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def read_emails():
    emails = []

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()

        latest_ids = mail_ids[-5:]  # Last 5 emails

        for i in latest_ids:
            status, msg_data = mail.fetch(i, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    from_ = msg.get("From")

                    emails.append((from_, subject))

        mail.logout()
        return emails

    except Exception as e:
        print("Error reading emails:", e)
        return []