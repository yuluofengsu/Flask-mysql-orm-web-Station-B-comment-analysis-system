# 发送请求
import csv
import re

import requests
# 每次请求停1s，太快会被B站拦截。
import time
requests.packages.urllib3.disable_warnings()
# 请求头
headers = {
    'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-encoding': 'deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'buvid3=2CFB6256-13B3-8651-481C-FE24A7B089B728597infoc; b_nut=1687421228; i-wanna-go-back=-1; b_ut=5; _uuid=9CD4CB9A-1F24-CC1B-5519-ECEF14EC1A9102039infoc; buvid_fp=822f2f65a0c839f4492f8e29fba5a1e1; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; buvid4=957FCF48-FE07-8D8D-360A-B729C4167FDE29781-023062216-7XDfT9HnZ766OgPs88qA25emwji0Atso1KvVJefn7TI%3D; home_feed_column=5; browser_resolution=1920-661; CURRENT_FNVAL=4048; rpdid=0z9ZwfQfjD|1TcD7RC|w2I|3w1QcfmN; LIVE_BUVID=AUTO8516887304406068; CURRENT_BLACKGAP…-channel=1; enable_web_push=DISABLE; sid=4p4vlnf6; SESSDATA=b2a1bda1%2C1730272598%2C2eea0%2A51CjAGSOo0EFMmk_4IPjaRzN6f3o4L-cn9iEhw6vF5ZGq1cSoLpUhRgcUenNrPij8F9e0SVnM0ZFFSeVZJU2ZKakNZUXRuRG9DM24tZ2dTbkNCTkhUX2RwandROXJPVnlpdnpLMHFTNWt4WV9oYWNBczF5bVNOYkhUaHg3ZWs2Y01VcUgtRjBpQ3NRIIEC; bili_jct=a7dbdcf2d3b09373cffb0ddc7680792f; DedeUserID=324173033; DedeUserID__ckMd5=b461d717d4224878; share_source_origin=WEIXIN; b_lsid=D916C72F_18F3D4FDBA7; bsource=search_bing; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com',
    'pragma': 'no-cache',
    # 'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
Cookie = 'buvid3=2CFB6256-13B3-8651-481C-FE24A7B089B728597infoc; b_nut=1687421228; i-wanna-go-back=-1; b_ut=5; _uuid=9CD4CB9A-1F24-CC1B-5519-ECEF14EC1A9102039infoc; buvid_fp=822f2f65a0c839f4492f8e29fba5a1e1; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; buvid4=957FCF48-FE07-8D8D-360A-B729C4167FDE29781-023062216-7XDfT9HnZ766OgPs88qA25emwji0Atso1KvVJefn7TI%3D; home_feed_column=5; browser_resolution=1920-661; CURRENT_FNVAL=4048; rpdid=0z9ZwfQfjD|1TcD7RC|w2I|3w1QcfmN; LIVE_BUVID=AUTO8516887304406068; CURRENT_BLACKGAP…-channel=1; enable_web_push=DISABLE; sid=4p4vlnf6; SESSDATA=b2a1bda1%2C1730272598%2C2eea0%2A51CjAGSOo0EFMmk_4IPjaRzN6f3o4L-cn9iEhw6vF5ZGq1cSoLpUhRgcUenNrPij8F9e0SVnM0ZFFSeVZJU2ZKakNZUXRuRG9DM24tZ2dTbkNCTkhUX2RwandROXJPVnlpdnpLMHFTNWt4WV9oYWNBczF5bVNOYkhUaHg3ZWs2Y01VcUgtRjBpQ3NRIIEC; bili_jct=a7dbdcf2d3b09373cffb0ddc7680792f; DedeUserID=324173033; DedeUserID__ckMd5=b461d717d4224878; share_source_origin=WEIXIN; b_lsid=D916C72F_18F3D4FDBA7; bsource=search_bing; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com'
headers2 = {
    'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-encoding': 'deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie':Cookie.encode('utf-8'),
    'pragma': 'no-cache',
    # 'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
# 发送爬取请求
def spider(url):
    response = requests.get(url, headers=headers2, verify=False)
    response.encoding = 'utf-8'
    return response.json()['data']['replies']


# 获取oid
def get_oid(bvid):
    video_url = 'https://www.bilibili.com/video/' + bvid

    page = requests.get(video_url, headers=headers).text
    aid = re.search(r'"aid":[0-9]+', page).group()[6:]
    return aid


# 时间戳转换成日期
def get_time(ctime):
    timeArray = time.localtime(ctime)
    otherStyleTime = time.strftime("%Y.%m.%d", timeArray)
    return str(otherStyleTime)


# 保存评论
def sava_data(node):
    data_dict = {
        "ID": str(node['rpid']).strip(),
        "用户名": node['member']['uname'].strip(),
        "头像链接": node['member']['avatar'].strip(),
        "评论时间": get_time(node['ctime']),
        "评论内容": node['content']['message'].strip().replace('\n', '')
    }
    global comment_count
    comment_count += 1

    print(f"当前评论数: {comment_count}\n",
          f"ID：{data_dict['ID']}\n",
          f"用户名：{data_dict['用户名']}\n",
          f"头像链接：{data_dict['头像链接']}\n",
          f"评论时间：{data_dict['评论时间']}\n",
          f"评论内容：{data_dict['评论内容']}\n",
          )

    writer.writerow(data_dict)


# 爬取子评论
def getSecondReplies(oid, root):
    # 页数
    page = 1
    # 不知道具体有多少页的评论，所以使用死循环一直爬
    while True:
        url = f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&ps=10&root={root}&_=1647581648753'
        # 爬一次就睡1秒
        time.sleep(1)
        json_data = spider(url)
        # 如果当前页为空（爬到头了），跳出子评论
        if json_data is None:
            break
        elif len(json_data) == 0:
            break

        # 组装数据，存入csv文件中
        for node in json_data:
            sava_data(node)
        # 每爬完一次，页数加1
        page += 1


# 爬取根评论
def getReplies(oid):
    page = 0
    flag = False
    # 不知道具体有多少页的评论，所以使用死循环一直爬
    while True:
        url = f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={page}&type=1&oid={oid}&mode=3&plat=1&_=1647577851745'
        json_data = spider(url)

        # 如果当前页为空（爬到头了），跳出循环，程序结束。
        if json_data is None:
            break
        # elif len(json_data) == 0:
        #     break

        # 组装数据，存入csv文件中。
        for node in json_data:
            print('===================')

            sava_data(node)

            # 如果有子评论，爬取子评论
            if node['replies'] is not None:
                print('>>>>>>>>>')
                getSecondReplies(oid, node['rpid'])
        if flag is True:
            break

        # 每爬完一页，页数加1
        page += 1
        print('================爬取Page{}完毕================'.format(page))


if __name__ == '__main__':
    comment_count = 0

    # 获取视频oid
    Bvid = input('输入视频Bvid:')

    # 向csv文件写入表头
    header = ["ID", "用户名", "头像链接", "评论时间", "评论内容"]
    f = open(f"评论.csv", "w", encoding="utf-8-sig", newline="")
    # f = open(f"{Bvid}_评论.csv", "w", encoding="utf-8-sig", newline="")
    writer = csv.DictWriter(f, header)
    writer.writeheader()

    Oid = get_oid(Bvid)

    getReplies(Oid)
    print('\n================爬取完毕================\n')

