---
name: persona-write
description: Install this skill set to draft, rewrite, audit, and refine text through a specific writing persona using a multi-pass workflow. Handles both short text and long-form documents.
install: npx skills add DurdeuVlad/persona-write
version: 2.3.0
skills:
  - persona-write
  - persona-review
  - persona-copy
  - persona-list
  - persona-create
  - persona-brief
  - persona-localize
  - persona-research
  - persona-wordcheck
---

# Installing Persona Write

---

## For Claude Code users

### Requirements

- [Claude Code](https://claude.ai/code)

### Install

```bash
npx skills add DurdeuVlad/persona-write
```

Add `-g` for a global install, or `--skill <name>` to install a single skill.

**Manual install (no CLI):**

```bash
git clone https://github.com/DurdeuVlad/persona-write.git
```

**Fresh `.claude/` setup:**
```bash
cp -r persona-write/.claude /your-project/.claude
```

**Existing `.claude/skills/` folder:**
```bash
cp -r persona-write/.claude/skills/persona-write /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-review /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-copy /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-list /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-create /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-brief /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-wordcheck /your-project/.claude/skills/   # persona-write calls it at pipeline step 10
cp -r persona-write/.claude/skills/persona-research /your-project/.claude/skills/
cp -r persona-write/.claude/skills/persona-localize /your-project/.claude/skills/
```

No configuration files. No environment variables. No package installs.

### Verify

Open Claude Code in your project and run:

```
/persona-list
```

Seven preset personas listed with descriptions. If command not found, check skill folders are in `.claude/skills/` at project root.

### Usage

```
/persona-write sharp-technical rewrite:
[paste text]
```

```
/persona-write pragmatic-builder draft:
Write an explanation of how our CI pipeline works, for a new engineer joining the team.
```

```
/persona-write:
Make this sound like a skeptical analyst who cares about evidence and does not overclaim.
[paste text]
```

No persona given? The skill asks you to pick one.

### Updating

```bash
cd persona-write && git pull
cp -r .claude/skills/persona-write /your-project/.claude/skills/
cp -r .claude/skills/persona-review /your-project/.claude/skills/
cp -r .claude/skills/persona-copy /your-project/.claude/skills/
cp -r .claude/skills/persona-list /your-project/.claude/skills/
cp -r .claude/skills/persona-create /your-project/.claude/skills/
cp -r .claude/skills/persona-brief /your-project/.claude/skills/
```

---

## For other AI agents

This repo is built for Claude Code, but the core system is plain Markdown. Any AI agent that can read files and follow instructions can use it.

### What matters

The system lives entirely in `.claude/skills/`. Copy that folder wherever your agent can read it.

```
.claude/skills/
  persona-write/     ← main skill — this is the one that does the work
  persona-review/    ← review existing text through a single reviewer persona
  persona-copy/      ← extract a writer's style from samples and reproduce it
  persona-list/      ← optional, helps the agent explain available personas
  persona-create/    ← optional, helps users build custom personas
  persona-brief/     ← optional, builds a reader brief before drafting
```

**Minimum viable install:** copy just `persona-write/` and point your agent at `persona-write/SKILL.md` as the entry point.

### What to tell your agent

Give your agent this instruction:

```
You have access to a writing persona system located at .claude/skills/persona-write/.

- SKILL.md describes what the skill does and how to use it
- personas/ contains the available persona definitions
- passes/ contains the step-by-step pass instructions
- longform/ contains the long-form document workflow
- dictionaries/ contains patterns to avoid

When the user asks to write, rewrite, audit, or refine text in a specific voice,
load the relevant persona from personas/ and follow the workflow in SKILL.md.
```

### What each folder does

| Folder | Purpose | Required? |
|---|---|---|
| `SKILL.md` | Entry point — persona resolution, mode handling, full workflow | Yes |
| `personas/` | One file per persona. Each defines identity, attention model, compression, stance, rhythm, taboos, failure modes | Yes |
| `passes/` | Step-by-step instructions for each internal pass (intent extraction, diagnostic audit, rewrite, scrub, etc.) | Recommended |
| `longform/` | Section-by-section workflow for large documents — global brief, chapter memory, revision tickets, consistency pass | Recommended for longform use |
| `dictionaries/` | Banned phrases, manager speak, AI writing patterns — reference material for the scrub pass | Recommended |
| `docs/` | Philosophy, pipeline explanation, contributor guide — context for humans and agents that want to understand the system | Optional |
| `examples/` | Worked examples for quickstart, rewrite, audit, and longform modes | Optional |

### Adding a custom persona

Create a `.md` file in `personas/` using the schema in `persona-create/template.md`. The agent will find it alongside the presets — no registration needed.

### How the workflow runs

**Short text:**
1. Resolve persona & create task-specific scratch folder
2. Extract intent (`01-intent.md`)
3. Diagnostic audit (`02-audit.md`)
4. Persona mapping (`03-mapping.md`)
5. Build sentence by sentence (`04a-skeleton.md`, `04b-sentences.md`, `04-draft.md`)
6. Voice coherence (`05-coherence.md`)
7. Refine (`06-refine.md`)
8. Native fluency, when the target is not English (`06b-native.md`)
9. Word check (`06c-wordcheck.md`)
10. Fidelity check (`07-fidelity.md`)
11. Cold reader, when the stakes call for it (`07b-cold-reader.md`)
12. Proofread (`08-proofread.md`)

**Long-form documents:**
1. Build global brief & document map in scratch folder
2. Process one section at a time, running the full short-text pipeline for each
3. Write chapter memory after each section
4. Log revision tickets when later sections affect earlier ones
5. Whole-document consistency pass
6. Assemble final output

---

## What you get

| Skill | Entry point | Purpose |
|---|---|---|
| persona-write | `persona-write/SKILL.md` | Draft, rewrite, audit, or refine text in a target persona |
| persona-review | `persona-review/SKILL.md` | Review existing text through a single reviewer persona, applying surgical fixes |
| persona-copy | `persona-copy/SKILL.md` | Extract a writer's style from samples and reproduce a new piece at matched quality |
| persona-list | `persona-list/SKILL.md` | Browse and explain the available preset personas |
| persona-create | `persona-create/SKILL.md` | Build a custom persona in plain language |
| persona-localize | `persona-localize/SKILL.md` | Adapt a text to a target language and locale so it reads as native |
| persona-research | `persona-research/SKILL.md` | Research genre norms and check claims against sources before writing |
| persona-wordcheck | `persona-wordcheck/SKILL.md` | Check every word and sentence for fit to the context and correct use in the target language |
| persona-brief | `persona-brief/SKILL.md` | Build a reader brief (what the reader knows, needs, and should do) before drafting |

**Preset personas:** `sharp-technical`, `pragmatic-builder`, `clear-teacher`, `skeptical-analyst`, `blunt-operator`, `problem-first-marketer`

---

## Design constraints

This skill does not optimize for AI detector scores. The goal is writing that sounds like a specific kind of person — not writing that games a classifier.

Full design rationale: `.claude/skills/persona-write/docs/philosophy.md`
