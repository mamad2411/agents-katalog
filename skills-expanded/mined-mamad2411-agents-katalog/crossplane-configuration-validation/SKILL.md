---
name: crossplane-configuration-validation
description: >
  Validates Crossplane `Composition`s, `CompositeResourceDefinition`s
  (XRDs), and `Claim`s before applying them — schema validation with
  `crossplane beta validate`/`crossplane render`, catching field-path
  patch typos, and dry-running a Claim against an XRD's schema to catch
  mismatches before they reach a live cluster and provision (or fail to
  provision) real cloud infrastructure. Use when a user asks to
  "validate a Crossplane Composition before applying," "why did my
  Composition patch silently not apply," "check an XRD schema against a
  Claim," "dry-run Crossplane render output," or "add a CI check for
  Crossplane manifest changes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Crossplane Configuration Validation

## Purpose

A `Composition`'s field-path patches (`fromFieldPath`/`toFieldPath`) are
plain strings, not compiler-checked references — a typo in either path,
or a transform that doesn't match the target field's actual type, fails
silently in many Crossplane versions rather than producing an obvious
error: the target field just keeps its `base` manifest's default value,
and a Claim that requested `tier: large` can quietly provision a
`small`-tier resource with no error surfaced anywhere an operator would
naturally look. Because a `Composition` sits between a namespaced
`Claim` (what an application team wrote) and real cloud infrastructure
(what actually gets provisioned, and billed, and depended on), this gap
is higher-stakes than a typical Kubernetes manifest typo. This skill
covers the validation tooling — schema validation, render/dry-run, and
patch-path checking — that should run before a
[crossplane-kubernetes-native-provisioning](../crossplane-kubernetes-native-provisioning/SKILL.md)-built
Composition or XRD reaches a live cluster.

## When to use

- Adding a CI check that validates `Composition`/XRD changes in a
  platform repo before merge, so a broken patch or schema mismatch
  surfaces in a PR check rather than in a silently-wrong provisioned
  resource.
- Reviewing a PR that changes a `Composition`'s patches, transforms, or
  an XRD's schema, and wanting to see the actual resulting managed
  resource manifest before approving.
- A `Claim` reconciles without error, but the resulting cloud resource
  doesn't match what the Claim's parameters seem to request.
- Testing a new field added to an XRD's schema actually flows through
  to the underlying provider resource via the Composition's patches.
- Debugging why a `Claim` is rejected at admission (a schema validation
  failure) versus one that's accepted but produces a wrong resource
  (a Composition patch problem) — these require different
  investigation paths.

## Prerequisites & environment

- The Crossplane CLI (`crossplane` ≥ v1.16, via `up` or the standalone
  binary) with `crossplane beta validate` and `crossplane render`
  support — check the CLI's own version against the installed
  Crossplane version, since render/validate behavior has evolved across
  releases.
- The `Composition`/XRD/Claim already defined per
  [crossplane-kubernetes-native-provisioning](../crossplane-kubernetes-native-provisioning/SKILL.md)
  — this skill validates changes to those definitions, not how to
  author them from scratch.
- For live-cluster cross-checks: `kubectl` read access to inspect
  `Composite`/managed resources' actual reconciled state, to compare
  against what local rendering predicted.
- Local copies (or CI-checked-out copies) of the provider package's CRD
  schemas for accurate offline schema validation — `crossplane render`
  can validate against these without needing a live cluster connection
  for the structural check itself.

## Step-by-step guidance

1. **Validate an XRD's own schema is well-formed OpenAPI** before
   testing anything downstream — catches basic schema authoring errors
   (bad types, invalid enum values, missing `required` fields) cheaply:
   ```bash
   crossplane beta validate xrd.yaml --extra-resources composition.yaml
   ```
   This is a structural check independent of any live cluster or cloud
   credentials, and should be the fastest, first CI gate on any XRD
   change.

