---
name: complete-devsecops-pipeline-for-serverless-from-scratch
description: >
  Builds the complete security-gate sequence for a serverless (Lambda-
  style) DevSecOps pipeline from scratch — SAST, SCA against a much larger
  bundled transitive-dependency surface, package/artifact signing, and
  least-privilege execution-role scoping as the primary release gate
  (rather than a Kubernetes-style admission policy), with runtime secrets
  fetched from a managed secrets service instead of baked into the
  deployment package. Use when the user asks to "build a DevSecOps
  pipeline for a Lambda function from scratch," "gate a serverless release
  on execution-role scope instead of admission policy," "sign a Lambda
  deployment package," or "make sure a Lambda function's secrets aren't
  baked into its zip."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Complete DevSecOps Pipeline Deployment for Serverless, From Scratch

## Purpose

A serverless DevSecOps pipeline's gate sequence differs from the
Kubernetes variant of this skill in two structural ways. First, its SCA
surface is proportionally larger and riskier: a Lambda zip bundles its
**entire** transitive dependency tree directly into the one artifact that
ships (no separate, independently-scanned base-image layer to isolate OS
packages from application code), so a vulnerable indirect dependency is
just as deployed as the top-level ones. Second, there is no cluster to
put an admission-policy gate in front of — the closest equivalent
"last line of defense" gate is **the function's own IAM execution role**:
scoping it to least privilege is the release gate that most directly
bounds what a compromised function can actually do, in the same way an
admission policy bounds what a compromised pod can do in Kubernetes.
Secrets, too, follow a different model from both other variants: fetched
directly from a managed secrets service (AWS Secrets Manager/Parameter
Store, Azure Key Vault) by the function's own runtime code using its
execution role's identity, never baked into the zip and never pulled by
an in-cluster operator (there is no cluster).

## When to use

- A serverless pipeline has individual security tools bolted on ad hoc,
  and the user wants the full gate sequence — including execution-role
  scoping as a release gate and package signing — designed coherently
  from scratch.
- The user is building a new Lambda-based service's pipeline and wants
  security gates designed in from the start.
- The user wants to understand why a serverless pipeline's primary release
  gate is IAM role scope rather than a Kubernetes-style admission policy,
  and how that changes what "the security review before shipping" actually
  checks.
- Diagnosing why a Lambda function's execution role has drifted broad
  ("just add the permission and move on") and needs to be pulled back to
  least privilege as part of the pipeline, not a one-off audit.

## Prerequisites & environment

- A working CI/CD pipeline that already packages a zip/layer, uploads it,
  and deploys via SAM/Serverless Framework with alias-based traffic
  shifting — see
  [complete-cicd-pipeline-deployment-for-serverless-from-scratch](../../../cicd-tooling/skills/complete-cicd-pipeline-deployment-for-serverless-from-scratch/SKILL.md)
  for that base pipeline; this skill adds the security-gate layer onto it.
- SAST and SCA tooling chosen per
  [sast-integration](../sast-integration/SKILL.md) and
  [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md).
- Artifact-signing tooling (Sigstore/cosign, or AWS Signer for Lambda)
  per
  [supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md).
- IAM least-privilege review practice per
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  and the execution-role scoping guidance in
  [aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md).
- A managed secrets service (AWS Secrets Manager, Azure Key Vault) already
  provisioned, per
  [secrets-management](../secrets-management/SKILL.md).

## Step-by-step guidance

### Phase 1 — SAST on the diff (PR-time)

Per [sast-integration](../sast-integration/SKILL.md): unchanged from any
other pipeline.

### Phase 2 — SCA against the fully-resolved, packaged dependency tree

This is where the serverless-specific risk lives. Scan **after** the
install/bundle step (`pip install -t package/`, `npm ci --omit=dev`), not
just the top-level manifest, since the entire resolved tree ships as one
artifact with no separate layer boundary the way a container image has
between base-OS and application dependencies:
```yaml
  sca:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: function-package }
      - run: |
          unzip -q function.zip -d unpacked/
          trivy fs --severity CRITICAL,HIGH --exit-code 1 unpacked/
```
Because a typical Lambda's own code is often a few hundred lines while its
`node_modules`/site-packages can be tens of thousands of files, a much
larger share of the *actual attack surface* here comes from transitive
dependencies than for a comparable Kubernetes service running behind a
slimmed, distroless runtime image — weight remediation effort
accordingly, per
[software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md).

### Phase 3 — Package/artifact signing

