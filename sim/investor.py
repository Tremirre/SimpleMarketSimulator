from random import choice, random, randint
NAMES = ["John", "Jack", "Adam", "Patrick", "Mark", "Tenet", "Robert", "Hubert", "Martinez", "Bob"]


class Investor:
    def __init__(self):
        self.name = choice(NAMES) + str(randint(100_000, 999_999))
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
        market.add_sell_offer(self, chosen_asset.company_id, latest_price * 1.10)

    def send_buy_order(self, market):
        asset_type_to_buy = choice(market.get_asset_types())
        latest_price = market.price_tracker.get_latest_asset_price(asset_type_to_buy)
        if (new_price := latest_price * 0.9) > self.funds:
            return
        market.add_buy_offer(self, asset_type_to_buy, new_price)

    def process_buy_order(self, asset_id, price):
        self.funds -= price
        self.stored_assets.append(asset_id)

    def process_sell_order(self, price):
        self.funds += price

    #offer.min_sell_price *= self.inertia
    #offer.max_buy_price = offer.max_buy_price * (2 - self.inertia)

    def generate_new_orders(self, market):
        ...

    def take_available_asset(self, asset_type):
        for i, asset_id in enumerate(self.assets_for_sale):
            if asset_id.company_id == asset_type:
                return self.assets_for_sale.pop(i)
