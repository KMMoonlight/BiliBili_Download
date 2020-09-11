import time
import home
import utils


def download_video_whole(url, title, bvid):
    header = {
        "User-Agent": utils.common_headers,
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Accept-Encoding": "identity",
        "Accept": "*/*",
        "Referer": "https://www.bilibili.com/video/" + bvid,
        "Host": "upos-sz-mirrorcos.bilivideo.com"
    }
    #success = save(title, url, header)
    # if success:
    #     print("休息30s 继续")
    #     time.sleep(30)
    # return success


def download_video_for_peer(url, title, bvid, size):
    page = int(size / (1024 * 1024 * 4))
    peer = int(size / page)
    result = []
    for i in range(page):
        if i == 0:
            start = "0"
        else:
            start = str(i * peer + 1)

        if i == (page - 1):
            end = str(size)
        else:
            end = str((i + 1) * peer)

        header = {
            "User-Agent": utils.common_headers,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Accept-Encoding": "identity",
            "Accept": "*/*",
            "Referer": "https://www.bilibili.com/video/" + bvid,
            "Range": "bytes=" + start + "-" + end,
        }
        success = save(title, url, header, (i+1), result)
        if success == False:
            return success
    for data in result:
        with open('./video/' + title + "/" + title + ".flv", 'ab') as f:
            f.write(data)
    print(title + "---视频组合完成")
    return True


def save(title, url, header, peer, result):
    print("开始下载视频---" + title + "第" + str(peer) + "片")
    try:
        r = home.my_session.get(url, headers=header, stream=True, cookies=utils.common_cookies)
        if r.status_code == 200 or r.status_code == 206:
            print("视频下载完成----" + title + "第" + str(peer) + "片")
            result.append(r.content)
            return True
        else:
            print("网络错误")
            print(r.status_code)
            return False
    except Exception as e:
        print("出现问题，尝试低分辨率")
        return False
