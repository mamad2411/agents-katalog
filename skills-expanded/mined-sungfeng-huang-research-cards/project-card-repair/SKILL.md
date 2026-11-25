---
name: project-card-repair
description: >-
  Repair broken card links in Heptabase project + project/progress cards —
  the dead plain-text `[[card:UUID]]` literals left by a `hb` bridge append
  (remote cluster) or a bare CLI append, which the heptabase CLI never renders
  into a real, clickable card-mention. Seals structural header/timeline shapes
  plus safe inline citations on progress/log cards back into live mentions:
  a log/progress card's `專案：[[card:…]]` back-ref to its
  project, a project card's `📎 date [[card:…]]` timeline line to a log, and a
  continuation child's `母卡：[[card:…]]` back-ref to its entry. Given card
  id(s) it repairs just those; given nothing it sweeps every project +
  progress card. Use when the user says 修卡片 link / 卡片連結斷了 / log 卡指回
  project 斷了 / timeline 連結壞掉 / repair/seal project card links / 專案回指
  變成純文字 / 掃全部修卡片連結. Mac-only (local heptabase CLI). Sentinels
  (▶續卡 chain edges) are left to project-card-log/repair_chain.py --seal
  unless --include-sentinel is passed.
allowed-tools: Bash(heptabase:*) Bash(python3 *) Read
---

# Project Card Repair — seal text-form card links into real mentions

## What breaks, and why

A card link should be a clickable **card-mention node**. But an append that
did NOT go through the local heptabase CLI's renderer writes it as the literal
text `[[card:<uuid>]]` — dead text in the UI, invisible to PM-level parsers.
This happens on the **`hb` bridge** (remote cluster over SSH, append-only) and
on bare CLI/Mac spills. Structural links use three shapes:

| shape | where | direction |
|---|---|---|
| `專案：[[card:<project>]]　環境：…` | log/progress card header | log → project |
| `📎 <date>　[[card:<log>]]　<summary>` | project card timeline line | project → log |
| `…母卡：[[card:<entry>]]。…` | continuation child header | chain child → entry |

Progress/log prose also cites earlier evidence inline（例如「完整前情見
`[[card:<previous-log>]]`」）. Those citations need the same conversion, but
only on cards explicitly known to be progress/log cards. Code marks and code
blocks remain literal examples; targets absent from the non-trashed Card
Library remain unchanged and are reported as `missing_inline_targets`.

Obsidian `.md` cards use `[[wikilink]]` and never hit this — **heptabase-only**.

## Usage

```bash
cd ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/project-card-repair
python3 repair.py --card <id> [--card <id> …]   # pinpoint: repair only these
python3 repair.py --inline-card <id>             # log card: structural + inline
python3 repair.py                               # sweep: every project + progress card
python3 repair.py --dry-run                     # preview; save nothing
python3 repair.py --include-sentinel            # also seal ▶續卡 (see below)
```

Output is one JSON object: `mode`, `scanned`, `cards_changed`, and a lean
`results` list (only cards that sealed something or errored, each with
`by_kind`: how many loglink / backref / sentinel paragraphs were sealed).
Idempotent — a second run reports `cards_changed: 0`. One card failing to read
records an `error` and does not abort the sweep.

## Design — reuse, don't reimplement

The split-in-place seal logic lives **once** in
`../project-card-log/append_card.py`:

- `seal_loglink_paragraphs` — the `📎` timeline lines
- `seal_backref_paragraphs(nodes, marks=(母卡：, 專案：))` — both header back-refs
  (the `專案：` mark was generalised in from this skill; the default still only
  matches `母卡：`, so the chain-walk caller in `repair_chain.py` is unchanged)
- `seal_sentinel_paragraphs` — the `▶續卡` chain edge (opt-in only)
- `seal_inline_card_literals` — recursively seal live prose citations,
  excluding inline code and code blocks

`repair.py` just routes cards to those helpers and saves via `rewrite_lib`
(md5-guarded — a concurrent edit aborts the save). No link-parsing logic is
duplicated here.

## Sentinels — prefer repair_chain.py --seal

The `▶ 續卡（本卡已達容量上限）：[[card:…]]` chain edge is also a text-form spill,
but sealing it has **chain semantics**. The canonical fix is:

```bash
python3 ../project-card-log/repair_chain.py --seal <entry-id>    # walks the whole chain
```

It follows each freshly-sealed edge hop-by-hop and, critically, respects the
forensics rule that a parallel session may have **deliberately folded + trashed**
a continuation card — re-linking a trashed edge corrupts the chain's terminal
state. This skill's `--include-sentinel` does a single-card seal with **no
walk and no trashed-check**; use it only when you know the continuation is live
(e.g. a lone card wrongly carrying a text sentinel). By default sentinels are
left untouched.

## Scope

Targets are the **project** and **project/progress** collections (config
`heptabase.collections.projects` / `.progress` tag ids). Passing `--card`
bypasses the scan and repairs exactly the ids given — those need not be project
cards (the seal helpers no-op on any paragraph without a matching header), but
the intended use is project/progress cards. Passing `--inline-card` additionally
enables safe inline sealing and is therefore reserved for known progress/log
cards. A no-argument sweep derives that distinction from collection membership:
project cards get structural repair only; progress cards get structural +
inline repair.

## After repairing

Card ids are unchanged (only text→mention within a card), so overview links and
chain edges still resolve. If the vault/HackMD mirrors matter, run **note-sync**
afterwards so the sealed cards forward out (heptabase is canonical, so this is a
forward mirror, never a write-back that could re-strand them).

Cluster `project-card-log` events may automate this sequence through
`project-card-log/post_log_sync.py`: it uses `--inline-card` for the log and
structural-only `--card` for the actual timeline tail, then runs note-sync and
refreshes both project canvases. Do not reverse that order.

Related: **project-card-log** (writes these cards; owns the seal helpers +
`repair_chain.py --seal` for chain edges), **project-card-merge** /
**project-card-cleanup** (consolidation — run repair first so every edge is a
real mention the merge parser can see), **note-sync** (mirror out).
