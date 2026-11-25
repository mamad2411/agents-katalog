---
name: deepwave
description: Deep web research with Opus synthesis (~70s to 10min). Use for "deep research", "comprehensive research", or multi-source synthesis.
user-invocable: true
---

# Searchwave Deep

Deep web research with Opus synthesis — Quick (~70s) / Standard (~90s) / Max (~5-10min).

## Overview

Three-tier research system with user-selected depth. All tiers use Opus
(model default) for synthesis. Max mode adds multi-agent research with
quality evaluation and follow-up loop.

**Token-efficient alternative:** Install `searchwave-sonnet` from the
marketplace for Sonnet synthesis variants with the same research architecture.

## When to Use

**Use /deepwave when:**
- User wants to select research depth
- Complex topics requiring multiple angles
- Need confidence assessment and source evaluation
- "Deep research" or "comprehensive" requests

**Use /wave instead when:**
- Quick lookup, no questions needed
- Simple factual questions
- Time-sensitive (< 60 sec)

**Use /searchwave-sonnet:deepwave instead when:**
- Token efficiency is a priority
- Sonnet synthesis quality is sufficient

---

## Phase 1: QA (~15 sec)

Use ONE AskUserQuestion call with 3-4 questions:

**Question 1 (only if needed): Clarification**
Include if query has ambiguity OR broad scope needing focus.

**Disambiguation** (different meanings):
- "Python" → programming language or snake?
- "Mercury" → planet, element, or band?

**Scope** (same meaning, what to cover):
- "home espresso" → machines? grinders? technique? beans? full setup?
- "AI in gaming" → NPC behavior? dev tools? procedural generation?

Skip for focused queries:
- "Python web frameworks" → clearly programming, clear scope
- "Gaggia Classic Pro review" → specific enough

**Question 2: Depth selection**
Always include:
```
"How deep should we go?"

- Quick (~1 min) — key facts, fast turnaround
- Standard (~2 min) — comprehensive research report
- Max (~5-10 min) — highest quality, multi-agent research, follow-up loop
```

**Question 3: Length preference**
Always include. Show options based on tier:
```
"Preferred length?"

Quick tier options: 500 / 800 / 1200 words
Standard tier options: 800 / 1200 / 1500 words
Max tier options: 800 / 1200 / 1500+ words (1500+ means Opus may extend to ~2500 if valuable)
```

**Question 4: Priority selection**
Always include, but GENERATE OPTIONS based on the specific query:
```
"What angle matters most?" (pick 1-2)

Generate 3-4 options relevant to THIS topic. Read the full query structure,
not just key terms — "shows like X" signals entertainment, "how X works" signals technical.

Examples:
- "terminal text display" → Configuration, How rendering works, Tools/solutions, Troubleshooting
- "sleep optimization" → Scientific research, Practical protocols, Products/tools, Recent findings
- "home espresso" → Equipment selection, Technique, Troubleshooting, Budget considerations
- "React state management" → Library comparison, Architecture patterns, Performance, Migration
- "shows like X" → Similar series, Themes/style, Behind the scenes, Critical reception

Always include one "Recent developments" option. NEVER include specific years in the description — just say "recent changes" or "latest approaches", not "2024-2025" or any year range.
```

---

## Quick Mode (~1 min)

Single orchestrator, Opus synthesis. Length options: 500 / 800 / 1200 words.

Print banner:
```
╔═════════════════════════════════════════╗
║           S E A R C H W A V E           ║
║                · · · · ·                ║
║      Searching: 3 parallel queries      ║
╚═════════════════════════════════════════╝
```

### Step 1: Search (parallel)

Fire 3 WebSearches in ONE message (all use `blocked_domains: ["medium.com"]`):
```
"$ARGUMENTS"
"$ARGUMENTS [user's first priority]"
"$ARGUMENTS interesting"
```

### Step 2: Fetch (parallel)

From search results, pick 3 best URLs. Skip Wikipedia for fetching (403s — use search snippets instead). Medium is blocked at search level.

Fire 3 WebFetches in ONE message.

### Step 3: Opus Synthesis

Spawn ONE Task with `model: opus` and `subagent_type: general-purpose`:

