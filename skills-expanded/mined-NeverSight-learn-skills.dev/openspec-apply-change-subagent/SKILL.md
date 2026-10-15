---
name: openspec-apply-change-subagent
description: Apply an OpenSpec change by grouping pending tasks by scope, delegating implementation to subagents, and keeping the main agent focused on openspec-cn state, context reading, review, and progress reporting.
---

# openspec-apply-change-subagent

Implement OpenSpec change tasks through orchestration.

## Platform Adapter

This skill is platform-neutral. It uses **logical role names** for implementation specialists and resolves each to a concrete subagent at runtime via the four-tier fallback below.

### Role registry

| Implementation group | Logical Role | agency-agents source | Source path |
|---|---|---|---|
| Frontend | `Frontend Developer` | `engineering/engineering-frontend-developer.md` | `name: Frontend Developer` |
| Backend/API | `Backend Architect` | `engineering/engineering-backend-architect.md` | `name: Backend Architect` |
| Data/database | `Data Engineer` / `Database Optimizer` (see selection rule below) | `engineering/engineering-data-engineer.md` / `engineering/engineering-database-optimizer.md` | `name: Data Engineer` / `name: Database Optimizer` |
| Infrastructure | `DevOps Automator` | `engineering/engineering-devops-automator.md` | `name: DevOps Automator` |
| Generic focused fix | `Minimal Change Engineer` | `engineering/engineering-minimal-change-engineer.md` | `name: Minimal Change Engineer` |

**Data/database selection rule**: prefer `Database Optimizer` when the task touches query plans, indexes, or schema migrations; otherwise use `Data Engineer`. When the task spans both concerns, dispatch both in parallel.

### Four-tier fallback (per group, resolved at dispatch time)

For each implementation group, resolve the specialist in this order:

1. **Registered agent** (`registered`) — If the runtime has the agency-agents agent installed (by `name` or `@<slug>` where slug = `slugify(name)`, e.g. `Frontend Developer` → `@frontend-developer`), dispatch it directly. This is the strongest tier.
2. **Local cache** (`local`) — If not registered, check whether `~/.agency-agents/<slug>.md` exists. If it does, read it, validate it (YAML frontmatter `---` + `name:` field), and embed the markdown body (skip frontmatter) as the role prompt for a generic subagent. No network access needed.
3. **Remote fetch** (`fetched`) — If the local cache file is missing or invalid, fetch from jsDelivr into `~/.agency-agents/`, then embed it as in tier 2.
4. **Embedded prompt** (`embedded`) — If the network is unavailable or the fetch fails validation, use the embedded fallback prompt below.

Tiers 2 and 3 deliver the same content as a registered agent (the full agency-agents source), just via a generic subagent. Tier 4 is a condensed prompt and is weaker.

**How to fetch** (tier 3): ensure the cache directory exists, then fetch:

```bash
mkdir -p "$HOME/.agency-agents"
# Check local cache first (tier 2)
[ -f "$HOME/.agency-agents/<slug>.md" ] && cat "$HOME/.agency-agents/<slug>.md" && exit 0
# Remote fetch (tier 3)
curl -fsSL --max-time 10 "https://cdn.jsdelivr.net/gh/msitarzewski/agency-agents@main/<path>" -o "$HOME/.agency-agents/<slug>.md"
# e.g. https://cdn.jsdelivr.net/gh/msitarzewski/agency-agents@main/engineering/engineering-frontend-developer.md
```

Or use any available web-fetch tool on the same URL, writing the result to `~/.agency-agents/<slug>.md`. Validate the fetched content before use (it must contain a YAML frontmatter block starting with `---` and include a `name:` field). If validation fails, delete the cached file and fall through to the embedded prompt. Extract the markdown body (skip the YAML frontmatter) and use it as the role prompt for a generic subagent.

**Embedded prompts** (tier 4, used when fetch fails):

- **Frontend Developer**: "You are a frontend developer. Implement the task using modern web technologies. Follow existing patterns in the codebase. Ensure accessibility and responsive design where applicable."
- **Backend Architect**: "You are a backend architect. Implement the task following existing API patterns, error handling conventions, and data models. Ensure backward compatibility."
- **Data Engineer / Database Optimizer**: "You are a data engineer. Implement the task following existing schema conventions, migration patterns, and query optimization practices."
- **DevOps Automator**: "You are a DevOps automator. Implement the task following existing IaC patterns, CI/CD conventions, and deployment practices."
- **Minimal Change Engineer**: "You are a minimal-change engineer. Implement only the specified task with the smallest possible diff. Do not add abstractions, config, dependencies, or features unless the task explicitly requires it. Do not touch unrelated code."

