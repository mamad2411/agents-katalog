---
name: open-source-maintenance
description: Use when preparing OpenArc or an OpenArc-governed repository for public open-source release, contribution readiness, license alignment, changelog hygiene, or public README cleanup.
---

# Open Source Maintenance

Use this skill when a repository needs public open-source readiness.

## Goal

Keep public project metadata consistent, useful, and low-maintenance.

## Checklist

1. Confirm the intended license and update `LICENSE` plus manifest/package metadata.
2. Make README useful to a first-time visitor:
   - what it is
   - what problem it solves
   - quick start
   - repository layout
   - usage examples
   - development and validation
   - contribution path
   - license
3. Add or update `CONTRIBUTING.md` when outside contributors are expected.
4. Add or update `CHANGELOG.md` for user-visible changes.
5. Check version impact with `version-governance`.
6. Run plugin or repository validation.
7. Use `release-workflow` before PR or GitHub release work.

For this plugin, prefer:

```bash
python3 plugins/openarc/scripts/openarc.py doctor plugins/openarc
```

## Rules

- Do not invent maintainer contact details, repository URLs, or governance promises.
- Prefer concise public docs over marketing copy.
- Keep README and manifest metadata aligned.
- Do not publish or tag a release without maintainer confirmation.
