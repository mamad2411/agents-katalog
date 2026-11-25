---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

**Dispatch contract.** Resolve every configured role through [`provider-dispatch.md`](../poteto-mode/references/provider-dispatch.md). Reviewers need the parent's live MCP surface, so the default and supported portable route is `inherit-parent` (or its `auto` alias). Pass the transcript or digest plus any required evidence paths. On Codex, resolve remaining Claude tool names via [`codex-tools.md`](../poteto-mode/references/codex-tools.md).

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, identify the active conversation through the current host's session metadata. Use Claude Code's per-project transcript directory only for this conversation; on Codex use the active thread reader or confirmed session path. Follow [`codex-tools.md`](../poteto-mode/references/codex-tools.md#active-conversation-and-evidence) for host paths and message schemas. Verify the conversation identity before reading. Do not search unrelated project transcripts or choose a file merely because it is newest. If the active transcript cannot be identified or read, pass a tight, explicitly labeled digest of confirmed current-session context instead.

## 2. Spawn three reviewers in parallel

Start all three lanes in one fan-out phase through provider dispatch. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, so keep them native to the parent; a mechanically read-only mode strips MCPs. The prompt forbids file writes; the parent applies edits.

Each lane names a role line in the current harness's pstack model sheet and a default descriptor: use the line's value, or the default when the sheet or the line is missing. `auto` and `inherit-parent` run on the parent model natively. A descriptor that fails its route is a dropout, not a substitution. Reviewers require the parent's live MCP surface, so supported routes stay on `inherit-parent` or `auto`; an external lane is not an equivalent fallback.

| Lens | Role line | Default descriptor | Prompt template |
|---|---|---|---|
| Judgment | `reflect tooling, judgment, divergent, synthesizer` | `inherit-parent` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling, judgment, divergent, synthesizer` | `inherit-parent` | `references/tooling-reviewer.md` |
| Divergent | `reflect tooling, judgment, divergent, synthesizer` | `inherit-parent` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Agent` response body.

## 3. Synthesize

Wait for all three reviewer lanes to reach verified native terminal results or recorded dropouts. Retain their handles and full outputs; progress and self-reported completion do not count. Then dispatch one lane using the `reflect tooling, judgment, divergent, synthesizer` line's descriptor (default `inherit-parent`). It spot-verifies citations through MCP, which a read-only mode would strip. Pass `references/synthesizer.md` verbatim, with each reviewer's full output and any named dropout inlined where marked. Verify its terminal result. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File Backlog items only when the task already authorizes that tracker write, using the repository's designated issue owner. Otherwise present them for approval. Reflect does not grant permission to message people, create an unrelated queue, or modify external state.

Never edit a skill inside a host's installed plugin cache or store. Before approval, show the destination: the project's `.claude/skills/<skill>/` or `.agents/skills/<skill>/`, or the matching user-level skill directory `~/.claude/skills/<skill>/` or `~/.agents/skills/<skill>/`. After approval, copy the skill folder there and edit the copy. Never open a PR or push from this skill.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the **plugin-dev:skill-development** skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `plugin-dev:skill-development` and run its description-optimization loop.
- `new skill via plugin-dev:skill-development: <kebab-name>`: hand creation to `plugin-dev:skill-development`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
