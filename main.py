import requests
import time
from dotenv import load_dotenv
from twilio.rest import Client
import os 
load_dotenv()


# STOCK_NAME = "TSLA"
STOCK_NAME = None
COMPANY_NAME = 'apple'
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
STOCK_ENDPOINT = os.getenv("STOCK_ENDPOINT")
NEWS_ENDPOINT = os.getenv("NEWS_ENDPOINT")
NEWS_API_KEY= os.getenv("NEWS_API_KEY")   
TWILIO_SID=os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")
FROM_PHNO = os.getenv("FROM_PHNO ")
TO_PHNO=os.getenv("TO_PHNO")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)




def get_stocks(stock_name,company_name):
    global STOCK_NAME,COMPANY_NAME
    STOCK_NAME = stock_name
    COMPANY_NAME = company_name

    stock_params = {
        'function':"TIME_SERIES_DAILY",
        'symbol' : STOCK_NAME,
        'apikey' : STOCK_API_KEY
    }
    response = requests.get(STOCK_ENDPOINT,params=stock_params)
    data = response.json()["Time Series (Daily)"]
    # data = response.json()

    data_list = [value for (key,value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price =  yesterday_data['4. close']

    day_before_yesterday_data = data_list[1]
    day_before_yesterday_data_closing_price = day_before_yesterday_data['4. close']

    difference = (float(yesterday_closing_price) - float(day_before_yesterday_data_closing_price))
    up_down = None
    if difference > 0 : 
        up_down = "🔺"
    else:
        up_down="🔻"

    diff_percent = round(difference/ float(yesterday_closing_price) * 100 ) 

    if abs(diff_percent) > 1 :
        pass 
            
    print("send!")
    news_params={
        'apiKey':NEWS_API_KEY,
        'q':COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles  = news_response.json()["articles"]



    three_articles = articles[:3]



    "headline :{article title}. \nBrief {article description}"

    formatted_articles  = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline :{article['title']}. \nBrief :{article['description']}" for article in three_articles]

    # print(formatted_articles[0])

    # for article in formatted_articles:
    #     message = client.messages.create(
    #     body= article,
    #     from_=FROM_PHNO,
    #     to=TO_PHNO
    #     )

    return formatted_articles


# stocks = get_stocks("AAPL",'apple')
# print(stocks)

# response = requests.get(STOCK_ENDPOINT,params=stock_params)
# data = response.json()
# print(data)


