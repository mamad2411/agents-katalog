---
name: plugin-skill-create
description: Use this skill when scaffolding a new skill (workflow, knowledge, or companion utility) under `plugin/skills/` and you need spec-conformant frontmatter, an eval test-case stub, and memory-write points pre-wired — the internal procedure for `/plugin-author create`. Generates a new skill INSIDE the ai-skills plugin conforming to the agentskills.io specification (https://agentskills.io/specification) and ai-skills plugin conventions. No longer slash-invocable — call `/plugin-author create <name>` instead. Read by the `prompt-engineer` agent at task start when DEV-ing or reviewing a plugin skill.
disable-model-invocation: true
---

# /plugin-skill-create — Plugin-Convention Skill Scaffold

Generate `plugin/skills/<name>/SKILL.md` plus eval/case stub plus memory-hook scaffolding. Conforms to:

1. **agentskills.io specification** — https://agentskills.io/specification (frontmatter, naming, directory layout, progressive disclosure)
2. **agentskills.io best practices** — https://agentskills.io/skill-creation/best-practices (description style, body length, calibration)
3. **agentskills.io description optimization** — https://agentskills.io/skill-creation/optimizing-descriptions (trigger phrasing, what+when, keywords)
4. **ai-skills plugin conventions** — H5 frontmatter trigger pattern, schema-validated frontmatter, `<untrusted_content>` G1 wrapping where applicable, G7 spawn payload format if the skill spawns subagents

The cached, offline-authoritative form of (1)–(3) is `prompt-engineering/skill-authoring-spec.md` + `prompt-engineering/optimizing-descriptions.md` — read those first; re-fetch the live URLs only when network is available.

## When to use

- Adding a new workflow skill to the plugin (e.g., a project-specific workflow)
- Adding a knowledge skill to the plugin
- Adding a companion utility skill

Not for: general-purpose Anthropic skill creation — use the upstream `skill-creator` for that. This scaffold ONLY targets plugin-convention skills under `plugin/skills/`.

## Invocation

```
/plugin-skill-create new-workflow --invocable --agent-spawn
/plugin-skill-create analyzer --type knowledge
/plugin-skill-create release-notes --type companion --invocable
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `<name>` (positional) | required | Lowercase + hyphens; ≤64 chars; must NOT clash with existing `plugin/skills/<name>/` |
| `--type` | `workflow` | `workflow` (full SDLC stage), `knowledge` (read-only reference), `companion` (helper) |
| `--invocable` | true (workflow + companion); false (knowledge) | Adds `context: fork` for slash invocation |
| `--agent-spawn` | off | Pre-wires G7 spawn payload section + return contract validation |
| `--ralph` | off | Pre-wires RALF Loop section per `ralph-budget.md` defaults |
| `--memory L4|L5` | off | Pre-wires memory write points per `memory-discipline.md` rule 1 |

## Behavior

1. Validate `<name>`:
   - Lowercase + hyphens only (per Anthropic skill name convention from docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
   - ≤64 chars
   - Does NOT collide with existing `plugin/skills/<name>/`
   - If collision: error and suggest `--overwrite` flag (but this skill never overwrites by default — minimum-change discipline)
2. Generate `plugin/skills/<name>/SKILL.md` with H5 frontmatter:

```yaml
---
name: <name>
description: Use this skill when <TODO: trigger phrase> — TODO replace this placeholder describing what the skill does.
context: fork           # if --invocable
argument-hint: "<arg>"  # if --invocable
disable-model-invocation: true  # if --type knowledge AND not --invocable
---
```

The `TODO —` token is a hard guard: `plugin-skill-audit` fails (CRITICAL severity) on any skill description that still contains `TODO`. This forces the scaffolded description to be edited before merge. Removing the literal `TODO` from your description is the gate that flips the audit from failing to passing.

3. Generate body skeleton:
   - `# /<name>` heading
   - Purpose section (placeholder)
   - When to use / Not for sections
   - Invocation examples (placeholder)
   - Arguments table (placeholder)
   - Behavior steps
   - Hard rules
   - Failure modes
   - Memory writes table (if `--memory`)
   - RALF Loop section (if `--ralph`)
   - G7 Spawn Payload + Return Contract section (if `--agent-spawn`)
   - Integration section: rules, hooks, schemas, companions

4. Generate `plugin/eval/cases/<name>/eval-case-001.json` stub (Tier 3):

```json
{
  "case_id": "<name>-001",
  "skill": "<name>",
  "input": {"prompt": "<test prompt>"},
  "expected": {"contains": ["<expected substring>"]},
  "judge_rubric": "plugin/eval/judge-rubrics/<name>.md",
  "judge_model": "haiku",
  "max_tokens_input": 30000,
  "max_tokens_output": 2000
}
```

5. Generate `plugin/eval/judge-rubrics/<name>.md` skeleton with the standard 5-dimension template.

6. Print summary: created files + next steps:
   - Fill placeholder content
   - Run `/plugin-skill-audit <name> --strict` to confirm spec compliance
   - Run `/eval --skill <name> --tier 1`

## Hard rules

Every scaffolded skill MUST satisfy the agentskills.io specification + ai-skills conventions below. The audit counterpart `/plugin-skill-audit` enforces the same rules — anything this skill emits MUST pass `/plugin-skill-audit <name> --strict`.

### agentskills.io spec, best-practices, scripts & description rules (cached digest)

The full cached rules live in two digests (read them before scaffolding — single source of truth, progressive disclosure; do NOT re-inline here):

- `prompt-engineering/skill-authoring-spec.md` — specification (frontmatter, naming, directory layout, 3-level progressive disclosure), best practices, using-scripts, and skill-output eval
- `prompt-engineering/optimizing-descriptions.md` — the `description` triggering surface (imperative phrasing, user-intent, be-pushy, trigger eval, 1024 hard limit)

Hard invariants every scaffold MUST satisfy (enforced by `/plugin-author audit --strict`):

- **`name`** 1–64 chars; lowercase a–z, digits, hyphens; no leading/trailing or consecutive (`--`) hyphens; MUST equal the parent directory name
- **`description`** 1–1024 chars; non-empty; what + when; trigger keywords; imperative; no `TODO` token (audit CRITICAL)
- **Body** ≤ 5000 tokens AND ≤ 500 lines recommended; file references one level deep from `SKILL.md`
- **Scripts/deps** (only when `scripts/` is generated): no interactive prompts (agents run non-interactive shells); `--help` usage; structured data → stdout, diagnostics → stderr; pinned deps or inline PEP 723 / equivalent — see the digest's "Using scripts in skills" section

### ai-skills plugin conventions

- **Body ≤ 12K chars** per project rule (matches the upstream ≤500-line recommendation)
- **Description in third person** — first-person breaks discovery
- **Form A**: every description **BEGINS with the literal `Use this skill when …`** phrase (ai-skills strict operationalization of upstream imperative phrasing; capability folded into the same sentence)
- **Never overwrite** existing skill — refuse if `plugin/skills/<name>/` already exists
- **Plugin-only scope** — never scaffolds skills outside `plugin/skills/`. For project-local skills use upstream `skill-creator`
- **English-only** per repo CLAUDE.md
- **No absolute user-machine paths** in templates or examples

## Best practices the scaffold bakes in

Sourced from the digest (`prompt-engineering/skill-authoring-spec.md` best-practices) — the scaffold output and the author MUST apply, not just cite:

- **Start from real expertise** — never generate a skill from generic LLM knowledge (produces vague generic procedures). Extract the pattern from a real completed task, or synthesize from project artifacts (runbooks, API specs, code-review comments, VCS history, real failure cases).
- **Refine with real execution** — the first draft is a draft. Run against real tasks, feed ALL results back (not just failures), read execution traces; wasted steps ⇒ vague/inapplicable/duplicate instructions.
- **Design coherent units** — one skill = one coherent capability. Too narrow ⇒ many skills per task; too broad ⇒ imprecise activation.
- **Output-format templates** — emit a concrete template (agents pattern-match well); short inline, long → `assets/`, referenced.
- **Checklists** for multi-step workflows; **plan-validate-execute** for batch/destructive ops (intermediate plan → validate vs source of truth → execute).
- **Bundle on reinvention** — if traces show the agent re-deriving the same logic each run, ship a tested script in `scripts/`.

## Scripts & dependencies (when the skill ships `scripts/`)

Sourced from the digest's "Using scripts in skills" section:

- **One-off runners** over committed code where possible: `uvx`/`pipx run` (Python), `npx`/`bunx` (Node), `deno run` (`--allow-*`), `go run`. **Pin versions** (`npx eslint@9.0.0`).
- **Inline deps** — Python PEP 723 block + `uv run scripts/x.py`; pin via PEP 508; `requires-python`. State runtime-level prerequisites in the `compatibility` frontmatter field, not body prose.
- **Non-interactive (HARD)** — no TTY-blocking prompts; input via flags/env/stdin; clear error+usage when a required input is missing.
- **`--help`** documented per script; **structured output** (JSON/CSV/TSV) → stdout, progress/diagnostics → stderr.
- **Documented exit codes** per failure type; **idempotency** ("create if not exists"); **`--dry-run`** for destructive/stateful ops; **predictable output size** (harnesses truncate ~10–30K chars — default to a summary, support `--offset`, or require `--output FILE|-`).

## Failure modes

- **Name collision:** refuse, suggest different name
- **Name fails validation:** refuse with examples of valid names (e.g., `release-notes`, NOT `Release Notes` or `releasenotes`)
- **Permission denied on write:** report path; suggest checking plugin/ writeability

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | After scaffold | `.ai-skills-memory/plugin-skills/<name>/scaffolded.md` — timestamp + flags used |

## Integration

- **Status**: internal procedure document for `/plugin-author create`. Not slash-invocable (frontmatter `disable-model-invocation: true`). The umbrella reads this file directly when scaffolding a new asset; `ai-skills:prompt-engineer` pre-reads it before any plugin-asset DEV pass.
- **Reachable via**: `/plugin-author create <name> [--type workflow|knowledge|companion] [--agent-spawn] [--ralph]`
- **Writes to**: `plugin/skills/<name>/`, `plugin/eval/cases/<name>/`, `plugin/eval/judge-rubrics/<name>.md`
- **References**:
  - `prompt-engineering/skill-authoring-spec.md` — cached spec + best-practices + scripts + eval digest (offline source of truth)
  - `prompt-engineering/optimizing-descriptions.md` — cached description-triggering digest
  - agentskills.io specification — https://agentskills.io/specification
  - agentskills.io best practices — https://agentskills.io/skill-creation/best-practices
  - agentskills.io description optimization — https://agentskills.io/skill-creation/optimizing-descriptions
  - Anthropic Agent Skills best-practices — https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- **Templates**: H5 frontmatter pattern, G7 schemas (if `--agent-spawn`), `ralph-budget.md` defaults (if `--ralph`)
- **Companion procedure**: `plugin/skills/plugin-skill-audit/SKILL.md` — audit + safe-fix discipline applied by `/plugin-author audit`.