2. **Render a `Composition` against a representative `Claim`/composite
   input, offline, before applying anything** — this is the single
   most important validation step, since it reproduces exactly what
   Crossplane's controller would produce from the patches, without
   provisioning anything real:
   ```bash
   crossplane render xr.yaml composition.yaml functions.yaml
   ```
   (`xr.yaml` here is a representative `XDatabaseInstance`/Claim-shaped
   input, `functions.yaml` an empty/no-op function pipeline file if the
   Composition uses the classic patch-and-transform mode rather than
   composition functions.) Read the rendered output for the actual
   `spec.forProvider` values a real Claim with those parameters would
   produce — this is where a silent field-path typo becomes visible:
   the target field will show its `base` default instead of the
   expected patched value.

3. **Confirm every `fromFieldPath` actually exists in the XRD's
   schema**, and every `toFieldPath` actually exists on the target
   provider resource's CRD — a mismatch on either side is exactly the
   silent-failure case this skill exists to catch:
   ```bash
   kubectl explain xdatabaseinstance.spec.parameters --recursive
   kubectl explain instance.rds.aws.upbound.io.spec.forProvider --recursive
   ```
   Cross-check each patch's `fromFieldPath` string against the first
   command's output and each `toFieldPath` against the second — a path
   that doesn't appear in either `explain` output is a patch that will
   never actually apply, regardless of how correct the `Composition`
   YAML otherwise looks.

4. **Test a representative Claim against the XRD's schema via
   server-side dry run**, which catches schema validation failures
   (a Claim with an invalid enum value, a missing required parameter)
   without actually creating anything:
   ```bash
   kubectl apply --dry-run=server -f databaseclaim.yaml
   ```
   A rejection here is the "loud" failure mode (an admission-time
   schema violation) — genuinely easier to debug than the "quiet"
   failure mode of a patch that's individually valid YAML but doesn't
   map to any real field.

5. **Compare rendered output across a matrix of representative
   parameter values**, not just one happy-path input, especially for
   any transform (`map`, `match`, `string`) whose behavior depends on
   which branch a given input value hits:
   ```bash
   for tier in small medium large; do
     yq ".spec.parameters.tier = \"$tier\"" xr-template.yaml > /tmp/xr-$tier.yaml
     echo "=== $tier ==="
     crossplane render /tmp/xr-$tier.yaml composition.yaml functions.yaml | yq '.spec.forProvider.instanceClass'
   done
   ```
   Confirm every enumerated value in the XRD's schema actually maps to
   something sensible in the `Composition`'s transform — an enum value
   the schema allows but the transform's map doesn't cover falls through
   to an undefined/zero value silently in many Crossplane versions.

6. **Wire render + explain-path checks into CI as a required PR
   check** on any change touching a `Composition`, `CompositionRevision`,
   or XRD:
   ```yaml
   # CI step (tool-agnostic pseudocode)
   - crossplane beta validate xrd.yaml --extra-resources composition.yaml
   - crossplane render xr-representative.yaml composition.yaml functions.yaml > rendered.yaml
   - diff rendered.yaml rendered.expected.yaml   # golden-file comparison, if maintained
   ```
   A golden-file comparison (checking rendered output against a
   committed expected-output snapshot) catches unintended behavior
   changes in a `Composition` refactor even when no individual check
   above fails outright.

7. **After a Composition/XRD change ships, cross-check a live `Claim`'s
   actual reconciled state against what local rendering predicted** —
   confirming the offline validation and the real cluster agree, not
   just trusting the offline check in isolation:
   ```bash
   kubectl get instance.rds.aws.upbound.io -o jsonpath='{.items[0].spec.forProvider}'
   ```
   Compare directly against the equivalent `crossplane render` output
   for the same Claim's parameters — a mismatch here means either the
   render tooling and the live controller are using different
   Composition Function/patch logic versions, or a `CompositionRevision`
   pin is holding a live resource to an older Composition than the one
   just validated.

