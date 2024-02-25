import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmails(title,body,receiver,filepaths): 
    """
    Sends an Email.

    Args:
        title (str): Title of the email.
        body (str): Body of the email.
        receiver (list): Who to send the Email to.
        filepaths (list): Filepaths of the attachements.

    Returns:
        True if email sent or false if email didnt send.
    """
    message = MIMEMultipart()
    message['From'] = "haijoa3@gmail.com"
    message['to'] = receiver
    message['subject'] = title
    password = 'niux yssb khhn norj'  
    if filepaths == None:
        message.attach(MIMEText(body,'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login("haijoa3@gmail.com", password)
            server.sendmail("haijoa3@gmail.com", receiver, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True