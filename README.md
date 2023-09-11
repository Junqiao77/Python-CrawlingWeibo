# Python-Crawling Weibo
用python爬取微博帖子的详细内容和信息，获取Ajax动态页面内容和结果

### 导入相应的库
```
import requests
import csv
from urllib.parse import urlencode
import time
from requests.exceptions import RequestException
```

### 确定对应的网址，设定请求头
```
# 观察微博网址的url发现相同的网址构造
base_url = 'https://weibo.com/ajax/statuses/mymblog?'
# cookie记得及时更新，不更新不会爬取成功
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.78 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'cookie':r'XSRF-TOKEN=D9RqbLD0pv17obo78BgBDH6r; login_sid_t=0ac2d1ce9e79cad260a66a9687ebd628; cross_origin_proto=SSL; _s_tentry=weibo.com; Apache=5738730368049.107.1682048142847; SINAGLOBAL=5738730368049.107.1682048142847; ULV=1682048142851:1:1:1:5738730368049.107.1682048142847:; wb_view_log=2560*14401; appkey=; WBtopGlobal_register_version=2023042111; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFU70eLSR0lofj0MT5rijkd5JpX5o275NHD95QcSoBc1he0e0npWs4Dqcjci--fi-i8iKn7i--fiK.7iKy8i--Xi-zRiKy2i--fiKnciKy2i--ciKn4iK.0i--ciKn4i-z7; SSOLoginState=1682048385; SUB=_2A25JRnXRDeRhGeBI71QZ8y3Pwz2IHXVqMuAZrDV8PUNbmtANLU7akW9NRpOyYWmToe7F6Fdz97b9Q9cHb6mQAr8V; ALF=1713584384; WBPSESS=YnGmI0xRXPJAIeboDANzVo6Lt9HOEuzmcOP2fMt9ZhMStZ2btEDGqPj_KCCJepadRmRcbdwITpBkOKO9cYVyBeOTX_SGxFN6-B5_3OPJLGdU3hnNJiPVxHemcsjdCkrBRCMK6f-PdLqBVLAJPHQZjg=='
           }
# 根据需要的数据量设定爬取的最大的页面数量
max_page = 10
```
