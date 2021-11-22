from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod


@dataclass
class Offer(ABC):
    sender: Any
    offer_id: int
    asset_type: str
    days_since_given: int
    price: float

    @abstractmethod
    def update_price(self):
        ...


@dataclass
class SellOffer(Offer):
    def update_price(self):
        self.price *= self.sender.inertia


@dataclass
class BuyOffer(Offer):
    def update_price(self):
        old_price = self.price
        self.price *= (2 - self.sender.inertia)
        self.sender.update_frozen_funds(old_price, self.price)


class OfferFactory:
    count = 0

    def create_offer(self, sender: Any, asset_type: str, price: float, sell: bool) -> Offer:
        if sell:
            return SellOffer(sender, self.__class__.count, asset_type, 0, price)
        return BuyOffer(sender, self.__class__.count, asset_type, 0, price)
