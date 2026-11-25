---
name: auto-edit-review
description: 分鏡表確認後的定稿與審查：build、audit、完成態拼圖、開完成影片預覽給使用者看；使用者看完給修改時開回饋輪 rN（先備份 plan.json、記原話與分類、改到的段存版本）；要一段重新設計時先出分鏡提案（work/versions/<段>/v<N>/）給使用者確認再做；退回某一版；使用者說「打開剪輯台」「調好了」時開關剪輯台。當分鏡表剛確認完，或使用者說「s05 的金句卡往左移」「這張卡…」「s12 的動畫想更完善」「s12 重新設計」「s12 用 v1」「打開剪輯台」「調好了」「照修改單改」時使用。還沒有確認分鏡表時不要用（改用 auto-edit-storyboard）；要輸出完成影片時不要用（改用 auto-edit-deliver）。
version: 0.2.0
---
# 定稿、審查、回饋輪、剪輯台

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| ③ 通過、內容設計動畫都做完 | 流程 A | 完成態拼圖、完成影片預覽網址 | build 0 個 ✖、audit 0 個 ✖、拼圖沒有 FAIL | ④ 完成影片預覽 |
| ④ 的修改；「照修改單改」（流程 F） | 流程 B | `work/feedback/r<N>.md`、改到的段的新版本 | `versions.mjs finish` 印停點 ④ | ④ 完成影片預覽 |
| ④ 之後一段要重新設計（D）、退回舊版（E） | 流程 D、E | D：`work/versions/<段>/v<N>/分鏡.md` → 做好的 v<N>；E：那段換回舊版 | D：使用者確認過分鏡；E：build 0 個 ✖ | D：③ 分鏡表（<段> v<N>）→ ④；E：④ |
| 「打開剪輯台」 | 流程 C | 剪輯台網址 | `editor.mjs --status` 印出網址 | ⑤ 剪輯台 |

審查門檻的唯一定義：`shared/template/REVIEW.md`（數字照 style.md「審查門檻」）。

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 停點紀錄 ③ 沒有「通過」 | 改用 `auto-edit-storyboard` |
| 內容設計動畫還是空白畫布（`--check` 印「內容設計動畫還沒做」） | 先照 `auto-edit-motion` 做完 |
| 剪輯台開著（`editor.mjs --status` 有網址） | 改 plan.json 或 rough.srt 前先重新讀要改的那一段（plan.json 用 `build.mjs --show <段>`），不要蓋掉剪輯台存的設定 |

## 步驟

**A. 定稿 → 停點 ④**

```
node shared/template/tools/build.mjs --project projects/<專案> --review
```

一條做完：build、量全部動畫、完成態拼圖、開完成影片預覽（只是把動畫疊在影片上，不 render）、記停點。內容沒變的段沿用上次的量測和截圖（印「沿用上次的量測和截圖：這次重做 N 段」）；kit、模板、底片、plan 共用的欄變了就全部重做，懷疑沒量到加 `--no-reuse`。**同一則回覆一次打開它印的所有拼圖頁**，只找 FAIL（REVIEW.md §2），不用每段寫 PASS。回覆附上六行、提醒「請看字幕有沒有對到嘴」。
完成判準：印 `audit：✖ 0`、停點 ④ 那一行；拼圖沒有 FAIL，或 FAIL 都修好重跑過。
常見錯誤：`✖ …` 在內容設計動畫段 → 把那幾行原文交回做那段的子代理；要看全片逐格（使用者要求才做）：`(cd projects/<專案>/work/hyperframes && npx hyperframes snapshot --review)`，15 段就 164 格，長片要好幾分鐘。

**B. 回饋輪**（停點 ④ 收到修改時。**流程 F**＝使用者說「照修改單改」、貼上「照剪輯台修改單改這 N 段（…）」或「# 剪輯台修改單」：一樣走 B，改法照 `work/feedback/editor-requests.md` 直接做、不出提案、不停 ③，要手改動畫的段一段一個子代理同時派出，開始與做完用 `editor.mjs --requests-state` 回報剪輯台；標籤解讀、派工、回報讀 `references/editor-requests.md`）

```
node shared/template/tools/versions.mjs begin --project projects/<專案> --seg <段,段> --say "使用者原話"
node shared/template/tools/versions.mjs finish --project projects/<專案>
```

