---
name: eop-sentinel
description: >
  The Elevation of Privilege (EoP) game that never ends — embedded in the pull request. Use
  this skill to "play a hand" against a diff or PR: pick the highest STRIDE card the change
  legitimately invites, comment in the card's voice (threat, why-here, candidate fix), and
  track clean-diff streaks plus a "hardest to threaten" leaderboard so the threat-modeling
  vocabulary stays alive between sessions. Trigger on "play a hand against this PR", "run the
  EoP sentinel on this diff", "STRIDE-review these changes", "what threat does this change
  invite?", or "update the sentinel leaderboard". Builds on eop-deck; complements eop-deal
  and eop-referee.
license: CC-BY-3.0-US (deck content © 2009 Microsoft Corporation)
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# eop-sentinel — the game that never ends, in the PR

`eop-deal` and `eop-referee` run a session at a table. The Sentinel keeps the game going
between sessions, where the work actually happens: **every diff is a hand of EoP.** It picks
the strongest STRIDE threat the change honestly invites, speaks it in the card's voice, and
keeps score — a streak for clean diffs and a "hardest to threaten" leaderboard. The point is
not a perfect scanner; it's a habit-former that keeps the deck's vocabulary in daily reach.

Builds on **`eop-deck`** for the deck, the grounding idea, and the bug-test. It grounds only
the *changed surface*, not the whole repo — so it's fast enough to run on every PR.

## Playing a hand — procedure

When asked to review a diff or PR:

### 1. Get the changes

Work from a diff: `git diff` (working tree), `git diff <base>...<head>`, or a PR (e.g.
`gh pr diff <n>`). Identify what the change *introduces or alters*: new endpoints, new data
flows, changed auth, new external input, new trust-boundary crossings, new agent/tool
permissions.

### 2. Ground the changed surface against the deck

For the changed surface only, find which of the 74 cards in `eop-deck`'s
[`assets/deck.json`](../eop-deck/assets/deck.json) can be **honestly** linked to the diff.
If a grounded deck for the repo already exists (`eop-grounded-deck/1`), consume it for
component/boundary context. The honesty bar is the whole game — a contrived link teaches the
wrong lesson. Full method: [`references/playing-a-hand.md`](references/playing-a-hand.md).

### 3. Play the highest card you can legitimately link

As in the real game's trick-taking, the Sentinel plays the **strongest** threat the change
exposes: among honestly-linkable cards, pick the one with the highest `rank_value`, with an
**Elevation of Privilege (trump)** card outranking any other suit. If the diff exposes a
genuinely novel attack no printed card covers, play that suit's **Ace** (open threat) — the
gen-AI-era headline. If no card links honestly, the diff is **clean**: the streak grows.

### 4. Comment in the card's voice

Emit one structured comment: the card (suit + the **quoted** threat from `deck.json`),
**why here** (the named file/hunk/boundary in the diff), and a **candidate fix**. Quote the
card; never paraphrase it. Voice and examples: [`references/card-voice.md`](references/card-voice.md).

### 5. Record the hand and refresh the board

Record the outcome — `threat` (with `card_id`, `component`, `why_here`, `candidate_fix`) or
`clean` (with the touched `subjects`) — into the ledger, then re-render the leaderboard:

```bash
echo '<hand json>' | python3 .claude/skills/eop-sentinel/assets/sentinel_ledger.py \
  <repo>/.threat-model/sentinel.json --record - --board <repo>/.threat-model/board.md
```

The ledger stores only the ordered list of hands; the **streak** and **leaderboard** are
recomputed from history every time, so they can't drift. Dependency-free (stdlib only);
auto-locates `deck.json`; warns (doesn't fail) on incomplete input. Schema and scoring
semantics: [`references/ledger-schema.md`](references/ledger-schema.md).

## Where the score lives (resolved)

The ledger persists at **`.threat-model/sentinel.json` inside the target repo** (with a rendered
`.threat-model/board.md` beside it), committed so standings travel with the project via git — every
teammate sees the same streak and leaderboard on pull. No shared service, no local-only
state, no dependency outside the repo: consistent with the suite's self-contained,
trunk-based design. The skill ships the helper and the schema; the *data* lives in the
user's repo (like grounded decks do). The helper writes the file but never commits it.

## The deliverable (plan's "done when")

A habit-former that keeps the vocabulary alive between sessions: each PR draws a card-voiced
threat (or a clean-streak point), and the leaderboard makes "which parts of our system are
hardest to threaten?" a running, social question — the whitepaper's table-talk, embedded in
the workflow.

## The guardrail

The Sentinel plays the strongest threat it can *honestly* link and proposes a fix — it does
**not** decide the threat is real or block the merge. The author and reviewers argue it with
the bug-test; the argument is the learning. Keep the Sentinel a prompt at the table, not a
gate: a clean streak is earned by the table agreeing nothing links, not by the tool staying
quiet.

## Provenance

Deck content © 2009 Microsoft Corporation, CC BY 3.0 US, via `eop-deck`.
