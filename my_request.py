import urllib
import http.client

def get_request(host, method, url, data, headers):
    data = urllib.parse.urlencode(data)
    conn = http.client.HTTPSConnection(host)
    payload = ''
    _url = url+data
    conn.request(method, _url, payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    # print(data)
    return data



# import requests

# def get_request(host, method, url, data, headers):
#     _url = "http://"+host+url
#     sess = requests.Session()
#     if method == "POST":
#         res = sess.post(_url, data=data, headers=headers)
#     elif method == "GET":
#         res = sess.get(_url, data=data, headers=headers)
#     else:
#         raise NotImplementedError
#     if res.status_code != 200:
#         print("网络错误")
#         return "网络错误"
#     res.encoding = 'utf-8'
#     return res.text