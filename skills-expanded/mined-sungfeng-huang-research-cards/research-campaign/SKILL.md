---
name: research-campaign
description: >-
  Scaffold and drive autonomous research-experiment campaigns: a MISSION.md
  brief that lives IN the target repo (runs/auto_research/), a persistent
  experiment ladder (queue.json) and results ledger (ledger.jsonl), hard
  measurement discipline (significance gating, representative eval slices,
  one change per rerun), and research-cards integration (project card
  bootstrap + Op5 gap-analysis pre-read + per-job progress append). Use when
  the user wants to 開/設定一個研究實驗 campaign for a repo, 接續/continue a
  campaign job, or asks campaign 進度/status. This skill owns the FORMAT and
  BOOKKEEPING — the agent executes experiments by following the repo's
  MISSION.md, and hyperparameter decisions defer to an alchemist-playbook
  style source-cited advisor when available.
---

# Research Campaign — 任務書格式＋記帳慣例＋知識庫掛鉤

把「一個 repo 裡的長期自主實驗戰役」標準化：任務書（MISSION.md）進 repo、
狀態（queue/ledger）可斷點續跑、量測紀律硬性把關、進度自動回流知識庫。
**本 skill 不是訓練執行器**——訓練怎麼跑由各 repo 的 MISSION.md 說了算；
這裡管的是格式、記帳、與 research-cards 的接口。

## Files

- `assets/MISSION.template.md` — 任務書模板（八段，含逐段填寫指引）。
- `assets/examples/example-mission.md` — 中性完整範例（Whisper LoRA 領域
  適應 campaign），照抄結構、換掉內容。
- `assets/repo-checklist.md` — **campaign-ready repo 檢查清單**：repo 要有
  哪些元件（可續訓 train 入口、per-utterance CSV 的 eval、顯著性工具、
  manifest 建構器…）campaign 才跑得動；intake 第一步就是對照它。
- `scripts/campaign.py` — 記帳工具（stdlib）：`init`（scaffold）、
  `status`（佇列＋帳本摘要）、`ledger-append`（schema 校驗寫入）、
  `report`（ledger/queue → 靜態 HTML campaign 報告，含指標趨勢圖；順帶
  regen index）、`demo`（manifest → 音檔對聽頁）、`pages-setup`
  （依 git remote 裝 GitHub 或 GitLab Pages 部署設定）、`progress-init`／
  `progress`（訓練 log → SVG 曲線進度儀表）。
- `scripts/progress_page.py` — 進度儀表引擎（stdlib）：log 解析規則全在
  `progress.json`（log_glob＋step_re＋kv_re＋charts 宣告），輸出自包含
  HTML（tiles／2px 曲線＋crosshair tooltip／資料表 fallback／ladder／
  ledger／job 鏈）。
- `assets/pages-workflow.yml` — GitHub Pages 部署 workflow 模板。
- `assets/gitlab-pages.yml` — GitLab CI Pages job 模板（發佈 `public/`）。
- `assets/update-pages.sh.template` — artifact-branch 模式的 repo 端刷新
  腳本模板（`pages-setup --deploy-branch` 生成；flock／無變動不 amend／
  state commit pathspec 隔離）。
- `assets/showcase.css` — **showcase 頁的預設設計系統**（vocodec 風格：
  色票 tokens、.tiles 狀態磚、.card 圖表卡、.chip 徽章、.report-list
  landing 卡、.examples/.audio-grid 對聽卡）。report/index/demo 內嵌它
  （self-contained）；`report` 也會把副本同步到發佈目錄，repo 自製頁
  （訓練儀表板等）`<link rel="stylesheet" href="showcase.css">` 即得同套視覺。

## Mode 1 — Setup（互動式 intake → MISSION.md）

使用者說「幫這個 repo 開一個 campaign」時：

1. **先驗 repo、再勘查、再提問**：先對照 `assets/repo-checklist.md` 檢查
   repo 具不具備 campaign 的必備元件（train --resume／eval 出 per-utterance
   CSV／顯著性工具／manifest 建構器／測試入口）——缺件讓使用者選「先補齊」
   或「列為 E0 前置」。**拆分式佈局（project root 非 repo）再多給一個
   選擇**：(a) 維持拆分——campaign 狀態靠檔案系統＋專案卡當恆久層；
   (b) 升級成 repo——`campaign.py init --git` 會 git init＋依當下目錄生成
   起手 .gitignore（大 artifact 與巢狀 core repo 自動排除、巢狀 repo 維持
   獨立版控），首 commit 留給使用者核可 `git status` 後執行。判準：要
   per-job commit 紀律完整覆蓋 campaign 狀態、或多人協作 → 建議 (b)；
   單人單機、artifact 巨大 → (a) 也夠。然後讀 README／configs／reports，
   能推斷的欄位直接預填草稿。**只問補不齊的**，且一次批量問完
   （AskUserQuestion／一則訊息），不要擠牙膏。最少要確認的欄位：
   - **專案佈局**：整包單一 repo，或 project root（普通目錄）＋核心
     code repo(s)？各路徑為何？（決定 git 步驟作用域與狀態持久化語義，
     見 repo-checklist 的拆分式佈局一節）
   - 目標與研究問題（FIXED GOAL 一段話＋非目標＝防漂移邊界）
   - 基線數字與主指標（現況多少、贏什麼才算贏、副指標護欄）
   - 執行環境（Slurm/local、單 job 牆鐘上限、會不會被搶佔）
   - 實驗 ladder 草案（E0..En 各自的 gate）
   - 過去的失敗模式（要寫進 banned practices——最有價值的一欄）
