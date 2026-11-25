---
name: project-card-canvas
description: >-
  Generate and refresh the VISUAL views of a research-project card chain
  as Obsidian JSON Canvas files: the timeline canvas (git-graph style —
  log cards as a commit column, the entry card as the HEAD pointer riding
  beside the newest distilled log with the 📎 backlog stacking above it,
  colored by origin machine by default) and the context mind map (three decomposition
  modes: logs = per-log-card subtrees hung on the 前情提要 citation graph;
  chain = the chain body's H2/H3 sections; story = the research NARRATIVE
  as a staged, multi-row DAG — the agent reads the chain and authors a
  story graph JSON of ideas→experiments→results→pivots with causal edges,
  the script renders it deterministically). Use when the user asks to
  畫/更新/刷新 project canvas、心智圖、脈絡圖、敘事圖、研究故事圖、
  mind map、story graph、timeline 圖, or after project-card-log /
  project-card-merge runs (refresh the views). Mac-only (heptabase CLI +
  local vault; backend=both).
allowed-tools: Bash(python3 *) Bash(heptabase:*) Bash(ls *) Bash(cat *) Read Write Edit
---

# Project Card Canvas — 專案卡鏈的視覺化視圖家族

一個專案卡鏈可以生成**兩張 canvas、四種視圖**，全部是**生成式視圖**
（每次重跑整張重建、節點 id 確定性——別手排；手排請用知識地圖 canvas）：

| 視圖 | 檔案 | 指令 |
|---|---|---|
| 時間線（git graph） | `<專案>.canvas` | `project_canvas.py --card <ENTRY>` |
| 心智圖（沿用既有模式擴充） | `<專案>·脈絡心智圖.canvas` | `context_mindmap.py --card <ENTRY>` |
| 心智圖 logs 模式（新建/切換） | 同上（共用檔） | `context_mindmap.py --card <ENTRY> --mode logs` |
| 心智圖 chain 模式 | 同上（共用檔） | `context_mindmap.py --card <ENTRY> --mode chain` |
| 心智圖 story 模式 | 同上（共用檔） | `context_mindmap.py --card <ENTRY> --mode story --graph <graph.json>` |

輸出資料夾＝`<vault>/<projects>/Canvas/`（config
`local.folders.project_canvas` 可覆蓋）。三種心智圖模式共用一個 canvas
檔（一專案一張脈絡圖）；canvas 左上皆有色彩圖例節點。

**裸跑 `context_mindmap.py --card <ENTRY>`（不給 `--mode`）＝就地擴充**
既有 canvas：讀 canvas 的**圖例節點文字**判斷它現在是哪個模式
（logs／chain／story——圖例每次 render 都重寫，必然反映當前模式）並用
**同模式**重生——生成式視圖的節點 id 是確定性的，重生本質上就是「加進
新內容、既有節點不動」，所以刷新永遠不會把 chain／story 卡洗回 logs。
偵測到是 story 卡時才自動接上同名 `.graph.json`（不用再手打 `--graph`）；
反過來說，story 切成 chain／logs 後即使殘留舊 `.graph.json`，圖例已改、
不會被硬拉回 story。**沒有既有 canvas → logs**（首建）；**明確給
`--mode X` ＝切換模式**（report 的 `extended` 欄：`true`＝沿用擴充／
`false`＝明確指定或首建）。

## 怎麼選視圖

- **時間線**：想看「發生過什麼、哪些已蒸餾」——log 卡＝commit 直欄
  （由新到舊、時間往上流），entry＝HEAD 指標（紫）**側貼在最新已蒸餾
  （📗）log 那排**並以側向箭頭指向它——所以 HEAD 之上堆的就是還沒
  蒸餾（📎）的 backlog，**蒸餾狀態由拓撲表達**（全未蒸餾＝HEAD 沉到
  欄底；無 log＝entry 獨立一格）。顏色軸因此讓給機器來源：
  `--color-by origin`（預設：Mac=cyan／cluster=yellow；讀 log 卡的
  `環境` 欄或回溯卡 `原段：📥 …` 行）或 `--color-by state`（📎橙／
  📗綠，與拓撲重複的舊軸）；config
  `heptabase.collections.projects.canvas_color_by` 改預設軸。
- **心智圖 logs**：專案用 log-as-card 週報體系——log 卡沿引用拓撲序
  **水平往右排成主幹**（時間線左→右），每張的 ❓這次要回答／🔬做了
  什麼／📊結果／💡這代表什麼／⚖️待裁決 分支**垂直垂在該卡下方**；
  非相鄰承接與「也承接」邊從主幹上方飛越。`--limit 1`＝最早根卡。
- **心智圖 chain**：舊 log 已蒸餾進卡鏈正文的專案——拆 H2（角色配色）
  →H3 結構目錄。
