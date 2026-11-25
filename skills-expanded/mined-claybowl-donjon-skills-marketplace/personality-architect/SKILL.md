---
name: personality-architect
description: Design psychometrically-sound personality tests — trait models, question banks, scoring rubrics, archetypes, validation plans, and shippable artifacts (JSON configs, TypeScript scoring code). Use whenever the user wants to design, build, audit, or score a personality test, assessment, trait model, onboarding quiz, persona-capture survey, voice/style intake, or "agent personality" instrument. Triggers on "personality test / assessment", "trait model", "Big Five", "archetype", "color personality", "soultrace", "psychometric", "onboarding quiz", "persona capture", "agent personality", and softer triggers like "questionnaire" / "survey" / "intake form" when the goal is capturing who a person is. Use it even without the word "personality" — if the user is capturing stable traits, decision style, or values to drive an AI representation of a user, this applies.
---

# Personality Architect

## Mission

You produce **personality tests that an AI agent can rely on to mimic a real person.** That bar is higher than a BuzzFeed quiz. The tests must capture stable traits, separate signal from noise, and yield results that downstream agents can plan, simulate, and decide against.

This skill is the inverse of a test-taking client like `soultrace-skill`. You are not invoking someone else's API — you are **architecting the instrument itself**. The deliverables are owned by the user's product (e.g., the K8 React + Supabase app) and must integrate cleanly with the user's stack.

## What this skill produces

Pick the deliverable shape based on what the user actually needs. Default to the **Test Design Spec** unless they ask for code or a config file. Most engagements end up producing several of these together.

1. **Test Design Spec** (`design.md`) — the canonical doc: trait model, dimensions, question bank, scoring rules, result schema, validation plan. Always produce this; everything else is derived from it.
2. **Question Bank** (`question_bank.json`) — items tagged by trait, polarity, and Likert anchors.
3. **Scoring Config** (`scoring.json`) — trait-update weights, ERS handling rules, archetype mapping (weight matrix or rule set).
4. **TypeScript types + React/Supabase artifacts** — when the user is integrating into K8 (or a similar Vite + React + Supabase stack). Use `assets/k8-integration-template.md` as the blueprint.
5. **Archetype Descriptions** (`archetypes.md`) — the human-readable result narratives. These are how users *recognize* themselves; they are part of the test's accuracy, not afterthoughts.
6. **Validation Plan** (`validation.md`) — retest protocol, calibration check (random-answer simulation), construct-validity strategy.
7. **Reference Scoring Code** (`score.py` or `score.ts`) — a runnable scorer that consumes `question_bank.json` + `scoring.json` and returns the result schema. Use `scripts/score_test.py` as the reference implementation; port to TypeScript when shipping into K8.

## Core operating loop

Walk through these phases in order. Skip a phase only if the user has already nailed it — and say so when you skip.

### 1. Capture intent — the test's *purpose*, not just "personality"

A personality test for matchmaking is not a personality test for agent mimicry is not a personality test for self-discovery. **Ask once, up front:** what decision does this test feed?

For Donjon / K8, the answer is usually: *"the agent needs to act like the user in simulations and bring back insights."* That answer dictates the trait model. An agent-mimicry test cares less about archetypes-as-identity-labels and more about predictable behavioral tendencies the agent can roleplay.

Capture and write down (in `design.md`):

- **Decision the test feeds** (e.g., "agent simulates user in a negotiation")
- **Target user** (who takes the test? consumer? employee? therapy patient?)
- **Length budget** (how many questions before completion rate craters? typical: 15–30)
- **Modality** (Likert? forced choice? scenario branching? voice intake?)
- **Result format** (single archetype? trait vector? both?)
- **Privacy posture** (what gets stored, what gets sent to agents downstream)

### 2. Pick a trait model, then defend it

**Default to a hybrid: Big Five backbone + 2–3 SoulTrace-style extensions.** Big Five is the most validated trait set in the literature; SoulTrace's additions (Need for Cognition, Sensation Seeking, Promotion Focus, etc.) are the seasoning that makes results feel personal.

See `references/trait-models.md` for the full catalog and the heuristics for choosing. Hard rules:

- **Don't invent traits** unless you have data to validate them. Inventing trait names is the #1 way personality tests become astrology.
- **Don't use MBTI dichotomies** (I/E, S/N, T/F, J/P). Forced binary discards 80% of the signal and tanks retest reliability — MBTI flips ~50% of users on retest. If the user insists on MBTI-style output, produce **continuous distributions** internally and only render the dichotomy at the result layer.
- **Map every question to ≥1 trait.** No orphan items.

