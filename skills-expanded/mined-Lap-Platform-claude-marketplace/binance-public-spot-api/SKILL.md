---
name: binance-public-spot-api
description: "Binance Public Spot API skill. Use when working with Binance Public Spot for api, sapi. Covers 340 endpoints."
version: 1.0.0
generator: lapsh
---

# Binance Public Spot API
API version: 1.0

## Auth
ApiKey X-MBX-APIKEY in header

## Base URL
https://api.binance.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/v3/ping -- verify access
3. POST /api/v3/order/test -- create first test

## Endpoints

340 endpoints across 2 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v3/ping | Test Connectivity |
| GET | /api/v3/time | Check Server Time |
| GET | /api/v3/exchangeInfo | Exchange Information |
| GET | /api/v3/depth | Order Book |
| GET | /api/v3/trades | Recent Trades List |
| GET | /api/v3/historicalTrades | Old Trade Lookup |
| GET | /api/v3/aggTrades | Compressed/Aggregate Trades List |
| GET | /api/v3/klines | Kline/Candlestick Data |
| GET | /api/v3/uiKlines | UIKlines |
| GET | /api/v3/avgPrice | Current Average Price |
| GET | /api/v3/ticker/24hr | 24hr Ticker Price Change Statistics |
| GET | /api/v3/ticker/tradingDay | Trading Day Ticker |
| GET | /api/v3/ticker/price | Symbol Price Ticker |
| GET | /api/v3/ticker/bookTicker | Symbol Order Book Ticker |
| GET | /api/v3/ticker | Rolling window price change statistics |
| POST | /api/v3/order/test | Test New Order (TRADE) |
| GET | /api/v3/order | Query Order (USER_DATA) |
| POST | /api/v3/order | New Order (TRADE) |
| DELETE | /api/v3/order | Cancel Order (TRADE) |
| POST | /api/v3/order/cancelReplace | Cancel an Existing Order and Send a New Order (Trade) |
| GET | /api/v3/openOrders | Current Open Orders (USER_DATA) |
| DELETE | /api/v3/openOrders | Cancel all Open Orders on a Symbol (TRADE) |
| GET | /api/v3/allOrders | All Orders (USER_DATA) |
| POST | /api/v3/orderList/oco | New Order list - OCO (TRADE) |
| POST | /api/v3/orderList/oto | New Order List - OTO (TRADE) |
| POST | /api/v3/orderList/otoco | New Order List - OTOCO (TRADE) |
| GET | /api/v3/orderList | Query OCO (USER_DATA) |
| DELETE | /api/v3/orderList | Cancel OCO (TRADE) |
| GET | /api/v3/allOrderList | Query all OCO (USER_DATA) |
| GET | /api/v3/openOrderList | Query Open OCO (USER_DATA) |
| POST | /api/v3/sor/order | New order using SOR (TRADE) |
| POST | /api/v3/sor/order/test | Test new order using SOR (TRADE) |
| GET | /api/v3/account | Account Information (USER_DATA) |
| GET | /api/v3/myTrades | Account Trade List (USER_DATA) |
| GET | /api/v3/rateLimit/order | Query Current Order Count Usage (TRADE) |
| GET | /api/v3/myPreventedMatches | Query Prevented Matches |
| GET | /api/v3/myAllocations | Query Allocations (USER_DATA) |
| GET | /api/v3/account/commission | Query Commission Rates (USER_DATA) |
| POST | /api/v3/userDataStream | Create a ListenKey (USER_STREAM) |
| PUT | /api/v3/userDataStream | Ping/Keep-alive a ListenKey (USER_STREAM) |
| DELETE | /api/v3/userDataStream | Close a ListenKey (USER_STREAM) |

