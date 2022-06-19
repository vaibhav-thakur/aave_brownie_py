from scripts.helpful_scripts import getAccount
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = getAccount()
    print("here")
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    print(f"{erc20_address}")
    # Change below to mainnet-fork for testing
    if network.show_active() in ["kovan"]:
        get_weth()
        lending_pool = getLendingPool()
        # print(lending_pool)
        # Approve sending out ERC20 tokens
        # approveERC20()
        approveERC20(amount, lending_pool.address, erc20_address, account)
        # deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)
        print("Depositing...")
        txn = lending_pool.deposit(
            erc20_address, amount, account.address, 0, {"from": account}
        )
        txn.wait(1)
        print("Deposited!")
        # how much?
        borrowableETH, totalDebt = getBorrowableData(lending_pool, account)
        print("Let's borrow!")
        # We need DAI in terms of ETH
        daiETHPrice = getAssetPrice(
            config["networks"][network.show_active()]["dai_eth_price_feed"]
        )
        amountOfDAIToBorrow = (1 / daiETHPrice) * (borrowableETH * 0.95)
        # Multiplied by 0.95 to keep the Health Factor High
        # borrowableETH -> borrowableDAI * 95%
        print(f"We are going to borrow {amountOfDAIToBorrow} DAI")
        # Now we will borrow.
        daiAddress = config["networks"][network.show_active()]["dai_token"]
        borrowTxn = lending_pool.borrow(
            daiAddress,
            Web3.toWei(amountOfDAIToBorrow, "ether"),
            1,
            0,
            account.address,
            {"from": account},
        )
        borrowTxn.wait(1)
        print("We borrowed some DAI!")
        getBorrowableData(lending_pool, account)
        # repayAll(amount, lending_pool, account)
        print(
            "You just Deposited, Borrowed and Repaid, with Aave, Brownie and Chainlink!"
        )


def repayAll(amount, lending_pool, account):
    approveERC20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repayTxn = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repayTxn.wait(1)
    print("Repaid!")


def getAssetPrice(priceFeedAddress):
    # ABI and Address
    daiETHPriceFeed = interface.IAggregatorV3(priceFeedAddress)
    latestPrice = daiETHPriceFeed.latestRoundData()[1]
    convertedLatestPrice = Web3.fromWei(latestPrice, "ether")
    print(f"The DAI/ETH Price is {convertedLatestPrice}")
    # 922413454297202
    # 0.000922413454297202
    return float(convertedLatestPrice)


def getBorrowableData(lending_pool, account):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowETH,
        currentLiquidationThreshold,
        loanToValue,
        healthFactor,
    ) = lending_pool.getUserAccountData(account.address)
    availableBorrowETH = Web3.fromWei(availableBorrowETH, "ether")
    totalDebtETH = Web3.fromWei(totalDebtETH, "ether")
    totalCollateralETH = Web3.fromWei(totalCollateralETH, "ether")

    print(f"You have {totalCollateralETH} worth of ETH deposited.")
    print(f"You have {totalDebtETH} worth of ETH borrowed.")
    print(f"You can borrow {availableBorrowETH} worth of ETH.")

    return (float(availableBorrowETH), float(totalDebtETH))


def approveERC20(amount, spender, erc20Address, account):
    print("Approving ERC20 Token...")
    erc20 = interface.IERC20(erc20Address)
    txn = erc20.approve(spender, amount, {"from": account})
    txn.wait(1)
    print("Approved!")
    return txn
    # ABI and Address


def getLendingPool():
    # ABI and Address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI and Address
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
