from __future__ import annotations

import json
from typing import List


class Price:

    def __init__(self, value, currency, cValue=None, cCurrency=None):
        if cValue is not None:
            cValue = float(cValue)
        self.value = float(value)
        self.currency = currency
        self.cValue = cValue
        self.cCurrency = cCurrency

    def getFxFmtString(self):
        return str(self.value) + " " + str(self.currency)

    def getCvFmtString(self):
        return str(self.cValue) + " " + str(self.cCurrency)


    def toJSON(self):

        return json.dumps(self.toDICT())

    def toDICT(self):
        d = dict()
        d["value"] = self.value
        d["currency"] = self.currency
        d["cValue"] = self.cValue
        d["cCurrency"] = self.cCurrency
        return d

    @staticmethod
    def jsonfyList(prices):
        if not prices:
            return ""
        l = list()
        for price in prices:
            l.append(price.toJSON())
        return json.dumps(l)

    @staticmethod
    def dictifyInnerList(prices: List[Price]):
        if not prices:
            return None
        l = list()
        for price in prices:
            l.append(price.toDICT())
        return l

    @staticmethod
    def reClassPrice(price: dict) -> object:

        return Price(price["value"], price["currency"], price["cValue"], price["cCurrency"])

    @staticmethod
    def reClassPrices(prices: List[dict]) -> List[object] or None:
        if prices is None: return None
        arr = []
        for price in prices:
            arr.append(Price.reClassPrice(price))
        return arr


        
