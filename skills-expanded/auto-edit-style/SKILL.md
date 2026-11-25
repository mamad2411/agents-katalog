---
name: auto-edit-style
description: 換工作區的主色、背景圖、講者調光瘦臉的預設，或換這一集的主題（亮／暗）、風格包：brand.mjs 換主色；背景圖有使用者的圖就縮放裁切，沒有就先跑 caps.mjs 探測生圖能力再照路由表生成（Codex／mmx／HTML 截圖），三張圖驗尺寸、出預覽，使用者同意才放進 shared/template/。風格包（shared/template/styles/<名稱>/）用 brand.mjs list／use／pack 試用、套用、存包。當使用者說「換風格」「換成我的風格」「換主色」「換背景」「生成背景圖」「以後都要調光」「預設不要調光」「換暗色」「換主題」「有哪些風格」「這集用 XX 風格」「做一個風格包」「講者設定成…」「不要講者介紹」時使用。只想移動某張卡的位置、改某一集的版面時不要用（改用 auto-edit-review）。
version: 0.1.0
---
# 換風格

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| 色碼、色名或使用者的圖 | `brand.mjs`、`caps.mjs`、生圖、`brand.mjs bg`、ffmpeg | `kit/brand.css`、`kit/pip-frame.png`、`bg-fs.jpg`、`bg-side.jpg`、`bg-ch.jpg`（＋`kit/look.json`） | 三張背景 ffprobe 尺寸對、使用者在停點 ⑥ 同意 | ⑥ 背景預覽 |
| 「換暗色」「換主題」 | 步驟 6 | 這一集 plan.json 第一層的 `theme` | `--check`、build 0 個 ✖ | — |
| 「有哪些風格」「這集用 XX 風格」「整個換成 XX」 | 步驟 7 | 這一集 plan.json 第一層的 `style`，或 `brand.mjs use` 換掉 `shared/template/` 那幾個檔 | `brand.mjs list` 的 ● 是對的那包、build 0 個 ✖ | — |

路由規則的唯一定義：USAGE-reference.md R9.3；背景圖規格與留空區：R9.2。只能改 AGENTS.md 規則 1 例外清單裡的檔。

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 只換主色 | 只做步驟 1 |
| 使用者有上傳圖片 | 步驟 2 直接走「使用者的圖」那條路，不用探測 |
| 使用者說「以後都要調光」「預設瘦一點」「預設不要調光」 | 只做步驟 5 |
| 使用者說「換暗色」「換主題」「改回亮色」 | 只做步驟 6 |
| 使用者說「有哪些風格」「這集用 XX 風格」「換回預設」 | 只做步驟 7 |
| 使用者說「做一個風格包」「換成我的風格」 | 步驟 1–4，第 4 步存成新的一包 |
| 會做到步驟 4（換背景、做風格包） | 開工先跑 `node shared/template/tools/brand.mjs list`，記下 ● 在哪一包；沒有 ● 就先跑 `node shared/template/tools/brand.mjs pack 原本-<YYYYMMDD>` 把目前的存起來，再做步驟 1，步驟 4 的 `use` 才不會卡住 |

## 步驟

**1. 主色**

```
node shared/template/tools/brand.mjs "#RRGGBB"
```

色名先轉成色碼，回報用了哪個色碼。brand.mjs 多印一行暗色主題跟著換的顏色（`kit/scene.css` 自動推，不用改）；直式的講者框 `kit/pip-frame-v.png` 一起重畫。
完成判準：brand.mjs 印的對比值與警告原文已貼給使用者。
常見錯誤：紅色系警告 → 明講「觀眾會分不出哪個是警告」（R9.1），由使用者決定；印 `⚠ 暗色主題標題列的白字對比只有…` → 把這行原文貼給使用者，建議換深一點的主色，或這支影片用亮色主題。

**2. 背景：選路**

```
node shared/template/tools/caps.mjs
```

把能力表貼給使用者。選路：在 R9.3 路由表找你這個模型那一列（MiniMax Code 是 MiniMax 系列、Claude Code 是 Claude 系列），從第一選擇往右找，第一個出現在 caps.mjs「可用的生圖路線」那一行裡的就用它（那一行的順序不是優先序）；寫一句選了哪條、為什麼。直式專案先沿用三張橫式背景（取中間），不用另做直式背景。
完成判準：能力表已貼、選了一條路。
常見錯誤：想幫使用者安裝 codex／mmx 或登入 → 不要，沒裝不裝、沒登入不登入，直接走下一條路（AGENTS.md 規則 3、工具注意事項）；使用者也要換暗色背景（`bg-fs-dark.jpg`、`bg-side-dark.jpg`、`bg-ch-dark.jpg`）→ HTML 路線還不能做暗色，走 mmx（`references/image-routing.md` 第 3 節的暗色提示詞）或使用者的圖，亮、暗各三張一起過停點 ⑥；沒有 mmx 也沒有使用者的圖，亮色三張照常換，暗色沿用目前的，回報寫「暗色背景沒換，要 mmx 或你給圖」。

