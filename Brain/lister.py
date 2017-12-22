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
                if item['tradeState'] is None:
                    if item['itemType'] == 'player':
                        Lister.listPlayer(item, session)
                        print('item listed!')
                    elif item['itemType'] == 'contract' or item['itemType'] == 'health' or item['itemType'] == 'manager':
                        session.sell(item['id'], 150, 200)
                    elif item['itemType'] == 'training':
                        if item['rareflag'] == 0:
                            session.sell(item['id'], 150, 200)
                        else:
                            session.sell(item['id'], 300, 400)
                    elif item['itemType'] == 'kit' or item['itemType'] == 'ball' or item['itemType'] == 'gkCoach':
                        session.quickSell(item['id'])
                    else:
                        print ("What should I list this item at?")
                        print item
                        userinput = int(input("Start price: "))
                        session.sell(item['id'], userinput, userinput + 100)
                        print('item listed!')
        except fut.PermissionDenied:
            print item

        except fut.UnknownError:
            print("I couldn't list this item. You figure it out, conscious human.")
            print(item)
            print "price: " + str(item)


    @classmethod
    def relist(cls, session):
        session.relist()

    @classmethod
    def listPlayer(cls, player, session):
            price = Scout.marketpricing(session, player['assetId'])
            if player['lastSalePrice'] == 0: # this player was packed
                if price == 10000:
                    session.sell(player['id'], 150, 200)
                    print('player listed!')
                else:
                    listprice = max(player['marketDataMinPrice'], price - 100)
                    session.sell(player['id'], listprice, listprice + 100)
                print('player listed!')




            #boughtfor = int(player['lastSalePrice'])  #this player was purchased by the buyer
            #breakeven = Scout.roundup(boughtfor / 0.95)  # accounting for EA tax
            #print breakeven
            #print Scout.roundup(breakeven * 1.1)
            #session.sell(player['id'], breakeven, Scout.roundup(breakeven * 1.1))
            #print('player listed!')
