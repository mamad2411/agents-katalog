# Release Communication

## Purpose
Notifies internal and external stakeholders after a successful production deployment.

## Role
Release Manager

## Phase
Release (after successful production deployment)

## Triggered By
`post-release-monitoring` confirms all clear.

## Inputs
- Release notes, changelog, deployment details

## Process

### Internal Notification (PM + Tech Lead + all subagents)
What shipped, release tag, deployment time, known issues.

### External Notification (if applicable, clients/stakeholders)
Plain language summary linking to release notes, known limitations or follow-up items, contact for issues.

Format: structured message, not free-form.

## Outputs
Internal and (where applicable) external release communications sent.

## Quality Gates
- [ ] Internal notification sent to PM, Tech Lead, and all subagents
- [ ] External notification uses plain language, links release notes
- [ ] Structured message format used (not free-form)

## References
- `.claude/skills/release-manager/release-notes-writing/SKILL.md`
- `.claude/skills/release-manager/post-release-monitoring/SKILL.md`
