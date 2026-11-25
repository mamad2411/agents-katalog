---
name: auto-edit-screen
description: 把專案的螢幕錄影與圖片配到講解：掃素材做 contact sheet、對字幕找每段該配哪支錄影的第幾秒、讀座標加運鏡／紅框／放大鏡，寫成分鏡表的 media 列。當使用者說「配螢幕錄影」「旁白配畫面」，或 auto-edit-storyboard 的素材決策表要你做時使用；也當 explore 子代理的派工說明（選用）。要改已經 build 好的 media 段位置時不要用（改用 auto-edit-review）。
version: 0.1.0
---
# 螢幕錄影與圖片配對

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| `assets/screen/`、`assets/images/`，或「只有聲音」區間 | `media.mjs scan`、`media.mjs frame --at --grid` | `work/media/notes/`、草稿裡的 media 段 | 每段講解對到同一個操作；「只有聲音」的區間全部蓋住 | 沒有（併進 ③） |

寫法照 `node shared/template/tools/build.mjs --project projects/<專案> --spec media`；細節要用才查 USAGE.md 第 5 節那一小節（寫法 5.3、座標 5.4、標註 5.5；邊錄邊講的錄影 5.7），不整節讀；節奏與標註規則：style.md「螢幕錄影與圖片」。

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 你是盤點素材的子代理 | 只做步驟 1，只寫自己那份筆記 |
| 你是寫分章草稿的子代理 | 照步驟 2–3 把 media 段寫進自己那份草稿（`work/drafts/<chNN>.json`），不寫別的檔 |
| 錄影已經接進主軌（`media.mjs scan` 的 index.md 有「已經接進主軌的邊錄邊講錄影」，plan.json 有 `sync01`…） | 那支不用配，sync 段的 `from`／`to`／`in` 不要改；要加紅框、運鏡就寫在 sync 段上（USAGE.md 5.7） |
| `work/media/notes/` 已經有這支的筆記、素材沒換 | 跳過步驟 1 |

## 步驟

**1. 盤點：看素材、寫筆記**（不用等使用者。`work/media/index.md` 已經有就不要跑下面這條：`media.mjs prep` 掃過了，重跑會把每支錄影重新分析一次。盤點子代理一律不跑）

```
node shared/template/tools/media.mjs scan --project projects/<專案>
```

每支錄影、每批圖片一個子代理，同一則回覆一次派出。錄影**只讀自己那支的 `work/media/<檔名>/events.md`**（哪一秒切頁、開視窗、哪一塊變了、哪裡在等、哪裡在捲）和 sheet；圖片看 `work/media/images/sheet-NN.jpg`。不用讀 `work/media/index.md`（那是總表）。寫 `work/media/notes/<檔名>.json`：

```json
{ "file": "assets/screen/操作A.mp4", "summary": "安裝工具的完整操作", "moments": [ { "from": 3.5, "to": 18, "what": "打開設定頁、建立金鑰", "keywords": ["設定", "金鑰"] } ] }
```

圖片一批一個檔，寫成陣列：`[{ "file": "assets/images/a.png", "what": "…", "keywords": ["…"] }]`。`keywords` 寫講解可能會說的詞，工具用它把素材配到講到那個詞的句子（`work/分鏡素材/chNN.md` 的「素材候選」）。
完成判準：每支錄影、每批圖片都有筆記。
常見錯誤：素材檔名有空白、括號 → 指令照 index.md 印的檔名加雙引號；筆記寫太細 → 一支錄影幾個段落就夠，細節之後看 events.md。

**2. 對字幕配起點**（寫草稿時）

```
node shared/template/tools/media.mjs frame --project projects/<專案> --src "assets/screen/<檔名>" --at 12.5,18,24 --grid
```

`work/分鏡素材/chNN.md` 的「素材候選」列這一份哪一句可能對得上哪支素材。每段講解找「錄影裡正在做同一個操作」的那一刻：**先照 `work/media/<檔名>/events.md` 抄**，事件的「建議 in」就是 `in`、`retime` 第一點的 `src`，「框」可以直接當 `box`，等待照表上的 `retime` 寫法壓短。表上沒有的才跑第 1 行，一次截好幾個時間點的座標格線圖讀座標。寫素材檔名、起點、理由，寫進草稿的 media 段。
完成判準：每一段都有素材檔名、起點（`in` 或 `retime`）、對到的句號（`#N`–`#Me`）、理由；`moves`、`marks`、`callouts`、`spot`、`lens` 都有素材原尺寸的 `[x, y, w, h]`，箭頭有 `[x, y]`（USAGE.md 5.4）。
畫面和講解的速度對不上時（寫法：`build.mjs --spec media`）：

