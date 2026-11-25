---
name: teaching-page
description: 開一個教學頁——會訓練的（worker ＋ WasmTrainer 逐步介面）或靜態的（bin 匯出 JSON ＋ 畫面）。當階段 6 要新增任何一幕視圖時使用。
---

# 開一個教學頁

兩半：**會訓練的**（worker ＋ `WasmTrainer`）與**靜態的**（`bin` 匯出 JSON ＋ 畫面）。

## 何時用

階段 6 要新增**任何一幕會訓練的視圖**：新的觀測、新的旋鈕對照、新的拼裝方式。

**不適用**：**量測台**——那用 `browser-measure`，而且**不要加在教學頁上**（見陷阱 1）。

## 會訓練的那一半

**這件事已經做了兩次**（功能 025 的 `live.html`、功能 026 的 `palette.html`），
而兩支 worker 的**實質差別是 1 行**：

```
diff live-worker.js palette-worker.js  →  14 行，其中 11 行是註解
真正的差別：new WasmTrainer(...)  vs  WasmTrainer.fromAssembly(...)
```

第三次之前把它固化——**不是為了省打字，是為了不再漏掉那三件容易漏的事**。

## 三件容易漏的事（這個 skill 存在的真正理由）

### 1. **不吞錯**

worker 裡的 `catch` 必須 `postMessage({type:'error', …})`。
設定不合法、策略認不得、訓練發散——**主執行緒看不到就等於沒發生**（憲章原則 V）。

### 2. **讓出事件迴圈，否則 `cancel` 永遠收不到**

```js
if (steps % 20 === 0) await new Promise((res) => setTimeout(res, 0))
```

worker 的 `onmessage` 在同步迴圈裡**排不進去**。沒有這一行，「停止」按鈕是死的。

### 3. **快照只在命中步才送**

```js
const arcs = r.arcs
if (arcs !== undefined) msg.arcs = arcs
```

語義與既有的 `geometry` 一致：**只在更新間隔命中的那幾步有值**。
每步都送會讓主執行緒忙著處理訊息，而那會把「Worker 沒有阻塞主執行緒」量成假的紅燈。

## 步驟

1. **複製 `web/live-worker.js`**，只改建構那一行。**不要從頭寫**——上面三件事已經在裡面
2. **複製 `web/live.html` 的 `panelSvg`**（弧線畫法）與 `render` 的骨架
3. **畫法參數用 `arcsweep` 掃出來的值**，不要憑感覺選（見「相關」）
4. **每一張有損視圖標「畫出 N ／ 總可能 M」**（原則 5）
5. **量不到的東西要明說**——不要顯示空圖或 0。
   `palette.html` 有一張「這個拼裝量得到什麼」的表可以照抄
6. 若要驗效能：**用 `browser-measure`**，不要自己想量法

## 靜態的那一半（不訓練，讀一份預先產生的 JSON）

這一半也做了四次了（`arcs`／`lift`／`cut`／`atlas`），而它的形狀固定：

```
src/bin/<名字>.rs   量測 ＋ 判準 ＋ 匯出 web/<名字>.json
web/<名字>.html     fetch('<名字>.json') → 畫
```

**為什麼資料在 Rust 側算完**：畫面只負責畫。判準若寫在 JS，
它就跑不進 `cargo test`，也不會被 `cargo run` 印出來給人看。

## 靜態頁的五個必要元素（每一個都是踩過的）

| # | 元素 | 為什麼 |
|---|---|---|
| 1 | **標示投影損失** | 原則 5。`atlas` 只解釋 **19.0%**——不標的話學生以為看到全部 |
| 2 | **一層零損失的呈現** | 散佈圖丟掉八成，而**最近鄰清單丟掉 0**。它不是附註，是**錨** |
| 3 | **不抽樣** | `cut` 的「第 0 層兩類逐位元相同」只有畫全部點才看得見 |
| 4 | **畫的例子要有代表性** | `lift` 第一版用第 0 個種子，而它是離群值（`history/048`） |
| 5 | **判準的限制寫在畫面上** | `cut` 三條、`atlas` 兩條、`lift` 兩條。**不是附錄，是內容** |

## ⚠ 匯出 JSON 的兩個實際陷阱

- **控制字元**：詞彙表裡有**換行**，它會出現在最近鄰裡。
  原始 `\n` 寫進 JSON 是非法的，瀏覽器直接解不開
  ——而錯誤訊息只說「line 6 column 9009」。**要逃脫。**
- **`f32` vs `f64`**：`Projected` 的座標與嵌入表可能不同精度，
  複製貼上一段計算會編不過（`atlas` 踩過）

## 靜態頁的樣板

`web/cut.html` 最小、`web/atlas.html` 最完整（散佈 ＋ 表格 ＋ 跨頁連結）。
**跨頁連結值得做**——`atlas` 連到 `cut`，讓「開場與收尾是同一個東西」
從一句話變成一個可以點的動作。

## 陷阱

- **靜態頁不要用 worker**——沒有東西要跑，`fetch` 就夠了
- **不要把畫面加在 `web/train.html` 上**——它是**功能 018 的量測台**
  （標題「訓練跑在 Worker 裡，分頁不會凍住」）。功能 025 的計畫原本這樣寫，
  讀程式碼才發現。同理 `background.html`、`probe.html` 也是量測台
- **`WasmTrainer` 的逐步介面 vs `train_with_callback`**：後者**一次呼叫跑完**，
  取不了中途快照。教學頁一律用前者
- **`Unflatten` 的批次**：拼裝模型的探針批次要能與訓練批次不同
  （功能 026 修過一次 `reshape` panic）
- **量效能前先驗 `document.visibilityState === 'visible'`**——
  背景分頁實測慢 **4.5~5.23 倍**

## 相關

- [browser-measure](../browser-measure/SKILL.md)——效能驗收用它，不要重新規劃量法
- `src/bin/arcsweep.rs`——畫法參數的掃描台（門檻／更新間隔）
- [history/045](../../history/045-活的弧線圖而我事先的推論錯了三次.md)——第一次
- [history/046](../../history/046-元件盤而兩個舊bug被實跑抓到.md)——第二次，以及觀測如何照出舊 bug
