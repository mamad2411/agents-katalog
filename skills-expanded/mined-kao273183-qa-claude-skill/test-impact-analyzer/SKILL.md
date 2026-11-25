---
name: test-impact-analyzer
description: Test Impact Analysis（TIA）——從 git diff 算出這次改動影響到哪些測試，PR 時只跑受影響的子集，大幅砍 CI 時間。支援 coverage-based（pytest-testmon / xccov / JaCoCo / jest --findRelatedTests）、dependency-graph（nx affected / Gradle / Bazel）、path-heuristic 三種策略，並內建安全網（改共用/config/lockfile → fallback 全量；定期全量校準）。當使用者提到「test impact / TIA / 受影響測試 / 只跑改到的測試 / affected tests / 砍 CI 時間 / 加速 CI / 選擇性跑測試 / testmon / nx affected / 增量測試」時觸發。配套：smoke-test-analyzer（靜態分層，TIA 是動態 per-PR 補強）、flaky-test-hunter（受影響集排除 flaky）、tc-to-pytest（pytest coverage 來源）、qa-signoff（release 仍全量，TIA 只加速 PR）。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[--base=main] [--strategy=coverage|deps|path] [--platform=python|ios|android|js]"
---

# test-impact-analyzer

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

`smoke-test-analyzer` 把測試分成 **T0/T1/T2/T3 靜態 tier**——但每個 PR 還是把**整個 tier** 跑完。當你的 PR 只改了 payment 模組一個函式，卻要等 800 條測試跑完，那是浪費。

TIA 問的是動態問題：「**這次 diff 改了什麼 → 哪些測試會被影響 → 只跑那些**」。

> 分層是「哪些測試重要」（靜態），TIA 是「這次改動碰到哪些測試」（動態 per-PR）。兩者互補：先靠 tier 框出候選，再靠 TIA 縮到受影響子集。

→ 本 skill 從 diff 算受影響測試集，產 CI 設定只跑子集，並用安全網確保不漏測。

## 適用場景

- ✅ 測試套件大、CI 跑很久、PR 等很久
- ✅ Monorepo / 多模組，改一塊不該全跑
- ✅ 已有 coverage map 或清楚的依賴/命名結構
- ✅ 想在「跑很快」和「不漏測」之間有可調的安全閥

## 不適用場景

- ❌ Release / merge-to-main 的最終守門 — **一律全量跑**（TIA 只加速 PR 階段）
- ❌ 測試套件本來就小（< 2 分鐘）— 收益不抵複雜度
- ❌ 決定哪些測試該存在 / 分層 — 用 `smoke-test-analyzer`

## 三種影響映射策略

| 策略 | 怎麼算 | 精準度 | 工具 |
|------|--------|--------|------|
| **coverage-based** | 既有 coverage map：哪個 test 覆蓋哪行 → diff 命中的行反查 test | 🟢 最高 | `pytest-testmon` · `coverage.py` · iOS `xccov`(.profdata) · Android JaCoCo · `jest --findRelatedTests` · `vitest related` |
| **dependency-graph** | import/module 圖：改 module A → 找依賴 A 的測試（反向閉包） | 🟡 中 | `nx affected` · Gradle test filtering · Bazel · Turborepo |
| **path-heuristic** | 命名/路徑規則：改 `src/payment/*` → 跑 `tests/payment/*` | 🟠 粗 | grep / glob 規則（無前兩者時的 fallback） |

> 優先序：有 coverage map 用 coverage → 否則 dep graph → 都沒有才 path heuristic（最保守，傾向多跑）。

## 執行流程

### Phase 1: 取 diff

```bash
BASE="${1:-main}"
# 改動的檔案（相對 base 的合併基準）
git diff --name-only "$(git merge-base $BASE HEAD)"...HEAD
# 改動的行（給 coverage-based 精準命中）
git diff --unified=0 "$(git merge-base $BASE HEAD)"...HEAD
```

### Phase 2: 建/讀影響映射

#### Python — pytest-testmon（最省事）
```bash
# testmon 自動維護 .testmondata（哪個 test 碰哪些程式碼）
pytest --testmon          # 只跑受影響 + 新增/改動的 test
```
或用 coverage.py 的 contexts 建反查表（`--cov-context=test`）。

