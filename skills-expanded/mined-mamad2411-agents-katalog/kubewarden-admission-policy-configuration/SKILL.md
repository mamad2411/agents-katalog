---
name: kubewarden-admission-policy-configuration
description: >
  Guides configuring Kubewarden as a WASM-based Kubernetes admission
  policy engine — installing the policy-server and controller, writing
  or reusing WebAssembly policies from the Kubewarden Policy Hub,
  ClusterAdmissionPolicy/AdmissionPolicy resources, monitor-mode
  rollout before enforce, and multi-language policy authoring (Rego,
  Rust, Go via the SDKs) as an alternative to OPA/Gatekeeper or Kyverno.
  Use when the user asks to "set up Kubewarden," "write a WASM admission
  policy," "why use Kubewarden instead of OPA/Kyverno," "reuse a policy
  from the Kubewarden Policy Hub," "run an admission policy in
  monitor mode before enforcing it," or "author a Kubernetes admission
  policy without writing Rego."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Kubewarden Admission Policy Configuration

## Purpose

Kubewarden is a Kubernetes admission policy engine, like OPA/Gatekeeper
and Kyverno, but its policies are compiled **WebAssembly (WASM)
modules** rather than Rego or pattern-matching YAML — which means a
policy can be authored in whatever language has a Kubewarden SDK (Rust,
Go, Rego-via-a-WASM-compiled-OPA-policy, and others), compiled once, and
distributed as an OCI artifact pulled from a registry exactly like a
container image. This makes Kubewarden's core value proposition
*language flexibility plus a shared distribution mechanism*: a team
that already writes Go or Rust doesn't have to learn Rego to write a
custom admission policy, and policies can be versioned, signed, and
pulled from an OCI registry the same way container images already are.
This skill covers installing Kubewarden's `policy-server` and
controller, writing or reusing a WASM policy (including pulling
pre-built ones from the community Kubewarden Policy Hub instead of
writing one from scratch), the `ClusterAdmissionPolicy`/`AdmissionPolicy`
CRDs, monitor-mode rollout before enforcing, and — critically — where
Kubewarden fits relative to
[opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md)
and
[kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md),
which solve the same admission-control problem with different authoring
and distribution models.

## When to use

- Installing Kubewarden on a cluster that needs WASM-based admission
  control, typically because the team wants to author policies in a
  general-purpose language (Rust, Go) rather than Rego or Kyverno's
  pattern-matching YAML.
- Reusing an existing, community-vetted policy from the **Kubewarden
  Policy Hub** (e.g. a pod-security-standard policy, an image-registry
  allowlist policy) instead of writing one from scratch.
- Writing a custom WASM policy using a Kubewarden SDK when the logic is
  complex enough to benefit from real language constructs (loops,
  helper functions, external library reuse) beyond what Rego's pattern
  matching or Kyverno's YAML DSL comfortably express.
- Deciding between Kubewarden, OPA/Gatekeeper, and Kyverno for a new
  cluster's admission-control strategy, or explaining the tradeoffs to a
  team that's only used one of the three.