```
Research on "$ARGUMENTS" from web sources:

[Insert fetched content and relevant search snippets]

User priority: [from QA]
Target length: [user's length selection] words

---

Synthesize into a [length]-word briefing:

**Voice and approach:**
1. Survey voice — report what you found
2. Key facts and numbers only — no filler
3. Inline citations for all statistics: "According to X..."
4. One actionable takeaway if applicable

**Avoid AI writing patterns:**
- No dramatic reframes or hyperbole
- Let facts speak; don't editorialize
- Be concise, lead with numbers

**Line width formatting (critical for terminal readability):**
- Prose and bullet lists: hard-wrap at 80 columns
- Tables, code blocks, diagrams: NO width limit

Output format:
# [Topic] Briefing

## Summary
[2-3 sentences — what we found]

## Key Facts
[Bullet points with specifics and inline citations]

## Sources
[2-3 sources with one-line descriptions]

*Searchwave Deep (Quick) · [N] sources*
```

---

## Standard Mode (~2 min)

Single orchestrator, full Opus synthesis. Length options: 800 / 1200 / 1500 words.

Print banner:
```
╔═════════════════════════════════════════╗
║           S E A R C H W A V E           ║
║                · · · · ·                ║
║      Searching: 6 queries (2 waves)     ║
╚═════════════════════════════════════════╝
```

### Step 1a: Search batch 1 (3 parallel)

Fire 3 WebSearches in ONE message (all use `blocked_domains: ["medium.com"]`):
```
"$ARGUMENTS"
"$ARGUMENTS [user's first priority]"
"$ARGUMENTS [user's second priority, or 'guide' if only one selected]"
```

### Step 1b: Search batch 2 (3 parallel)

Fire 3 WebSearches in ONE message (all use `blocked_domains: ["medium.com"]`):
```
"$ARGUMENTS guide"
"$ARGUMENTS interesting"
"$ARGUMENTS recent"
```

If any search fails, retry it individually. Do not re-run the batch.

### Step 2a: Fetch batch 1 (3 parallel)

From all search results, pick 6 best URLs. Skip Wikipedia for fetching (403s — use search snippets instead). Medium is blocked at search level.

Priority order:
1. gov/institutional, domain authorities
2. Quality blogs, practitioner content
3. Reddit/forums (real user experience)
4. News sites (recent)

Fire 3 WebFetches in ONE message (top 3 URLs).

### Step 2b: Fetch batch 2 (3 parallel)

Fire 3 WebFetches in ONE message (next 3 URLs). If any fetch fails, proceed with available results.

### Step 3: Opus Synthesis

Spawn ONE Task with `model: opus` and `subagent_type: general-purpose`:

```
Research on "$ARGUMENTS" from web sources:

[Insert all fetched content and relevant search snippets]

User priorities: [from QA]
Target length: [user's length selection] words

---

Synthesize into a [length]-word report:

**Voice and approach:**
1. Survey voice — report what you found, present the landscape
2. Attempt neutrality — present information, let reader decide
3. Cut educational filler that doesn't serve the user's priorities
4. Keep hard numbers, specific protocols, concrete thresholds
5. Name frameworks or mental models when useful

**Inline citations (critical):**
Every statistic or factual claim must include source attribution inline:
- "According to McKinsey (2024)..."
- "One study found..."
Acknowledge source limitations when relevant.

**Avoid AI writing patterns:**
- No dramatic reframes ("It's not X, it's Y")
- No hyperbole words: "brutal", "game-changer"
- Let facts speak; don't editorialize
- Be concise, lead with numbers

**Line width formatting (critical for terminal readability):**
- Prose and bullet lists: hard-wrap at 80 columns
- Tables, code blocks, diagrams: NO width limit

Output format:
# [Topic] Research Report

## Summary
[3-4 sentences. What we found, not what we conclude.]

## [Section titles as appropriate — don't force structure]
[Content with inline citations, organized by what's most useful]

## Sources
[Deduplicated, one-line descriptions]

*Searchwave Deep (Standard) · [N] sources*
```

---

## Max Mode (~5-10 min)

Multi-agent research with quality evaluation and follow-up loop.
Length options: 800 / 1200 / 1500+ words (1500+ allows Opus to extend up to ~2500 if valuable).

Print banner:
```
╔═════════════════════════════════════════╗
║           S E A R C H W A V E           ║
║                · · · · ·                ║
║      Dispatching research agents        ║
╚═════════════════════════════════════════╝
```

