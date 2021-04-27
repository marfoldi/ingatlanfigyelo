# -*- coding: utf8 -*-

#You have to allow less secure apps on your gmail account to use smtp:
# https://myaccount.google.com/lesssecureapps
def send_email(sender_name, recipient, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    gmail_user = '<your_gmail_username>'
    gmail_pwd = '<your_gmail_password>'
    FROM = gmail_user+'@gmail.com'
    TO = recipient
    SUBJECT = subject
    TEXT = body
    NAME = sender_name
    
    mail = MIMEText(TEXT.encode('utf-8'), 'html', 'utf-8')
    mail['From']= NAME + " <"+FROM+">"
    mail['To']=TO
    mail['Subject']=Header(SUBJECT, 'utf-8')
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, mail.as_string())
    server.close()
    print('Successfully sent the mail to ' + TO)
