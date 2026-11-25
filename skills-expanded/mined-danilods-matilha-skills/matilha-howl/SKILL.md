---
name: matilha-howl
description: Use when user asks about project state, current phase, active waves, or next action — reads project-status.md and surfaces the status in a stream-friendly format.
category: matilha
version: "1.0.0"
optional_companions: []
---

## When this fires

User asks "where am I?", "what's next?", "what's the state?", or similar intent. Read-only; no mutations. Works at any phase.

## Preconditions

- None. matilha-howl lazy-bootstraps `project-status.md` stub when absent, then reports on the stub.

## Execution Workflow

1. Check `project-status.md`. If missing, write a minimal stub (`current_phase: 0`, `phase_status: not_started`, `project_slug: <cwd basename>`, `next_action: "Run matilha-scout to begin discovery, matilha-plan to plan a feature, or matilha-init for fuller bootstrap"`). Then read it via Read tool.
2. Parse frontmatter.
3. Read any `docs/matilha/waves/wave-*-status.md` files via Glob + Read; summarize (how many active, completed, failed).
4. Emit a streaming section listing: current_phase, phase_status, next_action, active_waves, recent_decisions (last 3), blockers.
5. If `current_phase === 40` and a wave is `in_progress`, surface per-SP status per wave.
6. End with the next_action prompt from project-status.md.

## Rules: Do

- Keep output concise (≤ 50 lines).
- Prioritize next_action.
- Surface blockers prominently.

## Rules: Don't

- Modify any file (read-only).
- Guess next_action (use the one in project-status.md).
- Over-summarize if there are many waves (show them all).

## Expected Behavior

User reads output and knows exactly what to do next without further questions.

## Quality Gates

- Output mentions current_phase, phase_status, next_action.
- Active and completed waves enumerated.

## Companion Integration

No companion integrations in Wave 4a.

## Output Artifacts

None (read-only).

## Example Constraint Language

- Use "must" for: read project-status.md.
- Use "must not" for: modify any file.
- Use "may" for: include relative-time labels like "3 days ago" for stale phases.

## Troubleshooting

- **"project-status.md missing"**: Instruct user to run `/matilha-init`.
- **"frontmatter invalid"**: Instruct user to restore via `matilha init --force` or manual fix.

## CLI shortcut (optional)

> If matilha CLI is installed (`matilha --version` succeeds), you can run
> `matilha howl` to execute this deterministically. The plugin path
> above works without any CLI installation.
