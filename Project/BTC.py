import json
import optparse
import os
from threading import local
import requests
from xhtml2pdf import pisa
from datetime import datetime
import yagmail
import ftplib
from dotenv import load_dotenv

def main():
    try:
        price, name, history, percentage = apiRequest()
        data = htmlDocument(name, price, history, percentage)
        name = convertHTMLtoPDF(data)
        sendMail(name)
        sendFTP(name)
        log("-------------------------------")
    except:
        log("Error accured")
        log("-------------------------------")

load_dotenv()
MAIL = os.getenv('mail')
PASSWORD = os.getenv('app_password')
BPLACED_USERNAME = os.getenv('bplaced_username')
BPLACED_PASSWORD = os.getenv('bplaced_password')


def apiRequest():
    nowRequest = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=CHF").json()
    historyRequest = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=CHF&days=7&interval=daily").json()
    price = nowRequest["bitcoin"]["chf"]
    name = "Bitcoin"
    history = int(historyRequest["prices"][0][1])
    percentage = (price - history) / history * 100
    log("API Request successful")
    return str(price), str(name), str(history), percentage


def htmlDocument(name, price, history, percentage):
    percentage = str((round(percentage, 2))) + "%"
    htmlData = [name, price, history, percentage ]

    with open('./index.html', 'r') as file :
        filedata = file.read()

    for i in range(len(htmlData)):
        filedata = filedata.replace('[', htmlData[i], 1)
         
    with open('./mail.html', 'w') as file:
        file.write(filedata)
    log("Generated HTML File")
    return filedata

def convertHTMLtoPDF(sourceHtml):
    localDate = str(datetime.now()).split(" ")
    name = "./Report-{}.pdf".format(localDate[0])
    resultFile = open(name, "w+b")

    pisa.CreatePDF(
        sourceHtml,                
        dest=resultFile)           
    resultFile.close()

    log("HTML File converted to PDF")
   
    return name

def sendMail(name):
    to = 'stefan.laux007@icloud.com'

    subject = 'Bitcoin report'
    content = ['Here is your weekly report!!', name]

    with yagmail.SMTP(MAIL, PASSWORD) as yag:
        yag.send(to, subject, content)
    log("Mail send successful")
    
def sendFTP(name):
    session = ftplib.FTP('stefanlaux.bplaced.net', BPLACED_USERNAME, BPLACED_PASSWORD)
    file = open(name,'rb')                  
    session.storbinary('STOR {}'.format(name), file)     
    file.close()                                
    session.quit()
    log("FTP Sucessfully uploaded")

def log(message):
    localdate = str(datetime.now()).split(" ")
    localdate = "[{}] ".format(localdate[0])
    file = open("log.txt", "a")
    file.write("{} {}\n".format(localdate, message))

        

main()