### Step 1: Parallel Research (ONE message)

Fire 3 Task tools simultaneously with `run_in_background: true`:

**Agent A - Facts/Data** (the "what"):
```
Research "$ARGUMENTS" — focus on hard data, numbers, and studies.
Do 2 WebSearches (use blocked_domains: ["medium.com"]), pick 3 URLs (skip Wikipedia for fetching — use search snippets instead).
Prefer: .gov/.edu, research papers, official statistics, authoritative sources.
Do 3 WebFetches, write 400-word section.
Output: specific numbers, thresholds, study findings, comparisons. Tables encouraged.
Style: concrete > abstract, cite sources inline, no --- dividers.
```

**Agent B - Approaches/Application** (the "how"):
```
Research "$ARGUMENTS" — focus on practical application, approaches, common mistakes.
Do 2 WebSearches (use blocked_domains: ["medium.com"]), pick 3 URLs (skip Wikipedia for fetching — use search snippets instead).
Prefer: how-to guides, Reddit/forums for real experience, practitioner blogs, comparison articles.
Do 3 WebFetches, write 400-word section.
Output: actionable approaches, trade-offs, what to avoid, real-world experience.
Style: actionable > theoretical, include warnings, no --- dividers.
```

**Agent C - Mechanisms/Context** (the "why"):
```
Research "$ARGUMENTS" — focus on mechanisms, mental models, underlying processes.
Do 2 WebSearches (use blocked_domains: ["medium.com"]), pick 3 URLs (skip Wikipedia for fetching — use search snippets instead).
Prefer: educational content, explainers, technical deep-dives, expert breakdowns.
Do 3 WebFetches, write 400-word section.
Output: cause-effect relationships, how things work, frameworks for understanding.
Style: explain the "why" behind facts, cite sources inline, no --- dividers.
```

### Step 2: Wave 1 Collection (parallel, 90 sec timeout)

Call TaskOutput for ALL 3 agents in ONE message with `timeout: 90000`:
```
TaskOutput(task_id: A, block: true, timeout: 90000)
TaskOutput(task_id: B, block: true, timeout: 90000)
TaskOutput(task_id: C, block: true, timeout: 90000)
```

Proceed with available results. Do NOT print "Agent X completed" messages — collect silently.

### Step 3: Opus Evaluation

Print status banner:
```
╭─────────────────────────────────────────╮
│  Evaluating: Quality signals...         │
╰─────────────────────────────────────────╯
```

Spawn ONE Task with `model: opus` and `subagent_type: general-purpose`:

```
You are evaluating research quality on "$ARGUMENTS" before synthesis.

**Research collected:**
[Agent A output]
[Agent B output]
[Agent C output]

**User's original query:** "$ARGUMENTS"
**User priorities:** [from QA]

---

Evaluate these 4 quality signals:

1. **Source quality**: What's the ratio of authoritative sources (papers, .gov, experts)
   to shallow sources (marketing, listicles)? Score: HIGH / MEDIUM / LOW

2. **Query coverage**: Which aspects of the user's query are well-answered?
   Which aspects have gaps or thin coverage? List specific gaps.

3. **Named references**: Are there papers, frameworks, tools, or experts mentioned
   but not actually fetched/explored? List specific references worth pursuing.

4. **Contradictions**: Do sources disagree on key claims?
   Are there contested areas worth investigating further?

---

**Output format:**
DECISION: [SUFFICIENT or NEEDS_MORE]

If SUFFICIENT:
  Proceed to synthesis.

If NEEDS_MORE:
  GAPS: [specific gaps to address]
  REFERENCES: [specific references to fetch]
  CONTRADICTIONS: [specific disagreements to resolve]

  (Max 2-3 items total — prioritize highest value)
```

### Step 4: Targeted Follow-up (conditional)

**Only if Opus evaluation returns NEEDS_MORE.**

Print status banner:
```
╭─────────────────────────────────────────╮
│  Filling gaps...                        │
╰─────────────────────────────────────────╯
```

Spawn 1-2 targeted agents based on evaluation output:

```
For each gap/reference/contradiction identified:

Fire Task with `run_in_background: true`, timeout 60 sec:
  "Research [specific gap/reference/contradiction].
   Do 1-2 targeted WebSearches (use blocked_domains: ["medium.com"]), fetch 2-3 URLs.
   Write 200-word focused section addressing this specific point.
   Cite sources inline."
```

