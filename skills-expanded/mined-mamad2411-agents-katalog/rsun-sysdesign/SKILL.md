---
name: rsun-sysdesign
description: 系統設計決策框架。當需要做架構技術選型、評估系統擴展策略、AI/LLM 架構設計、或回答「這個系統應該怎麼設計」時使用。整合 system-design-primer、ByteByteGo system-design-101、awesome-software-architecture、Vercel AI SDK 的核心決策框架。
user-invocable: true
allowed-tools: "Read Write WebSearch"
---

# rsun-sysdesign — 系統設計決策框架

整合自 donnemartin/system-design-primer（298k ⭐）、ByteByteGoHq/system-design-101（65k ⭐）、mehdihadeli/awesome-software-architecture（20k ⭐）。

這份 skill 的目的是：**在 30 分鐘內對新專案做出初步架構決策**，後續用 `/rsun-adr` 記錄每個決定。

---

## Phase 1：需求收集（先問，再設計）

在畫任何架構圖之前，必須先確認：

### 功能性需求
- 主要用戶行為是什麼？（CRUD / 搜尋 / 上傳 / 串流 / 即時通訊）
- 資料的讀寫比是多少？（讀多還是寫多）
- 最核心的 3 個 API / 頁面是什麼？

### 非功能性需求
```
規模（Scale）：
  - 預計用戶數量：[日活 / 月活]
  - 資料量：[TB / GB，5 年後的預估]
  - 峰值 QPS（每秒請求數）：[正常 / 峰值]

可用性（Availability）：
  - SLA 要求：[99.9% = 8.7hr/年停機 / 99.99% = 52min/年]
  - 是否接受最終一致性？

一致性（Consistency）：
  - 金融 / 訂單 → 強一致性
  - 社群 / 內容 → 最終一致性可接受

延遲（Latency）：
  - P95 API 回應時間：[< 200ms / < 1s]
  - 讀取 vs 寫入延遲要求是否不同？
```

---

## Phase 2：架構模式選型

### 決策樹

```
這是第一版 MVP / 小團隊（< 5 人）？
  → YES → Monolith（先做，未來再拆）
  → NO ↓

業務域清楚，有 2-3 個明顯邊界？
  → YES → Modular Monolith（推薦！）
  → NO ↓

團隊 > 15 人，業務穩定，有強 DevOps 能力？
  → YES → Microservices（謹慎）
  → NO → 繼續用 Modular Monolith
```

### 架構風格比較

| 架構 | 適合情境 | 運維複雜度 | 開發速度 |
|------|---------|-----------|---------|
| Monolith | 早期產品、小團隊、MVP | ⭐ 低 | ⭐⭐⭐ 快 |
| Modular Monolith | 成長期、清楚業務邊界 | ⭐⭐ 中 | ⭐⭐ 中 |
| Microservices | 大規模、多團隊、穩定業務 | ⭐⭐⭐ 高 | ⭐ 慢 |

### 常見架構模式（依用途選擇）

| 問題情境 | 推薦模式 |
|---------|---------|
| 複雜業務邏輯 + 多角色 | Domain-Driven Design（DDD）|
| 讀寫模型差異大 | CQRS（讀寫分離）|
| 需要完整操作歷史 | Event Sourcing |
| 服務間需要解耦 | Event-Driven Architecture |
| 多客戶端（Web / Mobile / 第三方）| BFF（Backend for Frontend）|
| 長流程跨服務事務 | Saga Pattern |
| 舊系統逐步替換 | Strangler Fig Pattern |
| 乾淨的分層邊界 | Clean / Hexagonal Architecture |

---

## Phase 3：資料儲存選型

### 主要資料庫選型

```
需要 ACID 事務 / 複雜 JOIN？
  → PostgreSQL（首選，幾乎萬用）

需要彈性 schema / 文件 / JSON？
  → MongoDB（適合 schema 不穩定的早期產品）
  → Firestore（適合 Firebase 生態）

需要高速 K-V / Session / 排行榜？
  → Redis（記憶體，超快，但有限制）

需要全文搜尋 / 向量搜尋？
  → Elasticsearch（專業搜尋）
  → pgvector（PostgreSQL 擴充，小規模夠用）

需要時序資料（IoT / 監控日誌）？
  → TimescaleDB / InfluxDB
```

### 資料擴展策略

