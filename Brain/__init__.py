import fut
from lister import Lister
from scout import Scout
from packer import Packer
from buyer import Buyer

session = fut.Core('benfw0@gmail.com', 'Thub48sten82!', 'egham', 'ps4')

def list():
    Lister.list(session)

def buy():
    Buyer.buy(session, Scout.search())

def buyplayer(target):
    Buyer.buyone(target, session)

def buypack(price):
    Packer.buypack(session,price)