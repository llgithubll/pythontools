import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
import socket
import requests
from random import choice

socket.setdefaulttimeout(30)
user_agents = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    # 'Googlebot/2.1 (+http://www.google.com/bot.html)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36',
    # 'Gigabot/3.0 (http://www.gigablast.com/spider.html)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/533.3 '
    '(KHTML, like Gecko)  QtWeb Internet Browser/3.7 http://www.QtWeb.net',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, '
    'like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) '
    'Gecko/20070404 K-Ninja/2.1.3',
    'Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; '
    'en-US) iNet Browser 4.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) '
    'Gecko/20080414 Firefox/2.0.0.13 Pogo/2.0.0.13.6866',
    # 'WorldWideweb (NEXT)'
]


def get_html(url, code='utf-8'):
    """获取请求url返回的页面，默认utf-8解码"""
    for i in range(3):
        try:
            page = urllib.request.urlopen(url)
            break
        except HTTPError as e:
            print('!!!%s，服务器不能应答，Error Code:%s' % (url, str(e.code)))
        except URLError as e:
            print('!!!%s，连接服务器失败，Reason:%s' % (url, str(e.reason)))
        except socket.timeout:
            print('!!!%s 访问超时' % url)
            time.sleep(60)
        except Exception as e:
            print('!!!%s 访问出错' + str(e) % url)
        time.sleep(20)
    else:
        print('!!!%s 页面访问失败，丢弃' % url)
        return ""

    try:
        html = page.read().decode(code, errors='ignore')
        return html
    except:
        print('!!!%s 页面读取失败，丢弃' % url)
        return ""


def get_html_with_proxies(url, code='utf-8', proxies=None, timewait=10):
    """
    获取请求url返回的页面，默认utf-8解码，如果提供代理，则使用代理
    否则使用默认代理
    """
    if proxies is None:
        proxies = {
            'http': 'http://127.0.0.1:1080',
            'https': 'https://127.0.0.1:1080'
        }

    for i in range(3):
        headers = {'User-Agent': choice(user_agents)}
        response = requests.get(url, proxies=proxies, headers=headers)
        if response.status_code == requests.codes.ok:
            response.encoding = code
            return response.text
        print('!!!', url, response.status_code)
        time.sleep(timewait)
    else:
        return ""


def get_html_with_header(url, code='utf-8', header=None):
    """
    获取请求url返回的页面，默认utf-8解码
    对get_html进行了一些优化
    1. 对404信息迅速跳过
    2. 对403(服务器Forbidden)酌情添加headers伪装浏览器
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    if header:
        headers = header

    for i in range(3):
        try:
            req = urllib.request.Request(url=url, headers=headers)
            page = urllib.request.urlopen(req)
            break
        except HTTPError as e:
            print('!!!%s，服务器不能应答，Error Code:%s' % (url, str(e.code)))
            if str(e.code) == '404':
                return ''
        except URLError as e:
            print('!!!%s，连接服务器失败，Reason:%s' % (url, str(e.reason)))
        except socket.timeout:
            print('!!!%s 访问超时' % url)
            time.sleep(60)
        except Exception as e:
            print('!!!%s 访问出错' + str(e) % url)
        time.sleep(20)
    else:
        print('!!!%s 页面访问失败，丢弃' % url)
        return ""

    try:
        html = page.read().decode(code, errors='ignore')
        return html
    except:
        print('!!!%s 页面读取失败，丢弃' % url)
        return ""


def get_redirect_url_and_html(url, code='utf-8'):
    """获取重定向之后的url，和重定向url的页面内容，默认utf-8解码
    return redirect_url, html
    """
    for i in range(3):
        try:
            page = urllib.request.urlopen(url)
            break
        except HTTPError as e:
            print('!!!%s，服务器不能应答，Error Code:%s' % (url, str(e.code)))
        except URLError as e:
            print('!!!%s，连接服务器失败，Reason:%s' % (url, str(e.reason)))
        except socket.timeout:
            print('!!!%s 访问超时' % url)
            time.sleep(60)
        except Exception as e:
            print('!!!%s 访问出错' + str(e) % url)
        time.sleep(20)
    else:
        print('!!!%s 页面访问失败，丢弃' % url)
        return None, ""

    try:
        redirect_url = urllib.parse.unquote(page.geturl())
        html = page.read().decode(code, errors='ignore')
        return redirect_url, html
    except:
        print('!!!%s 页面读取失败，丢弃' % url)
        return None, ""


if __name__ == '__main__':
    html = get_html_with_proxies('http://www.google.com')
    print(html)