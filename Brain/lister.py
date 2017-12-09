from scout import Scout

class Lister:
    @classmethod
    def list(cls, session):
        print (session.unassigned())
        for item in session.unassigned():
            session.sendToTradepile(item['id'])
        for item in session.tradepile():
            if item['tradeState'] is None:
                if item['itemType'] == 'player':
                    Lister.listPlayer(item, session)
                elif item['itemType'] == 'contract':
                    session.sell(item['id'], 150, 200)
                elif item['itemType'] == 'training':
                    session.sell(item['id'], 150, 200)
                elif item['itemType'] == 'fitness':
                    session.sell(item['id'], 300, 450)
                else:
                    session.sell(item['id'], 150, 200)


    @classmethod
    def relist(cls, session):
        session.relist()
    @classmethod
    def listPlayer(cls, player, session):
        pricing = Scout.pricing(player['assetId'])
        if player['lastSalePrice'] == 0:
            session.sell(player['id'], pricing['low'], pricing['low'] + 100)
            print('player listed!')
        else:
            boughtfor = int(player['lastSalePrice'])
            breakeven = Scout.roundup(boughtfor / 0.95)  # accounting for EA tax
            buynow = Scout.roundup(breakeven * 1.1)  # 10% profit margin
            session.sell(player['tradeId'], breakeven, buynow)  ## probably using the wrong key here
            print('player listed!')