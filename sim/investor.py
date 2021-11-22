from random import choice, random, randint
from sim.offer import OfferFactory
NAMES = ["John", "Jack", "Adam", "Patrick", "Mark", "Tenet", "Robert", "Hubert", "Martinez", "Bob"]


class Investor:
    def __init__(self):
        self.name = choice(NAMES) + str(randint(100_000, 999_999))
        self.buy_orders = []
        self.sell_orders = []
        self.stored_assets = []
        self.assets_for_sale = []
        self.funds = 100
        self.inertia = 0.90 + random() * 0.1

    def send_sell_order(self, market):
        if not self.stored_assets:
            return
        chosen_asset = self.stored_assets.pop(choice(range(len(self.stored_assets))))
        self.assets_for_sale.append(chosen_asset)
        latest_price = market.price_tracker.get_latest_asset_price(chosen_asset.company_id)
        offer = OfferFactory().create_offer(self, chosen_asset.company_id, latest_price * 1.10, sell=True)
        market.add_sell_offer(offer)
        self.sell_orders.append(offer)

    def send_buy_order(self, market):
        asset_to_buy = choice(market.get_asset_types())
        latest_price = market.price_tracker.get_latest_asset_price(asset_to_buy)
        if (new_price := latest_price * 0.9) > self.funds:
            return
        offer = OfferFactory().create_offer(self, asset_to_buy, new_price, sell=False)
        market.add_buy_offer(offer)
        self.buy_orders.append(offer)

    def process_buy_order(self, asset_id, price):
        self.funds -= price
        self.stored_assets.append(asset_id)
        self.remove_buy_order(asset_id)

    def process_sell_order(self, asset_id, price):
        self.funds += price
        self.remove_sell_order(asset_id)

    def resend_sell_orders(self, market):
        for i, offer in enumerate(self.sell_orders):
            offer.min_sell_price *= self.inertia
            market.add_sell_offer(offer)

    def resend_buy_orders(self, market):
        for i, offer in enumerate(self.buy_orders):
            offer.max_buy_price = offer.max_buy_price * (2 - self.inertia)
            market.add_buy_offer(offer)

    def resend_orders(self, market):
        self.resend_sell_orders(market)
        self.resend_buy_orders(market)

    def generate_new_orders(self, market):
        lookup = [0.9, 0.5, 0.2, 0.01, 0]
        prob_buy = lookup[len(self.buy_orders)]
        if random() < prob_buy:
            self.send_buy_order(market)
        prob_sell = lookup[len(self.sell_orders)]
        if random() < prob_sell:
            self.send_sell_order(market)

    def remove_sell_order(self, asset_id):
        for i, order in enumerate(self.sell_orders):
            if order.asset_type == asset_id.company_id:
                self.sell_orders.pop(i)
                return

    def remove_buy_order(self, asset_id):
        for i, order in enumerate(self.buy_orders):
            if order.asset_type == asset_id.company_id:
                self.buy_orders.pop(i)
                return

    def get_free_asset(self, asset_company_id):
        for i, asset in enumerate(self.assets_for_sale):
            if asset.company_id == asset_company_id:
                return self.assets_for_sale.pop(i)
