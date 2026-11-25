---
name: premortem
description: "Kill bad plans before they kill you. Quick premortem: '!premortem' or 'premortem this'. Full premortem: '!premortem full'. Auto-detects what you're working on. Integrates Base Rates, Bias Circuit-Breaker, L/I Scoring, Commitment — all 4 core features in one pass. Designed for Claude Code CLI: minimal friction, terminal-native output."
version: 1.5.4
author: DasClown
license: MIT
metadata:
  triggers:
    immediate: ["!premortem", "!pm", "premortem this", "premortem my", "kill this plan", "stress test this"]
    strong: ["what could go wrong", "am I missing anything", "poke holes in this", "devil's advocate"]
    full_mode: ["!premortem full", "!pm full", "full premortem"]
    review: ["!pm review", "!premortem review", "premortem calibration"]
    persist: ["!pm persist", "!premortem log", "log premortem"]
  requires: []
---

# Premortem — Kill Bad Plans Before They Kill You

**Core idea:** Instead of asking "will this work?" → imagine it already failed 6 months from now, then explain *why*. This is Kahneman's single most valuable decision tool. It breaks the AI's default agreeableness and your own optimism bias.

**Philosophy:** *Denk dir Dinge zuende. Sei kritisch mit dir selbst.* The premortem is not about being pessimistic — it's about being *honest* before reality forces honesty on you.

---

## Two Modes

### Quick Premortem (`!premortem` / `!pm`) — 30 seconds

For small-to-medium decisions during coding. 3 questions + quick L/I calibration.

1. **What's the most likely way this fails?** — Rate L (1-5) + I (1-5)
2. **What's the worst-case failure?** — Even if unlikely, what's the damage?
3. **What's one thing you should verify right now?** — Checkable in this session

**Automatic L/I:** For the #1 failure, assign L × I and show the zone.
`L=4 I=3 → 12 🟠 Needs mitigation`

No ceremony. ~12-16 lines, 30 seconds.

### Full Premortem (`!premortem full` / `!pm full`) — 2-3 minutes

For high-stakes decisions: architecture choices, deploys, major refactors, feature launches. Runs all 4 core features:

1. **Base Rates** — Reference real failure statistics for this type of decision
2. **Bias Circuit-Breaker** — Systematic check for Sycophancy, Optimism, Availability, Anchoring
3. **L/I Scoring** — Likelihood × Impact scoring (1-5) for each failure mode
4. **Commitment** — Concrete next action with a date

---

## Context Auto-Detection

Before running, determine what the user is planning:

### Git Context (if in a repo)
- `git log --oneline -3` → What's the current branch doing?
- `git diff --stat HEAD~1` → How many files changed? What type of work?
- `git branch --show-current` → Feature branch? Fix branch? Main?
- **Keywords:** If commits mention "refactor", "migrate", "rewrite", "restructure" → auto-suggest `!pm`

### Conversation Context
- What was the user's last message? Are they describing a plan?
- Any architecture decisions, config changes, or dependency additions?
- Are they about to merge/deploy? High-risk?

**If unclear after scanning**, ask ONE question: "Was genau planst du gerade?" Don't ask more than that.

---

## Quick Premortem Flow

When the user says `!premortem` or any immediate trigger:

```
### Premortem 🔪

Plan: [one-line summary of what you detected they're doing]

#### 1. Most Likely Failure
[specific, grounded in their actual context. Not generic.]
L=? I=? → L×I=? [zone]

#### 2. Worst-Case Failure
[the one that would do real damage, even if less likely]
L=? I=? → L×I=? [zone]

#### 3. Verify Now
[one concrete thing they can check right now, in this session]
→ [actual command or check they can run]
```

That's it. Total output: ~12-16 lines. Keep moving.

#### Persist
Append this premortem as one JSON line to `.premortem/log.jsonl` (create dir if missing).
Set occurred=null, status="open". Confirm with: "Logged - !pm review checks it later."


---

## Full Premortem Flow

When the user says `!premortem full`:

### Step 1: Set the Frame

```
🔪 FULL PREMORTEM — 6 months from now, this has FAILED.

Plan: [one-line summary]
```

### Step 2: Failure Generation

Run all 4 features in parallel (spawn sub-agents or run as structured analysis). Produce:

```
## Failure Modes

[numbered list, each 1-2 sentences, specific to THIS plan]
```

### Step 3: The 4 Features (integrated output)

```
## Risk Assessment

| # | Failure Mode | L | I | L×I | Mitigation |
|---|-------------|---|---|-----|------------|
| 1 | [mode]     | 4 | 5 | 20  | [concrete] |
| 2 | [mode]     | 3 | 4 | 12  | [concrete] |
...
```

### Step 4: Base Rates Check

For each failure mode, ask: "What class of decision is this, and what does the base rate say?"

Source: `references/base-rates.md`. Quick reference:
- **Software project** → 70% timeline overshoot
- **Refactoring** → 64% exceed 50%+ of estimate
- **Product launch** → 70-95% failure rate
- **Feature without user research** → 64% fail

