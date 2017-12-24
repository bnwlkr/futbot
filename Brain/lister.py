from scout import Scout
import fut

# the lister transports any unassigned items to the tradepile, and then lists players
# at their average prices on the market, and consumables at pre-determined prices.

class Lister:  ##TODO: List items at the right price
    @classmethod
    def list(cls, session):
        try:
            for item in session.unassigned():
                session.sendToTradepile(item['id'])
            for item in session.tradepile():
                if item['tradeState'] == 'expired':       #relist expired players
                    Lister.relistExpired(session, item)
                if item['tradeState'] is None:
                    if item['itemType'] == 'player':
                        Lister.listPlayer(session, item)
                    else:
                        Lister.listItem(session, item)
        except fut.PermissionDenied:
            print item
        except fut.UnknownError:
            print("I couldn't list this item. You figure it out, conscious human.")
            print(item)


    @classmethod
    def relist(cls, session):
        session.relist()

    @classmethod
    def listPlayer(cls, session, player):
            price = Scout.marketpricing(session, player['assetId'])
            if player['lastSalePrice'] == 0: # this player was packed
                if price == 10000:
                    session.sell(player['id'], 150, 200)
                else:
                    listprice = max(player['marketDataMinPrice'], price-100)
                    session.sell(player['id'], listprice, listprice + (100 if price >= 1000 else 50))
                print('player listed!')

    @classmethod
    def listItem(cls, session, item):
        if item['itemType'] == 'kit' or item['itemType'] == 'ball' or item['itemType'] == 'gkCoach' or item['itemType'] == 'fitnessCoach':
            session.quickSell(item['id'])
        else:
            price = Scout.itemPricing(session, item['resourceId'])
            if price is None:
                session.sell(item['id'], 150, 200)
            else:
                session.sell(item['id'], max(150, price-50), price)
                print('item listed!')

    @classmethod
    def relistExpired(cls, session, item):
        startingBid = max(item['startingBid']-50, item['marketDataMinPrice'])
        session.sell(item['id'], startingBid, startingBid + (100 if startingBid >= 1000 else 50))
        print('expired item relisted')