---
name: ship-pro
description: Shipping and release readiness workflow for software changes. Inspired by gstack ship workflows and adapted for Codex v4.3. Use when preparing a feature, desktop app, web app, API change, or release for delivery, including final checks, docs, changelog, versioning, rollback, and deployment readiness.
---

# Ship Pro

## Workflow

1. Confirm scope: what is shipping and what is not.
2. Verify code quality: tests, lint, typecheck, build, and relevant manual checks.
3. Verify docs: `.ai_project.md`, feature docs, API docs, deployment notes, changelog.
4. Verify release safety: migrations, env vars, flags, rollback, monitoring, user impact.
5. Use `production-readiness-pro` for commercial go/no-go decisions.
6. Use `project-sync-audit` to catch stale project memory before handoff.
7. Summarize blockers, risks, and go/no-go decision.

## Release Checklist

- Tests or manual verification completed.
- Build/package succeeds.
- No secrets in code, bundles, logs, or artifacts.
- Migrations are reversible or risk-documented.
- Feature flags or rollout plan exist when risk is high.
- Release notes reflect actual changes.
- Rollback path is known.
- Monitoring/logging can identify failure.
- `.ai_project.md` Docs Index and relevant `docs/` files match the shipped behavior.

## Desktop App Checks

- Installer or bundle starts cleanly.
- Auto-update metadata is correct when used.
- Signing/notarization requirements are known.
- OS permissions and native capabilities are documented.

## Web/API Checks

- Env vars are documented.
- API compatibility and status codes are stable.
- Cache and CDN behavior are considered.
- Error monitoring is ready.

## Output

```markdown
发布判断：Go | No-Go | Conditional Go

已验证：
- ...

风险：
- ...

回滚：
- ...

项目记忆：
- ...
```

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
