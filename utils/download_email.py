import imaplib
import email
import os
from email.header import decode_header

# Function to decode email subject or sender
def decode_str(value):
    decoded_bytes, encoding = decode_header(value)[0]
    if isinstance(decoded_bytes, bytes):
        return decoded_bytes.decode(encoding if encoding else 'utf-8')
    return decoded_bytes

# Save attachments to the local folder
def save_attachments(msg, output_dir):
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if filename:
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            print(f"Attachment saved: {filepath}")

# Connect to the email server and fetch emails
def download_emails(username, password, imap_server, output_dir):
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select("inbox")  # Select inbox folder

        # Search emails
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        print(f"Total emails: {len(email_ids)}")
        os.makedirs(output_dir, exist_ok=True)

        # Loop through all emails
        for i, email_id in enumerate(email_ids, start=1):
            res, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_str(msg["Subject"])
                    sender = decode_str(msg.get("From"))

                    print(f"\nDownloading email {i}/{len(email_ids)}")
                    print(f"Subject: {subject}")
                    print(f"From: {sender}")

                    # Save email content
                    email_file = os.path.join(output_dir, f"email_{i}.eml")
                    with open(email_file, "w", encoding="utf-8") as f:
                        f.write(msg.as_string())
                    print(f"Email saved: {email_file}")

                    # Save attachments
                    save_attachments(msg, output_dir)

        # Close connection
        mail.logout()
        print("Emails downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Configuration
if __name__ == "__main__":
    # User credentials
    USERNAME = "rampanda.2597@gmail.com"
    PASSWORD = "RAMnarayan@1234"

    # IMAP server for your email provider
    IMAP_SERVER = "imap.gmail.com"  # Example: Gmail IMAP server
    OUTPUT_DIR = "emails"  # Directory to save emails and attachments

    # Call the function to download emails
    download_emails(USERNAME, PASSWORD, IMAP_SERVER, OUTPUT_DIR)
