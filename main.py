import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "KTSRD32WAINBJ68Y"
stock_parameters ={
    "function": "GLOBAL_QUOTE",
    "symbol": STOCK,
    "apikey" : STOCK_API_KEY

}
NEWS_API_KEY = "127c2977a8f34622989f09c80cddf646"
news_parameters = {
    "apiKey" : NEWS_API_KEY,
    "language": "en",
    "q": "Tesla",
    "pageSize": 3
}
account_sid = "AC833c02b13b1e3b1d6503b56b072e4c97"
auth_token = "eb80f45d1ae43d441a80b8da30ac62b8"

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
    #get_news()
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
            from_='+12054420086',
            to='+918291305179'
        )
        print(message.status)
else:
    print("No news")

