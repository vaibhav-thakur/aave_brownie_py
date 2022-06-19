1. Swap ETH for WETH.
2. Deposit ETH into AAVE
3. Borrow some asset with the ETH colllateral
    1. Sell the borrowed asset (Short Sell).
4. Repay everyhting back.

Testing:
    Integration tests: Kovan
    Unit tests: Mainnet-Fork (Mock all Mainnet)

When working with Network, use Development with mocking.
When not working with oracle, can use Mainnet Fork.