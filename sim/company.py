class Company:
    def __init__(self, name):
        self.name = name
        self.id = self.name[:3].upper()
        self.funds = 10_000_000
        self.assets_for_sale = []

    def take_available_asset(self, asset_company_id):
        for i, asset in enumerate(self.assets_for_sale):
            if asset.company_id == asset_company_id:
                return self.assets_for_sale.pop(i)
