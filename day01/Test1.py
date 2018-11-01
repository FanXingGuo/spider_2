import asyncio
import random
import time

import aiohttp
import requests
from aiomultiprocess import Pool

from day01.models import Proxy


#活动ip代理池




def checkIp(proxy):
    url='http://httpbin.org/ip'
    try:
        resp=requests.get(url,proxies=proxy,timeout=5)
    except:
        return False
    if(resp.status_code==200):
        return True
    else:
        return False

# 构建代理ip
ipLists = []
for i in range(51):
    ipLists.append(Proxy.get_random())
# 清洗ip代理池
for index, item in enumerate(ipLists):
    ipPort = item['address']
    if not checkIp({'http': ipPort}):
        print("删除:"+ipPort)
        del ipLists[index]
print(ipLists)

start = time.time()
async def get(url):
    # global ipLists
    # ipPort=random.choice(ipLists)['address']

    ipLists=['101.4.136.34:80','117.191.11.107:8080','117.191.11.106:8080','117.191.11.112:8080']
    headers = {

        "Connection": "keep-alive",
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",

    }
    session = aiohttp.ClientSession()
    ipPort=random.choice(ipLists)
    try:
        response = await session.get(url,headers=headers,proxy="http://"+ipPort)
    except Exception as e:
        print(e)
    result = await response.text()
    # print(result)
    print(len(result))
    await session.close()
    return result




async def request():
    url = 'http://www.thepaper.cn/newsDetail_forward_{}'
    urls = [url.format(i) for i in range(2570000,2570003)]
    async with Pool() as pool:
        result = await pool.map(get, urls)
        return result

coroutine = request()
task = asyncio.ensure_future(coroutine)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)

end = time.time()
print('Cost time:', end - start)
