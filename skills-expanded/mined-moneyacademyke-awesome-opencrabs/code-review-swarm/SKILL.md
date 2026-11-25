---
name: code-review-swarm
description: Review repository changes from multiple perspectives — correctness, security, tests, maintainability, performance — using OpenCrabs-native tools and optional subagents.
output_contract: |
  - all 5 review lanes have findings or explicit "clean"
  - findings cite specific file:line
  - each finding rated critical/warning/nit
---

# Code Review Swarm Skill

Use this when the user asks for a serious review, PR audit, diff review, or "review like multiple experts".

Inspired by Ruflo's `agent-code-review-swarm`, but trimmed into useful work instead of ceremonial bee noises.

## Review lanes

Run these lanes, in this order:

1. **Diff scope**
   - `git status --short`
   - `git diff --stat`
   - `git diff` or targeted file reads

2. **Correctness**
   - Logic bugs, edge cases, state transitions, race conditions.

3. **Security/privacy**
   - Secret leakage, auth bypass, injection, unsafe network/file access, PII exposure.

4. **Tests**
   - Missing regression tests, brittle tests, untested branches.

5. **Maintainability**
   - Over-complexity, naming, data shape, coupling, docs drift.

6. **Performance**
   - Avoid speculative micro-optimization; flag obvious algorithmic or IO waste.

## Tool routing

- GitHub PRs/issues: use `gh` via `bash`, never browser.
- Local diffs: use `bash git ...`, `grep`, `read_file`.
- Large reviews: use `plan`; optionally `spawn_agent` for independent lanes if activated.
- Always cite file paths and line numbers when possible.

## Output format

Use severity buckets:

- **Blockers** — must fix before merge.
- **Warnings** — should fix or consciously accept.
- **Nits** — optional cleanup.
- **Good calls** — important strengths worth preserving.

End with a merge/readiness verdict.
