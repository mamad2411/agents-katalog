# backend/src/piActivity

Pi's graph activity reporter generates `<dir>/.pi/extensions/lattice-activity.ts`.
The extension posts Claude-shaped tool and lifecycle bodies to Lattice's
activity routes. `../piActivity.ts` is the stable public facade; keep its four
exports and caller import paths unchanged.

## Ownership

- `template.ts` owns `renderPiActivityExtension` and the extension source literal.
  Keep it as TypeScript string source, with no runtime asset reads or copying.
- `install.ts` owns installation, project-mode removal and the private path
  helper. It imports the renderer and filename directly from sibling modules.
- `constants.ts` owns `PI_ACTIVITY_EXTENSION_FILE` (`lattice-activity.ts`).

Internal modules must not import the facade, so the dependency graph stays
acyclic. Keep backend imports suffixed with `.js`.

## Byte-sensitive output and filesystem policy

Installation compares existing UTF-8 contents with the rendered string before
writing. Preserve the entire output, including whitespace, comments, escaping,
the trailing newline and interpolations: `JSON.stringify(activityUrl)` and
`opts.projectSession === true`. This applies to arbitrary URLs and both modes.

Keep the installer ordering: compute the path and source, read and skip an
identical file, create the directory, then call `atomicWriteFile` (temp + rename).
Any read error falls through to writing; installation failures log the existing
`[pi-activity]` warning and never fail the spawn. Removal only unlinks files whose
contents include `/api/project-activity/`; read/unlink errors are swallowed.

## Session modes and shared state

Default task/session mode omits `session_id` and top-level lifecycle/turn posts;
presence comes from the spawn registry. Project mode (`projectSession: true`)
posts top-level SessionStart/SessionEnd and UserPromptSubmit/Stop, with Stop on
`agent_settled`. A top-level shutdown with reason `reload` skips SessionEnd so
the same session can resume. Tool start arguments are remembered by call id for
tool end, then deleted; shutdown clears the map.

In-memory sessions identify subagents: they carry `agent_id: pi-<sessionId>` and
`agent_type: subagent`, post SubagentStart/SubagentStop, and in project mode use
the parent's session id from `globalThis.__latticePiProjectSessionId`.

Pi re-evaluates extensions for subagents. Every instance shares
`globalThis.__latticePiActivityPostQueue` (`tail` and `pending`); keep both global
keys stable and never replace this with module-local state. Handlers queue
fire-and-forget posts in event order, drop new posts at 64 pending, swallow
reporting failures, and use a 1500 ms timeout starting when each request is sent.
A late PostToolUse must finish before the turn's Stop is sent.

Existing coverage lives in `../__tests__/piActivity.test.ts`; preserve it.
