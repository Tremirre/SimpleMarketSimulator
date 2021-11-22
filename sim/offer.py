from dataclasses import dataclass
from typing import Any


@dataclass()
class Offer:
    sender: Any
    offer_id: int
    asset_type: str


@dataclass()
class SellOffer(Offer):
    min_sell_price: float


@dataclass()
class BuyOffer(Offer):
    max_buy_price: float


class OfferFactory:
    count = 0

    def create_offer(self, sender: Any, asset_type: str, price: float, sell: bool) -> Offer:
        if sell:
            return SellOffer(sender, self.__class__.count, asset_type, price)
        return BuyOffer(sender, self.__class__.count, asset_type, price)