**3. 生成到暫存資料夾、驗證、預覽 → 停點 ⑥**（每條路的指令在 `references/image-routing.md`）

生圖很久，有能派子代理的工具就照 `references/bg-worker.md` 每張圖派一個工人，同一則回覆一次全部派出；全部回來後由你驗證、出預覽。沒有才自己一張一張做。下面的指令是工人（或你自己）照著跑的。

```
node shared/template/tools/brand.mjs bg --html <暫存資料夾>/bg-fs.html --kind fs --out <暫存資料夾>
ffprobe -v error -show_entries stream=width,height -of csv=p=0 <暫存資料夾>/bg-fs.jpg
```

第 1 行是 HTML 路線（USAGE-reference.md R9.4；`--kind` 依序 `fs`、`side`、`ch` 各跑一次，三張都有才產生 `preview.jpg`）；其他路線照 references 的指令，再用 references 的 ffmpeg 指令產生 `zones-fs.jpg`、`preview.jpg`。`--out` 不能是 `shared/template/` 裡面。
完成判準：三張尺寸是 `1920,1080`／`960,1080`／`1920,1080`；`zones-fs.jpg`、`preview.jpg` 存在；留空區乾淨（HTML 路線看 `brand.mjs bg` 每張印 `✔ 留空區乾淨`；其他路線看 `zones-fs.jpg`、`zones-side.jpg`、`zones-ch.jpg` 的框裡沒有裝飾，references 第 5 節）。
常見錯誤：尺寸不對 → 用 references 第 1 節的 `scale…crop` 指令裁成對的尺寸。

**4. ⑥ 同意後：存成風格包、套用，重跑 build**

```
node shared/template/tools/brand.mjs pack <名稱> --color "#RRGGBB" --bg <暫存資料夾> --note "<一句說明>"
node shared/template/tools/brand.mjs use <名稱>
node shared/template/tools/build.mjs --project projects/<專案>
```

第 1 行把主色、外框、三張背景（暫存資料夾有 `bg-*-dark.jpg` 也一起）存進 `shared/template/styles/<名稱>/`；第 2 行換掉整個工作區（使用者只要這一集就跳過，改照步驟 7 寫 plan.json 的 `style`）。這兩行就是「同意後放進 shared/template/」，不要另外 cp 背景圖。包名：使用者有說就用；沒說用「<主色名>-<YYYYMMDD>」（例 `綠色-20261109`），回報寫出來。沒換主色就拿掉 `--color`。
`use` 停下來說「不屬於任何包」：這次跑過步驟 1，開工時 ● 在某一包（或開工時已經先存成 `原本-<YYYYMMDD>`），就加 `--force` 再跑一次 use（只蓋掉這次換主色的半成品）；其他情況先 `brand.mjs pack <新名稱>` 把目前的存起來再 use。

完成判準：回報改了哪些檔、走的是哪一條路；有專案時 build 0 個 ✖。
常見錯誤：使用者說「重做」→ 回步驟 3，只重派要重做的那張；同一條路重做 2 次還不行就換下一條路（R9.3）。

**5. 講者調光、瘦臉的預設**（使用者說「以後都要調光」「預設瘦一點」「預設不要調光」時；預設兩個都是 0＝關）

```
node shared/template/tools/look.mjs status --project projects/<專案>
```

改 `shared/template/kit/look.json` 的 `color`（0–1）或 `slim`（0–1.2），其他鍵不動；只想改這一集（「這集要調光、瘦臉」）就寫 plan.json 第一層的 `look`（建議 `{ "color": 0.8, "slim": 0.6 }`），不要改這個檔。改了 `slim` 照 `look.mjs status` 的「→ 下一步」重跑 `look.mjs run`：「→ 下一步：<說明>」下面那一行（最後一行）就是指令，整行複製、單獨一行執行。
完成判準：`look.mjs status` 的「設定」那一行是新的值。
常見錯誤：把 `color`、`slim` 以外的鍵也改了 → 把那幾個鍵改回原本的值。

**6. 換主題（亮／暗）**（使用者說「換暗色」「換主題」「改回亮色」時）

```
node shared/template/tools/build.mjs --project projects/<專案> --check
node shared/template/tools/build.mjs --project projects/<專案>
```

先重新讀 plan.json（剪輯台可能改過），只改第一層的 `"theme"`：`"dark"`＝暗色（石墨黑底、玻璃卡）；`"light"`＝亮色（預設，不寫也是亮色）。只換顏色 token，版面與動態不變；這一步不改 `shared/`，不用停點 ⑥。
完成判準：`--check`、build 都 0 個 ✖；回報寫改成哪個主題、改的是哪個 plan.json。
常見錯誤：寫成 `"theme": "暗"`、或寫進某一段的 scene 裡 → 只能是 `"light"` 或 `"dark"`，寫在 plan.json 第一層。

**7. 風格包：列出、這一集用、整個工作區換**

```
node shared/template/tools/brand.mjs list
node shared/template/tools/brand.mjs use <名稱>
node shared/template/tools/build.mjs --project projects/<專案>
```

