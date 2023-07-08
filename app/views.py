import os
from flask import render_template, request, jsonify
from app import app
from bs4 import BeautifulSoup
import jieba
from wordcloud import wordcloud
import requests
from urllib3.exceptions import InsecureRequestWarning


@app.route('/')
def index():
    # 获取一周口碑榜数据
    movie_list = get_weekly_movies()
    return render_template('index.html', movie_list=movie_list)


@app.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
    if request.method == 'POST':
        # 处理POST请求，获取评论数据
        get_review_data(movie_id)
        return 0
    else:
        # 处理GET请求，获取电影详细信息
        movie_info = get_movie_info(movie_id)
        return render_template('movie_details.html', movie_info=movie_info)


# 豆瓣网址
def getHTMLText(url):
    try:
        kv = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 获取豆瓣一周口碑榜电影
def get_weekly_movies():
    url = "https://movie.douban.com"
    soup = BeautifulSoup(getHTMLText(url), 'html.parser')
    r_div = soup.find(attrs={'class': 'billboard-bd'})
    trs = r_div.find_all('tr')
    # 解析电影信息
    movie_list = []
    for tr in trs:
        for link in tr.select("a"):
            url = link["href"]
            soup = BeautifulSoup(getHTMLText(url), 'html.parser')
            movie = {}
            title_element = soup.find("span", property="v:itemreviewed")
            if title_element:
                movie['title'] = title_element.text
            else:
                movie['title'] = '未知标题'
            movie['id'] = url.split('/')[-2]
            img_element = soup.find("img", rel="v:image")
            if img_element is not None:
                movie['cover'] = img_element['src']
                if not os.path.exists(
                        '绝对路径\pythonProject18\\app\\static\\pictures\\' + movie[
                            'id'] + '.jpg'):
                    # 文件不存在，下载图片
                    response = requests.get(movie['cover'])
                    with open(
                            '绝对路径\pythonProject18\\app\\static\\pictures\\' + movie[
                                'id'] + '.jpg', 'wb') as f:
                        f.write(response.content)
                else:
                    pass
            else:
                movie['cover'] = None
            movie_list.append(movie)

    return movie_list

# 获取电影详细信息
def get_movie_info(movie_id):
    url = f"https://movie.douban.com/subject/{movie_id}/"
    soup = BeautifulSoup(getHTMLText(url), 'html.parser')
    movie_info = {}
    title_element = soup.find("span", property="v:itemreviewed")
    if title_element:
        movie_info['title'] = title_element.text
    else:
        movie_info['title'] = '未知标题'
    movie_info['id'] = url.split('/')[-2]
    # 饼图数据
    r_list = soup.find('div', class_='ratings-on-weight')
    data_a = []
    for div in r_list.select("div", class_='item'):
        for span in div.select("span", class_='rating_per'):
            data_a.append(span.text)
    data_b = []
    for i in range(1, 10, 2):
        data_b.append(data_a[i])
    movie_info['rate'] = [float(x.strip('%')) for x in data_b]

    return movie_info

# 获取评论数据
def get_review_data(movie_id):
    url = f"https://movie.douban.com/subject/{movie_id}/"
    # 禁用 SSL 证书验证警告
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    level = ['h', 'm', 'l']
    for item in level:
        # 前二十条消息
        url1 = url + "comments?percent_type=" + item + "&limit=20&status=P&sort=new_score"
        header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
        resp = requests.get(url=url1, headers=header, verify=False)
        soup = BeautifulSoup(resp.content, 'html.parser')
        r_list = soup.find('div', class_='mod-bd')
        a = []
        teststr1 = ''
        for p in r_list.select("p", class_='comment-content'):
            for span in p.select("span", class_='short'):
                a.append(span.text)
        for i in a:
            teststr1 += i

        teststr = ''
        for i in range(20, 201, 20):
            url2 = url + "comments?percent_type=" + item + "&start=" + str(i) + "&limit=20&status=P&sort=new_score"
            header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
            resp = requests.get(url=url2, headers=header)
            soup = BeautifulSoup(resp.content, 'html.parser')
            r_list = soup.find('div', class_='mod-bd')
            a = []
            for p in r_list.select("p", class_='comment-content'):
                for span in p.select("span", class_='short'):
                    a.append(span.text)
            for i in a:
                teststr += i
        teststr3 = teststr1 + teststr
        print(teststr3)
        ls = jieba.lcut(teststr3)  # 生成分词列表
        text = ' '.join(ls)  # 连接成字符串
        stopwords = ["的", "是", "了", "我", "自己", "和", "也", "不", "在", "都", "有", "很", "更", "又", "以为", "并",
                     "与", "但", "中", "会", "就", "上", "非常", "吧", "啊"]
        wc = wordcloud.WordCloud(font_path="msyh.ttc",
                                 width=1000,
                                 height=700,
                                 background_color='white',
                                 max_words=100, stopwords=stopwords)
        wc.generate(text)
        filename = '绝对路径\\pythonProject18\\app\\static\\pictures\\' + str(
            movie_id) + item + "worldcloud" + ".png"
        wc.to_file(filename)  # 保存词云文件

    return 0