> Example: Your "2-week estimate" → base rate says 3-4 weeks minimum.

### Step 5: Bias Circuit-Breaker

After generating failures, run these checks (source: `references/bias-circuit-breaker.md`):

- **Sycophancy check:** Am I being too nice? Would I say this to a stranger?
- **Optimism check:** What's the inside view vs. outside view timeline?
- **Availability check:** Am I anchoring on the last thing I built/saw?
- **Anchoring check:** Is my estimate anchored to an arbitrary starting point?

If any check triggers, note it in the output:

> ⚠️ **Bias alert:** Optimism bias detected. Inside view says 2 weeks. Outside view (similar projects) says 3-4 weeks.

### Step 6: Commitment

```
## Commitment

[ONE concrete action] by [DATE].

Example: "Test pricing at $47 with 10 users by Friday" — NOT "consider testing pricing."
```

### Output Format (Full)

```
🔪 PREMORTEM REPORT

## Failure Modes (N found)
1. [failure 1]
2. [failure 2]
...

## Risk Matrix
| # | Failure | L | I | L×I | Mitigation |
|---|--------|---|---|-----|------------|
...

## Bias Check
[any triggered biases with explanation]

## Commitment
[action] by [date]

→ Top priority: [the ONE thing to fix first]
```

---

## The 4 Core Features (always active in Full mode)

### 1. Base Rates

Every failure mode is evaluated against real statistics. See `references/base-rates.md`. Key data points:

| Domain | Failure Rate | Source |
|--------|-------------|--------|
| Software projects exceed time estimates | 70% | Standish CHAOS |
| Software projects exceed budget by 100%+ | 45% | Standish CHAOS |
| Startup 5-year survival rate | 50% | BLS / Statistic Brain |
| Product launches that fail | 70-95% | HBS / Nielsen |
| Wrong hires (fired within 18 months) | 40-50% | HBR / Leadership IQ |
| M&A value destruction | 70-90% | McKinsey / HBR | |
| **Open-source CLI tools reach < 100 stars** | **95%** | GitHub ecosystem data |
| **Features deployed but never used** | **45%** | Standish CHAOS |
| **Build-phase tool to distribution failure** | **~80%** | PM Learning Curve (build != ship)

### 2. Bias Circuit-Breaker

Run AFTER generating failures (not before — don't filter yourself). Check for:

- **Sycophancy:** Am I being too agreeable? Rephrase the failure in the harshest honest terms.
- **Optimism:** Inside view vs. outside view. What would someone who's done this 10 times say?
- **Availability:** Is this failure mode from the last thing I read/built, or is it genuinely relevant?
- **Anchoring:** Did I start from an arbitrary number and insufficiently adjust?
- **Scope Creep (Bonus):** Is the plan bounded? What's explicitly NOT included?

See `references/bias-circuit-breaker.md` for detailed protocols.

### 3. L/I Scoring - ordinale Heuristik, KEIN cardinales Mass

WARNING: LxI ist Sortier-Heuristik, nicht objektiver Score. Ordinal x ordinal ist
mathematisch nicht vergleichbar (Cox, "What's Wrong with Risk Matrices?", 2008).
Primar pro Dimension screenen:

1. **I=5 -> ROT immer** - aber die AKTION hangt von L ab:
   - I=5 & L>=3 -> **Pravention:** Eintrittspfad mitigieren. Hoch + wahrscheinlich = Plan andern.
   - I=5 & L<=2 -> **"insurable tail":** Eintritt kaum senkbar -> Schadensbegrenzung bauen
     (Rollback / Backup / Kill-Switch / Circuit-Breaker)
     ODER strukturelle Verwundbarkeit bewusst akzeptieren UND dokumentieren.
   Verbotener Default: I=5 ignorieren, weil L niedrig ist.
2. **L=5 -> mindestens ORANGE**, egal welches I.
3. Sonst nach LxI sortieren - als grobe Triage-Reihenfolge, nicht als Wahrheit.

Drop "15-25 Rot / 9-12 Orange" - suggerierte Prazision, die nicht existiert.

**Likelihood (L):** See `references/li-scoring.md` for full scoring anchors and decision rules.
**Impact (I):** 1 = minor, 2 = some rework, 3 = delay/reputation, 4 = major loss, 5 = project-killing

See `references/li-scoring.md` for tie-break rules (equal LxI).

### 4. Commitment

Every full premortem ends with ONE concrete commitment:

- **Format:** "[Specific action] by [Date]"
- **NOT:** "Consider X" or "Think about Y" or "Look into Z"
- **DE-FENCE Pattern (Distribution Engagement):** Wenn der Engpass Distribution ist (nicht Build), dann muss das Commitment ein Verteil-Akt sein, kein Bau-Akt. "dev.to-Artikel publishieren" OK - "CLI bauen" NICHT OK
- **Examples:** "Write integration tests for the payment flow by Thursday" OK - "Consider testing more" NICHT OK
See `references/commitment.md` for the commitment protocol.

### 5. Distribution Playbook

Wenn der Engpass Distribution ist (nicht Build): siehe `references/distribution.md`.
Der Commitment-Mechanismus in Schritt 6 muss ein Verteil-Akt sein (DE-FENCE Pattern).

---

## !pm review - Calibration Loop

1. **OPEN COMMITMENTS:** Read `.premortem/log.jsonl`. List every record where status="open".
   - due < today -> "OVERDUE"
   - due <= +3d -> "due soon"
   - else "open"
   - Ask: done / postponed / cancelled? -> set status = done | missed | dropped

2. **UNRESOLVED PREDICTIONS:** For records >14d old with any occurred=null:
   "Premortem from [date] - '[plan]'. Failure '[desc]' (you gave L=[L], p=[p]):
    actually occurred? [y/n]" -> set occurred = true | false

3. **BRIER SCORE:** Over all resolved predictions, calculate and interpret
   (see `references/calibration.md` for formula and band mapping).
   Report with n: "Brier X.XX over N resolved predictions."
   Note systematic direction: underestimating or overestimating risk?

---

## When to Use

**Good targets:**
- Architecture decision (monolith vs. microservice, library choice, DB schema design)
- Before a big refactor ("I'm going to rewrite the auth module")
- Before deploying to production
- Before committing to a timeline or estimate
- Before a major purchase or SaaS decision
- When you're *too confident* about a plan (that's the danger signal)
- **Before expanding a working tool to multiple new deliverables** (e.g. Skill -> CLI + MCP + Package = Scope Explosion)

