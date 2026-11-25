---
name: auto-edit-deliver
description: 輸出完成影片並驗收：deliver.mjs 一條指令做完 build、4 秒測試片段確認有聲音、整支 render、qc.mjs final，使用者要求先在背景算（--prerender）過的，內容沒變就直接接手。使用者要在剪映（CapCut）自己剪時，另外用 capcut.mjs 輸出主軌＋每段透明 MOV＋字幕 SRT。當使用者看完完成影片預覽之後說「可以了，輸出完成影片」「輸出」「輸出剪映素材」「要用剪映剪」「輸出 mov」時使用。還有要改的地方、還沒看過完成影片預覽時不要用（改用 auto-edit-review）。
version: 0.2.0
---
# 輸出完成影片與驗收

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| 停點 ④ 通過 | 步驟 1 | `output/final.mp4`、`output/test-clips/test-clip.mp4`、`output/qc/qc-sheet.jpg` | `deliver.mjs` 印 ✔ 完成影片；驗收 0 個 ✖ | — |
| 「輸出剪映素材」 | 步驟 2 | `output/capcut/` | `capcut.mjs status --wait` 印「✔ 做完了」 | — |

**不用輪詢、不用看 log**：工具在背景跑，前景最多等 9 分鐘；結束碼 75 表示還在跑，再跑一次同一條會接著等，不會重跑。

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 停點紀錄 ④ 沒有「通過」，使用者也沒說要輸出 | 改用 `auto-edit-review` |
| 使用者只要剪映素材（不要 final.mp4） | 只做步驟 2 |
| 停點紀錄 ④ 最後一列是「通過」、原話是「在剪輯台按「輸出完成影片」」，而且 `output/final.mp4` 比 plan.json 新 | 使用者已在剪輯台輸出並驗收，不要重做 |

## 步驟

**1. 輸出完成影片**

```
node shared/template/tools/deliver.mjs --project projects/<專案> --said "使用者原話"
```

使用者說要 4K 加 `--resolution 4k`；說字幕不要燒進影片（要字幕檔、要上 CC）加 `--no-captions`，字幕另存 `output/final.srt`。沒說就不加（預設 1080p、燒進影片）。

一條做完：重新產生 → 4 秒測試片段確認有影音 → 整支（`--quality looks`，成功才換成 `output/final.mp4`，失敗不動舊檔）→ `qc.mjs final`。使用者要求先在背景算（`--prerender`）過的，內容沒變就直接接手，只跑驗收；平常停點 ④ 不 render，沒有這份。上一支（完成影片或背景先 render 的）只差幾段時，工具只重畫改到的時間窗、接回去（印「只重畫改到的 N 秒」，通常不到一分鐘）；不是局部改動印一行「整支重新輸出：原因」再整支（`--force` 也是整支），都不用另外下指令。打開 `output/qc/qc-sheet.jpg` 掃一眼。`qc.mjs final` 有 ⚠ 想看那一段：`node shared/template/tools/qc.mjs observe --project projects/<專案> --from <秒> --to <秒>`。
完成判準：印 `✔ 完成影片`；驗收 0 個 ✖（包括沒有「沒有講者小視窗」的 ✖）；每個 ⚠ 寫「刻意」或「要修」。標「要修」的不在這一步改：回報列出來，最後一行改寫 `→ 下一個停點：④ 完成影片預覽（說「改 <段>」開始）`；使用者說要改就走 `auto-edit-review` 流程 B，改完再輸出。
常見錯誤：✖ 長度不符 → plan.json 比 index.html 新，再跑一次；`✖ s21 是全畫面清單卻沒有講者小視窗：work/rough.mp4 在 …–… 是全黑（原始素材不是）→ 初剪壞了…` → 不要交、不要改 plan.json，照 → 跑 `verify-rough` 重做初剪。

**2. 剪映素材（使用者要求才做）**

```
node shared/template/tools/capcut.mjs --project projects/<專案> --background
node shared/template/tools/capcut.mjs status --project projects/<專案> --wait
```

第 1 行在背景跑（同時 3 支）；第 2 行等到做完或快逾時才印一行，不用每 30 秒查。只重做某幾段：`--only s05,s12`。產出都在 `output/capcut/`：`主軌.mp4`（講者＋人聲＋片尾配樂，沒有字卡和字幕）、每段一支 ProRes 4444 `.mov`（有透明通道，帶自己那段的音效）、`字幕.srt`、`清單.md`（每支放在剪映時間軸的哪一秒）。
完成判準：`status --wait` 印「✔ 做完了」；把 `清單.md` 的路徑和怎麼排的四步貼給使用者。
常見錯誤：`✖ build 沒過` → 照它印的 ✖ 改 plan.json；某一支 `✖ render 失敗` → 看 `output/capcut/render.log` 最後幾行，修好後同一個指令再跑一次（做過、沒變的會略過）；使用者問章節角標 → 不輸出，請他在剪映用文字貼。

## 自我核對

- [ ] 用 `deliver.mjs`，沒有自己拆開 render、輪詢 log
- [ ] `qc.mjs final` 0 個 ✖，⚠ 逐項說明
- [ ] 附上 `output/qc/qc-sheet.jpg`
- [ ] build 的六行（人聲響度、音效比例、剪接點微淡化、講者調光、講者瘦臉、結尾配樂）和停點 ④ 報過的不一樣才貼；有配樂就提醒使用者把出處那一句貼進說明欄
- [ ] 有配樂、有 ⚠ 的地方回報都寫了

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| `⏳ … 還在跑` | 再跑一次同一條指令（會接著等） | — |
| render 失敗、記憶體不足 | 看 `work/render.log` 最後幾行，再跑一次（記憶體 8GB 以下會自動單 worker，USAGE-reference.md R13） | 停下來回報：指令、log 最後 20 行、已經試過什麼 |
| 已經在輸出、被鎖住 | 使用者可能按了剪輯台的「輸出完成影片」，等它做完；要取消：`deliver.mjs --project projects/<專案> --cancel` | 停下來回報 |
| qc final 的 ✖（格式、長度） | 照 `→` 改；格式不對多半是 render 用錯參數 | 停下來回報 |
| 工具呼叫超過預算 | 停下來回報卡在哪 | — |

## 工具呼叫預算

最多 4 次；超過等待上限再跑同一條不算。超過就停下來回報卡在哪。

## 回報格式

```
完成影片輸出完成：output/final.mp4（<長度>s）
驗證：<deliver.mjs 印的格式一行>
qc final：<✔／⚠／✖ 原文，每項一行>
⚠ 說明：<每個 ⚠ 一行：刻意／要修＋理由>
人聲響度 …、剪接點微淡化 …、音效比例 …、講者調光 …、講者瘦臉 …、結尾配樂 …（build 原文；和停點 ④ 報過的一樣就省略這行，不確定就照貼）
output/qc/qc-sheet.jpg
→ 完成（有標「要修」的 ⚠ 時改寫：→ 下一個停點：④ 完成影片預覽（說「改 <段>」開始））
```