| 畫面在做什麼 | 寫法 |
|---|---|
| 等待（進度條、轉圈、下載、AI 生成） | `retime` 跳過：`[{ "at": "#21", "src": 19 }, { "at": "#21+1", "src": 31 }]` |
| 要點之前、要看清楚的操作 | `retime` 放慢（×0.5–0.7），同時 `moves` 推近、`marks` 或 `arrows` 指出來 |
| 停在一個結果畫面講好幾句 | `retime` 裡 `src` 一樣的兩點（整段都停就寫 `hold`） |
| 整段同一個速度 | `in`、`out` |
| 露出金鑰、密碼、個資 | `redact` 打碼 |

常見錯誤：同一個操作為了變速拆成好幾段 → 併成一段寫 `retime`，運鏡和紅框才不會斷；講解和畫面對不上 → 重設 `in` 或 `src`；用了 1920×1080 的畫面座標 → `--check` 會 ✖「超出素材範圍」，用格線圖重讀；紅框畫在還沒出現的東西上 → 寫好框之後加 `--box "x,y,w,h"` 截那一刻看一次。

**3. 標註**

```
node shared/template/tools/build.mjs --project projects/<專案> --check-draft <chNN>
```

選哪一種照 USAGE.md 5.5 表下的「選哪一種標註」：講「這一塊」用紅框；講「這是什麼／按這個」用說明卡；只看一塊用聚光燈；目標太小用箭頭；字太小用放大鏡；一步一步的操作加 STEP 膠囊。直式專案：16:9 錄影一定加 `moves` 推近到操作區；手機直式錄影用 `"pip": false`＋`"fit": "cover"` 鋪滿；橫式專案的手機直式錄影寫 `side`。說明卡、聚光燈、箭頭出現的期間不能運鏡。數量、停留下限照 style.md「螢幕錄影與圖片」。
完成判準：和 media 相關的 ✖ 是 0，也沒有「沒有任何標註或運鏡」的 ⚠（真的沒有要指的東西，回報寫理由）。
常見錯誤：`marks：… 同時有 N 個紅框` → 位置相近、連續講同一塊的合成一個大框；`箭頭 0（拿掉 1）` → 照 ⚠ 改 `to` 或 `from`；還有沒蓋住的「只有聲音」區間 → 回步驟 2 補一段，或改用不透明的全幕。

## 自我核對

- [ ] 每段 media 都對到講解同一個操作
- [ ] 座標是素材原尺寸
- [ ] 只有聲音的區間全部蓋住
- [ ] 錄影段沒放下方資訊卡（style.md「螢幕錄影與圖片」）
- [ ] 段尾沒露出下一步、沒露出個資；停住的畫面都寫了 `hold`
- [ ] 當子代理時只寫自己那份筆記（盤點）或草稿（分章）

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| `src：找不到 assets/screen/… → 檔名要和專案的 assets/ 資料夾裡一模一樣（現有：…）` | 照括號裡的檔名改 | 停下來回報：指令、錯誤原文、已經試過什麼 |
| `素材 … 長 Ns；從第 Ns 起播 Ns 要用到第 Ns` | `in` 往前、`to` 提早或 `speed` 改小，或拆兩段 | 停下來回報 |
| `… 超出素材範圍 W×H` | 重跑步驟 2 的 `media.mjs frame --grid` 讀座標 | 停下來回報 |
| `只有聲音的區間 …–… 有 Ns 是黑畫面` | 把前一段的 `to` 延到下一段的 `from`（0 秒相接），或加一段 media；沒有對得上講解的錄影或圖片 → 不要硬配，交回主代理把這個區間當一段講解做情境判定（`auto-edit-storyboard` 步驟 5），做成不透明的全幕情境動畫（介面操作用 `x-ui-mock`），回報寫「<區間> 沒有對應素材，改做動畫」 | 停下來回報 |
| 說明卡、聚光燈、箭頭的 ✖ 寫「期間不能有運鏡」 | 推近的 `dur` 結束時間提早到標註 `at` 之前，或拉回全景改到標註退場之後 | 停下來回報 |
| 說明卡 ✖ 寫完整可讀不夠、或 `side` 放不下 | `until` 往後延；`side` 照訊息改，或不寫讓 build 自動挑 | 停下來回報 |

## 工具呼叫預算

每支錄影最多 6 次。超過就停下來回報卡在哪。

## 回報格式

當子代理時只回一行：盤點是 `<檔名> 筆記 <N> 段`；分章草稿照 `.agents/skills/auto-edit-storyboard/references/chapter-worker.md` 的「回報」。配對結果寫在草稿裡，不貼表。

主代理自己配時：

```
media <N> 段（<素材檔名>…）；只有聲音的區間：全部蓋住（或：還差 1:10.00–1:12.00）
驗證：--check-draft <chNN> → ✖ 0、⚠ <N>
```
