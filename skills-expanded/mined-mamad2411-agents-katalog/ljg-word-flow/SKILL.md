---
name: ljg-word-flow
description: "Word flow: deep-dive word analysis + infograph card in one go. Takes one or more English words, runs ljg-word (generates deep semantics analysis) then ljg-card -i (generates infograph PNG). Use when user says '詞卡', 'word card', 'word flow', or provides English words wanting both analysis and visual card."
user_invocable: true
version: "1.0.1"
---

# ljg-word-flow: 詞卡

一條命令完成：解詞 → 鑄資訊圖。支援多詞並行。

## 模式

**強制 NATIVE 模式。** 本 workflow 是純 skill 管道（ljg-word → ljg-card -i），不需要 Algorithm 的七步流程。直接按下方執行步驟呼叫 skill，不走 OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY/LEARN。

## 引數

直接傳入一個或多個英文單詞，空格分隔。

```
/ljg-word-flow Obstacle
/ljg-word-flow Serendipity Resilience Entropy
```

## 執行

### 1. 收集單詞列表

從使用者訊息中提取所有英文單詞。

### 2. 處理每個單詞

對每個單詞，序列執行兩步：

**步驟 A — 解詞（ljg-word）：**

呼叫 Skill tool 執行 `ljg-word`，傳入單詞。在對話中輸出 Markdown 解析結果。

**步驟 B — 鑄資訊圖（ljg-card -i）：**

以步驟 A 的解析內容為輸入，呼叫 Skill tool 執行 `ljg-card -i`。生成 PNG 檔案到 `~/Downloads/`。

### 3. 多詞並行

多個單詞時，每個單詞啟動一個 Agent subagent 並行處理（每個 subagent 內部 A→B 序列）。

### 4. 彙總報告

```
════ 詞卡完成 ═══════════════════════
📖 {Word1}
   🖼️ ~/Downloads/{Word1}.png

📖 {Word2}
   🖼️ ~/Downloads/{Word2}.png
...
```

## 關鍵約束

- 先解詞後鑄卡，順序不可逆
- ljg-word 和 ljg-card -i 各自的質量標準不變
- 資訊圖內容來自解詞結果，不是字典釋義
