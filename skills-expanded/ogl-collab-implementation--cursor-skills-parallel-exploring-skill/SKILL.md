---
name: parallel-exploring
description: Decomposes broad codebase questions into parallel explore subagents with distinct lenses, then synthesizes a cited report. Use when the user wants to explore, investigate, scan, or understand the codebase — e.g. "how does X work", architecture, data flow, "find all places where", project structure, or says explore/investigate/dig into/look into.
---

# Parallel Exploring

Explore large or multi-faceted codebase questions by spawning **3–5 parallel `explore` subagents**, each with a different lens. Synthesize into one skimmable report with file paths and line numbers.

## When to use

Use for questions that span directories, layers, or concerns. Skip for single-file lookups or a known path (read/grep directly).

## Step 1: Size the codebase and pick agent count

Run a quick estimate (any one is enough):

```bash
find . -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.go' -o -name '*.rs' \) 2>/dev/null | wc -l
```

| Source files (approx.) | Subagents |
|------------------------|-----------|
| &lt; 500                 | 3         |
| 500 – 5,000            | 4         |
| &gt; 5,000               | 5         |

Adjust ±1 if the question is very narrow (fewer) or touches many unrelated areas (more, max 5).

## Step 2: Decompose into lenses

Map the user's question to **non-overlapping lenses**. Pick exactly as many lenses as subagents. Default pool — use only what fits the question:

| Lens | Focus |
|------|--------|
| **Entry & structure** | App entrypoints, package layout, modules, config wiring |
| **Core logic** | Domain algorithms, services, business rules |
| **Data & I/O** | Loaders, schemas, persistence, file/API I/O |
| **Integration** | CLI, UI, APIs, external deps, cross-module calls |
| **Tests & examples** | Tests, fixtures, notebooks, sample usage |

Each lens becomes one sub-question answerable without the others.

## Step 3: Spawn parallel Explore subagents

Use the **Task** tool with `subagent_type: "explore"`. Launch **all agents in one message** so they run in parallel.

Set `run_in_background: true` when spawning 3+ agents.

**Prompt template** (fill per lens):

```
You are exploring this codebase from one lens only.

Lens: [e.g. Data & I/O]
User question: [original question verbatim]
Your sub-question: [one focused question for this lens]

Instructions:
- Thoroughness: [quick | medium | very thorough] — default medium; use very thorough for large repos or deep traces
- Search relevant dirs if known: [paths or globs, or "discover from project root"]
- Return: bullet findings, each with file path and line number
- Do not speculate; say "not found" for gaps
- Stay within your lens; do not duplicate other lenses
```

**Example** (4 agents on "How does training work end-to-end?"):

| description | Lens / sub-question |
|-------------|---------------------|
| Explore train entrypoints | Entry & structure — entrypoints and `train` modules |
| Explore data pipeline | Data & I/O — dataset load and batch flow |
| Explore training loop | Core logic — loop, loss, optimizer, checkpoints |
| Explore eval after train | Integration — eval hooks and result output |

## Step 4: Synthesize

After all subagents return:

1. Merge duplicate paths; resolve conflicts by re-reading if needed.
2. **Connect the dots** across lenses (not a paste of four dumps).
3. Use this report shape:

```markdown
# [Topic]: Exploration Results

## Summary
[2–3 sentences; answer the user's question directly]

## [Lens 1 name]
- Finding … (`path:line`)

## [Lens 2 name]
…

## Gaps & next steps
[Unanswered parts; suggested follow-up searches]
```

Rules: every code claim gets a path (+ line); most important findings first; flag gaps explicitly.

## Anti-patterns

- Spawning 1–2 agents for repo-wide architecture questions (under-explores).
- Spawning &gt;5 agents (diminishing returns; merge lenses instead).
- Identical prompts with only wording changed (lenses must differ).
- Reporting without citations.

## Additional resources

- Eval scenarios for this repo: [.claude/skills/parallel-exploring/evals/evals.json](.claude/skills/parallel-exploring/evals/evals.json)