三步：① `begin` 備份、存改前版本、開 `work/feedback/r<N>.md`，只印這幾段的 plan（不用讀整份）。② 改那幾段（文字、位置、時間改 plan.json；模板動畫改 `slots`；內容設計動畫檔裡的東西、`slots` 做不到的模板改動，一段派一個子代理照 `.agents/skills/auto-edit-motion/references/worker-brief.md` 改，內容設計動畫它會先載入 hyperframes skill，同一則回覆一次派出、全部回來才跑 ③；主代理不自己改動畫檔）。「s05」直接找 id；「1:10 那段」「這段」照 USAGE.md 2.6 換成段 id。③ `finish` build、量、存改後版本、寫驗證、記停點，印要看的那張圖，打開看一次。有 ✖ 它會停，改完再跑一次 `finish`。
完成判準：`finish` 印停點 ④ 那一行；要看的那張圖看過；流程 F 修改單每一段在 r<N>.md「改了哪幾段」都有一列 `- <段 id>：<做了什麼或沒做的理由>`，也用 `--requests-state` 回報了 `done` 或 `failed`。
常見錯誤：「規則」類的回饋（「以後金句都放左邊」）去改了 `shared/` → 只記在 r<N>.md 的「建議改規則」；使用者沒說怎麼改、只說要更好 → 改走流程 D；不知道怎麼歸類 → `references/feedback-round.md`。

**C. 剪輯台 → 停點 ⑤**（EDITOR.md「一、給 AI」；剪輯台會改哪些欄位看其中「3. 剪輯台會寫哪些欄位」）

```
node shared/template/tools/editor.mjs --project projects/<專案>
node shared/template/tools/editor.mjs --status --project projects/<專案>
```

第 1 行在背景啟動；第 2 行確認網址。使用者說「調好了」：直接跑流程 A（`--review` 會讀剪輯台存的最新檔，不用整份重讀 plan.json、rough.srt）；之後要改哪一段，再用 `build.mjs --show <段>` 讀那一段（剪輯台增刪字幕時會重對 plan.json 的句號，`work/storyboard.md` 的句號可能過期，以 plan.json 為準）。不要關剪輯台，停點 ④ 的網址就是它。
完成判準：`--status` 印出網址；「調好了」之後 `--review` 0 個 ✖。
常見錯誤：使用者在剪輯台改過的文字、斷句、時間被改回去 → 以剪輯台存的為準（AGENTS.md 規則 10）。

**D. 改版**（使用者指名一段要重新設計、更完善、換個動畫；步驟在 `references/revise.md`）

```
node shared/template/tools/versions.mjs begin --project projects/<專案> --seg <段> --say "使用者原話"
node shared/template/tools/versions.mjs new --project projects/<專案> --seg <段> --note "「使用者原話」"
```

提案寫在 `work/versions/<段>/v<N>/分鏡.md`，停點 ③ 確認才動手。**重新設計要回到內容，不是換一支模板**：設計師照 `.agents/skills/auto-edit-motion/references/design-build.md` 重想這段要傳達什麼。沒指名段（「動畫都更細節一點」）先列出動畫段、每段一句可以改的方向，問要改哪幾段。
完成判準：分鏡.md 沒有範本那一行「（寫 1–5 條」；回覆最後兩行是改版的停點 ③。
常見錯誤：直接改了 storyboard.md 或 x 檔 → 提案只寫在 v<N>/分鏡.md，使用者說「可以」後才 `accept`。

**E. 退回某一版**（「s12 用 v1」「退回上一版」）

```
node shared/template/tools/versions.mjs begin --project projects/<專案> --seg <段> --say "使用者原話"
node shared/template/tools/versions.mjs use --project projects/<專案> --seg <段> --ver v1
node shared/template/tools/versions.mjs finish --project projects/<專案>
```

三行都要跑：沒有 `begin` 的 `finish` 會 ✖，或把這次退回算進上一輪。不確定有哪幾版先跑 `versions.mjs list --project projects/<專案> --seg <段>`（「上一版」＝標「← 目前」的前一版）；use 會先把現在的樣子存起來再換回去。
完成判準：工具印「退回 v1」；`finish` 0 個 ✖。
常見錯誤：印 `⚠ 字幕在 v1 之後改過` → 看 `finish` 的「文字對時」，先跑 `node shared/template/tools/build.mjs --project projects/<專案> --autofix --only <段>` 讓工具照 → 改，剩下的 ✖ 再手改那段的 `#N@詞`。

## 停點

```
⏸ 停點 ③ 分鏡表（<段> v<N>）｜請看 work/versions/<段>/v<N>/分鏡.md
請回：「可以」或要改的拍

⏸ 停點 ④ 完成影片預覽｜請看 <完成影片預覽網址>
請回：要改的段落（例：s05 往左移）或「可以了，輸出完成影片」

⏸ 停點 ⑤ 剪輯台｜請看 <剪輯台網址>
請回：調完說「調好了」（會自動存）
```

