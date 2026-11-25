---
name: context
description: >
  Maintain CONTEXT.md and the knowledge/ OKF bundle (glossary and concepts).
  Use when domain terms resolve or change, after implement or code-review, when
  adding OKF concepts, or when glossary and AGENTS.md risk duplicating each other.
---

# context

Own the glossary and OKF progressive-disclosure bundle. Do not edit `AGENTS.md` or `CLAUDE.md` — that is `upkeep`.

## Completion bar

Done when: every new or changed term is in `CONTEXT.md`; affected `knowledge/` concepts and `knowledge/index.md` match; no ops commands were pasted into the glossary.

## Workflow

### 1. Load the SoT

Read `CONTEXT.md` and `knowledge/index.md`. Note existing terms and concept paths.

**Done when:** current language map is in hand.

### 2. Capture resolved terms

For each settled term: definition (one or two sentences), `_Avoid_` aliases, no implementation detail. Update `CONTEXT.md` immediately — do not batch.

**Done when:** Language section reflects the session’s resolved vocabulary.

### 3. Maintain OKF concepts

When a term needs depth beyond the glossary line, add or update `knowledge/<slug>.md` with YAML frontmatter (`title`, `description`, `type`, optional `tags`) and link it from `knowledge/index.md` with a one-line blurb.

**Done when:** index entries match files on disk; links resolve.

### 4. Anti-duplication check

If `AGENTS.md` restates a glossary definition, leave a note for `upkeep` to replace with a link — do not rewrite `AGENTS.md` yourself unless the user explicitly asked this skill to fix both (default: do not).

**Done when:** glossary remains the only definition SoT.

## Format pointers

- Glossary shape: term, definition, `_Avoid_`
- Bundle entry: [knowledge/index.md](../../knowledge/index.md)
- Hard rules live in [CONTEXT.md](../../CONTEXT.md)