### sapi
| Method | Path | Description |
|--------|------|-------------|
| POST | /sapi/v1/margin/borrow-repay | Margin account borrow/repay(MARGIN) |
| GET | /sapi/v1/margin/borrow-repay | Query borrow/repay records in Margin account(USER_DATA) |
| GET | /sapi/v1/margin/transfer | Get Cross Margin Transfer History (USER_DATA) |
| GET | /sapi/v1/margin/allAssets | Get All Margin Assets (MARKET_DATA) |
| GET | /sapi/v1/margin/allPairs | Get All Cross Margin Pairs (MARKET_DATA) |
| GET | /sapi/v1/margin/priceIndex | Query Margin PriceIndex (MARKET_DATA) |
| GET | /sapi/v1/margin/order | Query Margin Account's Order (USER_DATA) |
| POST | /sapi/v1/margin/order | Margin Account New Order (TRADE) |
| DELETE | /sapi/v1/margin/order | Margin Account Cancel Order (TRADE) |
| GET | /sapi/v1/margin/interestHistory | Get Interest History (USER_DATA) |
| GET | /sapi/v1/margin/forceLiquidationRec | Get Force Liquidation Record (USER_DATA) |
| GET | /sapi/v1/margin/account | Query Cross Margin Account Details (USER_DATA) |
| GET | /sapi/v1/margin/openOrders | Query Margin Account's Open Orders (USER_DATA) |
| DELETE | /sapi/v1/margin/openOrders | Margin Account Cancel all Open Orders on a Symbol (TRADE) |
| GET | /sapi/v1/margin/allOrders | Query Margin Account's All Orders (USER_DATA) |
| POST | /sapi/v1/margin/order/oco | Margin Account New OCO (TRADE) |
| GET | /sapi/v1/margin/orderList | Query Margin Account's OCO (USER_DATA) |
| DELETE | /sapi/v1/margin/orderList | Margin Account Cancel OCO (TRADE) |
| GET | /sapi/v1/margin/allOrderList | Query Margin Account's all OCO (USER_DATA) |
| GET | /sapi/v1/margin/openOrderList | Query Margin Account's Open OCO (USER_DATA) |
| GET | /sapi/v1/margin/myTrades | Query Margin Account's Trade List (USER_DATA) |
| GET | /sapi/v1/margin/maxBorrowable | Query Max Borrow (USER_DATA) |
| GET | /sapi/v1/margin/maxTransferable | Query Max Transfer-Out Amount (USER_DATA) |
| GET | /sapi/v1/margin/tradeCoeff | Get Summary of Margin account (USER_DATA) |
| GET | /sapi/v1/margin/isolated/account | Query Isolated Margin Account Info (USER_DATA) |
| DELETE | /sapi/v1/margin/isolated/account | Disable Isolated Margin Account (TRADE) |
| POST | /sapi/v1/margin/isolated/account | Enable Isolated Margin Account (TRADE) |
| GET | /sapi/v1/margin/isolated/accountLimit | Query Enabled Isolated Margin Account Limit (USER_DATA) |
| GET | /sapi/v1/margin/isolated/allPairs | Get All Isolated Margin Symbol(USER_DATA) |
| POST | /sapi/v1/bnbBurn | Toggle BNB Burn On Spot Trade And Margin Interest (USER_DATA) |
| GET | /sapi/v1/bnbBurn | Get BNB Burn Status(USER_DATA) |
| GET | /sapi/v1/margin/interestRateHistory | Margin Interest Rate History (USER_DATA) |
| GET | /sapi/v1/margin/crossMarginData | Query Cross Margin Fee Data (USER_DATA) |
| GET | /sapi/v1/margin/isolatedMarginData | Query Isolated Margin Fee Data (USER_DATA) |
| GET | /sapi/v1/margin/isolatedMarginTier | Query Isolated Margin Tier Data (USER_DATA) |
| GET | /sapi/v1/margin/rateLimit/order | Query Current Margin Order Count Usage (TRADE) |
| GET | /sapi/v1/margin/crossMarginCollateralRatio | Cross margin collateral ratio (MARKET_DATA) |
| GET | /sapi/v1/margin/exchange-small-liability | Get Small Liability Exchange Coin List (USER_DATA) |
| GET | /sapi/v1/margin/exchange-small-liability-history | Get Small Liability Exchange History (USER_DATA) |
| GET | /sapi/v1/margin/next-hourly-interest-rate | Get a future hourly interest rate (USER_DATA) |
| GET | /sapi/v1/margin/capital-flow | Get cross or isolated margin capital flow(USER_DATA) |
| GET | /sapi/v1/margin/delist-schedule | Get tokens or symbols delist schedule for cross margin and isolated margin (MARKET_DATA) |
| GET | /sapi/v1/margin/available-inventory | Query Margin Available Inventory (USER_DATA) |
| POST | /sapi/v1/margin/manual-liquidation | Margin manual liquidation(MARGIN) |
| POST | /sapi/v1/margin/order/oto | Margin Account New OTO (TRADE) |
| POST | /sapi/v1/margin/order/otoco | Margin Account New OTOCO (TRADE) |
| POST | /sapi/v1/margin/max-leverage | Adjust cross margin max leverage (USER_DATA) |
| GET | /sapi/v1/margin/leverageBracket | Query Liability Coin Leverage Bracket in Cross Margin Pro Mode (MARKET_DATA) |
| GET | /sapi/v1/system/status | System Status (System) |
| GET | /sapi/v1/capital/config/getall | All Coins' Information (USER_DATA) |
| GET | /sapi/v1/accountSnapshot | Daily Account Snapshot (USER_DATA) |
| POST | /sapi/v1/account/disableFastWithdrawSwitch | Disable Fast Withdraw Switch (USER_DATA) |
| POST | /sapi/v1/account/enableFastWithdrawSwitch | Enable Fast Withdraw Switch (USER_DATA) |
| POST | /sapi/v1/capital/withdraw/apply | Withdraw (USER_DATA) |
| GET | /sapi/v1/capital/deposit/hisrec | Deposit History(supporting network) (USER_DATA) |
| GET | /sapi/v1/capital/withdraw/history | Withdraw History (supporting network) (USER_DATA) |
| GET | /sapi/v1/capital/deposit/address | Deposit Address (supporting network) (USER_DATA) |
| GET | /sapi/v1/account/status | Account Status (USER_DATA) |
| GET | /sapi/v1/account/apiTradingStatus | Account API Trading Status (USER_DATA) |
| GET | /sapi/v1/asset/dribblet | DustLog(USER_DATA) |
| POST | /sapi/v1/asset/dust-btc | Get Assets That Can Be Converted Into BNB (USER_DATA) |
| POST | /sapi/v1/asset/dust | Dust Transfer (USER_DATA) |
| GET | /sapi/v1/asset/assetDividend | Asset Dividend Record (USER_DATA) |
| GET | /sapi/v1/asset/assetDetail | Asset Detail (USER_DATA) |
| GET | /sapi/v1/asset/tradeFee | Trade Fee (USER_DATA) |
| GET | /sapi/v1/asset/transfer | Query User Universal Transfer History (USER_DATA) |
| POST | /sapi/v1/asset/transfer | User Universal Transfer (USER_DATA) |
| POST | /sapi/v1/asset/get-funding-asset | Funding Wallet (USER_DATA) |
| POST | /sapi/v3/asset/getUserAsset | User Asset (USER_DATA) |
| POST | /sapi/v1/asset/convert-transfer | Convert Transfer (USER_DATA) |
| GET | /sapi/v1/asset/convert-transfer/queryByPage | Query Convert Transfer (USER_DATA) |
| GET | /sapi/v1/asset/ledger-transfer/cloud-mining/queryByPage | Get Cloud-Mining payment and refund history (USER_DATA) |
| GET | /sapi/v1/account/apiRestrictions | Get API Key Permission (USER_DATA) |
| GET | /sapi/v1/capital/contract/convertible-coins | Query auto-converting stable coins (USER_DATA) |
| POST | /sapi/v1/capital/contract/convertible-coins | Switch on/off BUSD and stable coins conversion (USER_DATA) (USER_DATA) |
| POST | /sapi/v1/sub-account/virtualSubAccount | Create a Virtual Sub-account(For Master Account) |
| GET | /sapi/v1/sub-account/list | Query Sub-account List (For Master Account) |
| GET | /sapi/v1/sub-account/sub/transfer/history | Sub-account Spot Asset Transfer History (For Master Account) |
| GET | /sapi/v1/sub-account/futures/internalTransfer | Sub-account Futures Asset Transfer History (For Master Account) |
| POST | /sapi/v1/sub-account/futures/internalTransfer | Sub-account Futures Asset Transfer (For Master Account) |
| GET | /sapi/v3/sub-account/assets | Sub-account Assets (For Master Account) |
| GET | /sapi/v1/sub-account/spotSummary | Sub-account Spot Assets Summary (For Master Account) |
| GET | /sapi/v1/capital/deposit/subAddress | Sub-account Spot Assets Summary (For Master Account) |
| GET | /sapi/v1/capital/deposit/subHisrec | Sub-account Deposit History (For Master Account) |
| POST | /sapi/v1/capital/deposit/credit-apply | One click arrival deposit apply (USER_DATA) |
| GET | /sapi/v1/asset/wallet/balance | Query User Wallet Balance (USER_DATA) |
| GET | /sapi/v1/asset/custody/transfer-history | Query User Delegation History(For Master Account) (USER_DATA) |
| GET | /sapi/v1/capital/deposit/address/list | Fetch deposit address list with network (USER_DATA) |
| GET | /sapi/v1/spot/delist-schedule | Get symbols delist schedule for spot (MARKET_DATA) |
| GET | /sapi/v1/capital/withdraw/address/list | Fetch withdraw address list (USER_DATA) |
| GET | /sapi/v1/account/info | Account info (USER_DATA) |
| GET | /sapi/v1/sub-account/status | Sub-account's Status on Margin/Futures (For Master Account) |
| POST | /sapi/v1/sub-account/margin/enable | Enable Margin for Sub-account (For Master Account) |
| GET | /sapi/v1/sub-account/margin/account | Detail on Sub-account's Margin Account (For Master Account) |
| GET | /sapi/v1/sub-account/margin/accountSummary | Summary of Sub-account's Margin Account (For Master Account) |
| POST | /sapi/v1/sub-account/futures/enable | Enable Futures for Sub-account (For Master Account) |
| GET | /sapi/v1/sub-account/futures/account | Detail on Sub-account's Futures Account (For Master Account) |
| GET | /sapi/v1/sub-account/futures/accountSummary | Summary of Sub-account's Futures Account (For Master Account) |
| GET | /sapi/v1/sub-account/futures/positionRisk | Futures Position-Risk of Sub-account (For Master Account) |
| POST | /sapi/v1/sub-account/futures/transfer | Transfer for Sub-account (For Master Account) |
| POST | /sapi/v1/sub-account/margin/transfer | Margin Transfer for Sub-account (For Master Account) |
| POST | /sapi/v1/sub-account/transfer/subToSub | Transfer to Sub-account of Same Master (For Sub-account) |
| POST | /sapi/v1/sub-account/transfer/subToMaster | Transfer to Master (For Sub-account) |
| GET | /sapi/v1/sub-account/transfer/subUserHistory | Sub-account Transfer History (For Sub-account) |
| GET | /sapi/v1/sub-account/universalTransfer | Universal Transfer History (For Master Account) |
| POST | /sapi/v1/sub-account/universalTransfer | Universal Transfer (For Master Account) |
| GET | /sapi/v2/sub-account/futures/account | Detail on Sub-account's Futures Account V2 (For Master Account) |
| GET | /sapi/v2/sub-account/futures/accountSummary | Summary of Sub-account's Futures Account V2 (For Master Account) |
| GET | /sapi/v2/sub-account/futures/positionRisk | Futures Position-Risk of Sub-account V2 (For Master Account) |
| POST | /sapi/v1/sub-account/blvt/enable | Enable Leverage Token for Sub-account (For Master Account) |
| POST | /sapi/v1/managed-subaccount/deposit | Deposit assets into the managed sub-account(For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/asset | Managed sub-account asset details(For Investor Master Account) |
| POST | /sapi/v1/managed-subaccount/withdraw | Withdrawl assets from the managed sub-account(For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/accountSnapshot | Managed sub-account snapshot (For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/queryTransLogForInvestor | Query Managed Sub Account Transfer Log (For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/queryTransLogForTradeParent | Query Managed Sub Account Transfer Log (For Trading Team Master Account) |
| GET | /sapi/v1/managed-subaccount/fetch-future-asset | Query Managed Sub-account Futures Asset Details (For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/marginAsset | Query Managed Sub-account Margin Asset Details (For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/info | Query Managed Sub-account List (For Investor) |
| GET | /sapi/v1/managed-subaccount/deposit/address | Get Managed Sub-account Deposit Address (For Investor Master Account) |
| GET | /sapi/v1/managed-subaccount/query-trans-log | Query Managed Sub Account Transfer Log (For Trading Team Sub Account)(USER_DATA) |
| GET | /sapi/v1/sub-account/subAccountApi/ipRestriction | Get IP Restriction for a Sub-account API Key (For Master Account) |
| DELETE | /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList | Delete IP List for a Sub-account API Key (For Master Account) |
| GET | /sapi/v1/sub-account/transaction-statistics | Query Sub-account Transaction Statistics (For Master Account) |
| POST | /sapi/v1/sub-account/eoptions/enable | Enable Options for Sub-account (For Master Account)(USER_DATA) |
| POST | /sapi/v2/sub-account/subAccountApi/ipRestriction | Update IP Restriction for Sub-Account API key (For Master Account) |
| GET | /sapi/v4/sub-account/assets | Query Sub-account Assets (For Master Account) |
| POST | /sapi/v1/userDataStream | Create a ListenKey (USER_STREAM) |
| PUT | /sapi/v1/userDataStream | Ping/Keep-alive a ListenKey (USER_STREAM) |
| DELETE | /sapi/v1/userDataStream | Close a ListenKey (USER_STREAM) |
| POST | /sapi/v1/userDataStream/isolated | Generate a Listen Key (USER_STREAM) |
| PUT | /sapi/v1/userDataStream/isolated | Ping/Keep-alive a Listen Key (USER_STREAM) |
| DELETE | /sapi/v1/userDataStream/isolated | Close a ListenKey (USER_STREAM) |
| GET | /sapi/v1/fiat/orders | Fiat Deposit/Withdraw History (USER_DATA) |
| GET | /sapi/v1/fiat/payments | Fiat Payments History (USER_DATA) |
| GET | /sapi/v1/lending/project/list | Get Fixed/Activity Project List(USER_DATA) |
| POST | /sapi/v1/lending/customizedFixed/purchase | Purchase Fixed/Activity Project (USER_DATA) |
| GET | /sapi/v1/lending/project/position/list | Get Fixed/Activity Project Position (USER_DATA) |
| POST | /sapi/v1/lending/positionChanged | Change Fixed/Activity Position to Daily Position (USER_DATA) |
| GET | /sapi/v1/mining/pub/algoList | Acquiring Algorithm (MARKET_DATA) |
| GET | /sapi/v1/mining/pub/coinList | Acquiring CoinName (MARKET_DATA) |
| GET | /sapi/v1/mining/worker/detail | Request for Detail Miner List (USER_DATA) |
| GET | /sapi/v1/mining/worker/list | Request for Miner List (USER_DATA) |
| GET | /sapi/v1/mining/payment/list | Earnings List (USER_DATA) |
| GET | /sapi/v1/mining/payment/other | Extra Bonus List (USER_DATA) |
| GET | /sapi/v1/mining/hash-transfer/config/details/list | Hashrate Resale List (USER_DATA) |
| GET | /sapi/v1/mining/hash-transfer/profit/details | Hashrate Resale Details (USER_DATA) |
| POST | /sapi/v1/mining/hash-transfer/config | Hashrate Resale Request (USER_DATA) |
| POST | /sapi/v1/mining/hash-transfer/config/cancel | Cancel Hashrate Resale configuration (USER_DATA) |
| GET | /sapi/v1/mining/statistics/user/status | Statistic List (USER_DATA) |
| GET | /sapi/v1/mining/statistics/user/list | Account List (USER_DATA) |
| GET | /sapi/v1/mining/payment/uid | Mining Account Earning (USER_DATA) |
| POST | /sapi/v1/futures/transfer | New Future Account Transfer (USER_DATA) |
| GET | /sapi/v1/futures/transfer | Get Future Account Transaction History List (USER_DATA) |
| GET | /sapi/v1/futures/histDataLink | Get Future TickLevel Orderbook Historical Data Download Link (USER_DATA) |
| POST | /sapi/v1/algo/futures/newOrderVp | Volume Participation(VP) New Order (TRADE) |
| POST | /sapi/v1/algo/futures/newOrderTwap | Time-Weighted Average Price(Twap) New Order (TRADE) |
| DELETE | /sapi/v1/algo/futures/order | Cancel Algo Order(TRADE) |
| GET | /sapi/v1/algo/futures/openOrders | Query Current Algo Open Orders (USER_DATA) |
| GET | /sapi/v1/algo/futures/historicalOrders | Query Historical Algo Orders (USER_DATA) |
| GET | /sapi/v1/algo/futures/subOrders | Query Sub Orders (USER_DATA) |
| POST | /sapi/v1/algo/spot/newOrderTwap | Time-Weighted Average Price (Twap) New Order |
| DELETE | /sapi/v1/algo/spot/order | Cancel Algo Order |
| GET | /sapi/v1/algo/spot/openOrders | Query Current Algo Open Orders |
| GET | /sapi/v1/algo/spot/historicalOrders | Query Historical Algo Orders |
| GET | /sapi/v1/algo/spot/subOrders | Query Sub Orders |
| GET | /sapi/v1/portfolio/account | Portfolio Margin Account (USER_DATA) |
| GET | /sapi/v1/portfolio/collateralRate | Portfolio Margin Collateral Rate (MARKET_DATA) |
| GET | /sapi/v2/portfolio/collateralRate | Portfolio Margin Pro Tiered Collateral Rate(USER_DATA) |
| GET | /sapi/v1/portfolio/pmLoan | Portfolio Margin Bankruptcy Loan Amount (USER_DATA) |
| POST | /sapi/v1/portfolio/repay | Portfolio Margin Bankruptcy Loan Repay (USER_DATA) |
| GET | /sapi/v1/portfolio/interest-history | Query Classic Portfolio Margin Negative Balance Interest History (USER_DATA) |
| GET | /sapi/v1/portfolio/asset-index-price | Query Portfolio Margin Asset Index Price (MARKET_DATA) |
| POST | /sapi/v1/portfolio/auto-collection | Fund Auto-collection (USER_DATA) |
| POST | /sapi/v1/portfolio/bnb-transfer | BNB Transfer (USER_DATA) |
| POST | /sapi/v1/portfolio/repay-futures-switch | Change Auto-repay-futures Status (USER_DATA) |
| GET | /sapi/v1/portfolio/repay-futures-switch | Get Auto-repay-futures Status (USER_DATA) |
| POST | /sapi/v1/portfolio/repay-futures-negative-balance | Repay futures Negative Balance (USER_DATA) |
| GET | /sapi/v1/portfolio/margin-asset-leverage | Get Portfolio Margin Asset Leverage (USER_DATA) |
| POST | /sapi/v1/portfolio/asset-collection | Fund Collection by Asset (USER_DATA) |
| GET | /sapi/v1/blvt/tokenInfo | BLVT Info (MARKET_DATA) |
| POST | /sapi/v1/blvt/subscribe | Subscribe BLVT (USER_DATA) |
| GET | /sapi/v1/blvt/subscribe/record | Query Subscription Record (USER_DATA) |
| POST | /sapi/v1/blvt/redeem | Redeem BLVT (USER_DATA) |
| GET | /sapi/v1/blvt/redeem/record | Redemption Record (USER_DATA) |
| GET | /sapi/v1/blvt/userLimit | BLVT User Limit Info (USER_DATA) |
| GET | /sapi/v1/c2c/orderMatch/listUserOrderHistory | Get C2C Trade History (USER_DATA) |
| GET | /sapi/v1/loan/vip/ongoing/orders | Get VIP Loan Ongoing Orders (USER_DATA) |
| POST | /sapi/v1/loan/vip/repay | VIP Loan Repay (TRADE) |
| GET | /sapi/v1/loan/vip/repay/history | Get VIP Loan Repayment History (USER_DATA) |
| GET | /sapi/v1/loan/vip/collateral/account | Check Locked Value of VIP Collateral Account (USER_DATA) |
| POST | /sapi/v1/loan/vip/borrow | VIP Loan Borrow |
| GET | /sapi/v1/loan/vip/loanable/data | Get Loanable Assets Data |
| GET | /sapi/v1/loan/vip/collateral/data | Get Collateral Asset Data (USER_DATA) |
| GET | /sapi/v1/loan/vip/request/data | Query Application Status (USER_DATA) |
| GET | /sapi/v1/loan/vip/request/interestRate | Get Borrow Interest Rate (USER_DATA) |
| POST | /sapi/v1/loan/vip/renew | VIP Loan Renew |
| GET | /sapi/v1/loan/income | Get Crypto Loans Income History (USER_DATA) |
| POST | /sapi/v1/loan/borrow | Crypto Loan Borrow (TRADE) |
| GET | /sapi/v1/loan/borrow/history | Get Crypto Loans Borrow History (USER_DATA) |
| GET | /sapi/v1/loan/ongoing/orders | Get Loan Ongoing Orders (USER_DATA) |
| POST | /sapi/v1/loan/repay | Crypto Loan Repay (TRADE) |
| GET | /sapi/v1/loan/repay/history | Get Loan Repayment History (USER_DATA) |
| POST | /sapi/v1/loan/adjust/ltv | Crypto Loan Adjust LTV (TRADE) |
| GET | /sapi/v1/loan/ltv/adjustment/history | Get Loan LTV Adjustment History (USER_DATA) |
| GET | /sapi/v1/loan/loanable/data | Get Loanable Assets Data (USER_DATA) |
| GET | /sapi/v1/loan/collateral/data | Get Collateral Assets Data (USER_DATA) |
| GET | /sapi/v1/loan/repay/collateral/rate | Check Collateral Repay Rate (USER_DATA) |
| POST | /sapi/v1/loan/customize/margin_call | Crypto Loan Customize Margin Call (TRADE) |
| POST | /sapi/v2/loan/flexible/borrow | Borrow - Flexible Loan Borrow (TRADE) |
| GET | /sapi/v2/loan/flexible/ongoing/orders | Borrow - Get Flexible Loan Ongoing Orders (USER_DATA) |
| GET | /sapi/v2/loan/flexible/borrow/history | Borrow - Get Flexible Loan Borrow History (USER_DATA) |
| POST | /sapi/v2/loan/flexible/repay | Repay - Flexible Loan Repay (TRADE) |
| GET | /sapi/v2/loan/flexible/repay/history | Repay - Get Flexible Loan Repayment History (USER_DATA) |
| POST | /sapi/v2/loan/flexible/adjust/ltv | Adjust LTV - Flexible Loan Adjust LTV (TRADE) |
| GET | /sapi/v2/loan/flexible/ltv/adjustment/history | Adjust LTV - Get Flexible Loan LTV Adjustment History (USER_DATA) |
| GET | /sapi/v2/loan/flexible/loanable/data | Get Flexible Loan Assets Data (USER_DATA) |
| GET | /sapi/v2/loan/flexible/collateral/data | Get Flexible Loan Collateral Assets Data (USER_DATA) |
| GET | /sapi/v1/pay/transactions | Get Pay Trade History (USER_DATA) |
| GET | /sapi/v1/convert/exchangeInfo | List All Convert Pairs |
| GET | /sapi/v1/convert/assetInfo | Query order quantity precision per asset (USER_DATA) |
| POST | /sapi/v1/convert/getQuote | Send quote request (USER_DATA) |
| POST | /sapi/v1/convert/acceptQuote | Accept Quote (TRADE) |
| GET | /sapi/v1/convert/orderStatus | Order status (USER_DATA) |
| POST | /sapi/v1/convert/limit/placeOrder | Place limit order (USER_DATA) |
| POST | /sapi/v1/convert/limit/cancelOrder | Cancel limit order (USER_DATA) |
| GET | /sapi/v1/convert/limit/queryOpenOrders | Query limit open orders (USER_DATA) |
| GET | /sapi/v1/convert/tradeFlow | Get Convert Trade History (USER_DATA) |
| GET | /sapi/v1/rebate/taxQuery | Get Spot Rebate History Records (USER_DATA) |
| GET | /sapi/v1/nft/history/transactions | Get NFT Transaction History (USER_DATA) |
| GET | /sapi/v1/nft/history/deposit | Get NFT Deposit History(USER_DATA) |
| GET | /sapi/v1/nft/history/withdraw | Get NFT Withdraw History (USER_DATA) |
| GET | /sapi/v1/nft/user/getAsset | Get NFT Asset (USER_DATA) |
| POST | /sapi/v1/giftcard/createCode | Create a Binance Code (USER_DATA) |
| POST | /sapi/v1/giftcard/redeemCode | Redeem a Binance Code (USER_DATA) |
| GET | /sapi/v1/giftcard/verify | Verify a Binance Code (USER_DATA) |
| GET | /sapi/v1/giftcard/cryptography/rsa-public-key | Fetch RSA Public Key (USER_DATA) |
| POST | /sapi/v1/giftcard/buyCode | Buy a Binance Code (TRADE) |
| GET | /sapi/v1/giftcard/buyCode/token-limit | Fetch Token Limit (USER_DATA) |
| GET | /sapi/v1/lending/auto-invest/target-asset/list | Get target asset list (USER_DATA) |
| GET | /sapi/v1/lending/auto-invest/target-asset/roi/list | Get target asset ROI data (USER_DATA) |
| GET | /sapi/v1/lending/auto-invest/all/asset | Query all source asset and target asset (USER_DATA) |
| GET | /sapi/v1/lending/auto-invest/source-asset/list | Query source asset list (USER_DATA) |
| POST | /sapi/v1/lending/auto-invest/plan/add | Investment plan creation (USER_DATA) |
| POST | /sapi/v1/lending/auto-invest/plan/edit | Investment plan adjustment |
| POST | /sapi/v1/lending/auto-invest/plan/edit-status | Change Plan Status |
| GET | /sapi/v1/lending/auto-invest/plan/list | Get list of plans |
| GET | /sapi/v1/lending/auto-invest/plan/id | Query holding details of the plan |
| GET | /sapi/v1/lending/auto-invest/history/list | Query subscription transaction history |
| GET | /sapi/v1/lending/auto-invest/index/info | Query Index Details(USER_DATA) |
| GET | /sapi/v1/lending/auto-invest/index/user-summary | Query Index Linked Plan Position Details(USER_DATA) |
| POST | /sapi/v1/lending/auto-invest/one-off | One Time Transaction(TRADE) |
| GET | /sapi/v1/lending/auto-invest/one-off/status | Query One-Time Transaction Status (USER_DATA) |
| POST | /sapi/v1/lending/auto-invest/redeem | Index Linked Plan Redemption (TRADE) |
| GET | /sapi/v1/lending/auto-invest/redeem/history | Index Linked Plan Redemption History (USER_DATA) |
| GET | /sapi/v1/lending/auto-invest/rebalance/history | Index Linked Plan Rebalance Details (USER_DATA) |
| POST | /sapi/v2/eth-staking/eth/stake | Subscribe ETH Staking V2(TRADE) |
| POST | /sapi/v1/eth-staking/eth/redeem | Redeem ETH (TRADE) |
| GET | /sapi/v1/eth-staking/eth/history/stakingHistory | Get ETH staking history (USER_DATA) |
| GET | /sapi/v1/eth-staking/eth/history/redemptionHistory | Get ETH redemption history (USER_DATA) |
| GET | /sapi/v1/eth-staking/eth/history/rewardsHistory | Get BETH rewards distribution history(USER_DATA) |
| GET | /sapi/v1/eth-staking/eth/quota | Get current ETH staking quota (USER_DATA) |
| GET | /sapi/v1/eth-staking/eth/history/rateHistory | Get WBETH Rate History (USER_DATA) |
| GET | /sapi/v2/eth-staking/account | ETH Staking account V2(USER_DATA) |
| POST | /sapi/v1/eth-staking/wbeth/wrap | Wrap BETH(TRADE) |
| GET | /sapi/v1/eth-staking/wbeth/history/wrapHistory | Get WBETH wrap history (USER_DATA) |
| GET | /sapi/v1/eth-staking/wbeth/history/unwrapHistory | Get WBETH unwrap history (USER_DATA) |
| GET | /sapi/v1/eth-staking/eth/history/wbethRewardsHistory | Get WBETH rewards history(USER_DATA) |
| GET | /sapi/v1/copyTrading/futures/userStatus | Get Futures Lead Trader Status(TRADE) |
| GET | /sapi/v1/copyTrading/futures/leadSymbol | Get Futures Lead Trading Symbol Whitelist(USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/list | Get Simple Earn Flexible Product List (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/list | Get Simple Earn Locked Product List (USER_DATA) |
| POST | /sapi/v1/simple-earn/flexible/subscribe | Subscribe Flexible Product (TRADE) |
| POST | /sapi/v1/simple-earn/locked/subscribe | Subscribe Locked Product (TRADE) |
| POST | /sapi/v1/simple-earn/flexible/redeem | Redeem Flexible Product (TRADE) |
| POST | /sapi/v1/simple-earn/locked/redeem | Redeem Locked Product (TRADE) |
| GET | /sapi/v1/simple-earn/flexible/position | Get Flexible Product Position (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/position | Get Locked Product Position (USER_DATA) |
| GET | /sapi/v1/simple-earn/account | Simple Account (USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/history/subscriptionRecord | Get Flexible Subscription Record (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/history/subscriptionRecord | Get Locked Subscription Record (USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/history/redemptionRecord | Get Flexible Redemption Record (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/history/redemptionRecord | Get Locked Redemption Record (USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/history/rewardsRecord | Get Flexible Rewards History (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/history/rewardsRecord | Get Locked Rewards History (USER_DATA) |
| POST | /sapi/v1/simple-earn/flexible/setAutoSubscribe | Set Flexible Auto Subscribe (USER_DATA) |
| POST | /sapi/v1/simple-earn/locked/setAutoSubscribe | Set Locked Auto Subscribe (USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/personalLeftQuota | Get Flexible Personal Left Quota (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/personalLeftQuota | Get Locked Personal Left Quota (USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/subscriptionPreview | Get Flexible Subscription Preview (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/subscriptionPreview | Get Locked Subscription Preview (USER_DATA) |
| GET | /sapi/v1/simple-earn/locked/setRedeemOption | Set Locked Product Redeem Option(USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/history/rateHistory | Get Rate History (USER_DATA) |
| GET | /sapi/v1/simple-earn/flexible/history/collateralRecord | Get Collateral Record (USER_DATA) |
| GET | /sapi/v1/dci/product/list | Get Dual Investment product list(USER_DATA) |
| POST | /sapi/v1/dci/product/subscribe | Subscribe Dual Investment products(USER_DATA) |
| GET | /sapi/v1/dci/product/positions | Get Dual Investment positions(USER_DATA) |
| GET | /sapi/v1/dci/product/accounts | Check Dual Investment accounts(USER_DATA) |
| POST | /sapi/v1/dci/product/auto_compound/edit-status | Change Auto-Compound status(USER_DATA) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all ping?" -> GET /api/v3/ping
- "List all time?" -> GET /api/v3/time
- "List all exchangeInfo?" -> GET /api/v3/exchangeInfo
- "List all depth?" -> GET /api/v3/depth
- "List all trades?" -> GET /api/v3/trades
- "List all historicalTrades?" -> GET /api/v3/historicalTrades
- "List all aggTrades?" -> GET /api/v3/aggTrades
- "List all klines?" -> GET /api/v3/klines
- "List all uiKlines?" -> GET /api/v3/uiKlines
- "List all avgPrice?" -> GET /api/v3/avgPrice
- "List all 24hr?" -> GET /api/v3/ticker/24hr
- "List all tradingDay?" -> GET /api/v3/ticker/tradingDay
- "List all price?" -> GET /api/v3/ticker/price
- "List all bookTicker?" -> GET /api/v3/ticker/bookTicker
- "List all ticker?" -> GET /api/v3/ticker
- "Create a test?" -> POST /api/v3/order/test
- "List all order?" -> GET /api/v3/order
- "Create a order?" -> POST /api/v3/order
- "Create a cancelReplace?" -> POST /api/v3/order/cancelReplace
- "List all openOrders?" -> GET /api/v3/openOrders
- "List all allOrders?" -> GET /api/v3/allOrders
- "Create a oco?" -> POST /api/v3/orderList/oco
- "Create a oto?" -> POST /api/v3/orderList/oto
- "Create a otoco?" -> POST /api/v3/orderList/otoco
- "List all orderList?" -> GET /api/v3/orderList
- "List all allOrderList?" -> GET /api/v3/allOrderList
- "List all openOrderList?" -> GET /api/v3/openOrderList
- "Create a order?" -> POST /api/v3/sor/order
- "Create a test?" -> POST /api/v3/sor/order/test
- "List all account?" -> GET /api/v3/account
- "List all myTrades?" -> GET /api/v3/myTrades
- "List all order?" -> GET /api/v3/rateLimit/order
- "List all myPreventedMatches?" -> GET /api/v3/myPreventedMatches
- "List all myAllocations?" -> GET /api/v3/myAllocations
- "List all commission?" -> GET /api/v3/account/commission
- "Create a borrow-repay?" -> POST /sapi/v1/margin/borrow-repay
- "List all borrow-repay?" -> GET /sapi/v1/margin/borrow-repay
- "List all transfer?" -> GET /sapi/v1/margin/transfer
- "List all allAssets?" -> GET /sapi/v1/margin/allAssets
- "List all allPairs?" -> GET /sapi/v1/margin/allPairs
- "List all priceIndex?" -> GET /sapi/v1/margin/priceIndex
- "List all order?" -> GET /sapi/v1/margin/order
- "Create a order?" -> POST /sapi/v1/margin/order
- "List all interestHistory?" -> GET /sapi/v1/margin/interestHistory
- "List all forceLiquidationRec?" -> GET /sapi/v1/margin/forceLiquidationRec
- "List all account?" -> GET /sapi/v1/margin/account
- "List all openOrders?" -> GET /sapi/v1/margin/openOrders
- "List all allOrders?" -> GET /sapi/v1/margin/allOrders
- "Create a oco?" -> POST /sapi/v1/margin/order/oco
- "List all orderList?" -> GET /sapi/v1/margin/orderList
- "List all allOrderList?" -> GET /sapi/v1/margin/allOrderList
- "List all openOrderList?" -> GET /sapi/v1/margin/openOrderList
- "List all myTrades?" -> GET /sapi/v1/margin/myTrades
- "List all maxBorrowable?" -> GET /sapi/v1/margin/maxBorrowable
- "List all maxTransferable?" -> GET /sapi/v1/margin/maxTransferable
- "List all tradeCoeff?" -> GET /sapi/v1/margin/tradeCoeff
- "List all account?" -> GET /sapi/v1/margin/isolated/account
- "Create a account?" -> POST /sapi/v1/margin/isolated/account
- "List all accountLimit?" -> GET /sapi/v1/margin/isolated/accountLimit
- "List all allPairs?" -> GET /sapi/v1/margin/isolated/allPairs
- "Create a bnbBurn?" -> POST /sapi/v1/bnbBurn
- "List all bnbBurn?" -> GET /sapi/v1/bnbBurn
- "List all interestRateHistory?" -> GET /sapi/v1/margin/interestRateHistory
- "List all crossMarginData?" -> GET /sapi/v1/margin/crossMarginData
- "List all isolatedMarginData?" -> GET /sapi/v1/margin/isolatedMarginData
- "List all isolatedMarginTier?" -> GET /sapi/v1/margin/isolatedMarginTier
- "List all order?" -> GET /sapi/v1/margin/rateLimit/order
- "List all crossMarginCollateralRatio?" -> GET /sapi/v1/margin/crossMarginCollateralRatio
- "List all exchange-small-liability?" -> GET /sapi/v1/margin/exchange-small-liability
- "List all exchange-small-liability-history?" -> GET /sapi/v1/margin/exchange-small-liability-history
- "List all next-hourly-interest-rate?" -> GET /sapi/v1/margin/next-hourly-interest-rate
- "List all capital-flow?" -> GET /sapi/v1/margin/capital-flow
- "List all delist-schedule?" -> GET /sapi/v1/margin/delist-schedule
- "List all available-inventory?" -> GET /sapi/v1/margin/available-inventory
- "Create a manual-liquidation?" -> POST /sapi/v1/margin/manual-liquidation
- "Create a oto?" -> POST /sapi/v1/margin/order/oto
- "Create a otoco?" -> POST /sapi/v1/margin/order/otoco
- "Create a max-leverage?" -> POST /sapi/v1/margin/max-leverage
- "List all leverageBracket?" -> GET /sapi/v1/margin/leverageBracket
- "List all status?" -> GET /sapi/v1/system/status
- "List all getall?" -> GET /sapi/v1/capital/config/getall
- "List all accountSnapshot?" -> GET /sapi/v1/accountSnapshot
- "Create a disableFastWithdrawSwitch?" -> POST /sapi/v1/account/disableFastWithdrawSwitch
- "Create a enableFastWithdrawSwitch?" -> POST /sapi/v1/account/enableFastWithdrawSwitch
- "Create a apply?" -> POST /sapi/v1/capital/withdraw/apply
- "List all hisrec?" -> GET /sapi/v1/capital/deposit/hisrec
- "List all history?" -> GET /sapi/v1/capital/withdraw/history
- "List all address?" -> GET /sapi/v1/capital/deposit/address
- "List all status?" -> GET /sapi/v1/account/status
- "List all apiTradingStatus?" -> GET /sapi/v1/account/apiTradingStatus
- "List all dribblet?" -> GET /sapi/v1/asset/dribblet
- "Create a dust-btc?" -> POST /sapi/v1/asset/dust-btc
- "Create a dust?" -> POST /sapi/v1/asset/dust
- "List all assetDividend?" -> GET /sapi/v1/asset/assetDividend
- "List all assetDetail?" -> GET /sapi/v1/asset/assetDetail
- "List all tradeFee?" -> GET /sapi/v1/asset/tradeFee
- "List all transfer?" -> GET /sapi/v1/asset/transfer
- "Create a transfer?" -> POST /sapi/v1/asset/transfer
- "Create a get-funding-asset?" -> POST /sapi/v1/asset/get-funding-asset
- "Create a getUserAsset?" -> POST /sapi/v3/asset/getUserAsset
- "Create a convert-transfer?" -> POST /sapi/v1/asset/convert-transfer
- "List all queryByPage?" -> GET /sapi/v1/asset/convert-transfer/queryByPage
- "List all queryByPage?" -> GET /sapi/v1/asset/ledger-transfer/cloud-mining/queryByPage
- "List all apiRestrictions?" -> GET /sapi/v1/account/apiRestrictions
- "List all convertible-coins?" -> GET /sapi/v1/capital/contract/convertible-coins
- "Create a convertible-coin?" -> POST /sapi/v1/capital/contract/convertible-coins
- "Create a virtualSubAccount?" -> POST /sapi/v1/sub-account/virtualSubAccount
- "List all list?" -> GET /sapi/v1/sub-account/list
- "List all history?" -> GET /sapi/v1/sub-account/sub/transfer/history
- "List all internalTransfer?" -> GET /sapi/v1/sub-account/futures/internalTransfer
- "Create a internalTransfer?" -> POST /sapi/v1/sub-account/futures/internalTransfer
- "List all assets?" -> GET /sapi/v3/sub-account/assets
- "List all spotSummary?" -> GET /sapi/v1/sub-account/spotSummary
- "List all subAddress?" -> GET /sapi/v1/capital/deposit/subAddress
- "List all subHisrec?" -> GET /sapi/v1/capital/deposit/subHisrec
- "Create a credit-apply?" -> POST /sapi/v1/capital/deposit/credit-apply
- "List all balance?" -> GET /sapi/v1/asset/wallet/balance
- "List all transfer-history?" -> GET /sapi/v1/asset/custody/transfer-history
- "List all list?" -> GET /sapi/v1/capital/deposit/address/list
- "List all delist-schedule?" -> GET /sapi/v1/spot/delist-schedule
- "List all list?" -> GET /sapi/v1/capital/withdraw/address/list
- "List all info?" -> GET /sapi/v1/account/info
- "List all status?" -> GET /sapi/v1/sub-account/status
- "Create a enable?" -> POST /sapi/v1/sub-account/margin/enable
- "List all account?" -> GET /sapi/v1/sub-account/margin/account
- "List all accountSummary?" -> GET /sapi/v1/sub-account/margin/accountSummary
- "Create a enable?" -> POST /sapi/v1/sub-account/futures/enable
- "List all account?" -> GET /sapi/v1/sub-account/futures/account
- "List all accountSummary?" -> GET /sapi/v1/sub-account/futures/accountSummary
- "List all positionRisk?" -> GET /sapi/v1/sub-account/futures/positionRisk
- "Create a transfer?" -> POST /sapi/v1/sub-account/futures/transfer
- "Create a transfer?" -> POST /sapi/v1/sub-account/margin/transfer
- "Create a subToSub?" -> POST /sapi/v1/sub-account/transfer/subToSub
- "Create a subToMaster?" -> POST /sapi/v1/sub-account/transfer/subToMaster
- "List all subUserHistory?" -> GET /sapi/v1/sub-account/transfer/subUserHistory
- "List all universalTransfer?" -> GET /sapi/v1/sub-account/universalTransfer
- "Create a universalTransfer?" -> POST /sapi/v1/sub-account/universalTransfer
- "List all account?" -> GET /sapi/v2/sub-account/futures/account
- "List all accountSummary?" -> GET /sapi/v2/sub-account/futures/accountSummary
- "List all positionRisk?" -> GET /sapi/v2/sub-account/futures/positionRisk
- "Create a enable?" -> POST /sapi/v1/sub-account/blvt/enable
- "Create a deposit?" -> POST /sapi/v1/managed-subaccount/deposit
- "List all asset?" -> GET /sapi/v1/managed-subaccount/asset
- "Create a withdraw?" -> POST /sapi/v1/managed-subaccount/withdraw
- "List all accountSnapshot?" -> GET /sapi/v1/managed-subaccount/accountSnapshot
- "List all queryTransLogForInvestor?" -> GET /sapi/v1/managed-subaccount/queryTransLogForInvestor
- "List all queryTransLogForTradeParent?" -> GET /sapi/v1/managed-subaccount/queryTransLogForTradeParent
- "List all fetch-future-asset?" -> GET /sapi/v1/managed-subaccount/fetch-future-asset
- "List all marginAsset?" -> GET /sapi/v1/managed-subaccount/marginAsset
- "List all info?" -> GET /sapi/v1/managed-subaccount/info
- "List all address?" -> GET /sapi/v1/managed-subaccount/deposit/address
- "List all query-trans-log?" -> GET /sapi/v1/managed-subaccount/query-trans-log
- "List all ipRestriction?" -> GET /sapi/v1/sub-account/subAccountApi/ipRestriction
- "List all transaction-statistics?" -> GET /sapi/v1/sub-account/transaction-statistics
- "Create a enable?" -> POST /sapi/v1/sub-account/eoptions/enable
- "Create a ipRestriction?" -> POST /sapi/v2/sub-account/subAccountApi/ipRestriction
- "List all assets?" -> GET /sapi/v4/sub-account/assets
- "Create a userDataStream?" -> POST /api/v3/userDataStream
- "Create a userDataStream?" -> POST /sapi/v1/userDataStream
- "Create a isolated?" -> POST /sapi/v1/userDataStream/isolated
- "List all orders?" -> GET /sapi/v1/fiat/orders
- "List all payments?" -> GET /sapi/v1/fiat/payments
- "List all list?" -> GET /sapi/v1/lending/project/list
- "Create a purchase?" -> POST /sapi/v1/lending/customizedFixed/purchase
- "List all list?" -> GET /sapi/v1/lending/project/position/list
- "Create a positionChanged?" -> POST /sapi/v1/lending/positionChanged
- "List all algoList?" -> GET /sapi/v1/mining/pub/algoList
- "List all coinList?" -> GET /sapi/v1/mining/pub/coinList
- "List all detail?" -> GET /sapi/v1/mining/worker/detail
- "List all list?" -> GET /sapi/v1/mining/worker/list
- "List all list?" -> GET /sapi/v1/mining/payment/list
- "List all other?" -> GET /sapi/v1/mining/payment/other
- "List all list?" -> GET /sapi/v1/mining/hash-transfer/config/details/list
- "List all details?" -> GET /sapi/v1/mining/hash-transfer/profit/details
- "Create a config?" -> POST /sapi/v1/mining/hash-transfer/config
- "Create a cancel?" -> POST /sapi/v1/mining/hash-transfer/config/cancel
- "List all status?" -> GET /sapi/v1/mining/statistics/user/status
- "List all list?" -> GET /sapi/v1/mining/statistics/user/list
- "List all uid?" -> GET /sapi/v1/mining/payment/uid
- "Create a transfer?" -> POST /sapi/v1/futures/transfer
- "List all transfer?" -> GET /sapi/v1/futures/transfer
- "List all histDataLink?" -> GET /sapi/v1/futures/histDataLink
- "Create a newOrderVp?" -> POST /sapi/v1/algo/futures/newOrderVp
- "Create a newOrderTwap?" -> POST /sapi/v1/algo/futures/newOrderTwap
- "List all openOrders?" -> GET /sapi/v1/algo/futures/openOrders
- "List all historicalOrders?" -> GET /sapi/v1/algo/futures/historicalOrders
- "List all subOrders?" -> GET /sapi/v1/algo/futures/subOrders
- "Create a newOrderTwap?" -> POST /sapi/v1/algo/spot/newOrderTwap
- "List all openOrders?" -> GET /sapi/v1/algo/spot/openOrders
- "List all historicalOrders?" -> GET /sapi/v1/algo/spot/historicalOrders
- "List all subOrders?" -> GET /sapi/v1/algo/spot/subOrders
- "List all account?" -> GET /sapi/v1/portfolio/account
- "List all collateralRate?" -> GET /sapi/v1/portfolio/collateralRate
- "List all collateralRate?" -> GET /sapi/v2/portfolio/collateralRate
- "List all pmLoan?" -> GET /sapi/v1/portfolio/pmLoan
- "Create a repay?" -> POST /sapi/v1/portfolio/repay
- "List all interest-history?" -> GET /sapi/v1/portfolio/interest-history
- "List all asset-index-price?" -> GET /sapi/v1/portfolio/asset-index-price
- "Create a auto-collection?" -> POST /sapi/v1/portfolio/auto-collection
- "Create a bnb-transfer?" -> POST /sapi/v1/portfolio/bnb-transfer
- "Create a repay-futures-switch?" -> POST /sapi/v1/portfolio/repay-futures-switch
- "List all repay-futures-switch?" -> GET /sapi/v1/portfolio/repay-futures-switch
- "Create a repay-futures-negative-balance?" -> POST /sapi/v1/portfolio/repay-futures-negative-balance
- "List all margin-asset-leverage?" -> GET /sapi/v1/portfolio/margin-asset-leverage
- "Create a asset-collection?" -> POST /sapi/v1/portfolio/asset-collection
- "List all tokenInfo?" -> GET /sapi/v1/blvt/tokenInfo
- "Create a subscribe?" -> POST /sapi/v1/blvt/subscribe
- "List all record?" -> GET /sapi/v1/blvt/subscribe/record
- "Create a redeem?" -> POST /sapi/v1/blvt/redeem
- "List all record?" -> GET /sapi/v1/blvt/redeem/record
- "List all userLimit?" -> GET /sapi/v1/blvt/userLimit
- "List all listUserOrderHistory?" -> GET /sapi/v1/c2c/orderMatch/listUserOrderHistory
- "List all orders?" -> GET /sapi/v1/loan/vip/ongoing/orders
- "Create a repay?" -> POST /sapi/v1/loan/vip/repay
- "List all history?" -> GET /sapi/v1/loan/vip/repay/history
- "List all account?" -> GET /sapi/v1/loan/vip/collateral/account
- "Create a borrow?" -> POST /sapi/v1/loan/vip/borrow
- "List all data?" -> GET /sapi/v1/loan/vip/loanable/data
- "List all data?" -> GET /sapi/v1/loan/vip/collateral/data
- "List all data?" -> GET /sapi/v1/loan/vip/request/data
- "List all interestRate?" -> GET /sapi/v1/loan/vip/request/interestRate
- "Create a renew?" -> POST /sapi/v1/loan/vip/renew
- "List all income?" -> GET /sapi/v1/loan/income
- "Create a borrow?" -> POST /sapi/v1/loan/borrow
- "List all history?" -> GET /sapi/v1/loan/borrow/history
- "List all orders?" -> GET /sapi/v1/loan/ongoing/orders
- "Create a repay?" -> POST /sapi/v1/loan/repay
- "List all history?" -> GET /sapi/v1/loan/repay/history
- "Create a ltv?" -> POST /sapi/v1/loan/adjust/ltv
- "List all history?" -> GET /sapi/v1/loan/ltv/adjustment/history
- "List all data?" -> GET /sapi/v1/loan/loanable/data
- "List all data?" -> GET /sapi/v1/loan/collateral/data
- "List all rate?" -> GET /sapi/v1/loan/repay/collateral/rate
- "Create a margin_call?" -> POST /sapi/v1/loan/customize/margin_call
- "Create a borrow?" -> POST /sapi/v2/loan/flexible/borrow
- "List all orders?" -> GET /sapi/v2/loan/flexible/ongoing/orders
- "List all history?" -> GET /sapi/v2/loan/flexible/borrow/history
- "Create a repay?" -> POST /sapi/v2/loan/flexible/repay
- "List all history?" -> GET /sapi/v2/loan/flexible/repay/history
- "Create a ltv?" -> POST /sapi/v2/loan/flexible/adjust/ltv
- "List all history?" -> GET /sapi/v2/loan/flexible/ltv/adjustment/history
- "List all data?" -> GET /sapi/v2/loan/flexible/loanable/data
- "List all data?" -> GET /sapi/v2/loan/flexible/collateral/data
- "List all transactions?" -> GET /sapi/v1/pay/transactions
- "List all exchangeInfo?" -> GET /sapi/v1/convert/exchangeInfo
- "List all assetInfo?" -> GET /sapi/v1/convert/assetInfo
- "Create a getQuote?" -> POST /sapi/v1/convert/getQuote
- "Create a acceptQuote?" -> POST /sapi/v1/convert/acceptQuote
- "List all orderStatus?" -> GET /sapi/v1/convert/orderStatus
- "Create a placeOrder?" -> POST /sapi/v1/convert/limit/placeOrder
- "Create a cancelOrder?" -> POST /sapi/v1/convert/limit/cancelOrder
- "List all queryOpenOrders?" -> GET /sapi/v1/convert/limit/queryOpenOrders
- "List all tradeFlow?" -> GET /sapi/v1/convert/tradeFlow
- "List all taxQuery?" -> GET /sapi/v1/rebate/taxQuery
- "List all transactions?" -> GET /sapi/v1/nft/history/transactions
- "List all deposit?" -> GET /sapi/v1/nft/history/deposit
- "List all withdraw?" -> GET /sapi/v1/nft/history/withdraw
- "List all getAsset?" -> GET /sapi/v1/nft/user/getAsset
- "Create a createCode?" -> POST /sapi/v1/giftcard/createCode
- "Create a redeemCode?" -> POST /sapi/v1/giftcard/redeemCode
- "List all verify?" -> GET /sapi/v1/giftcard/verify
- "List all rsa-public-key?" -> GET /sapi/v1/giftcard/cryptography/rsa-public-key
- "Create a buyCode?" -> POST /sapi/v1/giftcard/buyCode
- "List all token-limit?" -> GET /sapi/v1/giftcard/buyCode/token-limit
- "List all list?" -> GET /sapi/v1/lending/auto-invest/target-asset/list
- "List all list?" -> GET /sapi/v1/lending/auto-invest/target-asset/roi/list
- "List all asset?" -> GET /sapi/v1/lending/auto-invest/all/asset
- "List all list?" -> GET /sapi/v1/lending/auto-invest/source-asset/list
- "Create a add?" -> POST /sapi/v1/lending/auto-invest/plan/add
- "Create a edit?" -> POST /sapi/v1/lending/auto-invest/plan/edit
- "Create a edit-status?" -> POST /sapi/v1/lending/auto-invest/plan/edit-status
- "List all list?" -> GET /sapi/v1/lending/auto-invest/plan/list
- "List all id?" -> GET /sapi/v1/lending/auto-invest/plan/id
- "List all list?" -> GET /sapi/v1/lending/auto-invest/history/list
- "List all info?" -> GET /sapi/v1/lending/auto-invest/index/info
- "List all user-summary?" -> GET /sapi/v1/lending/auto-invest/index/user-summary
- "Create a one-off?" -> POST /sapi/v1/lending/auto-invest/one-off
- "List all status?" -> GET /sapi/v1/lending/auto-invest/one-off/status
- "Create a redeem?" -> POST /sapi/v1/lending/auto-invest/redeem
- "List all history?" -> GET /sapi/v1/lending/auto-invest/redeem/history
- "List all history?" -> GET /sapi/v1/lending/auto-invest/rebalance/history
- "Create a stake?" -> POST /sapi/v2/eth-staking/eth/stake
- "Create a redeem?" -> POST /sapi/v1/eth-staking/eth/redeem
- "List all stakingHistory?" -> GET /sapi/v1/eth-staking/eth/history/stakingHistory
- "List all redemptionHistory?" -> GET /sapi/v1/eth-staking/eth/history/redemptionHistory
- "List all rewardsHistory?" -> GET /sapi/v1/eth-staking/eth/history/rewardsHistory
- "List all quota?" -> GET /sapi/v1/eth-staking/eth/quota
- "List all rateHistory?" -> GET /sapi/v1/eth-staking/eth/history/rateHistory
- "List all account?" -> GET /sapi/v2/eth-staking/account
- "Create a wrap?" -> POST /sapi/v1/eth-staking/wbeth/wrap
- "List all wrapHistory?" -> GET /sapi/v1/eth-staking/wbeth/history/wrapHistory
- "List all unwrapHistory?" -> GET /sapi/v1/eth-staking/wbeth/history/unwrapHistory
- "List all wbethRewardsHistory?" -> GET /sapi/v1/eth-staking/eth/history/wbethRewardsHistory
- "List all userStatus?" -> GET /sapi/v1/copyTrading/futures/userStatus
- "List all leadSymbol?" -> GET /sapi/v1/copyTrading/futures/leadSymbol
- "List all list?" -> GET /sapi/v1/simple-earn/flexible/list
- "List all list?" -> GET /sapi/v1/simple-earn/locked/list
- "Create a subscribe?" -> POST /sapi/v1/simple-earn/flexible/subscribe
- "Create a subscribe?" -> POST /sapi/v1/simple-earn/locked/subscribe
- "Create a redeem?" -> POST /sapi/v1/simple-earn/flexible/redeem
- "Create a redeem?" -> POST /sapi/v1/simple-earn/locked/redeem
- "List all position?" -> GET /sapi/v1/simple-earn/flexible/position
- "List all position?" -> GET /sapi/v1/simple-earn/locked/position
- "List all account?" -> GET /sapi/v1/simple-earn/account
- "List all subscriptionRecord?" -> GET /sapi/v1/simple-earn/flexible/history/subscriptionRecord
- "List all subscriptionRecord?" -> GET /sapi/v1/simple-earn/locked/history/subscriptionRecord
- "List all redemptionRecord?" -> GET /sapi/v1/simple-earn/flexible/history/redemptionRecord
- "List all redemptionRecord?" -> GET /sapi/v1/simple-earn/locked/history/redemptionRecord
- "List all rewardsRecord?" -> GET /sapi/v1/simple-earn/flexible/history/rewardsRecord
- "List all rewardsRecord?" -> GET /sapi/v1/simple-earn/locked/history/rewardsRecord
- "Create a setAutoSubscribe?" -> POST /sapi/v1/simple-earn/flexible/setAutoSubscribe
- "Create a setAutoSubscribe?" -> POST /sapi/v1/simple-earn/locked/setAutoSubscribe
- "List all personalLeftQuota?" -> GET /sapi/v1/simple-earn/flexible/personalLeftQuota
- "List all personalLeftQuota?" -> GET /sapi/v1/simple-earn/locked/personalLeftQuota
- "List all subscriptionPreview?" -> GET /sapi/v1/simple-earn/flexible/subscriptionPreview
- "List all subscriptionPreview?" -> GET /sapi/v1/simple-earn/locked/subscriptionPreview
- "List all setRedeemOption?" -> GET /sapi/v1/simple-earn/locked/setRedeemOption
- "List all rateHistory?" -> GET /sapi/v1/simple-earn/flexible/history/rateHistory
- "List all collateralRecord?" -> GET /sapi/v1/simple-earn/flexible/history/collateralRecord
- "List all list?" -> GET /sapi/v1/dci/product/list
- "Create a subscribe?" -> POST /sapi/v1/dci/product/subscribe
- "List all positions?" -> GET /sapi/v1/dci/product/positions
- "List all accounts?" -> GET /sapi/v1/dci/product/accounts
- "Create a edit-status?" -> POST /sapi/v1/dci/product/auto_compound/edit-status
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
