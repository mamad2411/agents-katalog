---
name: card-rewrite
description: >-
  Rewrite a Heptabase paper card into the "teaching-style" format — written to
  onboard the reader configured at config profile.reader — assumed NOT an expert in that paper's subfield:
  a one-line essence + why-you-should-read framing, a 先備知識 glossary that
  defines the jargon in plain language, teaching prose that explains the WHY (not
  just the what), bilingual terms (English kept alongside Chinese), a filled-in
  快速摘要, preserved figures, and re-applied colorization. Use when the user asks
  to rewrite / 重寫 / 教學式 / upgrade a paper card, or to retrofit existing cards
  in batches. The gold reference is the card configured at config `gold_cards.card_rewrite`（未設定時以本 skill 的 teaching_spec.md 為準）.
allowed-tools: Bash(heptabase *) Bash(python3 *) mcp__alphaxiv__get_paper_content Task
---

# Card Rewrite — Teaching-Style Paper Cards

## Agent（claude / codex）

兩個 agent 皆可駕駛（Codex 端：`research-cards@private-plugins` plugin 的 card-rewrite skill）。alphaXiv MCP 的
grounding 僅 Claude 有；Codex 駕駛時以卡片現有內容＋arxiv HTML 抓取為準。

## Backend

`heptabase`/`both`：原路徑不變。`obsidian`：`read_card`/`save_card`/`list_todo` 走 vault
（PM doc 為共用記憶體模型，markdown 方言承載顏色/toggle，重寫與上色流程不變）。

Turns a terse "translated report" card into one that **teaches an unfamiliar
reader**. The single source of truth for the style + the easy-to-drop mechanics
(preserve figures, re-colorize, fit 100k). `scholar-inbox-clip` and the overview
skills reference this style; this skill owns it and drives batch retrofits.

**Core principle:** the card's #1 job is to let someone who does *not* know the
subfield absorb the paper fast. Simplifying reduces load, but **over-simplifying
makes it unreadable** — explain the jargon, teach, don't just summarize.

**MANDATORY grounding:** ALWAYS fetch the original English report (or full text)
via the alphaXiv MCP **every time**, before authoring — not only when a term
looks unclear. The existing card is a lossy translation; rewriting from it alone
risks amplifying any gap into hallucination. The MCP original is the source of
truth you write *from*; the existing card is only for diffing what's missing.

```python
import sys, os; sys.path.insert(0, os.environ.get("CLAUDE_PLUGIN_ROOT", os.path.expanduser("~/.claude/skills/research-cards")) + "/skills/card-rewrite")
import rewrite_lib as L
print(L.card_dump(CID))          # read the OLD card (recursive — sees nested bullets)
```

---

## The 8-point completeness checklist (every rewritten card MUST have)

A card is only "done" when ALL of these hold — ⑥ and ⑦ are the ones most easily
forgotten (a fresh rebuild silently drops figures and colorization):

1. **定位** — a `**一句話：**` essence + a `**為什麼〈config profile.reader〉該讀：**` line up top（讀者身分取自 config，例：語音研究者）.
2. **先備知識（名詞快速補帖）** — an H2 section defining the paper's jargon in plain
   language (skip only if the paper has almost no field-specific terms).
3. **教學式正文** — the 6-section arc (背景/定位 → 核心想法 → 方法 → 結果 → 意義),
   explaining the **WHY** inline ("dropless＝不丟 token，因為…"), not just listing facts.
4. **中英並列術語** — keep the English term alongside any non-trivial technical
   term: `共享降維投影（shared down-projection）`, `紅隊測試（red-teaming）`,
   `策略梯度（policy gradient）`. English is often clearer than a rare Chinese coinage.
   **Do not leave a domain term Chinese-only.**
5. **填滿快速摘要** — AI 摘要 / 問題 / 方法 / 結果 / 要點, each a scannable toggle.
6. **保留原圖** — re-insert every figure from the old card (`L.extract_images`).
7. **重新上色** — re-apply 🟡 (model/benchmark/method names) / 🟢 (gains, SOTA) /
   🔴 (limitations, failures) via `color_rules` → `L.finalize`.
8. **Source 連結** — keep the `Source: …alphaxiv.org/zh/overview/{id}` line.

---

## Workflow (one card)

### Step 1 — Fetch the ORIGINAL (mandatory), then read the current card
**Always** pull the original first — this is what you author from:
`mcp__alphaxiv__get_paper_content(url="https://alphaxiv.org/overview/{arxiv_id}")`
(load it via ToolSearch first; use `fullText=true` if the report is thin or you
need a specific mechanism/number the report omitted). Never skip this — writing
from the translated card alone risks amplifying its gaps into hallucination.
```python
import rewrite_lib as L
print(L.card_dump(CID))                       # the OLD card — only to see what's there / diff
imgs = L.extract_images(L.read_card(CID)[1])  # figures to preserve
```
Write the new card **from the MCP original**, using the old card only to diff
coverage and to grab the figures.

### Step 2 — Author the teaching content as ProseMirror blocks
Build a `C = []` list with the `L.*` builders, **using `L.add(C, *nodes)`** to
append them — it handles both single-node builders (which return a dict) and
`L.img` (which returns a list). ⚠️ Never write `C += L.h(...)`: `list += dict`
spreads the dict's keys and corrupts the document — always go through `L.add`.
⚠️ And do NOT wrap `L.add` in your own accumulator (e.g. `A(L.add(C, ...))`):
`L.add` already mutates **and returns** `C`, so wrapping it re-appends `C` into
itself → exponential blowup. Call `L.add(C, node, *L.img(src, cap), ...)` directly.
Follow the MAI-Thinking-1 shape (read it:
`python3 -c "import rewrite_lib as L; print(L.card_dump('<config gold_cards.card_rewrite 的卡 id>'))"`):

