from sim.investor import Investor
from sim.market import Market

PATH_TO_FILE = "C:\\Users\\sbart\\Desktop\\IDE Repositories\\VSC Repos\\Python\\Notebooks\\Market Data\\"


class Simulation:
    def __init__(self, number_of_investors=20, transaction_limit=10, export_filename="prices.txt", initial_market_size=20):
        self.asset_price_over_time = []
        self.transaction_limit = transaction_limit
        self.export_filename = export_filename
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
            print(f"Day {day + 1}/{number_of_days}")
            self.asset_price_over_time.append(self.market.price_tracker.get_latest_asset_price(self.market.get_asset_types()[0]))
            print(self.asset_price_over_time[-1])
            self.process_market_day()

    def get_sales_data(self):
        return self.asset_price_over_time

    def export(self):
        with open(PATH_TO_FILE + self.export_filename, "w") as file:
            for price in self.asset_price_over_time:
                file.write(str(price) + '\n')
