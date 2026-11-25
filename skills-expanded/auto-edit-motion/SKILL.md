---
name: auto-edit-motion
description: 做情境動畫。內容設計動畫：使用者在停點 ③ 勾了的段，設計師子代理從內容出發寫鏡位腳本、接著從空白畫布做出來。模板動畫：填資料工具自動產出，只有使用者要求特殊改動時才手改。當分鏡表確認後有內容設計動畫要做、使用者說「做動畫」「s12 重新設計」、或派工訊息指定某一段時使用。還沒有確認過的分鏡時不要用（改用 auto-edit-storyboard）。
version: 0.2.0
---
# 情境動畫

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| 確認過的分鏡（`work/storyboard.md`） | 步驟 1–3 | `compositions/x-design-<段>.html` | `audit --only` 0 個 ✖、拼圖親眼看過 | 沒有（做完接停點 ④） |

**兩種動畫不要混**：模板動畫（plan.json 寫 `template`＋`slots`）工具直接產出，不用動手。內容設計動畫（`design: true`）才要設計師，而且不能參考模板。

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 主代理，分鏡確認了 | 步驟 1 派工 |
| 你是設計師子代理 | 照派工訊息：寫腳本讀 `references/design-script.md`；做動畫先載入 `hyperframes` skill，再讀 `references/design-build.md` |
| `design: true` 的段沒有 `work/designs/<段>.md`（分鏡表裡那段的動畫分鏡可能是勾選前的模板拍，不算） | 派工照 `--apply-storyboard` 印的那一行（先寫腳本、接著做動畫）；那行沒寫就交回主代理 |
| 使用者要改模板動畫的文字、站數 | 改 plan.json 的 `slots`，不用動 HTML |
| 使用者要模板動畫做不到的改動（修改單、指定動作） | 步驟 3 |

## 步驟

**1. 派設計師**（主代理）

```
ls projects/<專案>/work/briefs/
```

一段一個子代理，同一則回覆一次全部派出；段數多時一次最多 4 個，回來再派下一批。派工訊息**只送** `--apply-storyboard` 印的那一行（換掉 `<段>`），不要加要求、範圍、檢查指令或完成判準：設計師要的都在 brief 和文件裡，多加的會蓋過文件（派工訊息優先），把設計師帶去翻原始資料。沒有能派子代理的工具才自己一段一段做。要新畫的線稿元件由設計師在同一輪自己畫（一段最多一個），不用另外派工人；只有使用者另外要求畫元件時才照 `references/illus-worker.md` 派。
完成判準：每個 `design: true` 的段都派了。
常見錯誤：一段一段派 → 慢好幾倍，要同一則回覆一次派出。

**2. 收件**（主代理）

```
node shared/template/tools/build.mjs --project projects/<專案> --review
```

全部回來才跑。它會 build、量全部動畫、出完成態拼圖，停在停點 ④（`auto-edit-review` 流程 A）。有 ✖ 就把那幾行原文交回做那段的子代理。
還有段沒回來時，每收到一個完成通知就跑一次 `node shared/template/tools/build.mjs --project projects/<專案> --design-status`（不要寫 sleep 迴圈等檔案）。印「⚠ 超過 20 分鐘沒進度」的段，照它印的派工訊息停掉原本那個、重派一個新的；沒有 ⚠ 的段繼續等它回報，不要停它。主代理不自己寫 x-design 檔。
完成判準：`--review` 印出停點 ④ 那一行。
常見錯誤：每收一個就 build → 不用，全部回來才跑一次。

**3. 手改模板動畫**（只有使用者要求模板做不到的改動才做）

```
node shared/template/tools/audit.mjs --project projects/<專案> --only <段> --shots --sheet
```

直接改 `compositions/<模板>-<段>.html`（改過之後工具不會再覆寫，slots 也不再生效；要回到填資料就刪掉這個檔）。派工照 `references/worker-brief.md`。
完成判準：`audit --only` 0 個 ✖；拼圖親眼看過，對得上要求。
常見錯誤：改了 slots 畫面沒變 → 那個檔手改過，工具印 ⚠「手改過」；要重新產生就刪掉它。

## 自我核對

- [ ] 內容設計動畫是從內容想出來的，不是某支模板的變形
- [ ] 派工訊息是照抄工具印的那一行（綁句、版面、節奏由 audit 量，不寫進派工訊息）
- [ ] 拼圖親眼看過：動作看得到、構圖有主角、遮住字幕看得懂
- [ ] brief 前後段寫到的插圖元件，用同一個名稱、同一個朝向（brief 沒寫就不用核對）
- [ ] 沒有改 plan.json、storyboard.md、shared/（子代理）

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| `壓到子母畫面`、`進字幕區`、`超出畫面` | 照 → 移元件。有小視窗的段留在 x 120–1300、y 150–858；全螢幕段留在 x 120–1800、y 112–900（brief「畫布」那一節） | 把原文交回主代理 |
| `✖ … 動態「…」不在語彙表`、`✖ 分鏡表表頭不對` | 分鏡表的問題：改 `work/designs/<段>.md` 用語彙表的名稱，告訴主代理重產那段 | 把原文交回主代理 |
| 改動畫時 `✖ … P.at(…) 不在分鏡表`（拍改了） | 改 `work/designs/<段>.md` 那張表（沒有就從 storyboard.md 那一節抄過去再改），audit 照比較新的那份對；`versions.mjs finish` 會寫回 storyboard.md | 把原文交回主代理 |
| `綁句對不上` | 照它給的 `P.at` 改；→ 寫「重跑 build」「snapshot」的那半句不用做，改好動畫檔就重跑同一條 audit | 回報那幾則 |
| `P.spot 要照時間先後寫` | 拍照講解的時間排 | 回報 |
| 同一個 ✖ 改兩次還在，或 → 要改 plan.json、storyboard.md | 停手，回報 `<段> ✖<N>｜卡在：<那行 ✖ 原文>`，主代理改 plan.json 後重派 | — |
| 工具呼叫超過預算 | 停下來，把卡住的 ✖ 原文交回主代理 | — |

## 工具呼叫預算

每段鏡位腳本 6 次、做動畫 18 次。超過就停下來，把卡住的 ✖ 原文交回主代理。

## 回報格式

子代理只回一行。主代理：`內容設計動畫 <N> 段做好了；audit ✖ 0、⚠ <N>`，接停點 ④。

## 什麼時候讀 references/

- `references/design-script.md`、`references/design-build.md`：你就是設計師時才讀（主代理派工不用讀，工具會印派工訊息）。
- `references/illus-worker.md`：使用者另外要求畫線稿元件時才讀（內容設計動畫要的新元件由設計師自己畫）。
- `references/worker-brief.md`：要手改動畫（步驟 3）時才讀。
- `references/kit-syntax.md`：手改模板動畫（`x-<模板>-<段>.html`）時才讀；內容設計動畫用 GSAP，不用讀。
