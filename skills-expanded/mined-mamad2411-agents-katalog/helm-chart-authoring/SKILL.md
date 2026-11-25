---
name: helm-chart-authoring
description: >
  Guides creating, templating, testing, versioning, and publishing Helm
  charts for Kubernetes applications — chart scaffolding, values schema
  design, template helpers, helm unittest/chart-testing (ct), semantic
  versioning of charts vs. app versions, and publishing to an OCI or
  classic chart repository. Use when a user asks to "write a Helm chart,"
  "template a Kubernetes deployment with Helm," "add helm unit tests,"
  "version and release a chart," "fix a failing helm lint/template," or
  "publish a chart to a registry."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Helm Chart Authoring

## Purpose

Helm is the de facto packaging format for distributing Kubernetes
applications: it turns a directory of YAML into a versioned, parameterized,
installable/upgradeable unit. A poorly authored chart — untyped values,
no schema validation, string-templated YAML that breaks on edge-case
input, no tests — produces silent misconfiguration in production that
`helm install` will happily apply without complaint. This skill covers
authoring charts that are safe to parameterize, safe to upgrade, and safe
to hand to another team or publish publicly.

## When to use

- Scaffolding a new Helm chart for a service or a reusable library chart.
- Designing `values.yaml` and a `values.schema.json` so invalid input
  fails at `helm lint`/`helm install --dry-run` instead of at runtime.
- Writing template helpers (`_helpers.tpl`) to avoid copy-pasted
  label/name logic across templates.
- Adding automated tests (`helm unittest`, `helm test`, `chart-testing`)
  to a chart's CI pipeline.
- Deciding how to bump `version` vs. `appVersion` in `Chart.yaml` for a
  release.
- Publishing a chart to an OCI registry or a classic `index.yaml`-based
  chart repository.
- Debugging a chart that renders valid YAML per template but fails on
  `helm upgrade` (immutable field changes, missing `--install` flag,
  hook ordering).

## Prerequisites & environment

- Helm ≥ 3.14 (OCI registry support has been stable since 3.8; `helm
  dependency update` for OCI-based subchart deps needs ≥ 3.7). Helm 3 has
  no Tiller — all rendering happens client-side against the cluster's
  Kubernetes API for capability lookups (`Capabilities.APIVersions`).
- `kubectl` context pointed at a real or kind/minikube cluster for
  `--dry-run=server` validation (server-side validation catches CRD
  schema mismatches that client-side `helm template` cannot).
- `helm plugin install https://github.com/helm-unittest/helm-unittest`
  for unit-testing templates without a live cluster.
- `chart-testing` (`ct`) ≥ 3.10 if the chart lives in a monorepo of
  charts and needs lint/install testing across a version bump.
- Access to a target registry: OCI-compliant (GHCR, ECR, ACR, Artifact
  Registry, Harbor ≥ 2.0) or a classic HTTP chart repo (GitHub Pages +
  `index.yaml`, ChartMuseum).

## Step-by-step guidance

1. **Scaffold the chart** and remove the boilerplate you won't use:
   ```bash
   helm create payments-api
   rm -rf payments-api/templates/tests payments-api/templates/hpa.yaml
   ```

2. **Design `values.yaml` as a stable contract**, not a dumping ground for
   every template's internals. Group by concern and give every value a
   sane, safe default:
   ```yaml
   # values.yaml
   image:
     repository: ghcr.io/example/payments-api
     tag: ""            # defaults to .Chart.AppVersion when empty
     pullPolicy: IfNotPresent

   replicaCount: 2

   resources:
     requests: { cpu: 100m, memory: 128Mi }
     limits:   { cpu: 500m, memory: 256Mi }

   serviceAccount:
     create: true
     annotations: {}

   ingress:
     enabled: false
     className: nginx
     hosts: []
   ```

3. **Add a JSON Schema** so bad input is rejected at `lint`/`install` time
   instead of producing broken manifests:
   ```json
   // values.schema.json
   {
     "$schema": "https://json-schema.org/draft-07/schema#",
     "type": "object",
     "required": ["image", "replicaCount"],
     "properties": {
       "replicaCount": { "type": "integer", "minimum": 1 },
       "image": {
         "type": "object",
         "required": ["repository"],
         "properties": {
           "repository": { "type": "string", "minLength": 1 },
           "pullPolicy": { "enum": ["Always", "IfNotPresent", "Never"] }
         }
       }
     }
   }
   ```

