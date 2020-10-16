import requests
from bs4 import BeautifulSoup
def get_html(url):
    try:
        # 访问来源伪装
        header_reset = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=header_reset)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        source = r.text
    except:
        source = "访问失败"
    return source
