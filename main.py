import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import os


try:
    Telegram_token = os.environ["SOME_SECRET"]
except KeyError:
    Telegram_token = "Token not available!"

# 6053215161:AAFNSmjcqALqAgSl3Wm6zvjGrkmn6Dc6OqY
bot = telegram.Bot(token=Telegram_token)


def ok(time):
    lst = time.split(" ")
    if len(lst) < 2:
        return True
    if lst[1] == "minutes" or int(lst[0]) <= 4 and lst[1] ==  "hours":
        return False
    return True


async def get_news_data(url_list):
    news_data = []
    for topic in url_list:
        response = requests.get('https://news.google.com'+topic[1:])
        soup = BeautifulSoup(response.text, 'lxml')
        elements = soup.find_all(class_='IBr9hb')
        h_tags = ["h1", "h2", "h3", "h4", 'h5', 'h6']
        for ele in elements[:7]:
            try:
                link = ele.find('a').get('href')
                img_link = ele.find('img')['src']
                text = ele.find(h_tags).get_text().strip()
                time = ele.find('time').get_text()
                if ok(time):
                    continue
                # print(time)
                if link and img_link and text and time:
                    data = {'link': link, 'img_link': img_link, 'text': text, 'time': time}
                    news_data.append(data)
            except Exception as e:
                print(e)
    return news_data


async def get_url(starting_url):
    url = []
    response = requests.get(starting_url)
    soup = BeautifulSoup(response.text, 'lxml')
    elements = soup.find_all(class_='EctEBd')
    for ele in elements[4:]:
        try:
            topic_link = ele.find('a').get('href')
            if topic_link:
                url.append(topic_link)
        except Exception as e:
            print(e)
    return url








async def main():
    url = await get_url('https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en')
    news_data = await get_news_data(url)

    print(news_data)
    for news in news_data:
        msg = "\n"
        text = news['text']
        link = news['link']
        img_src = news['img_link']
        time = news['time']
        msg += '<a href="https://news.google.com' + link[1:] + '">'+ text +'</a>'
        msg += "\n"
        status = await bot.send_message(chat_id="@news_bybot", text=msg, parse_mode='html')
        if status:
            print(status)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