4. **Centralize name/label logic in `_helpers.tpl`** so every template
   produces consistent, colliding-free names and the standard Helm/K8s
   recommended labels:
   ```yaml
   {{- define "payments-api.labels" -}}
   app.kubernetes.io/name: {{ include "payments-api.name" . }}
   app.kubernetes.io/instance: {{ .Release.Name }}
   app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
   app.kubernetes.io/managed-by: {{ .Release.Service }}
   helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
   {{- end -}}
   ```
   Reference it everywhere with `{{ include "payments-api.labels" . | nindent 4 }}`
   rather than repeating label blocks per template.

5. **Guard optional blocks explicitly** — never assume a nested value
   exists:
   ```yaml
   {{- if .Values.ingress.enabled }}
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   ...
   {{- end }}
   ```

6. **Validate before every commit**:
   ```bash
   helm lint ./payments-api
   helm template payments-api ./payments-api -f values-prod.yaml | kubectl apply --dry-run=server -f -
   ```
   Server-side dry-run catches things client-side `helm template` cannot
   — invalid CRD fields, admission webhook rejections, immutable field
   violations on upgrade.

7. **Write unit tests with `helm unittest`** to lock in template
   behavior independent of a live cluster:
   ```yaml
   # tests/deployment_test.yaml
   suite: deployment
   templates:
     - deployment.yaml
   tests:
     - it: sets replica count from values
       set:
         replicaCount: 3
       asserts:
         - equal:
             path: spec.replicas
             value: 3
     - it: fails closed when image.repository is missing
       set:
         image.repository: ""
       asserts:
         - failedTemplate:
             errorMessage: "image.repository is required"
   ```
   ```bash
   helm unittest ./payments-api
   ```

8. **Add `chart-testing` for install-level validation** in CI, especially
   for chart repos with multiple charts:
   ```bash
   ct lint --config ct.yaml
   ct install --config ct.yaml   # spins up a kind cluster and installs the chart
   ```

9. **Version deliberately**: `Chart.yaml`'s `version` is the *chart's*
   SemVer (bump on any template/values-contract change); `appVersion` is
   the version of the *application* the chart deploys and does not need
   to move in lockstep:
   ```yaml
   # Chart.yaml
   apiVersion: v2
   name: payments-api
   version: 2.3.0        # chart version — bump for template changes
   appVersion: "1.4.2"   # app version — tracks the container image tag
   ```
   Treat a breaking values-schema change (renaming/removing a key,
   changing a default that changes behavior) as a chart major bump, and
   document it in the chart's `README.md`/`CHANGELOG.md`.

10. **Publish to an OCI registry** (preferred over classic `index.yaml`
    repos for new charts — no separate index-hosting infrastructure
    needed):
    ```bash
    helm package ./payments-api
    helm push payments-api-2.3.0.tgz oci://ghcr.io/example/charts
    # consumers then run:
    helm install payments-api oci://ghcr.io/example/charts/payments-api --version 2.3.0
    ```

## Best practices

- Keep templates free of business logic beyond conditionals on
  `.Values` — anything more complex belongs in a helper template or,
  better, upstream in the values contract.
- Never template a Secret's *value* directly from a plaintext value in
  `values.yaml` committed to git; reference an existing Secret name/key
  or integrate with [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md)
  / an external secrets operator instead, and document the expectation
  in the chart's README.
- Pin subchart dependency versions in `Chart.yaml` (`dependencies:` with
  an exact or range-constrained `version`) and commit `Chart.lock` — an
  unpinned dependency can silently pull a breaking subchart update.
- Use `--atomic` on `helm upgrade`/`install` in CI/CD so a failed release
  automatically rolls back instead of leaving the release half-applied:
  `helm upgrade --install payments-api ./payments-api --atomic --timeout 5m`.
- Prefer library charts (`type: library` in `Chart.yaml`) for
  organization-wide template snippets (standard labels, common probes)
  shared across many application charts, instead of copy-pasting
  `_helpers.tpl` per chart.
- Set explicit resource `requests`/`limits` defaults in the chart rather
  than leaving them empty — an empty default silently produces
  unbounded/unscheduled-friendly workloads that are easy to forget in
  every consuming environment.