```
讀取瓶頸？
  → Read Replica（主從複製，讀寫分離）
  → 加快取層（Redis）

寫入瓶頸？
  → Sharding（水平分片，複雜度高）
  → CQRS（事件驅動，寫入非同步化）

資料量太大？
  → 冷熱分離（熱資料 PostgreSQL，冷資料 S3）
  → 定期歸檔
```

---

## Phase 4：快取策略

### 快取位置決策

```
Client（瀏覽器）→ CDN → Load Balancer → App Server → DB Cache → DB
                                          ↑
                                       Redis Cache
```

| 層級 | 技術 | 適合的資料類型 |
|------|------|-------------|
| 瀏覽器 Cache | HTTP Cache-Control | 靜態資源（CSS, JS, 圖片）|
| CDN | Cloudflare / Vercel Edge | 靜態頁面、API 回應 |
| Application | Redis | Session、常用查詢結果 |
| Database | Query Cache | 熱門 SQL 查詢 |

### 快取更新策略

| 策略 | 說明 | 適合 |
|------|------|------|
| Cache-aside（旁路）| 讀取時 miss 才寫入 cache | 讀多寫少，商品頁 |
| Write-through | 寫 DB 同時更新 cache | 一致性重要，訂單狀態 |
| Write-behind | 先寫 cache，非同步寫 DB | 高寫入吞吐，日誌統計 |
| Refresh-ahead | 背景定時刷新熱資料 | 排行榜、首頁推薦 |

### 快取失效問題

- **Cache Stampede**：大量請求同時 cache miss → 使用 Mutex 鎖或 Promise coalescing
- **Cache Penetration**：查不存在的資料 → 回寫 null，加 Bloom Filter
- **Cache Avalanche**：大量 key 同時過期 → 加隨機 TTL jitter

---

## Phase 5：API 設計

### API 風格選型

| 風格 | 優點 | 缺點 | 適合 |
|------|------|------|------|
| REST | 簡單、工具成熟、易理解 | Over-fetching | 一般 CRUD、公開 API |
| GraphQL | 靈活查詢、減少 round-trip | 學習曲線、N+1 問題 | 複雜前端、多客戶端 |
| gRPC | 高效能、強型別 | 瀏覽器支援差 | 服務間通訊 |
| WebSocket | 雙向即時 | 狀態管理複雜 | 聊天、即時通知 |
| SSE | Server→Client 單向 | 只能伺服器推 | Dashboard、通知推播 |

### REST 設計原則

```
GET    /properties          → 列表
GET    /properties/:id      → 單筆
POST   /properties          → 新增
PUT    /properties/:id      → 完整更新
PATCH  /properties/:id      → 部分更新
DELETE /properties/:id      → 刪除

狀態碼：
  200 OK / 201 Created / 204 No Content
  400 Bad Request / 401 Unauthorized / 403 Forbidden
  404 Not Found / 409 Conflict / 422 Unprocessable
  429 Too Many Requests / 500 Internal Server Error
```

---

## Phase 6：可用性 & 彈性設計

### CAP 定理應用

```
電商訂單 / 金融 / 庫存 → CP（一致性 + 分區容錯）
  → 強一致性，犧牲部分可用性
  → PostgreSQL + 同步複製

社群 / 內容 / 推薦 / 搜尋 → AP（可用性 + 分區容錯）
  → 最終一致性，永遠可用
  → Cassandra / DynamoDB

大多數 B2B CRUD 應用 → CP 就夠了
  → PostgreSQL 就好，不要過度設計
```

### 高可用性設計

| 模式 | 說明 | Downtime |
|------|------|---------|
| Active-Passive | 備援節點，主掛了切換 | ~30s failover |
| Active-Active | 多節點同時服務，分流 | ~0s |
| Multi-AZ | 跨資料中心備援 | 地區性災難保護 |

### 彈性模式

| 模式 | 說明 |
|------|------|
| Circuit Breaker | 下游服務掛了時，快速失敗，避免雪崩 |
| Retry + Backoff | 失敗自動重試，指數退避 |
| Bulkhead | 隔離不同功能的資源池，防止一個壞所有 |
| Rate Limiting | 限制 API 請求頻率，防過載 |
| Timeout | 設定合理超時，不讓慢請求拖垮系統 |

---

## Phase 7：非同步 & 訊息傳遞

### 何時需要訊息佇列（Message Queue）？

```
需要非同步 → 否則等太久影響 UX（圖片處理、Email 發送）
需要解耦 → 發布方不需要知道接收方
需要背壓 → 限制下游處理速度，防爆量
需要可靠性 → 確保訊息不丟失（訂單確認）
```

