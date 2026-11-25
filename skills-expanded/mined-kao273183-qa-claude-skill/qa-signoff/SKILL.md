---
name: qa-signoff
description: Release 上線前的 QA 放行門（go/no-go gate）。彙整各方訊號——測試通過率、未關 P0/P1 bug、回歸結果、security/compliance/a11y/效能/離線各 gate 的 blocker 數、flaky 狀態、跨平台一致性——算出 readiness 分數，套 hard/soft gate 規則產出 go / no-go 決策，並生成可簽核的 sign-off 文件（含風險聲明 + 條件式放行）。當使用者提到「放行 / sign-off / signoff / go no-go / release readiness / 上線檢查 / 出版檢查表 / QA gate / release gate / 可以上線嗎 / 放行決策 / readiness 評分」時觸發。配套：regression-test（前置，產回歸結果）、smoke-test-analyzer（測試分層通過率）、flaky-test-hunter（flaky 不該擋放行）、security-scan / compliance-test / a11y-audit（各 gate 來源）、publish-regression（放行後發報告）。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[版本號] [--platform=ios|android|both] [--strict]"
---

# qa-signoff

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

Release 流程裡：
- `regression-test` 產**回歸測試計劃**（要測什麼）
- 各 skill 跑出**各自的 gate 報告**（security / compliance / a11y / 效能 / 離線）
- `publish-regression` 發**測試報告**

但中間最關鍵的「**這個版本到底能不能上線？依據什麼？誰簽的？**」——這個放行決策沒有 skill 串起來。它通常散在某人腦袋、某個 Slack 訊息、某張手動 checklist。

> 這是 `regression-test → publish-regression` 之間缺的最後一塊：**把放行從「感覺可以」變成「可量化、可追溯、有簽核」**。

→ 本 skill 彙整訊號 → 算 readiness → 套 gate → 產 go/no-go + sign-off 文件。

## 適用場景

- ✅ 每次 release / hotfix 上線前的最後一道 QA 關
- ✅ 需要可追溯放行紀錄（稽核 / 合規 / 事後檢討）
- ✅ 多人 / 多平台 release，要一份權威的 readiness 真相
- ✅ 想把「上線前檢查」標準化、不靠某個人記得

## 不適用場景

- ❌ 規劃要測什麼 — 用 `regression-test`
- ❌ 發測試報告到 dashboard — 用 `publish-regression`
- ❌ 找出 flaky test — 用 `flaky-test-hunter`（但本 skill 會引用其結果）

## 彙整的放行訊號

| 訊號 | 來源 | 預設 gate |
|------|------|----------|
| 測試通過率 | smoke / regression 結果 | soft（< 門檻扣分） |
| 未關 **P0** bug | JIRA | 🔴 **hard**（>0 直接 no-go） |
| 未關 P1 bug | JIRA | soft（扣分 + 列風險） |
| Security blocker | `security-scan` | 🔴 **hard** |
| Compliance blocker | `compliance-test` | 🔴 **hard** |
| a11y Critical | `a11y-audit` | soft（依產業可升 hard） |
| 效能迴歸 | `mobile-resource-test` | soft |
| 離線韌性 fail（寫丟失/重複） | `offline-mode-test` | soft（金流類可升 hard） |
| Flaky 比率 | `flaky-test-hunter` | 參考（**不擋放行**，flaky ≠ 真失敗） |
| 跨平台一致 | iOS vs Android 結果 | soft |
| 自動化覆蓋 | smoke-test-analyzer | 參考 |

## Hard gate vs Soft gate

- **Hard gate**：任一不過 → **直接 no-go**，不看分數（P0 bug / security / compliance blocker）
- **Soft gate**：扣 readiness 分數 + 列入風險，但可由有權限者**條件式放行**（conditional go）

> 護欄：**flaky test 永遠不是 hard gate**——重跑就過的不穩定測試不該擋上線（交給 `flaky-test-hunter` quarantine）。

## 執行流程

### Phase 1: 蒐集訊號

```bash
# 未關 P0/P1 bug（JIRA，full-mcp）
#   JQL: project = {KEY} AND fixVersion = {version} AND priority in (Highest, High) AND status != Done

# 各 gate 報告（markdown 模式讀本地）
ls .claude/compliance/compliance-report.md 2>/dev/null
ls .claude/perf/mobile-resource-report.md 2>/dev/null
ls .claude/offline/offline-resilience-report.md 2>/dev/null
grep -rl "Critical\|Blocker" .claude/ 2>/dev/null

# 測試結果（CI / junit xml）
find . -name "*.xml" -path "*test-results*" 2>/dev/null
```

缺的訊號標「未提供」，**不假設通過**（保守：未知 = 風險）。

### Phase 2: 套 gate 規則 + 算 readiness

