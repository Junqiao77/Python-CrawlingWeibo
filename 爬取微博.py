import requests
import csv
from urllib.parse import urlencode
import time
from requests.exceptions import RequestException

base_url = 'https://weibo.com/ajax/statuses/mymblog?'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.78 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'cookie':r'XSRF-TOKEN=D9RqbLD0pv17obo78BgBDH6r; login_sid_t=0ac2d1ce9e79cad260a66a9687ebd628; cross_origin_proto=SSL; _s_tentry=weibo.com; Apache=5738730368049.107.1682048142847; SINAGLOBAL=5738730368049.107.1682048142847; ULV=1682048142851:1:1:1:5738730368049.107.1682048142847:; wb_view_log=2560*14401; appkey=; WBtopGlobal_register_version=2023042111; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFU70eLSR0lofj0MT5rijkd5JpX5o275NHD95QcSoBc1he0e0npWs4Dqcjci--fi-i8iKn7i--fiK.7iKy8i--Xi-zRiKy2i--fiKnciKy2i--ciKn4iK.0i--ciKn4i-z7; SSOLoginState=1682048385; SUB=_2A25JRnXRDeRhGeBI71QZ8y3Pwz2IHXVqMuAZrDV8PUNbmtANLU7akW9NRpOyYWmToe7F6Fdz97b9Q9cHb6mQAr8V; ALF=1713584384; WBPSESS=YnGmI0xRXPJAIeboDANzVo6Lt9HOEuzmcOP2fMt9ZhMStZ2btEDGqPj_KCCJepadRmRcbdwITpBkOKO9cYVyBeOTX_SGxFN6-B5_3OPJLGdU3hnNJiPVxHemcsjdCkrBRCMK6f-PdLqBVLAJPHQZjg=='
           }

max_page = 10

def get_page(page: object, since_id: object) -> object:  # 定义函数，用于获取指定页数和since_id的微博数据
    if page == 1:  # 如果是第一页，则不需要带since_id参数
        params = {
            'uid': '5827607123',  # 微博个人主页的uid
            'page': page  # 要获取的页数
        }
    else:  # 如果不是第一页，则需要带上since_id参数，以便获取更新的微博数据
        params = {
            'uid': '5827607123',  # 微博个人主页的uid
            'page': page,  # 要获取的页数
            'since_id': since_id  # 上一页最后一条微博的id，用于获取更新的微博数据
        }

    url = base_url + urlencode(params)  # 构造完整的url地址，包含查询参数
    try:
        response = requests.get(url, headers=headers)  # 发送get请求，获取响应数据
        if response.status_code == 200:  # 如果响应状态码为200，则表示请求成功
            response.encoding = response.apparent_encoding  # 自动检测响应数据的编码格式，进行解码
            since_id = response.json().get('data').get('since_id')  # 获取本页最后一条微博的id，用于下一页请求
            return since_id, response.json()  # 返回最后一条微博的id和响应的json数据
    except RequestException as e:  # 如果请求出错，则抛出异常并打印错误信息
        print('Error', e.args)

def parse_page(json):
    # 判断json是否存在
    if json:
        # 获取数据列表
        items = json.get('data').get('list')
    # 遍历列表
    for item in items:
        # 创建微博字典
        weibo = {}
        # 获取微博内容并去掉可能存在的空格字符
        weibo['content'] = item.get('text_raw').replace("\u200b", "")
        # 获取微博内容长度
        weibo['length'] = item.get('textLength')
        # 获取微博来源并去掉可能存在的空格字符
        weibo['source'] = item.get('source').replace("\u200b", "")
        # 获取微博转发数
        weibo['reposts_count'] = item.get('reposts_count')
        # 获取微博评论数
        weibo['comments_count'] = item.get('comments_count')
        # 获取微博点赞数
        weibo['attitudes_count'] = item.get('attitudes_count')
        # 获取微博创建时间
        weibo['created_at'] = item.get('created_at')

        # 通过生成器返回微博字典
        yield weibo

def write_to_csv(content, loop):
    """
    将数据写入CSV文件中，参数:content: dict, 待写入的数据内容，loop: int, 当前循环次数
    返回值:None
    """
    # 打开CSV文件，使用UTF-8编码写入数据
    with open('/Users/fujunqiao/Desktop/未命名文件夹/极客鞋谈.CSV', 'a', newline='', encoding='utf-8-sig') as csvfile:
        # 创建csv文件写入器
        writer = csv.DictWriter(csvfile, fieldnames=content.keys())
        # 如果是第一次循环，则写入表头
        if loop == 1:
            headers = {}
            for n in content.keys():
                headers[n] = n
            writer.writerow(headers)
        # 写入数据
        writer.writerow(content)
    # 关闭CSV文件
    csvfile.close()

def main():
    loop = 1  # 定义循环次数为1
    for page in range(1, max_page + 1):  # 遍历每一页
        time.sleep(1)  # 程序暂停1秒
        if page == 1:  # 如果是第一页
            since_id, json = get_page(page, '')  # 获取该页的微博信息和since_id
        else:  # 如果不是第一页
            since_id, json = get_page(page, since_id)  # 获取该页的微博信息和since_id
        for weibo in parse_page(json):  # 遍历该页中的每一条微博
            write_to_csv(weibo, loop)  # 将微博信息写入csv文件中
            loop += 1  # 循环次数加1
if __name__=='__main__':
    main()