2. **產出 MISSION 草稿**（照模板八段）給使用者過目核可——草稿必須把
   「哪些是勘查推斷、哪些是使用者說的」標清楚。
3. 核可後落檔：
   ```bash
   python3 scripts/campaign.py init --repo <target-repo> [--rungs E0 E1 …]
   # 然後把核可的 MISSION 內容寫進 <repo>/runs/auto_research/MISSION.md
   ```
4. **Project card bootstrap**：用 research-cards `project-card-log` 的
   resolve/create 流程確認該 repo 有 Heptabase 專案卡（無卡即建＋pin），
   並在卡的現狀段落記 campaign 開跑與 MISSION 位置。

## Mode 2 — Run（接續一個 campaign job）

在目標 repo 的 session（本機或 cluster job）說「接續 campaign」時：

1. 讀 `runs/auto_research/MISSION.md`——它是唯一的任務書，**照它執行**；
   本 skill 只疊加下面的通用紀律與掛鉤。
2. **Step-0 掛鉤（每個 fresh job）**：resolve 專案卡；卡上若有近期 `🔍`
   research-gap 分析（overview-graph Operation 5），先讀——知識庫已覆蓋的
   prior art 不要重新發現。
3. **量測紀律（violating any invalidates the result）**：
   - 代表性 eval 切片（分層抽樣、固定 seed），絕不用 manifest 開頭切片；
   - corpus 級指標，不用 per-utterance 未加權平均；
   - **顯著性 gate**：任何「贏」必須 paired-delta 95% CI 排除 0 才可信；
     基線重評 ≥3 次記錄 eval 非確定性；delta 小於 CI 寬度絕不 promote；
   - 一次只改一件事；架構級變更必 from-scratch，不 warm-start 跨架構；
   - 超參與 schedule 決策引用 alchemist-playbook（或同級有出處的建議），
     把引用寫進 ledger 的 `playbook_rules_cited`。
4. **記帳**：每個完成的評測寫一行 ledger（schema 由工具把關）：
   ```bash
   python3 scripts/campaign.py ledger-append --dir <repo>/runs/auto_research \
     --json '{"experiment":"E1","config_hash":"…",
              "purpose":"本列在驗證什麼（一句話）","metrics":{…},
              "significant":false,"decision":"…","playbook_rules_cited":[…]}'
   ```
   `purpose` 每列都要給——report/progress 頁的「驗證目標」欄靠它區別
   同 rung 的多列（缺值工具會警告；progress 頁不做 rung fallback、直接
   顯示 —）。`decision` 寫成自足敘事（結論＋關鍵數字＋脈絡承接）。
   更新 queue.json 狀態（pending|running|done|failed）。
5. **Step-7 掛鉤（job 收尾）**：code/config/ledger push 之前，若有裝
   showcase 層（Mode 4）先 regen report 一起 commit（觸發 Pages 自動
   重新部署）；push 之後把本 job 的 ledger row＋決策＋下一步，經
   `project-card-log` 的 **`append_card.py`** append 到專案卡
   （`--card` 一律傳 ENTRY 卡 id，script 自己沿續卡鏈走到 tail；
   **絕不用裸 `hb append <id>` 或 `hb log-exp --to <id>`**——那會直寫
   entry 卡，內容錯落在續卡 sentinel 之後）。cluster 走 hb bridge、
   append-only。整併（project-card-merge）與 `🔍` 折疊留在 Mac 端，
   不是 job 的事。
6. 卡住需要人類決策 → 寫 `runs/auto_research/BLOCKED.md` 並停。

## Mode 3 — Status

```bash
python3 scripts/campaign.py status --dir <repo>/runs/auto_research
```
出佇列各狀態計數、最近 ledger 摘要（experiment/significant/decision）、
BLOCKED 提示。回報時把「距離 campaign success gate 還差什麼」講清楚。

