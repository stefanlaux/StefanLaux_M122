import json
import requests


def main():
    price, name, history = apiRequest()
    htmlDocument(name, price, history)    


def apiRequest():
    nowRequest = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=CHF").json()
    historyRequest = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=CHF&days=7&interval=daily").json()
    price = nowRequest["bitcoin"]["chf"]
    name = "Bitcoin"
    history = int(historyRequest["prices"][0][1])
    return price, name, history


def htmlDocument(name, price, history):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="./Project/index.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Bitcoin</title>
    </head>
    <body>
        <h1>{}</h1>
        <h4>Price now: {}CHF</h4>
        <h4>7 Days Ago: {}CHF</h4>
    </body>
    </html>
    """.format(name, price, history)
    file = open("index.html", "w")
    file.write(html)
    file.close()

main()