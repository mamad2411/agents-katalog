---
name: project-card-merge
description: >-
  Consolidate a Heptabase research-project card on the Mac into a STANDALONE full report for the project lead (前情提要 + evolution story + current state — readable without session memory): fold the cluster's
  append-only `📥 cluster 補充/進度` blocks (and any `📝 待補成 paper 級參考`
  brief) into ONE focused, paper-grade, coherent card — update 現狀 to the latest
  state, supersede stale info, keep all paper-grade detail + figures + file
  citations + card-links, and remove the dated append shells. Also folds
  tail-appended `🔍` research-gap analysis sections (from overview-graph
  Operation 5) into the body after Findings, promoting actionable 發想 into
  下一步 and verification-type 洞 into 待補. Chain-aware: collapses a
  continuation chain (entry→續卡, from append-side overflow) back into the
  merge, and when the merged result itself exceeds the card cap it spills
  whole sections into a fresh chain instead of condensing (finalize_chain) —
  paper-grade content is never trimmed to fit 100K. This is the Mac-only
  "final merge" that pairs with the cluster-side append-only `project-card-log`.
  Use when the user says 整理/合併 project 卡, merge cluster progress, consolidate
  the Research-Projects cards, or update a project card for paper writing.
allowed-tools: Bash(heptabase *) Bash(python3 *) Read
---

# Project Card Merge — consolidate cluster-appended progress (Mac-side)

## Backend

卡片讀寫經由 rewrite_lib 路由（obsidian 模式可用），但 Research-Projects hub 的 card id
為 Heptabase UUID——obsidian 模式需改用 vault 內對應卡的 id。主要工作流仍以 heptabase/both 為準。

The cluster session appends dated `📥 cluster 補充/進度 YYYY-MM-DD` blocks to a
project card via the `hb` bridge (append-only — it cannot overwrite). This skill
is the **Mac-side counterpart**: it merges those blocks (and any leftover
`📝 待補成 paper 級參考` brief) back into one coherent, focused, paper-reference-grade
card. Three-layer principle (same as the cards already follow):
**card = synthesis + 發想; raw logs stay in the codebase; keep paper-grade detail but no append sprawl.**

Mechanics live in `card-rewrite`'s `rewrite_lib` (builders + `finalize`); this
skill's `merge_lib` adds the Research-Projects index, a merge-readiness scan, and
a table builder.

```python
import sys, os; sys.path.insert(0, os.environ.get("CLAUDE_PLUGIN_ROOT", os.path.expanduser("~/.claude/skills/research-cards")) + "/skills/project-card-merge")
import merge_lib as M           # M.L is rewrite_lib
```

## Step 1 — Pick the target card(s)
```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/project-card-merge/merge_lib.py          # list project cards + which NEED MERGE
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/project-card-merge/merge_lib.py <cardId> # scan one (appended blocks, brief, size, figs)
```
- If the user named a card, use it. Else show the list and act on the ones flagged **NEEDS MERGE** (or ask which).
- If `needs_merge` is false → already consolidated; report and skip（a clean
  chain counts as consolidated — see below）.
- The scan is **chain-aware**: `chain` lists `entry→續1→…→tail`（append 溢位或上次
  merge spill 產生）——a CLEAN chain is a consolidated state and does NOT flag
  by itself; what flags NEEDS MERGE is markers anywhere on the chain, `orphans`
  （`… · 續 N` children with a 母卡 back-ref that no card links to）, or a
  `chain_error`（cycle／斷鏈／超長）.

## Step 2 — Read the WHOLE card (the whole CHAIN)
```python
SCAN = M.scan(CID)                        # from Step 1（chain/orphans/markers）
READS = M.chain_dumps(CID)                # [(card_id, md5, dump)] — ONE read pass
MD5S = {cid: m for cid, m, _ in READS}    # ★ optimistic-lock 基準：Step 4/5 都用它
CHAIN = [cid for cid, _, _ in READS]
imgs = []
for cid, _m, dump in READS:
    print(f"===== {cid} =====\n{dump}")
    imgs += M.L.extract_images(M.L.read_card(cid)[1])   # figures from EVERY card
    # （此處重讀僅取圖，非鎖基準——基準永遠是 READS 的 md5）
for oid, _t in SCAN["orphans"]:           # orphans: ONE read → md5 基準+dump+figures
    if oid in CHAIN:                      # scan 之後才被鏈入 → 已在 READS，跳過
        continue
    omd5, odoc = M.L.read_card(oid)
    MD5S[oid] = omd5                      # ★ 沒有基準的卡 cleanup 會拒絕 trash
    print(M.L.doc_dump(odoc))
    imgs += M.L.extract_images(odoc)
```
`card_dump` renders every node type（tables `| … |`、card-links `[[card:<id>]]`、
code blocks、lists、blockquotes——未知型別也會以 `[type]` 現形）; anything it
surfaces must survive the rebuild. Figures live in the PM doc, not the dump —
that's why `extract_images` must run over EVERY chain card, not just the entry.
`card_dump` surfaces tables as `| … |` rows and card-links as `[[card:<id>]]` —
**note every table and card-link; the rebuild does NOT auto-carry them**. Recreate
tables with `M.table([...])` and card-links with `M.cardlink("<id>")` in Step 4
(they were the exact things a naive read would drop).
Read the existing main sections AND every `📥` block fully — the appended blocks
hold the newest 現狀, corrected facts (`更正先前理解`), full numbers/tables, and
file citations. Do not skim.