### 工具選型

| 工具 | 適合 | 注意 |
|------|------|------|
| Redis Pub/Sub | 簡單通知，不需要持久化 | 訂閱者離線會丟失訊息 |
| Redis Queue（BullMQ）| 任務佇列，需要持久化 | 容晟常用，簡單夠用 |
| Kafka | 高吞吐、事件溯源、多消費者 | 架設成本高，小專案不需要 |
| RabbitMQ | 複雜路由、多協議 | 比 Kafka 簡單，但不如 Redis 輕量 |

---

## 系統設計清單（設計完後自查）

```
功能面：
  - [ ] 主要功能都覆蓋了嗎？
  - [ ] 用戶認證方案確認了嗎？
  - [ ] 讀寫比估算了嗎？

資料面：
  - [ ] 資料庫選型有理由嗎？（→ 用 /rsun-adr 記錄）
  - [ ] 需要快取嗎？快取什麼？
  - [ ] 資料備份策略？

擴展性：
  - [ ] 流量 10x 的時候，哪裡會是瓶頸？
  - [ ] 是否需要 Load Balancer？
  - [ ] 是否需要 CDN？

可靠性：
  - [ ] 單點失敗在哪裡？
  - [ ] Circuit Breaker 是否需要？
  - [ ] 重要操作的 Retry 策略？

安全性：
  - [ ] 認證 / 授權方案？
  - [ ] 敏感資料加密？（at rest + in transit）
  - [ ] Rate Limiting？
  - [ ] SQL Injection / XSS 防護？

運維面：
  - [ ] Logging 策略（結構化 JSON log）？
  - [ ] Monitoring & Alerting（Uptime / Error rate / Latency）？
  - [ ] 部署策略（Blue/Green / Canary）？
```

---

## Phase 8：AI / LLM 架構決策

當系統涉及 AI 功能（翻譯、搜尋、推薦、生成、分析），在傳統系統設計之外額外執行本 Phase。

### 8.1 LLM Provider 選型

```
任務需要最高推理能力（複雜分析、程式生成）？
  → Claude Sonnet / Opus（Anthropic）

任務需要超長 context（大量文件、程式庫）？
  → Gemini 1.5 Pro（200k token）/ Claude（200k token）

任務需要超快速度（即時回應、高並發）？
  → Groq（Llama / Gemma，毫秒等級）

任務需要圖片 / 影像理解？
  → GPT-4o / Gemini Vision / Claude Vision

需要本地部署 / 資料不出境？
  → Ollama + Llama 3 / Mistral

成本最敏感 + 簡單任務？
  → Gemini Flash / Claude Haiku / GPT-4o-mini
```

### 8.2 容晟瀑布流（Provider Cascade）

參考 TRACKER knowledge graph 的既有設計：

```
Request 進來
    ↓
Groq（主力，最快最便宜）
    ↓ 失敗/超時
Cloudflare AI Gateway（備援 + 路由）
    ↓ 失敗
Gemini Flash（Google 備援）
    ↓ 失敗
Claude Haiku（最終備援）
```

實作：Vercel AI SDK `experimental_fallback` 或自訂 retry 邏輯。

### 8.3 RAG 架構（Retrieval-Augmented Generation）

何時需要 RAG：
- 知識庫 / 文件問答（客戶手冊、法規、產品目錄）
- 資料超過 LLM context window
- 需要引用來源 / 防幻覺
- 資料需要實時更新

RAG 四層：
```
[資料層]   文件 / 資料庫 / API → 分塊（Chunking）
[嵌入層]   Embedding Model → 向量化
[儲存層]   向量資料庫 → 相似度搜尋
[生成層]   LLM + Retrieved Context → 回答
```

Chunking 策略：
```
固定大小（512 token）→ 簡單，但切斷語意
語意分塊（句子 / 段落）→ 品質好，需要 NLP
階層式（章節 → 段落）→ 適合結構化文件
```

### 8.4 向量資料庫選型

```
已有 PostgreSQL，資料量 < 100萬向量？
  → pgvector（最省，不用另建服務）

需要高效能、多租戶、雲端托管？
  → Pinecone（成熟、Serverless 定價）

需要開源自建、功能豐富？
  → Weaviate / Qdrant（Docker 部署）

需要與 Cloudflare 深度整合？
  → Vectorize（CF 原生向量 DB）
```

### 8.5 Embedding Model 選型