### Tier echo and review impact

Note the resolved tier for each group in the progress report (Workflow step 7). Tier affects review confidence:

- **All groups `registered` or `local` or `fetched`** → standard review. Tiers 1-3 all deliver the full agency-agents source content.
- **Any group `embedded`** → flag in the progress report; the main agent should apply extra scrutiny during review (Workflow step 6), since an embedded condensed prompt is a weaker specialist than the full agency-agents source.

### Platform rules

- Do not use Claude Code `Agent tool`, `Task tool`, or `subagent_type`.
- Do not use `codex:codex-rescue` (it is a Claude-hosted bridge, not a standalone agent).
- Dispatch all dependency-ready groups in parallel when the runtime supports it; otherwise run waves serially preserving dependency order.

## Inputs

The user may provide a change name. If omitted:

1. Infer it from conversation when unambiguous.
2. If exactly one active change exists, use it.
3. Otherwise run:

```bash
openspec-cn list --json
```

Ask the user to choose only when the change cannot be safely inferred.

Always announce:

```text
正在使用变更：<name>
```

## Workflow

1. Inspect status:

```bash
openspec-cn status --change "<name>" --json
```

Read `schemaName` and locate the artifact that contains tasks.

2. Fetch apply instructions:

```bash
openspec-cn instructions apply --change "<name>" --json
```

Handle states:

- `blocked`: report missing artifacts and suggest continuing the change definition.
- `all_done`: report completion and suggest archive.
- otherwise continue.

3. Read context files yourself.

Read every file listed in `contextFiles` before grouping or delegation. Do not assume fixed filenames; follow CLI output.

4. Group pending tasks by scope.

Scope means subproject, module, technology stack, capability area, or ownership boundary. Prefer groups of 3-8 tasks. Identify dependencies between groups and produce:

```text
## 任务分组：<change-name>（Schema：<schema-name>）

待处理任务 M 个，按范围分为 K 组：

- 组 A — <范围名>（N 个任务）：任务 1, 2, 5
- 组 B — <范围名>（N 个任务）：任务 3, 4

依赖：组 A 独立；组 B 依赖组 A。
```

5. Delegate implementation.

Dispatch all dependency-ready groups in parallel when the runtime supports it; otherwise run waves serially preserving dependency order.

Each subagent prompt must include:

- Change name and schema name.
- The complete task text for the group.
- Absolute paths to all relevant context files.
- The task file path.
- The rule: after completing a task, immediately change that task checkbox from `- [ ]` to `- [x]`.
- Scope boundary: do not edit other groups' tasks or checkboxes.
- Stop and report ambiguity, design issues, errors, or out-of-scope discoveries instead of guessing.
- Return exactly one JSON object in a fenced `json` block with this schema:

```json
{
  "group": "group name",
  "schema": "schema name",
  "completed": [
    { "task": "exact task text", "checkboxMarked": true }
  ],
  "incomplete": [
    { "task": "exact task text", "reason": "why incomplete" }
  ],
  "filesChanged": [
    { "path": "absolute path", "summary": "change summary" }
  ],
  "issues": [
    {
      "kind": "ambiguous-requirement | design-issue | error | out-of-scope | blocker",
      "detail": "specific detail",
      "relatedTask": "exact task text or null"
    }
  ],
  "needsAttention": false
}
```

6. Review subagent output.

Parse each JSON response. If any group reports `needsAttention: true`, pause and present the issue to the user before declaring progress complete.

For completed groups, read the changed files yourself. Use `filesChanged` only as navigation. Verify implementation against:

- Exact task text.
- Context files and specs.
- Existing contracts and tests.
- Scope boundaries.

If review fails, delegate a focused fix to the appropriate subagent with exact file paths, failure details, expected behavior, and verification steps. Re-review after the fix.

7. Confirm progress:

```bash
openspec-cn instructions apply --change "<name>" --json
```

Report completed tasks, total progress, review conclusion, and whether archive is ready.

## Guardrails

- Main agent handles OpenSpec state, grouping, delegation prompts, review, progress, and archive suggestion.
- Main agent may make tiny checkbox/status corrections only after review.
- All substantial implementation goes through subagents.
- Do not assume platform-specific subagent APIs beyond the Platform Adapter.
- Do not mark tasks complete based only on subagent self-report; inspect files and task checkboxes.
- Pause on ambiguity, design conflict, or out-of-scope work.
