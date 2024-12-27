import smtplib
from smtplib import SMTP
from email.message import EmailMessage

def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('velpurivennela@gmail.com','nyzd ifqk kbtx ujrb')
    msg=EmailMessage()
    msg['From']='vennela2020220903@gcrjy.ac.in'
    msg['Subject']=subject
    msg['To']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()