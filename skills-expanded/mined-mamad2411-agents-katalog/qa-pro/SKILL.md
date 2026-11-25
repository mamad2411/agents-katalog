---
name: qa-pro
description: Release-quality QA workflow for web and desktop software. Inspired by gstack QA workflows and adapted for Codex v4.3. Use before shipping, after feature completion, for regression sweeps, smoke testing, manual QA plans, automated QA, and acceptance validation.
---

# QA Pro

## Workflow

1. Identify release scope and critical user paths.
2. Map risks: auth, payments, data loss, API failures, desktop permissions, migration, browser/device differences.
3. Build a QA matrix: happy path, edge path, error path, regression path.
4. Run or propose the narrowest reliable verification commands.
5. Use `production-readiness-pro` for commercial release gates when real users, data, security, or desktop installers are involved.
6. Use `project-sync-audit` after meaningful work to ensure `.ai_project.md` and docs reflect the tested behavior.
7. Record blockers, non-blocking issues, and residual risk.

## QA Matrix

Include when relevant:
- Install/startup.
- Login/logout/session expiry.
- Primary workflow.
- Forms and validation.
- API offline/timeout/error states.
- Data persistence.
- Permissions and authorization.
- Desktop packaging/update behavior.
- Responsive layout.
- Accessibility smoke check.
- Docs/project-memory consistency.
- Production readiness P0/P1/P2 when relevant.

## Severity

- `Blocker`: cannot ship.
- `High`: likely user-visible failure or data/security risk.
- `Medium`: important edge case or workflow friction.
- `Low`: polish or minor inconsistency.

## Output

```markdown
QA 结果：
- Blocker: ...
- High: ...

验证：
- ...

残余风险：...
```

If QA cannot run locally, provide a concrete checklist and explain the missing dependency.

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
