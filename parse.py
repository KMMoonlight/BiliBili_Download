import home
import utils
import biliDownload

cid_url = 'https://api.bilibili.com/x/web-interface/view?aid='
video_url = 'https://api.bilibili.com/x/player/playurl?avid='
header = {
    "User-Agent": utils.common_headers
}


def get_video_cid(aid, title, bvid):
    r = home.my_session.get(cid_url+aid, headers=header)
    if r.status_code == 200:
        cid = r.json()['data']['cid']
        video_download_address, size = get_video_url(aid, cid, "112")
        success = biliDownload.download_video_for_peer(video_download_address, title, bvid, size)
        #success = biliDownload.download_video_whole(video_download_address, title, bvid)
        if not success:
            video_download_address, size = get_video_url(aid, cid, "80")
            success = biliDownload.download_video_for_peer(video_download_address, title, bvid, size)
            #success = biliDownload.download_video_whole(video_download_address, title, bvid)
            if not success:
                video_download_address, size = get_video_url(aid, cid, "64")
                success = biliDownload.download_video_for_peer(video_download_address, title, bvid, size)
                #success = biliDownload.download_video_whole(video_download_address, title, bvid)
                if not success:
                    video_download_address, size = get_video_url(aid, cid, "32")
                    success = biliDownload.download_video_for_peer(video_download_address, title, bvid, size)
                    #success = biliDownload.download_video_whole(video_download_address, title, bvid)
        #biliDownload.download_video_for_peer(video_download_address, title, bvid, size)



def get_video_url(aid, cid, qn):
    r = home.my_session.get(video_url + str(aid) + "&cid=" + str(cid) + "&qn=" + qn + "&otype=json", cookies=utils.common_cookies)
    if r.status_code == 200:
        address = r.json()['data']['durl'][0]['url']
        #qn = r.json()["data"]["accept_quality"][0]
        size = r.json()['data']['durl'][0]['size']
        # params = address.split('.flv')[1]
        # p_address = address.split('.flv')[0]
        # high_address = p_address[0: len(p_address)-2] + str(qn) + ".flv" + params
        return address, size
