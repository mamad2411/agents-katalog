---
description: Take the current build through the pre-ship gauntlet — code review, security audit, E2E verification, deploy.
argument-hint: [optional: target environment (staging|prod), default staging]
allowed-tools: Read, Write, Edit, Bash, Agent, TodoWrite
---

Run the pre-ship gauntlet.

Target: $ARGUMENTS (default: staging)

## Your plan

1. **progress-keeper** → load state; confirm which features are eligible (passing=true or ready-to-verify).
2. **In parallel**:
   - `code-reviewer` → full-repo review of unreviewed diffs
   - `security-auditor` → OWASP + secrets scan + dependency audit
   - `test-engineer` → run full test suite, report coverage
3. **Wait for all three.** Any blocker → route to the relevant build specialist, then re-run that gate. Don't proceed with known critical issues.
4. **qa-verifier** → full E2E against `features.json` acceptance criteria on the target environment.
5. **devops-engineer** → deploy to target, run smoke tests, verify observability is live.
6. **progress-keeper** → log the ship, update milestones, note any known issues.
7. Report release readiness summary: green / yellow / red, with specifics.

Refuse to ship if: any Critical security finding is open, any P0 feature is failing, or qa-verifier returns red.
