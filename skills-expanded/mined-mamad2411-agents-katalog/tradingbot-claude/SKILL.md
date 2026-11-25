# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **⚠️ 작업(코드수정/진단/손실분석) 시작 전 `SYSTEM_MAP.md`를 먼저 정독할 것.** 봇 전체 로직 지도(진입/청산/추적/모드/데이터) + "자주 틀리는 지점"이 정리돼 있다. 특히: 이 봇은 **테스트넷($1만 테스트머니)** 구동(appsettings의 IsSimulationMode=false는 stale). `ACCOUNT_UPDATE_RESTORED/외부` 라벨은 **봇 자신 거래의 추적 오라벨**(수동매매 0). 손실 원인은 외부가 아니라 **전략 자체**. 코드가 SYSTEM_MAP과 다르면 문서를 실제에 맞게 갱신.

## Project

C# WPF cryptocurrency futures trading bot (.NET 9, Binance/Bybit). Single-user-per-machine WPF app with per-user data isolation in SQL Server. Self-contained Velopack-deployed Setup.exe (~220MB).

## Common Commands

### Build / Run

```bash
# Release build (WPF main app)
dotnet build TradingBot.csproj -c Release --nologo -v q

# Publish for Velopack packaging
dotnet publish TradingBot.csproj -c Release -r win-x64 --self-contained true -o "./bin/publish" -p:PublishSingleFile=false

# Full release (commit → push → publish → Velopack → GitHub release)
git push Tradingbot main
dotnet publish TradingBot.csproj -c Release -r win-x64 --self-contained true -o "./bin/publish" -p:PublishSingleFile=false
echo "Y" | powershell -ExecutionPolicy Bypass -File publish-and-release.ps1 -PublishPath "./bin/publish" -Version "X.X.X"
gh release view vX.X.X --json url -q .url
```

`RELEASE_CHECKLIST.md` is **mandatory reading** before any release — also auto-checked by `publish-and-release.ps1`. Memory rule: when user says "배포", check the checklist + run the full pipeline above. Bump version in `TradingBot.csproj` and add a `## [X.X.X]` entry at the top of `CHANGELOG.md` first.

The bot remote is named `Tradingbot` (not `origin`).

### Backtest Tool — `Tools/LorentzianValidator/`

Standalone .NET 9 console project that ports the same Lorentzian KNN engine from the main app and re-implements the bot's 5 entry triggers (PUMP/SPIKE/MAJOR/SQUEEZE/BB_WALK) for chart-data backtesting. Use this — not the live DB stats — to compare gate/TP/SL changes.

```bash
cd Tools/LorentzianValidator
dotnet build -c Release --nologo
dotnet run -c Release --no-build -- <mode> [flags]
```

Modes (each fetches fresh klines from `fapi.binance.com`, paginated, with 0.8s throttle + 429 retry):

- `--logic-30d` / `--logic-60d` / `--logic-90d` / `--logic-180d` / `--logic-365d` — 5 triggers × 4 guards × 3 TP/SL matrix
- `--final` — apply current production gates only, report PnL/ROI/win-rate per TP/SL config
- `--diagnose` — Lorentzian Pred distribution, TP/SL hit-time, RSI/ATR bucket win-rates, single-gate AB
- `--redesign` — sweep filter combinations searching for profitable setups
- `--target70` / `--target70-90d` — sweep tight-TP/wide-SL combos targeting 70%+ win-rate
- `--pump-tune` — PUMP-only deep sweep (RSI threshold × TP/SL × WIN)
- `--elliott` / `--elliott2` / `--elliott-oos` / `--elliott-final` / `--elliott-live` — [v5.33.0] 엘리엇 파동(15m 진입 · 손익비 1:3). 순서대로 구조기본 → 필터조합 스윕(8,640) → 워크포워드 OOS(과최적화 판정) → 고정규칙 폴드안정성 → **라이브 코드 재생검증**(`Services/ElliottWaveEngine.cs` 링크 컴파일). 새 규칙을 만들면 반드시 `--elliott-oos`로 곡선맞춤 여부부터 확인할 것 — 조합 1등 선택은 OOS에서 붕괴했다.

Flags (any mode):
- `--lev N` — leverage override (default 10)
- `--margin-major N` — sets MAJOR/SQUEEZE/BB_WALK margin
- `--margin-pump N` — sets PUMP/SPIKE margin

