---
name: overview-graph
description: >-
  Maintain the study/overview knowledge graph in Heptabase: the hierarchy (📚 root
  index → topic hubs → comparison cards, Level property = tree depth), the lateral
  edges (相關主題（橫向連結） mention sections, ↔/→ direction semantics), the
  knowledge-map whiteboard, hub creation, and hung-yi-lee narrative-act card
  re-splits when a card nears the 100K cap or its taxonomy stops matching the
  story. Use when the user asks to 新增/調整 hub、拆卡/重分 overview、加/改 graph
  邊 or 橫向連結、調 Level/目錄/知識地圖 whiteboard、或稽核 knowledge graph 一致性.
allowed-tools: Bash(heptabase *) Bash(python3 *)
---

# Overview Knowledge Graph — Maintenance Skill

## Backend

`heptabase`/`both`：原路徑不變（whiteboard、tag、UUID）。`obsidian`：四支 scripts 全部
支援——卡片 id 用 `Folder/Name`；**知識地圖對應 Obsidian Canvas**（config
`obsidian.graph.canvas`，JSON Canvas 格式）：工具只「加缺少的檔案節點」到畫布下方的
暫存區，**永不移動使用者手動排好的節點**（與 Heptabase whiteboard 的人工策展分工相同：
腳本管帳、人管圖）。`make_hub`/`resplit` 建新卡時自動補 canvas 節點（等同原本手動
`whiteboard add-card` 那步）。`audit_graph` 檢查對應：Level→frontmatter `level`、根目錄
覆蓋→`obsidian.graph.root_card`、whiteboard 成員→canvas 檔案節點（`canvas_optional`
豁免清單）、↔ 鏡像照常；topology snapshot 檢查為 heptabase 專屬（跳過並註明）。

The `study/overview` cards form a **knowledge graph**: a navigation **tree**
(spine) plus **lateral edges** (cross-links). This skill owns structural changes;
per-card content is owned by the unified `overview` skill (topics/<key>.md docs) and `overview-daodu`.

```
L1 📚 目錄 (nested-bullet hierarchy of everything)
L2 topic hubs（幕次脈絡 narrative → 子卡）＋術語卡
L3 comparison cards ＋ sub-hubs（e.g. 聽覺理解・推理＝Spoken 主題的聽覺翼）
L4 cards under a sub-hub
＋ lateral edges: 相關主題（橫向連結） sections, rendered as whiteboard lines
```

## Key IDs

| thing | id |
|-------|----|
| overview tag | config `heptabase.collections.overviews.tag_id` |
| `Level` property (select, options 0–4) | config `heptabase.graph.level_prop` |
| 📚 root index | config `heptabase.graph.root_card` |
| knowledge-map whiteboard | config `heptabase.graph.whiteboard` |
| hubs: Tokenizer / Spoken / Duplex / 聽覺翼(sub) | （config） / （config） / （config） / （config） |

Overview cards carry `study/overview` ONLY (never `study/paper`). New-card
checklist: tag + Level + root-index bullet + `whiteboard add-card`.

## Invariants (audit enforces these)

```bash
python3 scripts/audit_graph.py    # exit 0 = consistent（含 topology snapshot staleness）
```
1. every member has a Level; 2. root index mentions every member exactly (and
nothing else); 3. every member is on the whiteboard; 4. every `↔` lateral edge
has its mirror on the target card; 5. every registered skill's `topic_snapshot.json` matches a fresh
graph derivation (`_shared/topology.py check`). Run after ANY structural change, and when a
parallel session may have touched cards.

**After ANY structural operation (hub add/re-split/adopt/re-home/edge changes affecting 子卡 lists):**
run `python3 ../_shared/topology.py refresh` so the sync skills' graph-derived snapshots follow, then the audit.
**Hub format is an API**: the 「子卡與閱讀順序」 section (one mention per bullet, sub-hub bullets nested)
is parsed by topology.py — keep that structure when editing hubs.

**Authority direction（單向，不可倒灌）**: graph 決定結構（hub 樹）→ `topology.py`
派生（own_cards／sub_topics／kind／task_values）→ topic 對齊；registry（`TOPICS`）
只保存 key↔anchor 身分與不可派生的 ALIASES／散文（topics/<key>.md、config.py 的
內容設定）。結構永遠改在 Heptabase 的 hub 卡上，refresh 讓 code 跟上——不要在
code 裡硬編 kind、parentage 或 include/exclude 來「修」結構（e.g. 把聽覺翼 sub-hub
bullet 移出 Spoken hub，refresh 後 `auditory` 自動變頂層 topic，零 code 改動）。