- When the chart manages CRDs, put them under `crds/` (Helm-managed CRD
  install/no-uninstall semantics) rather than `templates/`, and read
  [kubernetes-operator-development](../kubernetes-operator-development/SKILL.md)
  for CRD versioning/compatibility implications before doing so.

## Common pitfalls

- **Symptom:** `helm upgrade` fails with an error about an immutable
  field (e.g. `spec.selector` on a Deployment, or a StatefulSet's
  `volumeClaimTemplates`).
  **Fix:** Some fields cannot be changed in place. Either avoid
  templating that field from a mutable value, or perform an explicit
  `helm uninstall`/recreate — but note this is destructive for stateful
  resources (PVCs may or may not be retained depending on the reclaim
  policy); confirm data is backed up first and prefer a blue/green
  release of a new resource name over an in-place delete when in doubt.

- **Symptom:** Chart renders fine with `helm template` but
  `helm install` fails against the real cluster with a validation error.
  **Fix:** `helm template` only renders client-side and does not know
  live CRD schemas, admission webhooks, or API server feature gates.
  Always validate with `helm template ... | kubectl apply --dry-run=server -f -`
  (or `helm install --dry-run=server`) before treating a chart as
  release-ready.

- **Symptom:** Two resources collide (`already exists`) when the same
  chart is installed twice into one namespace, or names change
  unexpectedly between installs.
  **Fix:** Template names must incorporate `.Release.Name` (via the
  standard `{{ include "chart.fullname" . }}` helper) rather than a
  fixed string, so multiple releases of the same chart don't collide.

- **Symptom:** A subchart's default values silently override the parent
  chart's intended configuration after a `helm dependency update`.
  **Fix:** Pin subchart versions exactly (or with a narrow range) in
  `Chart.yaml`, commit `Chart.lock`, and re-run `ct install`/unit tests
  on every dependency bump rather than treating `dependency update` as a
  no-op maintenance task.

- **Symptom:** `values.schema.json` passes locally but CI's `helm lint`
  doesn't catch an invalid values file that was later found in
  production.
  **Fix:** `helm lint` alone does not always enforce the schema against
  every values overlay; run `helm lint -f <each-values-overlay>.yaml`
  (or `ct lint`) explicitly against every environment's values file, not
  just the chart's own defaults.

## Worked example

**Scenario:** Package `payments-api` as a Helm chart with schema
validation, unit tests, and an OCI publish step wired into CI.

```
payments-api/
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── tests/
    └── deployment_test.yaml
```

`templates/deployment.yaml` (excerpt):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "payments-api.fullname" . }}
  labels:
    {{- include "payments-api.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "payments-api.name" . }}
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "payments-api.name" . }}
        app.kubernetes.io/instance: {{ .Release.Name }}
    spec:
      serviceAccountName: {{ include "payments-api.serviceAccountName" . }}
      containers:
        - name: payments-api
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

CI pipeline stage (GitHub Actions):

```yaml
jobs:
  chart:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-helm@v4
        with: { version: "3.15.3" }
      - run: helm plugin install https://github.com/helm-unittest/helm-unittest || true
      - run: helm lint ./payments-api
      - run: helm unittest ./payments-api
      - run: helm dependency update ./payments-api
      - run: |
          helm template payments-api ./payments-api -f payments-api/ci/values-test.yaml \
            | kubectl apply --dry-run=server -f -
      - name: Package and push (on tag)
        if: startsWith(github.ref, 'refs/tags/chart-')
        run: |
          helm package ./payments-api
          echo "${{ secrets.REGISTRY_PASSWORD }}" | helm registry login ghcr.io -u ${{ github.actor }} --password-stdin
          helm push payments-api-*.tgz oci://ghcr.io/example/charts
```

`helm unittest` output confirms the replica-count and label assertions
pass before the chart is ever packaged, and the server-side dry-run
catches any CRD/webhook incompatibility before a real `helm upgrade` is
attempted against a live namespace.

## Cross-references

- [kustomize-overlay-management](../kustomize-overlay-management/SKILL.md) — when to patch a chart's rendered output with Kustomize instead of adding more values, or combine both.
- [kubernetes-operator-development](../kubernetes-operator-development/SKILL.md) — packaging an Operator and its CRDs as a chart, and CRD lifecycle caveats.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — installing cert-manager itself via its official Helm chart and templating Certificate/Issuer resources from a values contract.
