from Asset import Asset

def execute_order(initial_cash, _asset_list):
    asset_list = []
    for asset in _asset_list:
        name = asset[0] #e.g. Spotify
        print(name)
        ticker = asset[1] #e.g. "SPOT"
        asset_level = asset[2] #e.g. 2 (for already having 2 shares)
        _asset = Asset(name, ticker)
        order = _asset.execute_order(asset_level, initial_cash)
        _asset.plot_projections()
        asset_list.append([_asset, order])
    return asset_list
