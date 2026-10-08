---
name: rsun-stack-deploy
description: 給 client + Phoenix module(s)，自動 wire 出 client repo (跨 module orchestration)。觸發詞：「stack deploy」「客戶部署」「組 stack」「給某客戶 wire 起 domain-rag + chatbot」「rsun-stack-deploy」。Phoenix Tier 4 第六進化 — 從 scaffold-generator → stack-architect。
---

# rsun-stack-deploy — 自動編排 client repo

## 用途

容晟接客戶時的常見場景：
- 「Apex Gold 要房產估價 chatbot + 文章 CMS」→ 需 domain-rag + chatbot-platform + cms-headless 三個 module
- 「wismth 要命理 D2C 加客服機器人」→ 需 domain-rag + chatbot-platform
- 「某客戶要 ERP 加 AI 異常偵測」→ 需 erp-companion

**沒有本 skill 之前**：senior-developer 手動 cp templates → 改 wrangler.toml → 改 binding ID → 寫 wire 邏輯，2-4 hr。

**有本 skill 之後**：1 個指令 1 分鐘搞定。

## 觸發

任何「給客戶部署一組 module」的需求，必先呼叫此 skill。

## 用法

### 基本（dry-run 看計畫）

```bash
python3 scripts/stack_deploy.py \
  --client apex-gold \
  --modules domain-rag,chatbot-platform,cms-headless
```

→ 印出計畫 + 偵測到的 integrations，不實寫。

### 真寫

```bash
python3 scripts/stack_deploy.py \
  --client apex-gold \
  --modules domain-rag,chatbot-platform \
  --apply
```

→ 實寫 `clients/apex-gold/` 含：
- `README.md` — 整體部署流程
- `setup.sh` — 一條龍腳本
- `domain-rag/` — 整 template 副本（已 patch wrangler.toml）
- `chatbot-platform/` — 同上 + RAG_ENDPOINT auto-wire 到 domain-rag worker URL

## 可用 modules（Phoenix v1 全 5 vertical）

| Module | Vertical | 用途 |
|---|---|---|
| `domain-rag` | ai | 領域 RAG chatbot 引擎 (corpus + 向量檢索 + 引用) |
| `crm-modern` | crm | B2B CRM (contacts/companies/deals/activities/pipelines) |
| `cms-headless` | cms | Workers-native headless CMS (collections + items + R2) |
| `chatbot-platform` | chatbot | 對話層 (sessions + multi-channel + personalities) |
| `erp-companion` | erp | Odoo/ERPNext companion (cache + AI 異常 + webhook) |

## Auto-wire 規則

當你選的 modules 滿足某 integration rule，自動 wire：

| 觸發 modules | 自動 wire |
|---|---|
| `chatbot-platform + domain-rag` | chatbot 的 `RAG_ENDPOINT` 自動填到 domain-rag worker URL |
| `crm-modern + chatbot-platform` | 建議在 README 提示 `personality: sales-assistant` + 寫 webhook 把對話 lead 進 contacts |
| `erp-companion` (任何時候) | 已預設接 rsun-worker /api/ai/chat (5-LLM waterfall) |

## 客戶情境範例

### Apex Gold (房產 ESG)
```bash
python3 scripts/stack_deploy.py \
  --client apex-gold \
  --modules domain-rag,chatbot-platform,cms-headless \
  --apply
```
- domain-rag corpus = 實價登錄 + 法規
- chatbot-platform → personality `realestate-agent`
- cms-headless → 房源列表 (collections=properties)

### wismth (命理 D2C)
```bash
python3 scripts/stack_deploy.py \
  --client wismth \
  --modules domain-rag,chatbot-platform \
  --apply
```
- domain-rag corpus = 命理三本聖經
- chatbot-platform → personality `helpful-zh-tw`

### legal-firm (法律事務所)
```bash
python3 scripts/stack_deploy.py \
  --client some-legal \
  --modules domain-rag,chatbot-platform,crm-modern \
  --apply
```
- domain-rag corpus = 判例 + 條文
- chatbot-platform → personality `legal-consultant`
- crm-modern → 改名 contacts → clients (手動 schema patch)

### 製造業 ERP 加 AI
```bash
python3 scripts/stack_deploy.py \
  --client some-mfg \
  --modules erp-companion \
  --apply
```
- 接客戶既有 Odoo
- AI 異常發票偵測

## 紀律

- 預設 dry-run，必加 `--apply` 才實寫
- 同名 client 已存在 → abort（不會覆蓋）
- 不複製 `node_modules` / `.wrangler` / `*.log` (太重)
- 不放 client secrets 進 repo（留空殼讓客戶 `wrangler secret put`）

## v2 規劃

- [ ] 加 `--target apex-gold-realestate` 客戶 profile（從 contingency-matrix 注入）
- [ ] 自動跑 `npm install` + `wrangler login` 檢查
- [ ] 加 GitHub repo 自動 init + push
- [ ] 加 deployment metric 自動回填到 METRIC

---

> 「Phoenix #6 進化：從『產 scaffold』→『編排可部署的 client stack』。
> 客戶 onboard 從 4 hr 降到 1 min（不含 wrangler login + secrets 設定，那 30 min）。」
