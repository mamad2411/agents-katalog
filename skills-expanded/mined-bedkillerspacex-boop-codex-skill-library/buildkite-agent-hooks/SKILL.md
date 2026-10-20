---
name: buildkite-agent-hooks
description: >
  Buildkite agent hooks for owned CI fleets: environment, pre-checkout, pre-command,
  post-command, pre-exit hooks, secrets injection patterns, hook security, timeouts,
  and fleet consistency. Use when customizing Buildkite agents, shared hooks on
  bastion/builders, or hardening hook scripts — not for attacking shared CI.
---

# Buildkite Agent Hooks

## Scope And Authorization

- **In scope:** Buildkite organizations, pipelines, and agents you administer.
- **Out of scope:** Modifying hooks on agents you do not own; stealing pipeline secrets.
- Hooks run as the agent user with often broad SCM/cloud access — treat as privileged code.
- Redact secrets from hook debug logs.
- Pair pipeline design with `ci-cd-pipeline-patterns`; secrets with `secrets-management-hygiene`.

## When To Use

- Standardizing checkout, auth (cloud OIDC, vault), or artifact setup across agents.
- Injecting environment policy (proxy, GOPROXY, npm registry) before jobs.
- Cleaning workspaces, collecting logs, or notifying on `pre-exit`.
- Hardening existing hooks against untrusted pipeline injection.
- Debugging “works on one agent only” drift caused by local hooks.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General CI/CD patterns | `ci-cd-pipeline-patterns` |
| GitHub Actions specifics | GHA skills |
| Secret inventory program | `secrets-management-hygiene` |
| Supply chain for build images | container/supply-chain skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Hook | When it runs | Typical use |
| --- | --- | --- |
| `environment` | Early env setup | Export policy vars, secrets fetch |
| `pre-checkout` | Before git checkout | SSH known_hosts, clean dir |
| `post-checkout` | After checkout | Submodules policy, lfs |
| `pre-command` | Before command | Activate venv, login registries |
| `post-command` | After command | Parse junit, metrics |
| `pre-artifact` / `post-artifact` | Artifact phases | Scan artifacts |
| `pre-exit` | Always near end | Cleanup, workspace wipe |
| `agent-startup` / `agent-shutdown` | Agent lifecycle | Fleet bootstrap |

Paths (default patterns): under agent `hooks/` directory or `BUILDKITE_HOOKS_PATH` — confirm your install.

## Workflow

### 1. Confirm scope and success criteria

1. Record agent stacks (Linux/Windows), queue names, privileged vs untrusted pipelines.
2. Success: hooks version-controlled; identical across fleet; secrets not in world-readable scripts; untrusted PR pipelines cannot abuse hook assumptions.
3. Separate **trusted** release queues from **untrusted** PR queues when possible.

### 2. Inventory hooks and agent config

```bash
# On an agent host (authorized)
buildkite-agent --version
ls -la "${BUILDKITE_HOOKS_PATH:-/etc/buildkite-agent/hooks}"
# Agent config
sudo rg -n "hooks-path|command-eval|plugins|git" /etc/buildkite-agent/buildkite-agent.cfg
```

1. List custom plugins vs hooks ownership.
2. Note `command-eval` and plugin settings that expand attack surface.
3. Identify secrets currently hardcoded in hooks.

### 3. Baseline job environment

1. Run a diagnostic pipeline step: `env | sort` (redact) and capture which hook-exported vars appear.
2. Measure checkout times and failure rates pre-change.
3. Document required tools (docker, kubectl) provided by hooks vs images.

### 4. Implement hooks as code

**Principles:**

1. Store hooks in a controlled git repo; deploy via config management (Ansible/Puppet) or golden images.
2. `set -euo pipefail` on bash hooks; explicit exit codes.
3. Fail closed on secret fetch errors for release queues; decide fail mode for PR queues.
4. Never `eval` pipeline-provided strings in hooks.
5. Least privilege: hooks should not mark every job as global admin AWS role.

