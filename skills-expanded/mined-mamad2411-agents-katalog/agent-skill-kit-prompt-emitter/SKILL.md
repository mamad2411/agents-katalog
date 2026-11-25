---
name: agent-skill-kit-prompt-emitter
description: Emit progressive-disclosure artifacts from a skills tree — an `<available_skills>` XML block for stage-1 agent startup, or canonical JSON of frontmatter properties for CI consumption. Use when the user asks to export skill metadata, build a prompt block, generate JSON for CI, or wire skills into an agent host.
tier: app
license: Apache-2.0
compatibility: requires `skills-ref` CLI; reads files only — no network
---

# Agent Skill Prompt Emitter

Wraps two read-only export verbs of the `skills-ref` CLI. Both build on the validator's frontmatter parser and the dependency resolver's toposort — no separate YAML re-parsing, no network calls.

## When to use

- "Emit the available_skills block for our agent host"
- "Give me JSON of every skill's frontmatter for the CI pipeline"
- "Export the skills tree as a single XML/JSON artifact"
- "Build a stage-1 system prompt section listing skills the agent can reach"

## `to-prompt` — XML for stage-1 agent startup

```bash
skills-ref to-prompt <root> [--max-tokens N] [--include-invalid]
```

Output (excerpt):

```xml
<available_skills>
  <skill name="agent-skill-kit-creator" tier="org">Scaffold a new spec-compliant Agent Skill...</skill>
  <skill name="agent-skill-kit-validator" tier="org">Validate one or many SKILL.md files...</skill>
  ...
</available_skills>
```

Children are ordered by the topological order from `skills-ref deps` — dependencies appear before consumers, so a host that scans the block top-to-bottom never references a skill it has not yet seen. The XML escapes the five mandatory characters (`& < > " '`); two-space indentation is fixed; there is no line-wrapping inside `<skill>` elements; the trailing newline is always present.

Truncation: when `--max-tokens N` is set, the cumulative character count divided by four is compared to `N`; if it overflows, the lowest-priority skills (last in topological order) are dropped and a `<truncated count="K"/>` marker is appended immediately before the closing element. Token estimation is `chars / 4` — a deterministic approximation, not a real BPE count.

Invalid skills: by default, skills that fail to parse are silently skipped. `--include-invalid` includes them with an `invalid="true"` attribute and the parse-error message in the description slot for debugging.

## `read-properties` — JSON for CI and downstream tooling

```bash
skills-ref read-properties <skill-dir>          # one skill -> object
skills-ref read-properties --root <root-dir>    # tree      -> array
```

Stable JSON shape: every spec-defined frontmatter field as a top-level key (`null` when absent in the source), plus a synthetic `_path` pointing at the source SKILL.md. Canonical key order via sort-keys, two-space indent, UTF-8 output (non-ASCII characters preserved verbatim).

Example (single mode):

```json
{
  "_path": "/abs/path/.agents/skills/agent-skill-kit-creator/SKILL.md",
  "allowed_tools": [],
  "compatibility": null,
  "dependencies": [],
  "description": "Scaffold a new spec-compliant Agent Skill...",
  "license": "Apache-2.0",
  "metadata": {},
  "name": "agent-skill-kit-creator",
  "tier": "org"
}
```

`--root` returns an array of these objects ordered alphabetically by `name`.

## Exit codes

| Code | Meaning |
| ---- | ------- |
| `0`  | Success — XML or JSON written to stdout. |
| `1`  | `to-prompt`: registry has cycles, missing in-repo dep targets, or another graph-level defect. `read-properties`: frontmatter parse failure (missing or malformed delimiter). |
| `2`  | No SKILL.md found under the target path. |
| `64` | Usage error. |

## Two-mode CLI contract for `read-properties`

- A positional `<skill-dir>` invokes single-skill mode and returns one JSON object.
- `--root <root-dir>` invokes tree mode and returns a JSON array.
- The two are mutually exclusive: pick one.

## Limits

- Token estimation for `--max-tokens` is `chars / 4`. A real BPE counter would force a per-runtime tokenizer dependency and still be model-specific. The approximation is deliberately conservative — under-counting overhead, never over-counting — so a host that sizes its budget from the result has slack.
- The XML serializer is intentionally tiny and dependency-free. It only emits the shape the stage-1 contract requires (`<available_skills>` with `<skill>` children plus an optional `<truncated/>`). Do not extend it for richer XML.
- `read-properties` emits absolute paths in `_path` so a downstream consumer can open the file without ambient cwd context.

## Reference

Full specification: see the canonical spec at [../../../agentskills.io.md](../../../agentskills.io.md).
