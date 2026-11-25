---
name: django-6-upgrade-guide
description: >-
  Plan, audit, or complete an upgrade from Django 5.x to Django 6. Verify runtime and dependency compatibility, deprecations, settings, databases, migrations, tests, and deployment. Do not use for general Django work, earlier upgrades, frontend styles, or unrelated maintenance.
---

# Django 6 Upgrade Guide

## Workflow

For a plan or audit, assess these steps without changing project files or deployed services. Identify checks that require implementation. For implementation, perform the applicable steps.

1. Inspect the Django and Python constraints. Inspect the dependency manager, settings modules, databases, and deployment images. Inspect the CI matrix, third-party packages, and release process.
2. Use primary sources to verify supported Python versions and current Django 5.2 and 6.0 patch releases. Verify relevant security notices and third-party compatibility. If a required source is not available, report the missing verification. Do not claim that an unverified version or dependency is current.
3. Establish a clean baseline on the latest compatible Django 5.2 patch. Run the full test suite, Django system checks, migrations check, and representative production commands.
4. Run tests with deprecation warnings visible. Remove deprecated use that the project owns before you change the major version. Separate dependency warnings from application warnings.
5. Update Python and dependencies in an order that keeps failures attributable. Follow the repository's package-management policy and inspect lockfile changes.
6. Upgrade Django. Run the migration check. Create a migration only for an intentional model-state change. Review each new migration. Then review settings, middleware, templates, URLs, forms, authentication, storage, database behavior, and deployment startup.
7. Validate the upgrade locally and in CI. Define staging checks, monitoring, deployment order, and rollback limits. Adopt new Django 6 features only after you confirm compatibility.

## Evidence and decisions

- Record the discovered baseline and verified target patch. Record the documentation date, incompatible dependencies, warning list, migration effects, and unresolved risks.
- Prefer official Django release notes, topic guides, deployment checklists, and package maintainers' compatibility declarations.
- Never infer production safety from import success or a passing unit subset. Exercise migrations, static assets, background work, management commands, and database-specific paths used by the service.
- Evaluate schema reversal and application rollback separately. A deployment can require a forward fix even when you can roll back the code.

## Verify Current Information

Do not store current patch versions, Python support, security status, or third-party compatibility in this skill. Verify this information during each upgrade. Include the checked versions, sources, and date in the output. If verification is not possible, identify the missing evidence.

## Resource

Read [references/django-6-upgrade.md](references/django-6-upgrade.md) when building the compatibility inventory, warning pass, migration review, or rollout checklist. Load it only for an actual upgrade or audit.

## Output

Return the requested patch, upgrade plan, or audit. Separate confirmed blockers from risks that require validation. List optional Django 6 features separately. Ask only about choices that the repository or current primary documentation cannot resolve.
