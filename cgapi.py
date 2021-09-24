import requests
import json


def cryptolist_eur():
    
    api_eur = ''
    #Get the info from api
    api_r_eur = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage='24h'")
    api_eur = json.loads(api_r_eur.content)

    return(api_eur)

def cryptolist_usd():
    
    api_usd = ''
    api_r_usd = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage='24h'")
    api_usd = json.loads(api_r_usd.content)

    return(api_usd)