Collect with `TaskOutput(timeout: 60000)`. Proceed with available results.

**Max 2 waves total** — no infinite loops. If Wave 2 doesn't improve coverage, proceed anyway.

### Step 5: Opus Synthesis

Print status banner:
```
╭─────────────────────────────────────────╮
│  Building report...                     │
╰─────────────────────────────────────────╯
```

Spawn ONE Task with `model: opus` and `subagent_type: general-purpose`:

```
You have research on "$ARGUMENTS" from multiple sources:

**Wave 1 Research:**
[Agent A - Facts/Data output]
[Agent B - Approaches/Application output]
[Agent C - Mechanisms/Context output]

**Wave 2 Follow-up (if any):**
[Targeted research outputs]

**Quality evaluation:**
[Opus evaluation output — confidence levels, remaining gaps]

**User priorities:** [from QA]
**Target length:** [user's length selection] words (if 1500+, extend up to 2500 if genuinely valuable)

---

Synthesize into a research survey:

**Voice and approach:**
1. Survey voice — report what you found, present the landscape
2. Attempt neutrality — present information, let reader decide
3. Structure as: "We researched X, here's what we found"
4. Cut filler — remove content that doesn't serve stated priorities
5. Keep the specifics — hard numbers, exact protocols, concrete thresholds

**Inline citations (critical):**
Every statistic or factual claim must include source attribution inline:
- "According to McKinsey (2024)..."
- "A Gartner study found..."
- "One analysis suggests... (methodology unclear)"

Acknowledge source limitations when relevant:
- "This figure comes from a vendor report, so interpret with caution"
- "Sample size was small"
- "Methodology not disclosed"

**Avoid AI writing patterns:**
- No dramatic reframes ("It's not X, it's Y — it's Z")
- No hyperbole words: "brutal", "game-changer", "the entire story"
- No false confidence: "This should end the debate"
- Let facts speak; don't editorialize

**Plain language:**
- Be concise by default
- Lead with numbers, be direct and specific
- No corporate speak
- Simple prose over elaborate formatting

**Line width formatting (critical for terminal readability):**
- Prose and bullet lists: hard-wrap at 80 columns
- Tables, code blocks, diagrams: NO width limit

**Output format:**

# [Topic] Research Survey

## Summary
[2-3 sentences. What we found, not what we conclude.]

## [Section titles as appropriate — don't force structure]
[Content with inline citations: "According to X...", "Y reports that..."]
[Acknowledge source limitations where relevant]

## Confidence Assessment
- **High confidence:** [aspects with multiple authoritative sources]
- **Lower confidence:** [aspects with limited or conflicting sources]
- **Not addressed:** [aspects we couldn't find material on]

## Sources
[Deduplicated from all agents, one-line descriptions]

## Go Deeper?
Want me to explore any particular area further?

*Searchwave Deep (Max) · [N] sources*
(If follow-up wave was triggered, append: " · 2 waves")

IMPORTANT: The "Go Deeper?" section must be exactly as shown — one simple question.
Do NOT add bullet points, angle suggestions, or commentary about gaps.
```

### Step 6: Follow-up Loop

If user replies with an area to explore further:
1. Spawn 1-2 targeted agents (same pattern as Wave 2)
2. Collect results (60 sec timeout)
3. Append to output:

```markdown
---

## Follow-up: [Area name]

[300-500 words of additional findings, same survey style with inline citations]

### Additional Sources
[New sources from this follow-up]

## Go Deeper?
Want me to explore any other area?
```

4. Repeat until user says "done" or indicates they're finished.

### Failure Handling

| Failure | Behavior |
|---------|----------|
| Agent times out | Proceed with available results, note gap in Confidence Assessment |
| All Wave 1 agents fail | Return error, suggest retry or fall back to Standard mode |
| Wave 2 adds nothing | Proceed to synthesis, don't spawn more waves |
| Evaluation unclear | Default to SUFFICIENT, proceed to synthesis |

**CRITICAL: Output discipline**
- Return the Opus synthesis output ONLY — no wrapper text before or after
- Do NOT announce agent completions ("Agent X completed")
- Do NOT add commentary after the report ("Research complete...", "Let me know if...")
- The synthesis output IS the final response — nothing else
