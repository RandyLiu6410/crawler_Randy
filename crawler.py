import os
os.getcwd()

import pandas as pd
import numpy as np

df = pd.read_csv('hw1-3/data/野村客服.csv')
df.drop('Unnamed: 0', axis = 1, inplace = True)

#----------------------------------------------------------
"""
import jieba
from langconv import Converter

df_descp = pd.DataFrame()
for i in df['Unique ID'].value_counts().index:
    for j in df[df['Unique ID'] == i].reset_index().index :
        trad_descp = df[df['Unique ID'] == i].reset_index().at[j, '客戶事件描述']
        simp_descp = Converter('zh-hans').convert(trad_descp)
        text = jieba.cut(simp_descp, cut_all=True)
        df_descp.at[i, j] = Converter('zh-hant').convert("/ ".join(text))

df_descp.to_csv(path_or_buf='~/Desktop/Randy/Fintech/Result.csv')

stopWords = []
with open('hw1-3/data/stopWords.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)

error_lst = []
terms=[]
for i in range(len(df['客戶事件描述'])):
    try:
        for j in list(jieba.cut(df['客戶事件描述'][i], cut_all = False)):
            if j not in stopWords:
                terms.append(j)
    except:
        error_lst.append([i, df['客戶事件描述'][i]])

#-----------------------------------------------------------

from wordcloud import WordCloud
from matplotlib import pyplot as plt
from collections import Counter

wc = WordCloud(background_color = "white", width = 1440, 
                height = 900, margin= 2, font_path= "/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc")

wc.generate_from_frequencies(Counter(terms))
plt.figure(figsize = (10, 10))
plt.imshow(wc)
plt.axis("off")
plt.savefig('Result.png')
"""

#-----------------------------------------------------------

from bs4 import BeautifulSoup as bs
import requests
import jieba
from langconv import Converter

def yahoo(url):
	res = requests.get(url)
	doc = bs(res.text,"lxml")
	try:
		news_content = doc.find_all('article',itemprop="articleBody")
		paras = news_content[0].find_all('p')
		content = ""
		for item in paras:
			content = content + item.get_text()
		return content
	except:
		return ""

'''
# 下載 Yahoo 首頁內容
r = requests.get('https://tw.yahoo.com/')

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 程式碼
  soup = bs(r.text, 'html.parser')

  # 以 CSS 的 class 抓出各類頭條新聞
  stories = soup.find_all('a', class_='story-title')
  for s in stories:
    # 新聞標題
    print("標題：" + s.text)
    # 新聞網址
    print("網址：" + s.get('href'))
'''

def anue_stories(url):

    # 鉅亨網 搜尋 URL
    anue_url = url
    anue = requests.get(anue_url)

    # 確認是否下載成功
    if anue.status_code == requests.codes.ok:
        soup = bs(anue.text, 'html.parser')

    # 以 CSS 的 class 抓出各類頭條新聞
    stories = soup.find_all('a', class_='jsx-2489854855')
    for s in stories:
        # 新聞標題
        print("標題：" + s.text)
        # 新聞網址
        print("網址：" + s.get('href'))

    return stories

stories = anue_stories('https://www.cnyes.com')

def anue_get(stories):
   for s in stories:
       link = requests.get(s.get('href'))

       if link.status_code == requests.codes.ok:
         soup = bs(link.text, 'html.parser')

       title = soup.find('h1')
       print(title.text)
       for words in soup.find_all('p'):
           if words.find('a'):
               continue
           print(words)

#anue_get(stories)


import random
import urllib.request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
def down_pic(url, path):
    try:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read()
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
    except Exception as e:
        print(str(e))

def download_image(url):
    name = random.randrange(1,100)
    fullname = str(name)+".jpg"
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')]
    urllib.request.install_opener(opener)
    down_pic(url, fullname)  

def av_stories(url):

    # 鉅亨網 搜尋 URL
    anue_url = url
    anue = requests.get(anue_url)

    # 確認是否下載成功
    if anue.status_code == requests.codes.ok:
        soup = bs(anue.text, 'html.parser')

    # 以 CSS 的 class 抓出各類頭條新聞
    stories = soup.find_all('img', class_='content_img')
    #print(stories)
    for s in stories:
        # 新聞標題
        #print("標題：" + s.text)
        # 新聞網址
        print("網址：" + s.get('src'))
        download_image(s.get('src'))

    return stories

stories = av_stories('https://www.meitulu.com/item/13025.html')
#stories = av_stories('http://easywinbooks198.pixnet.net/blog/post/213960792-%E9%9B%9E%E6%8E%92%E5%A6%B9%E9%84%AD%E5%AE%B6%E7%B4%942018%E6%9C%80%E6%96%B0%E5%AF%AB%E7%9C%9F-%5B%E5%A4%9A%E5%9C%96%5D-%E5%B0%BA%E5%BA%A6%E6%9B%B4%E8%A7%A3%E6%94%BE~')
#stories = av_stories('https://www.chinatimes.com/cn/realtimenews/20181212005057-260404?chdtv')

def av_get(stories):
    for s in stories:
       link = requests.get(s.get('href'))

       if link.status_code == requests.codes.ok:
         soup = bs(link.text, 'html.parser')

       title = soup.find('h1')
       print(title.text)
       for words in soup.find_all('p'):
           if words.find('a'):
               continue
           print(words)
 
#download_image("https://mtl.ttsqgs.com/images/img/13025/1.jpg")