Chain semantics for the merge input: a child's content = its dump **minus the
auto-header**（`# … · 續 N` 標題＋`母卡：…` back-ref 行）and **minus the `▶ 續卡…`
sentinel links** — treat what remains exactly like `📥` blocks that happen to
live on another card. (`M.child_payload(doc, ENTRY_ID)` does this strip at the
PM level if you need the nodes; the dumps above are for reading.)

## Step 3 — Merge into one focused structure
Rebuild a single coherent card (adapt section names to the project; the two
existing cards use this arc):

**讀者設定（hard rule，同 log 卡總綱）**：merged 卡＝一份**完整報告**，
讀者是單獨打開這張卡的專案主持人／mentor——不靠 session 記憶、不用
回翻 log 卡，就能理解專案的整體狀況與進度。無縮寫規則同 log 卡：盡量避免；
代號首現必展開，整卡反覆使用的代號集中在「定位與前情提要」末尾的
小詞彙表定義。

1. **定位與前情提要** — 完整報告的開場，三件事：
   (a) **專案一句話**：目標＋為什麼重要（動機——讀者記得大方向、
   不記得細節）；
   (b) **演進故事**（3–6 句，敘事線不是列點，同 overview 卡導讀的
   寫法）：從起點到現在走過哪幾個階段、每階段的關鍵結論——單獨看
   這段就知道專案怎麼走到今天；
   (c) Codebase + 權威紀錄（codebase docs / wandb）+ 母題/子題 card-link.
2. **現狀（一眼掌握）** — **rewrite to the LATEST state** from the newest `📥` block
   (supersede the old 現狀; note 資料事件/blockers if any).
3. **進展里程碑（已完成）** — fold in newly-completed milestones (infra changes, runs finished).
4. **方法 / Method** — fold appended Method detail (architecture, dims, mechanisms)
   into the main method section; **keep file citations** (`path:line`) and bilingual terms.
5. **實驗統整 / Results** — fold appended numbers/tables; keep the ablation table
   (use `M.table([...])`), eval protocol, and key metrics verbatim.
6. **Findings / 關鍵發現** — fold new insights (supersede/extend earlier ones).
6.5. **`## 🔍 研究漏洞與發想`** — fold the dated `🔍` analysis section(s) the
   research_gaps workflow (overview-graph Operation 5) appends at the card
   TAIL into this position (after Findings, before 下一步):
   - **The `🔍` heading prefix is a HARD CONTRACT** — `research_gaps.py`
     excludes these sections from concept extraction by the prefix
     (position-independent). Keep it. Recommended folded title:
     `🔍 研究漏洞與發想`; move the analysis date to a light line inside the
     section (or per-item `（YYYY-MM-DD）` tags when multiple analyses merge).
   - Multiple dated analysis sections merge into ONE: 洞/發想 resolved by
     later progress are removed (same supersede principle as `📥`); still-open
     ones stay, lightly dated.
6.7. **log 卡蒸餾（log-as-card 時間線，0.37.0 起）** — `scan` 的
   `pending_logs`＝鏈尾 `📎 date [[log卡]] 摘要` 行（尚未蒸餾）：
   - **逐張讀 log 卡**（`L.read_card(<log id>)`）——它們是 self-contained
     的蒸餾素材，地位同 `📥` blocks：結果/數字進實驗統整、意義進
     Findings、待裁決進下一步（同 supersede 原則）。
   - **log 卡本身不 trash**：它是一等歷史記錄，永久保留。
   - **時間線＝永久記錄，link 絕不能丟**：重建時用
     `M.timeline_section(done_logs + 剛蒸餾的 pending_logs)` 在卡尾
     （待補之後）生成 `## 📜 log 時間線` 區——每行 `📗 date [[log卡]] 摘要`
     （真 card node）。`📎`（未蒸餾）→`📗`（已蒸餾）的標記轉換就是
     「分辨新舊」的機制：merge 後新 append 的 `📎` 行自然落在時間線區
     之後的卡尾，下輪 scan 再收。
