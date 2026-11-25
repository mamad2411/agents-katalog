---
name: grill-with-docs
description: 面試式需求對齊。挑戰你的計劃、精煉術語、更新 CONTEXT.md 和決策記錄(ADR)。需求模糊、要開新功能、或說「先討論清楚」時使用。
---

<what-to-do>

就這個計劃的每個面向，一直問我直到我們達成共識。沿著決策樹逐個分支推進，每次一個問題。每個問題都附上你的推薦答案。

一次一個問題，等我回答再繼續。

能透過程式碼探索回答的問題，直接探索而不要問我。

</what-to-do>

<supporting-info>

## 領域感知

探索程式碼時，同時讀取現有文檔：

### 檔案結構

```
/
├── CONTEXT.md           ← 本專案的領域詞彙表
├── .claude/
│   ├── agents/          ← CEO + 13 子角色提示詞
│   ├── llmwiki/         ← LLM Wiki (知識層 1)
│   ├── knowledge-vectordb/  ← RAG 向量庫 (層 2)
│   ├── knowledge-graph.json ← 知識圖譜 (層 3)
│   └── mcp.json         ← MCP 工具註冊
├── sync-rag.ts          ← RAG 同步工具
└── src/
    └── multi-role/
        └── knowledge-base/
            ├── engine.ts         ← RAG 引擎
            ├── auto-learner.ts   ← 自動學習器
            └── knowledge-graph.ts ← 圖譜引擎
```

## 對話期間

### 用詞彙表挑戰

當用戶使用的術語與 CONTEXT.md 中的定義衝突時，立刻指出。「CONTEXT.md 定義『LLM Wiki』是 X，你現在似乎是指 Y — 哪個？」

### 精煉模糊語言

當用戶使用模糊或過載的詞語時，提出標準術語。「你說『知識庫』— 是指 LLM Wiki、RAG 向量庫，還是知識圖譜？這三個是不同的東西。」

### 用具體場景壓力測試

討論系統關係時，用具體場景測試邊界。

### 與程式碼交叉驗證

用戶說某個東西如何運作時，檢查程式碼是否一致。發現矛盾立刻指出。

### 即時更新 CONTEXT.md

術語確定後立刻更新 CONTEXT.md，不要批次處理。

### 謹慎建立 ADR

只有同時滿足三個條件才建立 ADR：
1. 難以逆轉
2. 沒有上下文會令人困惑
3. 來自真正的取捨

</supporting-info>
