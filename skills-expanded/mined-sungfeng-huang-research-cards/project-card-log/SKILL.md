---
name: project-card-log
description: >-
  From a project-wise session, find THIS project's Heptabase card and log
  progress as SELF-CONTAINED log cards — weekly reports to the project
  lead/mentor: each log event becomes its own card (前情提要 recap that
  needs no back-reading, what was done, results with explained metrics,
  what it means, decisions pending — no unexplained abbreviations), and the project chain only gains
  one human-readable timeline line (📎 date [[card]] one-sentence summary) —
  the chain stays a readable project timeline for handoff (to the user, to
  the Mac, to the paper side). Auto-resolves which card via a per-repo
  .heptabase-card marker, then a registry (projects.json), then search. Use
  when the user says 補卡 / 記實驗 / log progress / 記進度 / handoff 實驗進度 /
  update my Heptabase project card / 把進度寫進 Heptabase. Transport: local
  `heptabase` CLI when available (Mac), else the `hb` bridge (remote over SSH).
allowed-tools: Bash(hb:*) Bash(heptabase:*) Bash(python3 *) Bash(git *) Bash(rg *) Bash(grep *) Bash(ls *) Bash(cat *) Read
---

# Project Card Log — enrich THIS project's card from its codebase

## Transport（先確認用哪條路）

```bash
command -v heptabase && heptabase --version   # 本機有 CLI（Mac + desktop app）→ 直連
command -v hb                                  # 否則走 hb bridge（遠端 session）
```

指令對應（下文以 `hb` 示例；本機直連時換用右欄）：

| bridge | 本機 CLI |
|---|---|
| `hb read <ID>` | `heptabase note read <ID>` |
| `hb append <ID> "<md>"` | `heptabase note append <ID> -c "<md>"` |
| `hb search "<q>"` | `heptabase card list -q "<q>" --limit 5` |
| `hb log-exp …` | （bridge 專屬離線佇列；直連時用一般 append） |

> ⚠️ 表中的 `append`／`log-exp --to` 都是**單卡低階指令**：卡片有續卡鏈時
> 它們直寫你給的那張卡（通常是 entry），內容會錯落在 sentinel 之後。
> 對專案卡寫進度**一律走 `append_card.py`**（自動 tail-walk）；已經錯落
> 的卡用 `repair_chain.py --card <ENTRY_ID>` 修（Mac-only，先 `--dry-run`）。

兩條路都是 **append-only 的用法**：即使 CLI 支援 overwrite 也不要用——
enrichment 一律附加帶日期的新段落，合併整理交給 project-card-merge。

Each cluster session lives in one project's repo. This skill resolves the
**matching Heptabase card** and appends codebase-grounded content to it via the
`hb` bridge. The card is the synthesis/ideation + paper-reference layer; the raw
logs stay in the repo (`CHANGELOG.md` / `NOTES.md` / sweep docs / wandb).

> **`hb` is append-only** (the bridge exposes read + append/create, NOT overwrite
> or todo-checking). So enrichment = **append a dated section**, never edit the
> existing brief in place. The user tidies/merges later on the Mac.

