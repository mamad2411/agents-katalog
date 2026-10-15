---
name: skill-backup-flow
description: Backup local OpenClaw skills into a git repo with basic PII/secrets sanitization before commit and push. Use when you want to archive or version custom skills safely.
---

# Skill Backup Flow

Backup skills into a git repo with a repeatable and safer process.

## Quick use

Preferred (JSON config):

```bash
./scripts/backup_skill.sh \
  --source /home/harry/.openclaw/workspace/skills/remote-android-adb \
  --config ~/.openclaw/skill-backup-flow.json
```

Direct repo arg (optional):

```bash
./scripts/backup_skill.sh \
  --source /home/harry/.openclaw/workspace/skills/remote-android-adb \
  --repo /home/harry/.openclaw/workspace/src/openclaw-skills
```

## What it does

1. Copy source skill into `<repo>/skills/<skill-name>/`
2. Run a basic red-flag scan for likely secrets/PII patterns
3. Show findings (if any) for manual sanitization
4. If this is a newly added skill folder in the repo, update `<repo>/README.md` to include a one-line entry for the new skill.
5. Stage + commit + push when clean

## Notes

- Keep runtime/private configs out of backup repo.
- Prefer placeholders in examples (`REPLACE_WITH_*`).
- Review scan output manually before commit.

## References

- `references/config.example.json`
- `references/sanitize-checklist.md`
