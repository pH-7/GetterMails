If you would like to output just the packages of the apps, change this code:

def writeFile():
    writeFile = open("OutputEmails.txt", "w")
    for email in emailList:
        writeFile.write("%s\n" % email)
    writeFile.close()

to this code:

def writeFile():
    writeFile = open("apppackages.txt", "w")
    for package in finalLinkList:
        writeFile.write("%s\n" % package)
    writeFile.close()


