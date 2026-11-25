---
name: dropoff
description: '跨專案／跨 session 交接「推球」。把一件事連同完整脈絡交給另一個專案（或同專案的未來 session）的 Claude。當使用者說「交接給 X」「handoff 給某專案」「推球給 X」「把這件事丟給下個 session」時觸發。產出＝目標專案 `.claude/handoffs/` 下的一張交接卡（Markdown 檔），對面 session 用 /pickup 接手；偵測到目標的活躍 session 時加發即時門鈴（使用者說「不用即時通知」則靜默排隊）。 English triggers: "hand this off to X", "drop this off for <project>", "pass this to the next session".'
---

# /dropoff — 交接·推球

把一件事**可靠地**交給另一個 Claude session（別的專案、或同專案的下一個 session）。

核心問題：對面 session 讀不到你這個對話的 context。口頭交代會漏、聊天記錄會斷 —— 所以交接卡必須是**磁碟上的檔案**，寫清楚到「陌生 session 光看這張卡就能接手」。

> 🤖 R2-D2 時刻：Leia 把 Death Star 圖紙和求救訊息存進 R2 的記憶體 —— 這就是 dropoff。
> 訊息不靠 Leia 本人送達，靠的是那台會自己滾去找 Obi-Wan 的機器人。

## 交接卡格式

一張卡 = 一個 Markdown 檔，放在**目標專案**的 `.claude/handoffs/` 目錄：

```
<目標專案根目錄>/.claude/handoffs/YYYYMMDD-HHMM-<短slug>.md
```

```markdown
---
status: pending          # pending → picked → done
from: <來源專案或 session 描述>
from-session: <來源 session 名稱或 ID，選填 — 有跨 session 傳訊能力時填，供對面完成後回訊>
to: <目標專案>
created: YYYY-MM-DD HH:MM
priority: high | normal | low
notify: rung | silent    # 選填 — 已按門鈴／使用者要求靜默排隊
---

# <事項一句話>

## 要做什麼
<具體、可執行的任務描述>

## 脈絡（陌生 session 也看得懂的程度）
<為什麼要做、之前做到哪、決策背景>

## 相關檔案／連結
- <路徑或 URL，一行一個>

## 完成的定義
<怎樣算做完 —— 可驗證的條件，不是感覺>
```

## 用法

`/dropoff <目標專案路徑或名稱> <事項>`

- 沒給目標 → 問使用者。
- 目標是「同專案的未來 session」→ 寫進本專案自己的 `.claude/handoffs/`。

## 動作

1. **建目錄**（若不存在）：`mkdir -p <目標專案>/.claude/handoffs`
2. **寫卡**：依上述格式。「脈絡」與「完成的定義」是卡的靈魂 —— 只寫標題的交接卡等於沒交接。
3. **驗證落地**：寫完 `cat` 回讀確認內容完整（寫入可能靜默失敗，別信工具回的成功訊息字面）。
4. **即時門鈴**（選用 — 環境有跨 session 傳訊能力才跑；Claude Code v2.1.224+ 的 cross-session messaging，其他工具自動跳過）：
   - ① 使用者說過「不用即時通知」「先不通知」「排著就好」之類 → **跳過本步**，卡上補 `notify: silent`。門鈴會讓閒置的對面立刻開工——大任務要挑時間處理的，開工時機留給使用者。
   - ② 否則列出可達的 session（`ListAgents`／`/list-agents`；桌面版用 session 管理工具的 list）。先查本專案 `.claude/handoffs/routing.md` 有沒有記過這個目標的對應——有、且那個 session 仍在且仍新鮮 → 直接用。否則依「最近活躍」（建議 7 天內）篩出目標專案的候選，分三種情況：
     - **恰好一個** → 自動發訊。
     - **超過一個** → 列出來問使用者挑，**並把選擇記進 `routing.md`**（一行：目標專案 → session 名稱），下次同目標免問。
     - **一個都沒有**（全過期）→ **也要問**：「1＝按給最近的那個過期 session（附名稱與閒置天數）2＝不按，只留卡片等 /pickup」。別自作主張喚醒沉睡 session——它會重載大量舊 context，且舊脈絡可能立刻開始行動。
   - ③ 找到 → 傳訊：「有交接卡：<卡片路徑>。手上沒事請跑 /pickup 接手；完成後請回訊本 session。」並在卡上補 `from-session:` 與 `notify: rung`。⚠️ 送達 ≠ 必動工：對面忙碌時會先做完手上的事；對面以 bypass-permissions 模式跑時，訊息會被押著等人工核准。
   - ④ 連過期候選都沒有（該專案完全無 session）→ 明講「卡已落地，無 session 可即時通知」，照舊等對面 /pickup。
5. **回報**：卡片路徑＋一句摘要＋門鈴結果（發給誰／靜默／無人可通知）＋提醒「對面 session 跑 `/pickup` 即可接手」。

## 鐵律

- **一卡一事**。兩件事就寫兩張卡，別打包。
- **脈絡自包含**：假設讀卡的 session 對你的對話一無所知。需要的背景、連結、路徑全放卡上。
- **門鈴只是通知，卡片檔案才是真相**：門鈴發失敗、環境沒有跨 session 傳訊、對面不在線 —— 交接照樣成立，一切以卡為準。門鈴訊息裡也別塞卡上沒有的任務內容。
- **「不用即時通知」是使用者的節流閥**：說了就靜默排隊，別自作主張補發。
- **按錯門鈴立刻補救**：發現目標錯了 → 馬上補發更正訊息請對方停手並還原卡片狀態；更正時**別覆蓋卡上原文**。
- **時效性高的事**，除了寫卡＋門鈴，再用你手上現有的即時通道（通知、訊息）提醒使用者一聲 —— 門鈴只到得了活躍的 session，到不了人。
- 配對命令＝`/pickup`（對面接手）。

## 進階：接上你自己的任務系統

如果你有跨專案的任務管理系統（CLI todo、Notion、Linear、GitHub Issues…），可以把「寫卡」替換成「在你的系統建一筆 type=dropoff 的任務」，`/pickup` 端同步替換查詢方式。檔案版是零依賴的最小公倍數，不是天花板。