7. **計畫 / 下一步 + 發想** — update; drop items the new progress resolved.
   **下一步只放「還沒做的事」（hard rule，2026-07-18 教訓）**：
   - 已完成項**不留殼**——連「✅ 已完成」行都不留：其內容的歸宿是 現狀／
     進展里程碑／實驗統整，下一步直接刪項（被取代的舊裁決/舊交付路線同理）。
   - 活項目**不累積進度尾巴**——每輪 merge 把該項重寫成「當前待辦狀態」
     （一項 1–3 句，細節用「見實驗統整（N）/現狀」指回），歷程屬於 現狀
     與 實驗統整，不屬於 下一步。
   - 膨脹判準：一個 下一步 項目裡出現日期串（07-16：…07-17：…）、✅、或
     超過 ~4 句，就是該收的訊號。實案：A 卡 E8 項曾累積成 ~1400 字連載
     （四輪 merge 的尾巴），重寫後 10 條 4.6K 字 → 7 條 1.2K 字。
   **Promote actionable 發想 from the `🔍` section** into 下一步 as one-line
   items with a back-ref（`（← 發想 N）`）— the full argument stays in the
   `🔍` section; dedupe against existing 下一步 items (an existing item that
   matches a 發想 merges into one entry, keeping the back-ref).
8. **已知未解 / 待補·仍待確認** — keep genuinely-open items (offline baseline, figures, bugs).
   **Verification-type 洞**（missing metrics, unexamined interactions, facts
   to confirm）become 待補 entries with a back-ref（`（← 洞 N）`）; if an
   existing 待補 entry already states what a 洞 re-raises, just back-ref it
   instead of duplicating.
9. **參考** — CarelessWhisper-style links, **preserved figures**, Source/原文 links.

Rules:
- **Supersede, don't duplicate** — when a `📥` block corrects/updates an earlier
  fact (e.g. `start_idx` meaning, current step, v10→v11 status), the merged card
  carries only the corrected/latest version.
- **Remove the shells** — after folding, the `📥 cluster …` H2 blocks and any
  satisfied `📝 待補成 paper 級參考` brief must be gone (their *content* lives on
  in the main sections; only the dated wrapper is dropped).
- **Preserve**: every figure (`M.L.extract_images` → re-insert via `M.L.img`),
  every card-link (母題/子題), Source/原文 links, file-path citations, exact numbers.
- **Don't lose paper-grade depth** — this is a paper-reference card; fold detail,
  don't summarize it away.

## Step 4 — Rebuild + finalize_chain
Build `C=[]` with `M.L.add(C, …)` and the builders (`M.L.h/pp/bul/bp/img/hr/source`,
`M.cardlink`, `M.table`). Then colorize + size-check + save in one call:
```python
COLOR = [("最佳","green"),("SOTA","green"), ("尚未","red"),("bug","red"), ("v11","yellow"), ...]
print(M.finalize_chain(CID, MD5S[CID], C, COLOR))   # [(card_id, size), …]
```
**md5 一定用 Step 2 讀取時的 `MD5S[CID]`，不要在這裡重讀**——重讀會拿到新
token，把 rebuild 期間落地的 append 靜默蓋掉；用舊基準，有新內容就會被
optimistic lock 擋下（重讀整條鏈再重跑）。
`finalize_chain` runs the same colorize→figure-shrink pipeline as `finalize`,
but a project card is **never trimmed to fit the 100K cap**: an over-threshold
result spills whole H2 sections into a fresh continuation chain（entry 留前段
＋`▶ 續卡…` sentinel link；子卡自帶 auto-header＋母卡 back-ref＋tag）。**Do NOT
condense paper-grade content to dodge the cap** — that's exactly what the chain
is for. `dry_run=True` prints the split plan without writing.
- Crash-safe order: children are created and tagged BEFORE the entry is saved —
  a failure can only leave discoverable orphans, never lost content.
- 若切出來的段落結構上更適合「主題拆卡」（人類可讀的 taxonomy split），可改走
  overview-graph 的 resplit（narrative-act 拆卡）——chain 是無損預設，resplit
  是更好讀的選項；先問使用者再動 resplit。

