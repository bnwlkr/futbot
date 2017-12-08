from scout import Scout

class Lister:
    @classmethod
    def listpurchased(cls, session):
        print (session.unassigned())
        for item in session.unassigned():
            session.sendToTradepile(item['id'])
        for item in session.tradepile():
           boughtfor = int(item['lastSalePrice'])
           breakeven = Scout.roundup(boughtfor / 0.95)  # accounting for EA tax
           buynow = Scout.roundup(breakeven * 1.1) # 10% profit margin
           session.sell(item['id'], breakeven, buynow)     ## probably using the wrong key here
           print ('player listed!')
    @classmethod
    def relist(cls, session):
        session.relist()

