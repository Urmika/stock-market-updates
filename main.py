import os

import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = os.getenv('STOCK_API_KEY')
stock_parameters ={
    "function": "GLOBAL_QUOTE",
    "symbol": STOCK,
    "apikey" : STOCK_API_KEY

}
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
news_parameters = {
    "apiKey" : NEWS_API_KEY,
    "language": "en",
    "q": "Tesla",
    "pageSize": 3
}
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')

TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
MY_NUMBER = os.getenv('MY_NUMBER')


def get_news():
    response = requests.get(url="https://newsapi.org/v2/everything?", params=news_parameters)
    response.raise_for_status()
    data = response.json()
    return data

response = requests.get(url="https://www.alphavantage.co/query?",params=stock_parameters)
response.raise_for_status()
data = response.json()
flux = float(str(data["Global Quote"]["10. change percent"]).strip("%"))

arrow = None
if flux > 0:
    arrow = "🔺"
else:
    arrow = "🔻"
client = Client(account_sid, auth_token)

abs_flux = abs(flux)
if abs_flux >= 2:
    print("Get News")

    response = requests.get(url="https://newsapi.org/v2/everything?", params=news_parameters)
    response.raise_for_status()
    data = response.json()
    articles = data["articles"]
    print(articles)
    formatted_articles = [f"TSLA{arrow}: {round(flux)}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in articles]

    for article in formatted_articles:
        message = client.messages \
                    .create(
                body=article,
                from_= TWILIO_NUMBER,
                to= MY_NUMBER
            )
        print(message.status)
else:
    print("No news")

