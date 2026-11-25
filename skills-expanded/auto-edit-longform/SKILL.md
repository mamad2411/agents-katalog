---
name: auto-edit-longform
description: 長片總指揮：判斷 projects/<專案> 做到哪一步、第一次開工填開工決策表、把工作交給對應的階段 Skill、維護 work/製作進度.md 的階段表與停點紀錄。當使用者說「用 auto-edit-longform 剪 projects/X」「剪這支影片」「繼續」「繼續 projects/X」「下一集」「做到哪了」「剪成短影片」「做直式」時使用。只做單一階段（只剪乾淨、只換主色、只開剪輯台）時不要用，直接用那個階段的 Skill（auto-edit-rough、auto-edit-style、auto-edit-review）。
version: 0.2.0
---
# 總指揮：做到哪、交給誰

規則在 AGENTS.md；本檔只寫這一階段的指令、判準、停點、退路。
衝突時：使用者當下的話 > AGENTS.md > shared/style.md > USAGE.md > USAGE-reference.md > 本 Skill；派工時派工訊息 > 本 Skill。

| 輸入 | 指令 | 產出 | 完成判準 | 停點 |
|---|---|---|---|---|
| 「剪這支影片」「繼續」「做到哪了」 | `status.mjs` | 下一條指令、該讀哪支 Skill | 照印的下一條做 | 看目前在哪 |

## 開始前

| 條件（看得到的事實） | 做法 |
|---|---|
| 沒指定專案 | 列出 `projects/` 底下的專案，問要處理哪一個 |
| `assets/camera/`、`assets/voice/` 都是空的，專案裡有散落的素材 | 先照 `references/sort-assets.md` 分類 |
| 專案裡沒有散落的素材，步驟 1 的 `status.mjs` 印「開新專案（還沒有主軌素材）」（`assets/screen/` 有邊錄邊講的錄影就不會印，照常往下做） | 照 `references/new-project.md` 第 2 點告訴使用者放什麼，最後一行 `→ 下一步：素材放好後說「剪乾淨」` |
| 使用者只問「做到哪了」 | 步驟 1 回報就好 |

## 步驟

**1. 看做到哪**

```
node shared/template/tools/status.mjs --project projects/<專案>
```

它印目前階段、該讀哪支 Skill 的第幾步、**完整可貼的下一條指令**，有待回覆停點就印停點那兩行。照著做，不用另外查路由。第一次開工：`media.mjs prep`（或 `status.mjs --project projects/<專案> --init`）會自動填開工決策表；使用者說直式時，`prep` 加 `--format portrait`。
完成判準：讀到 `目前在：`、`Skill：`、`→ 下一步：` 或待回覆的停點。
常見錯誤：印「講者：⚠ 還沒設定」→ 在回報裡問姓名與頭銜（不擋流程，不要自己編）。

**2. 有待回覆的停點**

```
（不用指令：重貼 status 印的那個停點的最後兩行）
```

完成判準：回覆最後兩行＝AGENTS.md「停點總表」那個停點的原文。
常見錯誤：使用者這句話其實就是在回覆那個停點 → 照那支 Skill「停點」表做，不要重貼。

**3. 交棒**

```
（不用指令：讀 status 印的 Skill，從它印的那一步接著做）
```

status 和實際檔案不符時以產物為準，判斷表在 `references/progress-template.md`。
完成判準：接著做的就是 status 印的那一步。
常見錯誤：把 Skill 整份讀完才動手 → 只讀那一步。

可以全自動、不用問的：轉逐字稿、`--check`、build、audit、`qc.mjs`、`status.mjs`。一定要停的：AGENTS.md「停點總表」的 ①–⑥。

## 版式（橫式／直式）

開工時決定一次，`media.mjs prep` 寫進開工決策表「版式」：使用者說「短影片」「直式」「Shorts」「Reels」「抖音」→ `prep` 加 `--format portrait`；說「長片」「橫式」或都沒說 → 工具看主軌，寬 < 高才是直式。之後說「改成直式」：先在 `work/hyperframes/plan.json` 第一層加 `"format": "portrait"`（還沒有 plan.json 就跳過），再跑 `node shared/template/tools/status.mjs --project projects/<專案> --init --format portrait` 改開工決策表的版式。改橫式：刪掉 plan.json 的 `format`，`--init` 改加 `--format landscape`。不用記停點紀錄。`--check` 說兩邊版式不一樣時，照這兩步補齊，不要把 plan.json 改回原本的版式。直式素材做橫式：不支援，告訴使用者；橫式素材做直式：還不支援（`--check` 會 ✖），請使用者提供直拍素材。直式的數字（畫布、版面、字幕、安全區、構圖）看 `shared/style.md`「直式」。

## 自我核對

- [ ] 專案只有一個、確定了
- [ ] 照 status 印的下一條做，沒有自己猜流程
- [ ] 有待回覆停點時重貼了那一行
- [ ] 沒讀寫其他專案的 `work/`
- [ ] 回報最多 15 行

## 退路表

| 症狀（工具原文） | 做法 | 第二次還失敗 |
|---|---|---|
| status 印的和 `work/製作進度.md` 不一致 | 以產物為準，用 `status.mjs --mark` 補一列，回報裡提醒一句 | — |
| 使用者說「繼續」但沒有 `work/` | 當作第一次開工：`media.mjs prep` | — |

## 工具呼叫預算

接手最多 2 次。超過就停下來回報卡在哪；交棒之後照那支 Skill 的預算。

## 回報格式

```
專案：projects/<專案>
目前在：<status 原文>
下一步：<status 原文，但停點那兩行不放這裡>
<最後：停點原文（兩行），或一行 → 下一個停點：…>
```

## 什麼時候讀 references/

- `references/new-project.md`：使用者說「開一個新專案」，或還沒有任何素材時才讀。
- `references/sort-assets.md`：使用者說「分類素材」，或素材散落在專案裡時才讀。
- `references/progress-template.md`：status 和實際檔案不符、要以產物判斷階段時才讀。
