---
name: deploy-hotfix
description: Prepare and promote an Infiquetra hotfix tag through the deployment workflow.
---

# Deploy Hotfix

Prepare an Infiquetra hotfix deployment.

## Procedure

1. Read `../deploy-state/SKILL.md`.
2. Verify the issue, regression scope, rollback path, and target environment.
3. Use `../../scripts/mint_tag.py`; hotfix versions normally use an extra patch
   segment such as `1.2.3.1`.
4. Require `--confirm-plan` matching the printed repo, tag, and ref before any tag push.
5. Update the related issue through mission-control with the tag, workflow URL,
   checks, and follow-up risks when an SDLC issue exists.

```bash
python3 plugins/deploy/scripts/mint_tag.py \
  --env production \
  --version 1.2.3.1 \
  --repo infiquetra/example \
  --ref hotfix/branch \
  --dry-run
```
