import jieba  # 分词
import jieba.analyse  # 分词
# from jieba import analyse
from matplotlib import pylab as plt     # 绘图，数据可视化
from wordcloud import WordCloud         # 词云
from PIL import Image                   # 图片处理
import numpy as np                      # 矩阵运算
from pymysql import *
from wordcloud import WordCloud, STOPWORDS
import nltk

from nltk.corpus import stopwords
import json
# wordCloud
jieba.analyse.set_stop_words("stopwords.txt")

def stopwordslist():
    stopwords = [line.strip() for line in open(r'stopwords.txt',encoding='UTF-8').readlines()]
    return stopwords

# 所有词
def get_img(field,targetImgSrc,resImgSrc):
    con = connect(host='localhost', user='root', password='123456', database='bstation', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select {field} from jobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i,item in enumerate(data):
        text += item[0]
    cursor.close()
    con.close()



    # # 分词   原始

    cut = jieba.cut(text)
    string = ' '.join(cut)
    # # 去除停用词
    # # final_list = []
    # for word in cut:
    #     if word not in jieba.analyse.get_stop_words():
    #         string.append(word)

    print(string)

    # 图片
    img = Image.open(targetImgSrc)  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 显示生成的词语图片
    # plt.show()

    # 输入词语图片到文件
    plt.savefig(resImgSrc, dpi=500)

def getTitleCloudWord(targetImgSrc,resImgSrc):
    con = connect(host='localhost', user='root', password='123456', database='bstation', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select content from videocomments"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i, item in enumerate(data):
                text = text + item[0]
    cursor.close()
    con.close()

    # 分词

    cut = jieba.cut(text)
    string = ' '.join(cut)
    # 去除停用词
    # string = []
    # for word in cut:
    #     if word not in jieba.analyse.get_stop_words():
    #         string.append(word)
    print(string)

    # 图片
    img = Image.open(targetImgSrc)  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 显示生成的词语图片
    # plt.show()

    # 输入词语图片到文件
    plt.savefig(resImgSrc, dpi=500)

getTitleCloudWord(r'.\static\1.jpg',r'.\static\title_cloud.png')
# getTitleCloudWord(r'.\static\2.jpg',r'.\static\comment_content_cloud.png')
# get_img('companyTitle',r'.\static\2.jpg',r'.\static\companyTitle.jpg')
# get_img('summary',r'.\static\2.jpg',r'.\static\summary_cloud.jpg')
# get_img('casts',r'.\static\3.jpg',r'.\static\casts_cloud.jpg')

