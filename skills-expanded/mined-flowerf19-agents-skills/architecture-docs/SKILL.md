---
name: architecture-docs
description: Writes and updates lean project guidance, Feature Maps, and Tier-1-first rule documentation grounded in verified code and accepted decisions. Use when asked to write, audit, or simplify architecture docs, README.md, AGENTS.md, SKILL.md, or Feature Maps. Documentation only; do not edit runtime code.
license: MIT
---

# Architecture docs

Keep project guidance lean, verified against live code, and backed by Tier 1 guardrails and Feature Maps.

**Documentation only:** Edit only requested docs or guidance directly affected by an approved change. Never edit runtime code, tests, config, dependencies, or plan approvals to make docs true.

## Step 1: Verify Facts & Apply Tier-1-First Filter

1. Read the request, accepted decisions, current source, commands, and existing guides (`.agents/README.md`, `README.md`, Feature Map).
2. Verify every path, symbol, flag, and behavior against live files. Separate current behavior, unimplemented accepted decisions, and proposals.
3. **Tier-1-First Escalation Filter:** Before adding rules to `AGENTS.md` or skills, check if a compiler, typechecker, linter, or script can enforce them. Turn repeated mechanical agent mistakes into **Tier 1 lint rules** (what failed + root cause + exact fix; [lint-rules/README.md](../lint-rules/README.md)) instead of adding prose.

## Step 2: Ownership & Feature Map

1. Update the single doc owning the topic; link to shared rules instead of repeating them.
2. **Maintain the Feature Map:** Create and update the project Feature Map from [templates/feature-map.md](../templates/feature-map.md) (Feature ID, entrypoint/route/CLI, owning modules, invariants/contracts, and live runtime verification flow) so agents can code, test, and fuzz accurately.
3. Keep `README.md` focused on purpose, layout, install, usage, and executable checks. Delete stale paths and superseded workflow claims.

## Step 3: Write Concise Guidance

1. Follow the language and plain-writing rules in [AGENTS.md](../AGENTS.md). Explain necessary technical terms once in plain words and structure with tables and numbered steps.
2. Record only decisions an agent cannot infer from code. Never repeat rules already owned by [AGENTS.md](../AGENTS.md); link to them instead.
3. For skills, follow the Anthropic / Agent Skills specification: portable YAML frontmatter (`name` matching folder, <=64 chars; third-person `description` <=1024 chars with trigger and negative scope; optional `license`, `compatibility`, `metadata`, `allowed-tools`, `disable-model-invocation`), plus clear permissions, required artifacts, and stop conditions.

## Step 4: Check and Report

1. Verify all relative Markdown links, paths, commands, and cross-doc consistency.
2. Run [check-repo-skills.sh](../scripts/checks/check-repo-skills.sh) (and any project doc checks); never describe unexecuted flows as tested.
3. Report changed docs, check results, Tier 1 lint rule candidates, and unresolved conflicts.
