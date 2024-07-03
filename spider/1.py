import csv
import time

import requests
import re
import json
from bs4 import BeautifulSoup
import datetime




def xinxi():
    with open('result.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['Author', 'Description', 'Title', 'Video Review', 'Rank Score', 'Pubdate', 'Favorites', 'Tag', 'Duration',
             'Review', 'Like', 'Share', 'Coin', 'Fans'])

    for i in range(1,2):    #(1,20)

        #获取 "综合热门" 视频
        url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={}'.format(i)

        # 获取 "入站必刷" 视频
        # url = 'https://api.bilibili.com/x/web-interface/popular/precious?page_size=20&pn={}'.format(i)



        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }
        requests.packages.urllib3.disable_warnings()
        h1 = requests.get(url=url, headers=headers, verify=False)


        print(h1.json())
        for resu in h1.json()['data']['list']:
            time.sleep(1)
            author = resu['owner']['name']  # 作者
            url = 'https://www.bilibili.com/video/' + resu['bvid']
            description = resu['desc']  # 简介
            title = resu['title']  # 标题
            video_review = resu['stat']['danmaku']  # 弹幕量
            rank_score = resu['stat']['view']  # 播放量
            pubdate = resu['pubdate']  # 投稿时间,时间戳类型
            favorites = resu['stat']['favorite']  # 收藏量
            tag = resu['tname']  # 分区
            duration = resu['duration']  # 时长
            review = resu['stat']['reply']  # 评论
            h2 = requests.get(url=url, headers=headers, verify=False)
            initial = re.findall('__INITIAL_STATE__=({.*?});', h2.text, re.DOTALL)
            try:
                initial_json = json.loads(initial[0])
                like = initial_json['videoData']['stat']['like']  # 点赞
                share = initial_json['videoData']['stat']['share']  # 转发
                coin = initial_json['videoData']['stat']['coin']  # 转发
                fans = initial_json['upData']['fans']  # 粉丝数
            except:
                continue
            print(author, description, title, video_review, rank_score, pubdate, favorites, tag, duration,
                  review,like,share,coin,fans)



            with open('result.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [author, description, title, video_review, rank_score, pubdate, favorites, tag, duration, review,
                     like, share, coin, fans])




if __name__ == '__main__':
    xinxi()



