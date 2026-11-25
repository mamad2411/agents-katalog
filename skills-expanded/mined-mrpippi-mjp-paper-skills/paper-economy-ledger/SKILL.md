---
name: paper-economy-ledger
description: "插件內建經濟核心：long 最小單位金額（不用 double）、多幣種、純 Ledger（OK/INSUFFICIENT/NO_ACCOUNT/INVALID_AMOUNT）、只增不改交易紀錄、k/m/b 簡寫解析與格式化、託管（escrow）例外安全、write-behind 持久化、內部 API 與選用 Vault Economy 提供端 / In-plugin economy core with long minor units, multi-currency pure Ledger, append-only transaction log, k/m/b parsing, exception-safe escrow, write-behind persistence, internal API and optional Vault provider"
---

# Paper Economy Ledger

## Skill Name

`paper-economy-ledger`

## Purpose

Provide an economy core you can drop straight into a plugin. The point: money must never be miscalculated or vanish.

1. **Amounts are always `long` minor units** (`decimals = 2` -> 1 dollar = 100). `double` appears only at the Vault boundary, and every crossing goes through `BigDecimal` rounded to the minor unit.
2. **A pure `Ledger`**: no Bukkit types. Deposit/withdraw/transfer return an explicit result `OK / INSUFFICIENT / NO_ACCOUNT / INVALID_AMOUNT`, never throw, never apply half a change; additions use `Math.addExact` to guard against overflow.
3. **Append-only transaction log**: every change produces a `Transaction` (who, delta, balance after, note, time), written to the persistence layer atomically as one batch.
4. **Shorthand and formatting**: parse `1.2k / 3m / 4b` (rejecting negatives, `NaN`, scientific notation, too many decimals, and values over the cap) and display amounts.
5. **Escrow**: reserve the buyer's money first, pay the seller only after delivery succeeds; if delivery throws, refund in `finally`, so money or items never vanish.
6. **Write-behind persistence**: memory is authoritative, and a single-thread queue writes to storage in order (implementation in [`paper-sqlite-repository`](../paper-sqlite-repository/SKILL.md)).
7. **External surface**: expose the internal API first (see [`paper-service-api`](../paper-service-api/SKILL.md)), then optionally register a Vault `Economy` provider (isolation rules in [`paper-softdepend-hook`](../paper-softdepend-hook/SKILL.md)).

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (uses only the Bukkit API and Vault 1.7.1; the code is identical on both versions, with no version-specific lines)
- Pure Paper API, no Paperweight needed; `Ledger`, `Escrow`, formatting and parsing do not depend on Bukkit at all and can be tested directly with JUnit
- **Spigot**: Core portable — the ledger and Vault provider use Bukkit and Vault only; replace Adventure messages

## Triggers

- 「經濟」「economy」「帳本」「ledger」「餘額」「balance」「轉帳」「pay」
- 「貨幣」「multi-currency」「小數」「minor units」「k m b」「1.5k」「簡寫金額」
- 「託管」「escrow」「退款」「refund」「訂單」「交易紀錄」「transaction log」
- 「Vault Economy 提供端」「register Economy」「ServicePriority.Highest」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `base_package` | `com.example.economy` | Root package; the API lives in `<base>.api` (must not be relocated) |
| `currencies` | `coins` (2 decimals), `gems` (0) | Per currency: `id`, symbol, decimals, display pattern, starting balance |
| `vault_currency` | `coins` | The one currency exposed to Vault (Vault supports a single currency) |
| `persistence` | `sqlite` | Persistence layer; the template includes an in-memory `InMemoryLedgerStore` for tests |
| `expose_vault` | `true` | Whether to register the Vault provider |

## Outputs

