class Company:
    def __init__(self):
        self.name = "Company A"
        self.id = "COPA"
        self.funds = 10_000_000
        self.assets_for_sale = []

    def get_free_asset(self, asset_company_id):
        for i, asset in enumerate(self.assets_for_sale):
            if asset.company_id == asset_company_id:
                return self.assets_for_sale.pop(i)