| 停點 | 使用者回 | 做什麼 |
|---|---|---|
| ④、⑤ | 「s05 的金句卡往左移」這類修改／「照修改單改」 | 流程 B／流程 F |
| ④ | 「s12 的動畫想更完善」「s12 重新設計」／「s12 用 v1」 | 流程 D → 停點 ③（<段> v<N>）／流程 E → 停點 ④ |
| ③（<段> v<N>） | 「可以」／要改的拍 | `references/revise.md`／改那份分鏡.md → 重貼停點 ③ |
| ④ | 「可以了，輸出完成影片」／「打開剪輯台」 | 交 `auto-edit-deliver`／流程 C |
| ⑤ | 「調好了」 | 直接跑流程 A（不用整份重讀 plan.json、rough.srt；剪輯台不關） |

## 自我核對

- [ ] build、audit 0 個 ✖
- [ ] 拼圖一次看完，有 FAIL 的修好了
- [ ] 回饋輪用 `versions.mjs begin`／`finish`，沒有手動備份、複製版本
- [ ] 改版先停在停點 ③（<段> v<N>），使用者說「可以」才 accept、才動手
- [ ] 沒蓋掉剪輯台存的設定
- [ ] 「規則」類的修改只記在 r<N>.md，沒改 `shared/`

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| `⚠ 這些檔被手改過，沒有覆寫：… → 把改動搬進 plan.json 後加 --force` | 看改了什麼，搬進 plan.json，再加 `--force`（USAGE.md 2.6） | 停下來回報：指令、錯誤原文、已經試過什麼 |
| 預覽網址打不開、`✖ 剪輯沒有啟動成功` | `editor.mjs --status`，沒開就重開；還是不行讀它印的 log 最後幾行 | 停下來回報 log 原文 |
| 完成影片預覽按鈕是灰的 | 看按鈕提示：還沒 build 就跑 build；找不到播放器就在根目錄 `npm install`，再 `--stop` 後重開 | 停下來回報 |
| audit `✖ … 綁句失敗`、`未定位頂層`、`標題壓到內容` | 把那幾行原文交回做那段的子代理；模板動畫就是 slots 字太多，縮文案 | 停下來回報 |
| `✖ 文字對時：… 才講到 → beats.keyAt 寫 "#20@到電腦"` | 先跑 `node shared/template/tools/build.mjs --project projects/<專案> --autofix --only <這輪改的段>`（工具照 → 自動改，改不好會退回；一定要加 `--only`：別段是使用者在剪輯台改過的，不能動），剩下的照 → 一則一則改；⚠ 也照改（USAGE-reference.md R2.8） | 停下來回報那幾則原文 |
| `✖ work/rough.mp4 在 … 是全黑，但素材沒有純聲音檔 → 初剪壞了…` | 不要改 plan.json 繞過；照訊息跑 `verify-rough`，照它印的重做初剪 | 停下來回報 |
| `⚠ build 會停下來：瘦臉底片不是最新的（…）→ 先跑 … look.mjs run …` | 照它的 → 跑 `look.mjs`，再跑一次 | 停下來回報 |
| `✖ <段> 的 v<N> 分鏡還在等使用者確認 → …` | 使用者已經說「可以」就照 → 跑 accept；不改了就照 → 跑 use | 停下來回報 |
| 回饋某一項工具呼叫超過 6 次 | 停下來回報那一項卡在哪 | — |

## 工具呼叫預算

流程 A 最多 8 次（不含內容設計動畫）；回饋輪每一項最多 6 次；改版開提案到停點 ③ 每段 6 次、確認後到停點 ④ 12 次（不含動畫）。超過就停下來回報卡在哪。

## 回報格式

```
預覽好了：<N> 段；audit ✖ 0、⚠ <N>（⚠ 逐項：改了／保留的理由）
人聲響度 …、音效比例 …、剪接點微淡化 …、講者調光 …、講者瘦臉 …、結尾配樂 …（--review 印的六行）
拼圖：<FAIL 的段與問題；沒有寫「沒有 FAIL」>
請看字幕有沒有對到嘴；說「輸出」才 render。
<停點 ④ 那一行原文>
```

## 什麼時候讀 references/

- `references/feedback-round.md`：不確定修改該歸哪一類時才讀。
- `references/revise.md`：流程 D 改版時才讀。
- `references/editor-requests.md`：流程 F 照修改單改時才讀。
- `references/reviewer-brief.md`：使用者要求逐格抽查、要派子代理看全片截圖時才讀。