- **心智圖 story**：要看**研究思考脈絡**（因為想法→做了實驗→結果→
  轉向/分岔/回頭）——推理鏈藏在散文裡，需要 agent 讀鏈撰寫敘事
  graph（下節），script 只做確定性佈局。**這是本 skill 的主打視圖。**

## story 模式：敘事 graph 撰寫契約（agent 的工作）

**分工**：你（讀鏈的 agent）負責理解與撰寫 graph JSON；script 負責
驗證＋分層 DAG 佈局（重生成、id 穩定、--limit 重播由 code 保證）。

### 工作流

1. **讀鏈**：把 chain 各卡的 sections 全文讀懂（重點：定位/演進故事、
   進展里程碑、各實驗統整的結論句、Findings/設計理路、🔍/下一步）。
2. **撰寫/更新 graph JSON**：存 `<vault>/<projects>/Canvas/
   <專案>·脈絡心智圖.graph.json`（canvas 同資料夾）。已存在＝歷史 graph
   **只增不改**：新進展在尾端加節點/邊；唯一例外是下節明確標記的
   lifecycle-managed 開放節點。
3. **渲染**：`context_mindmap.py --card <ENTRY> --mode story --graph <path>`；
   讀 report 的 `label_warnings`（過長箭頭字）與 `stages`。

### graph schema（schema of record 在 context_mindmap.py 的
load_story_graph 上方註解；此處為撰寫規則）

```json
{"nodes": [{"id": "slug", "kind": "…", "label": "短標題", "text": "一兩句",
            "anchor": "出處 section", "date": "MM-DD", "stage": "幕標題"}],
 "edges": [{"from": "slug", "to": "slug", "label": "所以"}]}
```

- **id**＝穩定 slug（如 `exp-e7-attribution`）——圖的擴充契約靠它。
- **sources**＝此節點蓋掉的 log 卡 id（coverage 稽核的鍵；一個節點
  蒸餾了哪幾張 log 就列哪幾張）；anchor＝蓋掉的 section（・分隔多個）。
- **kind**：`idea`💡/`question`❓（橙）、`experiment`🧪（黃）、
  `result`📊（灰）、`finding`✅/`decision`⚖️（綠）、`pivot`🔀/
  `open`⏳（紅）。
- **節點順序＝敘事序**（驅動 --limit 重播與 row 內堆疊）。
- **stage**：只標**每幕第一個節點**，其餘沿敘事序繼承——一幕一 row
  （multi-row 換行；幕標題掛列首、跨幕邊自動向下流）。幕＝研究的
  章節轉折（沿用 entry 卡「演進故事」的分幕最自然）。
- **text 自足**：一兩句把「為什麼/是什麼/所以呢」講完，數字帶上；
  anchor 填出處 section 名（可追溯）。
- **邊 label＝短連接詞**（所以/但是/坐實/回頭重審/隔離歸因…）——
  預算 ~12 顯示單位（CJK≈2），過長會被 report 警告；語義放節點 text。
- **分岔與回頭要畫**：同一結果引出多條線＝多條出邊；回頭重審／方法論
  重演＝跨幕邊（自動 bottom→top 下行）。
- 引用先前結論時，該結論就該是一個節點——寧可多切節點，別把兩步
  推理擠在一個節點裡。
- **無縮寫（硬規則，同 log 卡週報規格）**：canvas 節點是**獨立閱讀**的
  （沒有卡片「名詞備忘」兜底）——label/text 中的代號、縮寫**首現必
  展開**（「同句對決（head-to-head）」「清濁邊界（unvoiced↔voiced）」）；
  **整圖反覆使用的代號收進 top-level `glossary`**（一行一個，渲染成
  legend 旁的名詞節點），正文即可放心用。撰寫時自問：沒讀過這條鏈的
  人看得懂這個節點嗎？

### 開放語義的受限 lifecycle

「進行中／開放線／開放洞／下一步／待捕」不是永遠凍結的歷史結論；完成
或放棄後，原節點應就地結案，而不是留下過時的「進行中」。因此只有這類
節點可加顯式 marker：

```json
{"id": "open-e9", "kind": "open", "label": "E9 進行中",
 "semantic": "open_thread",
 "lifecycle": {"state": "open", "revision": 0}}
```

- `semantic` 描述這條線的角色，合法值：
  `open_thread`／`open_hole`／`next_step`／`pending_capture`；一經建立
  不可改。
- `lifecycle.state`：`open`／`active` 可持續受限更新，之後只能收斂到
  `resolved`／`abandoned`／`superseded`；結案後重新凍結。
- 每次更新 `revision` **恰好 +1**；`sources` 只能附加。可改欄位只限
  `kind/label/text/anchor/date/sources/lifecycle`，stage、id、semantic
  不可改。
- open/active 時 `kind` 必須仍是 `open`；結案時可依語義改成
  `result/finding/decision/pivot`。
