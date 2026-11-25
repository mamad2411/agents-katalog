---
name: handoff-patterns
description: "Pattern library and procedure for writing a HANDOFF.md at the end of a session: what belongs in it versus the git log, PR, or memory, how much detail each resume gap needs, the anti-patterns (status-report tone, diff restatement, vague next steps, missing verify commands), and ready templates. Use when ending a session with unfinished work, before a context clear or machine switch, when handing work to a teammate, or when reviewing a handoff."
user-invocable: false
---

# Handoff pattern library

## Writing one

To write a handoff, follow the procedure in `${CLAUDE_PLUGIN_ROOT}/commands/handoff.md` (the same steps `/handoff` runs): establish the resume gap, choose the location, draft from the template, show the draft, save it, index it for `/pickup`, and put the resume prompt on the clipboard. Use this library to decide what goes in and how much.

## What belongs in HANDOFF.md

| Content | Goes in |
|---|---|
| What changed file-by-file | git log (not HANDOFF) |
| Why a decision was made | HANDOFF + ADR if architectural |
| False leads explored | HANDOFF |
| Open questions | HANDOFF |
| Customer-facing summary | PR description |
| Lessons that survive this task | project memory (~/.claude/projects/) |
| Verify-still-done commands | HANDOFF |
| One specific next step | HANDOFF |

## Detail calibration table

| Gap | Lines | Detail focus |
|---|---|---|
| < 4 hours | 20-40 | Just the next step + open questions |
| Overnight | 40-80 | Plus what's NOT done + verify commands |
| Weekend | 80-150 | Plus decisions + false leads |
| Week+ | 150-300 | Plus references + project-level context |
| Month+ | 300+ | Plus role-of-this-task in the broader work |
| Team handoff | varies | Plus teammate context + "appreciate this first" |

## Anti-patterns

### Status-report tone

Bad:
> "Today was productive. We made significant progress on the auth refactor. Looking forward to continuing tomorrow."

Good:
> "Auth refactor: extracted token refresh into its own service. Next: wire the worker pool to use it."

### Diff-restatement

Bad:
> "Changed auth.ts to add null check. Modified types in auth.types.ts. Updated tests in auth.test.ts."

Good:
> "Added null check on `Session.refresh()` because the bug was triggered when the refresh token expired mid-flight. The fix preserves the existing retry logic; don't refactor it (we tried, broke worker pool integration)."

### Vague next step

Bad:
> "Next step: continue auth refactor"

Good:
> "Next step: edit `worker/pool.ts:89` to instantiate `TokenRefreshService` (the new class), remove the inline refresh logic at `pool.ts:91-145`."

### Skipped verify commands

Bad: (no verify section)

Good:
```bash
npm test auth                              # 47 tests, all should pass
gh pr view 412 --json state -q .state      # OPEN
curl -s https://api/health | jq .auth      # "ok"
```

## Pickup contract

HANDOFF writes; PICKUP reads. The contract:

- HANDOFF's "What's done" → PICKUP runs verify commands to confirm
- HANDOFF's "Next step" → PICKUP either confirms it's still the right step or revises
- HANDOFF's "Key context" → PICKUP reads twice before doing anything else
- HANDOFF's "Open questions" → PICKUP either resolves them (with the user) or carries them forward to the next handoff

## Templates

### Overnight handoff (40-80 lines)

```markdown
# HANDOFF — auth-refactor — 2026-05-23

## What I was doing
Extracting `Session.refresh` into its own service so the worker pool and CLI share the retry logic.

## Where I left off
worker/pool.ts:91, mid-refactor. Inline refresh logic still there; new service exists but isn't called yet.

## What's done
- TokenRefreshService at `auth/token-refresh.ts` with the extracted logic
- Unit tests at `auth/token-refresh.test.ts` (47 tests, passing)
- CLI updated to use TokenRefreshService

## What's NOT done
- Worker pool still has inline refresh at `pool.ts:91-145`. Replace with TokenRefreshService.

## Key context
- Tried passing TokenRefreshService via DI in pool.ts:78 — broke because pool.ts is instantiated before the DI container. Use direct import for now.
- The retry/backoff in TokenRefreshService matches the old worker pool's exactly. Verified by running both side-by-side.

## Open questions
None.

## Verify what's done is still done
- `npm test auth/token-refresh` — should be 47 passing
- `grep -c "refreshToken" worker/pool.ts` — should still be > 0 (we haven't removed it yet)

## Next step
Edit `worker/pool.ts:91-145`: replace inline refresh logic with `await new TokenRefreshService().refresh(token)`. Remove the imports for the inline helper. Run `npm test worker` to confirm.
```

### Weekend handoff (~120 lines)

Add: more context on the broader auth refactor goal, links to related ADRs, list of files touched.

### Month-long-vacation handoff (300+ lines)

Add: complete project context, who's working on what, what was tried previously, all related PRs.

### Team handoff

Add explicitly:

```markdown
## For Sam (resuming on 2026-05-26)

Why I'm handing off: I'm out Tuesday-Friday for the family thing.

What I'd appreciate you doing FIRST:
1. Read the "Next step" section
2. Skim the "Key context" section
3. Run the verify commands to make sure I didn't leave a half-broken state

Ping me on chat if anything is unclear. I'll have phone access Tuesday evening, my time zone.

Branch: feature/token-refresh-service (pushed)
PR: #412 (draft)
```

## Cross-references

- `pickup` plugin — the reader-half of the contract
- `absorb` plugin — distilling learnings INTO project memory (different from HANDOFF state)
- `close` plugin — the end-of-session ritual that wraps handoff + memory update + notification