- `EconomyResult.java`, `EconomyApi.java` - public API (JDK types only)
- `Currency.java`, `Money.java`, `MoneyFormat.java`, `AmountParser.java` - currencies, minor-unit conversion, display, parsing
- `Transaction.java`, `Ledger.java` - pure ledger and transaction log
- `Escrow.java` - exception-safe escrow
- `LedgerStore.java`, `InMemoryLedgerStore.java`, `WriteBehindQueue.java` - persistence interface and write-behind queue
- `EconomyApiImpl.java` - API implementation restricted to the main thread
- `VaultEconomyProvider.java`, `VaultHook.java` - optional Vault provider and registration entry point
- `EconomyPlugin.java` - wiring, registration, and draining the queue on disable

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Vault is `compileOnly` and must not be shaded; add JUnit for tests:

```groovy
dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable' // 1.21.11: '1.21.11-R0.1-SNAPSHOT'
    compileOnly('com.github.MilkBowl:VaultAPI:1.7.1') { exclude group: 'org.bukkit' }

    testImplementation platform('org.junit:junit-bom:5.12.2')
    testImplementation 'org.junit.jupiter:junit-jupiter'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

tasks.withType(Test).configureEach { useJUnitPlatform() }
```

`plugin.yml`:

```yaml
name: Economy
main: com.example.economy.EconomyPlugin
api-version: '26.3'
softdepend: [Vault]
```

`config.yml` (currency definitions; `decimals` is 0 to 2, `pattern` only controls thousands grouping and the fraction digits come from `decimals`; quote `starting-balance` so it is parsed as a string):

```yaml
vault-currency: coins
currencies:
  coins:
    symbol: "$"
    decimals: 2
    pattern: "#,##0"
    starting-balance: "100.00"
  gems:
    symbol: "G"
    decimals: 0
    pattern: "#,##0"
    starting-balance: "0"
```

## Code Template

