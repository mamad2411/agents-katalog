---
name: share-of-model-audit
description: Use when a founder needs to know how often the AI engines name them versus rivals for the questions buyers actually ask, when they say "measure my Share of Model", "do ChatGPT and Perplexity cite us", "are we losing to a competitor in the answer box", "did the GEO work move the number", "set my baseline", or "track this monthly". Also when a buyer keeps arriving pre-decided in favour of a rival. Produces a Share-of-Model scoreboard (you vs named competitors, per query, per engine), a citation-share number with a baseline, and the content gaps it exposes. Run after geo-content; feeds capture-learning and the weekly Share-of-Model loop.
stage: grow
function: growth
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Share-of-Model Audit

Buyers now ask an AI engine before they ask you, and the engine names three companies as proof. If it does not name you, the considered-buying journey starts with your competitor's case study, not yours, and you never see the loss. Share of Model is the percentage of those answers that cite you versus rivals. It is the new top of funnel, and a single reading lies. This skill turns it into a tracked number with a baseline, so you can tell whether your narrative is landing or a competitor is being cited in the rooms you cannot see.

## The method

Fixed query set, several engines, a scoring sheet, a tracked trend. Full framework: [`references/audit-protocol.md`](references/audit-protocol.md), drawn from handbook [Chapter 10](../../handbook/10-narrative-positioning-geo.md) and [Chapter 12](../../handbook/12-measuring-real-pmf.md).

### Step 1: Design the buyer query set

Write 20 to 50 queries a real buyer types, not the ones that flatter you. Lock the set so months are comparable. Mix the three intents.

| Intent | Example shape | What it tests |
| --- | --- | --- |
| Category | "best tool for [job]" | Do you appear in the top-of-funnel shortlist? |
| Comparison | "[competitor] alternatives", "[X] vs [Y]" | Do you survive the head-to-head? |
| Problem-led | "how do I [solve PROBLEM]" | Do you own the job, not just the category? |

### Step 2: Run a fixed engine panel

Run every query through at least three engines; one engine is not a reading. Use a clean session each time so prior chat does not seed the answer.

| Engine | Why include |
| --- | --- |
| ChatGPT | Largest buyer reach |
| Claude | Different citation behaviour |
| Perplexity | Source-first, names citations explicitly |

### Step 3: Score each answer

For every query and engine, record one row. Count citation, not vibes.

| Field | Values |
| --- | --- |
| Cited me? | yes / no |
| Named first? | yes / no |
| Competitors cited | list of names |
| Outcome | me / rival / neither |

### Step 4: Compute the share and the gaps

Citation share = answers naming you divided by total answers. First-mention share = answers naming you first divided by total. Write both down as the baseline. Then rank the queries where you are most absent but most should appear: that is the content backlog for `geo-content`.

### Step 5: Set the cadence

Re-score the same locked set monthly. Treat a flat line as confirmed flat, not as fine. A rising share means your content is becoming the reference; a falling one means a rival is being cited where you cannot watch.

## Output

- A **Share-of-Model scoreboard**: you vs named competitors, per query, per engine, with citation share and first-mention share.
- A dated **baseline** and the one competitor beating you most, with a one-line hypothesis why.
- The **content gaps**: the queries where you are absent but should lead.
- Next: feed the gaps to `geo-content`, then `capture-learning` to record what the number proved.

## Constraints

- Name the failure mode: cherry-picked queries on one engine with no baseline. A set you tuned to flatter yourself, run once in your favourite engine, measures nothing. Lock the set, run the panel, keep the series.
- Apply research-before-asserting: a single snapshot is not a trend, and any figure you quote must survive a re-run. Watch the series, not the reading.
- Stay theme-agnostic; the founder supplies the domain and the real competitor names. Never invent a competitor or a figure.

## Dictionary

[Share of Model](../../dictionary/07-ai-native-business.md#share-of-model) ·
[GEO (Generative Engine Optimization)](../../dictionary/07-ai-native-business.md#geo-generative-engine-optimization)

## Copy-paste version

> For non-coders: paste into Claude.ai, ChatGPT, and Perplexity, once each, and compare. Tag: `chat`.

```
Act as my AI-native go-to-market analyst. Product: [ONE_LINER]. For: [ICP]. Domain: [DOMAIN].
Real competitors: [2-4 NAMES].

1. Write 20 buyer queries my [ICP] actually types when deciding: a mix of category ("best tool
   for [job]"), comparison ("[competitor] alternatives", "[X] vs [Y]"), and problem-led ("how do I
   [solve PROBLEM]"). Do not tune them to flatter me.
2. Answer each query the way a buyer reads it. For each, record: was I cited (yes/no), was I named
   first (yes/no), which competitors were cited, and who won the answer (me / rival / neither).
3. Build the scoreboard as a table: query, me cited, named first, competitors, winner.
4. Compute two numbers plainly: my citation share (answers naming me / total) and my first-mention
   share. This is my baseline; tell me to write it down with today's date.
5. Name the one competitor cited most and give a one-line hypothesis why. Then list the three
   queries where I am most absent but most should appear: that is my content backlog.

This is ONE engine's view. Tell me to re-run the identical set in ChatGPT, Claude, and Perplexity
and compare, and to re-run the same set every month. Do not pad my number; if I am rarely cited,
say so. OUTPUT: the scoreboard, the two share numbers, the top gap, then ONE next action.
```