**Bad targets:**
- One-line changes or trivial fixes (just do it)
- Questions with a factual answer (just answer it)
- Problems you can't change anymore (premortem requires agency)
- When you're already in crisis mode (premortem is PRE, not DURING)

**Auto-detection:** If the user describes a plan spanning 3+ files, an architecture decision, or uses words like "refactor," "rewrite," "migrate," "restructure" — suggest a quick premortem: "Want me to premortem this before you start?"

---

## Anti-Patterns

- **Generic failures:** "The code might have bugs" is useless. Be specific to THIS plan.
- **Going through the motions:** Actually think. The user can spot a phoned-in premortem.
- **Sugarcoating:** The whole point is to hear what you DON'T want to hear.
- **Too many questions:** Auto-detect context. Ask max ONE question if unclear.
- **Analysis paralysis:** Quick mode exists for a reason. Don't full-premortem a CSS fix.
- **No self-audit:** Du hast den Skill gebaut — also MUSST du ihn selbst benutzen. Jeder Commit, jeder Push.
- **Scope Explosion:** "Klingt cool, mach CLI + MCP + Package" = 3 Projekte, fertig wird keins. Ein Deliverable, max zwei. Alles andere ist Ablenkung.
- **Building statt Distributing:** Wenn das Tool 9.5/10 ist aber 0 Nutzer hat, ist der Engpass **nicht** Features. Es ist Reichweite. Bauen verschiebt das Problem nur auf ein anderes Frontend.
- **"KI fuer KI" vergessen:** Wenn deine Intention "KI fuer KI, nicht fuer Menschen" war, aber der Plan ein CLI ist (Mensch tippt Enter, Mensch liest Output) - dann widerspricht der Plan deiner Intention. Pruef das frueh.

---

## Pro-Tipp

**Gewohnheit aufbauen:** Vor jedem `git commit -m "refactor"` → `!pm`. Vor jedem `git push` mit Breaking Changes → `!pm full`. 30 Sekunden jetzt sparen Stunden später.

> **Beispiel aus der Praxis:** "20 Tulpen — zack, Abfahrt." Der Plan: D2C Blumen-Dropshipping in 2 Wochen live. Premortem nach 5 Minuten: Kühlkette killt die Marge, VAT/EORI frisst den Gewinn, Reklamationen sind unkalkulierbar. Ergebnis: **Nicht bauen. 5 Minuten gespart vs. 6 Monate Learned.** Das ist der Wert.

> **Beispiel 2 - Selbst-Premortem auf den Premortem-Skill:** 6 Monate nach dem Build hat der Skill 9.5/10 Qualitat, aber 0 Nutzer. Der Autor will CLI + MCP Server bauen. Premortem: Scope Explosion (L=5 I=4 -> 20 ROT), Wartungsfalle (L=4 I=3 -> 12 ORANGE), Nutzerloser CLI (L=4 I=3 -> 12 ORANGE). Bias-Check: Optimismus (Bau-Launch-Reflex statt Promote-Learn-Iterate). Base Rate: 95% der Open-Source-CLIs erreichen < 100 Sterne. Commitment: **Nicht bauen. Stattdessen dev.to-Artikel publishieren fur Reichweite.** Ergebnis: 30 Minuten Content vs. Wochen Build-Verschwendung. Der Skill wurde auf sich selbst angewandt - und hat seine eigene Uber-Engineering-Phase gekillt.

---

*Siehe `CHANGELOG.md` für die Versionshistorie.*
