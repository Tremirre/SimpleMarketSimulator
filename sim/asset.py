from random import randint
from typing import NamedTuple


class AssetID(NamedTuple):
    company_id: str
    unique_asset_id: str


class Asset:
    def __init__(self, company):
        self.type = "Stock"
        self.id = AssetID(company.id, str(randint(100_000_000_000_000, 999_999_999_999_999)))

    def get_id(self):
        return self.id


class AssetManager:
    available_assets: dict[str, list[Asset]] = {}

    def add_asset(self, asset: Asset):
        if asset.id.company_id not in self.__class__.available_assets:
            self.__class__.available_assets[asset.id.company_id] = [asset]
        else:
            self.__class__.available_assets[asset.id.company_id].append(asset)

    def create_asset(self, company):
        new_asset = Asset(company)
        self.add_asset(new_asset)
        return new_asset