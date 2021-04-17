from urllib.request import HTTPRedirectHandler, build_opener

from config import *


def get_redirected_url(url):
    '''
        获取重定向之后的链接.
        参考https://stackoverflow.com/a/5538568.
    '''
    opener = build_opener(HTTPRedirectHandler)
    opener.addheaders = HEADER
    request = opener.open(url)
    return request.url

if __name__ == '__main__':
    print(get_redirected_url('https://b23.tv/5uhwOb?share_medium=android&share_source=qq&bbid=XYAC60FA0F925954DC2C68F73DD660DC541CC&ts=1618223517906'))
