---
name: daily-debrief
description: '產生某一天的工作日報:做了什麼+reflection,存成本地 Markdown。以 mission-log 的零 token 骨架為原料,不重讀原始 transcript。當使用者說「日報」「今天的 daily summary」「幫我補某天的日報」「daily debrief」時觸發。⚠️ 需一併安裝 mission-log(收割器在那支裡);超過 transcript 保留期(預設 30 天)的日期無法補生成。 English triggers: "daily debrief", "daily summary", "write up my day", "backfill the daily for <date>".'
---

# /daily-debrief — 日報

把一天的所有 session 收斂成一頁:**做了什麼+reflection**,落地成 `~/.claude/journal/daily/YYYY-MM-DD.md`。transcript 30 天就蒸發,日報是把價值撈上岸的動作。

> 🤖 R2-D2 時刻:任務結束後的 debrief —— 中隊不是靠飛行員的記憶開檢討會,
> 是靠 astromech 的記錄。

## 用法

`/daily-debrief [日期]` —— 不帶參數＝今天(到目前為止);`yesterday`＝昨天;`YYYY-MM-DD`＝補生成指定日。**冪等**:重跑同一天就覆蓋更新。

## 動作

1. **歸檔舊檔(順手做)**:`journal/daily/` 裡超過 30 天的 md → 移到 `journal/archive/YYYY-MM/`。日報/週報永不讀 archive,舊檔不再消耗 context。
2. **取骨架**:優先讀已存的 `journal/raw/<日期>.*.jsonl`(有排程收集的環境);沒有就現場跑 mission-log 的 `scripts/harvest.py --date <日期> --format jsonl`(零 token)。找不到收割器＝mission-log 未安裝,請使用者補裝後重來。
3. **補充資料源(環境有就用,沒有就略過該節,不硬造)**:
   - **行事曆**:當日事件(會議/行程/面談)→「今天的重點」節。用你環境既有的行事曆工具。
   - **任務系統**:當日**完成**與**新增**的事項 →「Todo 異動」節。用你環境既有的任務工具/CLI;新增很多時依專案聚合,別流水帳。
4. **寫日報**,依骨架+補充資料源、模板如下:

   ```markdown
   # YYYY-MM-DD 日報
   ## 今天的重點(行程/會議/面談)
   - <HH:MM> <事件>:<一句話;可與 session 骨架互相印證>
   ## 做了什麼
   - <專案>:<一句話,依骨架的時間段/原話/工具推斷>
   ## Todo 異動
   - 完成(<N>): #id <標題>…
   - 新增(<N>): #id <標題>(球:誰)…(多時依專案聚合)
   ## 數字
   <N> 個 session｜<turns> turns｜<tokens> tokens｜主要模型（用全形｜,半形 | 會被當表格語法）
   ## Reflection
   - 順的:
   - 卡的:
   - 明天第一件事:
   ```

5. **落地並驗證**:寫入 `journal/daily/YYYY-MM-DD.md` 後回讀確認(`wc -l`/`grep` 命中),別信寫入成功的字面。
6. **同場寫通知摘要** `journal/daily/YYYY-MM-DD.digest.txt` —— **純文字、零 markdown 語法**(通知管道多為純文字模式,`#`/`**` 會裸露),≤18 行:

   ```text
   ▸ <N> sessions(<機器分布>)｜<tokens>
   ▸ 重點行程: <當日會議/面談,一行;無則省略>
   ▸ Todo: 完成 <N>｜新增 <N>(要點 1-2 個)
   ▸ 主線: <最多 3 條,一句話>
   ▸ 明天第一件事: <一句>

   — sessions —
   [<機器>] <HH:MM-HH:MM> <專案>: <一句話>
   ```

7. **產出後動作(選配)**:若存在 `~/.claude/journal/config.env`,依其設定執行(見進階節);沒有就跳過。通知管道建議發「標題+完整報告連結 → digest」的順序:**連結放最上面**,要看全文的人直接點走,不用滑過細節。
8. **對話內回報**:完成訊息裡把完整報告的網址**以裸連結原樣貼出**(有上傳就貼上傳後的 URL,沒有就貼本地檔路徑)——別用 markdown 文字連結(網址被藏在文字後),也別包進 code block(顯示得出來但點不了);就是普通文字行裡放裸網址。

## 鐵律

- ✅ **只寫骨架撐得起的話**:原話與工具紀錄是證據,推斷要標推斷;骨架沒有的活動不寫。
- 🚫 **不重讀原始 transcript**(那是 token 大戶);要深挖某 session 是 /mission-log 的互動場景。
- 🔁 **冪等**:任何一天可重生、可補跑,產出即最新真相。
- ⚠️ 該日無記錄或超出保留期 → 日報檔照寫,內容明講「無記錄(原因)」,不留空洞。

## 進階:排程自動化/跨機/產出後通知

- **自動收集(零 token)**:排程器(macOS launchd/cron)每天 00:30 跑 `harvest.py --date yesterday --format jsonl > journal/raw/<日期>.$(hostname -s).jsonl` —— 骨架落檔後**不受 30 天限制**,回溯無上限。
- **跨機**:各機各自收集(檔名帶主機名不互撞);日報時把多台的 raw 併著讀(同步方式自選:ssh 拉/共用資料夾/git)。
- **產出後通知**:`config.env` 可定義 `JOURNAL_POST_CMD`(收到日報檔路徑當參數),接你自己的 Notion 上傳/Telegram/Slack —— 本 skill 只負責呼叫,不綁任何服務。
