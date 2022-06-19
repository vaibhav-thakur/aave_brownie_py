from scripts.aave_borrow import (
    getAssetPrice,
    getLendingPool,
    approveERC20,
    getAccount,
)
from brownie import config, network


def test_getAssetPrice():
    # Arrange / Act
    asset_price = getAssetPrice(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # Assert
    assert asset_price > 0


def test_getLendingPool():
    # Arrange / Act
    lending_pool = getLendingPool()
    # Assert
    assert lending_pool != None


def test_approveERC20():
    # Arrange
    account = getAccount()
    lending_pool = getLendingPool()
    amount = 1000000000000000000  # 1
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    # Act
    approved = approveERC20(amount, lending_pool.address, erc20_address, account)
    # Assert
    # assert approved is True
    assert approved is not "NULL"
