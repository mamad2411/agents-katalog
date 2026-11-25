---
name: compare-competitors
description: Compare a subject against competitors with deep-research → matrix + gap list
argument-hint: "<subject> [alternatives...]"
related:
  - deep-research
  - alternative
  - apply
  - bench-competitors
  - idea-features
  - report
  - check-reference
  - ask-me
  - suggest-next-action

---

## Goal

Compare a subject (project, tool, library, feature) against alternatives systematically with `/deep-research`, producing a comparison matrix and a gap list where every claim has evidence, then generate idea features from the gaps

## Scope

Use when you need an evidence-based comparison between a subject and alternatives — features, capabilities, performance, pricing, DX — plus implementable feature ideas derived from the gaps

- If you need to find better new alternatives → use `/alternative` first
- If you need to pick the best option → use `/apply choose` (this skill produces the matrix, it does not decide)
- If comparing a project with competitors in order to implement something better → use `/bench-competitors` (which calls this skill internally)

## Execute

### 1. Define Subject And Alternatives

> Goal: Know what is being compared with what

1. Take `<subject>` and the list of alternatives from the argument or context
2. If no alternatives are given → run `/alternative` or `/deep-research` to find 3-5 relevant alternatives
3. If the subject or scope is unclear → use `/ask-me`

### 2. Define Comparison Criteria

> Goal: Know which dimensions to compare on

1. List the criteria/dimensions to compare, e.g. features, performance, DX, pricing, ecosystem
2. Use criteria that are measurable and relevant to the context
3. If the criteria are unclear → use `/ask-me` or defaults for the subject's domain

### 3. Deep Research Each Alternative

> Goal: Evidence behind every claim

1. Run `/deep-research` per alternative — official docs, changelogs, benchmarks, reviews, and user feedback
2. Run `/deep-research` or scan the codebase to confirm the subject's current state if information is lacking
3. Separate `fact` (backed by a source) from `assumption` (believed to exist)
4. If `/deep-research` cannot find the data → stop and report

### 4. Build Comparison Matrix

> Goal: A matrix that is easy to read, with every cell comparable

1. Run `/report` to build the comparison table — the `No.` column comes first
2. For each criterion, mark the subject's status versus the alternative with emoji + label: `✅ Has`, `❌ Missing`, `🟢 Better`, `🟡 Worse`, `⚪ Equal`
3. Every cell needs a source — without evidence, mark it as `assumption`
4. The summary row at the bottom of the matrix uses `🏆` for unique strengths and `🔺` for gaps to close

### 5. Extract Gaps And Uniques

> Goal: An actionable gap list plus the uniques to protect

1. Collect items where the subject is `❌ Missing` or `🟡 Worse` into a gap list — each gap lists: item, the alternative that has it, impact, rough effort, source
2. Identify the subject's unique strengths that alternatives lack — these must be preserved (mark `🏆`)
3. Set priorities: `🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Nice-to-have`
4. Output ready to hand off to `/create-plan-in-dot-devin`, `/apply choose`, or `/idea-features`

### 6. Generate Feature Ideas From Gaps

> Goal: Implementable feature ideas from the gap list

1. Run `/idea-features` fed with the gap list + unique strengths — each idea lists name, what, why (from the gap), rough effort, and source gap
2. Ideas must be own-brand — never copy an alternative's naming/terminology directly
3. Keep the idea list at the end of the output together with the matrix + gap list

## Rules

### 1. Evidence First

- Always use `/deep-research` whenever alternative data is needed — never guess from memory
- Every claim in the matrix must have a source (official docs are the primary source)
- Clearly separate `fact` from `assumption` — never conclude "worse" without evidence
- Every gap must map to an implementable item — split broad gaps into smaller ones

### 2. Comparison Not Decision

- Output is only the matrix + gap list + idea list — do not pick "the best one" and do not implement
- This skill only answers the comparison — if you want to compare and immediately implement better than competitors → use `/bench-competitors`
- Hand the picking decision to `/apply choose`; hand implementation to plan/implement skills

### 3. Matrix Format

- Every table has `No.` as its first column, numbered 1, 2, 3, ...
- Status always uses one fixed set with a leading emoji: `✅ Has`, `❌ Missing`, `🟢 Better`, `🟡 Worse`, `⚪ Equal`
- Priority in the gap list uses emoji: `🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Nice-to-have`
- The same criteria must be compared across every alternative — never skip a cell

### 4. Lightweight

- Never research deeper than necessary — just enough to decide has/missing/better/worse
- Keep the report concise, at most one A4 page per alternative
- Use /check-reference if needed
- Use /suggest-next-action if needed


## Expected Outcome

- Comparison matrix: subject vs alternatives across every criterion, with status and source per cell
- Prioritized gap list (Critical → Nice-to-have) with impact/effort
- Unique strengths to preserve
- Own-brand, implementable idea features
- Output ready to hand off to `/apply choose`, `/create-plan-in-dot-devin`, or `/idea-features`