8. **Validate `CompositionRevision` pinning explicitly** when a
   Composition has been updated but existing Claims are pinned to a
   prior revision, so what's validated matches what's actually live:
   ```bash
   kubectl get compositions.apiextensions.crossplane.io xdatabaseinstances.aws -o jsonpath='{.status.currentRevision}'
   kubectl get databaseclaim payments-db -n payments -o jsonpath='{.spec.compositionRevisionRef.name}'
   ```
   If these differ, the live Claim is still running against an older
   revision — validate against *that* revision's manifest, not only
   the newest one, before assuming your validation covers what's
   actually deployed.

## Best practices

- Make `crossplane render` (not just schema validation) the primary CI
  gate for any Composition/patch change — schema validation alone
  cannot catch a field-path typo, since the typo produces a
  syntactically valid patch that simply never applies.
- Maintain a small set of representative Claim inputs covering every
  enum/branch value an XRD's schema allows, and render all of them in
  CI, not just one happy-path example — this is what actually catches
  an uncovered transform branch before a real Claim hits it.
- Keep golden-file (expected rendered output) comparisons for
  Compositions that back anything cost-sensitive or production-critical
  — a Composition refactor that changes rendered output unexpectedly
  is exactly the kind of regression a diff-based check catches cheaply
  and a human review easily misses.
- Cross-check `fromFieldPath`/`toFieldPath` against `kubectl explain`
  output for both the XRD and the target provider CRD as a standard
  part of Composition code review, not just as an incident-response
  step after something goes wrong.
- Track `CompositionRevision` pinning explicitly when validating —
  render against the revision a Claim is actually pinned to, not
  reflexively the newest Composition in the repo.
- Treat a Composition/XRD change with the same review rigor as a
  Terraform module change in
  [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)
  — both define the shape of real, billed cloud infrastructure other
  teams depend on without seeing the underlying implementation.

## Common pitfalls

- **Symptom:** A `Composition` patch is reviewed and looks correct, but
  a live Claim using the field it patches shows the `base` manifest's
  default value instead.
  **Fix:** This is the classic silent field-path-typo failure — run
  `crossplane render` locally with the Claim's actual parameters and
  inspect the rendered `spec.forProvider` output directly; a
  `fromFieldPath`/`toFieldPath` that doesn't exactly match the schema
  (a typo, wrong casing, or an outdated path after a schema refactor)
  produces no error, just a patch that never applies.

- **Symptom:** `crossplane beta validate` passes cleanly on an XRD/
  Composition pair, but applying a real Claim against it in a live
  cluster is rejected at admission.
  **Fix:** Schema-level validation (`crossplane beta validate`) checks
  structural correctness of the XRD/Composition themselves, not
  necessarily every admission-time constraint the live API server
  enforces (webhooks, additional CRD-level validation from the
  provider). Add a server-side dry run of the actual Claim
  (`kubectl apply --dry-run=server`) against a real cluster as a
  second, complementary check rather than trusting offline validation
  alone.