Sign the built zip (or the container image, if using Lambda's
container-image packaging option) so its provenance is verifiable before
deploy, per
[supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md):
```bash
cosign sign-blob --key awskms:///alias/lambda-signing-key \
  --output-signature function.zip.sig function.zip
```
Or, using AWS Signer's native Lambda code-signing integration:
```bash
aws signer put-signing-profile --profile-name payments-webhook-signing \
  --platform-id AWSLambda-SHA384-ECDSA
aws lambda update-function-code --function-name payments-webhook \
  --zip-file fileb://function.zip --code-signing-config-arn "${CSC_ARN}"
```
With a `CodeSigningConfig` attached and set to `Enforce`, Lambda itself
refuses to update the function's code from an unsigned or
signature-mismatched package — this is a deploy-time technical control,
not just a CI-side check, and is the serverless equivalent of requiring an
admission-controller-verified signed image in Kubernetes (per
[supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md)).

### Phase 4 — Least-privilege execution-role scoping as the primary release gate

Where the Kubernetes variant's primary pre-deploy gate is a policy check
on the rendered manifest, the serverless equivalent is a **diff review of
the function's execution role** against what it actually calls — since
there's no cluster-side admission control to catch an over-broad grant
after the fact, this has to be caught before the role change ships:
```yaml
  iam-role-diff-gate:
    needs: sca
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          NEW_ACTIONS=$(python3 scripts/diff_iam_actions.py template.yaml)
          if [ -n "$NEW_ACTIONS" ]; then
            echo "New IAM actions requested, requires review: $NEW_ACTIONS"
            exit 1
          fi
```
A role-diff gate that fails routes to manual security review rather than
auto-blocking forever — the point is to force a deliberate look at *why*
a function suddenly needs `s3:DeleteObject` or `dynamodb:*`, not to make
every role change impossible. Pair this with the actual policy authored
per
[aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md)'s
least-privilege guidance — resource-ARN-scoped statements, not
`Resource: "*"`.

### Phase 5 — Deploy (unchanged from the base CI/CD pipeline)

Package upload, SAM/Serverless Framework deploy, alias-based canary — per
[complete-cicd-pipeline-deployment-for-serverless-from-scratch](../../../cicd-tooling/skills/complete-cicd-pipeline-deployment-for-serverless-from-scratch/SKILL.md).

### Phase 6 — Secrets: fetched by the function at runtime, never baked in

The function's own code, at invoke time, calls the managed secrets service
directly using the execution role's own identity — the deployment package
never contains a secret value, and there is no cluster-side operator
involved (unlike Kubernetes's External Secrets Operator model):
```python
import boto3
_secrets_client = boto3.client("secretsmanager")

def get_db_credentials():
    resp = _secrets_client.get_secret_value(SecretId="payments-webhook/prod/db")
    return json.loads(resp["SecretString"])
```
The execution role (scoped per Phase 4) grants exactly
`secretsmanager:GetSecretValue` on that one secret ARN — nothing broader —
and CI never sees the secret value at any point in the pipeline.

### Phase 7 — Verify

```bash
aws lambda get-function --function-name payments-webhook --query "Configuration.CodeSigningConfigArn"
aws lambda get-policy --function-name payments-webhook
aws iam get-role-policy --role-name payments-webhook-execution-role --policy-name inline-policy
```
Confirm the code-signing config is attached and enforcing, and that the
execution role's actual policy document matches what Phase 4's diff gate
reviewed — no drift introduced by a manual console edit after deploy.

## Best practices

- Treat the execution-role diff (Phase 4) as the gate most worth a
  human's attention — a signed package with a known-good SCA scan can
  still be dangerous if its execution role was quietly broadened, since
  IAM scope (not the code itself) is what bounds a compromised function's
  reach.
- Scan the *unpacked* deployment package (Phase 2), not the top-level
  manifest — this is the single highest-leverage difference from a
  container pipeline's SCA step, since there's no separate base-image
  layer to isolate OS-level risk.
- Enforce code signing (`CodeSigningConfig` with `Enforce`, not `Warn`)
  once the signing pipeline is proven reliable — a signing requirement set
  to warn-only is bypassed the first time someone needs to deploy in a
  hurry.
- Fetch secrets by resource ARN, never a wildcard `secretsmanager:*` or
  `Resource: "*"` grant, even for a function that legitimately needs
  several secrets — one scoped statement per secret ARN.
- Cache secret values in the function's execution environment (module-
  level, outside the handler) across warm invocations rather than calling
  the secrets service on every single invoke — reduces both latency and
  the secrets service's request volume, mirroring the cold-start
  mitigation guidance in
  [aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md).

