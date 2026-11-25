---
name: ns-best-practices
description: >-
  (NS) Security/compat/a11y hygiene + Vercel Web Interface Guidelines review
  (headers, CSP, deps, accessibility). Use when hardening security, fixing
  CSP/CORS/headers, reviewing UI / checking a11y / auditing UX, or applying
  Web Interface Guidelines — even without saying "best practices"; also at
  ns-proto-creator close-out. Do NOT use for MR/SOLID review
  (ns-reviewer), visual redesign (ns-frontend-design), or feature
  implementation (ns-coder / ns-spec-driven).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.1"
depends:
  - ns-harness
---

# Best Practices

Focused **quality + security hygiene** pass — not substitute for senior code review or visual design direction.

## Session boot

See `../ns-harness/references/session-boot.md`. Read `architecture-rules.md` + security-related harness rules.

## When to use

| Request | This skill | Use instead |
| ------- | ---------- | ----------- |
| Security headers / CSP / HSTS | Yes | — |
| Dependency audit / known CVE sweep | Yes | — |
| Browser compatibility baseline | Yes | — |
| Accessibility quick pass (landmarks, alt, labels) | Yes | — |
| "Review my UI" / Web Interface Guidelines / UX a11y audit | Yes (`references/ui-guidelines-review.md`) | — |
| Distinctive visual redesign / anti-slop aesthetics | No | `ns-frontend-design` |
| "Review this MR" / SOLID deep dive | No | `ns-reviewer` |
| New feature implementation | No | `ns-coder` / `ns-spec-driven` |

## Workflow

1. **Scope** — web app surface, API gateway, static assets, or `prototype/`.
2. **Baseline** — read `references/checklist.md`; tick only applicable sections (offline security/compat/a11y).
3. **Guidelines** — UI/a11y/UX audit **or** invoker is `ns-proto-creator` close-out: read `references/ui-guidelines-review.md` fully (bundled rules; no external fetch).
4. **Scan** — configs (nginx, Vite, Next, Laravel middleware, etc.); no stack assume.
5. **Report** — findings table: severity, location (`file:line` when possible), recommendation, effort.
6. **Fix** — minimal safe diffs when user asked implement; else report only.

## Overlap with other skills

- **This skill:** cross-cutting hygiene + Web Interface Guidelines compliance.
- **ns-frontend-design:** distinctive look, typography, motion, anti–generic AI UI.
- **ns-reviewer:** change-specific SOLID, tests, maintainability on diff.

Delivery may use sequentially — face skills route explicit.

## Forbidden

- Declare production secure without evidence
- Break existing integrations without calling out risk
- Replace threat modeling for high-risk domains (escalate to human)
- Skip `references/ui-guidelines-review.md` on UI audit / proto close-out and claim full UI pass
