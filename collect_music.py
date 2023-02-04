import requests, bs4
import csv
import re
import time

urls = []
url = "https://entamedata.com/2020/03/25/%e9%9f%b3%e6%a5%bd%e3%82%b7%e3%83%b3%e3%82%b0%e3%83%ab%ef%bd%a5%ef%bd%a5%ef%bd%a5%e6%ad%b4%e4%bb%a3%e5%b9%b4%e9%96%93%e3%81%ab%e3%83%92%e3%83%83%e3%83%88%e3%81%97%e3%81%9fcd%ef%bd%a5%e3%83%ac%e3%82%b3/"
res = requests.get(url)
res.encoding = res.apparent_encoding
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser", from_encoding='utf-8')
elems = soup.select('td a')
i = 0
for elem in elems:
    if i > 32:
        urls.append(elem.get("href"))
    i += 1
for i in range(22):
    del(urls[-1])

print("URL読み込み完了")

info = [[]]
year = 2022
for url in urls:
    time.sleep(1)
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser", from_encoding='utf-8')
    elems = soup.select('td')
    for elem in elems:
        title = ""
        artist = ""
        words = elem.get_text()
        titles = re.findall(r'^.+? ⇒', words)
        artists = re.findall(r'\/ .+? 【発売】',words)
        if len(titles) == 1:
            title = re.sub(r' ⇒','',titles[0])
        if len(artists) == 1:
            artist = re.sub(r'^\/ ','',artists[0])
            artist = re.sub(r' 【発売】$','',artist)
        if title != "" and artist != "":
            info.append([year,title,artist])
    print(year)
    year -= 1

print("合計：",len(info))

filepath = 'music_list.csv'
with open(filepath, 'w', newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(info)

print("書き込みました。")
