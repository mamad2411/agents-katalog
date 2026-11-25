---
name: pr-merge-review
description: Walk through a GitHub pull request as a pre-merge review — the same paginated, plain-English, one-page-at-a-time history walkthrough as walk-through-work-history, pinned to PRs and tilted toward the merge decision (how it works, the tradeoffs, and the risks to merging). Use when someone says "walk me through this PR", "review this pull request before I merge", "explain this PR like I'm 18", "what are the risks of merging this", or wants a paginated, ADHD-friendly merge-readiness walkthrough of a github.com/<owner>/<repo>/pull/<n> link.
---

# Walk a PR toward a merge decision

A thin GitHub-PR lens over `walk-through-work-history`. Operate exactly as if that skill had been invoked directly on the pull request — the same paginated, causal, one-page-per-turn history — with two adjustments for a reader who is about to merge. This adds a lens; it does not replace the method.

## Load and follow the base skill

The artifact is always a GitHub pull request. Read and follow both of these before page 1:

- Claude: `${CLAUDE_PLUGIN_ROOT}/skills/walk-through-work-history/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/skills/walk-through-work-history/references/github-pr.md`
- Codex: resolve `skills/walk-through-work-history/SKILL.md` and `skills/walk-through-work-history/references/github-pr.md` relative to the plugin directory two levels above this `SKILL.md`.

## The two adjustments

1. **GitHub PR only.** The user hands you a pull request and nothing else. Do not run the base skill's non-GitHub branches (Google Doc, ticket, incident). If the artifact is not a PR, say so and hand off to `walk-through-work-history` directly.

2. **Fold merge risk into the story, and end on next steps.** The reader is deciding whether to merge, so weave the risk thread through the causal chapters as it naturally arises — the concerns raised in review, in checks, or visible in the diff; how each one was addressed; and which remain open — as part of what happened, not bolted on as a separate risk section. Then make the final page a forward-looking summary: the open items that still stand between this PR and merge, the concrete next steps to close them, and — if nothing meaningful remains — a plain suggestion that it looks ready to merge. Do not invent new chapter types to carry this; it is the same walkthrough, told with the merge decision in view. If the evidence does not support a confident call, say so and name what you would need to see.
