from email.message import EmailMessage
import ssl
import smtplib

from profil import db, Guest

db.connect() 

def send_mail(message,subject):
    """
    Sends an email to all guests from the wedding with the specified subject and message.
    The email will be sent from the "mariageseatingco@gmail.com" account.
    
    :param message: The body of the email that has to be sent
    :type message: StringField 
    :param subject: The subject of the email that has to be sent
    :type subject: StringField
    :param communication_list: The mailing list. The list of email adress to which the email will be sent 
    :type communication_list: List 
    """
    email_sender = 'mariageseatingco@gmail.com'
    email_password = 'xasrtzphtmtiouyr'
    query = Guest.select()
    context = ssl.create_default_context()
    for guest in query:
        email_receiver=guest.email
        em=EmailMessage()
        body = message
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_mail_organisation(message,subject,communication_list):
    """
    Sends an email to the specified email addresses in the communication_list with the specified subject and message.
    The email will be sent from the "mariageseatingco@gmail.com" account.

    :param message: The body of the email that has to be sent
    :type message: StringField 
    :param subject: The subject of the email that has to be sent
    :type subject: StringField
    :param communication_list: The mailing list. The list of email adress to which the email will be sent 
    :type communication_list: List 
    """
    email_sender = 'mariageseatingco@gmail.com'
    email_password = 'jiwkwizanjbcykwq'
    context = ssl.create_default_context()
    for email_receiver in communication_list:
        email = EmailMessage()
        body = message
        email['From'] = email_sender
        email['To'] = email_receiver
        email['Subject'] = subject
        email.set_content(body)        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465 ,context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, email.as_string())


db.close()