- 未帶 marker 的既有節點與所有既有 edges 逐項不可變；新 node/edge
  只能附加。`story_graph.py validate <before> <after>` 是機器守門員。
- 舊 graph 的 `kind: open` 可用
  `story_graph.py migrate <graph> --write` 一次性補 marker；依 label/text
  區分開放線、開放洞、下一步、待捕，其餘歸 `open_thread`。

## 擴充工作流：coverage 稽核（新 log／蒸餾後怎麼知道缺什麼）

story render 的 report **自帶 `coverage` 稽核**——machine 告訴你圖裡
還缺什麼材料，你只讀缺的部分、不用重讀整條鏈：

```bash
python3 <此 skill 目錄>/context_mindmap.py --card <ENTRY> --mode story \
    --graph <graph.json> --dry-run     # 只稽核不寫檔
```

- `uncovered_logs`：時間線上**沒有任何節點認領**的 log 卡（附日期＋
  摘要）。認領＝節點的 `sources` 列其 id（或 ≥8 碼前綴）。log 卡永不
  trash，id 跨蒸餾穩定——這是為什麼 sources 用 log id 當鍵。
- `uncovered_sections`：卡鏈 H2 裡**沒有任何 anchor 蓋到**的 section
  ——merge 蒸餾後新長的段（如「實驗統整(八)」）會在這裡現形。
  刻意不入圖的參考型段落（方法／評估協定…）放 graph 頂層
  `coverage_ignore` 顯式豁免，稽核才能收斂到空。

**手動擴充循環**：`--dry-run` 看 coverage → 只讀未覆蓋的 log 卡／section
→ graph 尾端加節點（記得 `sources`＋`anchor`；開新幕標 `stage`）→
重渲染 → coverage 回到空。**加節點時同步補邊**：新節點的前情提要引用
誰、承接哪個結論，邊就畫到哪。

**最便宜的補圖時機＝寫 log 的當下**：project-card-log 寫完 log 卡後，
那個 session 脈絡全在手上——順手在 graph 尾端補節點（sources=[新 log
卡 id]）＋承接邊、重渲染，缺口就不會累積（log skill 的 Step 4 有對應
步驟）。

**Fallback：紅色待補橫幅**——render 時稽核不乾淨，canvas 圖例旁會自動
長一個紅色「⚠️ 待補」節點列出缺口（canvas-only、不進 graph JSON；
補完重渲染即消失）。看到它＝這張圖落後現實，照上面循環補。

## 刷新時機

- **render 之前先跑 note-sync（硬規則）**——canvas 判「已鏡像」讀
  heptabase-sync 的 state 帳、origin 嗅探優先讀 vault mirror 內容；
  卡側剛動過（log/merge/cleanup/拆卡）而沒 sync，節點會降級「未鏡像」
  text、origin 判 unknown（0.51.0 上線當日兩度實測踩坑）：
  ```bash
  python3 <plugin 的 skills/note-sync 目錄>/sync.py   # 全鏈；趕時間至少 --mode heptabase
  ```
- `project-card-log` 寫完 log、`project-card-merge` 整併完 → 重跑
  **時間線**（HEAD 貼點/鏈型會變）＋**裸跑心智圖**（`context_mindmap.py
  --card <ENTRY>`，不帶 `--mode`）就地擴充既有那張——不用記它是 story
  還是 chain/logs，偵測到什麼就沿用什麼。story 卡則先 `--dry-run` 看
  coverage 稽核 → 按上節循環擴充 graph JSON → 再裸跑重渲染。
- cluster 端無 vault：跳過，回 Mac 再刷。
- 啟用 cluster project-log handoff 時，Mac drainer 會由
  `project-card-log/post_log_sync.py` 在 repair＋note-sync 成功後自動跑
  timeline 與裸跑心智圖；同一批 entry 會去重。story graph 的 coverage
  會照常稽核；若有缺口，hook 會啟動 `story_auto_expand.py`：把缺的
  log/section 材料放進隔離 task 目錄，由 Codex 只改 proposal copy，再經
  `story_graph.py` 的 append/lifecycle guard 與 coverage=0 雙重驗證才
  原子套用。失敗會回復 live graph 並保留 event 供重試。設定
  `RESEARCH_CARDS_STORY_AGENT=off` 可停用 agent（有 story gap 時 pipeline
  會 fail-closed，不會把落後 canvas 當成功）。
- logs 與 chain 不需要語義 agent：裸跑已確定性包含所有 log/H2-H3，
  hook 另外要求 `logs_mapped == logs_total` 或
  `sections_mapped == sections_total`；不相等同樣 fail-closed。

## 已知邊界

- Mac-only：讀卡走本機 heptabase CLI、canvas 檔住 vault（backend=both）。
- story graph 的正確性責任在撰寫的 agent——這是「理解」不是「解析」；
  讀歪了就改 graph 重渲染。
