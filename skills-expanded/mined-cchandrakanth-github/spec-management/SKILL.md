---
name: spec-management
description: "Create, update, review, and manage feature specs. Use when creating new features, breaking down requirements, updating spec status, or resolving spec conflicts across the project."
argument-hint: "Describe the feature or requirement to spec out"
---

# Spec Management Skill

## When to Use

- Creating a new feature spec from a requirement or user story
- Updating an existing spec's status, acceptance criteria, or edge cases
- Resolving conflicts between specs
- Breaking down a large requirement into multiple specs
- Auditing all specs for completeness

## Procedure

### Bootstrapping `specs/`

If `specs/` does not exist yet at the project root, create it and write `specs/README.md` from [the specs README template](./assets/specs-readme.template.md). Do **not** copy the other templates into `specs/` — they stay here in `assets/` as the single source of truth.

### Creating a New Spec

1. Read the requirement from user input or GitHub issue
2. Search existing specs: `specs/*/spec.md` for overlap
3. Create feature folder: `specs/{feature-name}/`
4. Generate all 4 files from templates:
   - `spec.md` from [template](./assets/spec.template.md)
   - `styles.md` from [template](./assets/styles.template.md)
   - `test.yml` from [template](./assets/test.template.yml)
   - `schema.yml` from [template](./assets/schema.template.yml)
5. Cross-reference with existing specs and flag conflicts
6. Set `status: draft`

### Updating a Spec

1. Read the current spec
2. Validate the status transition is legal (see [lifecycle](./references/lifecycle.md))
3. Apply changes
4. If ACs changed, update `test.yml` to match
5. If schema changed, update `schema.yml`

### Spec Audit

1. List all specs in `specs/`
2. For each spec, verify:
   - All 4 files exist
   - Status is valid
   - ACs are testable
   - No orphaned specs (code deleted but spec remains)
3. Report findings

## References

- [Spec Lifecycle](./references/lifecycle.md)
- [Templates](./assets/) — the 4 spec-file templates plus `specs-readme.template.md`
