import mailbox
import os
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import re


def extract_links(html_content):
    """Extract all links from the HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    return [a['href'] for a in soup.find_all('a', href=True)]


def process_mbox(mbox_file, output_dir, missing_idx_file):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the mbox file
    mbox = mailbox.mbox(mbox_file)

    print(f"Processing {len(mbox)} emails...")

    # Initialize lists to store email details
    subject_list = []
    sender_list = []
    date_list = []
    email_body_list = []

    # List to store indices of emails with missing details
    missing_details_idx = []

    for idx, message in enumerate(mbox, start=1):
        # Parse the email message
        msg = BytesParser(policy=policy.default).parsebytes(message.as_bytes())

        # Extract metadata
        subject = msg.get("subject")
        sender = msg.get("from")
        date = msg.get("date")
        parsed_date = parsedate_to_datetime(date) if date else None

        if re.search(
                r"leave|salary\W*slip|form\W*16|payroll|appraisal|performance\W*revi|pay\W*slip|tax\W*document|income\W*details|offer\W*letter|resignation|employment\W*history|personal\W*details|insurance|confidential|private\W*information|onsurity",
                subject.replace("_", ""), flags=re.I) or \
                re.search(r"bharti|greyt|onsurity", sender, flags=re.I):
            continue

        # Extract email body
        email_body = ""
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_type() == "text/plain":
                    email_body += part.get_content()
                elif part.get_content_type() == "text/html":
                    html_content = part.get_content()
                    email_body += BeautifulSoup(html_content, "html.parser").get_text()
        else:
            if msg.get_content_type() == "text/plain":
                email_body = msg.get_content()
            elif msg.get_content_type() == "text/html":
                html_content = msg.get_content()
                email_body += BeautifulSoup(html_content, "html.parser").get_text()

        # Add extracted details to respective lists
        if not subject:
            subject_list.append(idx)
        if not sender:
            sender_list.append(idx)
        if not parsed_date:
            date_list.append(idx)
        if not email_body:
            email_body_list.append(idx)

        # Check for missing details
        if not (subject and sender and date and email_body):
            missing_details_idx.append(idx)

        # Clean subject for file naming
        safe_subject = "".join(c if c.isalnum() else "_" for c in (subject or "No Subject"))[:50]

        # Define file paths
        email_basename = f"{idx:04d}_{safe_subject}"
        email_file = os.path.join(output_dir, f"{email_basename}.txt")

        # Save email content
        with open(email_file, "w", encoding="utf-8") as f:
            f.write(f"Subject: {subject or 'No Subject'}\n")
            f.write(f"From: {sender or 'Unknown Sender'}\n")
            f.write(f"Date: {parsed_date or 'Unknown Date'}\n\n")
            f.write("Email Body:\n")
            f.write(email_body or "No body content found\n")

        print(f"Email saved: {email_file}")

    # Save missing indices to a file
    with open(missing_idx_file, "w") as f:
        for idx in missing_details_idx:
            f.write(f"{idx}\n")
    print(f"Missing details indices saved to {missing_idx_file}")

    return subject_list, sender_list, date_list, email_body_list


if __name__ == "__main__":
    # Path to the mbox file

    # for i in ('/home/rampanda/Documents/DG Assist/data/takeout-20250110T124614Z-001/Takeout/Mail/Inbox.mbox',
    # '/home/rampanda/Documents/DG Assist/data/takeout-20250110T124614Z-001/Takeout/Mail/Sent.mbox'):

    MBOX_FILE = '/home/rampanda/Documents/DG Assist/data/takeout-20250110T124614Z-001/Takeout/Mail/Sent.mbox'

    # Output directory for readable emails
    OUTPUT_DIR = "/home/rampanda/Documents/DG Assist/data/email_trisha_sentbox/"

    # File to store missing indices
    MISSING_IDX_FILE = "/home/rampanda/Documents/DG Assist/data/email data_ram/missing_sent.txt"

    # Process the mbox file
    subject_list, sender_list, date_list, email_body_list = process_mbox(MBOX_FILE, OUTPUT_DIR, MISSING_IDX_FILE)

    # Example: Print the lists
    print("\nSubjects:", subject_list)
    print("\nSenders:", sender_list)
    print("\nDates:", date_list)
    print("\nEmail Bodies:", email_body_list)