## Step 5 — Clean up absorbed children + verify
```python
OLD_CHILD_IDS = CHAIN[1:] + [oid for oid, _t in SCAN["orphans"]]
M.cleanup_children(OLD_CHILD_IDS, md5s=MD5S)   # tag 補齊後移入垃圾桶
```
`md5s=MD5S` 是安全網：merge 期間若有新 append 落到某張舊續卡（cluster append
走鏈 tail！），該卡 md5 已變 → **不會被 trash**，保留為孤兒等下一輪 merge。
⚠️ **殘餘競態（操作面防線）**：md5 驗證與 trash 之間仍有毫秒級窗口（CLI 無
條件式 trash），落在其間的 append 會隨卡進垃圾桶（軟刪除、可還原）。所以
**merge 只在 cluster 沒有進行中的 campaign job／append 時跑**——開跑前先看
佇列（squeue）或跟使用者確認，不確定就不 cleanup（children 留著無害）。
```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/project-card-merge/merge_lib.py <cardId>   # needs_merge should be false now
```
Confirm: no `📥`/`待補成 paper` headings remain, no `🔍` section left AFTER the
下一步/計畫 headings (folded position = after Findings), the `🔍` heading
prefix survived, figures + card-links intact; **old** children trashed;
`needs_merge` false. A fresh chain from `finalize_chain` is a consolidated
state — scan lists it informationally but does NOT flag it（只有鏈上再出現
📥/brief/🔍、孤兒、或 `chain_error` 才需要下一輪 merge）。
Report what was folded, what was superseded, the chain layout（if any）, and
remaining 待補 items.

## Step 5.2 — 自動收斂 repair → note-sync → 全視圖（硬規則）

```bash
python3 <plugin 的 skills/project-card-log 目錄>/post_project_sync.py \
  --card <ENTRY_ID>
```

只在 Step 5 的 child cleanup＋verify 完成後呼叫。runner 與 cluster
project-log drain **共用同一條實作**，固定依序：
**repair_chain --seal → pinpoint project-card-repair → 一次 note-sync →
timeline canvas → 裸跑 context mind map**；若既有 mind map 是 story 且
coverage 有缺口，再進 `story_auto_expand.py` 的 guarded proposal 流程。
merge 動了整條鏈（entry 重建、子卡 trash、📎→📗 翻轉），所以 repair
與 sync 都必須先於視圖；順序反了會把未鏡像節點、trash 殘影或斷 link
畫進圖。任何一步失敗、note-sync conflict、canvas coverage 不完整都以
非零退出，修好後重跑同一指令（全流程 idempotent）。

Heptabase-only、沒有 local hub 時仍完成 repair，並略過不可用的
note-sync／canvas；`--dry-run` 可先看完整 command plan。merge 後蒸餾狀態
的翻轉會同輪反映在 timeline 拓撲：entry（HEAD）側貼最新已蒸餾 log，
HEAD 上方的 📎 backlog 清空。

## Notes
- This skill **only consolidates an existing card** — it does not invent content.
  Everything comes from the card's own `📥` blocks (which the cluster grounded in
  the codebase). If a `📥` block says `（待確認）`, keep it as 待補.
- Pairs with cluster-side **`project-card-log`** (append) — see
  [[heptabase-cluster-bridge]]. Per the user's rule, cluster appends; Mac merges.
- **Continuation-chain contract**（`../project-card-log/CARD-OVERFLOW.md`）:
  sentinel＝`▶ **續卡（本卡已達容量上限）**：[[card:<id>]]`（`append_card.LINK_MARK`）；
  marker/registry 永遠指 ENTRY。Append 側（cluster）滿了建續卡；merge 側（這裡）
  收鏈重排，重排完超限再 spill 成新鏈。Idempotent：無鏈無 📥 的卡重跑 merge 是
  no-op。**Enablement**：config `projects.overflow_spill` 必須在本 skill 的
  chain-aware 版上線後才開（已達成）。
- **Closed loop with research_gaps (overview-graph Operation 5)**: its analysis
  section always APPENDS at the card tail (dated, `🔍`-prefixed); the next
  merge folds it into the body after Findings (arc item 6.5) and refreshes
  下一步/待補 accordingly. Append 落尾、merge 折進正文——same rhythm as `📥`.
- Project cards are the card mentions on the Research-Projects hub
  (config `heptabase.collections.projects.hub_card`); list them via
  `merge_lib.list_project_cards()`.
