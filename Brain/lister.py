from scout import Scout


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
                elif item['itemType'] == 'fitness':
                    session.sell(item['id'], 550, 650)
                    print('item listed!')
                elif item['itemType'] == 'kit':
                    session.quickSell(item['id'])
                else:
                    session.sell(item['id'], 150, 200)
                    print('item listed!')


    @classmethod
    def relist(cls, session):
        session.relist()

    @classmethod
    def listPlayer(cls, player, session):
        pricing = Scout.pricing(player['assetId'])
        if player['lastSalePrice'] == 0: # this player was packed
            print "packed player, rating: " + str(player['rating']) + ", attempted sale at: " +  str(pricing['low'])
            if pricing['low'] == 10000:
                session.sell(player['id'], 150, 200)
            else:
                session.sell(player['id'], pricing['low'], pricing['low'] + 50)
            print('player listed!')


            #boughtfor = int(player['lastSalePrice'])  #this player was purchased by the buyer
            #breakeven = Scout.roundup(boughtfor / 0.95)  # accounting for EA tax
            #print breakeven
            #print Scout.roundup(breakeven * 1.1)
            #session.sell(player['id'], breakeven, Scout.roundup(breakeven * 1.1))
            #print('player listed!')
