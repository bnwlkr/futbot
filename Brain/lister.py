from scout import Scout
import fut

# the lister transports any unassigned items to the tradepile, and then lists players
# at their average prices on the market, and consumables at pre-determined prices.

class Lister:  ##TODO: List items at the right price
    @classmethod
    def list(cls, session):
        for item in session.unassigned():
            session.sendToTradepile(item['id'])
        for item in session.tradepile():
            if item['tradeState'] is None:
                if item['itemType'] == 'player':
                    Lister.listPlayer(item, session)
                    print('item listed!')
                elif item['itemType'] == 'contract' or item['itemType'] == 'health':
                    session.sell(item['id'], 150, 200)
                elif item['itemType'] == 'kit' or item['itemType'] == 'ball':
                    session.quickSell(item['id'])
                else:
                    print ("What should I list this item at?")
                    print item
                    userinput = int(input("Start price: "))
                    session.sell(item['id'], userinput, userinput + 100)
                    print('item listed!')


    @classmethod
    def relist(cls, session):
        session.relist()

    @classmethod
    def listPlayer(cls, player, session):
        try:
            price = Scout.marketpricing(session, player['assetId'])
            if player['lastSalePrice'] == 0: # this player was packed
                if price == 10000:
                    session.sell(player['id'], 150, 200)
                else:
                    listprice = max(player['marketDataMinPrice'], price - 100)
                    session.sell(player['id'], listprice, listprice + 100)
                print('player listed!')
        except fut.PermissionDenied:
            print player
        except fut.UnknownError:
            print("I couldn't list this player. You figure it out, conscious human.")
            print(player)
            print "price: " + str(price)



            #boughtfor = int(player['lastSalePrice'])  #this player was purchased by the buyer
            #breakeven = Scout.roundup(boughtfor / 0.95)  # accounting for EA tax
            #print breakeven
            #print Scout.roundup(breakeven * 1.1)
            #session.sell(player['id'], breakeven, Scout.roundup(breakeven * 1.1))
            #print('player listed!')