## Step 1 — Resolve which card this project maps to
```bash
python3 <此 skill 目錄>/resolve_card.py   # plugin 內路徑；兩個 agent 皆同
```
It prints one JSON line. Act on `source`:
- `marker` / `registry` / `env` → you have `card` (+ `title`). Proceed to Step 2.
- `registry-ambiguous` → show `candidates`, ask the user which.
- `none` → this repo isn't pinned yet:
  1. Search first（`hb search` / `heptabase card list -q`）—— the card may
     exist but be unpinned. Found → confirm with the user, pin via the
     marker (below).
  2. **Not found → create it**: confirm the title with the user, then

     ```bash
     python3 <此 skill 目錄>/create_project_card.py --title "<Title>"
     ```

     It creates the card WITH the 定位/現狀/brief skeleton, tags it with
     config `heptabase.collections.projects.tag_name`（default `project`；
     tag 不存在會自動建立）, and pins the mapping — check `record` in the
     JSON output: inside a git repo it writes `.heptabase-card` at the git
     root（`record: marker`）；cwd NOT in a git repo（典型：project root 是
     普通目錄、git repos 在它底下）→ 改為在 registry 追加
     `match_any: [<dir name>]` 條目（`record: registry`——marker 放在
     nested repo 的 git root 之上會被 marker 搜尋的 stop-at-git-root 規則
     擋住，registry 的路徑子字串比對才蓋得到；條目 per-machine，別台機器
     要重加）. Transport auto-picked（local heptabase CLI → tag 完整；
     hb bridge → 建卡＋提醒回 Mac 補 tag；backend=obsidian →
     `Projects/` 資料夾＋frontmatter tag）.
  3. Manual pin (existing card):
     ```bash
     printf 'card: <CARD_ID>\ntitle: <Title>\n' > "$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.heptabase-card"
     ```
  (Or register globally: add a `match_any` entry to
  `~/.config/research-cards/projects.json` — template: this dir's projects.example.json.)

Never guess a card id — resolve or confirm first.

## Step 2 — Read the card, focus on what's missing
```bash
hb read <CARD_ID>          # markdown; or `hb read <CARD_ID> --json`
```
Read **「現狀」** and the **「📝 待補成 paper 級參考」** brief. That brief is your
to-do list: each bullet names specific files/metrics to pull (e.g.
`docs/experiments/cos2_sweep_curriculum.md`, `NOTES.md §9`, a wandb project).

## Step 3 — Gather from THIS repo (evidence only)
Use Read / `rg` / `git log` on the local codebase to collect exactly what the
brief asks: method specifics + dimensions, full ablation numbers/tables,
baselines, design rationale (the WHY), figure sources.
- **Only write what the codebase/logs actually support.** If a number or claim
  can't be found, write it as `（待確認：…）` rather than inventing it.
- Keep model/metric/config names verbatim; numbers exact.

## Step 4 — 寫進度：log-as-card（預設）

**每次 log＝建立一張 self-contained 的新 log 卡，鏈尾只 append 一行時間線
連結**——專案卡鏈保持成一條**人看得懂的時間線**（一行一事件），完整脈絡
住在 log 卡上；把時間線蒸餾回正文是 project-card-merge 的事。

```bash
python3 <此 skill 目錄>/append_card.py --card <ENTRY_CARD_ID> \
    --log-title "<專案短名>｜<一句主題>（YYYY-MM-DD）" \
    --log-summary "<一句人話摘要——不用代號>" \
    --content-file log_body.md
```

鏈尾長出的一行：`📎 2026-07-21　[[card:<log卡>]]　<一句人話摘要>`
（Mac 直連會自動 seal 成可點的卡片節點；bridge 端是文字型——輸出的
`note` 會提醒回 Mac 跑 `repair_chain.py --card <ENTRY> --seal` 收斂。）

log 卡出生掛 **log tag**（config `log_tag_name`，預設＝projects tag 的
child tag `<tag_name>/progress`，如 `project/progress`）——log 卡是進度
紀錄、不是專案卡，自成一族才不會淹沒 project tag 掃描（0.40.0 起；設
`log_tag_name` 等於 `tag_name` 可恢復舊行為）。想讓 log 卡帶機器可讀的
「屬於哪個 entry」邊：在 app 裡給該 log tag 加一個叫 `relation_property`
名（預設 `project`）的 relation property，之後的 log 卡自動設值（輸出
`log_related:true`），無須改 code。

### log 卡寫作規格（週報 hard rules——讀者＝專案主持人／mentor）

**讀者設定（總綱）**：把使用者當成 project manager／lead／mentor——
記得專案的目標、**不記得上週的細節**、同時看好幾個專案。每張 log 卡
＝一份**能單獨讀懂的週報**：前情提要把脈絡補齊到「讀者不用回翻任何
先前的卡」的程度（同論文卡的先備知識段之於論文）。

1. **無縮寫**：盡量避免代號／縮寫；用到的**首次出現必須展開或一句話
   解釋**——「E0（＝baseline 訓練、無 curriculum）」「RTF（real-time
   factor，越低越快）」。**整卡反覆使用的代號集中在前情提要末尾當
   小詞彙表**（一行一個，同論文卡先備知識的角色），正文即可放心用；
   只出現一次的就地展開即可。
2. **前情提要先行**（三小段——取代舊版「背景脈絡」）：
   1. **專案一句話**：目標＋為什麼重要（從 entry 卡定位段精煉，
      勿假設讀者記得）。
   2. **至上次為止**：與本次最相關的 1–3 個已確立結論／數字，
      **附出處**（上一張 log 卡的 card-link 或 entry 卡段落）。
   3. **這次要回答什麼、為什麼現在做**。
3. **結構模板**：

   ```markdown
   # <專案短名>｜<一句主題>（YYYY-MM-DD）

   **專案**：[[card:<ENTRY_ID>]]　**環境**：<cluster host／Mac>　**代碼**：<repo>@<short-sha>

   ## 前情提要
   （三小段：專案一句話 → 至上次為止的關鍵結論（附出處）→ 這次要回答
   什麼；反覆使用的代號在此段末尾一行一個定義）
   ## 做了什麼
   ## 結果
   （數字表格；每個指標一句「這個數字是什麼、越高還越低好」）
   ## 這代表什麼
   （對專案的意義，1–3 句——接回前情提要提出的問題）
   ## 待裁決／下一步
   （需要主持人拍板的事**逐條列**，每條含裁決選項與你的建議）
   ```

4. **--log-summary 用人話**：時間線行是主持人掃鏈時唯一看到的字——
   「課程學習讓 val loss 再降 8%，但推理變慢待裁決」勝過「E3 done」。

- `--card` 一律傳 **Step 1 的 ENTRY 卡**（母卡）；script 沿鏈走到 tail。
- `--dry-run` 先看計畫（不建卡、不寫入）。
- 離線（bridge down）會 fail-fast 不建孤兒卡；create 成功但 link 失敗時
  會存 recovery 檔並印補救指令。
- **（Mac）log 完先跑 note-sync（硬規則）**——log 卡剛出生，鏡像
  （obsidian mirror／HackMD）與 heptabase-sync 的 state 帳都還沒有它；
  下面兩步視圖刷新都讀 vault mirror（canvas 靠 state 帳判「已鏡像」、
  origin 嗅探讀 mirror 內容），不 sync 先刷＝節點降級「未鏡像」＋
  origin 判 unknown：
  ```bash
  python3 <plugin 的 skills/note-sync 目錄>/sync.py   # 全鏈；趕時間至少 --mode heptabase
  ```
  cluster 端無 vault／CLI：跳過（回 Mac 補跑）。
- **（Mac）log 完補 story graph**——若現有心智圖是 story，優先跑
  `story_auto_expand.py --card <ENTRY>`：它只把 coverage 缺口交給隔離的
  Codex task 改 proposal copy，通過 append/lifecycle guard 且 coverage
  清空才套用。手動補時，新進展通常在 graph 尾端 append 節點/邊；只有
  明確帶 `semantic`＋`lifecycle` 的「進行中／開放線／開放洞／下一步／
  待捕」節點可受限更新（完整契約見 **project-card-canvas** skill）。
  graph 不存在＝該專案還沒建敘事圖，跳過（建圖是 canvas skill 的事）。
- **（Mac）log 完刷新 project canvas**——git-graph 視圖（log 卡＝
  commit 直欄由新到舊；entry＝HEAD 指標側貼**最新已蒸餾 📗** 那排、
  📎 backlog 堆在 HEAD 之上——蒸餾狀態由拓撲表達）：
  ```bash
  python3 <plugin 的 skills/project-card-canvas 目錄>/project_canvas.py --card <ENTRY_CARD_ID>
  ```
  生成 `<vault>/Projects/Canvas/<專案>.canvas`（生成式視圖，別手排；
  資料夾可用 config `local.folders.project_canvas` 覆蓋；cluster 端
  無 vault 跳過，回 Mac 再刷）。顏色預設按 **log 來源機器**分色
  （Mac session=cyan／cluster session=yellow／判不出=灰；讀 log 卡的
  `環境` 欄或回溯卡 `原段：📥 …` 行）；`--color-by state` 換回
  📎橙/📗綠 舊軸；config
  `heptabase.collections.projects.canvas_color_by` 可改預設軸。
- **（cluster→Mac 自動收斂）**——`hb` transport 的 log 卡＋時間線行都
  成功後，`append_card.py` 會把
  `{entry_card, log_card, timeline_card, repair_chain}`
  寫進 cluster 的
  `~/.heptabase-bridge/project-log-events.jsonl` durable queue。啟用新版
  heptabase-ssh-bridge 的 `HB_POST_DRAIN_HOOK` 後，Mac drainer 每次拉取
  queue 會呼叫本目錄 `post_log_sync.py`，固定依序跑：
  **必要時 repair_chain --seal → pinpoint project-card-repair
  （log 卡含安全 inline 引用；timeline tail 僅結構 link）→
  整批一次 note-sync → 每個 entry 的
  timeline canvas＋裸跑 context mind map**。同一批同專案自動去重；
  任一步失敗／note-sync 有 conflict 都保留事件重試。logs/chain 會驗證
  所有 log/section 都已映射；story 有 coverage gap 時自動追加
  `story_auto_expand.py` 的受限語義擴充，失敗則回復 graph 並保留事件。
  若 Mac config 是 Heptabase-only、沒有 local hub，仍會完成 repair，
  但會略過本來就不可用的 note-sync／canvas，不製造永久 retry queue。
  queue 寫入失敗不會把已成功落卡的 log 偽報成失敗，JSON report 會以
  `automation_queued:false` 明示需回 Mac 手動補跑。
- **（實驗）脈絡心智圖**——三種拆解單位（需 backend=both）：
  ```bash
  python3 <plugin 的 skills/project-card-canvas 目錄>/context_mindmap.py --card <ENTRY_ID>   # 沿用既有模式擴充（無既有→logs）
  python3 <同目錄>/context_mindmap.py --card <ENTRY_ID> --mode chain  # 切 chain 模式
  python3 <同目錄>/context_mindmap.py --card <ENTRY_ID> --mode story \
      --graph <vault>/…/<專案>·脈絡心智圖.graph.json                        # 新建 story（既有 story 裸跑即自動接圖）
  ```
  **裸跑（不帶 `--mode`）＝就地擴充**既有那張心智圖（偵測其模式重生；
  story 自動接同名 `.graph.json`），刷新不必記模式。**logs**（首建預設）：
  每張 self-contained log 卡拆成 root（軸卡）→ hub
  （log）→ ❓這次要回答／🔬做了什麼／📊結果／💡這代表什麼／⚖️待裁決
  分支，掛點＝前情提要引用的最新 log（隨新 log 卡擴充、節點 id 穩定；
  `--limit 1`＝最早根卡單獨拆解）。**chain**：拆卡鏈正文 H2（hub，依
  角色配色）→ H3（葉）——結構目錄視圖。**story（研究敘事 DAG）**：
  「因為想法→做了實驗→結果→轉向/分岔/回頭」的推理鏈藏在散文裡，
  由 **agent 讀鏈撰寫 graph JSON**（完整撰寫契約見 **project-card-canvas skill**；
  節點 kind＝idea/question/experiment/result/finding/decision/pivot/open、
  邊帶連接詞 label；節點順序＝敘事序、id＝穩定 slug；選填 stage 欄
  只標每幕第一個節點＝multi-row 換行排版，一幕一 row），script 做確定性
  分層 DAG 佈局；三模式 canvas 皆含色彩圖例節點。graph JSON 放 canvas 同資料夾（`<專案>·脈絡心智圖
  .graph.json`）；新進展＝agent 在 graph 尾端加節點/邊再重跑（圖只增
  不動）。輸出 `<vault>/<Canvas 資料夾>/<專案>·脈絡心智圖.canvas`。

### 舊模式：直接 append 段落（相容保留；append 完同樣適用上面的
（Mac）note-sync 硬規則——直寫段落一樣讓鏡像落後）

小型機械性補充（不值一張卡的一兩行）仍可直接 append；campaign step 7
等內部流程也還走這條：
```bash
python3 <此 skill 目錄>/append_card.py --card <ENTRY_CARD_ID> --content-file section.md
```
- `--card` 一律傳 **Step 1 的 ENTRY 卡**（母卡）。script 自己沿鏈走到 tail——**絕不傳子卡 id**。
- **卡沒滿**（常態）：`overflowed:false` → 內容直接 append 到 tail。
- **卡接近容量上限**：**預設（0.24.1 起）自動 spill**——建續卡子卡並在 tail 補
  `▶ 續卡…[[card:<id>]]`（`overflowed:true, child:<id>`）；無 config 的機器
  （cluster bridge）同樣適用。子卡自動上 project tag（bridge 484db04+ 有
  `hb tag-add`；更舊的 hb client 拿不到 tag → 讀輸出 `note` 補），並 best-effort
  把 tag 的 relation property（config `relation_property`，預設同 tag 名）指回
  entry 卡（輸出 `related` 欄位）——tag 掃描因此能區分 entry 與續卡。config 顯式設
  `heptabase.collections.projects.overflow_spill=false` 可改回滿卡 fail-fast
  （不 spill、不移內容，訊息叫你先回 Mac 用 project-card-merge 整併）。
- 想先看會不會溢位：加 `--dry-run`（只讀，回報 `dry_run:true`＋是否 would-block/would-spill）。
- 把一條鏈**整併回一張卡**是 **Mac-only 的 project-card-merge** 的事（需 overwrite/
  delete，append-only 的 bridge 做不到）——完整規格與 `overflow_spill` 啟用順序見
  `CARD-OVERFLOW.md`。

範例段落內容（append_card.py 的 `--content` 就餵這個）：
```markdown
## 📥 cluster 補充 2026-06-24（from <repo>@<git short-sha>）
### Method
- <evidenced detail …>
### Experiments
- <full ablation numbers / table …>
### Findings / Results
- <…>
```
（低階等價 `hb append <ID> "<md>"` 直接寫、但**不處理容量上限**——一律走 append_card.py。）
For a quick single experiment result instead of a full enrichment:
```bash
hb log-exp model=<m> val_loss=<x> step=<n> --to <CARD_ID>
```
Writes queue locally and auto-sync if the Mac/tunnel is down (`hb drain-status`).
> ⚠️ `hb log-exp --to` 直接寫進 **ENTRY 卡**，**不走 append_card.py 的 tail-walk /
> 容量檢查**。只在母卡「沒有續卡鏈、且離上限還遠」時用。卡已 chained 或接近上限時，
> 把該結果當一小段 markdown 餵給 `append_card.py`（`--content`），才會落到正確的 tail
> 並受容量保護。

## Step 5 — Report
Tell the user what you appended and what's still `（待確認）`. Suggest they do a
final merge/cleanup on the Mac (where full edit/overwrite is available), since
`hb` could only append.

## Notes
- One repo ↔ one card. A monorepo with several projects: put a `.heptabase-card`
  in each subproject dir (the marker search walks up from cwd, nearest wins).
- Adding a brand-new project: `create_project_card.py` handles card + skeleton
  + tag + pin in one step from anywhere（見上方 none 分支）；monorepo 子專案
  記得傳 `--marker-dir "$(pwd)"`，marker 才不會 pin 到整個 repo。
- Project root 不是 git root（git repos 在它底下）：從 project root 跑
  create_project_card.py 會自動 fallback 成 registry 條目
  （`match_any: [<dir name>]`），底下所有 nested repo 都經路徑子字串比對
  解析到同一張卡——一卡對多 repo 本來就是 registry 的守備範圍。
