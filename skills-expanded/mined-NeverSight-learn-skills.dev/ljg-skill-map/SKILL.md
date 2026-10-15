---
name: ljg-skill-map
description: "Skill map viewer. Scans all installed skills and renders a visual overview — name, version, description, category at a glance. Use when user says 'skills', '技能', '技能地圖', 'skill map', '我有哪些技能', '看看技能', '列出技能', 'list skills'. Also trigger when user asks what skills are available or installed."
user_invocable: true
version: "1.0.0"
---

# ljg-skill-map: 技能地圖

掃描 `~/.claude/skills/` 下所有已安裝技能，生成一目瞭然的視覺化地圖。

## 執行

### 1. 掃描

執行 `scripts/scan.sh`，獲取所有技能的 JSON 資料（name, version, invocable, desc）。

### 2. 分類

根據技能名稱和描述，將技能自動歸入以下類別：

| 類別 | 圖示 | 含義 | 典型成員 |
|------|------|------|----------|
| 認知原子 | ◆ | 內容處理的原子操作 | ljg-plain, ljg-word, ljg-writes, ljg-paper |
| 輸出鑄造 | ▲ | 將內容轉化為可交付物 | ljg-card |
| 聯網觸達 | ● | 與外部世界互動 | agent-reach |
| 系統運維 | ■ | Agent 自身的維護和管理 | datetime-check, memory-review, save-conversation, skill-creator, ljg-skill-map |
| 環境部署 | ★ | 一次性安裝和配置 | Her-init |

歸類依據名稱字首和描述關鍵詞判斷。遇到新技能無法歸類時，放入「未分類」。

### 3. 渲染

用 ASCII 方框圖呈現，格式如下：

```
╔══════════════════════════════════════════════════════════╗
║              SKILL MAP  ·  {N} skills installed         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  ◆ 認知原子                                              ║
║  +-----------------+----------------------------------+  ║
║  | ljg-plain v4.0  | 白 — 好問題+類比讓人 grok        |  ║
║  | ljg-word  v1.0  | 英文單詞深度拆解                  |  ║
║  | ljg-writes v4.0 | 寫作引擎                          |  ║
║  | ljg-paper v2.0  | 論文閱讀與分析                    |  ║
║  +-----------------+----------------------------------+  ║
║                                                          ║
║  ▲ 輸出鑄造                                              ║
║  +-----------------+----------------------------------+  ║
║  | ljg-card  v1.5  | 鑄 — 內容轉 PNG 視覺化           |  ║
║  +-----------------+----------------------------------+  ║
║                                                          ║
║  ...                                                     ║
╚══════════════════════════════════════════════════════════╝
```

規則：
- 每個類別一個區塊，類別圖示 + 中文名做標題
- 技能名左對齊，版本號緊跟（無版本顯示 `-`）
- 描述截斷到一行，保留核心語義
- user_invocable 為 true 的技能名後加 `/` 標記（表示可直接 `/技能名` 呼叫）
- 底部統計行：總數、可呼叫數、分類數

### 4. 輸出

直接在對話中渲染 ASCII 地圖。不生成檔案，不寫入磁碟。