- **Symptom:** An XRD's schema enum includes a value (e.g. a new `tier:
  xlarge`) that was added without updating the Composition's
  corresponding transform map, and a Claim using it reconciles without
  error but provisions an unexpected/undersized resource.
  **Fix:** Render every enum value the schema allows (step 5), not just
  the ones already known to work — an enum value the schema accepts
  but the transform doesn't explicitly map typically falls through to
  a zero-value/undefined result silently rather than failing the
  Claim outright.

- **Symptom:** A validated, working Composition change doesn't seem to
  affect an existing production Claim at all after being merged and
  applied to the cluster.
  **Fix:** Check whether the Claim is pinned to an older
  `CompositionRevision` (step 8) — Crossplane's revision-pinning
  mechanism is designed to prevent exactly this kind of unexpected
  live change from an in-place Composition edit, but it also means
  "I validated and merged the new Composition" doesn't automatically
  mean "this Claim now uses it" until the pin is deliberately updated.

- **Symptom:** A CI validation pipeline is given write/apply credentials
  to a real cluster "to make the dry-run more thorough," and a bug in
  the CI script accidentally applies a test Claim against production,
  provisioning real (billed) cloud infrastructure from a validation run.
  **Fix:** Validation tooling (`crossplane render`, `crossplane beta
  validate`, `--dry-run=server`) needs, at most, read-only cluster
  access and no cloud-provisioning credentials at all for the render/
  validate steps specifically — never grant a CI validation job the
  same write-capable `ProviderConfig` credentials real reconciliation
  uses, and treat any pipeline that can apply real Claims as a
  deployment job, not a validation job, with the corresponding review
  gates.

## Worked example

**Scenario:** A platform team adds a new `xlarge` tier to the
`DatabaseClaim` XRD from
[crossplane-kubernetes-native-provisioning](../crossplane-kubernetes-native-provisioning/SKILL.md)'s
worked example, and wants to validate the change end-to-end before
merging.

1. Update the XRD schema (`tier` enum gains `xlarge`) and run
   structural validation:
   ```bash
   crossplane beta validate xrd.yaml --extra-resources composition.yaml
   ```
   Passes — the schema itself is well-formed.

2. Render every enum value, including the new one, against the
   *current* Composition (deliberately, before updating its transform
   map, to see what happens):
   ```bash
   for tier in small medium large xlarge; do
     yq ".spec.parameters.tier = \"$tier\"" xr-template.yaml > /tmp/xr-$tier.yaml
     echo "=== $tier ==="
     crossplane render /tmp/xr-$tier.yaml composition.yaml functions.yaml | yq '.spec.forProvider.instanceClass'
   done
   ```
   Output:
   ```
   === small ===
   db.t3.small
   === medium ===
   db.t3.medium
   === large ===
   db.r6g.xlarge
   === xlarge ===
   null
   ```
   `xlarge` renders `instanceClass: null` — exactly the silent
   fall-through failure mode this validation step exists to catch,
   caught before merge instead of after a real Claim requests it.

3. Fix the Composition's transform map to include the new tier:
   ```yaml
   transforms:
     - type: map
       map:
         small: db.t3.small
         medium: db.t3.medium
         large: db.r6g.xlarge
         xlarge: db.r6g.2xlarge
   ```
   Re-run the render loop — `xlarge` now correctly produces
   `db.r6g.2xlarge`.

4. Dry-run a representative Claim requesting the new tier against a
   real (non-prod) cluster before merging:
   ```bash
   kubectl apply --dry-run=server -f databaseclaim-xlarge-test.yaml
   ```
   Passes cleanly — the schema and admission chain both accept it, and
   the render output confirms it maps to the intended instance class.
   The PR merges with confidence that no Claim requesting `xlarge` will
   hit the silent-default failure the render step caught.

## Cross-references

- [crossplane-kubernetes-native-provisioning](../crossplane-kubernetes-native-provisioning/SKILL.md) — the Composition/XRD/Claim model and provisioning workflow this skill validates before it reaches a live cluster.
- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the `terraform plan`-review discipline this skill's render/dry-run workflow mirrors for a Kubernetes-native provisioning model.
- [flux-cd-configuration-validation](../flux-cd-configuration-validation/SKILL.md) — an analogous dry-run/diff validation workflow, applied to Flux Kustomizations/HelmReleases instead of Crossplane Compositions.
- [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) — enforcing organization-wide constraints (e.g. disallowed instance types) on Claims/Composites as an admission-time policy layer complementary to this skill's schema/render validation.
- [argocd-sync-failure-and-drift-investigation](../../../gitops-argo-ecosystem/skills/argocd-sync-failure-and-drift-investigation/SKILL.md) — the equivalent investigative discipline for distinguishing "applied without error" from "actually correct," applied there to Argo CD Applications.
