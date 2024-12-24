import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Retrieve API data for asset information
assets = ['SOL', "ETH", "BTC", "OP", "ARB"]
API_KEY = os.getenv('API_KEY')
rates = []
new_prices = [assets, rates]
for i in assets:
    url = f'https://rest.coinapi.io/v1/exchangerate/{i}/USD?apikey={API_KEY}'
    response = requests.get(url)
    rate = float(round(response.json()["rate"],2))
    rates.append(rate)

# merge the asset name and their latest prices (new_prices)
merged_list = [(assets[i], new_prices[1][i]) for i in range(0, len(new_prices[1]))]

message_body = ""
for m in merged_list:
    message = (f"The price of {m[0]} at this moment is ${m[1]}.\n\n")
    message_body += message

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=os.getenv('user'), password=os.getenv('password'))
    connection.sendmail(from_addr=os.getenv('user'), to_addrs=os.getenv('to_addrs'),
                        msg=f"Subject: Price Updates\n\n{message_body}")