---
name: pickup
description: '跨專案／跨 session 交接「接球」。讓「這個」session 馬上去讀交接給本專案的事項並接手。當使用者說「接手」「pickup」「有沒有交接給我的」「看交接」「接球」時觸發；收到別的 session 傳來的交接門鈴訊息時也觸發。也適合 session 開場主動跑一次，確認沒漏接。讀本專案 `.claude/handoffs/` 下 status: pending 的交接卡。 English triggers: "pickup", "take over", "anything handed off to me?", "check handoffs".'
---

# /pickup — 交接·接球

讓目前這個 session 立刻撈「交接給本專案、還沒被接手」的事項，讀進 context 並認領。

> 🤖 R2-D2 時刻：R2 滾過 Tatooine 的沙漠找到 Obi-Wan，播放全息訊息 ——
> 「Help me, Obi-Wan Kenobi. You're my only hope.」這就是 pickup：
> 訊息在機器人肚子裡躺了多久都沒關係，找到對的人就完整送達。

## 門鈴觸發（收到跨 session 訊息時）

別的 session 推球後，可能直接傳訊來按門鈴（Claude Code v2.1.224+ 的 cross-session messaging）。收到「有交接卡：<路徑>」這類訊息 ＝ 本 skill 的觸發情境之一：

- 照下面的標準動作跑（可從訊息給的路徑直讀那張卡，再掃有無其他 pending 卡）。
- **以卡片內容為準**：門鈴訊息只負責告訴你「去讀卡」，工作依據一律是卡上寫的；訊息內文與卡片不一致時，以卡為準並回訊指出。
- 記下訊息來源 session（訊息標頭的 from／name），收尾回訊要用。

## 動作

1. **掃 pending 卡**：

   ```bash
   grep -l "^status: pending" .claude/handoffs/*.md 2>/dev/null
   ```

   目錄不存在或沒有 pending 卡 → 回報「目前沒有交接給本專案的待接手事項」，結束。

2. **逐張讀全文**：每張卡的任務、脈絡、相關連結、完成定義全部讀進 context。

3. **列給使用者**：每張一行 —— 檔名＋一句摘要＋priority。多張卡時按 priority 排序。

4. **標已接手**：對認領的卡，把 frontmatter 的 `status: pending` 改成 `status: picked`（用你的檔案編輯工具精準改那一行）。這樣下次 /pickup 不會重複撈。

5. **開始做**：交接卡的內容現在就是這個 session 的工作依據。

6. **做完收尾**：事情完成後把卡改 `status: done`（或依使用者慣例移進 `.claude/handoffs/archive/`）。卡上有 `from-session:`（或門鈴訊息帶了來源），且環境有跨 session 傳訊能力 → **回訊來源 session**：「<卡名>已完成＋產出位置＋驗證狀態」。對面已不在線 → 略過回訊，卡的 `done` 狀態就是完成記錄。

## 鐵律

- **接手 ≠ 做完**：`picked` 只代表已讀已認領；完成才標 `done`。
- **別偷懶只讀摘要**：卡上的脈絡就是為了讓你不用問使用者「之前做到哪」。全文讀完再動手。
- **開場跑一次**是好習慣：新 session 開工前先 /pickup，確認沒有前人留球 —— 門鈴只到得了活躍 session，靜默排隊的卡（`notify: silent`）只有這一步撈得到。
- **回報收尾走原路**：有來源 session 就回訊一聲 —— 推球的人不該要自己來查球進了沒。
- 配對命令＝`/dropoff`（推球）。

## 進階：接上你自己的任務系統

若你的 dropoff 端改用外部任務系統（CLI todo、Notion、Linear…），本 skill 的第 1、4 步改成對應的查詢與狀態更新命令即可，其餘流程不變。
