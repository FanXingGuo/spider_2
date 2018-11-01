import aiohttp
import asyncio
import time
# from day01.models import Proxy
from lxml import etree
import random
from aiomultiprocess import Pool
import motor.motor_asyncio

client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db=client.test_database

# 获取代理池ip
# ipLists=[]
# for _ in range(100):
#     ipPort={}
#     ipPort['http']=Proxy.get_random()['address']
#     ipLists.append(ipPort)
#
# print(ipLists)

# [{'http': '116.192.171.154:57706'}, {'http': '122.243.9.180:9000'}, {'http': '117.90.6.65:9000'}, {'http': '115.218.214.88:9000'}, {'http': '121.9.249.98:36127'}, {'http': '121.232.194.147:9000'}, {'http': '39.105.95.204:80'}, {'http': '171.37.157.65:8123'}, {'http': '121.232.148.180:9000'}, {'http': '121.232.147.69:9000'}, {'http': '183.158.206.170:9000'}, {'http': '120.197.100.130:1080'}, {'http': '123.191.74.89:9000'}, {'http': '183.203.214.148:8118'}, {'http': '115.223.249.185:9000'}, {'http': '39.135.11.96:8080'}, {'http': '121.232.148.112:9000'}, {'http': '60.191.57.78:10800'}, {'http': '115.196.51.96:9000'}, {'http': '101.4.136.34:80'}, {'http': '124.79.164.87:8118'}, {'http': '114.234.82.59:9000'}, {'http': '211.159.219.225:8118'}, {'http': '183.48.27.184:51367'}, {'http': '221.2.174.28:8060'}, {'http': '121.232.146.217:9000'}, {'http': '171.37.157.65:8123'}, {'http': '117.71.4.62:8998'}, {'http': '220.184.149.22:8998'}, {'http': '39.135.10.170:8080'}, {'http': '47.94.230.42:9999'}, {'http': '115.218.222.75:9000'}, {'http': '59.62.26.156:9000'}, {'http': '116.192.171.154:57706'}, {'http': '121.232.145.73:9000'}, {'http': '113.109.25.245:8118'}, {'http': '183.158.203.74:9000'}, {'http': '117.90.137.254:9000'}, {'http': '106.32.8.208:8998'}, {'http': '39.135.11.90:8080'}, {'http': '218.198.117.194:39248'}, {'http': '121.232.144.188:9000'}, {'http': '115.223.196.226:9000'}, {'http': '112.95.27.16:8118'}, {'http': '180.104.62.250:9000'}, {'http': '115.218.223.15:9000'}, {'http': '59.62.35.145:9000'}, {'http': '182.139.111.77:9000'}, {'http': '163.125.221.127:8118'}, {'http': '27.19.11.218:8998'}, {'http': '61.50.131.234:8080'}, {'http': '121.232.148.238:9000'}]


async def checkIp(dict={"http":'101.4.136.34:81'}):
    '''
    :param dict: {"http":"ip:port"}
    :return: True or Flase
    '''

    url = 'http://httpbin.org/ip'
    session = aiohttp.ClientSession()
    try:
        resp = await session.get(url, proxy="http://" + dict['http'],timeout=3)
        await session.close()
    except Exception as e:
        print(e)
        return False
    if resp.status==200:
        return True
    else:
        return False
async def getIpAP():
    global ipLists
    for index,ipPort in enumerate(ipLists):
        if not (await checkIp(ipPort)):
            del ipLists[index]
            print("已删除:"+ipPort['http'])
    print(ipLists)

async def getHtml(url):
    '''

    :param url: http://...
    :param proxy: {'http':'ip:Port'}
    :return: html text
    '''
    session = aiohttp.ClientSession()
    headers = {

        "Connection": "keep-alive",
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",

    }
    try:
        response= await session.get(url,headers=headers,timeout=1)#,proxy='http://'+proxy['http'])
        await session.close()
        html= await response.text()
    except Exception as e:
        print(e)
        return
    if len(html) > 10:
        htmlEle = etree.HTML(html)
        title = htmlEle.xpath('//h1[@class="news_title"]/text()')[0]

        print(title)
        result = await db.test_collection.insert_one({"title": title})
        print("result%s" % repr(result.inserted_id))
    else:
        print("file:" + url)


async def main():
    url = 'http://127.0.0.1:5000/'
    urls = [url for _ in range(2580800, 2580810)]
    async with Pool() as pool:
        await pool.map(getHtml,urls)








start=time.time()
# 单进程异步
# loop=asyncio.get_event_loop()
# loop.run_until_complete(getIpAP())
# 多进程 异步

cur=main()
task=asyncio.ensure_future(cur)
loop=asyncio.get_event_loop()
loop.run_until_complete(task)
end=time.time()
print("Cost time:%f"%(end-start))