```
多語言（中文 + 英文 + 越南文）？
  → text-embedding-3-large（OpenAI，最通用）
  → multilingual-e5-large（開源，本地部署）

中文優化？
  → m3e-large（中文特化，Hugging Face）

速度敏感 + 省成本？
  → text-embedding-3-small（OpenAI，便宜 5 倍）
  → nomic-embed-text（Ollama 本地）
```

### 8.6 AI SDK 選型

```
Next.js / Vercel 生態？
  → Vercel AI SDK（useChat / useCompletion / streamText）
  → 支援 30+ provider，統一介面，Streaming 原生支援

需要複雜 Agent / 工具鏈？
  → LangChain.js / LlamaIndex.TS（工具多但重）
  → 容晟推薦：Vercel AI SDK + 自訂 tool use

Python 後端？
  → LangChain / LlamaIndex / Haystack

Anthropic 直接 SDK？
  → @anthropic-ai/sdk（工具使用、思考模式、快取）
```

### 8.7 AI Agent 架構

```
單一任務，不需要規劃？
  → 直接 LLM call（最簡單）

需要使用工具（搜尋 / 計算 / API）？
  → ReAct Pattern（推理 → 行動 → 觀察 → 再推理）
  → Vercel AI SDK tool use

需要多步驟複雜任務？
  → Multi-step Agent（claude-code 模式）

需要多個 Agent 協作？
  → Multi-Agent（Orchestrator + Workers）
  → 注意：複雜度高，小專案不需要
```

### 8.8 Prompt 管理策略

```
版本控制：
  → Prompt 存在 DB，帶版本號（不要 hardcode 在程式裡）
  → A/B 測試不同 prompt 版本

快取（Prompt Caching）：
  → Anthropic：system prompt 超過 1024 token 啟用快取（省 90% 費用）
  → 把固定的 context / 文件放在 system prompt 前段

防幻覺策略：
  → RAG 提供來源 → 要求 LLM 只引用提供的資料
  → 結構化輸出（JSON schema）→ 減少格式錯誤
  → Self-consistency：同一問題問 3 次取多數答案
```

### 8.9 AI 成本控制

```
最大槓桿（依序）：

1. 模型降級：複雜任務用 Sonnet，簡單分類用 Haiku
   → 同任務可省 5-20 倍成本

2. Prompt Caching：長 system prompt 快取
   → 省 90% input token 費用

3. Streaming：用戶感知變好，不影響成本但降低 timeout

4. Batch API：非即時任務（夜間處理）→ 省 50% 費用

5. 本地模型：高並發簡單任務 → Ollama + Llama/Gemma
```

### AI 架構 Checklist

```
  - [ ] LLM Provider 選型完成並有 ADR？
  - [ ] 是否需要 RAG？向量 DB 選型了嗎？
  - [ ] Embedding model 支援所需語言？
  - [ ] AI SDK 選型（Vercel AI SDK / LangChain / 直接 SDK）？
  - [ ] Prompt 版本控制策略？
  - [ ] Prompt Caching 設定了嗎？（Anthropic system prompt > 1024 token）
  - [ ] Provider 失敗時的 fallback 策略？
  - [ ] AI 回應的成本估算（月費）？
  - [ ] 敏感資料不傳給第三方 LLM 的保護？
  - [ ] AI 輸出的驗證（hallucination 防護）？
```

---

## 輸出：架構摘要格式

設計完後用這個格式輸出，方便進 `/rsun-adr` 記錄：

```markdown
## 架構摘要 — [專案名稱]

**架構模式：** [Monolith / Modular Monolith / Microservices]
**主要資料庫：** [PostgreSQL / MongoDB / ...]
**快取：** [Redis / 無]
**訊息佇列：** [BullMQ / Kafka / 無]
**API 風格：** [REST / GraphQL]
**認證方案：** [JWT + Refresh / Session / OAuth]
**部署：** [Vercel / CF Pages / Fly.io]
**CDN：** [Cloudflare / Vercel Edge]

**AI 相關（如有）：**
**LLM Provider：** [Claude / Gemini / Groq / ...]
**RAG：** [有 / 無]
**向量 DB：** [pgvector / Pinecone / 無]
**AI SDK：** [Vercel AI SDK / LangChain / 直接 SDK]
**瀑布流：** [Groq → CF → Gemini → Claude / 無]

**主要 ADR 需要決策：**
- [ ] ADR-001: 資料庫選型
- [ ] ADR-002: 認證方案
- [ ] ADR-003: LLM Provider（如有 AI 功能）
- [ ] ADR-00N: [其他重要決策]
```
