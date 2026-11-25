---
name: session-context
audience: team
description: Git change summarization, ADR relevance matching, and pattern applicability for building session context. Provides techniques for analyzing recent project activity, scoring context relevance, and detecting patterns that accelerate AI coding session starts. Use when explicitly asked to prime/build context for a new coding session or onboarding. Do NOT use for a simple factual lookup like "what did I commit yesterday?" -- that's a plain `git log`, not a context-building request.
---

# Session Context

> "Context is worth 80 IQ points. The difference between a productive coding session and a stumbling
> one is whether you understood the state of the system before you started changing it."
> -- Alan Kay (attributed)

## Core Philosophy

Every AI coding session starts with a context gap: the model doesn't know what changed yesterday,
which architectural decisions govern this module, or which files are volatile. This skill bridges
that gap systematically, turning cold-start into a solved problem. Session context is not about
knowing everything — it is about knowing the *right* things. Relevant context, delivered concisely
at session start, prevents more bugs than any amount of testing after the fact.

**Non-Negotiable Constraints:**
1. RELEVANCE OVER RECENCY — score context by relevance to the focus area; recency is only a tiebreaker.
2. CITE EVERY CLAIM — every statement references a commit hash, file path, line number, or ADR; no exceptions.
3. SUMMARIZE, DON'T DUMP — never reproduce full ADRs, logs, or files; summarize with citations.
4. CONCISE SUMMARY — the executive summary fits one screen (< 40 lines); detailed sections are for drill-down.
5. OBSERVATION ≠ INFERENCE — label inferences explicitly; only verifiable facts are stated as facts.

Full principle table, the change-summarization and ADR-matching protocols, discipline rules,
anti-patterns, and error recovery live in `references/conventions.md`.

## Workflow

```
SCOPE       Define the focus area + time window (default 2 weeks active / 4 weeks less active);
            identify the repo root and branch topology.

GATHER      Collect raw context: git log --stat for the window, file change frequencies (hotspots),
            imports/deps in the focus area, ADR files + dates, convention files, README/design docs.
            (Protocols: conventions.md; techniques: change-summarization.md.)

SCORE       Rate each item: proximity to focus, recency weighting, ADR applicability, dependency
            relevance. Filter below the relevance threshold. (Scoring: relevance-matching.md.)

SYNTHESIZE  Group git changes by feature/area; rank ADRs by relevance; present the focused dependency
            subgraph; surface warnings (hotspots, overdue reviews, breaking changes); form recommendations.

DELIVER     Present the briefing (templates in output-templates.md): executive summary first
            (< 40 lines), detailed sections following, every claim cited, recommendations actionable.
```

**Exit criteria:** a briefing with a < 40-line executive summary, every claim cited, ADRs ranked by
relevance with stated reasons, dependency blast radius shown, staleness/hotspot warnings surfaced,
and specific session recommendations.

## State Block

```
<session-context-state>
mode: scope | gather | score | synthesize | deliver
focus_area: [files, modules, or features]
time_window: [date range]
repository: [path to repository root]
commits_collected: [count]
files_in_focus: [count]
adrs_discovered: [count]
adrs_relevant: [count]
dependencies_traced: [count]
hotspots_detected: [count]
relevance_threshold: [score cutoff]
last_action: [what was just completed]
next_action: [what should happen next]
</session-context-state>
```

## Output Template

- **Executive summary, change group, dependency context, hotspot analysis** — `references/output-templates.md`.
- **Git log analysis techniques (grouping, diff-stat, hotspot detection, branch topology)** — `references/change-summarization.md`.
- **Relevance scoring (proximity, recency, ADR applicability, dependency-path relevance)** — `references/relevance-matching.md`.
- **Principle table, summarization + ADR protocols, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `architecture-journal` | This skill surfaces relevant ADRs and overdue retrospectives; architecture-journal provides the templates and review protocols to act on them. |
| `dependency-mapper` | This skill traces dependencies at summary level for blast radius; dependency-mapper provides full Martin metrics (Ca, Ce, I, A, D) when patterns look concerning. |
| `qrspi-research` / `qraspi-research` | Use session-context as a pre-step to seed research with recent-change context before deeper codebase exploration. |
