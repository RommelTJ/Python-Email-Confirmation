#!/usr/local/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cx_Oracle, sys
import argparse

####################################################
# File: frosh_advising_email_confirmation.py       #
# Author: Rommel Rico                              #
# Last Modified: 01/Apr/2013                       #
# Description: This script is passed a Banner ID,  #
#              locates the email address from it,  #
#              and sends email confirmation.       #
####################################################

#GLOBAL VARIABLES
CONNSTR = '<USER>/<PASS>@sgproddb:<PORT>/<SID>'
CON = cx_Oracle.connect(CONNSTR)
CURSOR = CON.cursor()

#Main function
def main():
    #Get Banner ID from command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="Banner ID of person to send notification.")
    args = parser.parse_args()
    #Get email from Banner ID through the GOREMAL table.
    email = get_email(args.id)
    CON.close()
    #Send email to recipient.
    send_mail(email)

#Get the email address.
def get_email(spriden_ID):
    pidm = get_pidm(spriden_ID)
    CURSOR.execute("select * from GOREMAL where goremal_pidm='"+pidm+"' and GOREMAL_PREFERRED_IND='Y'")
    user_email = str(CURSOR.fetchone()[2])
    return user_email

#Get the User PIDM
def get_pidm(spriden_ID):
    CURSOR.execute("select * from SPRIDEN where SPRIDEN_ID='"+spriden_ID+"'")
    user_pidm = str(CURSOR.fetchone()[0])
    return user_pidm

def send_mail(recipient):
    me  = "<Email address>" # Sender's email address
    you = recipient                 # Recipient's email address    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Freshman Advising Questionnaire"
    msg['From'] = me
    msg['To'] = you

   # Create the body of the message (a plain-text and an HTML version).
    text = """        ----------------------------------------------\n        You have successfully submitted your Freshman Advising Questionnaire. USD's team of faculty advisors will use this information to prepare your schedule of classes in order of submission date. Schedules will not be finalized until July 12 at 5pm, at this time, they will be viewable on the MySanDiego Portal.\n        In the interim, if you have any questions you may visit the Freshman Registration website: http://www.sandiego.edu/freshreg.\n\n
        Welcome to the University of San Diego!\n
        ----------------------------------------------\n
    """
    html = """
        <html>
        <head><title>Freshman Advising Questionnaire</title></head>
        <body>        <p>----------------------------------------------<br />        You have successfully submitted your Freshman Advising  Questionnaire. USD's team of faculty  advisors will use this information to prepare your schedule of classes in order  of submission date. <strong>Schedules will not be finalized until July 12 at 5pm, at this time,  they will be viewable on the MySanDiego Portal.</strong> <br />        In the interim, if you have any questions you may visit the  Freshman Registration website: <a href="http://www.sandiego.edu/freshreg">http://www.sandiego.edu/freshreg</a>.<br />
        <br />
        Welcome to the University of San Diego!<br />
        ----------------------------------------------</p>
        </body>
        </html>
    """
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container. According to RFC 2046, the last part of 
    # a multipart message, in this case the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via our SMTP server.
    s = smtplib.SMTP('smtp.<SERVER HOST NAME>')
    # sendmail function takes 3 arguments: sender's address, recipient's address, and message to send.
    s.sendmail(me, you, msg.as_string())
    s.quit()

#Launch program.
if __name__ == "__main__":
    main()
                                             

