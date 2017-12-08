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
            if coins < 1000:
                print('out of coins!')
                return
            iteminfo = Scout.pricing(target)
            if iteminfo['low'] < coins:
                auction = session.searchAuctions('player', assetId=int(target), max_buy=Scout.roundup(iteminfo['low']*0.95))
                print (iteminfo['low']*0.95)
                print (Scout.roundup(iteminfo['low']*0.95))
                print(len(auction))
                lsf = None
                for player in auction:
                    buynow = int(player['buyNowPrice'])
                    if buynow < iteminfo['avg'] and buynow < coins: # accounting for EA tax
                        if lsf is None or buynow < lsf['buyNowPrice']:
                            lsf = player
                if lsf is not None:
                    session.bid(int(lsf['tradeId']), int(lsf['buyNowPrice']))
                    print('I just bought a player for: ' + str(lsf['buyNowPrice']))
                    print('Its average price on the market is: ' + str(iteminfo['avg']))
                    return
                else:
                    print('no players found here')

    @classmethod
    def buyone(cls, target, session):
        iteminfo = Scout.pricing(target)
        if iteminfo['low'] < session.credits:
            auction = session.searchAuctions('player', assetId=int(target), max_buy = 20000)
            lsf = None
            for player in auction:
                buynow = int(player['buyNowPrice'])
                if buynow < iteminfo['avg'] and buynow < session.credits:  # accounting for EA tax
                    if lsf is None or buynow < lsf['buyNowPrice']:
                        lsf = player
            if lsf is not None:
                session.bid(int(lsf['tradeId']), int(iteminfo['low']+200))
                print('I just bought a player for: ' + str(lsf['buyNowPrice']))
                print('Its average price on the market is: ' + str(iteminfo['avg']))
                return
            else:
                print('no players found here')
