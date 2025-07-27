import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com/cricket-news/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

news_blocks = soup.select("div.cb-col-100.cb-lst-itm.cb-pos-rel")

news_list = []

for block in news_blocks:
    try:
        title_tag = block.select_one("h2.cb-nws-hdln a")
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        link = "https://www.cricbuzz.com" + title_tag['href'] if title_tag else "No link"

        summary_tag = block.select_one("div.cb-nws-intr")
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary available"

        img_tag = block.find("img")
        img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else "No image available"

        news_list.append({
            "title": title,
            "link": link,
            "summary": summary,
            "image": img_url
        })

    except Exception as e:
        print("Error processing block:", e)

# Print all news
for i, news in enumerate(news_list, start=1):
    print(f"\n📰 News {i}")
    print("Title:  ", news["title"])
    print("Link:   ", news["link"])
    print("Summary:", news["summary"])
    print("Image:  ", news["image"])
