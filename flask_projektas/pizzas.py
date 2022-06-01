import requests
from pizzas_api import api_key

url = "https://pizza-and-desserts.p.rapidapi.com/pizzas"

headers = {
    'x-rapidapi-host': "pizza-and-desserts.p.rapidapi.com",
    'x-rapidapi-key': api_key
    }

response = requests.request("GET", url, headers=headers).text
#print(response)