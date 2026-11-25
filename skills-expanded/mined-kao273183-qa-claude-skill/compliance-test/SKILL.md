---
name: compliance-test
description: 把法規合規（GDPR / CCPA·CPRA / PCI-DSS / HIPAA / SOC 2 / EU EAA）轉成可驗證的合規 TC 與 audit checklist，掃 code/config 找證據缺口，產出含嚴重度分級、法條引用、罰則風險的合規缺口報告 + 稽核 log。當使用者提到「合規測試 / compliance test / GDPR / CCPA / CPRA / PCI-DSS / HIPAA / SOC2 / 個資法 / 資料保留 / 同意管理 / 被遺忘權 / data subject rights / 合規稽核 / 法規檢查」時觸發。配套：security-scan（技術漏洞，本 skill 是法規層）、a11y-audit（無障礙合規 EAA/Section508）、test-master（規劃合規 TC）、bug-report（追合規缺口）。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[法規 / 功能範圍] [--regulations=GDPR,PCI-DSS] [--region=EU|US-CA|TW]"
---

# compliance-test

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

現有 skill 各管一塊，但「**法規合規**」沒人覆蓋：
- `security-scan` 找**技術漏洞**（SQLi / XSS / 弱密碼）— 是「程式對不對」
- `a11y-audit` 查**無障礙**（WCAG）— 是「障礙者用不用得到」
- `test-master` 規劃**功能 TC** — 是「功能對不對」

但合規問的是「**做這件事合不合法**」：同意有沒有先取得？卡號有沒有落地？個資刪除請求 30 天內有沒有處理？稽核軌跡完不完整？

> 你已有 `government` / `enterprise` preset，卻沒有對應的合規 skill —— 本 skill 補這個缺口。

→ 本 skill 把**法規條文**翻成**可驗證的 control + TC + 證據掃描**。

## 適用場景

- ✅ 金融 / 醫療 / 政府 / 跨境 SaaS — 受法規約束
- ✅ 上線前 / 稽核前 合規 readiness 檢查
- ✅ 進入新市場（歐盟 / 加州 / 醫療）前的 gap 分析
- ✅ 處理信用卡 / 健康資料 / 個資的新功能
- ✅ 產生稽核員要看的合規證據包

## 不適用場景

- ❌ 找技術漏洞 — 用 `security-scan`
- ❌ 無障礙細項 — 用 `a11y-audit`（本 skill 只在 EAA/Section508 層連動）
- ❌ 法律意見 — 本 skill 產**工程可驗證項**，不取代法務／DPO 審核

## ⚠️ 重要免責

本 skill 協助**工程團隊把合規要求落實到可測項**，產出供法務 / DPO / 稽核員審閱的證據。**不構成法律意見**，最終合規判定須由合格法律專業人士確認。報告會明確標註此點。

## 支援法規 + control 對照

| 法規 | 地區 / 適用 | 核心 control（本 skill 可驗的） |
|------|------------|------------------------------|
| **GDPR** | 歐盟個資 | 同意先行、被遺忘權、資料可攜、72h breach 通知、資料最小化、DPO |
| **CCPA / CPRA** | 加州消費者 | opt-out「Do Not Sell」、資料揭露請求、刪除請求、敏感資料限制 |
| **PCI-DSS v4.0** | 收信用卡 | 卡號不落地、傳輸加密 (TLS)、tokenization、不存 CVV、存取控管 |
| **HIPAA** | 美國醫療 PHI | PHI 加密（傳輸+靜態）、最小必要、access log、BAA、自動登出 |
| **SOC 2** | B2B SaaS 信任 | 存取控管、變更管理、稽核軌跡、加密、可用性監控 |
| **EU EAA / Section 508 / ADA** | 無障礙法規 | → 委派 `a11y-audit`，本 skill 收斂其結果到合規報告 |
| **個資法 (TW PDPA)** | 台灣個資 | 告知同意、特定目的、當事人權利、安全維護義務 |

## 嚴重度分級（合規 × 罰則風險）

| 等級 | 定義 | 範例 |
|------|------|------|
| 🔴 **Blocker** | 直接違法、可被立即裁罰 / 禁止上線 | 卡號明文落地、無同意就收集個資 |
| 🟠 **Critical** | 法規明訂義務未實作 | 無「刪除我的資料」流程、無 breach 通知機制 |
| 🟡 **Major** | 有實作但不完整 / 可舉證不足 | 有同意但無撤回途徑、稽核 log 不含 actor |
| 🟢 **Minor** | 最佳實踐建議 | 同意文案可更白話、保留期可再縮短 |

## 執行流程

### Phase 1: 判定適用法規

依「地區 × 產業 × 處理的資料類型」推導，不要全測：

```
收信用卡？        → PCI-DSS
有歐盟使用者？     → GDPR
有加州使用者？     → CCPA/CPRA
存健康/醫療資料？  → HIPAA
台灣個資？        → PDPA
B2B 要過稽核？    → SOC 2
有 UI？           → EAA/Section508（委派 a11y-audit）
```

互動式確認後，載入對應 control checklist。

### Phase 2: 證據掃描（code / config）

對每條 control 自動找證據，標 ✅ 有證據 / ⚠️ 證據不足 / ❌ 找不到：

