---
name: generic-feedback-capture
description: Apply when the user issues a correction, preference, "remember X" / "don't do Y" / "next time", invokes /learn, or at Gate 7. Routes feedback to the correct skill / rule / glossary / memory / new-skill destination based on this project's structure.
metadata:
  stack: [generic]
  specificity: 95
---

# Feedback capture & routing

The `dev-team:feedback-learning` plugin skill owns the **mechanics** of capturing user corrections — keyword detection, audit-trail JSONL format, rollback machinery, and the "3+ corrections on same topic → propose update" heuristic. Read it for those concerns.

This skill owns the **destinations**. Where does each kind of feedback land in this project's toolbox? When this skill is loaded alongside `dev-team:feedback-learning`, **this skill's destination table takes precedence** for files under this project. The plugin's table (which defaults to `CLAUDE.md` and `REVIEW-CONTEXT.md`) is the wrong shape for our skill-based structure.

## When to apply

- **Explicit triggers** (the plugin's keywords): `amend`, `learn`, `remember`, `forget`.
- **Passive triggers** in chat: `don't do X`, `stop doing X`, `prefer Y`, `actually use Z`, `from now on`, `next time`, `yes exactly`, `perfect, keep doing that`.
- **`/learn` slash command** invocation.
- **Gate 7 of `generic-gate-pipeline`** — explicit invocation at the cleanup step.

## Destination table

The load-bearing artifact. Classify each feedback item against this table; pick exactly one destination.

| Feedback type | Destination | Notes |
|---|---|---|
| .NET coding pattern, API convention, EF/data rule, vendor-adapter rule | `dotnet-*` skill matching the topic | Append under an existing ANTI-PATTERNS or rule section |
| Frontend (Next.js / React / Tailwind) convention or anti-pattern | `nextjs-*` skill (or a local `vendor-*-bff` skill for auth specifics) | Same |
| Mobile / Expo / React Native pattern | `expo-*` skill | Same |
| Vendor integration quirk (third-party API, auth provider, IDV) | Project-local `vendor-*` skill (live in the consuming project, not the plugin) | Same |
| Cross-cutting process, gate behaviour, orchestrator threshold tweak | `generic-*` skill | Most common destination after dotnet/nextjs |
| User preference (commit/PR flow, terminology, tone, what to mention or skip) | User-level auto-memory at `~/.claude/projects/<slug>/memory/` (with `MEMORY.md` index) | Persists across sessions; harness owns the format |
| Project glossary term, terminology decision | Project-local `.claude/rules/project-glossary.md` | No load trigger needed |
| Stack manifest change (enabling/disabling a stack, adding a tag) | Consuming project's `CLAUDE.md` fenced YAML block | The only routine reason to touch CLAUDE.md; `guard-stack-manifest.sh` validates |
| Anti-pattern that could be enforced mechanically (a regex / file scope check) | New `hooks/guard-*.sh` PLUS entry in the owning skill's ANTI-PATTERNS section | Hook beats prose |
| Architecture or scope decision (non-obvious routing choice, scope cut, override) | `memory/decisions.md` as `DEC-YYYY-MM-DD-NNN` entry | Plugin's three-phase workflow already uses this |
| Doesn't fit any existing skill but is recurring | Propose a **new skill** (see "New skill proposal" below) | Gated behind explicit user approval |

When classifying, prefer the most-specific stack-tagged skill. If feedback could plausibly land in two skills (e.g. an auth cookie rule could go in a project-local `vendor-*-bff` skill or `nextjs-frontend-standards`), pick the one whose `metadata.stack` is the better narrow match.

## Processing flow

Mirror the plugin's flow with destination routing:

1. **Parse** — extract the change request from the user input (or `$ARGUMENTS` for `/learn`).
2. **Classify** — match against the destination table. If unambiguous, pick the destination. If two destinations are plausible, ask the user which.
3. **Preview** — show the proposed edit as a diff: which file, which section, before vs after. **No exceptions** — every edit under `.claude/`, `CLAUDE.md`, or `memory/decisions.md` shows a diff first.
4. **Apply** — write the edit.
5. **Log** — append a line to `metrics/config-changelog.jsonl` using the format below.
6. **Verify** — read back the modified section to confirm correctness.

Behavioural tweaks (a single bullet appended to an existing skill section) can apply after diff preview. Structural changes (new section, removed override, new skill file) require explicit user approval.

## Audit-trail format

Append to `metrics/config-changelog.jsonl` (one JSON object per line, append-only — same format the plugin uses, so its rollback works against our edits):

```json
{
  "timestamp": "2026-05-20T14:30:00Z",
  "type": "amend",
  "trigger": "user",
  "description": "Add IReadOnlyList<T> preference to dotnet-coding-patterns",
  "file_modified": ".claude/skills/dotnet-coding-patterns/SKILL.md",
  "section_modified": "Anti-patterns",
  "previous_value": "",
  "new_value": "- Repository methods that return `IEnumerable<T>` after materialising — return `IReadOnlyList<T>` to make intent explicit",
  "approved_by": "user"
}
```

| Field | Required | Description |
|---|---|---|
| `timestamp` | yes | ISO 8601 UTC |
| `type` | yes | `amend`, `learn`, `remember`, `forget`, `rollback` |
| `trigger` | yes | `user` (explicit) or `system` (recurring-correction detector) |
| `description` | yes | Human-readable one-liner |
| `file_modified` | yes | Repo-relative path |
| `section_modified` | yes | Heading or "Anti-patterns" or "<new-file>" |
| `previous_value` | yes | Content before (empty string if new section / new file) |
| `new_value` | yes | Content after (empty string if removal) |
| `approved_by` | yes | `user` or `auto` (auto reserved for behavioural tweaks below the structural-change bar) |

## New-skill proposal

When the destination table has no match (feedback doesn't fit any existing skill) and the feedback feels durable rather than one-off:

1. **Suggest a name** following the prefix convention — `<stack>-<topic>` (e.g. `vendor-card-state-machine`, `dotnet-event-sourcing`) or `generic-<topic>`.
2. **Draft the frontmatter** — `name`, `description` (one line, triggering language), `metadata.stack` (a list including the stack prefix).
3. **Write the first paragraph** capturing the feedback verbatim where possible.
4. **Present the proposal** as a file at the suggested path. Do NOT write the file yet.
5. **Wait for explicit user approval.** No auto-creation.
6. **On approval, write the file AND log** to `metrics/config-changelog.jsonl` with `type: "learn"`, `section_modified: "<new-skill-path>"`, `previous_value: ""`.

This is the only path that creates new skill files outside an explicit skill-authoring flow.

## Anti-patterns

- **Don't auto-append to CLAUDE.md.** The only routine change to CLAUDE.md is the stack-manifest YAML block.
- **Don't create a new skill for a one-off comment.** The bar for new-skill creation is "this will keep coming up." Comment-once, drop-once is fine.
- **Don't drop feedback into auto-memory just because routing is hard.** Make a routing choice from the table. Auto-memory is for *user preferences* and *project-level facts not in the repo*, not for "I couldn't decide."
- **Don't skip the diff-preview step** for any edit to a file under `.claude/`, `CLAUDE.md`, or `memory/decisions.md`. Even a one-bullet addition is shown first.
- **Don't lose the audit-trail entry.** `metrics/config-changelog.jsonl` is the only mechanism that makes rollback work. Skipping it means the change is invisible to the plugin's rollback flow.
- **Don't reorder or rename existing destination categories** in this table without coordinating with the README architecture guide — the README cross-references this table.

## Related

- `dev-team:feedback-learning` — the plugin skill that owns trigger detection, the JSONL format, rollback, and recurring-correction detection. This skill defers to it for those mechanics.
- `generic-gate-pipeline` — Gate 7 explicitly invokes this skill in the cleanup step.
- `generic-memory-policy` — defines what user-level auto-memory accepts vs project-local `memory/`.
- `generic-claudemd-authoring` — explains why CLAUDE.md should not grow.
- `/learn` slash command — explicit-invocation entry point for "capture this now" moments.

## Out of scope

- Detection of recurring corrections (the plugin's "3+ on same topic" heuristic). When the plugin proposes a recurring update, this skill provides the destination.
- Editing the plugin cache (`~/.claude/plugins/cache/...`). Plugin files are read-only — all edits go to project-local files.
- Rotating `metrics/config-changelog.jsonl`. Append-only by design; archive by year if it grows past usefulness.
