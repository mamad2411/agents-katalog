---
name: "iac-toolchain-provisioning"
description: "Technology-agnostic rule for provisioning the IaC validation CLI on demand (not installed by default) and running BASIC OFFLINE validation in the terminal WITHOUT any cloud login — resolved from cloud_provider + iac_format. Detects the OS/package manager, installs the right tool (terraform, bicep, cfn-lint, spectral, deck, helm/kubeconform...), then runs login-free checks (e.g. terraform fmt -check; terraform init -backend=false; terraform validate)."
version: 1
created: "2026-06-25T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use before reporting an IaC artifact deployable, in ANY cloud and ANY format. The validation CLI is usually NOT
pre-installed, so this skill PROVISIONS it on demand and then runs **basic, offline, login-free** validation.
Stack-independent: resolve the tool from `cloud_provider` + `iac_format` (and the artifact itself), install it,
verify it, run it. This mirrors how the JVM build path uses `build-toolchain-alignmentv2` — but for IaC.

## Core Principle
"Validation" here means **static / offline** checks that need NO cloud credentials and touch NO real account:
syntax, formatting, schema, type, and provider-plugin resolution. NEVER `login`, NEVER `apply`/`deploy`/`plan`
against a live cloud, NEVER configure credentials, NEVER use a remote backend. If a check would require auth,
skip it and mark it `review-only` — do not fake a pass.

## ⛔ TOOL-CALL DISCIPLINE (operating constraint)
The runtime hard-terminates the agent at ~100 `command_line` calls. Stay far below it.
- READ files with the native `read_file` tool; CREATE/edit with native `write_file` — NOT shell cat/echo/heredoc.
- Use `command_line` ONLY for genuine shell needs: install a CLI, run a validator.
- ≤ ~20 `command_line` calls per invocation. BATCH installs; run each validator ONCE; never re-run for a
  different result; no sleep/poll loops. Scope every find/grep to the artifact dir; never scan from `/` or `~`.

## Procedure
1. **Resolve the tool(s)** from `cloud_provider` + `iac_format` (see matrix below).
2. **Probe first** — `command -v <tool>`; if already present and `--version` works, skip install.
3. **Detect OS + package manager** (run once):
   - Debian/Ubuntu → `apt-get`  · Alpine (musl) → `apk`  · RHEL/Fedora → `dnf`/`yum`  · macOS → `brew`
   - Detect Alpine via `/etc/alpine-release` (or `ldd --version` reporting musl).
   - Python linters → `pip`/`pipx`; Node linters → `npm`/`npx`.
4. **Install** the tool with the detected manager, or download the official static binary for the platform.
   - **Alpine/musl caution:** prefer `apk add` packages; if downloading a binary, get the musl/static build —
     a glibc-only binary fails on musl with loader/`Exec format` errors. (Same trap as glibc JDKs on Alpine.)
5. **Verify** the install (`<tool> --version`) before using it.
6. **Run the offline validators** (matrix below); capture exit code + stdout/stderr for the report.
7. **Network-locked fallback** — if no network / locked registry blocks the install, do NOT fake a pass: mark
   the gate `review-only` (or `BLOCKED-ON-ENV`), name the exact missing tool, and fall back to the
   documented-API audit from `iac-deployability-verificationv2`.

## Coverage principle (ALL clouds × ALL formats)
Cloud provider almost never changes WHICH validator you run — `iac_format` does. Azure, AWS, GCP, OCI, Alibaba,
IBM, and on-prem all use the SAME tool for a given format (e.g. Terraform is identical across clouds; only the
provider plugin differs, and `init -backend=false` fetches it without credentials). So: **resolve the validator
from `iac_format` first**, run the FULL offline battery for it, and add any cloud-specific extra. Run EVERY
applicable login-free check (syntax + lint + static security), not just one — capture each result.

## Universal offline layer (run for EVERY format, in addition to the per-format battery)
- **Static security / policy scan (no login):** `checkov -d .` (covers Terraform/CFN/Bicep/ARM/K8s/Helm/
  Serverless/ARM) ; `trivy config .` (IaC misconfig + secrets) ; OPA policy: `conftest test <file>`.
- **Secret scan (no login):** `gitleaks detect --no-git -s .` or `trivy fs --scanners secret .`.
- These need NO cloud auth. Install via `pip install checkov`, the trivy apt/apk pkg or static binary,
  `conftest`/`gitleaks` static binaries. If any can't install, mark that sub-gate review-only — keep the rest.

## Per-format battery (resolve from iac_format; same across ALL clouds incl. OCI/Alibaba/IBM/on-prem)
- **Terraform / OpenTofu** (Azure/AWS/GCP/OCI/any):
  install: `apt-get install -y terraform` (HashiCorp repo) · `apk add terraform` · static zip from
  releases.hashicorp.com (`tofu` for OpenTofu). Optional: `tflint`, `checkov`, `trivy`.
  RUN (no login): `terraform fmt -check -recursive` ; `terraform init -backend=false` ; `terraform validate` ;
  `tflint --recursive` ; `checkov -d .` ; `trivy config .`.
  If the registry is unreachable, run `fmt -check` + best-effort `init -backend=false` + `validate -no-color`
  and mark provider-dependent checks review-only.
