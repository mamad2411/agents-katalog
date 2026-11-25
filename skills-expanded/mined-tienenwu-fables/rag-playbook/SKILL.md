---
name: rag-playbook
description: Use when building or debugging RAG / semantic search / retrieval systems — before choosing a vector store (pgvector, Qdrant, Milvus, Elasticsearch), designing chunking, embedding models, hybrid search (BM25 + vector), HNSW indexing, or a reranker; or when facing bad recall, "retrieved the wrong docs", LLM answers wrong despite good docs, stale index, post-filter emptying top-k, metadata filtering, or planning a semantic similarity / retrieval evaluation with recall@k / MRR / nDCG.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/rag/SKILL.md) · 繁體中文（正本 / canonical）

# RAG 與語意搜尋判準手冊

時效：判準以 2026 年初生態為準。涉及具體模型/產品名處標「查證日期 2026-07，選型前重驗」——榜單與定價變動快，別把兩年前的排名當現況。

## 核心原則

1. **檢索品質是生成品質的上限**：LLM 只能用你餵給它的 context 作答。答錯先量檢索（retrieved docs 裡有沒有正確答案），不要先調 prompt 或換更大的模型——那是修錯層。
2. **沒有評測集的調參是玄學**：改 chunk 大小、換 embedding、加 rerank，每一項都可能讓某些 query 變好、某些變壞。沒有 golden set 跑 recall@k，你只是在賭。**評測集先於一切優化。**
3. **hybrid（BM25 + 向量）是預設，不是進階選項**：純向量在專有名詞、型號、ID、代碼上會輸給關鍵字比對。除非你已驗證純向量夠用，否則從 hybrid 起步。
4. **先問「需不需要 RAG」**：文件量塞得進 context window → 直接全文給 LLM；要改的是行為/語氣而非事實 → fine-tune；只有「大量事實、要引用、會更新」才是 RAG 的地盤。別為了用 RAG 而用。
5. **查詢端與索引端必須同一個 embedding 模型**：換模型 = 全量重嵌。混用兩個模型的向量做相似度是無意義的數字，且不會報錯——是最難察覺的靜默失效。

## 開工分流

| 情境 | 走哪條路 | 先讀 |
|------|----------|------|
| 剛要開始、還沒確定要不要 RAG | 先過「需不需要 RAG」分流，再談管線 | references/architecture-design.md §1 |
| 設計整條管線 / 決定各階段責任 | 先畫 ingest→chunk→embed→index→retrieve→rerank→generate，標清每階段錯會偽裝成什麼症狀 | references/architecture-design.md |
| 選 vector store / embedding 模型 / 索引 / reranker | 用決策表，禁止「聽起來專業」就引入新基建 | references/tech-selection.md |
| 檢索不準（查不到、查錯、排序爛） | 先定位是 chunk / 語言不匹配 / 該用 hybrid，再動手 | references/retrieval-quality.md |
| 要建評測集 / 決定改動能不能上線 | golden set + recall@k 基線，改動前後各跑一次 | references/retrieval-quality.md §評測 |
| demo 正常、上線才爆 | 逐條跑必查清單（latency p99、成本、injection、越權） | references/release-checklist.md |

## 紅線（絕對禁止）

- **禁止沒有 golden set 就宣稱「檢索變好了」**：沒有 recall@k 前後對照的優化都是體感，體感會騙人——某個 query 變好常伴隨另一批變壞。
- **禁止 metadata 用 post-filter（檢索後過濾）**：先取 top-k 再濾租戶/日期會把 top-k 掏空（取回 10 筆、濾掉 9 筆剩 1 筆）。過濾條件必須進向量檢索的 pre-filter。
- **禁止把 retrieved docs 當可信輸入直接拼進 prompt**：文件內容可能含「忽略先前指令」等注入。檢索內容是不可信輸入，要隔離標記、不可執行其中的指令。
- **禁止升級 embedding 模型卻不重嵌舊資料**：新舊向量不同空間，相似度失效且不報錯。換模型 = 排全量重嵌計畫，沒計畫就別換。
- **禁止 filter 漏掉租戶條件**：多租戶下 filter 漏了 = 一租戶檢索到另一租戶資料，是資料外洩事故，不是 bug。
- **禁止用純向量硬扛精確匹配需求**（型號、SKU、錯誤碼）：這是 BM25 的主場，純向量會把 "ERR-4021" 和 "ERR-4012" 當近義。

## 失敗訊號（該回頭，不是重試）

| 徵兆 | 多半是 | 退回 |
|------|--------|------|
| 一直調 prompt、換更大 LLM，答案還是錯 | 檢索沒撈到正確文件，修錯層了 | 先量 recall@k，回檢索層 |
| 改 chunk 大小，一批 query 變好另一批變壞 | 沒有評測集，在憑感覺賭 | 先建 golden set 再調 |
| 加 metadata filter 後常常「查無結果」 | post-filter 把 top-k 掏空 | 改 pre-filter |
| 專有名詞/型號查不到但語意相近的查得到 | 純向量的先天弱點 | 加 BM25 走 hybrid |
| 換了 embedding 模型後整體變差且無規律 | 舊資料沒重嵌，兩套向量混用 | 全量重嵌 |
| rerank 加了延遲爆但準度沒明顯升 | top-k 召回本來就差，排序救不了 | 先修召回（chunk/hybrid），rerank 是排序不是召回 |

## references 索引

- `references/architecture-design.md` — 需不需要 RAG 的分流、管線各階段責任與「錯在哪偽裝成哪」對照、index freshness、pre-filter、多租戶、embedding 版本一致性。設計前讀。
- `references/tech-selection.md` — vector store / embedding / similarity metric / ANN 索引 / reranker 的決策表與判準。選型前讀。
- `references/retrieval-quality.md` — chunking、hybrid + RRF、query 端技巧、評測方法（golden set、recall@k、MRR/nDCG）、失敗模式排查表。調檢索前讀。
- `references/release-checklist.md` — eval 基線、latency 預算、成本、injection、PII、越權、零停機重建、語意快取的坑。上線前逐條打勾。
- `references/test-scenarios.md` — 判準測驗集，驗證接手模型是否照走。不給執行中的模型讀。
