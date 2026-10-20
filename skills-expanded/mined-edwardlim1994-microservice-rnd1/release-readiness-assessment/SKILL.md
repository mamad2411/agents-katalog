# Release Readiness Assessment

## Purpose
Formal checklist gate before Staging deployment.

## Role
Release Manager

## Phase
Release (shown as pre-check in `/release-staging`)

## Triggered By
`/release-staging` command invoked.

## Inputs
- Story approval labels (qa/po/security)
- Story changelogs
- Bug card state
- Image scan results

## Process
Verify the checklist below before allowing `/release-staging` to proceed.

### Checklist
- [ ] All stories `qa: uat-approved`
- [ ] All stories `po: uat-approved`
- [ ] All stories `security: cleared`
- [ ] Tech Lead `story-changelog-writing` complete for all stories
- [ ] Release notes drafted
- [ ] Rollback plan documented and tested
- [ ] No open critical/high bug cards in release
- [ ] Harbor Trivy scan clean on release images
- [ ] SonarQube quality gate green on release branch

## Outputs
Readiness confirmation or blocking gap list.

## Quality Gates
- [ ] Every checklist item explicitly verified (not assumed)
- [ ] Any failing item blocks `/release-staging`
- [ ] Gaps communicated to PM/Tech Lead for resolution

## References
- `.claude/skills/qa-engineer/uat-sign-off/SKILL.md`
- `.claude/skills/tech-lead/story-changelog-writing/SKILL.md`
- `.claude/skills/release-manager/staging-release-trigger/SKILL.md`
