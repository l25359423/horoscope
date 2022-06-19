import os
import utils
import time
import requests

from lxml import etree


JSON_DIR = '../ares_forum/constellation/'


def getHTML(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding if response.apparent_encoding != 'ISO-8859-1' else 'utf-8'
    return response.text


def parseHTMLByXPath(content):
    html = etree.HTML(content)

    lis = html.xpath('//div[@id="view"]//dd//ul/li')
    res = {}
    for index, li in enumerate(lis):
        title = li.xpath('label/text()')[0].split('：')[0]
        if index < 4:
            width = li.xpath('span/em/@style')[0]
            star = "🌟"
            if '32px' in width:
                star = star * 2
            elif '48px' in width:
                star = star * 3
            elif '64px' in width:
                star = star * 4
            elif '80px' in width:
                star = star * 5
            res[title] = {}
            res[title]['star'] = star
        else:
            res[title] = {}
            res[title]['star'] = li.xpath('text()')[0]
    for i in range(5):
        p_index = "p{}".format(i+1)
        title = html.xpath("//strong[@class='{}']/text()".format(p_index))[0]
        if title == '健康运势':
            title = '健康指数'
        text = html.xpath("//strong[@class='{}']/following-sibling::span/text()".format(p_index))[0]
        res[title]['text'] = text
    return res


def main():
    urls = [
        'https://www.xzw.com/fortune/aries',  # 白羊座
        'https://www.xzw.com/fortune/taurus',  # 金牛座
        'https://www.xzw.com/fortune/gemini',  # 双子座
        'https://www.xzw.com/fortune/cancer',  # 巨蟹座
        'https://www.xzw.com/fortune/leo',  # 狮子座
        'https://www.xzw.com/fortune/virgo',  # 处女座
        'https://www.xzw.com/fortune/libra',  # 天秤座
        'https://www.xzw.com/fortune/scorpio',  # 天蝎座
        'https://www.xzw.com/fortune/sagittarius',  # 射手座
        'https://www.xzw.com/fortune/capricorn',  # 摩羯座
        'https://www.xzw.com/fortune/aquarius',  # 水瓶座
        'https://www.xzw.com/fortune/pisces',  # 双鱼座
    ]

    for url in urls:
        content = getHTML(url)
        res = parseHTMLByXPath(content)

        filename = '{}.json'.format(url.split("/")[-1])
        filename = os.path.join(JSON_DIR, filename)

        # 文件不存在则创建
        if not os.path.exists(filename):
            utils.save(filename, {})
        utils.save(filename, res)
        time.sleep(10)


if __name__ == '__main__':
    main()