- `L.h(1, "[alphaXiv] {Title}")`
- `L.pp([("一句話：", True), "…"])`, `L.pp([(f"為什麼{reader}該讀：", True), "…"])`（reader＝config profile.reader）, `L.hr()`
- `L.h(2, "快速摘要")` + 5 × `L.toggle(label, [L.p(...) | L.bp(...)])`
- `L.hr()` + author/keyword `L.pp` lines + `L.hr()`
- `L.h(2, "0. 先備知識（名詞快速補帖）")` + `L.bul(term, plain explanation)` per term
- `L.h(2, "1. …背景與定位")`, `L.h(2, "2. 核心想法…")`, `L.h(2, "3. 怎麼做的（方法）")`
  (with `L.h(3, …)` subsections; `L.add(C, *L.img(imgs[k]["src"], "圖：…"))` where a figure belongs),
  `L.h(2, "4. 發現了什麼（結果）")`, `L.h(2, "5. 為什麼重要（意義）")`
- `L.hr()`, `L.source(url)`

Match comment density / tone to the example. All prose in the configured
output language — config `profile.language`; unset → Claude Code's `language`
setting (mapped); default Traditional Chinese（`hbconfig.output_language()`
is the single resolution rule）. Model/benchmark/metric names and the
bilingual original-language terms stay untranslated.

### Step 3 — Define color rules + finalize
```python
COLOR_RULES = [
  ("MAI-Thinking-1","yellow"), ("GRPO","yellow"), ("AIME 2026","yellow"),  # names
  ("94.5%","green"), ("追平","green"),                                      # gains
  ("缺乏可操控性","red"), ("不能直接外推","red"),                            # limits
]
md5, _ = L.read_card(CID)
print("size", L.finalize(CID, md5, C, COLOR_RULES))   # colorize → 100k check → save
```
`finalize` raises if as-built > 100k and warns above ~80k (UUID inflation on save
adds ~20%). If it warns/raises, trim the least-central bullets, not the teaching.

### Step 4 — Verify
```bash
python3 -c "import rewrite_lib as L; print(L.card_dump('$CID'))"   # reads back clean
```
Confirm: figures present, 快速摘要 filled, terms bilingual, no Chinese-only jargon.

---

## Retrofit mode (batch) — rewrite many existing cards

The mechanics are cheap; the **authoring** is the work, so fan out: **one
subagent per card**, each doing the full Step 1–4 for its card. Pick a small,
coherent first batch (e.g. one topic cluster), validate with the user, then
continue. Dispatch with the Task tool, giving each subagent: the card id + arxiv
id, the path to this skill, the 8-point checklist, and the MAI card as the gold
example. Collect sizes / color counts / image counts and report; **do not** touch
overview cards (paper card ids are unchanged, so overview links still resolve —
no resync needed).

⚠️ **Concurrency hygiene** (batch runs many rewrites at once):
- Each subagent must write its build script to a **card-specific temp path**
  (e.g. `/tmp/rewrite_<cardid8>.py`), NEVER a shared `/tmp/build_card.py` — a
  shared name lets one agent execute another's script and clobber the wrong card.
- After a batch, **verify titles match** (the H1 contains the expected paper),
  exactly one H1 node, `is_upgraded`, and size < 100k — to catch any race or
  oversize. `finalize` auto-shrinks large data-URL figures, but verify anyway.

Candidate selection: cards whose subfield is likely unfamiliar / jargon-dense
benefit most. Avoid re-running on already-teaching-style cards (those with a
`先備知識` section).

⚠️ **完成驗證（收工的硬條件）**——2026-07 實案：一次批次中途停掉留下
11 張尾巴，近三年沒人發現。兩個層級：

- **本批次收工**（topic-scoped 小批次合法）：逐一驗證本批次的 card IDs
  已 `is_upgraded`（title 相符、單 H1、<100k）——不要求全域 todo 清空。
- **campaign 收工**（目標是「全部改寫完」時）：
  1. `res = L.list_todo()`，直到 `res["todo"] == []`；
  2. `res["read_errors"]` 必須為空——讀取失敗的卡不在 todo/done 內，
     沉默消失會把「沒掃到」誤判成「掃完了」；非空先查明再收工；
  3. `res["excluded_by_filter"]`（Source Type 過濾的沉默排除數）非零時
     用 `L.list_todo(source_type=None)` 全掃一次，人工判定被排除者是否
     為合法例外（hub 卡、手寫筆記）；合法例外**記錄並回報使用者**即可
     ——這個數字不會歸零，歸零不是條件，「已審核」才是。

---

## Notes for the referencing skills

- **scholar-inbox-clip**: new cards should be produced in this teaching style; an
  interactive clip can invoke this skill for the final card. (Cron `run.py` still
  emits a baseline translated card; a later retrofit upgrades it.)
- **overview skills** (unified `overview` topics: auditory / spoken / tokenizer /
  duplex / …): they author only 3 bullets per paper, so they use the **light
  subset** — bilingual terms + give the WHY — not the full machinery (no 先備知識,
  no figures, no retrofit here).
