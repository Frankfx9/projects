import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Load the CSV file
csv_file = r"C:\Users\PC\Downloads\Untitled spreadsheet - Sheet1.csv"
data = pd.read_csv(csv_file)

# Email account credentials
sender_email = "your_email@gmail.com"
sender_password = "your_appkey@gmail.com"

try:
    # SMTP server setup using SSL on port 465
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(sender_email, sender_password)

    # Loop through each row in the CSV
    for index, row in data.iterrows():
        recipient_email = row['emails']
        first_name = row['Name'].strip()  # Strip any extra spaces from the value

        # Create the MIMEMultipart object# Create the MIMEMultipart object
        message = MIMEMultipart("alternative")
        message["From"] = f"Tobi Franklin <{sender_email}>"  # Set the display name to "Tobi Franklin"
        message["To"] = recipient_email
        message["Subject"] = f"5 more quotes {first_name}? (free)"

 
        # Create the hidden preview text
        preview_text = f"""
        <div style="display: none; max-height: 0px; overflow: hidden;">
            Hey {first_name}. Can you handle 5 more jobs at the right now?
        </div> 
        """

        # Customize your email content with the recipient's first name
        email_body = f"""
        {preview_text}
        <p>Hey {first_name},</p>

        <p>Could you handle another 5 quotes right now?</p>

        <p>I’m Tobi, and I run HueLeads, a digital marketing agency based in Birmingham that helps painters and decorators like you get at least 5 quote-ready leads a month.</p>

        <p>I’ll be straight with you - I’m just starting out, and I’m looking to build up some testimonials. That’s why I’m offering to do all this for free. No strings attached - just to help you out and see if it’s something you’d be interested in.</p>

        <p>Would you be opposed to a quick 15-minute chat? I’ll walk you through the proven strategy, and even if you decide it’s not for you, you can take the plan and run with it.</p>

        <p>Let me know what you think!</p>

        <p>Cheers,<br>Tobi.</p>
        """

        # Attach the email body to the message
        part = MIMEText(email_body, "html")
        message.attach(part)

        try:
            # Attempt to send the email
            smtp_server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email}")
            time.sleep(150)
        except smtplib.SMTPException as e:
            # Handle exceptions and continue
            print(f"Failed to send email to {recipient_email}: {e}")
            time.sleep(150)

finally:
    # Close the SMTP server connection
    try:
        smtp_server.quit()
    except:
        pass