## Common pitfalls

- **Symptom:** A function's execution role was broadened to include
  `dynamodb:*` "to unblock a deploy," and six months later nobody
  remembers which of the function's code paths actually needs write
  access versus just read.
  **Fix:** This is exactly what the Phase 4 role-diff gate exists to
  catch at the moment the change is proposed — audit the current role
  against CloudTrail's actual API call history for the function
  (`aws cloudtrail lookup-events` filtered by the function's role) to
  determine real usage, then scope the policy down to those specific
  actions/resource ARNs.

- **Symptom:** The SCA scan (Phase 2) reports clean because it only
  checked `package.json`/`requirements.txt`, but the deployed zip (after
  `npm ci --omit=dev`) contains a vulnerable transitive dependency that
  never appeared in the scan.
  **Fix:** Scan the unpacked, fully-resolved package after the
  install/bundle step, not the manifest alone — identical lesson to the
  base CI/CD serverless skill, restated here because it's specifically the
  SCA gate this pipeline depends on catching.

- **Symptom:** Code signing is configured with `CodeSigningConfig.Policy:
  Warn`, and an unsigned or tampered package deploys successfully anyway,
  only surfacing a warning in CloudWatch nobody was watching.
  **Fix:** `Warn` mode logs but does not block — set `Policy: Enforce`
  once the signing step (Phase 3) is confirmed to run reliably in the
  pipeline, so an unsigned package is technically rejected at deploy time,
  not just flagged after the fact.

- **Symptom:** A secret value shows up in CloudWatch Logs because the
  function's error-handling code logs the full exception object from a
  failed `get_secret_value` call, including the secret string in a
  downstream retry's debug output.
  **Fix:** This is the same log-redaction lesson as
  [secrets-management](../secrets-management/SKILL.md) — never log the
  raw response object from a secrets-service call; log only the secret's
  identifier/ARN and a boolean success/failure, and add structured-logging
  field redaction for known secret-shaped values as a backstop.

## Worked example

**Scenario:** `payments-webhook` gets its full DevSecOps gate sequence:
SAST/SCA on the packaged dependency tree, cosign signing of the zip, an
IAM-role-diff review gate before deploy, and its database credential
fetched at runtime from AWS Secrets Manager instead of baked into the
package.

```yaml
jobs:
  sast: { /* per sast-integration */ }
  build: { /* zip packaging, per the base serverless CI/CD skill */ }

  sca:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: function-package }
      - run: |
          unzip -q function.zip -d unpacked/
          trivy fs --severity CRITICAL,HIGH --exit-code 1 unpacked/

  sign:
    needs: sca
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: function-package }
      - run: cosign sign-blob --key awskms:///alias/lambda-signing-key --output-signature function.zip.sig function.zip

  iam-role-diff-gate:
    needs: sign
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/diff_iam_actions.py template.yaml

  deploy:
    needs: iam-role-diff-gate
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: sam deploy --stack-name payments-webhook --no-confirm-changeset --capabilities CAPABILITY_IAM
```
`payments-webhook`'s handler calls `secretsmanager:GetSecretValue` on
exactly `payments-webhook/prod/db` at invoke time; its execution role
(reviewed by the `iam-role-diff-gate` job whenever `template.yaml`'s IAM
statements change) grants nothing broader — no secret value, signing key,
or vault token is ever present in the CI pipeline itself.

## Cross-references

- [complete-cicd-pipeline-deployment-for-serverless-from-scratch](../../../cicd-tooling/skills/complete-cicd-pipeline-deployment-for-serverless-from-scratch/SKILL.md) — the base packaging/deploy pipeline this skill adds security gates onto.
- [sast-integration](../sast-integration/SKILL.md) and [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md) — Phase 1-2 gate mechanics.
- [supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md) — Phase 3's signing/provenance mechanics.
- [aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md) — execution-role least-privilege design referenced in Phase 4.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — the least-privilege review principles Phase 4's gate applies.
- [secrets-management](../secrets-management/SKILL.md) — the managed-secrets-service pattern used in Phase 6.
- [complete-devsecops-pipeline-for-kubernetes-from-scratch](../complete-devsecops-pipeline-for-kubernetes-from-scratch/SKILL.md) and [complete-devsecops-pipeline-for-vm-based-workloads-from-scratch](../complete-devsecops-pipeline-for-vm-based-workloads-from-scratch/SKILL.md) — the same gate-sequencing goal with fundamentally different primary gates and secrets models.
