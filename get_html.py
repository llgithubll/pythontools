import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
import socket


socket.setdefaulttimeout(30)


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