## Operation 1 — Add a hub

**When**: a topic grows to ≥2 cards, or several cards turn out to share one
punchline (e.g. AU/Reasoning/E all asked 真聽 vs 讀 → 聽覺翼 hub).

1. Author the hub with `scripts/make_hub.py <spec.json>` (creates card, real
   mentions, tags study/overview). Hub content = hung-yi-lee **主題導覽**, NOT a
   lecture: topic punchline → why it splits into these sub-cards (幕次) → 建議
   閱讀順序 → 子卡與閱讀順序 bullets → 相關主題. Ground every claim in the
   sub-cards' 導讀 (extract lean via `note read`, don't load full cards).
2. Set Level; demote sub-cards' Levels if the hub inserts a layer.
3. Root index: nest the sub-cards' bullets under the hub bullet (3-deep nesting
   works — child `bullet_list_item` inside the parent's `content`).
4. `whiteboard add-card` the hub; run the audit.
5. **If the hub is a NEW TOPIC** (it owns Tasks values of its own): set them on
   the hub's Tasks property, register the anchor in `_shared/topology.py`
   `TOPICS` (key↔anchor only — kind/parentage/include are all derived), create
   `overview/topics/<key>/config.py` + write `overview/topics/<key>.md`, add
   the scholar-inbox routing, then `topology.py refresh`. (`topology.py check`
   flags unowned Tasks values if you forget.)

A hub may be a **sub-hub** under another topic (the hierarchy is a DAG in
spirit): keep the parent hub's bullet pointing at the sub-hub, and say so in
both narratives (e.g. 聽覺翼＝Spoken 主題的 Audio LM 那塊). If the sub-hub is
itself a registered topic, `refresh` NESTS it automatically (parent snapshot's
`sub_topics`; `sync_overview.py <parent> status|sort` runs the subtree) — the
parent topic doc then routes to the sub-topic delegatively, never naming its
cards.

## Operation 2 — Re-split cards along hung-yi-lee 脈絡

**When**: a card nears the **~100K char cap** (check before adding papers), or
its taxonomy stops matching the narrative acts.

1. **Proposal first** (get user approval): the topic's acts (問題→撞牆→下一幕
   genealogy), per-paper destination table (papers may live in MULTIPLE cards by
   facet), which cards survive/rename/dissolve, sync-config impact, honest cost.
   Prefer act boundaries that minimise moves (an act = an existing paradigm
   group is the cheap split line).
2. **Mechanical move** with `scripts/resplit.py <plan.json> [--dry-run]`:
   backs up every touched card (`~/.cache/overview-resplit/<ts>/`), creates
   skeleton cards (tagged), moves L3 sections + dimension rows, retitles.
   ALWAYS dry-run first — every heading key must resolve to exactly 1 match.
3. **Narrative pass per card** (parallel forks): intro cross-refs, paradigm
   table regroup, synthesis cleanup, dup sections, fresh 導讀 via
   `overview-daodu`. Cards whose punchline moved get a NEW 導讀, not a reuse.
4. **Follow-through**: update the hub 子卡 list, root index, Levels,
   `whiteboard add-card`; **re-home any 相關主題（橫向連結） bullets living on a
   dissolved/split card**; then `python3 ../_shared/topology.py refresh` — the
   sync skills' own_cards/MATCH/task_values are graph-derived snapshots now (no
   CARDS transcription; MATCH auto-generates from section mentions' arxiv
   property — only add an ALIAS in topology.py for new short-name variants or
   non-arxiv papers); **rewrite the topic doc's routing rules**
   (`overview/topics/<key>.md`) — the routing prose is a byproduct of the new
   acts, so the MODEL re-authors it from the act design (hung-yi-lee voice) as
   part of every re-split, never hand-patched later; keep chains DELEGATIVE
   (a parent topic routes 「聽覺理解類 → auditory」 and stops — it never names a
   sub-topic's cards; the sub-topic's own doc decides); run
   `overview/sync_overview.py <topic> status` + `sort` + this skill's audit.

## Operation 3 — Adjust lateral edges

