---
name: humanizer
version: 4.1.0
description: "Removes AI writing patterns and injects human quality (specificity, burstiness, precise emotional language) into drafted content. Includes an optional personal-brand mode (voice reference + deterministic eval gate) you can adapt to your own voice. Use when editing drafts so they don't sound like AI. NOT for generating new content, fact-checking, SEO scoring, or research."
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: Remove AI Patterns + Inject Human Quality

## Full routing notes

> Removes AI writing patterns and injects human quality — specificity, burstiness, and precise emotional language. Use when editing drafted content, cleaning up LinkedIn posts, product copy, or blog content so it doesn't sound like AI. Two-phase process: Phase 1 removes 33 AI tells (significance inflation, AI vocabulary, em dash overuse, contrastive negation, vague attributions, soulless structure); Phase 2 injects humanity (sentence length variation, specificity via "what kind?" technique, precise emotional language). An optional personal-brand mode (below) adapts the two phases to a specific author's voice, using a scoreable voice-schema gate and a deterministic eval harness. Do not use for generating new content from scratch, fact-checking, SEO scoring, or research. Does not use humanizer tools (gpthuman.ai, WriteHuman) — those are detectable; this skill does structural rewriting.

Two-phase editing skill. Phase 1 removes AI tells. Phase 2 injects specificity, burstiness, and emotional precision. Clean-but-generic is still a failure — both phases are required.

## Setup

Load both reference files before starting:
1. `references/patterns-reference.md` — 33 AI tell patterns with before/after examples
2. `references/specificity-techniques.md` — "What kind?" technique, 7 levers, Emotions Wheel

Both are mandatory. Do not skip either.

---

## Brand Context Intake

Before editing, identify the context. If not supplied, ask:

> "Which context is this for? (a) Personal brand — LinkedIn/X/blog, (b) Analytical deliverable (report/memo/brief), (c) Generic content"

| Context | Risk level | Quality gate |
|---------|-----------|-------------|
| Personal brand (LinkedIn/X/blog) | Highest | Use **Personal-brand mode** below (voice reference + schema gate + eval harness). Always offer 2 variations. Read-aloud test mandatory. At least one thing only the author could know. |
| Analytical deliverable (paired with a `write-report`-style caller before its humanization pass) | Highest | Match the register the document already uses — keep analytical clarity, strip generic AI texture. Zero em-dashes. Preserve evidence tags, codes, and cited numbers untouched — relocate, never delete. |
| Generic content | Standard | Run Phase 1 + Phase 2 only. No voice gate. |

---

## Personal-brand mode (example — adapt to your own voice)

When the draft is the author's own LinkedIn or X post, this mode wraps the two generic
phases with a specific voice and a scoreable gate. It only **rewrites an existing draft**;
generating a post from scratch is out of scope for this skill.

**Required inputs:** `draft` and `channel` (`linkedin` | `x`). Ask for either if missing.
Optional: `purpose`, `known_context` (facts/examples that must be preserved).

**Load, in order, before editing:**
1. `references/voice-schema.md` — a scoreable quality gate template. Fill in the "Banned
   Vocabulary" / "Forbidden Phrases" / dimension descriptions with the author's own rules,
   or use it as shipped as a reasonable generic default.
2. Any voice-reference notes the author already maintains (brand guidelines, prior
   approved posts, a style doc). If none exist yet, ask 2-3 questions about tone,
   audience, and what they never say, and note the answers for next time.

**Workflow:**
1. **Preserve meaning** — capture the core claim, audience, concrete facts, personal
   details, caveats. Mark facts that must not change. If the draft lacks enough
   factual/personal material to feel author-specific, say so under *Residual risks*
   rather than inventing details.
2. **Substance & structure** — lead with the point, cut padded intros / fake balance /
   list symmetry that does not serve the argument. LinkedIn keeps a considered prose
   rhythm unless clearly tactical; X compresses to one idea per tweet.
3. **Voice & humanize** — run Phase 1 + Phase 2 below, then apply the author's voice
   rules from step 1: precise, direct, evidence-first; confident but not certain; no
   corporate-polish theater, no generic AI commentary, no fake certainty; no em-dashes
   if that's one of their rules.
4. **Score & gate** — score the output against `references/voice-schema.md`. When
   editing files/fixtures, run the deterministic harness:
   ```bash
   python scripts/eval_voice.py fixtures --format markdown
   ```
   If not run, state that the scorecard is manual-only.
5. **Capture feedback** — on approve/reject/manual-edit, save before/after to
   `fixtures/before-after/` (approved), `fixtures/aiish/` (rejected), or `fixtures/gold/`
   (strong published). This builds a calibration set over time — don't rely on chat
   history alone.

**Output:** Revised Draft (2 variations) · Scorecard (vs schema) · Deterministic-check
summary · Change notes · Residual risks · Publishability verdict. Never publish or send
on the author's behalf — drafts are review inputs for a human.

---

## Phase 1: Remove AI Tells