先跑 list 把清單貼給使用者（內建「預設」橘色、示範「藍圖」藍色；也可以請他打開 `shared/template/index.html`，上方「風格」選單可以直接預覽每一包、亮／暗）。只換這一集：重新讀 plan.json，在第一層寫 `"style": "<名稱>"`（不跑 use）；換回工作區目前的就刪掉 `style`。整個工作區換：跑 use（之後每集都用它）。這一步不用停點 ⑥（風格包已經是使用者同意過的檔）。
完成判準：只換一集時 build 印 `風格包：<名稱>`；整個換時 list 的 ● 在那一包；build 0 個 ✖。
常見錯誤：`✖ style：找不到風格包` → 名稱照 list 抄（資料夾名，含中文）；use 說「不屬於任何包」→ 先 pack 存起來，不要直接加 `--force`（步驟 4 換過主色的例外寫在步驟 4）。

**8. 講者資料**（使用者說「講者設定成 <姓名>，頭銜 …」「不要講者介紹」，或 `status.mjs`／`--check` 印「還沒設定講者」而使用者給了資料時）

```
node shared/template/tools/brand.mjs speaker --name "<姓名>" --titles "<頭銜1>,<頭銜2>" [--short "<金句出處>"]
node shared/template/tools/brand.mjs speaker
```

寫 `shared/講者.json`（不進版控；14 講者介紹不寫 `name`、`titles` 就用它，15 金句不寫 `by` 用 `short`）。頭銜用逗號或「、」分開；只改頭銜就只給 `--titles`。不要講者介紹：`brand.mjs speaker off`。姓名、頭銜一定是使用者給的，不要從講稿或頻道名猜；這一步不用停點 ⑥。
完成判準：第 2 行印 `講者：<姓名>…`；有專案時重跑 build 0 個 ✖、沒有「還沒設定講者」的 ⚠。
常見錯誤：`✖ 講者資料不對：… 最多 6 字` → 把超過的頭銜唸給使用者、請他給短一點的，不要自己縮。

## 停點

```
⏸ 停點 ⑥ 背景預覽｜請看 <暫存資料夾>/preview.jpg 和 <暫存資料夾>/zones-fs.jpg
請回：「可以」或「重做」
```

停點 ⑥ 不能略過：背景圖放進 `shared/` 一定要使用者同意（AGENTS.md 規則 1）。暫存資料夾寫完整路徑。

| 使用者回 | 做什麼 |
|---|---|
| 「可以」 | 步驟 4 |
| 「重做」 | 步驟 3（只重派要重做的那張）；同一條路第 2 次還不行換下一條路 |

## 自我核對

- [ ] 用了哪個色碼已回報
- [ ] 能力表已貼
- [ ] 沒有安裝工具、沒有幫使用者登入任何服務
- [ ] 三張圖先在暫存資料夾，尺寸 1920×1080／960×1080／1920×1080
- [ ] 背景圖、新的風格包在停點 ⑥ 通過才寫進 `shared/`（步驟 1 換主色、開工時存 `原本-<YYYYMMDD>` 不用等 ⑥）
- [ ] 只改了 AGENTS.md 規則 1 允許的檔；換主題只改了 plan.json 第一層的 `theme`、單集換風格只改了 `style`

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| 能力表 codex 是「未登入」或「沒有安裝或壞掉」 | 走路由表的下一條路；回報寫「登入 codex 之後可以改用生圖」 | — |
| 能力表 mmx 是「未登入」 | 同上 | — |
| `可用的生圖路線：無 → 背景圖只能用使用者上傳的圖` | 只換主色、保留目前的背景，告訴使用者原因，請他上傳圖片 | — |
| `⚠ 紅框（全畫面主卡）裡有 N% 的像素是裝飾` | 裝飾移到框外，重跑同一個 `brand.mjs bg` | 換下一條路 |
| `✖ 輸出資料夾不能在 shared/template/ 裡` | `--out` 改成暫存資料夾 | 停下來回報：指令、錯誤原文、已經試過什麼 |

## 工具呼叫預算

最多 15 次。超過就停下來回報卡在哪。

## 回報格式

```
主色：<色碼>（<色名>）；對比 <brand.mjs 原文>
能力表：<貼 caps.mjs 的表>
走的路：<使用者的圖／Codex／mmx／HTML>，理由：<一句>
主題（只在換主題時）：<light／dark>，改了 projects/<專案>/work/hyperframes/plan.json；build ✖ 0
三張背景：<暫存資料夾>/bg-fs.jpg 1920×1080、bg-side.jpg 960×1080、bg-ch.jpg 1920×1080
<停點 ⑥ 那一行原文，暫存資料夾寫完整路徑>
```

⑥ 通過後：`存成風格包：shared/template/styles/<名稱>/；套用：<整個工作區（brand.mjs use）／只有這一集（plan.json style）>`＋`→ 重新打開 shared/template/index.html，上方「風格」選 <名稱> 預覽`。

## 什麼時候讀 references/

- `references/image-routing.md`：步驟 3 生成背景圖時才讀。
- `references/bg-worker.md`：步驟 3 要派工人同時生成時才讀。
