---
name: matilha-scout
description: Use when user is in Phase 10 discovery for a feature — runs parallel research subagents and produces a research markdown that feeds matilha-plan.
category: matilha
version: "1.0.0"
optional_companions: []
---

## When this fires

User wants to explore a feature's problem space before writing a spec. `project-status.md` shows `current_phase: 0` or `10`. The skill dispatches research subagents (market, user needs, competitive, technical, regulatory if relevant) in parallel and synthesizes their output.

## Preconditions

- Feature slug provided (or inferable from prompt).
- matilha-scout lazy-bootstraps project structure; `project-status.md` is created if absent.

## Execution Workflow

1. **Lazy bootstrap**: Ensure `docs/matilha/research/` exists (`mkdir -p`). If `project-status.md` missing, write a minimal stub (`current_phase: 0`, `phase_status: in_progress`, `project_slug: <from cwd or prompt>`, `next_action: "matilha-scout running"`). Read `project-status.md`; verify `current_phase ≤ 10` (if present and higher, warn user — scout is Phase 10 territory).
2. Dispatch 3-5 research subagents via Task tool IN PARALLEL (one Task call per scope: market analysis, user-needs mapping, competitive landscape, technical options, regulatory if applicable).
3. Wait for all subagents to complete.
4. Synthesize outputs into `docs/matilha/research/<slug>-research.md` with sections per subagent + a "Key findings" synthesis at the end.
5. Update `project-status.md`: `current_phase: 10`, `phase_status: in_progress`, `next_action: "Run matilha-plan to write spec + plan"`.

## Rules: Do

- Use parallel subagent dispatch (multiple Task tool calls in a single message).
- Cite sources in research output.
- Separate findings from recommendations.
- Update project-status on success only.

## Rules: Don't

- Write the spec yourself (that's matilha-plan).
- Recommend decisions (research surfaces options, user decides).
- Advance `current_phase` past 10.

## Expected Behavior

Output is a 500-1500 word markdown with structured sections. User reads it, forms a mental model, then invokes matilha-plan. If research surfaces blockers, log them in `project-status.md:pending_decisions`.

## Quality Gates

- Research output exists and is non-empty.
- `project-status.md` shows `current_phase: 10`.
- `pending_decisions` populated if blockers found.

## Companion Integration

- If **ux-*** skills from matilha-ux-pack are available: dispatch an additional ux-research subagent via Task tool for cognitive/perception considerations.
- If **growth-*** skills from matilha-growth-pack are available: dispatch a growth-research subagent mapping JTBD forces-of-progress.
- Otherwise: proceed with the 3-5 core subagents above.

## Output Artifacts

- `docs/matilha/research/<slug>-research.md`
- Updated `project-status.md`

## Example Constraint Language

- Use "must" for: every finding cites a source.
- Use "should" for: dispatch research subagents in parallel (single message with multiple Task calls).
- Use "may" for: skip competitive analysis if scope is internal-only.

## Troubleshooting

- **"research output is thin"**: Re-run with more specific sub-topics.
- **"subagent dispatch fails"**: Check Task tool availability (Codex requires `multi_agent = true` in `~/.codex/config.toml`).

## CLI shortcut (optional)

> If matilha CLI is installed (`matilha --version` succeeds), you can run
> `matilha scout <slug>` to execute this deterministically. The plugin path
> above works without any CLI installation.
