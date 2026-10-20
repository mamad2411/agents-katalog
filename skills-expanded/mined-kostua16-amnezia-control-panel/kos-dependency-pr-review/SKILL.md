---
name: kos-dependency-pr-review
description: Review a Dependabot PR using only local repository context and return the prompt's JSON verdict (passed|manual|blocked) + update_type + risk_notes; do not approve or edit labels.
user-invocable: true
when_to_use: "When the dependency-review workflow reviews a Dependabot PR, or when wiring/repairing its wake-orchestrator step."
category: utilities
argument-hint: "[pr-number]"
keywords: [dependabot, dependency, review, compatibility, breaking-change, passed, manual, blocked, json]
related: [kos-zai-agent-runtime-contract, kos-gh-automation-tooling, kos-zai-run-failure-prevention, kos-claude-turn-budget]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from dependency-review.yml prompt (local-context-only dep review + JSON verdict)
  license: repo
  version: "1.1"
---

# Idea

`dependency-review` runs an AI review of a Dependabot PR using **only local repository context** — no web. The value is a fast, grounded compatibility/breaking-change/security read that returns the prompt's exact JSON verdict. The workflow consumes the verdict; the agent does not approve or label.

## When to invoke this skill directly
- Reviewing a Dependabot/dependency-update PR.
- Deciding the verdict token for a version bump.

## References
- `dependency-review.yml` prompt (local-context-only; do NOT browse web or claim changelogs).
- Local signals: `package.json` / `package-lock.json` diff, `src/` usages, `npm audit`, `npm ls`, lockfile/manifest metadata.
- `evaluate-pr-policy.cjs` / `orchestrate-pr-flow.cjs` (wake-orchestrator path).
- [[kos-zai-agent-runtime-contract]] — return the prompt's JSON; no approve/label.

## Communication Style
One verdict token + 1–3 cited risks. Local evidence only.

## Core Principles
YAGNI / KISS / DRY. Local context only. Decide with the prompt's tokens. A patch/minor bump with no removed APIs and no usage of changed APIs → `passed`.

## Output contract (enforce)
Return **JSON only**:
- `verdict`: `passed` | `manual` | `blocked`
- `summary`: one short sentence
- `update_type`: `patch` | `minor` | `major` | `unknown`
- `risk_notes`: short justification

**Do NOT approve the PR or edit labels** — the workflow handles dependency-review signals and comments.

## Risk triage

| Delta | Default verdict | Flip away from `passed` if |
|---|---|---|
| patch | `passed` | advisory / regression noted locally |
| minor | `passed` | a used API is removed/deprecated |
| major | `manual` (until verified) | used API changed/removed; lockfile conflicts → `blocked` |

Also weigh: Node 24 / Next.js 16 / React 19 compatibility; auto-merge eligibility.

## Your Approach
1. Identify bumped package + semver class from manifest/lockfile diff.
2. Find usages in `src/` (grep import/require).
3. Map delta to used-API risk; check `npm audit`.
4. Verdict token + cited risks; return JSON.

## Failure modes to avoid
- **Wrong tokens** — must be `passed|manual|blocked` (not APPROVE/REQUEST_CHANGES).
- **Web claims** — local context only; never cite a changelog you didn't read locally.
- **Approving/labeling** — forbidden; the workflow does it.
- **wake-orchestrator misread** — tolerate its pre-auth non-zero exit.

## Process Flow (Authoritative)
1. Parse the bump (package, from→to, semver class).
2. grep usages; check `npm audit`/`npm ls`.
3. Map delta → used-API risk + compat + auto-merge.
4. Return the JSON verdict; do not approve/label.

## Output Format
```json
{"verdict":"passed|manual|blocked","summary":"…","update_type":"patch|minor|major|unknown","risk_notes":"…"}
```

## Critical Constraints
- Verdict tokens are `passed|manual|blocked` only.
- Local context only; never claim a risk you cannot cite to repo code or local lockfile/audit.
- Never approve the PR or edit labels.
