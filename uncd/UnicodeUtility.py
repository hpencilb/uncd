import requests
from bs4 import BeautifulSoup
import re
import os
import json

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


class UnicodeInfo:
    def __init__(self, code=None, letter=None):
        self.site = 'https://unicode-table.com/en/'
        self.info = {}
        if letter:
            self.code = hex(ord(letter[0])).replace('0x', '')
            self.flag = True
        if code:
            if 0 < int(code, 16) < 0xFFFFF:
                self.flag = True
                self.code = code
            else:
                self.flag = False

    def getUnicodeInfo(self):
        url = self.site + self.code
        bs = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=20).text, 'lxml').find_all('div', class_="meta")[
            0]
        self.info['Name'] = re.findall('"symbol-title">(.*?)</td>', str(bs))[0]
        self.info['Unicode number'] = re.findall('"unicode-num"><span class="code">(.*?)</span>', str(bs))[0]
        self.info['HTML'] = re.findall('"html-code"><span class="code">(.*?)</span>', str(bs))[0].replace('&amp;', '&')
        try:
            self.info['Entity'] = re.findall('/">(.*?)</a></div>', str(bs))[0].replace('&amp;', '&')
        except IndexError:
            self.info['Entity'] = None
        self.info['CSS-code'] = re.findall('"css-code"><span class="code">(.*?)</span>', str(bs))[0]
        self.info['Block'] = re.findall('">(.*?)</a></td>', str(bs))[0]
        try:
            self.info['Unicode version'] = re.findall('<td>(.*?)</td></tr> </table>', str(bs))[0]
        except IndexError:
            self.info['Unicode version'] = None
        self.code = fillCode(int(self.code, 16))


def fillCode(code):
    code = hex(code).replace('0x', '\\U')
    le = len(code)
    if le < 10:
        code = '\\U' + '0' * (10 - le) + code[2:]
    return code


class UnicodeBlock:
    def __init__(self, name):
        self.site = 'https://unicode-table.com/en/blocks/'
        self.block_dict = {}
        self.block_name = name
        self.begin = None
        self.end = None
        self.flag = False
        self.path = None
        self.detect()
        self.findBlock()

    def findBlock(self):
        range_ = self.block_dict.get(self.block_name)
        if range_:
            self.begin, self.end = range_.split('—')
            self.flag = True

    def detect(self):
        self.path = os.path.realpath(__file__).replace('UnicodeUtility.py', 'UnicodeBlock.json')
        if not os.path.exists(self.path):
            self.getUnicodeBlock()
        else:
            with open(self.path, 'r+') as f:
                self.block_dict = json.loads(f.readline())

    def getUnicodeBlock(self):
        site = 'https://unicode-table.com/en/blocks/'
        navigation = BeautifulSoup(requests.get(site).text, 'lxml').find_all('div', class_='navigation')[0]
        li = navigation.find_all('li')
        for l in li:
            block_name = re.findall('">(.*?)</a>', str(l))[0]
            range_ = re.findall('"range">(.*?)</span>', str(l))[0]
            self.block_dict[block_name] = range_
        with open(self.path, 'w+') as f:
            f.write(json.dumps(self.block_dict))


if __name__ == '__main__':
    u = UnicodeInfo(letter='abc')
    u.getUnicodeInfo()
    print(u.info)
    # b = UnicodeBlock('Basic Latin')
    # print(b.flag)
