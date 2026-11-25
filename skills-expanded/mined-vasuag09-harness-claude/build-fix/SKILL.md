---
name: build-fix
description: Resolve build failures and type/compile errors fast, with minimal diffs. Use when a build or typecheck fails during implementation. Delegates to the harness-claude:build-error-resolver agent.
---

# /build-fix — get the build green

Goal: smallest correct change that makes the build/types pass. No refactoring.

## Do this
1. **Delegate to `harness-claude:build-error-resolver`**, or inline:
2. Run the real build/typecheck to reproduce (`npm run build`, `npx tsc --noEmit`,
   `pytest`, ...). Read the **first** real error — the rest are often cascades.
3. Fix the root cause with a minimal diff. Re-run. Repeat on the next first-error.
4. Never silence with `any` / `@ts-ignore` / bare `except:` / disabled lints unless
   that is genuinely correct (and say why). Never use `--no-verify`.

## Escalate
If the only real fix is a design change, stop and return to `/harness-claude:architect` or `/harness-claude:plan`
rather than hacking around it.

## Exit criterion
Build, types, and lint are clean. Resume `/harness-claude:implement` or proceed to `/harness-claude:review`.
