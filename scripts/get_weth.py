from os import access
from brownie import interface, config, network
from scripts.helpful_scripts import getAccount


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH
    """
    # ABI
    # Address
    account = getAccount()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    txn = weth.deposit({"from": account, "value": 0.1 * 10**18})
    txn.wait(1)
    print("Received 0.1 WETH")
    return txn
