---
name: ljg-paper-flow
description: "Paper workflow: read papers + cast cards in one go. Takes one or more arxiv links, paper URLs, PDFs, or paper names. For each paper, runs ljg-paper (generates org analysis) then ljg-card -c (generates comic-style card PNG). Use when user says '論文流', 'paper flow', '讀論文並做卡片', '論文卡片', or provides multiple papers wanting both analysis and cards."
user_invocable: true
version: "1.0.1"
---

# ljg-paper-flow: 論文流

一條命令完成：讀論文 → 生成解讀 → 鑄成卡片。支援多篇並行。

## 模式

**強制 NATIVE 模式。** 本 workflow 是純 skill 管道（ljg-paper → ljg-card），不需要 Algorithm 的七步流程。直接按下方執行步驟呼叫 skill，不走 OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY/LEARN。

## 引數

| 引數 | 說明 |
|------|------|
| 無引數 | 對話中已提供的論文連結/檔案 |
| `-l` | 卡片模具改用長圖模式（預設 `-c` 漫畫） |
| `-i` | 卡片模具改用資訊圖模式 |

## 執行

### 1. 收集論文列表

從使用者訊息中提取所有論文來源（arxiv URL、PDF 路徑、論文名稱等）。

### 2. 並行處理每篇論文

對每篇論文，啟動一個 Agent subagent，每個 subagent 按順序執行兩步：

**步驟 A — 讀論文（ljg-paper）：**

呼叫 Skill tool 執行 `ljg-paper`，傳入該論文的來源。等待完成，獲得生成的 org 檔案路徑。

**步驟 B — 鑄卡片（ljg-card）：**

讀取步驟 A 生成的 org 檔案，呼叫 Skill tool 執行 `ljg-card`（預設 `-c`，或按使用者指定的模具引數），以 org 檔案內容為輸入。等待完成，獲得 PNG 檔案路徑。

### 3. 彙總報告

所有論文處理完成後，彙總輸出：

```
════ 論文流完成 ═══════════════════════
📄 {論文標題1}
   📝 解讀: {org 檔案路徑}
   🖼️ 卡片: {PNG 檔案路徑}

📄 {論文標題2}
   📝 解讀: {org 檔案路徑}
   🖼️ 卡片: {PNG 檔案路徑}
...
```

## 關鍵約束

- 每篇論文的兩步必須序列（先 paper 後 card），但多篇論文之間並行
- ljg-paper 和 ljg-card 各自的質量標準、紅線、品味準則不變
- 卡片內容來自生成的 org 檔案，不是原始論文
