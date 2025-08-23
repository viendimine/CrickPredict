# News Catcher API API Example
import requests

url = "https://newscatcherapi.com/"
headers = {
    "Content-Type": "application/json"
}

response = requests.get(url)
data = response.json()
print(data)