```bash
# PCI-DSS: 卡號 / CVV 是否落地（log / DB / 變數）
grep -rniE "card[_ ]?number|pan|cvv|cvc|card[_ ]?code" --include=*.{kt,swift,py,ts,js,sql} .

# GDPR: 是否有同意管理 / 刪除流程
grep -rniE "consent|gdpr|right.to.be.forgotten|data.deletion|erasure" .

# HIPAA / 通用: 是否有稽核 log
grep -rniE "audit[_ ]?log|access[_ ]?log|activity[_ ]?trail" .

# 加密傳輸: 是否有明文 http / 寫死的 endpoint
grep -rniE "http://(?!localhost|127\.)" --include=*.{kt,swift,ts,js} .
```

> 掃描只證明「找不到證據」，**不等於違規** — 報告會請人工確認，不誇大。

### Phase 3: 合規缺口報告

合併掃描結果 → `compliance-report.md`：

```markdown
# Compliance Report · my-app · 2026-06-02

## 📋 範圍
- 法規: GDPR + PCI-DSS v4.0
- 地區: EU + 收信用卡
- ⚠️ 本報告為工程可驗證項，非法律意見，須經 DPO/法務確認。

## 📊 合規評分
| 法規 | controls | Pass | Gap | 評分 |
|------|----------|------|-----|------|
| GDPR | 18 | 13 | 5 | 72% |
| PCI-DSS | 24 | 22 | 2 | 92% |

## 🔴 Blocker（上線前必修）

### PCI-DSS 3.4 — 卡號明文落地
- **法條**: PCI-DSS v4.0 Req 3.4「PAN 須遮蔽 / 不可還原儲存」
- **證據**: `PaymentLogger.kt:88` 把完整卡號寫進 log
  ```kotlin
  Log.d("payment", "charging card $cardNumber")  // ❌ 卡號落地
  ```
- **修法**: 只 log 後四碼 `****${cardNumber.takeLast(4)}`，或改用 token
- **罰則風險**: PCI 罰款 + 銀行停止收單資格

### GDPR Art.7 — 收集個資前無同意
- **法條**: GDPR Art.6/7「處理須有合法基礎，同意須事前、明確、可撤回」
- **證據**: 找不到 consent gate（`grep consent` 無結果）
- **修法**: 加入同意畫面，記錄同意時間戳 + 版本，提供撤回入口

## 🟠 Critical / 🟡 Major / 🟢 Minor
[依等級列出，含法條 + 證據 + 修法]

## 📝 須人工確認（工具無法自動驗）
- [ ] 隱私權政策是否涵蓋實際收集欄位
- [ ] 是否簽署 BAA（HIPAA）/ DPA（GDPR 處理者）
- [ ] breach 通知流程是否能在 72h 內啟動
- [ ] 資料保留排程是否真的有跑（非只是寫在文件）

## 📈 趨勢
- 上次 audit (2026-05): GDPR 61% / PCI 88%
- 這次:                 GDPR 72% / PCI 92%
```

### Phase 4: 生成合規 TC

把每條 control 轉成可重複跑的 TC（進 Sheet 或 markdown，套 14 欄格式）：

| ID | 標題 | 分類 | 優先度 | 前置 | 步驟 | 預期 |
|----|------|------|--------|------|------|------|
| CMP-GDPR-001 | 使用者可請求刪除個資 | 功能測試 | P0 | 已登入有資料 | 設定→刪除帳號→確認 | 30 天內資料清除，回確認信 |
| CMP-PCI-003 | 卡號不出現在 log | API 驗證測試 | P0 | 完成一筆付款 | 搜尋 log | log 僅後四碼，無完整 PAN |

→ 可接 `tc-to-pytest`（API 類）或 `test-automation`（UI 類）自動化。

### Phase 5: 稽核 log + 建 ticket

- 每次 audit 寫不可竄改的稽核紀錄到 `compliance_test.audit_log_path`（誰、何時、跑了哪些法規、結果）
- Blocker / Critical 自動 propose 為 P0 JIRA ticket（用 `bug-report`）
- 可選：把合規 TC 排進 release-gate（接 `regression-test` / `qa-signoff`）

## ⚠️ 安全護欄

- ❌ 不出具法律結論 — 一律標「須法務/DPO 確認」
- ❌ 不誇大 — 「找不到證據」≠「違規」，明確區分
- ✅ 報告含「須人工確認」section（工具盲區）
- ✅ 處理真實個資 / 卡號的掃描只在程式碼層，**不外傳任何樣本資料**
- ✅ Blocker 預設擋上線（接 `qa-signoff`）

## ♿ a11y 必檢（本 skill 專屬）

合規流程的 UI 本身也要無障礙（否則 EAA 反而不合規）：
- [ ] 同意畫面的 checkbox / 按鈕有 label，TalkBack / VoiceOver 讀得出
- [ ] 「刪除我的資料」「Do Not Sell」入口在字級放大 (AX5 / 200%) 下不破版
- [ ] 隱私設定的開關狀態（開/關）有 accessibility value，不只靠顏色
- [ ] 錯誤訊息（如同意未勾）非僅紅色，附文字說明

> 深度無障礙審查委派 `a11y-audit --standard=Section508`。

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `compliance_test.regulations` | 啟用的法規清單 | `[]`（不啟用） |
| `compliance_test.region` | 地區（推導適用法規） | `""` |
| `compliance_test.severity_threshold` | 擋上線門檻 | `critical` |
| `compliance_test.audit_log_path` | 稽核紀錄輸出位置 | `.claude/compliance/audit.log` |
| `workflow.auto_cross_platform_check` | 合規缺口自動配對 iOS+Android | true |

## 範例

詳見 [`examples.md`](./examples.md)
