---
name: how
version: "1.0.0"
model: opus
description: "Explain how a subsystem works or where code belongs: trace the flow, map the files, cite file:line. Use for \"how does X work\", walkthroughs before a change, layering questions. Read-only."
argument-hint: "[question about a subsystem, a flow, or where something should live]"
compatibility: Designed for Claude Code
---

# How: Explain a Subsystem

## Outcome Contract

- Outcome: an explanation a senior engineer new to the area can start working from: what it is, how a call flows through it, where things live, what trips people up.
- Done when: every section that applies is written, each claim about the code cites `file:line`, and what was not traced is listed rather than guessed.
- Writes: nothing. No file, plan or commit.

## Process

1. **Size it.** An ambiguous scope → state your reading and continue; the user can redirect. One module, a small utility or a narrow question → simple: trace it yourself and go to step 4. A subsystem across several files or services, a cross-cutting feature or a full overview → complex. When in doubt, simple.
2. **Explore (complex only).** Split the question into 2–4 angles, each a distinct slice. Spawn one `scout` per angle in one message, each briefed from [references/explorer-brief.md](references/explorer-brief.md), per `work` [work-swarm.md](../../stages/work/references/work-swarm.md).
3. **Reconcile (complex only).** Merge overlapping findings. Settle a contradiction by reading the code yourself, never by majority. A slice a scout could not trace: read it yourself, or list it under Open Questions.
4. **Explain.** Write the sections below, dropping any that do not apply. A placement question ("where should this live", "which layer owns this") is answered from the boundaries you found: name the owner and cite the code that shows it.

## Output

- **Overview** — 1–2 paragraphs: what it is, what it does, why it exists. A reader can stop here and decide whether to go on.
- **Key Concepts** — the types, services or abstractions the rest depends on, one line each.
- **How It Works** — the longest section: what triggers it, each step, where the data goes, the decision points. Prose with function names and `file:line`, not code dumps. Add a diagram (mermaid, or ASCII for a simple relation) only when components call each other or data changes shape across stages.
- **Where Things Live** — the few files to open first.
- **Gotchas** — surprising behavior, history, pitfalls.
- **Open Questions** — what you could not trace.

Name things concretely: "`install` calls `registry::update`", not "the service delegates to the registry". Explain why a part is complex; do not pad a simple one.

Defer to: `hunt` (a symptom to diagnose), `think` (a decision, or why it was built this way), `librarian` (code in another GitHub repo), `learn` (a domain rather than this codebase).
