import time
from urllib import request, parse
from lxml import etree
from typing import Union
import json

sign_url = 'https://tieba.baidu.com/sign/add'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Cookie': '你自己的Cookie'
}

data = {
    'ie': 'utf-8',
    'kw': ''
}


def get_html(total_page: Union[int, None], current_page: int) -> list[str]:
    """
    获取关注的吧名
    :param total_page: 展示总页面条数
    :param current_page: 当前爬取的页面
    :return: 所有关注的吧名
    """
    if total_page is not None:
        if current_page > total_page:
            return list()
        else:
            print(f'当前页面为:{current_page},数据准备初始化...')
    time.sleep(0.5)
    url = f'https://tieba.baidu.com/f/like/mylike?pn={current_page}'
    req = request.Request(url, headers=headers)
    content = request.urlopen(req).read().decode('gbk')
    # 获取关注列表参数
    tree = etree.HTML(content)
    # 获取关注列表页数,方便后续递归遍历
    if total_page is None:
        total_page = tree.xpath('//div[@class="pagination"]/a[text()="尾页"]/@href')[0][-1:-2:-1]
    # 当前页面展示的吧名
    arr: list = tree.xpath('//tr/td[1]/a/@title')
    print(f'当前页面为{current_page},值为{arr}')
    arr.extend(get_html(int(total_page), current_page + 1))
    return arr


def do_sign(sign_list: list[str]) -> list[dict]:
    """
    签到,并获取签到响应信息
    :param sign_list: 需要签到的吧名
    :return: 响应信息
    """
    res_list = []
    for name in sign_list:
        time.sleep(0.1)
        data['kw'] = name
        # post数据编码
        url_data = parse.urlencode(data).encode('utf-8')
        req = request.Request(sign_url, data=url_data, headers=headers)
        res = request.urlopen(req).read().decode('utf-8')
        res = json.loads(res)
        res_list.append(res)
    return res_list


if __name__ == '__main__':
    sign_list = get_html(None, 1)
    res_data = do_sign(sign_list)
    print(res_data)