**Example `environment` sketch:**

```bash
#!/usr/bin/env bash
set -euo pipefail
# Fleet policy
export PIP_DISABLE_PIP_VERSION_CHECK=1
export DOCKER_BUILDKIT=1

# Example: only trusted pipelines get prod role
if [[ "${BUILDKITE_PIPELINE_SLUG}" == "app-release" ]]; then
  # Prefer OIDC/Vault over long-lived keys
  # source /opt/ci/fetch-role.sh
  :
fi
```

**Example `pre-exit` cleanup:**

```bash
#!/usr/bin/env bash
set -euo pipefail
# Wipe workspace if agent is sticky
if [[ -n "${BUILDKITE_BUILD_CHECKOUT_PATH:-}" ]]; then
  find "${BUILDKITE_BUILD_CHECKOUT_PATH}" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
fi
```

**`pre-command` docker login (secret via agent vault, not echo):**

```bash
#!/usr/bin/env bash
set -euo pipefail
if [[ -f /run/ci/registry_password ]]; then
  # password file mode 600 root:buildkite
  docker login -u "${REGISTRY_USER}" --password-stdin < /run/ci/registry_password
fi
```

### 5. Security review of hooks

| Risk | Mitigation |
| --- | --- |
| Untrusted PR modifies what hooks trust | Don’t trust repo content for auth decisions; use pipeline slug/org |
| Secret in hook world-readable | `chown root:buildkite`, mode `0750` scripts; secrets `0600` |
| Persistent workspace leak | `pre-exit` wipe; ephemeral agents |
| Plugin from untrusted source | Pin plugins; restrict plugin source |
| `command-eval` true | Avoid if possible; limit who can create pipelines |
| Checkout SSH key | Per-pipeline deploy keys; not one mega-key for all repos |

1. Hooks must treat build directory as **untrusted code**.
2. Do not automatically `source` files from the repository in global hooks without allowlist.

### 6. Verify

```bash
# Deploy hook to canary agent queue
# Pipeline step
echo "hello from job"
# Confirm env vars and cleanup
# Negative: untrusted pipeline cannot assume prod AWS creds
```

1. Failure injection: Vault down → job fails with clear message on release queue.
2. Confirm logs do not print secrets (`buildkite-agent annotate` careful).
3. Roll hooks to remaining fleet after canary.

### 7. Hand off

1. Document hook purposes and owners in runbook.
2. Version hooks (embed `HOOK_RELEASE=` echo in `environment` for support).
3. Apply `code-quality-standards` and shell style skills to scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Delivery | Git + config mgmt | Hand-edited on one agent |
| Secrets | Vault/OIDC file 0600 | `export AWS_SECRET=...` in hook |
| Trust | Queue-based prod access | Any PR job gets prod role |
| Cleanup | Wipe checkout in pre-exit | Sticky dirty workspaces |
| Eval | No eval of repo scripts | `source $BUILDKITE_BUILD_CHECKOUT_PATH/ci.sh` blindly |
| Debug | Redacted traces | `set -x` with secrets |

## Output Checklist

- [ ] Agent fleets and queues inventoried
- [ ] Existing hooks and cfg audited
- [ ] Hooks versioned and deployed consistently
- [ ] Secret injection hardened and least-privilege
- [ ] Untrusted pipeline isolation verified
- [ ] Cleanup/ephemeral strategy in place
- [ ] Canary verification done
- [ ] Runbook + owner documented
- [ ] `code-quality-standards` applied to hook scripts

## Rules

- Agent hooks are privileged malware-equivalent if compromised — control write access tightly.
- Never trust checkout contents for authorization decisions.
- Prefer ephemeral agents for untrusted code.
- Authorized Buildkite orgs only.
- Pipeline structure details → `ci-cd-pipeline-patterns`.
