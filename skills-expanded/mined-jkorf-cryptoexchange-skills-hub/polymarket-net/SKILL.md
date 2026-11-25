---
name: polymarket-net
description: Build C#/.NET Polymarket integrations with Polymarket.Net V5, including PredictionApi market discovery and orders, PerpsApi futures data and trading, EthKey credentials, WebSocket streams, Shared APIs, local books, trackers and V4 migration. Use for Polymarket-specific .NET code or converting raw Polymarket API usage to the library.
---

# Polymarket.Net V5

Use `Polymarket.Net` for Polymarket-specific C#/.NET integrations. This skill targets
V5.0.0. Check the user's installed version before applying V5 names to an existing
application; use the migration notes below when upgrading V4 code.

## Setup and routing

```bash
dotnet add package Polymarket.Net --version 5.0.0
```

Use `Polymarket.Net.Clients` for clients, `Polymarket.Net.Enums` for trading enums,
`Polymarket.Net` for credentials, and `CryptoExchange.Net.Web3` for `EthKey`.
Reuse `PolymarketRestClient` / `PolymarketSocketClient` or register `AddPolymarket`.

| Workflow | REST | WebSocket |
|---|---|---|
| Prediction CLOB data, Gamma discovery/search, token lookup | `PredictionApi.ExchangeData` | `PredictionApi` |
| Prediction credentials and allowances | `PredictionApi.Account` | `PredictionApi` user stream |
| Prediction orders, trades, Data API positions | `PredictionApi.Trading` | `PredictionApi` user stream |
| Perps instruments, tickers, books, candles, funding | `PerpsApi.ExchangeData` | `PerpsApi.ExchangeData` |
| Perps proxy credentials, balances, portfolio, leverage | `PerpsApi.Account` | `PerpsApi.Account` |
| Perps orders and fills | `PerpsApi.Trading` | `PerpsApi.Trading` |
| Shared futures contracts | `PerpsApi.SharedApi` | `PerpsApi.SharedApi` |

Do not invent `SpotApi`, `FuturesApi`, `GeneralApi` or `SharedClient` roots.
Prediction has no `SharedApi`. For portable futures operations, use the Perps shared
contracts or `IPolymarketSharedApiClient`, not prediction token methods.
Read [API surfaces](references/api-surfaces.md) to choose exact groups and methods.

## Credentials

Public market data needs no credentials. Prediction L1 uses a wallet key to create
or derive L2 credentials and sign orders. L2 is the API key/secret/passphrase for
private CLOB endpoints and authenticated user streams. Order placement needs both.

```csharp
using CryptoExchange.Net.Web3;
using Polymarket.Net;
using Polymarket.Net.Enums;

var credentials = new PolymarketCredentials()
    .WithL1(SignType.Poly1271, new EthKey(privateKey: "PRIVATE_KEY"), "POLYMARKET_DEPOSIT_ADDRESS")
    .WithL2("L2_KEY", "L2_SECRET", "L2_PASSPHRASE");
```

`PolymarketL1Credential` also takes `EthKey`. Select the account's `SignType`:
`EOA`, `Email`, `Proxy` or `Poly1271`; Poly1271 requires the deposit address.
With L1 only, call `PredictionApi.Account.GetOrCreateApiCredentialsAsync()`, check
`.Success`, then `UpdateL2Credentials(result.Data)`. The socket client also supports
this update when initial prediction credentials are configured.

Perps uses separate proxy credentials:

```csharp
using CryptoExchange.Net.Web3;
using Polymarket.Net;

var credentials = new PolymarketCredentials().WithPerps(
    secret: "PERPS_API_SECRET",
    signerKey: null,
    proxyKey: new EthKey(privateKey: "PERPS_PROXY_PRIVATE_KEY"));
```

Owner `signerKey` credentials register proxies with `PerpsApi.Account.CreateProxyAsync`.
Retain the returned secret and proxy key. Proxy private keys sign trading operations;
proxy address plus secret authenticate private reads and streams. Combine credential
families with `.WithL1(...).WithL2(...).WithPerps(...)`. Assign through client
`options.ApiCredentials`; properties are `PredictionL1`, `PredictionL2` and `Perps`.

## Identifiers and results

