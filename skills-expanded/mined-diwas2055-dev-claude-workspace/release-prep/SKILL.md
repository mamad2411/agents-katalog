# Skill: release-prep

Prepares a production release from the current develop branch state.

## When to Use
When the team is cutting a release and needs a complete release package:
changelog, migration checklist, breaking change summary, and deployment steps.

## Steps

1. **Diff since last release**
   - `git log <last-tag>...HEAD --oneline`
   - Group commits by type: feat, fix, chore, refactor

2. **Check for migrations**
   - `ls alembic/versions/` — list new migration files since last release
   - Confirm each migration has a working `downgrade()`

3. **Check for breaking changes**
   - API schema changes that remove or rename fields
   - Endpoint removals or path changes
   - Auth behavior changes

4. **Generate release notes**
   - Use `release-template.md` as the output format
   - Fill in version, date, sections

5. **Deployment checklist**
   - [ ] All migrations reviewed
   - [ ] Environment variables added/changed documented
   - [ ] Feature flags toggled if applicable
   - [ ] Smoke tests defined

## Output
A filled-out `release-template.md` ready for the team to review.
