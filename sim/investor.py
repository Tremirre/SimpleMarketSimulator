from random import choice, random, randint
NAMES = ["John", "Jack", "Adam", "Patrick", "Mark", "Tenet", "Robert", "Hubert", "Martinez", "Bob"]

MAX_INITIAL_FUNDS = 40


class Investor:
    def __init__(self):
        self.name = choice(NAMES) + str(randint(100_000, 999_999))
        self.stored_assets = []
        self.assets_for_sale = []
        self.funds = 20 + randint(0, 20)
        self.frozen_funds = 0
        self.inertia = 0.88 + random() * 0.04

    def send_sell_order(self, market):
        if not self.stored_assets:
            return
        chosen_asset = self.stored_assets.pop(choice(range(len(self.stored_assets))))
        self.assets_for_sale.append(chosen_asset)
        latest_price = market.price_tracker.get_latest_asset_price(chosen_asset.company_id)
        market.add_sell_offer(self, chosen_asset.company_id, latest_price * (1.025 + 0.5 * random() * (2 - self.inertia)))

    def send_buy_order(self, market):
        asset_type_to_buy = choice(market.get_asset_types())
        latest_price = market.price_tracker.get_latest_asset_price(asset_type_to_buy)
        if (new_price := latest_price * (0.84 + 0.6 * random() * self.inertia)) > self.funds:
            return
        self.funds -= new_price
        self.frozen_funds += new_price
        market.add_buy_offer(self, asset_type_to_buy, new_price)

    def process_buy_order(self, asset_id, price):
        self.frozen_funds -= price
        self.stored_assets.append(asset_id)

    def process_sell_order(self, price):
        self.funds += price

    def generate_new_orders(self, market):
        probabilities = [0.7, 0.4, 0.1, 0.01, 0, 0]
        if random() < probabilities[market.count_own_offers(self.name, sell=False)]:
            self.send_buy_order(market)
        if random() < probabilities[market.count_own_offers(self.name, sell=True)]:
            self.send_sell_order(market)

    def take_available_asset(self, asset_type):
        for i, asset_id in enumerate(self.assets_for_sale):
            if asset_id.company_id == asset_type:
                return self.assets_for_sale.pop(i)

    def update_frozen_funds(self, old_price, new_price):
        self.frozen_funds += old_price
        self.frozen_funds -= new_price

    def retract_buy_offer(self, price):
        self.frozen_funds -= price
        self.funds += price

    def retract_sell_offer(self, asset_type):
        asset_id = self.take_available_asset(asset_type)
        assert asset_id is not None
        self.stored_assets.append(asset_id)