## Mode 4 — Showcase（選配，GitHub／GitLab Pages 自動更新展示層）

一次性安裝（依 git remote 自動選軌）：

```bash
python3 scripts/campaign.py pages-setup --repo <repo>   # --host github|gitlab 可覆寫
# github remote → 裝 .github/workflows/pages.yml，報告輸出 docs/
#   （repo Settings → Pages → Source 選 "GitHub Actions"）
# gitlab remote → 裝 .gitlab-ci.yml 的 `pages` job，報告輸出 public/
#   （GitLab Pages 慣例：job 名 pages、artifact 目錄 public/）
# 選擇（host/output_dir/ci_ready）記進 runs/auto_research/pages.json；
# .gitlab-ci.yml 已存在時不覆蓋（印片段請你手動合併，合併完把 pages.json
# 的 ci_ready 改 true）；github workflow 的觸發分支自動改寫成安裝當下分支
```

之後產報告不用再指定 --out（依 pages.json 自動落對的目錄）：

```bash
python3 scripts/campaign.py report --dir <repo>/runs/auto_research
```

**訓練進度儀表（選配，收編 vocodec 的 gen_progress_page 模式）**——把
訓練 log 變成即時曲線頁，與 report 同目錄互連：

```bash
python3 scripts/campaign.py progress-init --dir <repo>/runs/auto_research
# 生成 progress.json 模板（_doc 欄逐項說明）；填三件事：
#   log_glob（如 slurm_logs/*.out）
#   step_re／kv_re（步數與 key=value 指標的 regex——log 格式是 campaign
#     自己的，所以規則放設定不寫死）
#   charts（每張圖一個 y 軸、series ≤4、可畫參考線 refs）
python3 scripts/campaign.py progress --dir <repo>/runs/auto_research
# → <output_dir>/campaign-progress.html（同樣吃 pages.json 落位）
# scheduler:"slurm" 會 best-effort squeue 顯示佇列狀態與 ETA（指令寫死
# 不吃設定，progress.json 不能被用來跑任意指令）；預設 "none" 全離線
```

儀表特性：搶佔重跑的重疊步數以較新 job 為準（逐 key 合併，雜訊行不
清空資料）；曲線抽稀至 ≤700 點、資料存 6 位有效數字（lr=5e-06 這種小
量級存活）；非有限值丟棄；資料表為無滑鼠 fallback（取 step 為
table_every 倍數的列＋最後一列）；輸出對相同輸入位元級確定（無牆鐘
時間戳；頁面含 log mtime＝輸入衍生，跨機器 mtime 不同輸出即不同）。
進階（欄位說明見 progress.json 模板的 `_doc_*`）：`runs`＝多個訓練 run
疊同一張圖（勾選顯示子集，desc/purpose 渲染成 run 總覽表）——**`name`
是人看的顯示名**（圖例/總覽表用，隨時可能被美化改寫）、`short` 是縮寫；
**自動化要定位 run 請比對 `short` 或用 name 前綴**，別對 name 全等比對。
另注意 progress.json 是**人機共用的活設定檔**：程式要修改它必須
read-modify-write 當下的檔案內容，別把記憶體裡的舊快照整檔寫回（會把
並行編輯無聲蓋掉）；`gstep_re`
＋`gstep_scale`／`gstep_native`＝x 軸統一成全域 optimizer step（跨重啟
單調，log_glob 可為 list 把含 ckpt 訊息的 stderr 一併掃入）；
`job_group_re`＝搶佔/重啟的 job 鏈聚合。
進度頁固定連 campaign-report.html——step 7 的 regen 契約本來就是兩頁
一起產，report 缺席時 progress 指令會提示。

**自動更新契約（per-job step 7 的一部分）**：每個 campaign job 收尾時
regen report（有 progress.json 也 regen progress）→ 連同 ledger/queue
一起 commit＋push——push 到部署分支
（github＝安裝時寫定的分支、gitlab＝default branch；實驗分支刻意不觸發）
時 CI 的 paths 過濾即重新部署 Pages，頁面跟著 campaign 自動演進，
不需要另外的排程器。ci_ready=false（CI 檔待手動合併）期間 report 照產，
但不會部署——合併完記得把 pages.json 的 ci_ready 改 true。commit message 慣例：
`Auto-update campaign progress page (session refresh)`。

**Artifact-branch 模式（選配，高頻 regen 的 campaign 用）**：`pages.json`
含 `deploy_branch: "<branch>"` 時，部署契約改為——
- 生成站台住該 **orphan 分支**（單一 commit，每次 regen 後由 repo 內
  `scripts/campaign/update_pages.sh` rsync 到 `.pages-worktree/` →
  `commit --amend` → `push -f`；per-job step 7 呼叫這支腳本），CI rule
  是分支條件（`$CI_COMMIT_BRANCH == "<branch>"`）；**不得**把 output_dir
  內容 commit 到 main。
