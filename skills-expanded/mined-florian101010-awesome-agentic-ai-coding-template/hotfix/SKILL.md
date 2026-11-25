---
name: hotfix
description: Fast but controlled hotfix workflow for urgent production incidents. Use when a critical bug needs an immediate targeted fix.
disable-model-invocation: true
---

# Hotfix

Follow `.agent/workflows/hotfix.md` strictly.

Execution requirements:

1. Document incident impact and minimal fix scope.
2. Apply smallest root-cause-oriented fix.
3. Run critical smoke tests for affected flows.
4. Update `CHANGELOG.md` and minimal impacted docs.
5. Run pre-commit checks before final handoff.
6. Record post-hotfix follow-up items.

Do not bundle unrelated improvements.
