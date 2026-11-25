---
name: weekly-debrief
description: '產生某一週的工作週報:彙整 7 份日報成趨勢與 reflection,存成本地 Markdown。只讀日報 md,不碰原始 transcript。當使用者說「週報」「這週做了什麼」「weekly summary」「補上週的週報」時觸發。⚠️ 這裡的週報=個人工作回顧;要對外發布的內容型「週報」(電子報/社群貼文)不歸本 skill。需一併安裝 daily-debrief 與 mission-log(缺的日報會先自動補生成)。 English triggers: "weekly debrief", "weekly summary", "wrap up my week", "backfill last week".'
---

# /weekly-debrief — 週報

把一週的日報收斂成一頁:**主線、趨勢、reflection**。只讀 `journal/daily/` 的 7 份 md —— 便宜、快,且不受 transcript 保留期影響。

> 🤖 R2-D2 時刻:一次任務是一筆記錄,一場戰役是七筆記錄的樣子 ——
> 看得出補給線問題的,從來是後者。

## 用法

`/weekly-debrief [週]` —— 不帶參數＝本週(到目前);`last`＝上週;`YYYY-Www`＝指定週;給任一 `YYYY-MM-DD` ＝該日所在的週。週一起算。

## 動作

1. **盤點該週 7 天的日報檔**(`journal/daily/`):
   - 缺的日子、且仍在 transcript 保留期內 → **先照 /daily-debrief 的流程補生成**(自癒);
   - 真的無料可補 → 週報裡標「X/X 無記錄(超出保留期)」,不裝沒事。
2. **寫週報**,只依 7 份日報、模板如下:

   ```markdown
   # YYYY-Www 週報(MM-DD ~ MM-DD)
   ## 本週主線
   - <跨多日的工作線,含起訖與結果>
   ## 數字與趨勢
   總 sessions/tokens|最花 token 的專案|與上週比(若上週檔在)
   ## Reflection
   - 這週最值得留的一課:
   - 重複出現的卡點:
   - 下週優先:
   ```

3. **落地並驗證**:寫入 `journal/weekly/YYYY-Www.md` 後回讀確認。
4. **同場寫通知摘要** `journal/weekly/YYYY-Www.digest.txt`(純文字零 markdown,格式同 daily-debrief 第 5 步,sessions 列表換成「每日一行」)。
5. **產出後動作(選配)**:同 daily-debrief,存在 `config.env` 就執行 `JOURNAL_POST_CMD`,連結放訊息最上面。
6. **對話內回報**:同 daily-debrief 第 7 步,完整報告網址以裸連結貼出。

## 鐵律

- ✅ **只讀日報 md**:原始 transcript 與 raw 骨架都不碰;日報寫錯就先修日報再重跑週報。
- 🔁 **冪等**:任一週可重生;缺口自癒優先於報錯。
- 🚫 **趨勢要有兩點才叫趨勢**:上週檔不存在就不寫「比上週」,不假造基準。
