import requests
from bs4 import BeautifulSoup
import urllib.parse
import xlwt
import xlrd
def login(username, password):
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
        'Origin': 'https://accounts.douban.com',
        'content-Type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'connection': 'keep-alive'
        , 'Host': 'accounts.douban.com'
    }
    data = {
        'ck' : '',
        'name': '',
        'password': '',
        'remember': 'false',
        'ticket': ''
    }
    data['name'] = username
    data['password'] = password
    data = urllib.parse.urlencode(data)
    print(data)
    req = requests.post(url, headers=header, data=data, verify=False)
    cookies = requests.utils.dict_from_cookiejar(req.cookies)
    print(cookies)
    return cookies
def getcomment(cookies, mvid):
    start = 0
    w = xlwt.Workbook(encoding='ascii')  # #创建可写的workbook对象
    ws = w.add_sheet('sheet1')  # 创建工作表sheet
    index = 1  # 表示行的意思，在xls文件中写入对应的行数
    while True:
        # 模拟浏览器头发送请求
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        # try catch
        try:
            url = 'https://movie.douban.com/subject/' + str(mvid) + '/comments?start=' + str(
                start) + '&limit=20&sort=new_score&status=P&comments_only=1'
            start += 20
            req = requests.get(url, cookies=cookies, headers=header)
            res = req.json()
            res = res['html']
            soup = BeautifulSoup(res, 'lxml')
            node = soup.select('.comment-item')
            for va in node:
                name = va.a.get('title')
                comment = va.select_one('.short').text
                ws.write(index, 4, comment)
                index += 1
        except Exception as e:
            print(e)
            break
    ws.to_csv("data.csv")
if __name__ == '__main__':
    username = input('输入账号：')
    password = input('输入密码：')
    cookies = login(username, password)
    mvid = input('电影的id为：')
    getcomment(cookies, mvid)
