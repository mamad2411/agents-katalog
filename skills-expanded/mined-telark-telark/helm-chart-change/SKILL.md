---
name: helm-chart-change
description: Use when changing anything under charts/ (values.yaml, templates, mode presets, Chart.yaml dependencies, the CRDs in telark-crds) or adding or changing a service env var or tunable. Covers the lint, render and kubeconform gate, the generated VALUES.md, and the docs that change in the same diff.
---

# Helm chart change

Goal: both charts lint and validate in every install mode, the rendered output contains exactly what you intended, and the docs describe the new behavior in the same change. The rules themselves (app.name identity, subchart wiring, shared sizing, lean values, CRD-first ordering, tunables) are in `AGENTS.md` under "Helm chart" and "Go services".

## While editing

- **Identity.** After a template edit, `grep -rn telark charts/*/templates` should turn up only helper identifier names (`telark.labels`, `telark.fullname`, …) and prose in comments or `NOTES.txt`, never the literal as rendered data.
- **New env var or tunable.** `Env*` and `Default*` constants plus the `config/` loader in the service, then the value under `services.<svc>.env` in `charts/telark/values.yaml`, and in `charts/telark/modes/*.yaml` when it varies by mode. Subcharts don't follow `app.mode`.
- **New value key.** Add it to `values.schema.json` when the surrounding block sets `additionalProperties: false`.
- **CRD field.** Change the schema in `charts/telark-crds/templates/crds/` before the Go type. The app chart renders a vendored copy of `telark-crds`, so run `helm dependency build charts/telark` before linting or rendering it again. Applying CRDs to a cluster belongs to a deploy the user asked for, not to the code change.
- **Versions.** Leave the `Chart.yaml` versions and `services.<svc>.version` alone; release workflows bump them.
- **Kubernetes range.** `K8S_VERSIONS` in the `Makefile`, `kubeVersion` in `charts/telark/Chart.yaml` and the kubeconform action stay in step; the action fails when the floor goes untested.

## Gate

From the repo root:

```sh
make deps            # once after a fresh clone, and after dependency or CRD changes
make helm-lint
make helm-validate   # renders every mode and validates it with kubeconform
make values-docs     # regenerates VALUES.md; CI fails when it drifts
```

If `make deps` reports a missing repository, add the repositories listed in `.github/actions/helm-add-dependency-repos/action.yaml` (the list CI uses).

Then read the rendered output you changed, in each mode it affects:

```sh
helm template t charts/telark --set app.auth.bootstrap.admin=test@example.com --set app.mode=<mode> --set app.persistence.storageClass=validate > rendered.yaml
grep -c '^# Source:' rendered.yaml
```

The placeholder class makes the render cover a named class; more than one exporter replica refuses to render without one (`templates/_storage_guard.tpl`). `helm template` cannot look up live objects, so the storage logic that reads the cluster (`templates/_storage.tpl`) needs a `helm upgrade --dry-run=server` against a release to check. Check the document count against what you expect before trusting a grep over the output, and delete `rendered.yaml` afterwards.

## Docs in the same change

1. `docs/INSTALL.md`: how to use the value (the `--set` example) and its non-obvious gotchas.
2. `charts/<chart>/README.md`: a value-reference row that links to that INSTALL section. Check that the anchor resolves (GitHub lowercases the heading, turns spaces into hyphens and drops punctuation).
3. `VALUES.md`: `make values-docs`, never by hand.
4. Sweep `README.md`, `docs/PUBLISHING.md`, `CONTRIBUTING.md` and the service READMEs for references the change makes stale.

User docs use the literal `telark` names, with no custom-app.name caveats, and procedures are inline command blocks rather than scripts.

## Report

List the modes you rendered, the lint and validate results, and the docs you updated.
