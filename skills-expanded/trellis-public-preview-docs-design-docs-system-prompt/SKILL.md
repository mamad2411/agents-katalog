# Claude Code's base system prompt

Trellis is a layer on top of Claude Code. The harness injects its own base system prompt — tool-use discipline, safety rules, response style, and a git block — before any Trellis content is seen. One block of that prompt contradicts Trellis. This doc records what the contradiction is, whether the base prompt can be replaced, and the decision: don't replace it, disable the one conflicting block via `includeGitInstructions: false`.

## The contradiction

Claude Code's base prompt contains a `# Git` block whose operative line is:

> Commit or push only when the user asks. If on the default branch, branch first.

Trellis says the opposite about commit autonomy:

- `rules/verification.md`: "Verified work is committed work. When tests pass and the build is clean, commit before ending the turn — don't leave verified changes uncommitted for the user to deal with."
- `CLAUDE.md` Guidelines: "End Deliver turns at a terminal state: merged + closed, `blocked`, or `needs-human-review` — worktree clean."
- `git-workflow.md`: autonomy squash-merges to `main` auto-after-gates, with no per-commit human ask.

So the base prompt says *commit only when asked*; Trellis says *commit and merge autonomously once verified*. (The "branch first" half of the base line actually agrees with branch-per-issue — only the commit-gating half conflicts.)

This is not cosmetic. It is the bug a user notices as the agent hesitating to commit verified work, or asking for permission Trellis already granted.

## Why CLAUDE.md doesn't just win

Trellis ships as `CLAUDE.md` + `rules/` + skills, symlinked into `~/.claude/`. None of those is the system prompt. Per Anthropic's own guidance ([modifying-system-prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)), CLAUDE.md and append-mode content are **additions** to the preset; changing a *conflicting core behavior* requires replacing the prompt, not appending to it. CLAUDE.md arrives as project context, structurally weaker than the system message it contradicts. So the agent gets two instructions and the wrong one carries more weight. Stacking more emphatic prose in `rules/verification.md` does not fix a precedence problem — it just makes the conflict louder.

## Can the base prompt be replaced?

Yes. Four confirmed mechanisms (Claude Code 2026):

| Mechanism | Effect | Reachable from Trellis-as-distributed? |
| --- | --- | --- |
| `--system-prompt` / `--system-prompt-file` (CLI) | Full replace | No — Trellis doesn't control the launch command |
| `--append-system-prompt[-file]` (CLI) | Append to preset | No — same reason; and append still loses on hard conflicts |
| SDK `systemPrompt` option (`{type:'preset',preset:'claude_code',append}` or full string) | Replace or append | No — applies only to SDK-embedded callers, not the user's `claude` CLI |
| `settings.json` → `includeGitInstructions: false` | Removes the built-in git block + git-status snapshot from the prompt | **Yes** — `dist/settings.json` is symlinked to `~/.claude/settings.json` (the settings split was eliminated; see `settings-split.md`) |

The first three operate at launch/SDK time. Trellis is a set of symlinked files; it never owns the invocation of `claude`, so it cannot rely on CLI flags or SDK options. Only the settings file is part of the distribution and therefore actually reachable.

## Decision

**Do not replace the system prompt. Disable the conflicting block with `includeGitInstructions: false` in `dist/settings.json`, and let Trellis's git workflow be the sole git authority.**

The setting is purpose-built for this. Its documented description:

> **Default `true`.** Include built-in commit and PR workflow instructions and the git status snapshot in Claude's system prompt. Set to `false` to remove both, **for example when using your own git workflow skills.** (`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var takes precedence.)

Trellis *is* "your own git workflow skills" — branch-per-issue, `/git`, `/implement`, `/review`, the Two Routes. With the built-in block gone, there is no competing system-message instruction; Trellis's CLAUDE.md and rules become the only git policy in context, and the precedence problem disappears at the root rather than being shouted over.

### Why not full replacement

Replacing the whole prompt to override one paragraph is a shallow-module move: a huge, brittle interface (re-author and maintain tool-use discipline, safety rules, harness behavior, response style) to change a small piece of implementation. It throws away a large, well-tuned prompt that Anthropic updates frequently, and goes stale against every Claude Code release. It's also unreachable for the standard symlink distribution. Disabling one documented block is the small interface that does exactly the needed work.

### Side effect, and why it's fine

`includeGitInstructions: false` also drops the **git-status snapshot** from the prompt. Trellis doesn't depend on that snapshot: skills run `git status --short` explicitly when they need state ("Start clean before new work"), and the passive snapshot is stale by mid-session anyway. Losing it is neutral-to-positive.

## Considered alternatives

- **Do nothing; rely on CLAUDE.md precedence.** Rejected. This *is* the reported bug — contradictory signals with the wrong one weighted higher.
- **`--append-system-prompt` with a counter-instruction.** Rejected twice over: append still loses on hard conflicts per the docs, and it isn't reachable from a symlink distribution.
- **Full replacement via `--system-prompt-file` / SDK string.** Rejected as the default (see "Why not full replacement"). Remains a viable opt-in for someone who wraps `claude` themselves and wants total control — out of scope for the shipped layer.

## Consequences

- One-line addition to `dist/settings.json`: `"includeGitInstructions": false`. Applies at the user scope, so it covers every project using Trellis — correct, since Trellis is the global process layer.
- Worth a one-line note in `CLAUDE.md`'s Git Workflow section that the built-in git instructions are intentionally disabled so Trellis owns git policy — otherwise a future reader sees the setting and wonders why.
- `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` is the belt-and-suspenders equivalent if a context ever can't read settings.

## Open questions

- **Non-git contradictions.** There is no per-block toggle for other parts of the base prompt. If a future conflict lands in, say, the safety or commit-attribution wording, the only levers are append-softening (weak) or a full opt-in replacement wrapper. Defer until such a conflict actually appears — don't pre-build the wrapper.
- **Whether to ship an opt-in full-replacement launcher** for power users who want Trellis to own the entire prompt. Not justified by the current single-block conflict.
