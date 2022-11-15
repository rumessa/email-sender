import os
import sys
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# get email addresses from text file
def getEmailAddresses():
    filename = "emailAddress.txt"
    emails= []
    with open(os.path.join(sys.path[0],filename), mode='r', encoding='utf-8') as file:
        for address in file:
            emails.append(address.split()[0])     # gets rid of \n at end of the line
    return emails

# read the body of the email from text file
def readMessage():
    filename = "email.txt"
    with open(os.path.join(sys.path[0],filename), 'r', encoding='utf-8') as file:
        emailBody = file.read()
    return Template(emailBody)

# getting my CV pdf
def getPDF():
    # attaching my CV
    pdfname = 'CV.pdf'
 
    # open the file in binary
    binary_pdf = open(os.path.join(sys.path[0],pdfname), 'rb')
    
    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload((binary_pdf).read())
    
    # enconding the binary into base64
    encoders.encode_base64(payload)
    
    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    return payload

# set up the SMTP server
s = smtplib.SMTP(host='smtp.gmail.com', port=587)     # create SMTP instance for gmail
s.starttls()
myEmail = 'email@gmail.com'
myPassword = 'password123'
s.login(myEmail, myPassword)

emails = getEmailAddresses()    # get list of email addresses
emailBody = readMessage()       # get the email body
payload = getPDF()              # get my CV

# send the email to the email addresses one by one
for emailAddress in emails:
    msg = MIMEMultipart()       # create a message object

    # add in the person name to the email body (not really neccassary here)
    message = emailBody.substitute(PERSON_NAME='Hocam')

    # setup the basics of the email
    msg['From']= myPassword
    msg['To']= emailAddress
    msg['Subject']= "Summer Internship 2021"

    # add in the body as plaintext and attach the CV pdf
    msg.attach(MIMEText(message, 'plain'))     
    msg.attach(payload)

    s.send_message(msg)   # send the message via the server set up earlier
    
    del msg               # delete this one so we have new one for next itertion
