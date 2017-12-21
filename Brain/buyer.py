import json
import urllib3
from scout import Scout
import pickle
import sys

#the buyer buys individual players on the transfer market to be re-sold at a profit

class Buyer():
    @classmethod
    def buy(cls, session, targets):
        http = urllib3.PoolManager()
        coins = session.credits
        for target in targets:        # target is assetId
            print(target)
            if coins < 150:
                print('out of coins!')
                return
            else:
                Buyer.buyone(target, session)

    @classmethod
    def buyone(cls, target, session):
        iteminfo = Scout.futheadpricing(target)
        if iteminfo['low'] < session.credits:
            auction = session.searchAuctions('player', assetId=int(target), max_buy = Scout.roundup(iteminfo['low'] * 0.95))
            lsf = None
            for player in auction:
                buynow = int(player['buyNowPrice'])
                if buynow < iteminfo['avg'] and buynow < session.credits:
                    if lsf is None or buynow < lsf['buyNowPrice']:
                        lsf = player
            if lsf is not None:
                session.bid(int(lsf['tradeId']), lsf['buyNowPrice'])
                print('I just bought a player for: ' + str(lsf['buyNowPrice']))
                print('Its average price on the market is: ' + str(iteminfo['avg']))
                return
            else:
                print('no players found here')
