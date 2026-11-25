---
name: integrate-daisyui-into-django
description: >-
  Integrate or refactor Tailwind CSS and DaisyUI in a Django application. Define the asset pipeline, file ownership, theme tokens, migration process, and verification. Do not use for one template edit, non-Django work, visual design, or backend-only work.
---

# Integrate DaisyUI into Django

## Workflow

1. Inspect the Django version, package managers, template layout, and component conventions. Inspect the static-file pipeline and deployment build. Inspect the CSS and JavaScript entrypoints, Content Security Policy, and existing Tailwind or DaisyUI configuration.
2. Verify current installation and configuration guidance in the official Tailwind CSS and DaisyUI documentation.
3. Use the existing asset pipeline when it supports the required Tailwind CSS and DaisyUI configuration. If it does not support the configuration, identify the exact limitation before you replace the pipeline. Do not add a second asset pipeline.
4. Choose one CSS entrypoint and one deterministic build command. Include all template sources in content detection. Send generated assets through Django's established static-file handling.
5. Define file ownership. Django templates contain semantics and server data. The CSS entrypoint contains framework imports and intentional overrides. Reusable template components contain repeated markup. Scripts contain only behavior that native HTML cannot provide.
6. Define semantic theme tokens before component-specific styles. Add theme switching only when the user requests it. Define the default theme and persistence policy. Define the behavior when scripts are unavailable.
7. Migrate one representative page before you migrate all pages. Verify the new pipeline and component convention. Then migrate the remaining pages. Remove replaced assets and configuration only after the replacements pass the required checks.
8. Validate the development build, CI build, production build, and collected assets. Check accessibility and representative rendered pages.

## Decisions

- Preserve established repository conventions and supported versions unless the task includes a change to them.
- Prefer Django template inclusion or the project's existing component system. Do not add a component package solely to wrap every DaisyUI class combination.
- Keep business rules and authorization in Django, not in CSS classes or browser scripts.
- Use native HTML first. If the repository already uses HTMX or Hyperscript, follow its existing request and event conventions. Do not introduce Alpine or another enhancement library by default.
- Keep generated CSS out of hand-edited source. Avoid broad global overrides that conflict with DaisyUI component contracts.

## Verify Current Information

Tailwind CSS and DaisyUI installation details can change. Plugin syntax, content detection, theme configuration, and supported package versions can also change. Verify this information in current official documentation. Inspect the resolved packages before you edit the configuration. Record the sources, versions, and check date in the plan or audit report.

## Resource

Read [references/django-daisyui-patterns.md](references/django-daisyui-patterns.md) when you choose the build pipeline, component boundary, theme model, or migration sequence.
Also read it when you define the validation matrix.
Load it only when those details affect the task.

## Output

Return a repository-specific patch or plan. Identify the selected pipeline, source and generated file ownership, template component convention, theme behavior, and migration sequence. Identify completed or proposed checks. Ask only when you cannot determine an important product or deployment choice.
