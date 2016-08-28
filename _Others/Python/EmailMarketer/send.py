#!/usr/bin/python

import smtplib
import sys
import os
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

__location__ = os.path.dirname(__file__)

numberOfEmails = 0
fromAddress = ""
fromAddressPassword = ""
bccAddress = ""
appName = ""
appUrl = ""
isAndroid = True
emailNumber = 1

def readInfo():
    text_file = open(os.path.join(__location__, "Info.txt"));
    info = text_file.readlines()

    #makes it so these assign to the global variables, not new ones
    global numberOfEmails, fromAddress, fromAddressPassword, bccAddress, appName, appUrl, isAndroid, emailNumber

    numberOfEmails = info[0]
    fromAddress = info[1]
    fromAddressPassword = info[2]
    bccAddress = info[3]
    appName = info[4]
    appUrl = info[5]
    isAndroidText = info[6]
    emailNumber = int(info[7])

    if("Y" in isAndroidText.upper()):
        isAndroid = True
    else:
        isAndroid = False

def verify():
    print "Is the following information correct?:\n"
    print "Number of Emails:\t" + numberOfEmails
    print "From Address:\t\t" + fromAddress
    print "From Address PW:\t" + fromAddressPassword
    print "BCC Address:\t\t" + bccAddress
    print "App Name:\t\t" + appName
    print "App URL:\t\t" + appUrl
    print "isAndroid:\t\t" + str(isAndroid)
    print "startingNumber:\t\t" + str(emailNumber)

    answer = raw_input("Y = Yes, N = no\n\n")
    if answer != "Y" and answer != "y":
        print "Exiting..."
        sys.exit()

def readEmailList(isAndroid):
    if isAndroid:
        text_file = open("AndroidEmailList.txt", "r")
    else:
        text_file = open("IphoneEmailList.txt", "r")
    return text_file.readlines()

def readEmailMessageList():
    text_file = open("EmailMessages.txt", "r")
    #the [0::2] makes it skip every other line
    messageList = text_file.readlines()[0::2]
    return messageList

def composeEmailMessage(message, appName, appUrl):
    newMessage = message.replace("[appname]", appName.rstrip())
    return "Hello,\n\n" + newMessage.rstrip() + "\n\nHere is the link to the app:\n" + appUrl + "\nThank you!"


# def sendEmail(fromAddress, toAddress, bccAddress, message):
#     print "from: " + fromAddress + " to: " + toAddress + " bcc: " + bccAddress
#
#     TOADDR = []
#     BCCADDR = []
#     newToAddress = ("\"" + toAddress.strip() + "\" <" + toAddress.strip() + ">").replace('\n', ' ').replace('\r', '')
#     newBccAddress = ("\"" + bccAddress.strip() + "\" <" + bccAddress.strip() + ">").replace('\n', ' ').replace('\r', '')
#     TOADDR.append(newToAddress)
#     BCCADDR.append(newBccAddress)
#
#     # Create message container - the correct MIME type is multipart/alternative.
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = "App News Tip"
#     msg['From'] = fromAddress
#     msg['To'] = ', '.join(TOADDR)
#     msg['Bcc'] = ', '.join(BCCADDR)
#
#     # Record the MIME types of both parts - text/plain and text/html.
#     body = MIMEText(message, 'plain')
#
#     # Attach parts into message container.
#     msg.attach(body)
#
#     # Send the message via local SMTP server.
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     #s.set_debuglevel(1)
#     s.ehlo()
#     s.starttls()
#     username = 'waylonjbrown@gmail.com'
#     password = 'grillbrew2'
#     s.login(username, password)
#     s.sendmail(fromAddress, TOADDR + BCCADDR, msg.as_string())
#     s.quit()

def sendEmail(fromAddress, toAddress, subject, message):
    print "from: " + fromAddress + " to: " + toAddress

    TOADDR = []
    TOADDR.append(toAddress)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = ', '.join(TOADDR)

    # Record the MIME types of both parts - text/plain and text/html.
    body = MIMEText(message, 'plain')

    # Attach parts into message container.
    msg.attach(body)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    username = fromAddress
    password = fromAddressPassword
    s.login(username, password)
    s.sendmail(fromAddress, TOADDR, msg.as_string())
    s.quit()

print "Running..."

#stores info into input parameters
readInfo()
verify()
print "Sending..."

emailList = readEmailList(isAndroid)
emailMessageList = readEmailMessageList()
random.shuffle(emailMessageList)
messageCount = emailNumber

print messageCount

for num in range(0, int(numberOfEmails)):

    finalMessage = composeEmailMessage(emailMessageList[messageCount], appName, appUrl)
    #send first email to app site
    sendEmail(fromAddress, emailList[messageCount], "App News Tip", finalMessage)
    #send second email to user
    sendEmail(fromAddress, bccAddress, "Campaign Email #" + str(messageCount + 1), "This is a message from AppNinja letting you know for your marketing campaign the following message was sent to the email " + emailList[messageCount] + "\n\n" + finalMessage)
    print str(num + 1) + " sent\n"
    messageCount += 1

    #make sending emails more authentic and help with errors from logging in/out too much
    time.sleep(5)

print "\nSuccess!"
