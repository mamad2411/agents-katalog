# Hotfix Release Management

## Purpose
Manages the hotfix release cycle for production emergencies, following the full release cycle rather than a shortcut.

## Role
Release Manager

## Phase
Release (production emergency)

## Triggered By
Critical production issue requiring an out-of-band fix.

## Inputs
- Root cause / issue requiring hotfix

## Rule
Hotfix follows FULL release cycle — NOT a shortcut.

## Process
1. Create `release/v{X}.{Y}.{Z+1}` from `main` (patch version bump).
2. Create `hotfix/{KAN-N}` from `release/v{X}.{Y}.{Z+1}`.
3. Kanban: `type: hotfix`, `priority: critical`.
4. Run abbreviated planning (no full 7-stage session).
5. Still requires: QA UAT, PO UAT, Security clearance.
6. Still requires: all 4 of Edward's approval commands.
7. Release branch: 30-day retention then delete (same as normal release).

## Outputs
Hotfix released through the full, abbreviated-planning release cycle.

## Quality Gates
- [ ] Correct branch hierarchy used (release/ → hotfix/)
- [ ] QA UAT, PO UAT, Security clearance all still obtained
- [ ] All 4 Edward approval commands still required
- [ ] Same 30-day retention policy applied

## References
- `.claude/skills/release-manager/release-branch-management/SKILL.md`
- `.claude/skills/release-manager/versioning/SKILL.md`
