import os

import requests
import utils
import parse

base_url = "https://api.bilibili.com/x/web-interface/ranking/region?rid=129&day=3&original=0"
my_session = requests.Session()
header = {
    "User-Agent": utils.common_headers
}


def parse_video_list():
    r = my_session.get(base_url, headers=header, cookies=utils.common_cookies)
    r.encoding = 'utf-8'
    if r.status_code == 200:
        rank = r.json()
        for item in rank['data']:
            bvid = item['bvid']
            aid = item['aid']
            title = item['title']
            pic = item['pic']
            if not os.path.exists('./video/' + title):
                os.makedirs('./video/' + title)

            r_img = requests.get(pic, stream=True)
            with open('./video/' + title + '/' + title + "." + pic.split('.')[-1], 'wb') as f:
                f.write(r_img.content)

            # get video detail
            parse.get_video_cid(aid, title, bvid)


if __name__ == "__main__":
    my_session.get("https://www.bilibili.com/", headers=header, cookies=utils.common_cookies)
    parse_video_list()
    #要下载单个视频的话，实际调用下面的方法即可
    #aid = ''
    #bid = ''
    #title = ''
    #if not os.path.exists('./video/' + title):
    #   os.makedirs('./video' + title)
    #parse.get_video_cid(aid, title, bid)