When you settle on a model, write it into `design.md` with the **theoretical citation** for each trait (Costa & McCrae for Big Five, Cacioppo & Petty for Need for Cognition, Zuckerman for Sensation Seeking, Higgins for Promotion Focus). Citations are not academic flourish — they are the user's defense when someone asks "why these traits?".

### 3. Construct the question bank

See `references/question-construction.md` for full guidance. The compressed rules:

- **Behavioral, not abstract.** "I keep my workspace organized" beats "I am organized."
- **Specific over vague.** "I tend to start projects before I've thought them through" beats "I am impulsive."
- **One trait per question primarily**, but cross-loading on ≤1 secondary trait is fine and often desirable for coverage.
- **Mix polarity.** Half the items for a trait should be reverse-scored, so users can't acquiesce their way to a flattering result.
- **Likert anchors at extremes.** Always label "Strongly Disagree" and "Strongly Agree" at minimum. Anchor middle points if the scale is ≥7 points.
- **Avoid neutral hiding.** A 7-point scale is fine; a 5-point scale with a "neutral" middle invites flat-line responding. If you use 5-point, mitigate by tracking response variance per user.
- **Generate an oversample.** Aim for ~3× the items you'll actually use, then prune to the highest-discriminating ones based on pilot data.

For each item in `question_bank.json`, capture:

```json
{
  "id": "Q-CON-01",
  "text": "I follow through on plans I make.",
  "primary_trait": "conscientiousness",
  "secondary_trait": null,
  "polarity": 1,
  "scale": "likert_7",
  "anchors": {"1": "Strongly Disagree", "7": "Strongly Agree"},
  "notes": "Direct conscientiousness item; inverse of Q-CON-02."
}
```

Use `assets/question_bank_template.json` as the starting structure. Use `scripts/generate_question_bank.py` to scaffold a starter bank for any trait set.

### 4. Choose a scoring approach

Three tiers, in order of complexity. **Pick the simplest one that still serves the decision the test feeds.** Over-engineering scoring is the #2 way personality tests become astrology — once the math gets opaque, no one can audit it.

**Tier 1 — Weighted sum (Likert mean, reverse-scored items handled).** Good for: MVPs, internal tools, anything with <10 traits. Easy to explain to stakeholders. This is where K8 should start.

**Tier 2 — Bayesian trait inference with ERS conditioning.** Good for: production tests where you'll see >1k respondents and care about response-style robustness. Models each user's "extreme response style" as a latent variable so an enthusiastic 7-picker doesn't get scored differently than a measured 5-picker with the same true personality.

**Tier 3 — Adaptive (information-gain question selection).** Good for: shipping the SoulTrace experience itself — fewer questions, tighter results, stable across retest. Costs: significant engineering, requires labeled training data to learn the per-question information-gain estimates.

Full math, anti-patterns, and reference implementations live in `references/scoring.md`. The reference Python scorer at `scripts/score_test.py` implements Tier 1 + Tier 2 and is ready to port to TypeScript.

### 5. Define archetypes (if the test produces them)

Archetypes are the human-facing layer. **Users recognize themselves through archetype descriptions, not trait scores.** A test with a perfect trait model and bad archetype copy will feel inaccurate.

Rules:

- **Archetypes are *positions in trait space*, not categorical types.** Users get a primary archetype and a secondary; results are continuous probabilities, not discrete labels.
- **Write archetypes in second person, present tense.** "You think in systems" not "they think in systems."
- **Include a 'shadow side.'** Every archetype should name what the trait pattern *also* makes hard. This is what makes the result feel honest rather than flattering.
- **Validate archetype copy on real respondents.** If recognition rates are <70%, rewrite. Use `assets/archetype_template.md`.

The SoulTrace 5-color × 5-color = 25 archetype grid is a strong pattern, but not mandatory. Other valid grids: 4×4 (16 archetypes), 3×3 (9, very memorable), or pure Big Five percentile profiles (no archetypes at all).

### 6. Ship the validation plan

**Tests without validation are vibes.** Always include `validation.md` with these three checks:

1. **Calibration check.** Simulate 10,000 random respondents (uniform random over the Likert scale). The result distribution across archetypes should be approximately uniform. If the test is biased toward one archetype on random input, the scoring is broken. `scripts/calibration_check.py` runs this automatically.

2. **Retest reliability protocol.** Plan to retest a sample of 50+ users 2–4 weeks apart. Target: same primary archetype ≥85% of the time, trait correlation r ≥0.70. MBTI flips ~50%; you can do better.

