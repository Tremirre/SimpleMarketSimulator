from sim.investor import Investor
from sim.market import Market

PATH_TO_FILE = "C:\\Users\\sbart\\Desktop\\IDE Repositories\\VSC Repos\\Python\\Notebooks\\Market Data\\"


class Simulation:
    def __init__(self,
                 number_of_investors=20,
                 transaction_limit=10,
                 export_filename="prices.txt",
                 initial_market_size=20,
                 silenced=False):
        self.asset_prices_over_time = [[] for _ in range(10)]
        self.transaction_limit = transaction_limit
        self.export_filename = export_filename
        self.silenced = silenced
        self.investors = [Investor() for _ in range(number_of_investors)]
        self.market = Market()
        self.market.initialize_market(initial_market_size)

    def process_market_day(self):
        for investor in self.investors:
            investor.generate_new_orders(self.market)

        self.market.process_all_offers(self.transaction_limit)
        self.market.update_offers()

    def run(self, number_of_days):
        for day in range(number_of_days):
            self.asset_prices_over_time[0].append(
                self.market.price_tracker.get_latest_asset_price(self.market.get_asset_types()[0]))
            self.asset_prices_over_time[1].append(
                self.market.price_tracker.get_latest_asset_price(self.market.get_asset_types()[1]))
            if not self.silenced:
                print(f"Day {day + 1}/{number_of_days}")
                print(f"Asset price: {self.asset_prices_over_time[-1]}")
            self.process_market_day()

    def get_sales_data(self, idx=0):
        return self.asset_prices_over_time[idx]