**Edge criteria** (all must hold): the relation is **verified in live card
content** (shared papers / shared 判準 / 方法↔評測 pairing — check the actual L3
lists before asserting; never from memory), and it crosses tree branches (intra-
hub siblings don't need edges — the hub covers them).

**Direction semantics**: `↔` mutual facets (write BOTH ends), `→` deep-dive
pointer (source end only). Put the semantics in the label text:
「↔ 同 7 篇論文的全雙工工程面（本卡看原生 LM 演化面）」.

```bash
python3 scripts/add_edges.py edges.json --dry-run   # then run for real
```
Idempotent — reruns only add missing bullets. Edges live in a trailing H2
「相關主題（橫向連結）」 section, which `sort` and `insert_daodu` never touch.
The whiteboard draws them automatically with 顯示 mention link on.

**Removing/moving an edge**: edit the section by hand (note read/save); then
audit (it will flag a missing `↔` mirror if you only removed one end).

## Operation 4 — Export the graph into hung-yi-lee (Direction A)

TWO collections feed the hung-yi-lee knowledge graph as external corpora
(members enumerated live — counts never hardcoded): **study/overview** →
`heptabase-overview/` (the topic/hub layer — plays the role wiki topics play
for lectures) and **study/paper** → `heptabase-papers/` (the leaf layer —
the card analogue of video nodes):

```bash
python3 scripts/hungyi_query.py "<question>"   # everyday entry: freshness + graph query
python3 scripts/export_hungyi_corpus.py --if-stale --build   # card freshness alone
# --backend heptabase|obsidian overrides the config backend (default:
# config's backend; `both` reads from heptabase as source of truth)
```

`hungyi_query.py` query mode deliberately does NOT sync lecture data (network
-heavy, dirties the fork tree) — the scholar-inbox desktop routine's closing
step (`hungyi_query.py --refresh-only`, TTL-throttled 24h) owns that, and the
routine session commits the fork afterwards. The card-side freshness is cheap
enough to run **before every `graph query`**:
member scans skip everything when nothing changed; pure content edits
rewrite ONLY the changed/new/missing docs (incremental); membership or
title changes trigger a full re-export (titles + `links:` resolve across
docs). Card-to-card links inside exported members land in each doc's
`links:` frontmatter — the graph builder turns them into **EXTRACTED
`links_to` edges** (overview card → its papers, paper → paper). Trashed
cards lingering in the tag index are skipped and remembered (retried when
their ts changes). Then `graph build --external` runs only when the local
graph is older than the corpus or the tracked lecture graph. Outputs land
in the skill's gitignored `wiki/graph/*.local.*` overlay — `graph query`
auto-prefers it and tags card nodes with provenance
(`heptabase_overview_card/overview`, `heptabase_paper_card/papers`). Every
REBUILD ends with a condensed `[alignment]` notice (top suggest_alignments.py
candidates) so alignment drift surfaces as soon as new data lands — the
merge-vs-align call stays human; edit `graph_alignment.json` and re-run.

## Operation 6 — Mirror a whiteboard into an Obsidian Canvas（單向）

把 Heptabase whiteboard 的實際版面（卡片座標/顏色/摺疊、section 分區、
連線）鏡像成 vault 裡的 JSON Canvas。版面以 Heptabase 為準——每次執行
整檔覆寫，鏡像出的 canvas 不要手排。

```bash
cd "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/overview-graph/scripts"
python3 whiteboard2canvas.py                 # config 登記的全部 whiteboard
python3 whiteboard2canvas.py --dry-run       # 只出報告不寫檔
python3 whiteboard2canvas.py --whiteboard <id> --all-data <path>
```

- 資料來源（預設順位：live → 備份）：
  1. **live**：桌面 app 自己的 SQLite（`hepta.db`，預設
     `~/Library/Application Support/project-meta`，可用 config
     `heptabase.app_data_dir` 或 `--live-db` 覆蓋）——用 SQLite backup API
     取一致性快照，app 開著也能跑，資料即時。schema 無文件：表／欄位有
     明確檢查，app 改版對不上會直接報錯並提示改用備份。
  2. **備份**：Heptabase「Export all data」的 All-Data.json——config
     `heptabase.backup_dir`（自動撿最新）或 `--all-data` 直接給；備份超過
     7 天會出提醒。live 讀不到時自動退回這裡。
- 鏡像對象：config `obsidian.graph.mirror_whiteboards`
  `{"<whiteboard-id>": "<vault 相對路徑>.canvas"}`。
- 已同步的卡 → `file` 節點（借 heptabase-sync 的 state 解析 vault 路徑）；
  未同步的卡 → 帶 Heptabase 連結的 `text` 節點（報告列在
  `unsynced_cards`）；浮動文字 → `text`（PM→md）；section → `group`；
  連線 → edge（sides/顏色/label 對應；mindmap/媒體等不支援的物件計入
  `skipped_unsupported`）。
- **Mention 線**（Heptabase 自動畫的卡片互相 mention 連線）也會重現：
  掃板上每張卡的內文 mention（`{"type":"card"}` 節點），兩端都在板上就
  畫 edge——互相 mention 收斂成一條雙箭頭、與 explicit connection 重複的
  pair 不重畫。關閉：config `obsidian.graph.mirror_mention_edges: false`。

## Operation 5 — Research-gap analysis for a project card (Direction A 應用)

**When**: the user asks 找研究漏洞 / gap 分析 / 方向發想 for a Research-Projects
card (the ones project-card-log accumulates and project-card-merge consolidates).

Two stages — structure finds candidates, the model makes the judgment:

1. **Structural candidates**:
   ```bash
   python3 scripts/research_gaps.py <project-card-id> [--top 15]
   ```
   Three sections: **(c)** uncited papers by log-damped concept overlap (the
   card's concepts are extracted with the hung-yi-lee extractor + a reverse
   vocabulary match against graph labels, so ids line up); **(c2)** the
   top-matching overview cards' shelves (links_to papers the project doesn't
   cite) — the TOPICAL channel for papers whose relevance raw lexical overlap
   can't see; **(a)** distance-2 concepts everyone around the project handles
   but the card never mentions. Class (b) cross-community bridges is
   deliberately absent — the pilot found it drowned in god nodes; redesign
   (document-level bridges / links_to endpoints) before adding it.
