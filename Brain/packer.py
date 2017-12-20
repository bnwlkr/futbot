import json
import urllib3

class Packer:
    @classmethod
    def buypack(cls, session, price):
        packs = session.packs()['purchase']
        for pack in packs:
            if pack['coins'] == price:
                session.buyPack(pack['id'])







