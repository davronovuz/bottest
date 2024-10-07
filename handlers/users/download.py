import requests
from loader import dp,bot





# api  download  video  and  send


url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"

payload = { "url": "https://www.tiktok.com/@yeuphimzz/video/7237370304337628442" }
headers = {
	"x-rapidapi-key": "a89071279emsh52d6dfefe773534p1ef94ejsn4a8c42c2ddb2",
	"x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())