from sim.asset import AssetManager
from sim.offer import OfferFactory
from sim.company import Company
from random import shuffle

MAX_DAYS = 50


class Market:
    def __init__(self):
        self.sell_offers = []
        self.buy_offers = []
        self.price_tracker = PriceTracker()
        self.companies = set()

    def initialize_market(self, initial_market_size=20, initial_price=5.0):
        self.companies.add(company := Company("NetFuel"))
        self.companies.add(company_2 := Company("ByTron"))
        for _ in range(initial_market_size//2):
            new_asset = AssetManager().create_asset(company)
            company.assets_for_sale.append(new_asset.id)
            self.add_sell_offer(company, new_asset.id.company_id, initial_price)
        for _ in range(initial_market_size//2):
            new_asset = AssetManager().create_asset(company_2)
            company.assets_for_sale.append(new_asset.id)
            self.add_sell_offer(company, new_asset.id.company_id, 13.2)
        self.price_tracker.set_latest_asset_price(company.id, initial_price)
        self.price_tracker.set_latest_asset_price(company_2.id, 13.2)

    def add_sell_offer(self, sender, asset_type, price):
        self.sell_offers.append(OfferFactory().create_offer(sender, asset_type, price, sell=True))

    def add_buy_offer(self, sender, asset_type, price):
        self.buy_offers.append(OfferFactory().create_offer(sender, asset_type, price, sell=False))

    def process_all_offers(self, transaction_limit=10):
        processed_transactions = []
        shuffle(self.sell_offers)
        shuffle(self.buy_offers)
        for i, sell_offer in enumerate(self.sell_offers):
            for j, buy_offer in enumerate(self.buy_offers):
                if sell_offer.asset_type == buy_offer.asset_type and sell_offer.price <= buy_offer.price:
                    self.process_offer(buy_offer, sell_offer)
                    processed_transactions.append(i)
                    self.buy_offers.pop(j)
                    break
            if len(processed_transactions) >= transaction_limit:
                self.remove_processed_sales(processed_transactions)
                return
        self.remove_processed_sales(processed_transactions)

    def process_offer(self, buy_offer, sell_offer):
        buyer = buy_offer.sender
        seller = sell_offer.sender
        asset_for_sale = seller.take_available_asset(buy_offer.asset_type)
        common_price = sell_offer.price
        self.price_tracker.set_latest_asset_price(asset_for_sale.company_id, common_price)
        buyer.process_buy_order(asset_for_sale, common_price)
        if not isinstance(seller, Company):
            seller.process_sell_order(common_price)

    def get_asset_types(self):
        return [company.id for company in self.companies]

    def remove_outdated_offers(self, sell: bool):
        for_removal = []
        offers = self.sell_offers if sell else self.buy_offers
        for offer in offers:
            if offer.days_since_given >= MAX_DAYS and not isinstance(offer.sender, Company):
                for_removal.append(offer.offer_id)
                if not sell:
                    offer.sender.retract_buy_offer(offer.price)
                else:
                    offer.sender.retract_sell_offer(offer.asset_type)
        while for_removal:
            if sell:
                self.remove_sell_offer(for_removal.pop())
            else:
                self.remove_buy_offer(for_removal.pop())

    def update_offers(self):
        self.remove_outdated_offers(sell=True)
        self.remove_outdated_offers(sell=False)
        for offer in self.sell_offers + self.buy_offers:
            if offer.days_since_given >= 1 and not isinstance(offer.sender, Company):
                offer.update_price()
            offer.days_since_given += 1

    def remove_sell_offer(self, offer_id):
        for i, offer in enumerate(self.sell_offers):
            if offer.offer_id == offer_id:
                self.sell_offers.pop(i)
                return

    def remove_buy_offer(self, offer_id):
        for i, offer in enumerate(self.buy_offers):
            if offer.offer_id == offer_id:
                self.buy_offers.pop(i)
                return

    def remove_processed_sales(self, list_of_sales):
        for index in sorted(list_of_sales, reverse=True):
            self.sell_offers.pop(index)

    def display_sell_offers(self):
        for offer in self.sell_offers:
            print(f"{offer.sender.name} offers asset {offer.asset_type} to sell for at least {offer.min_sell_price}")

    def display_buy_offers(self):
        for offer in self.buy_offers:
            print(f"{offer.sender.name} offers to buy asset {offer.asset_type} for at most {offer.max_buy_price}")

    def count_own_offers(self, name, sell: bool):
        offers = self.sell_offers if sell else self.buy_offers
        return sum([1 if offer.sender.name == name else 0 for offer in offers])


class PriceTracker:
    def __init__(self):
        self.asset_price = dict()

    def set_latest_asset_price(self, asset_type, price):
        self.asset_price.setdefault(asset_type, []).append(price)

    def get_latest_asset_price(self, asset_type):
        return self.asset_price[asset_type][-1]