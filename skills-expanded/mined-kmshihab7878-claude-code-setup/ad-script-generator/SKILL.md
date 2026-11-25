---
name: "ad-script-generator"
description: "Generate 100+ ad script variations from competitor intelligence. Takes ad-research output, rewrites competitor angles in brand voice, multiplies across ICPs, and produces production-ready scripts for UGC creators and AI video (Arcads). Use when creating ad scripts, generating creative variations, writing ad copy at scale, or building a creative testing pipeline. Mirrors Eddie's Stage 3 (Script Generation)."
risk: low
tags: [growth, marketing, content, creative]
created: 2026-03-23
updated: 2026-03-23
---

# Ad Script Generator — Volume Creative Engine

Generate dozens to hundreds of ad script variations from proven competitor patterns, rewritten in your brand voice and multiplied across ICPs. This is UAOP Stage 3 (Variation Generation) for the Growth department.

## When to use

- After running `ad-research` and having a competitive intel dump
- When you need fresh ad creatives for testing
- When existing ads are burning out (fatigue after 4-6 weeks)
- When expanding to a new ICP or product surface
- Monthly creative refresh cycles

## When NOT to use

- Competitor research (use `ad-research` first)
- Performance analysis of running ads (use `ad-performance-loop`)
- Brand strategy or positioning work (use `brand-guidelines` or `marketing-strategy-pmm`)

## Prerequisites

Before running, ensure these files are loaded:

```
REQUIRED CONTEXT:
1. ~/.claude/contexts/writing-rules.md        (anti-slop filter)
2. ~/.claude/contexts/growth/voice.md          (brand communication style)
3. ~/.claude/contexts/growth/rules.md          (growth invariants)
4. ~/.claude/contexts/growth/products/{surface}.md  (product facts)
5. ~/.claude/contexts/growth/icps/{icp}.md     (ideal customer profiles)
6. Ad research intel dump (from ad-research skill)
```

## Pipeline

### Step 1: Ingest Competitor Intel

Load the competitive ad intel dump from `ad-research`. For each competitor ad:
- Extract the hook, angle, structure, and body copy
- Rate reusability: High (proven angle, easy to adapt) / Medium / Low
- Filter to High + Medium reusability ads only

### Step 2: Rewrite in Brand Voice

For EACH high-reusability competitor ad, produce 2 outputs:

**Output A — Original Analysis:**
```markdown
## Original: [Competitor] Ad #[N]

**Hook:** "[exact hook]"
**Angle:** [angle type]
**Structure:** [hook → problem → solution → proof → CTA]
**Why it works:** [specific analysis]
**Body copy:** "[exact copy]"
**Transcript:** "[if video]"
```

**Output B — Brand Rewrite:**
```markdown
## Rewrite: [Our Product] — Based on [Competitor] Ad #[N]

**Hook:** "[rewritten hook in our voice]"
**Angle:** [same angle, our positioning]
**Structure:** [same structure, our product facts]

### Script (Video — 30 seconds)

[HOOK — 0-3s]
"[opening line — must stop the scroll]"

[PROBLEM — 3-8s]
"[pain point in ICP's language]"

[SOLUTION — 8-18s]
"[our product solving it — specific features/benefits]"

[PROOF — 18-25s]
"[testimonial/stat/demo]"

[CTA — 25-30s]
"[clear call to action]"

### Body Copy (for static/carousel)
Headline: "[headline]"
Primary text: "[body copy]"
CTA: "[button text]"
```

### Step 3: ICP Multiplier

Take each rewrite and multiply across ICPs:

```
For each rewrite:
  For each ICP in ~/.claude/contexts/growth/icps/:
    → Adapt language to ICP's vocabulary
    → Swap pain points to ICP-specific problems
    → Adjust proof points to what ICP cares about
    → Keep the same angle and structure
```

**Example:** If you have 20 rewrites and 3 ICPs, you get 60 scripts.

### Step 4: Variation Generation

For top-performing angles (identified by ad-performance-loop or human judgment):

```
For each top script:
  → Generate 3-5 hook variations (different opening lines, same angle)
  → Generate 2-3 length variations (15s, 30s, 60s)
  → Generate 2 tone variations (serious vs. casual)
```

This multiplies 60 scripts into 100-300+ variations.

### Step 5: Production Routing (UAOP Stage 4)

Sort scripts into two pipelines:

**Pipeline A — UGC Creators (Top 10-15):**
- Highest-conviction scripts (proven angle + strong hook + clear ICP fit)
- Include: script + reference competitor video + brand voice guide
- Budget: $15-50 per video
- Format: Creator brief with shot list

**Pipeline B — AI Video (Remaining):**
- All other scripts go to Arcads (or equivalent) via API
- Same script → 3-5 different AI actors
- Same actor → 5-10 different hooks
- Output: 50+ finished video ads per batch

## Output Format

### Script Document
```markdown
# Ad Script Batch — [Date]

## Batch Summary
- Competitor ads analyzed: [N]
- Rewrites generated: [N]
- ICP multiplication: [N] ICPs × [N] rewrites = [N] scripts
- Hook variations: [N]
- Total scripts: [N]

## Pipeline A — UGC Creator Scripts (Top [N])
[numbered list with full scripts + reference videos]

## Pipeline B — AI Video Scripts (Remaining [N])
[numbered list with full scripts + actor recommendations]

## Angle Breakdown
| Angle | Scripts Using | Source Competitors | Expected Performance |
|-------|--------------|-------------------|---------------------|
```

## Anti-Slop Rules (Mandatory)

Before finalizing ANY script:
1. Run through `anti-ai-writing` banned word list — zero tolerance
2. Check against `growth/voice.md` — must sound human
3. Verify product facts against `growth/products/{surface}.md`
4. Ensure ICP language matches `growth/icps/{icp}.md`
5. Read the script aloud — if it sounds like an AI wrote it, rewrite it

## Tools Used

| Tool | Purpose |
|------|---------|
| memory MCP | Load competitor intel, store winning scripts |
| sequential MCP | Multi-step reasoning for rewrites |
| filesystem | Read context files (voice, product, ICP) |

## Agents

| Agent | Role |
|-------|------|
| growth-marketer (L2) | Owns script strategy, selects top scripts |
| content-strategist (L3) | Writes rewrites, ensures voice consistency |
| prompt-engineer (L3) | Optimizes script templates for quality |
| analytics-reporter (L3) | Tracks which angles produce winners |