- main 只收 campaign 狀態（ledger/queue/glossary/progress.json 等）的
  **pathspec-scoped** commit，且僅在內容真變動時——全域 staged 的無關
  內容絕不能被 state commit 吃進去。
- **未設 `deploy_branch` ＝上面的原契約**（default-branch 部署、paths
  過濾），完全向後相容；`report`/`progress` runtime 不感知部署分支
  （它們只寫本地 output_dir），僅 gitignore 誤忽略警告在此模式關閉
  （main 側 ignore 生成物是設計本身）。
- 動機：每小時 regen 的 HTML（內嵌 log mtime、新曲線點）必然天天數十
  commit——放 orphan 分支 amend 後，main 歷史只剩有意義的 commit。

scaffold 一鍵佈置（gitlab；冪等、重跑安全）：

```bash
python3 scripts/campaign.py pages-setup --repo <repo> --deploy-branch pages
# 做的事：orphan 分支（git <2.42 無 worktree add --orphan——以 hash-object/
#   mktree/commit-tree plumbing 建，tree=CI 檔＋既有 output_dir 子樹）、
#   git worktree add .pages-worktree、main 的 .gitignore 補 output_dir/
#   與 .pages-worktree/、git rm -r --cached 解除 main 追蹤（untracking
#   commit 留給使用者）、CI rule 換分支條件、deploy_branch 寫進 pages.json、
#   生成 update 腳本模板（flock 防重疊、site 無變動不 amend、狀態 commit
#   pathspec 隔離——三個都是實戰踩雷後的硬規矩）
```

報告頁自動含：狀態磚、ladder 表（rung 的實驗內容／目標／gate／備註——
取 queue.json 選配欄位 `title`/`goal`/`gate`/`note`）、**ledger 指標圖**
（出現 ≥2 次的數值 metric 一張互動小圖，巢狀 metrics 攤平成 `key.sub`；
x＝ledger 順序、游標懸停顯示 rung 名與精確值；單次數值在 Ledger 表的
指標膠囊可見，不畫孤點）、ledger 全表（metrics 逐項成**指標膠囊**，
滑過即顯示指標說明；「驗證目標」欄＝該列的 `purpose`（step 4 的必填慣例；
缺值的 legacy 列 report 退回所屬 rung 的 title、progress 頁顯示 —），
experiment 名稱滑過可看所屬 rung 的完整內容與 gate）、BLOCKED 橫幅；無時間戳
（輸出確定性，發佈時間交給 git 歷史）。指標說明來自選配的
`runs/auto_research/glossary.json`（`{"指標名": "說明"}`，支援攤平前綴
如 `detail`——campaign 起跑時就把會入帳的指標寫進去，讀者才看得懂）。
report 收尾自動 **regen `index.html`**（landing 頁：掃發佈目錄
所有 \*.html、report 排最前、各頁標題取其 `<title>`；`--no-index` 略過）。

**音檔對聽頁（demo）**——manifest → A/B（多系統）對聽頁；音檔複製進發佈
目錄的**版本化**資產目錄 `assets/<name>-<ver8>/`（換版原子切換、job 被 kill
不留混種頁、舊版自動清）、`<audio preload="none">`（不預載）、產完 regen index：

```bash
python3 scripts/campaign.py demo --dir <repo>/runs/auto_research \
  --manifest demo.json --name ab-listen
# demo.json：{"title":"…","systems":["original","stride1"],
#   "utterances":[{"id":"u1","audio":{"original":"a.wav","stride1":"b.wav"},
#                  "note":"（選填）"}]}   # 音檔路徑相對 manifest 所在目錄
```

訓練曲線儀表（解析訓練 log 畫 loss/step 曲線——參考 vocodec 的
`scripts/gen_progress_page.py`）仍屬各 repo 的 MISSION 資產（log 格式
repo-specific），自行加在同一發佈目錄，index 會自動列進來。**紀律**：
進度頁（ladder＋ledger 全表＋趨勢圖）每 job 誠實刷新，not-significant rows
照登、有徽章標示；受顯著性 gate 管的是對外的「勝出宣稱」與 demo checkpoint
（GUARDRAILS 同款條文）；對聽頁是素材，勝出宣稱以 report 為準。

## 分工界線（防止本 skill 膨脹）

- MISSION 內容（目標/設計/ladder/指令）＝使用者資料，住在各 repo。
- 訓練執行、sbatch 包裝、續投＝MISSION 的 per-job procedure 管，agent 照做。
- 本 skill 永遠只有：模板＋intake 合約＋記帳工具＋量測紀律＋KB 掛鉤。
