---
name: Helm Chart Structure
description: Reference for Helm chart organization, metadata, templates, dependencies, and tests.
---

# Helm Chart Structure

Use this skill when creating, reviewing, or explaining Helm chart structure, metadata, templates, dependencies, CRDs, tests, and packaging conventions.

This skill is an operating contract for safe chart-structure work. Load the reference files only when deeper examples, templates, or troubleshooting details are needed.

## When To Use

- Designing a new Helm chart directory layout.
- Reviewing `Chart.yaml`, `values.yaml`, `values.schema.json`, `.helmignore`, `templates/`, `crds/`, or `charts/`.
- Deciding between an application chart and a library chart.
- Adding template helpers, dependency declarations, CRDs, hooks, tests, or repository packaging.
- Explaining why a chart fails linting, templating, dependency resolution, or installation checks.

## Required Inputs

Ask for or infer the smallest safe set of inputs:

- Chart name, application name, and intended namespace behavior.
- Whether the chart is an installable application chart or reusable library chart.
- Target Kubernetes and Helm versions when compatibility matters.
- Expected resources: deployments, services, ingress, config maps, secrets, autoscaling, monitoring, tests, CRDs, or hooks.
- Dependency requirements and whether subchart values must be conditionally enabled, tagged, aliased, or imported.
- Validation evidence available: `helm lint`, `helm template`, `helm dependency build`, schema checks, or `helm test` output.

Do not invent cluster state, credentials, repository URLs, maintainer identities, or validation results.

## Core Workflow

1. Identify chart intent: application chart for installable workloads, library chart for shared helpers.
2. Confirm required files: `Chart.yaml`, `values.yaml`, `templates/`, plus optional `values.schema.json`, `.helmignore`, `charts/`, `crds/`, `files/`, `README.md`, and `LICENSE`.
3. Check metadata: `apiVersion: v2`, chart `name`, SemVer chart `version`, optional `appVersion`, `type`, compatibility, dependencies, and annotations.
4. Organize values: defaults in `values.yaml`, validation in `values.schema.json`, and no plaintext secrets.
5. Organize templates: resource templates in `templates/`, helpers in `_helpers.tpl`, post-install notes in `NOTES.txt`, and tests under `templates/tests/`.
6. Handle special resources: CRDs live in `crds/` and are not templated; hooks require explicit lifecycle annotations and deletion policies.
7. Validate locally before claiming completion.
8. Report structure, decisions, files changed or proposed, validation evidence, and unresolved risks.

## Decision-Critical Rules

- Use `type: application` for installable Kubernetes applications.
- Use `type: library` only for shared helper templates that are consumed by other charts and not installed directly.
- Keep CRDs in `crds/`; do not template CRDs unless the user explicitly asks for a nonstandard pattern and accepts the tradeoff.
- Put chart dependencies in `Chart.yaml` and pin versions intentionally.
- Use `condition`, `tags`, `alias`, and `import-values` only when they are needed for dependency control or value mapping.
- Keep default configuration in `values.yaml`; keep environment-specific overrides outside the base chart unless the repo has an existing pattern.
- Use `values.schema.json` for user-facing value validation when inputs are configurable.
- Use `_helpers.tpl` for repeated names, labels, selectors, and image helpers.
- Keep chart names, labels, selectors, and generated resource names stable across upgrades unless a breaking change is intended.

## Safety And Security

- Never place secrets, tokens, credentials, private URLs, local paths, or session records in chart files or examples.
- Prefer secret references, external secret systems, or placeholder values over literal secrets.
- Do not run `helm install`, `helm upgrade`, `helm rollback`, `helm uninstall`, or cluster-mutating `kubectl` commands without explicit approval and target context.
- Do not claim a chart was installed, tested, or rendered unless the corresponding command output was inspected.
- Treat dependency updates and lockfile changes as intentional supply-chain changes; report them clearly.
- Preserve repository safety, public-safety, validation, and scanner requirements when editing tracked files.

## Validation Gates

Use the checks that fit the task:

```bash
helm lint <chart-dir>
helm template <release-name> <chart-dir>
helm dependency build <chart-dir>
helm dependency list <chart-dir>
helm test <release-name> --logs
```

For repository changes in this project, also run the repo-level validation requested by the user or canonical policy before completion.

## Output Expectations

Return a concise implementation or review packet:

- Chart type and directory structure decision.
- Required files created, changed, or recommended.
- Key metadata, values, templates, dependencies, CRDs, hooks, and tests.
- Safety decisions, especially secret handling and cluster-mutating actions not taken.
- Validation commands run and exact result summary, or clear reason they were not run.
- Follow-ups for environment-specific values, chart repository publishing, or cluster testing.

## Minimal Examples

Minimal application chart skeleton:

```text
my-app/
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── .helmignore
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   └── tests/
│       └── test-connection.yaml
└── crds/
```

Minimal `Chart.yaml`:

```yaml
apiVersion: v2
name: my-application
version: 1.2.3
appVersion: "2.5.0"
description: A Helm chart for my application
type: application
```

## Reference Map

- [Chart structure and metadata](references/chart-structure.md)
- [Values and schema examples](references/values-and-schema.md)
- [Templates, helpers, and notes](references/templates-and-notes.md)
- [Dependencies, CRDs, hooks, and tests](references/dependencies-crds-hooks-and-tests.md)
- [Packaging, validation, and troubleshooting](references/packaging-validation-and-troubleshooting.md)
