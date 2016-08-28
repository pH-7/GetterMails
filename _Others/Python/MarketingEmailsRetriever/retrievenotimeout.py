#TO USE:
# Go here http://www.appszoom.com/android_games/by_new
# and any app you see, enter the URL into the apppackages.txt list
# the output is the emails of the apps

import os
from lxml import html
import requests
import feedparser

__location__ = os.path.dirname(__file__)
emailList = []
linkList = []

def scrapePageAndAddPackage(url, returnList):
    newUrl = url.split(".html")[0] + "-download.html"
    page = requests.get(newUrl)
    tree = html.fromstring(page.text)
    packageString = str(tree.xpath('//span[@class="package"]/text()'))[:-2]
    print "Package: " + packageString.split()[1]
    package = packageString.split()[1]
    returnList.append(package)

def readLinkList():

    returnList = []
    for url in linkList:
        try:
            scrapePageAndAddPackage(url, returnList)
        except:
            print "Timeout, trying that page one more time..."
            try:
                scrapePageAndAddPackage(url, returnList)
                print "Worked that time :)"
            except:
                print "Another timeout, moving on..."

    return returnList

    # text_file = open(os.path.join(__location__, "apppackages.txt"));
    # urlList = text_file.readlines()
    #
    # returnList = []
    # for url in urlList:
    #     newUrl = url.split(".html")[0] + "-download.html"
    #     page = requests.get(newUrl)
    #     tree = html.fromstring(page.text)
    #     packageString = str(tree.xpath('//span[@class="package"]/text()'))[:-2]
    #     package = packageString.split()[1]
    #     returnList.append(package)
    #
    # print returnList 
    # return returnList


def writeFile():
    writeFile = open("OutputEmails.txt", "w")
    for email in emailList:
        writeFile.write("%s\n" % email)
    writeFile.close()

print "Retrieving..."

rssFeed1 = feedparser.parse('http://www.appszoom.com/android_games/by_new?rss=') # 80 new emails every 7 hours (next at 9pm)
rssFeed2 = feedparser.parse('http://www.appszoom.com/android_applications/by_new?rss=') # 80 new emails every 4 hours
#for each rss entry, get link and add to link list
for index in range(len(rssFeed1['entries'])):
    link = rssFeed1['entries'][index]['link']
    parsedLink = link.split(".html")[0]
    linkList.append(parsedLink)
#for each rss entry, get link and add to link list
for index in range(len(rssFeed2['entries'])):
    link = rssFeed2['entries'][index]['link']
    parsedLink = link.split(".html")[0]
    linkList.append(parsedLink)

finalLinkList = readLinkList()

for package in finalLinkList:
    page = requests.get("https://play.google.com/store/apps/details?id=" + package)
    tree = html.fromstring(page.text)
    links = tree.xpath('//a[@class="dev-link"]/text()')

    for link in links:
        if "Email" in link:
            emailList.append(link.strip().split()[1])

emailList = list(set(emailList))
writeFile()




#  FOR USE FOR AN INPUT OF JUST PACKAGES, NOT THE APPSZOOM LINK

# import os
# from lxml import html
# import requests
#
# __location__ = os.path.dirname(__file__)
# newPackageList = []
# emailList = []
#
# def readPackageList():
#     text_file = open(os.path.join(__location__, "apppackages.txt"));
#     return text_file.readlines()
#
# def writeFile():
#     writeFile = open("OutputEmails.txt", "w")
#     for email in emailList:
#         writeFile.write("%s\n" % email)
#     writeFile.close()
#
#
# packageList = readPackageList()
# for package in packageList:
#     newPackageList.append(package.replace("\n", ""))
#
# for package in newPackageList:
#     page = requests.get("https://play.google.com/store/apps/details?id=" + package)
#     tree = html.fromstring(page.text)
#     links = tree.xpath('//a[@class="dev-link"]/text()')
#
#     for link in links:
#         if "Email" in link:
#             emailList.append(link.strip().split()[1])
#
# writeFile()