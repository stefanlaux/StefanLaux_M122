import json
import optparse
import os
from threading import local
import requests
from xhtml2pdf import pisa
from datetime import datetime
from decouple import config
import yagmail
import ftplib



def main():
    price, name, history, percentage = apiRequest()
    data = htmlDocument(name, price, history, percentage)
    name = convertHTMLtoPDF(data)
    sendMail(name)
    sendFTP(name)
    


def apiRequest():
    nowRequest = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=CHF").json()
    historyRequest = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=CHF&days=7&interval=daily").json()
    price = nowRequest["bitcoin"]["chf"]
    name = "Bitcoin"
    history = int(historyRequest["prices"][0][1])
    percentage = (price - history) / history * 100
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
    return filedata

def convertHTMLtoPDF(sourceHtml):
    localDate = str(datetime.now()).split(" ")
    name = "./Report-{}.pdf".format(localDate[0])
    resultFile = open(name, "w+b")

    pisa.CreatePDF(
        sourceHtml,                
        dest=resultFile)           

    resultFile.close()
   
    return name

def sendMail(name):
    user = config('mail')
    app_password = config('app_password')
    to = 'stefan.laux007@icloud.com'

    subject = 'Bitcoin report'
    content = ['Here is your weekly report!!', name]

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
    
def sendFTP(name):
    session = ftplib.FTP('stefanlaux.bplaced.net', config('bplaced_username'), config('bplaced_password'))
    file = open(name,'rb')                  
    session.storbinary('STOR {}'.format(name), file)     
    file.close()                                
    session.quit()
        

main()