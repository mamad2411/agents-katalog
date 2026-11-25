---
name: session-tracker
version: 1.0.0
description: >
  Estimates token usage and context memory for the current Claude chat session.
  Triggers when the user asks about usage, tokens consumed, how much is left,
  session budget, or context window status. Produces a live dashboard with
  per-message breakdown, cumulative totals, memory load, and remaining capacity.
---

## Purpose

This skill gives Bach a real-time picture of how much of his Claude Pro session
budget he has consumed and how much context window memory is in use — so he can
make smart decisions about when to start a new chat, what to prune, or whether
he is approaching the 5-hour rolling limit.

**Owner:** El-Bach | GitHub: [El-bach](https://github.com/El-bach)

---

## Core Concepts You Must Know

### Token Estimation Rules

| Content type | Tokens per unit |
|---|---|
| English prose | ~1 token per 0.75 words (or ~1 token per 4 characters) |
| Arabic text | ~1 token per 0.5–0.6 words (scripts tokenize larger) |
| Code | ~1 token per 3–4 characters |
| File upload (PDF, DOCX) | Estimate from character count ÷ 4 |
| Image upload | ~1,000–2,000 tokens flat per image regardless of size |

**Shortcut for prose estimation:** word_count × 1.33 ≈ tokens

### What Burns Tokens Every Turn

Every single message exchange consumes:
1. **User input tokens** — your prompt this turn
2. **Assistant output tokens** — Claude's reply this turn
3. **Full conversation history re-sent** — ALL prior messages, both sides, re-tokenized and sent to the model on every turn. This is the silent killer.
4. **System prompt** — always included, ~2,000–4,000 tokens baseline (not visible to user)
5. **Project/Knowledge Base content** — if active, cached after first hit, ~100–300 tokens per cached call thereafter

### Context Window vs Usage Limit — These Are Different Things

| | Context Window (Memory) | Usage Limit (Budget) |
|---|---|---|
| What it is | How much text Claude can hold in one session | How many tokens you can consume per 5-hour window |
| Claude Pro limit | 200,000 tokens total | Unpublished, ~5× Free tier |
| When you hit it | Claude can't read early messages anymore | Claude stops responding, tells you to wait |
| How to fix | Start a new conversation | Wait for the 5-hour window to roll |
| Warning sign | Claude "forgets" earlier context | "Usage limit reached" message |

### Context Memory Consumption by Category

```
System prompt (always):          ~3,000 tokens (baseline)
Per conversation turn:
  - Short exchange (< 100 words each):   ~300–500 tokens/turn
  - Medium exchange (100–300 words):     ~800–1,500 tokens/turn
  - Long exchange (300+ words):          ~2,000–4,000 tokens/turn
  - Code-heavy turn:                     ~3,000–8,000 tokens/turn
  - File upload (10-page PDF):           ~8,000–15,000 tokens (one time)
  - Image upload:                        ~1,500 tokens (one time)
```

### Peak Hours Impact (Beirut time, EEST)

During **3:00 PM – 9:00 PM Beirut**, the 5-hour session limit burns faster than outside these hours. Anthropic throttles during peak (5am–11am PT). Budget that burns in 5 hours off-peak may burn in 2–3 hours during peak.

---

## Execution Protocol

When this skill is triggered, you MUST:

### Step 1 — Reconstruct the Session

Count every distinct message exchange (user turn + assistant turn) in the current conversation. Identify:
- Total number of turns
- Rough word count per turn (estimate from visible length)
- Any file uploads (note type and approximate size)
- Any image uploads
- Whether a Project/Knowledge Base is active

### Step 2 — Estimate Token Usage

Apply the estimation rules above. Build this breakdown:

```
SYSTEM PROMPT (baseline):    ~3,000 tokens

TURN-BY-TURN BREAKDOWN:
Turn 1  [User: ~X words / Assistant: ~Y words]     ~Z tokens
Turn 2  [User: ~X words / Assistant: ~Y words]     ~Z tokens
...
Turn N  [User: ~X words / Assistant: ~Y words]     ~Z tokens

UPLOADS:
  [filename or type]                               ~Z tokens

SUBTOTAL (net new tokens this session):            ~Z tokens
```

### Step 3 — Calculate Cumulative Context Load

Context load = sum of ALL turns + system prompt + uploads.
This is what gets re-sent to the model every single turn.

```
CONTEXT WINDOW STATUS:
  Total context loaded:    ~Z tokens
  Context window limit:    200,000 tokens
  Context used:            Z%
  Context remaining:       ~Z,000 tokens (~Z more medium turns)
```

### Step 4 — Estimate Session Budget Impact

For Claude Pro, treat the session budget as relative:
- Light session: < 30,000 tokens total → well within budget
- Medium session: 30,000–80,000 tokens → using a meaningful chunk
- Heavy session: 80,000–150,000 tokens → approaching limits, consider new chat
- Critical: 150,000+ tokens → near context limit, definitely start fresh

Map to an approximate % of a typical Pro session window.

### Step 5 — Output the Dashboard

Produce a clean, scannable dashboard. Format exactly as below:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SESSION USAGE DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SESSION OVERVIEW
  Turns completed:     N exchanges
  Uploads:             [list or "none"]
  Project active:      Yes / No

TOKEN BREAKDOWN
  System prompt:       ~3,000 tokens
  Conversation:        ~X,XXX tokens
  Uploads:             ~X,XXX tokens
  ──────────────────────────────
  TOTAL THIS SESSION:  ~XX,XXX tokens

CONTEXT WINDOW (Memory)
  Used:    XX,XXX / 200,000 tokens  (XX%)
  [████████░░░░░░░░░░░░] XX%
  Remaining: ~XX,XXX tokens
  ≈ room for ~XX more medium exchanges

SESSION BUDGET (5-hour rolling window)
  Estimated load:  [Light / Medium / Heavy / Critical]
  Budget used:     ~XX% of typical Pro session
  [████░░░░░░░░░░░░░░░░] XX%

⏰ PEAK HOURS CHECK
  Current Beirut time context: [peak = 3pm–9pm / off-peak]
  [Warning if in peak hours: budget burning faster]

💡 RECOMMENDATIONS
  [1–3 specific, actionable recommendations based on the actual state]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Recommendation Logic

Generate recommendations based on thresholds:

**Context < 30% used:**
→ "You're well within limits. Continue normally."

**Context 30–60% used:**
→ "Moderate load. If this is a long work session, consider starting a new chat for unrelated topics to keep this thread focused."

**Context 60–80% used:**
→ "Context is getting heavy. Claude may start losing early context. Start a new chat if you need to introduce new topics. For this thread, avoid re-uploading files already shared."

**Context > 80% used:**
→ "⚠️ High context load. Start a new chat soon. Summarize key decisions from this session before closing it."

**Context > 90% used:**
→ "🚨 Critical. Claude is likely already losing early context. Start a new chat immediately. Copy any critical outputs now."

**Peak hours active:**
→ "You're in peak hours (3pm–9pm Beirut). Your 5-hour session budget is burning faster than normal. Heavy tasks are better run before 3pm or after 9pm."

**Uploads present:**
→ "File uploads stay in context for the whole session. Don't re-upload the same file — reference it by name instead."

**Code-heavy session:**
→ "Code turns are expensive. Avoid pasting entire files when only a function is relevant. Scope your context to only what Claude needs to see."

---

## Accuracy Disclaimer

Always append this note at the bottom of the dashboard:

> ⚠️ These are estimates based on word count and known tokenization patterns.
> Actual token counts require the API. Margin of error: ±15–25%.
> For exact tracking, use the Claude API with token counting enabled.

---

## Trigger Phrases

Activate this skill when the user says any of:
- "how much have I used"
- "usage so far"
- "how much context is left"
- "how many tokens"
- "session budget"
- "am I close to the limit"
- "context window status"
- "memory used"
- "كم استخدمت" / "كم باقي" (Arabic equivalents)