```
hard_gates = [P0_open > 0, security_blocker > 0, compliance_blocker > 0]
if any(hard_gates): decision = NO-GO   # 不看分數

readiness = 100
 - 每個 soft gate 未達 → 依權重扣分
 - P1 open bug 每個 -X
 - 測試通過率每低 1% -Y
decision = GO if readiness >= threshold and no hard gate
         = CONDITIONAL-GO if 接近門檻且風險可接受
         = NO-GO otherwise
```

### Phase 3: 產 sign-off 文件

`qa-signoff-{version}.md`：

```markdown
# QA Sign-off · v3.2.0 · 2026-06-02

## 🎯 決策：⚠️ CONDITIONAL GO
Readiness: 84 / 100（門檻 80）

## 🚦 Gate 結果
| Gate | 類型 | 狀態 | 說明 |
|------|------|------|------|
| P0 open bug | 🔴 hard | ✅ 0 | — |
| Security blocker | 🔴 hard | ✅ 0 | semgrep clean |
| Compliance blocker | 🔴 hard | ✅ 0 | GDPR/PCI pass |
| P1 open bug | soft | ⚠️ 2 | PROJ-1234 / PROJ-1240（已列風險） |
| 回歸通過率 | soft | ✅ 98.2% | 218/222 |
| a11y Critical | soft | ⚠️ 1 | 對比度（非阻擋，已開單 P1） |
| 效能迴歸 | soft | ✅ | 冷啟動 +120ms（容忍內） |
| 離線韌性 | soft | ✅ | 8/8 場景 pass |
| Flaky 比率 | 參考 | 1.4% | 4 條 quarantine（不擋放行） |

## ⚠️ 已接受風險（Conditional Go 條件）
- PROJ-1234（P1）：邊緣帳號設定頁 crash — 影響 < 0.5% 用戶，hotfix 排下版
- a11y 對比度：商品價格對比 4.2:1（< 4.5）— 下版修

## 📋 上線後監控項
- [ ] 監控 PROJ-1234 相關 crash 率
- [ ] 觀察冷啟動 p90（已 +120ms）

## ✍️ 簽核
| 角色 | 姓名 | 決定 | 時間 |
|------|------|------|------|
| QA Lead | {待簽} | | |
| Release Owner | {待簽} | | |

## 📎 證據連結
- 回歸報告 · security-scan 報告 · compliance 報告 · 測試 CI run
```

### Phase 4: 通知 + 歸檔

- 發 sign-off 摘要通知（依 `config.notifications.enabled_channels` 可多管道）：
  - **Slack**（MCP）：發到 release channel，@release owner
  - **Telegram / Line**：見 [`modules/multichannel-notify.md`](./modules/multichannel-notify.md)（Bot API curl，token 從 config）
- 歸檔到 `.claude/signoff/`（可追溯）
- NO-GO 時：自動列出「要放行還缺什麼」清單（NO-GO 通知一定要發）

### Phase 5: 與發布銜接

- GO / CONDITIONAL-GO → 觸發 `publish-regression` 發布報告
- NO-GO → 擋住，回 `bug-report` / 各 gate skill 補洞

## ⚠️ 安全護欄

- ✅ **未提供的訊號視為風險**（不假設通過）——報告明確標「未驗證」
- ✅ **Flaky 不擋放行**（重跑就過 ≠ 真失敗）但要顯示比率供判斷
- ✅ Hard gate **不可被分數蓋過**（P0/security/compliance 不過就是 no-go）
- ✅ CONDITIONAL-GO **必須記錄已接受風險 + 監控項 + 簽核人**（不可空白放行）
- ❌ 不自動「簽核」——決策可自動算，但**簽名一定是人**

## ♿ a11y 必檢（本 skill 專屬）

- [ ] a11y Critical 數納入 gate（預設 soft，政府/金融可在 config 升 hard）
- [ ] sign-off 報告本身（若有 HTML 版）符合基本可讀性
- [ ] 已接受的 a11y 風險明確列入「上線後監控 / 下版修」清單，不可默默吞掉

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `qa_signoff.readiness_threshold` | GO 的最低分數 | 80 |
| `qa_signoff.hard_gates` | 硬性放行門（任一不過即 no-go） | p0_bug / security_blocker / compliance_blocker |
| `qa_signoff.soft_gate_weights` | 各 soft gate 扣分權重 | 見預設 |
| `qa_signoff.signoff_roles` | 必須簽核的角色 | QA Lead / Release Owner |
| `qa_signoff.block_on_flaky` | flaky 是否擋放行 | **false**（建議保持） |
| `jira.project_key` / `slack.release_channel_id` | 撈 bug / 發通知 | — |

## 範例

詳見 [`examples.md`](./examples.md)