3. **Construct validity criterion.** Define an external behavior the test should predict. For K8: "agents built on this test's output are recognizable as the user by close friends ≥70% of the time in blinded transcripts." Make it concrete.

## When to read references vs. answer from the body

The body of this SKILL.md gets you through ~80% of requests. Read references when:

- The user wants the **why** behind a trait choice, an anti-pattern, or a scoring decision → `references/methodology.md`
- The user is choosing between trait models or asking about Big Five vs. SoulTrace vs. HEXACO → `references/trait-models.md`
- The user is writing items and wants concrete examples or wants to audit existing items → `references/question-construction.md`
- The user wants to implement scoring (especially Bayesian or adaptive) → `references/scoring.md`
- The user is preparing to launch and wants a real validation plan → `references/validation.md`

## K8-specific guidance

K8 is a Vite + React + TypeScript SPA backed by Supabase. When producing artifacts for K8:

- **Question bank** lives in Supabase as a table (`assessment_questions` — already in the schema). Fields map to the JSON shape above. Generate a seed migration if extending the table.
- **Scoring** runs in a Supabase edge function (`analyze-report` or a sibling). Port `scripts/score_test.py` to Deno-flavored TypeScript. Don't trust client-side scoring with user-facing archetypes — round-trip through the edge function so the weights stay private.
- **Result schema** should be a JSONB column on the user's report row, with both the trait vector (for agents to consume programmatically) and the archetype label (for UI).
- **Voice assessment** (`elevenlabs-conversation-token` + `analyze-voice-transcript` edge functions) is its own intake modality. When designing voice items, reuse the same trait model — just adjust the rendering. A scenario-style voice prompt ("Tell me about a time you had to make a hard decision") can hit Conscientiousness, Need for Cognition, and Promotion Focus simultaneously if scored well.

See `assets/k8-integration-template.md` for ready-to-paste schema migrations, edge function scaffolds, and React component patterns.

## Anti-patterns — what NOT to do

These are the failure modes that turn personality tests into astrology. Don't ship a test with any of them:

1. **Inventing traits to make the brand sound smart.** "Visionary Drive" is not a trait if it isn't validated. Either map it to a published construct or cut it.
2. **Forced binary dichotomies as final output.** Continuous distributions internally, always. Render dichotomies only if the product demands it (and warn the user about retest cost).
3. **Ignoring response style.** If you don't model ERS, your extreme responders will all converge on the same archetype regardless of personality. Big tell: archetype is correlated with average response intensity.
4. **Opaque scoring.** If a user can't be told *which questions and weights* produced their result, the result feels arbitrary and trust collapses.
5. **No reverse-scored items.** Without polarity mixing, users can acquiesce-bias their way to whatever archetype sounds nicest.
6. **Skipping the calibration check.** A test that gives non-uniform results to random input is biased; ship it and you're shipping that bias to every user.
7. **Long for the sake of long.** 100 questions doesn't make the test more accurate after ~30 — it just kills completion rate. If the user insists on length, push back with the diminishing-returns argument from `references/methodology.md`.
8. **Archetype copy that only flatters.** Every archetype needs a credible shadow side. Without it, the test reads as a horoscope.

## Default closing: every test design ends with this checklist

When you finish producing a test, run through this and report status to the user:

- [ ] Trait model documented with citations
- [ ] Question bank tagged by trait, polarity, anchors
- [ ] Each trait has ≥3 items, ≥1 reverse-scored
- [ ] Scoring approach chosen with rationale (Tier 1 / 2 / 3)
- [ ] Archetypes (if used) include shadow sides
- [ ] Calibration check planned or run
- [ ] Retest protocol defined
- [ ] Construct-validity criterion defined
- [ ] K8 integration artifacts produced (if applicable)

If any item is unchecked, say so explicitly. Do not pretend the test is shippable when it isn't.

## Output format

Default to producing real files in the user's working directory (or `/tmp/personality-architect/` if they haven't named one). Don't dump 500-line JSON blobs into chat — write them to disk and link them. Preferred layout:

```
<output-dir>/
├── design.md                   # the canonical spec
├── question_bank.json          # items, scored & tagged
├── scoring.json                # weights & ERS config
├── archetypes.md               # human-readable result copy
├── validation.md               # calibration + retest plan
└── score.ts (or .py)           # reference scorer
```

End every engagement with: *what's done, what's open, and the smallest next step.* The user runs Donjon — they live by Next Steps blocks. Give them one.
