import urllib3
from bs4 import BeautifulSoup
import re
import json
import math


class Scout:
    @classmethod
    def search(cls):
        http = urllib3.PoolManager()
        r = http.request('GET', "https://www.futbin.com/market/")
        soup = BeautifulSoup(r.data, "lxml")
        list = soup.find_all('td')
        rsf = 0
        for i in list:
            if ("pre_up" in str(i.span)):
                rsf += 1
        list = list[0:rsf * 2 + 1]
        regexList = []
        for i in list:
            regexList.append(re.search("[0-9]+\.", (str(i.img))))
        newList = filter(lambda x: x is not None, regexList)
        finalList = map(lambda x: x.group(0)[:-1], newList)
        return finalList

    @classmethod
    def futheadpricing(cls, assetId):
        http = urllib3.PoolManager()
        r = http.request('GET', "http://www.futhead.com/prices/api/?year=18&id=" + str(assetId))
        data = json.loads(r.data)
        avgprice = int(data[str(assetId)]['psAvg'])
        lowprice = int(data[str(assetId)]['ps'])
        return {'avg': avgprice, 'low': lowprice}


    @classmethod
    def marketpricing(cls, session, assetId):
        players = session.search('player', assetId=assetId)
        lowestprice = None
        for player in players:
            if (lowestprice is None or player['buyNowPrice'] < lowestprice):
                lowestprice = player['buyNowPrice']
        return lowestprice

    @classmethod
    def itemPricing(cls, session, resourceID):
        items = session.search('development', defId=resourceID)
        lowestprice = None
        for item in items:
            if (lowestprice is None or item['buyNowPrice'] < lowestprice):
                lowestprice = item['buyNowPrice']
        return lowestprice


# this scout happens to be carrying a cheeky calculator lol
    @classmethod
    def roundup(cls, x):
        return int(math.ceil(x / 100.0)) * 100