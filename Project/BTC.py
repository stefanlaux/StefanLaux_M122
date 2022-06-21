import json
import optparse
import requests



def main():
    price, name, history, percentage = apiRequest()
    htmlDocument(name, price, history, percentage)    


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

    with open('./Project/index.txt', 'r') as file :
        filedata = file.read()

    for i in range(len(htmlData)):
        filedata = filedata.replace('{', htmlData[i], 1)
        print(htmlData[i])
         
    with open('./Project/mail.html', 'w') as file:
        file.write(filedata)

   
main()