Load `references/patterns-reference.md`. Scan for all 33 patterns. Rewrite each flagged section.

**Priority flags** (most common, fix first):
- **Em dashes (—):** Do a mechanical character search for U+2014 before anything else. Every instance outside a code block must be replaced. This is not optional and not stylistic — em dashes are one of the strongest AI detection signals and must be eliminated completely from prose. Replace with: comma (asides), period (strong breaks), colon (heading label-separators). Zero exceptions outside code blocks.
- AI tell-words: delve, unpack, leverage, tapestry, landscape, pivotal, comprehensive, robust, seamless, furthermore, moreover, genuine, genuinely, "it's worth noting," "this underscores"
- **2025-26 cluster** (the delve-era words are fading; these replaced them): unlock, elevate, holistic, nuanced, resonate, align, transformative, dynamic, empower, streamline, harness, paramount, meticulous
- **Contrastive negation** ("It's not just X, it's Y" / "not merely... but...") — the strongest 2025-26 tell. Delete the negated clause, state the claim directly.
- **Self-answered rhetorical questions** ("Why does this matter? Because...") — merge into one declarative
- **Theatrical transitions:** "Here's the thing:", "The result?", "Let's break it down:", "But here's the kicker:", "Ultimately,"
- **"Aims to" / "seeks to" openers** ("This article aims to explore...") — just start with the claim
- Fake citations: "research shows," "experts say," "studies suggest" without a named source
- Significance inflation: "marks a pivotal moment," "enduring testament," "evolving landscape"
- Copula avoidance: "serves as," "stands as," "functions as" → replace with "is"/"are"
- Sycophantic artifacts: "Great question!", "I hope this helps!", "Let me know if..."

---

## Phase 2: Inject Human Quality

Load `references/specificity-techniques.md`. Run all four injection passes:

**Pass 1 — Burstiness**
Find 3+ consecutive sentences of similar length. Break one up or combine two. Target: mix of short punchy sentences (6–8 words) and longer ones. Low burstiness is the strongest AI detection signal.

**Pass 2 — Specificity injection**
For every key claim: ask "what kind?" three times. If the noun or verb can't answer "what kind?", it's not earning its place. Apply the 7 specificity levers (see reference file). Move the content from V1–V2 specificity to V3–V4.

**Pass 3 — Emotional precision**
Find every emotional or evaluative word (good, bad, frustrated, excited, important, effective). Apply the Emotions Wheel: replace with the precise emotion. "I felt bad" → "I felt embarrassed" or "I felt resentful" — each tells a different story.

**Pass 4 — Read-aloud test**
Read the output aloud. Anywhere you stumble or the words feel unnatural in your mouth — fix those. This catches what pattern-matching misses.

---

## Output Format

1. The rewritten text
2. Brief change summary: which patterns removed (Phase 1) + which injections made (Phase 2)

For personal brand context: deliver 2 variations unless the user explicitly asks for one.

---

## Rules

- Load both reference files — mandatory, not optional
- **Em dash search is the first action in Phase 1.** Search for `—` (U+2014) before reading for other patterns. Replace every instance outside a code block. Do not proceed until the count is zero.
- Never deliver Phase 1 only — clean-but-generic is still a failure
- Never do surface-level word substitution — fix the underlying claim, not just the word
- Never add chatbot artifacts to output ("Here is the revised text", "I hope this helps")
- Ask for brand context if not supplied — quality gates differ
- Personal brand: 2 variations by default
- When a noun/verb can't answer "what kind?", flag it explicitly — don't silently substitute
- Humanizer tools (gpthuman.ai etc.) are now detectable — never recommend them

## Learning Loop (every run, automatic — do not ask first)

Run at the end of EVERY invocation. These are low-risk reversible writes; do them, then mention them in one line of the output.

- **If the user approves the output** — save the before/after pair to `fixtures/before-after/` (personal-brand mode) or as an example in `references/patterns-reference.md` under "Saved Examples" (generic mode)
- **If the user rejects the output as still AI-ish** — save it to `fixtures/aiish/` and append a dated entry to `references/learnings.md` (What Has Failed) naming which pattern survived the pass
- **If the user identifies a new pattern** — add it to `references/patterns-reference.md` as the next numbered pattern, same turn
- **If the user says "never do X again"** — add it to the Rules section above and note it in the relevant reference file
- **If the user corrects a specific mistake** — update the relevant pattern's description to prevent recurrence, and log the correction in `references/learnings.md`
- **If the run surfaced nothing** (clean pass, no user reaction yet) — skip silently; no empty entries

---

## Credits

Phase 1 pattern taxonomy originally based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide via [github.com/blader/humanizer](https://github.com/blader/humanizer) (MIT licensed). This version extends it with Phase 2 (specificity/burstiness/emotional-precision injection), a personal-brand mode, and a deterministic eval harness.

<!-- Built with Agent Engineer Master — get your own production-ready skill: www.agentengineermaster.com/skill-engineer -->