- Prediction V1 markets use `ClobTokenIds`. For `Version == "v2"`, use `PositionIds` and `marketVersion: 2` when placing orders; batch requests use `PolymarketOrderRequest.MarketVersion`.
- Prediction prices are between 0 and 1; token/position ids differ from condition ids and numeric Gamma market ids. `GetMarketByIdAsync` takes `long`.
- `PredictionApi.ExchangeData.GetMarketsAsync` returns a Gamma market array, not a CLOB cursor page. Keyset discovery uses `GetMarketsKeysetPaginationAsync`.
- Concrete Perps calls use numeric `SymbolId` values discovered through `PerpsApi.ExchangeData.GetSymbolsAsync()`. Check `QuantityDecimals`, `PriceDecimals` and `MinNotional`. Use `PerpTimeInForce` for Perps and `TimeInForce` for prediction orders.
- REST returns `HttpResult<T>` / `HttpResult`; subscriptions return `WebSocketResult<UpdateSubscription>`; Perps socket operations return `QueryResult<T>` / `QueryResult`.
- Check outer `.Success` before `.Data`. Prediction orders also need `.Data.Success` checks. Perps single-order rejections are outer failures; payloads contain `Status`, `Error` and numeric `OrderId`.
- Batch placement contains per-order `CallResult<T>` entries; check both outer and per-order results before reading data.
- Read-only retries may use `Error.IsTransient` and bounded backoff. Avoid blindly retrying order placement after an uncertain response.
- Store successful subscriptions and unsubscribe on shutdown or partial failure. Keep handlers short and propagate cancellation.

## DI, books and trackers

`services.AddPolymarket(options => ...)` configures REST and socket clients. Inject
`IPolymarketRestClient`, `IPolymarketSocketClient`, `IPolymarketSharedApiClient`,
`IPolymarketOrderBookFactory`, `IPolymarketTrackerFactory` or
`IPolymarketUserClientProvider` as needed.

Local books are `PolymarketPredictionSymbolOrderBook(tokenId)` and
`PolymarketPerpsSymbolOrderBook(symbolId)` in `Polymarket.Net.SymbolOrderBooks`.
Factory methods are `CreatePrediction(tokenId)` and `CreatePerps(symbolId)`.
Start books, check the result and stop/dispose them on shutdown.
`PolymarketUserPerpsDataTracker` is available via `CreateUserPerpsDataTracker`.
Read [usage](references/usage.md) for examples and [operational guidance](references/safety.md)
when working with private account or trading workflows.

## V4 migration

- Rename `ClobApi` and its explicit types/namespaces to `PredictionApi`. Move Gamma calls to `PredictionApi.ExchangeData` and Data positions to `PredictionApi.Trading`.
- Replace string wallet arguments with `EthKey`; `L1`/`L2` properties become `PredictionL1`/`PredictionL2`. Credential constructor named arguments become `predictionL1`/`predictionL2`. L1 `PrivateKey` becomes `WalletKey`; construct new L1 credentials when changing read-only properties.
- Consolidate REST `ClobOptions`, `GammaOptions`, `DataOptions` into `PredictionOptions`; socket prediction settings also use `PredictionOptions`. REST `BuilderCode` moves to `PredictionOptions.BuilderCode`; Perps settings use `PerpsOptions`.
- Rename `PolymarketClobSymbolOrderBook` to `PolymarketPredictionSymbolOrderBook` and factory `CreateClob` to `CreatePrediction`.
- The former CLOB `GetMarketsAsync(cursor)` and `GetMarketAsync(id)` are removed. Choose Gamma discovery or `GetMarketInfoAsync(conditionId)` for the required data.
- Positions now return `PolymarketDataPage<PolymarketPosition>` with items in `.Data.Data` and cursor in `.Data.Pagination.NextCursor`. Replace `GetClosedPositionsAsync` with `GetPositionsAsync(status: PositionStatus.Closed)`; review filters and renamed model fields.
- Custom environments additionally require PolyBolt and Perps REST/socket addresses.

## Source of truth

For unlisted signatures inspect `Polymarket.Net/Interfaces/Clients/PredictionApi/`
and `Polymarket.Net/Interfaces/Clients/PerpsApi/` in the library source. In a sibling
maintainer checkout, the repository is `../Polymarket.Net/`; read its
`docs/ai-api-map.md` or `Examples/ai-friendly/` for detailed routing and complete
examples. References here are relative to the hub repository root when referring
to sibling repositories.

- [Polymarket.Net source](https://github.com/JKorf/Polymarket.Net)
- [Client reference](https://cryptoexchange.jkorf.dev/Polymarket.Net/)