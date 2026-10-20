---
name: end-of-turn-review
description: Run a GPT-5.5 critique of the work just produced in the current turn — applied diffs, proposed plans, or both. Triggers at end-of-turn (via Stop hook) or on explicit request ("review what you just did", "critique this plan", "second-opinion this before I commit"). Returns a verdict (LGTM / notes / block) plus specific issues with file:line citations. Do NOT trigger for trivial 1-3 line changes, doc-only edits, or read-only research turns.
---

# End-of-turn review

A second-opinion pass over work just produced. Designed to catch: bugs the implementer missed, edge cases the planner glossed over, regressions in unmodified behavior, and plans that look reasonable but have a load-bearing flaw.

The reviewer never edits. It produces a verdict and structured feedback. The primary decides what to do with it.

## When to use

- End of any non-trivial coding turn (multi-file edit, new feature, refactor, bugfix beyond a typo)
- After a planner subagent produces a plan, before the worker starts executing it
- On explicit "review", "critique", "second opinion", "is this safe", "what would break"
- Pre-commit, pre-push, pre-PR-create

## When NOT to use

- Trivial edits (1–3 lines, single-file typo fixes, comment-only changes)
- Read-only turns (research, log digests, no state change)
- Documentation-only edits (README, comments, doc strings)
- When the user explicitly says "skip review" / "just commit"

## Tools

### `scripts/review.sh`

Runs the review. Accepts the work-to-review on stdin (a diff, a plan, or freeform text) and prints a structured critique to stdout.

**Usage:**

```bash
# Review a code diff
git diff | scripts/review.sh --kind=diff

# Review a plan markdown
cat plan.md | scripts/review.sh --kind=plan

# Mixed: pass a turn transcript
scripts/review.sh --kind=turn < /tmp/turn-context.txt
```

**Env vars:**

- `REVIEW_MODEL` — model alias to call (default `gpt-5.5`). Must be configured in LiteLLM at `LITELLM_BASE_URL`.
- `LITELLM_BASE_URL` — defaults to `https://litellm.drkmttr.dev/v1`
- `LITELLM_API_KEY` — required; read from `~/.config/litellm/key` if unset
- `REVIEW_CONTEXT` — optional path to a file with extra context (the user prompt, prior plan, etc.) the reviewer should consider

**Output format** — first line is one of:

```
LGTM
LGTM with notes
BLOCK — <one-line reason>
```

followed by a numbered list of specific issues (each with `file:line` if applicable) and an optional "what I'd change" section.

### `scripts/diff-review-hook.sh`

Client-agnostic wrapper around `review.sh`. Designed to be called from any agent runtime's end-of-turn / session-stop event, or from a plain git pre-commit hook. It checks for a non-trivial uncommitted diff and pipes it through `review.sh`, printing the critique on stdout.

The hook makes no assumptions about the caller beyond *(a)* cwd is inside a git repo and *(b)* stdout is captured and surfaced somewhere — to the next agent turn, to the developer's terminal, or wherever the calling system routes it.

Not auto-installed. See `reference/hook-setup.md` for per-client wiring (Claude Code, opencode, Cursor, Aider, plain git).

## Reference

- `reference/system-prompt.md` — the reviewer's full system prompt (loaded by `review.sh`)
- `reference/hook-setup.md` — how to wire the skill into Claude Code Stop hooks and opencode session-end hooks
- `reference/output-schema.md` — exact format the reviewer is constrained to produce