#### iOS — xccov coverage map
```bash
xcrun xccov view --report --json Result.xcresult > cov.json
# 解析 functions/lines → 反查 diff 命中的檔案對應哪些 test target
```

#### Android — JaCoCo
解析 `jacoco.exec` + class→test 映射，diff 命中的 class 反查測試。

#### JS/TS — jest / vitest / nx
```bash
jest --findRelatedTests $(git diff --name-only main...HEAD)
# monorepo:
npx nx affected -t test --base=main
```

### Phase 3: 算受影響測試集（含安全網）

```
affected = ∅
for f in changed_files:
    if f matches SAFETY_FALLBACK (config/CI/lockfile/共用util):
        return FULL_RUN          # 影響範圍無法靜態界定 → 全跑
    affected ∪= map(f)           # coverage/dep/path 反查
affected ∪= changed_test_files   # 改/新增的測試「本身」一定跑
affected ∪= smoke_T0             # 核心冒煙永遠跑（最後防線）
affected −= quarantined_flaky    # flaky 不該汙染（flaky-test-hunter）
```

**安全網（hard rules，任一觸發 → 全量跑）**：
- 改到 `config/` / CI 設定 / dependency lockfile（`Podfile.lock` / `package-lock.json` / `*.gradle` / `poetry.lock`）
- 改到標記為「共用核心」的路徑（config 可設）
- coverage map **過期**（map 的 commit 比 HEAD 舊 → 不可信）
- 改動的測試檔超過某比例（大規模重構）

### Phase 4: 產 CI 設定 + 預估收益

```markdown
# Test Impact Report · PR #482 · 2026-06-02

## 📊 影響分析
- 策略: coverage-based (pytest-testmon)
- 改動檔案: 3（src/payment/charge.py, src/payment/refund.py, tests/test_charge.py）
- 全套測試: 842 條
- 受影響: 37 條（charge/refund 相關 + 反向依賴）
- 安全網: 未觸發（未改 config/共用）

## ⏱ 預估收益
- 全跑: ~14 min
- 只跑受影響: ~1.2 min（省 ~91%）

## ▶️ 本次該跑
tests/test_charge.py, tests/test_refund.py, tests/test_payment_api.py, ... (37)

## 🛡 校準
- 上次全量校準: 2 天前（main nightly）
- 下次全量: 今晚 nightly（驗證 TIA 沒漏）
```

CI 設定：把受影響清單寫成 pytest `-k` / `xctestplan` skip / Gradle `--tests` filter / jest 參數。

### Phase 5: 安全護欄與校準

- **PR 階段**：跑 TIA 子集（快）
- **merge to main / nightly**：跑全量（校準 + 補 TIA 可能漏的）
- **release**：全量（接 `qa-signoff`，TIA 不參與放行）
- coverage map 隨全量跑更新並 commit / 快取

## ⚠️ 安全護欄

- ✅ **TIA 只加速 PR，不取代全量**——main / release 一律全跑
- ✅ 影響範圍無法靜態界定的改動（config / lockfile / 共用核心）→ **fallback 全量**
- ✅ coverage map 過期 → 不信任，**全量 + 重建 map**
- ✅ 改動/新增的測試本身 + smoke T0 **永遠納入**（不只既有受影響測試）
- ✅ 定期全量校準，量測「TIA 漏掉但全量抓到」的 escape rate，>0 就放寬規則
- ❌ 不宣稱「100% 精準」——明確標示這是「機率性加速 + 安全網」

## ♿ a11y 必檢（本 skill 專屬）

- [ ] 任一 **UI 元件改動**一律把對應的 **a11y 測試納入受影響集**（a11y 常跨元件，靜態 diff 抓不到連鎖影響）
- [ ] 設計系統 / 共用元件 / theme 改動 → a11y 測試走 fallback 全量（對比度/字級影響面廣）

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `test_impact.strategy` | coverage / deps / path | auto（依工具偵測） |
| `test_impact.base_ref` | diff 比較基準 | main |
| `test_impact.full_run_triggers` | 觸發全量的路徑 glob | config/ · *.lock · CI yml |
| `test_impact.shared_core_paths` | 視為「共用核心」的路徑 | [] |
| `test_impact.coverage_map_path` | coverage map 位置 | 依平台預設 |
| `test_impact.always_include` | 永遠跑的測試（如 smoke T0） | smoke_t0 |

## 範例

詳見 [`examples.md`](./examples.md)
