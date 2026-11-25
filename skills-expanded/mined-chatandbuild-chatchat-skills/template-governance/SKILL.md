---
id: template-governance
name: Template Governance
description: Use this skill when creating or maintaining reusable infrastructure, CI/CD, service, or pipeline templates with governance, versioning, rollout consistency, and environment provisioning.
category: DevOps
---

# Template Governance

Define reusable DevOps templates with clear inputs, defaults, and validation.

## When to Use

- You need consistent scaffolding for CI/CD, infrastructure, or service setup.
- You want to reduce copy-paste drift across repositories or teams.
- You need a controlled approach to evolving shared template versions.

## Workflow

1. Identify repeated workflow or infrastructure patterns to templatize.
2. Define template parameters, defaults, and required validations.
3. Separate stable base logic from optional environment-specific extensions.
4. Add usage examples and migration notes for adopters.
5. Establish versioning and deprecation policy for safe updates.

## Template Patterns

**Cookiecutter/Yeoman for project scaffolding.** Use Cookiecutter (Python) or Yeoman (Node) to generate new projects from a template. Prompts collect parameters; template engine fills placeholders. Good for new repos, microservices, or app boilerplates. Version templates via git tags.

**GitHub template repositories.** Mark a repo as template; users click "Use this template" to create a copy. No runtime tooling required. Combine with `.github/template` or `cookiecutter.json` for parameterized generation. Document required manual steps (e.g. secrets, env setup).

**Reusable workflow templates.** GitHub Actions reusable workflows, GitLab CI includes, or similar. Define once, call from multiple repos with `inputs` and `secrets`. Version via branch or tag; consumers pin to a version. Reduces drift across team pipelines.

**Terraform modules as templates.** Package infrastructure as modules with variables and outputs. Use `source` with version constraint (`?ref=v1.2.0`). Publish to registry or private git. Document required variables and example `module` blocks.

## Template Governance

**Versioning strategy.** Use semver: major for breaking changes, minor for additive, patch for fixes. Tag releases. Consumers pin to major version; document upgrade path for major bumps.

**Deprecation announcements.** Announce deprecation at least one minor version ahead. Add deprecation notice in template output and docs. Provide migration guide and support window.

**Migration guides for breaking changes.** For each breaking change: what changed, why, step-by-step migration, rollback option. Include before/after examples. Test migration path before release.

## Common Pitfalls

- **Templates that drift from real usage.** Templates become outdated when real projects fork and evolve. Periodically sync template from a canonical consumer; or derive template from working project.
- **No validation of template parameters.** Invalid inputs cause cryptic failures. Validate at generation time: required params, format (URL, enum), ranges. Fail fast with clear errors.
- **Breaking consumers with silent updates.** Changing defaults or removing params breaks consumers. Treat template as API; use deprecation and versioning. Never change behavior in patch without explicit opt-in.
- **Over-parameterization.** Too many options make templates hard to use and maintain. Prefer convention over configuration; add parameters only when multiple consumers need different behavior.

## Output Format

```markdown
## Template Scope
- Target: <pipeline/infra/service>
- Consumers: <teams/repos>
- Pattern: <Cookiecutter/GitHub template/reusable workflow/Terraform module>

## Inputs
- Required: <param list with types and validation>
- Optional: <param list with defaults>
- Deprecated: <params with migration path>

## Validation Rules
- <rule 1>
- <rule 2>

## Versioning and Governance
- Current version: <semver>
- Deprecation policy: <notice period, support window>
- Breaking change process: <announcement, migration guide>

## Adoption Checklist
- [ ] Example usage works end-to-end
- [ ] Backward compatibility reviewed
- [ ] Versioning plan documented
- [ ] Migration guide for last breaking change
```

## Constraints

- Keep templates composable and avoid hidden side effects.
- Do not hardcode secrets, credentials, or account-specific identifiers.
- Prefer explicit parameter contracts over implicit conventions.