- Rolling out a new or changed `ClusterAdmissionPolicy` safely — starting
  in `monitor` mode and reviewing before switching to `protect`
  (Kubewarden's enforce mode).
- Debugging a Kubewarden policy that isn't rejecting resources it should
  (or is over-rejecting), including inspecting the actual
  `AdmissionRequest` payload a WASM policy receives.
- Setting up policy signing/verification (via `sigstore`/`cosign`
  integration) so only trusted, signed policy artifacts are pulled and
  run.

## Prerequisites & environment

- A Kubernetes cluster (1.23+ recommended) with cluster-admin access to
  install Kubewarden's CRDs, the `kubewarden-controller`, and one or
  more `policy-server` Deployments (the component that actually loads
  and executes WASM policies against admission requests).
- Kubewarden installed via its official Helm charts
  (`kubewarden-crds`, `kubewarden-controller`, `kubewarden-defaults`) —
  confirm the installed chart/CRD version's `ClusterAdmissionPolicy`
  API version (`policies.kubewarden.io/v1`) since field names have
  evolved across Kubewarden's early releases.
- For reusing Policy Hub policies: no authoring toolchain required —
  the policy is already a published OCI artifact
  (`registry://ghcr.io/kubewarden/policies/...`) that `policy-server`
  pulls directly.
- For authoring a custom policy: a Kubewarden SDK for the chosen
  language (`policy-sdk-rust`, `policy-sdk-go`, or writing Rego compiled
  via `opa build -t wasm`), plus that language's WASM build toolchain
  (`cargo` with the `wasm32-wasi` target for Rust, or the Go WASM/TinyGo
  toolchain for Go).
- `kwctl` (Kubewarden's CLI) for building, running, and testing a policy
  locally against sample `AdmissionRequest` JSON before ever deploying
  it to a cluster — this is Kubewarden's equivalent of `opa
  eval`/`gator test` for offline policy testing.
- A rollout plan: **every new or changed `ClusterAdmissionPolicy` should
  be applied with `mode: monitor` first**, not `protect` — identical
  discipline in spirit to Gatekeeper's `dryrun` and Kyverno's `Audit`,
  and for the same reason.
- If policy signing is required (recommended for any policy pulled from
  a public registry rather than authored/reviewed in-house): `cosign`
  and a configured `VerificationConfig` so `policy-server` refuses to
  load an unsigned or wrongly-signed policy artifact.

## Step-by-step guidance

1. **Install Kubewarden's controller and a policy-server** via Helm:
   ```bash
   helm repo add kubewarden https://charts.kubewarden.io
   helm repo update
   helm install kubewarden-crds kubewarden/kubewarden-crds -n kubewarden --create-namespace
   helm install kubewarden-controller kubewarden/kubewarden-controller -n kubewarden
   helm install kubewarden-defaults kubewarden/kubewarden-defaults -n kubewarden
   kubectl get pods -n kubewarden   # controller + policy-server Running
   ```

2. **Reuse a vetted policy from the Kubewarden Policy Hub** rather than
   authoring one from scratch, for common cases (pod security standard
   checks, registry allowlisting, resource-limit requirements):
   ```yaml
   apiVersion: policies.kubewarden.io/v1
   kind: ClusterAdmissionPolicy
   metadata:
     name: allowed-registries
   spec:
     module: registry://ghcr.io/kubewarden/policies/trusted-repos:v0.2.0
     mode: monitor   # start here — never `protect` on first rollout
     rules:
       - apiGroups: [""]
         apiVersions: ["v1"]
         resources: ["pods"]
         operations: ["CREATE", "UPDATE"]
     settings:
       reject_configmap_authorities: false
       constrained_labels: []
       registries:
         - "registry.example.internal/"
   ```
   The `module` field is an OCI reference exactly like a container
   image pull — Kubewarden's policy distribution model deliberately
   mirrors container image distribution, including support for
   registries with authentication and signature verification.

3. **Author a custom policy when Policy Hub doesn't cover the need**,
   using a language SDK rather than Rego, if the team prefers a
   general-purpose language. Rust example (`policy-sdk-rust`, validating
   a required label):
   ```rust
   use kubewarden_policy_sdk::{
       accept_request, reject_request, request::ValidationRequest,
       validate_settings,
   };

   fn validate(payload: &[u8]) -> CallResult {
     let validation_request: ValidationRequest<Settings> =
       ValidationRequest::new(payload)?;
     let pod = validation_request.request.object;
     if pod.metadata.labels.get("team").is_none() {
       return reject_request(
         Some("pods must have a 'team' label".to_string()),
         None, None, None,
       );
     }
     accept_request()
   }
   ```
   ```bash
   cargo build --target=wasm32-wasi --release
   kwctl run target/wasm32-wasi/release/policy.wasm \
     -r sample-admission-request.json
   ```
   `kwctl run` evaluates the compiled WASM module against a sample
   `AdmissionRequest` payload offline — always test this way before
   deploying, the same way `opa eval`/`gator test` are used for Rego
   policies.

4. **Inspect the actual `AdmissionRequest` payload** a policy receives
   before assuming a field path, exactly as with Rego/Kyverno policies —
   this is a general admission-controller pitfall, not
   Kubewarden-specific:
   ```bash
   kubectl create --dry-run=server -o json -f pod.yaml > sample-request.json
   kwctl run policy.wasm -r sample-request.json --execution-mode wasi
   ```

5. **Deploy in `monitor` mode and review before switching to
   `protect`**:
   ```bash
   kubectl apply -f allowed-registries-policy.yaml   # mode: monitor
   kubectl get clusteradmissionpolicy allowed-registries -o yaml \
     | grep -A5 "status:"
   ```
   Kubewarden's `monitor` mode logs what *would* have been rejected
   (visible in `policy-server`'s logs / an observability pipeline) but
   admits every request regardless, exactly like Gatekeeper's `dryrun`
   and Kyverno's `Audit` — review this output for at least one full
   deploy cycle before promoting.

6. **Switch to `protect` (Kubewarden's enforce mode) once monitor is
   clean**, with narrowly-scoped, documented exceptions:
   ```yaml
   spec:
     mode: protect
     rules:
       - apiGroups: [""]
         apiVersions: ["v1"]
         resources: ["pods"]
         operations: ["CREATE", "UPDATE"]
     namespaceSelector:
       matchExpressions:
         - key: kubernetes.io/metadata.name
           operator: NotIn
           values: ["kube-system", "legacy-migration"]  # owner: platform-team, review: 2026-10-15
   ```
   > **Warning — destructive action risk:** switching `mode` to
   > `protect` on a broadly-scoped `ClusterAdmissionPolicy` blocks every
   > matching admission cluster-wide the instant it's applied — identical
   > blast-radius risk to Gatekeeper's `deny` or Kyverno's `Enforce`.
   > Confirm the monitor-mode review period covered representative
   > traffic (including infrequent workflows) and that a fast rollback
   > (`kubectl patch clusteradmissionpolicy <name> --type merge -p
   > '{"spec":{"mode":"monitor"}}'`) is understood by on-call before
   > enforcing against production namespaces.

7. **Configure policy signature verification** so `policy-server` only
   loads artifacts signed by a trusted key, especially for anything
   pulled from a public registry rather than an internal one:
   ```yaml
   # policy-server VerificationConfig (illustrative)
   allOf:
     - kind: pubKey
       owner: kubewarden-policies@example.com
       key: |
         -----BEGIN PUBLIC KEY-----
         <BASE64_PUBLIC_KEY_MATERIAL>
         -----END PUBLIC KEY-----
   ```
   Reject any policy pull that fails verification rather than logging a
   warning and loading it anyway — an unsigned or wrongly-signed policy
   artifact silently running in the admission path is a supply-chain
   risk equivalent to running an unverified container image.

8. **Watch `policy-server` availability as an admission-path
   dependency**, the same operational concern as any admission
   webhook — Kubewarden's webhook `failurePolicy` (configured via the
   `ClusterAdmissionPolicy`'s underlying webhook object) determines
   whether a `policy-server` outage blocks or allows admission
   cluster-wide:
   ```yaml
   spec:
     failurePolicy: Fail   # or Ignore — choose deliberately per policy criticality
   ```
   As with Gatekeeper/Kyverno, `Fail` on a broadly-scoped policy plus a
   `policy-server` outage blocks all matching admission, including
   unrelated emergency deploys — monitor `policy-server` health and keep
   a fast rollback path ready.

## Best practices

- Reuse a vetted Kubewarden Policy Hub artifact for common, well-trodden
  policy needs (pod security baseline, registry allowlisting) before
  investing in authoring a custom WASM policy — the distribution model
  is specifically designed to make sharing and reusing policies as easy
  as pulling a container image.
- Choose Kubewarden over OPA/Gatekeeper or Kyverno when the team's
  authoring strength is a general-purpose language (Rust, Go) rather
  than Rego or YAML pattern-matching, or when a policy's logic
  genuinely benefits from real language constructs (external libraries,
  complex control flow) that are awkward in either alternative. Choose
  OPA/Gatekeeper
  ([opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md))
  when the org needs the same policy engine to also gate non-Kubernetes
  artifacts (Terraform plans via Conftest) or has already standardized
  on Rego. Choose Kyverno
  ([kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md))
  when the team wants zero new language to learn and needs first-class
  `mutate`/`generate` rules, not just `validate`.
- Always test a policy offline with `kwctl run` against sample
  `AdmissionRequest` JSON before deploying — this catches the same class
  of field-path/schema bugs that make a Rego or Kyverno policy silently
  never fire.
- Always roll out via `monitor` → review → `protect`, never straight to
  `protect`, mirroring the Gatekeeper/Kyverno audit-first discipline
  exactly.
- Verify policy artifact signatures (`cosign`/`sigstore`) for anything
  pulled from a registry outside direct organizational control — an
  admission policy is code that runs on every matching request, and an
  unverified WASM artifact is a supply-chain attack surface exactly like
  an unverified container image.
- Treat `policy-server` health as a monitored admission-path dependency,
  and choose `failurePolicy` per policy criticality with a documented,
  fast rollback path — not a default nobody has thought about.

## Common pitfalls

- **Symptom:** A new `ClusterAdmissionPolicy` is deployed directly with
  `mode: protect` and immediately rejects a legitimate deployment,
  paging on-call.
  **Fix:** Always deploy new/changed policies with `mode: monitor`
  first, review `policy-server` logs for what would have been rejected
  over a representative period, then switch to `protect` with
  documented namespace exceptions for anything legitimate monitor mode
  surfaced.

- **Symptom:** A custom WASM policy loads successfully and the
  `ClusterAdmissionPolicy` shows ready, but it never rejects a resource
  that obviously should violate it.
  **Fix:** Test with `kwctl run` against the actual `AdmissionRequest`
  JSON shape (step 4) rather than assuming the field path — this is the
  same "policy compiles but the field path assumption is wrong" bug
  common to Rego and Kyverno pattern-matching, just manifesting in
  whatever language the WASM policy was authored in.

- **Symptom:** A policy pulled from a public registry behaves
  unexpectedly after the maintainer pushes an update to the same tag,
  and nobody signed off on the change.
  **Fix:** Pin `module` references to an immutable digest
  (`registry://.../policy@sha256:...`) rather than a mutable tag, and
  configure signature verification (step 7) so only artifacts signed by
  a trusted key are loaded — treat an unpinned, unverified policy
  reference the same as an unpinned, unverified base image in a
  Dockerfile.

- **Symptom:** A `policy-server` outage combined with
  `failurePolicy: Fail` on a broadly-scoped policy blocks every deploy
  cluster-wide, including an unrelated emergency hotfix, during an
  incident.
  **Fix:** Treat `policy-server` health as a monitored, alertable
  dependency of cluster admission, and keep a documented, fast rollback
  path (patching the policy's `mode` back to `monitor`, or in a genuine
  emergency, patching the webhook's `failurePolicy` to `Ignore`
  temporarily) that on-call can execute without deep Kubewarden
  expertise under pressure.

- **Symptom:** A team picks Kubewarden specifically to avoid Rego, then
  ends up writing a WASM policy that's harder for the rest of the
  platform team to review and maintain than a Rego or Kyverno
  equivalent would have been.
  **Fix:** Kubewarden's language flexibility is a benefit only when the
  team authoring *and reviewing* the policy shares that language
  fluency — if the platform team standardizes on Rego for review
  purposes, writing custom Kubewarden policies in an unfamiliar
  language just shifts the maintenance burden rather than reducing it.
  Reserve custom WASM authoring for cases where the language fit is
  genuinely better across the whole reviewing team, not just the
  original author.

## Worked example

**Scenario:** A platform team wants to require all `Pod` images come
from an approved internal registry, reusing a Kubewarden Policy Hub
policy, rolled out safely via `monitor` mode.

```yaml
apiVersion: policies.kubewarden.io/v1
kind: ClusterAdmissionPolicy
metadata:
  name: require-approved-registry
spec:
  module: registry://ghcr.io/kubewarden/policies/trusted-repos@sha256:8f2a1c9b7e4d...  # pinned digest
  mode: monitor
  failurePolicy: Fail
  rules:
    - apiGroups: [""]
      apiVersions: ["v1"]
      resources: ["pods"]
      operations: ["CREATE"]
  namespaceSelector:
    matchExpressions:
      - key: kubernetes.io/metadata.name
        operator: NotIn
        values: ["kube-system"]
  settings:
    registries:
      - "registry.example.internal/"
```

Offline test before deploying, against a sample disallowed-image
request:
```bash
kubectl create --dry-run=server -o json -f pod-using-dockerhub.yaml > sample-request.json
kwctl run policy.wasm -r sample-request.json --settings-json \
  '{"registries": ["registry.example.internal/"]}'
```
```
{"allowed":false,"status":{"message":"image docker.io/library/nginx:latest is not from an approved registry"}}
```

Deploy in `monitor` mode, review for one week:
```bash
kubectl apply -f require-approved-registry.yaml
kubectl logs -n kubewarden -l app=kubewarden-policy-server --since=168h \
  | jq -c 'select(.policy_id == "require-approved-registry" and .response.allowed == false)'
```
After a clean week showing only expected/known non-compliant test
traffic (no legitimate workload flagged), the team promotes:
```bash
kubectl patch clusteradmissionpolicy require-approved-registry \
  --type merge -p '{"spec":{"mode":"protect"}}'
```
From then on, `kubectl apply -f pod-using-dockerhub.yaml` is rejected at
admission time, and the pinned digest reference means the policy's
behavior can't change underneath the team without a deliberate,
reviewed update to the `module` field.

## Cross-references

- [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) —
  the Rego-based alternative engine; read this to compare authoring
  model and rollout discipline (both share the audit-before-enforce
  pattern) when deciding between the two for a given team.
- [kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md) —
  the YAML-native alternative, notably stronger for `mutate`/`generate`
  use cases Kubewarden doesn't target as directly.
- [falco-runtime-threat-detection-configuration](../falco-runtime-threat-detection-configuration/SKILL.md) —
  runtime/eBPF detection that complements (not substitutes for)
  admission-time policy enforcement — a resource that passes a
  Kubewarden policy can still misbehave at runtime, which Falco is
  positioned to catch.
- [falco-configuration-validation](../falco-configuration-validation/SKILL.md) —
  the same audit-before-enforce validation philosophy applied to Falco
  rules instead of admission policy.