2. **Model judgment pass**: read the project card + the candidates, verify
   each candidate against live card content (grounding rules below), then
   write the gap analysis — 漏洞 with evidence + severity/confidence, 發想 in
   hung-yi-lee 問題→撞牆→怎麼辦呢 genealogy — and **append** it to the project
   card as a dated `## 🔍 研究漏洞與方向發想（YYYY-MM-DD…）` section.
   Append through the overflow-safe helper, NOT a raw `heptabase note append`:
   ```bash
   python3 ../project-card-log/append_card.py --card <ENTRY_ID> --content-file gap.md
   ```
   It follows project-card-log's append-only convention, walks any
   continuation chain to the tail（a raw append would land mid-chain on a
   chained card）, and near the size cap spills to a new 續卡 when
   `projects.overflow_spill` is enabled instead of overflowing. The
   append always lands at the chain TAIL; the next `project-card-merge` run
   folds it into the body after Findings (its arc item 6.5), promoting
   actionable 發想 into 下一步 and verification-type 洞 into 待補 — the `🔍`
   heading prefix must survive the fold (it is research_gaps.py's
   extraction-exclusion contract, position-independent). Distinguish provenance throughout:
   筆記側 (external cards) vs 課程側, evidence vs speculation.

Pilot reference: the 2026-07-06 Causal Audio Tokenizer analysis on card
（config） (5 gaps + 4 directions; validated this workflow).

## hung-yi-lee grounding rules (apply to ALL narrative writing here)

- 脈絡 not 流水帳: hubs/導讀 weave ONE evolution thread; tables do the listing.
- One punchline per topic/card; genealogy (怎麼辦呢) drives each act.
- **Grounded-only**: verify paper overlap/claims against live cards; a directive
  or memory may be stale (this playbook once claimed an overlap that wasn't
  there — the fork checked and dropped it. Do that.).
- Cross-card duplication rule: if a card's 導讀/歸納 mentions or compares a
  paper, that card carries a full hung-yi-lee-style section for it, cross-ref'd
  to the main-facet card. In-section incidental citations do NOT trigger this.

## Concurrency & safety

`note save` uses contentMd5 optimistic locking — parallel sessions can't
silently clobber, but content added AFTER your read won't be in tables/導讀:
re-read before narrative passes and run the audit after. Backups: resplit
(`~/.cache/overview-resplit/`), 導讀 (`~/.cache/overview-daodu/`; restore via
`insert_daodu.py --restore`).

Gold references: 聽覺翼 sub-hub （config hubs）（hub 兼 sub-hub）、Spoken A→A1/A2
split（size-cap 拆卡）、tokenizer 3→6 re-split（脈絡重分）。Related skills:
`overview-daodu` (導讀), the unified `overview` skill (per-topic sync;
`sync_overview.py <topic> status|sort`), and
[[hung-yi-lee]] (voice).