The full source lives in [`template.md`](template.md) (about 1,300 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `EconomyResult.java` | `.api` | Operation result enum (append-only); non-`OK` means no balance changed |
| `EconomyApi.java` | `.api` | Cross-plugin API, JDK types only |
| `Currency.java` | `.domain` | Currency definition (id, symbol, decimals, format pattern, starting balance) |
| `Money.java` | `.domain` | Minor-unit cap (`MAX`) and `double` conversion for Vault |
| `MoneyFormat.java` | `.domain` | Amount display: minor units in, plain text out |
| `AmountParser.java` | `.domain` | Player input with k/m/b shorthand → minor units |
| `Transaction.java` | `.domain` | Append-only transaction record with balance after |
| `Ledger.java` | `.domain` | Pure ledger: validate, mutate, record; no Bukkit, JUnit-testable |
| `Escrow.java` | `.domain` | Reserve buyer funds, pay seller after delivery, refund in `finally` |
| `LedgerStore.java` | `.storage` | Persistence interface |
| `InMemoryLedgerStore.java` | `.storage` | In-memory store for tests and development |
| `WriteBehindQueue.java` | `.storage` | Single-thread write-behind queue (ordered writes) |
| `EconomyApiImpl.java` | root | Main-thread check + currency lookup; delegates to `Ledger` |
| `VaultEconomyProvider.java` | `.vault` | Optional Vault `Economy` provider, built only by `VaultHook` |
| `VaultHook.java` | `.vault` | Isolated Vault entry point (no Vault types leak out) |
| `EconomyPlugin.java` | root | Wiring, service registration, synchronous drain on disable |

### Core Rules

1. **Amounts are `long` minor units**, capped at `Money.MAX` (9x10^15, below 2^53, so `double` can still represent integers exactly up to that point). Never use `double` inside the ledger.
2. **`Ledger` never touches Bukkit**; the outer layer (`EconomyApiImpl`) checks the thread, and `Ledger` itself assumes single-threaded use.
3. **Validate first, mutate second, record third**: change balances only after every check (account, amount, balance, overflow) passes; a non-`OK` result guarantees balances are unchanged.
4. **Memory is authoritative, persistence is write-behind**: a failed write is only logged and memory is not rolled back; each transaction carries the "balance after", so the next successful write self-heals, and `onDisable` drains synchronously.
5. **Escrow refunds in `finally`**: on every path out of `trade`, the reserved money has either been paid to the seller or returned to the buyer.
6. Vault `double` values always go through `Money.toMinor`, rounded to the minor unit; the return value of `Economy.format()` is **not** MiniMessage (see the note on `VaultEconomyProvider`).

## Recommended Directory Structure

```
economy/
└── src/main/java/com/example/economy/
    ├── EconomyPlugin.java
    ├── EconomyApiImpl.java
    ├── api/                       <- must not be relocated, append-only (JDK types)
    │   ├── EconomyApi.java
    │   └── EconomyResult.java
    ├── domain/                    <- pure Java, no org.bukkit; test directly with JUnit
    │   ├── Currency.java  Money.java  MoneyFormat.java  AmountParser.java
    │   └── Transaction.java  Ledger.java  Escrow.java
    ├── storage/
    │   ├── LedgerStore.java  InMemoryLedgerStore.java  WriteBehindQueue.java
    │   └── SqliteLedgerStore.java <- see paper-sqlite-repository
    └── vault/                     <- the only place that imports net.milkbowl
        ├── VaultEconomyProvider.java
        └── VaultHook.java
```

## Thread Safety

- `Ledger`/`Escrow` assume a single thread; `EconomyApiImpl` and the Vault provider allow only the **main thread** (violations throw `IllegalStateException`)
- Persistence runs only on the single writer thread of `WriteBehindQueue`; only immutable `Transaction` records go through the queue, never Bukkit objects
- When async work (HTTP, database) needs an amount, read the value on the main thread first and pass it in; to write back, return to the main thread with `runTask` and then call the API
- The scheduler is already shut down in `onDisable`: drain synchronously with `queue.close(...)` and do not submit `runTaskAsynchronously` again
- See [`references/paper-threading.md`](references/paper-threading.md)

## Fallback

| Error | Cause | Fix |
|------|------|------|
| Balance off by 1 cent, `0.1 + 0.2` does not add up | `double` was used inside the ledger | Use `long` minor units throughout; `double` is used only at the Vault boundary via `Money.toMinor` (rounded) |
| Total goes up or down after a transfer | Failure between debit and credit, or the receiver overflowed | `Ledger.transfer` checks both sides first and then changes both; a non-OK result guarantees balances are unchanged |
| `ArithmeticException: long overflow` | Used `+` directly, or `Math.addExact` was not caught | Always use `Money.checkedAdd`; overflow returns `INVALID_AMOUNT` |
| Player input `1e3`, `-5`, `NaN` is accepted as money | Parsed with `Double.parseDouble` | Use `AmountParser` (regex + BigDecimal), never via double |
| After a delivery exception the buyer got nothing and no refund | No `finally` after reserving | Use `Escrow.trade`; in custom flows put `Hold.refund()` in `finally` |
| Items vanish after a delivery exception | Items were already taken from the screen/inventory and the exception skipped restoration | In `Delivery`, `catch` -> restore items first -> rethrow (see examples.md); `Escrow` handles the refund |
| Messages show raw `§a$ 100` / `&a100` | Another provider's `Economy.format()` was put into MiniMessage | Convert to `Component` with `LegacyComponentSerializer`, or use the plain text from `EconomyApi.format` |
| Other plugins still use the old economy | Priority too low, or this plugin is not registered | Register with `ServicePriority.Highest`; `softdepend: [Vault]`; confirm registration in the startup log |
| `NoClassDefFoundError` without Vault installed | A Vault type appears in an `EconomyPlugin` field or signature | Vault types appear only in the `vault/` package; check `isPluginEnabled("Vault")` before calling `VaultHook` |
| One entry missing after restart | A write failed, or the queue was not drained on shutdown | Look for `Ledger write failed` in the log (includes uuid and amount); confirm `onDisable` calls `queue.close` |
| `getOfflinePlayerIfCached` returns null | Legacy Vault method called by name for a player who never joined | Return `FAILURE`/0; callers should switch to the UUID variant |
