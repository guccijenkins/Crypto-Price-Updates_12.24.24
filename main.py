import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Retrieve API data for asset information
assets = ['SOL', "ETH", "BTC", "OP", "ARB"]
rates = []
new_prices = [assets, rates]
API_KEY = os.getenv('API_KEY')

for i in assets:
    url = f'https://rest.coinapi.io/v1/exchangerate/{i}/USD?apikey={API_KEY}'
    response = requests.get(url)
    rate = float(round(response.json()["rate"],2))
    rates.append(rate)

# merge the asset name and their latest prices (new_prices)
merged_list = [(assets[i], new_prices[1][i]) for i in range(0, len(new_prices[1]))]

# send an email with price updates for assets above
message_body = ""
for m in merged_list:
    message = (f"The price of {m[0]} at this moment is ${m[1]}.\n\n")
    message_body += message

COIN_GECKO_API_KEY = os.getenv('COIN_GECKO_API_KEY')

coin_gecko_url = "https://api.coingecko.com/api/v3/search/trending"
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": COIN_GECKO_API_KEY
}

# /// NFT API ///

response = requests.get(coin_gecko_url, headers=headers)
NFTS = response.json()['nfts']

nft_id = []
nft_symbol = []
for nft in NFTS:
    nft_id.append(nft['id'])
    nft_symbol.append(nft['symbol'])

merged_NFT_list = [(nft_id[i], nft_symbol[i]) for i in range(0, len(nft_id))]

nft_message_body = ""
for m in merged_NFT_list:
    message = (f"The NFT, {m[0]}, is trending at this moment. The symbol for {m[0]} is {m[1]}.\n\n")
    nft_message_body += message

#send an email to user for latest price updates and trending NFTs
with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=os.getenv('user'), password=os.getenv('password'))
    connection.sendmail(from_addr=os.getenv('user'), to_addrs=os.getenv('to_addrs'),
                        msg=f"Subject: Price Updates & Trending NFTs\n\n{"Coin Price Updates\n\n" + message_body + "Trending NFTs\n\n" + nft_message_body}")