Always run a long-window check (`--logic-180d` minimum) before bumping production thresholds — short windows show whipsaw effects from market-regime drift.

### Diagnostic / Fix Scripts

Loose PowerShell scripts at the repo root (`diag-*.ps1`, `fix-*.ps1`, `query-*.ps1`) are ad-hoc throwaway tools. Common patterns:

- All scripts decrypt the DB connection string from `appsettings.json` using a hardcoded AES-256 key (see `AesDecrypt` function header).
- **PowerShell 5.1 here-string `@'...'@` is fragile** — terminator must be at column 0, file should be CRLF (run `unix2dos <file>.ps1` after writing or the `'@` won't be recognized).
- Korean characters in titles/strings break parsing intermittently — fall back to ASCII labels when scripts fail with `MissingEndParenthesisInExpression`.
- Many sample scripts assume column names that may have drifted (e.g., `Bot_Log` actually has `EventTime/Symbol/CoinType/Allowed/Reason/ML_Conf/TF_Conf` — not `Message/LogTime`).

## Architecture (Big Picture)

### Data isolation — per-user vs shared

| Layer | Scope | Mechanism |
|---|---|---|
| Settings / slots / stats | **Per-user** | DB tables keyed by `UserId` (`GeneralSettings.Id`, `TradeHistory.UserId`, `PositionState.UserId`, `Bot_Log.UserId`, all SPs take `@userId`) |
| Open positions / trade history / PnL | **Per-user** | DB |
| Entry guards / `_settings` | **Per-user** | `MainWindow.CurrentGeneralSettings` static, loaded per logged-in user |
| **Chart kline data** | **Shared** | `MarketDataManager.Instance` singleton, `KlineCache` 5m/15m/1h |
| `DbManager` | **Shared** | `DbManager.Shared` static (added v5.21.4) — `GetShared(cs)` to avoid Ensure-DDL re-runs |
| ML.NET model `.zip` files | **Machine-wide** | `%LOCALAPPDATA%\TradingBot\Models\` — no UserId in path. One bot per Windows account is the assumed deployment. |

The "shared chart data, per-user everything else" boundary is intentional. Don't add `UserId` to `MarketDataManager` keys — it'll multiply WebSocket subscriptions and break the singleton.

### Entry pipeline

Every new entry (reduceOnly=false) must funnel through `TradingEngine.IsEntryAllowed(symbol, source, out reason)` — direct calls to `_exchangeService.PlaceMarketOrderAsync` are forbidden (history of regressions noted inline). The gate is **source-aware** (added v5.21.0):

```
source string → entryCat
  "TICK_SURGE" / "*SPIKE*"   → SPIKE   (always blocked, "30d_loss_proven")
  "*SQUEEZE*"                → SQUEEZE (no gate beyond basics)
  "*BB_WALK*" / "*BBWALK*"   → BB_WALK (no gate)
  "*MAJOR*"                  → MAJOR   (no gate beyond basics)
  default                    → PUMP    (EMA20 rising + RSI<65 v5.21.1)
```

Universal gates (apply to all categories): `SETTINGS_NOT_LOADED`, `MANUAL_CLOSE_COOLDOWN`, `MAJOR_DISABLED`, `MODEL_ZIP_MISSING`, `HIGH_TOP_CHASING`, `TOP_DISTRIBUTION`, `SIDEWAYS_BOX`, `BTC_1H_DOWNTREND`, `ALT_RSI_FALLING_KNIFE`. Each emits `⛔ [GATE] {symbol} {source} 차단 | reason=…` so block reasons can be audited from `Bot_Log.Reason` after the fact.

Category strings written to `TradeHistory.Category` come from `DbManager.ResolveTradeCategory(symbol, signalSource)` — uses both symbol (BTC/ETH/SOL/XRP/BNB → MAJOR override) and signalSource keyword matching. Keep this in sync with the gate categorisation above and the UI `MajorStats/PumpStats/SqueezeStats/SpikeStats` properties on `MainViewModel`.

### AI subsystem

- **`AIDoubleCheckEntryGate.cs`** owns 4 `EntryTimingMLTrainer` instances (Default/Major/Pump/Spike variants) + 1 `LorentzianV2Service`. Variant zips: `EntryTimingModel.zip`, `EntryTimingModel_Major.zip`, `EntryTimingModel_Pump.zip`, `EntryTimingModel_Spike.zip` in `%LOCALAPPDATA%\TradingBot\Models\`.
- Initial training trigger: `TradingEngine` checks `IsInitialTrainingComplete` on startup — getter validates **both** `initial_training_ready.flag` **and** all 5 model zips exist + are >30KB. Mismatch → flag auto-deletes (v5.21.3) → `TriggerInitialTrainingAsync` runs on next start.
- ML.NET binary classification training has a known failure mode: when test split (80/20) lands a single-class subset, `BinaryClassificationMetrics.AreaUnderRocCurve` throws `"AUC is not defined when there is no positive class"`. v5.21.2 wrapped all `Evaluate(...)` calls in try/catch with AUC=0 fallback so training itself never fails on this. **If you add a new ML.NET trainer, do the same.**
- `Bot_Log.ML_Conf == 1E-15` (or any `<1E-9`) is the diagnostic signature for "model file missing or schema mismatch" — not "model thinks it's a bad trade".

### Settings / TP-SL conventions

`Models.cs` `TradingSettings` defaults reflect chart-validated values from the v5.21.x backtest sweeps:

- `TargetRoe = 15.0`, `StopLossRoe = 45.0` → at 15× leverage = price TP 1.0% / SL 3.0% (1:3 ratio chosen for ~85% win-rate at break-even WR=75%)
- `MajorTp1Roe = 15.0`, `MajorStopLossRoe = 45.0`, `PumpTp1Roe = 15.0`, `PumpStopLossRoe = 45.0` — kept symmetric on purpose
- `DefaultLeverage = 15`, `MajorLeverage = 15`, `PumpLeverage = 15`

**These are *defaults* for new installs. Existing users' DB-saved `GeneralSettings` overrides them.** Code-only changes do not propagate to the live bot's TP/SL — the user has to update their settings in the UI.

### Single-instance enforcement

`App.xaml.cs` uses `Local\TradingBot_SingleInstance_8F9A2B3C` mutex (was `Global\` until v5.21.4 — `Global\` requires `SE_CREATE_GLOBAL_NAME` which silently fails for non-elevated users, so duplicate processes slipped through). Mutex catch path now `Shutdown()`s instead of continuing. On collision, user gets a Yes/No prompt — Yes kills the existing `TradingBot.exe` processes by name and retakes the mutex.

## Repository Conventions

- **Komentary, commit messages, log strings, alert text are written in Korean.** Match the existing style — short, often emoji-prefixed (`⛔`, `✅`, `🚦`, `📊`).
- Commit messages follow loose Conventional-Commits-with-Korean: `v5.X.Y: 한국어 요약 메시지` for releases, `fix(vX.Y.Z):`, `hotfix(vX.Y.Z):`, `refactor(vX.Y.Z):` for inline fixes.
- Inline version tags `[v5.X.Y]` mark when a change was added — useful for blame archaeology, leave existing ones alone.
- The `Tools/` directory is **excluded** from the main `.csproj` build via `<Compile Remove="Tools\**\*.cs" />`. Sub-projects under `Tools/` build independently with their own `.csproj`.
- `.history-memo/` and the loose `diag-*.ps1` / `fix-*.ps1` / `query-*.ps1` scripts at the repo root are work-in-progress diagnostic tools — they accumulate. Don't try to clean them up unless asked.

## Memory (auto-loaded)

A persistent memory store at `C:\Users\COFFE\.claude\projects\e--PROJECT-CoinFF-TradingBot-TradingBot\memory\` is auto-loaded each session via `MEMORY.md`. Notable rules already there:
- "메이저" = BTC/ETH/SOL/XRP only (4 coins) — BNB/DOGE/everything else is PUMP territory
- All entries must come from AI inference (ML.NET / Lorentzian), not hardcoded conditions
- 3 separated AI models for major / PUMP-normal / PUMP-spike, with separate training/inference/thresholds
- Per-user data separation is required everywhere — DB / slots / stats all keyed on UserId
- "초소형" PUMP filter means **market cap**, not volume (CoinGecko required)
- Before any "배포" operation: read `RELEASE_CHECKLIST.md`, update `CHANGELOG.md`, run the full pipeline
- For deploy operations: commit/push are auto-OK, but `release` / `publish` waits for explicit user approval
