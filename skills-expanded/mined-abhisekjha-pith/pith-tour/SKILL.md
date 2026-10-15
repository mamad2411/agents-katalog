---
name: pith-tour
description: >
  Interactive guided tour of Pith. Walks the user through each feature
  experientially — one step at a time, hands-on, using their actual project.
  Resumable. Skippable. State tracked via tour.py.
---

## Tour conductor rules

You are running an interactive Pith tour. You are the guide.

Rules:
- One step at a time. Never show two steps at once.
- Every step ends with a prompt for action — user does something, you react.
- Use their ACTUAL project files (find one with glob). Never use fake examples.
- Show effects numerically where possible (token counts, line counts).
- Never lecture. Do, then explain.
- After each step action: acknowledge what happened, show the effect, then offer "next" or "skip".
- If the user says "skip", advance to the next step immediately.
- If the user says "done" or "quit", end the tour gracefully with a command summary.
- Track step via: `python3 tools/tour.py --step <n> --action set`

---

## Tour structure (7 steps)

### Step 0 — Welcome card

Display this exactly:

```
╔══════════════════════════════════════════╗
║          PITH INTERACTIVE TOUR           ║
║    7 steps · ~8 minutes · hands-on       ║
╚══════════════════════════════════════════╝

Each step: I show you one thing. You try it. You see it work.
No reading. Just doing.

Type  next  to advance ·  skip  to skip a step ·  quit  to exit
```

Then immediately show Step 1 without waiting.

---

### Step 1 — Compression (the core)

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 1 / 7   Tool Output Compression
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: Pith compresses tool results before they eat your context.
      Fires automatically. You never invoke it.

Watch: I'm going to read a file from your project right now.
```

Then: use Glob to find the largest source file in the project (prefer .ts, .py, .go, .java, .js — avoid node_modules, vendor, .git). Read it. After the read completes, say:

```
↑ That file: [N] lines.

Without Pith → Claude sees the full file as raw text (~[N*4] tokens).
With Pith    → Claude sees imports + signatures + types only (~[N*0.5] tokens).
Savings: ~[calculated %]% on that single read.

This fires on every Read, Grep, Bash call over 30 lines. Silently.
```

Then: `→ Say "next" to continue`

---

### Step 2 — Token meter

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 2 / 7   Live Token Meter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: See exactly where you are in the context window.
      Updates every response.

Do this: run /pith status
```

Wait for user to run it. When they do (or if they say "next" without running it, run it yourself and show output), explain the output fields:

```
Context bar    → how full the window is (auto-compact fires at 70%)
Output mode    → which compression level is active
Tool savings   → tokens saved by compression this session
Lifetime saved → total across all sessions
```

`→ Say "next" to continue`

---

### Step 3 — Output compression

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 3 / 7   Output Compression
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: Claude's responses can be compressed too.
      3 levels. You control them.

Do this: ask me any coding question you have right now.
         (anything — I'll answer it twice, normal then lean)
```

When they ask a question: answer it normally first, clearly labeled `[NORMAL MODE]`. Then answer the same question in lean mode labeled `[LEAN MODE]`. Show approximate token counts for each. Then:

```
/pith lean   → like that, every response
/pith ultra  → even tighter (arrows, tables, abbreviations)
/pith off    → back to normal

Activating lean now for the rest of this tour.
```

Set LEAN mode active immediately.

`→ Say "next" to continue`

---

### Step 4 — Structured formats

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 4 / 7   Structured Formats
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: Swap Claude's prose output for a tight template.
      Each format built for a specific task.

Do this: paste a bug or error you're dealing with right now.
         (or type "use example" and I'll make one up)
```

If they paste a real bug: use `/pith debug` format to answer it — Problem / Cause / Fix / Verify. Four fields. No prose.

If they say "use example": invent a realistic bug from their tech stack (detect from files in project), answer in debug format.

After: show the five formats briefly:
```
/pith debug   → Problem / Cause / Fix / Verify
/pith review  → L42: BUG. Fix: ...  (one line per issue)
/pith arch    → options table + decision + risks
/pith plan    → numbered steps + risks + done-when
/pith commit  → feat(auth): add token refresh on 401
```

`→ Say "next" to continue`

---

### Step 5 — Token budget

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 5 / 7   Token Budget
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: Set a hard ceiling per response.
      Claude stops when it hits the limit. No fluff to fill space.

Do this: type  /budget 40
         Then ask me something — anything.
```

After they set the budget and ask something: honor the 40-token limit strictly, then say (outside the budget):

```
↑ That response: ~40 tokens hard ceiling honored.

Use this when you want:
  - Quick answers, no elaboration
  - Forcing yourself to ask precise questions
  - Expensive API calls you want kept short

Clear it: /budget off
```

Clear the budget yourself at end of step.

`→ Say "next" to continue`

---

### Step 6 — Wiki: save something

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 6 / 7   Project Wiki — Saving
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: Pith maintains a persistent knowledge base for your project.
      Decisions, architecture, solved bugs — all searchable next session.

Do this: tell me one real decision you've made about this project.
         (tech choice, architecture call, tradeoff — anything real)
         (or type "use example" and I'll invent one)
```

When they share a decision: write it as a decision record to `wiki/decisions/` — use exact format from pith-wiki SKILL.md. Show the file being created. Then:

```
Saved → wiki/decisions/[slug].md

Next session:
  /pith wiki "why did we [decision]?" → retrieves this instantly
  /pith wiki                          → toggle wiki mode (auto-offers to save)
```

`→ Say "next" to continue`

---

### Step 7 — Wiki: query it back

**Card:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STEP 7 / 7   Project Wiki — Querying
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What: Retrieve what you've saved — in this session or any future one.

Do this: type  /pith wiki  followed by a question about the
         decision you just saved.
```

When they query: read `wiki/decisions/` + `wiki/index.md`, synthesize the answer with a citation to the file. Show exactly:

```
Based on [[decisions/[slug]]] (saved [today's date]):
[answer citing the decision]
```

Then show the full wiki structure:

```
wiki/
  index.md          ← catalog + search entry point
  log.md            ← session history
  decisions/        ← architecture decision records  ← you're here
  entities/         ← services, tools, components
  concepts/         ← patterns, ideas
```

`→ Say "next" or "done" to finish`

---

## Tour completion

Show this:

```
╔══════════════════════════════════════════╗
║            TOUR COMPLETE  ✓              ║
╚══════════════════════════════════════════╝

Active now:
  ✓ Tool compression    (automatic, always on)
  ✓ Token meter         (statusline)
  ✓ Lean mode           (/pith off to disable)
  ✓ Project wiki        (1 decision saved)

Cheat sheet:
  /pith lean|ultra|off      output compression
  /pith debug|arch|plan     structured formats
  /pith commit              write commit message
  /pith wiki "question"     query the wiki
  /pith ingest <file>       add a doc to wiki
  /pith status              token usage
  /budget <n>               hard response limit

Resume anytime: /pith tour
```

Mark tour complete: `python3 tools/tour.py --action complete`

Then: ask what they want to work on.

---

## Recovery rules

- User confused at any step → answer their question, then return to current step card
- User asks a real work question mid-tour → answer it fully, then offer to resume: "Want to continue the tour? We were on step [N]."
- User says "start over" → reset to step 1
- `/pith tour 3` → jump directly to step 3
