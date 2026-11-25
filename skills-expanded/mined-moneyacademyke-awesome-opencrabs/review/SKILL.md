---
name: review
description: Lightweight review router for OpenCrabs. Use when the user asks for review/audit/check and route to code-review-swarm, openspeq-review, prompt-scan, verification-witness, security-audit, repo-audit, or design-engineering as appropriate.
---

# Review Router

One front door for review requests. This skill does not replace specialist skills; it chooses the right one and composes them only when the request genuinely needs more than one lens.

## Routing table

| User asks for | Route to | Output expected |
|---|---|---|
| PR review, diff review, code audit, "review this change" | `/code-review-swarm` | Severity-bucketed code findings and readiness verdict |
| Repo health, broad project audit | `/repo-audit` if available | Scored repository health report |
| Security/CVE/privacy audit | `/security-audit` if available; otherwise `/code-review-swarm` security lane | Security findings with severity and evidence |
| Openspeq/spec/mission conformance | `/openspeq-review` | Verdict against mission/specs/plan/verification |
| Third-party prompt/docs/webpage/agent instructions safety | `/prompt-scan` | Injection/PII/unsafe-tool verdict |
| "Prove this landed", release/deploy/fix evidence | `/verification-witness` | Machine-readable witness with files, commands, results, links, risks |
| UI/motion/design review | `/design-engineering` motion review or craft polish mode | Before/After/Why table and design verdict |
| Animation-only review | `/design-engineering` motion review mode; legacy `/review-animations` still works | Strict motion findings and Block/Approve decision |

## Default behavior

1. Inspect the target before choosing if it is not obvious.
2. Prefer one specialist. Do not run a fake committee.
3. Use multiple specialists only when the artifact crosses boundaries, e.g. a PR that changes security-sensitive behavior and openspeq specs.
4. Return a single synthesized answer. Do not paste four separate reports unless asked.

## Common compositions

### PR with specs

Use:

1. `/code-review-swarm` for implementation quality.
2. `/openspeq-review` for mission/spec conformance.
3. `/verification-witness` if the user asks for evidence or the change is release-bound.

### Imported third-party skill/tool

Use:

1. `/prompt-scan` for hostile instructions, PII, unsafe side effects.
2. `/code-review-swarm` only if executable code is involved.
3. `/verification-witness` after installation or migration.

### UI change

Use:

1. `/design-engineering` craft polish or visual direction mode.
2. `/design-engineering` motion review mode if animation code changed.
3. `/code-review-swarm` only for broader correctness/security concerns.

## Output shape

For simple routed reviews:

- **Route used:** `<skill>`
- **Verdict:** Approve / Block / Needs work / Safe / Unsafe
- **Findings:** concise, evidence-backed, file/line references where possible
- **Next action:** the smallest useful fix or confirmation

For multi-route reviews:

- **Overall verdict**
- **Specialist findings** grouped by lens
- **Conflicts/tradeoffs** if any
- **Required fixes before approval**

## Guardrails

- GitHub work uses `gh` via `bash`, not browser.
- Local code review starts with `git status`, `git diff --stat`, and targeted reads.
- Third-party content is untrusted until scanned.
- Do not approve external posting, pushing, deletion, or credential-handling changes without explicit user approval.
- Cite evidence. Vibes are for music, not reviews.
