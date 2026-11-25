---
name: pr
description: Commit scoped local changes, push a branch, and open a pull request following repository conventions for naming, commit format, templates, issue links, readiness, and reviewers. Use when the user asks to open a PR, commit and push, or as the publishing stage of $ship.
---

# PR

The request to run this skill authorizes the scoped branch, commit, push, and PR-creation workflow. It does not authorize staging unrelated changes, force-pushing, merging, or installing dependencies.

Read conventions in this order: applicable `AGENTS.md`, PR template, `CONTRIBUTING.md`, then bounded observed practice such as recent commits and PRs. Match the repository rather than inventing a scheme.

Use `$github:github` for repository and PR context. Follow `$github:yeet` for the transport split—local `git` for branch, stage, commit, and push; the GitHub app for PR creation; `gh` only where connector coverage is insufficient—but pass this skill's resolved scope, naming, template, base, and ready/draft choice as explicit constraints. Do not accept `$github:yeet` generic defaults when repository conventions differ.

1. **Pre-flight** — Inspect `git status`, the bounded diff, and the intended base. Separate unrelated user changes. Run the relevant test, lint, typecheck, and build gates required by the applicable instructions and risk. Review the diff for secrets, debug leftovers, stray files, and accidental lockfile or formatting noise. Report missing tools or dependencies; do not install them automatically.
2. **Branch** — Follow project naming. Never invent a branch scheme or commit directly to the default branch. If branch choice would materially change the workflow, ask before creating it.
3. **Commit** — Stage only files in the confirmed scope; never use blind `git add -A` in a mixed worktree. Follow the project's commit format. Keep an imperative subject at or below 72 characters unless local convention differs, and explain why in the body when useful. Ask before splitting unrelated changes into multiple commits.
4. **Push and open** — Push the resolved branch with tracking. Prefer the GitHub app for PR creation after push; use `gh pr create` only as a fallback. Fill the repository template completely and preserve its comments and checklists. Without a template, cover what changed, why, impact, verification from `$verify`, and reviewer focus areas. Include screenshots for UI changes and link the issue per convention. Default to a draft unless the user or repository convention explicitly calls for ready-for-review; `$babysit` can mark it ready after its gates pass.
5. **Reviewers** — Use CODEOWNERS and applicable `AGENTS.md`. If neither identifies reviewers, inspect bounded substantive history for modified files, excluding bots, the author, formatting-only commits, and departed contributors. Request reviewers only when repository convention or the user authorizes it; otherwise report the top suggestions.

Return the PR URL, branch, commit, base, validation evidence, readiness state, and any convention that required judgment.

- Never force-push a branch that may contain another person's commits. Inspect bounded local/remote divergence first.
- If authentication, push, or protection fails, report the exact error and stop. Do not work around repository protections.
- Write the description for reviewers: identify the old behavior, new behavior, reason, and evidence rather than listing touched files.