- **CDK** (AWS/Terraform-CDK, any language): `npm ci` / `pip install -r` then `cdk synth --no-lookups` (offline,
  no creds) → produces CFN/TF → then run the CFN/Terraform battery on the synth output. (`cdk deploy` = login → skip.)
- **Bicep** (Azure): install `bicep` (`az bicep install` or `bicep-linux-x64`/musl binary).
  RUN: `bicep build <f>.bicep` ; `bicep lint <f>.bicep` ; `checkov -d .` ; `trivy config .`.
- **ARM templates** (Azure JSON): arm-ttk via `pwsh` (`Test-AzTemplate`) ; JSON schema check ; `cfn-lint` does
  not apply ; `checkov -d .` (supports ARM). (`az deployment ... validate` = login → skip.)
- **CloudFormation / SAM** (AWS): install `pip install cfn-lint`, `aws-sam-cli`.
  RUN: `cfn-lint <t>` ; SAM `sam validate --lint` ; `checkov -d .` ; `trivy config .`.
  (`aws cloudformation validate-template` = creds → skip.)
- **Google Cloud Deployment Manager / config-connector**: prefer the Terraform path; raw YAML → schema lint +
  `checkov`/`conftest`. (`gcloud deployment-manager` = login → skip.)
- **Pulumi** (any cloud, any language): `npm ci`/`pip install`/`go build` to TYPE-CHECK the program offline ;
  `checkov -d .` on any emitted IaC. (`pulumi preview`/`up` need a stack/login → skip, mark review-only.)
- **Ansible** (provisioning): `ansible-lint` ; `ansible-playbook --syntax-check` ; `yamllint`. (No `-i` against
  real hosts; no connection.)
- **OpenAPI / Swagger / API spec** (any gateway contract): install `npm i -g @stoplight/spectral-cli` or
  `pip install openapi-spec-validator`. RUN: `spectral lint <spec>` ; `openapi-spec-validator <spec>` ;
  `redocly lint <spec>` (if available).
- **Azure APIM policy XML**: `xmllint --noout <f>` (well-formed) + the APIM policy-expression documented-API
  audit from `iac-deployability-verificationv2`. No public offline semantic validator → mark semantic review-only.
- **AWS API Gateway** (REST/HTTP, OpenAPI + `x-amazon-apigateway-*`): `spectral lint` the OpenAPI ; if defined in
  CFN/SAM/Terraform, run that format's battery.
- **GCP API Gateway**: api-config is OpenAPI → `spectral lint` ; if via Terraform, the Terraform battery.
- **Apigee** (proxy bundle XML): `xmllint --noout` ; `apigeelint -s <proxydir>` (`npm i -g apigeelint`).
- **Kong**: `deck file lint` / `deck gateway validate` (offline) ; declarative YAML schema check.
- **Kubernetes / Gateway-API / Ingress / Helm / Kustomize**: install `helm`, `kubeconform`.
  RUN (no cluster): `helm lint <chart>` ; `helm template <chart> | kubeconform -strict -summary` ;
  `kustomize build <dir> | kubeconform -strict` ; `kubectl apply --dry-run=client -f <manifest>` ;
  `kubeconform -strict <manifest>` ; `checkov -d .` ; `conftest test`.
- **OCI Resource Manager** = Terraform with the `oci` provider → Terraform battery (no OCI login needed for
  fmt/init -backend=false/validate). **Alibaba/IBM/DigitalOcean/etc.** = same Terraform battery, different provider.

## Patterns
- Probe → detect OS/pkg-mgr → install → verify `--version` → run validator → capture output.
- Always pass the login-free flags: terraform `-backend=false`; never `plan`/`apply`; no `az/aws/gcloud` auth.
- Prefer the distro package manager; fall back to the official static binary for the right libc/arch.
- One install batch, one run per validator; record exit codes for the deployability report.

## Anti-Patterns
- Assuming the CLI is pre-installed (it is not) and skipping validation.
- Logging in / configuring credentials / running `plan`/`apply`/`deploy` to "validate".
- Reporting deployable from well-formedness when a real validator could have run.
- On Alpine/musl, installing a glibc-only binary (won't execute).
- Using `command_line` for file reads/writes (burns the tool budget); blind full-filesystem scans.

## Validation Rules
- TOOL-RESOLVED: the validator matching cloud_provider × iac_format is identified.
- INSTALLED-OR-BLOCKED: tool installed and `--version` verified, OR network-locked → review-only/BLOCKED-ON-ENV.
- LOGIN-FREE: no auth/login/credentials; no plan/apply/deploy; no remote backend.
- RAN-AND-CAPTURED: the FULL applicable offline battery executed once each (format-native syntax + lint +
  static security/secret scan + universal layer) — not just one check; exit code + output captured for each.
- HONEST-COVERAGE: each gate marked tool-verified vs review-only — never a false pass.

## RAG Sources
When use_rag is on, call `get_rag_context` to confirm the exact install command / offline-validation flags for
the resolved tool and OS, and any org-approved internal mirror/registry for air-gapped installs.
