---
name: rsun-adr
description: 建立架構決策記錄（ADR）。當做重要技術選型決策時使用：選資料庫、決定架構模式、選擇 AI 框架、決定認證方案、選部署平台。採用 Michael Nygard 輕量格式。
user-invocable: true
allowed-tools: "Read Write Bash(ls * mkdir * cat *)"
---

# rsun-adr — 架構決策記錄（Architecture Decision Record）

ADR 記錄重大技術決策的「為什麼」。確保未來成員理解決策背景，避免在錯誤的時機點重新打開已解決的問題。一個好的 ADR 誠實說明取捨，不美化，不迴避負面影響。

---

## 何時寫 ADR？（任一符合即需要）

✅ **需要寫 ADR：**
- 選擇資料庫類型（關聯式 vs NoSQL vs 混合）
- 決定架構模式（Monolith / Modular Monolith / Microservices）
- 選擇第三方服務（金流、地圖、簡訊、AI provider）
- 決定認證方案（JWT / Session / OAuth）
- 選擇部署平台（Vercel / CF Pages / Fly.io / AWS）
- 建立重要設計模式（CQRS、Event Sourcing、API Gateway）
- 決定放棄某技術（記錄「為什麼不用」）

❌ **不需要 ADR：**
- 例行 library 選擇（UI 元件、date utils）
- 可以輕易反轉的小決定
- 格式、命名慣例等實作細節

---

## ADR 格式（Nygard 輕量格式）

```markdown
# ADR-[NNN]: [動詞 + 名詞，簡潔說明決定]

**狀態：** Proposed | Accepted | Deprecated | Superseded by ADR-[NNN]
**日期：** YYYY-MM-DD
**專案：** [專案名稱]
**決策者：** [名字]

---

## 背景（Context）

[描述促使這個決定的情況與制約因素。
說明系統在做什麼、面對什麼問題、有哪些技術/業務限制。
只陳述事實，不評判，不推薦。]

## 考慮選項

| 選項 | 優點 | 缺點 |
|------|------|------|
| 選項 A（[名稱]）| ... | ... |
| 選項 B（[名稱]）| ... | ... |
| 選項 C（[名稱]）| ... | ... |

## 決定（Decision）

我們決定採用 **[選項 X]**。

理由：[2-3 句，說明為什麼這個選項最適合當前情境]

## 後果（Consequences）

**✅ 變得更容易的事：**
- ...

**⚠️ 變得更困難的事：**
- ...

**📋 新的限制或約束：**
- ...
```

---

## ADR 存放位置

```
~/Projects/[repo]/docs/adr/
├── README.md          ← ADR 索引（自動維護）
├── ADR-001-[描述].md
├── ADR-002-[描述].md
└── ...
```

命名規則：`ADR-[三位數字]-[kebab-case-描述].md`
範例：
- `ADR-001-use-postgresql-as-primary-database.md`
- `ADR-002-adopt-nextjs-app-router.md`
- `ADR-003-use-cloudflare-pages-over-vercel.md`

---

## 系統設計決策速查

執行 ADR 時，以下決策樹幫助快速收斂選項：

### 資料庫選型

```
需要複雜 JOIN 查詢 / ACID 事務？
  → 是 → PostgreSQL（首選）/ MySQL
需要彈性 schema / JSON 文件？
  → MongoDB / Firestore（Firebase）
需要高速 K-V / Session / 快取？
  → Redis
需要全文搜尋？
  → Elasticsearch / pgvector（PostgreSQL 擴充）
需要時序資料（IoT / 監控）？
  → TimescaleDB / InfluxDB
```

### 架構模式選型（從小做起）

```
團隊 < 5 人 + 單一業務域 + 早期產品？
  → Monolith（先跑起來最重要）

多業務域 + 需要獨立部署 + 團隊擴張？
  → Modular Monolith（推薦：先做這個再說）
  邊界清楚後再考慮拆 Microservices

規模龐大 + 團隊 > 20 人 + 業務域穩定？
  → Microservices（謹慎，運維成本極高）
```

### CAP 定理選型

```
電商訂單 / 金融交易 / 庫存
  → CP（一致性優先）→ PostgreSQL / MySQL

社群 / 內容 / 推薦 / 搜尋
  → AP（可用性優先）→ Cassandra / DynamoDB

一般 CRUD 應用（80% 的情況）
  → CP 就夠 → PostgreSQL
```

### 快取策略

```
讀多寫少，資料不常變（商品頁、設定檔）
  → Cache-aside（Redis，手動更新）

讀寫均衡，一致性重要（訂單狀態）
  → Write-through（寫入時同步更新快取）

高速寫入，可接受輕微延遲（Log、統計）
  → Write-behind（非同步寫入 DB）

預測性熱資料（排行榜、首頁內容）
  → Refresh-ahead（背景定時刷新）
```

### API 設計選型

```
一般 REST CRUD API
  → REST（簡單、工具成熟、客戶容易理解）

前端複雜查詢需求（多種資料組合）
  → GraphQL（彈性但學習曲線高）

服務間高效能通訊（Microservices 內部）
  → gRPC（效能好但僅限後端間）

即時雙向通訊（聊天、通知、儀表板）
  → WebSocket / Server-Sent Events
```

### 認證方案選型

```
傳統 Web App（表單登入，Server-side session）
  → Session + Cookie（簡單，安全）

API-first / Mobile App / SPA
  → JWT（無狀態，適合分散式）
  注意：短期 access token + refresh token 機制

第三方社群登入（Google / GitHub）
  → OAuth 2.0 / OIDC（不要自己實作）
  推薦：NextAuth.js / Auth.js / Clerk

企業 SSO（B2B 客戶）
  → SAML 2.0 / OIDC + 企業 IdP
```

### 部署平台選型（容晟科技常用）

```
靜態網站 / 簡單 Serverless
  → Cloudflare Pages（便宜，全球 CDN）

Next.js / React 全端應用
  → Vercel（最佳 DX，與 Next.js 深度整合）

需要長時間執行 / WebSocket
  → Fly.io（有 persistent container）

純 Edge Logic / API Gateway
  → Cloudflare Workers（超低延遲）
```

---

## ADR 索引模板（docs/adr/README.md）

```markdown
# 架構決策記錄（ADR Index）

本目錄記錄 [專案名] 的所有重大技術決策。

| ADR | 標題 | 狀態 | 日期 |
|-----|------|------|------|
| [ADR-001](ADR-001-xxx.md) | ... | ✅ Accepted | YYYY-MM-DD |
| [ADR-002](ADR-002-xxx.md) | ... | ✅ Accepted | YYYY-MM-DD |
```

---

## 注意事項

- ADR 只記錄「決定」，不是討論記錄
- **Consequences 必須誠實說明負面影響**，不美化
- 狀態改為 Superseded 時，在舊 ADR 加上指向新 ADR 的連結
- 每個專案的 ADR-001 通常是「確認主要語言 / 框架」
- ADR 一旦 Accepted，不能修改正文（只能新增 Superseded by）
