# DeployGuard Guard Skill

Validates Kubernetes manifests and Terraform configs against the DeployGuard policy
ruleset. Acts as a senior reviewer: every violation explains *why it matters* and
*what to fix*, not just what's wrong.

**Trigger:** `/guard`

---

## Installation

```
~/.claude/skills/guard/SKILL.md     # global (available in all projects)
.claude/skills/guard/SKILL.md       # project-local
```

**Prerequisites:** `deployguard` package must be importable in the Python environment
where Claude Code is running.

```bash
pip install dg-deploy            # from PyPI
# or from the repo:
pip install -e /path/to/DeployGuard
```

Run `dg doctor` to confirm the package and its tools are ready.

---

## What it checks

| Rule | Default level |
|---|---|
| Missing `resources.requests` / `resources.limits` | ERROR |
| Missing `livenessProbe` / `readinessProbe` | ERROR |
| Missing pod `securityContext.runAsNonRoot` | ERROR |
| `:latest` or untagged image | ERROR |
| `runAsUser: 0` (root) | ERROR |
| `privileged: true` | ERROR |
| `automountServiceAccountToken` not disabled | WARN |
| Malformed YAML (`yaml_parse`) | ERROR |
| Schema violations (`kubeconform`) | ERROR (when installed) |
| Misconfigs (`trivy`) | ERROR/WARN (when installed) |

---

## Instructions for Claude

When the user invokes `/guard [args]`:

### Step 1 — Determine what to guard

- **Path argument** (e.g. `/guard k8s/` or `/guard deployment.yaml`): use that path.
- **Pasted manifest** (YAML block in the same message, no path given): write the YAML
  to a temp file (`/tmp/guard_input.yaml`), guard it, delete it after.
- **No argument, no YAML**: ask once — "What should I guard? Provide a path or paste
  a manifest."

### Step 2 — Check if deployguard is available

Run:
```bash
python3 -c "import deployguard.guard" 2>&1
```

- **If it succeeds**: proceed to Step 3.
- **If it fails**: tell the user `deployguard` is not installed and show the install
  command. Then fall back to Step 3b (manual review).

### Step 3a — Run the guard (package available)

Run the following Python snippet via Bash. Replace `TARGET` with the resolved path:

```bash
python3 - << 'PYEOF'
import sys
from deployguard.guard import guard, format_result
from rich.console import Console
import io

TARGET = "TARGET_PATH"

DEFAULT_RULES = {
    "require_resource_limits": "error",
    "require_probes": "error",
    "require_security_context": "error",
    "no_latest_tag": "error",
    "no_root_user": "error",
    "no_privileged_containers": "error",
    "iam_least_privilege": "warn",
}

result = guard(TARGET, DEFAULT_RULES, run_kubeconform=True, run_trivy=True)

buf = io.StringIO()
Console(file=buf, markup=True, highlight=False, width=100).print(
    format_result(result, explain=True)
)
print(buf.getvalue())
sys.exit(0 if result.passed else 1)
PYEOF
```

Read the output and present it per Step 4.

### Step 3b — Manual review (fallback, no package)

Read every `.yaml` / `.yml` file under the target path. For each manifest, apply the
rules in the table above using your own analysis. Produce the same output format as
Step 4 — grouped by file, with why-it-matters and what-to-add for each violation.
Make clear at the top that this is a manual review (no guard binary available).

### Step 4 — Present the results

**Group violations by file.** For each file that has violations, show:

```
── k8s/deployment.yaml ────────────────────────────────────────
ERROR  [require_resource_limits]
  Container 'api' is missing resources.requests and resources.limits.
  Why it matters: Without resource limits one pod can starve the node and bring
  down its neighbours. Kubernetes will not schedule your pod if the node is
  overcommitted.
  What to add: Add resources.requests and resources.limits to every container spec.

WARN   [iam_least_privilege]
  ServiceAccount 'default' does not explicitly disable automountServiceAccountToken.
  Why it matters: Auto-mounted tokens give every pod API server access by default.
  If a pod is compromised the token is the attacker's first lateral-movement tool.
  What to add: Set automountServiceAccountToken: false on the ServiceAccount.
```

End with a summary line:

```
Guard result: 3 error(s), 1 warning(s) — FAILED.
```
or
```
Guard result: 0 error(s), 0 warning(s) — PASSED. All manifests are clean.
```

**Rules for how you present findings:**
- Never list a bare rule name with no explanation. Every violation gets its full
  why-it-matters and what-to-add text.
- Do not suggest fixes that haven't been explained. Explain first, prescribe second.
- If a file has no violations, do not list it.
- If the guard passed, say so clearly in one line — do not pad with generic advice.
- Act as a senior reviewer, not a linter. Tone: precise and helpful, not alarming.

---

## Example invocations

```
/guard k8s/
/guard deployment.yaml
/guard .
/guard
<paste YAML here>
```

---

## Example output (3 violations, 1 file)

```
── k8s/deployment.yaml ────────────────────────────────────────────────────────

ERROR  [no_latest_tag]
  Container 'payments-api' uses image 'payments-api:latest' — no pinned tag.
  Why it matters: :latest is mutable — the image you tested is not guaranteed to
  be the image that deploys. Pinned tags make rollbacks and audits reliable.
  What to add: Pin every image to a specific digest or semantic version tag.

ERROR  [require_resource_limits]
  Container 'payments-api' is missing resources.requests and resources.limits.
  Why it matters: Without resource limits one pod can starve the node and bring
  down its neighbours. Kubernetes will not schedule your pod if the node is
  overcommitted.
  What to add: Add resources.requests and resources.limits to every container spec.

WARN   [iam_least_privilege]
  ServiceAccount 'default' does not explicitly disable automountServiceAccountToken.
  Why it matters: Auto-mounted tokens give every pod API server access by default.
  If a pod is compromised the token is the attacker's first lateral-movement tool.
  What to add: Set automountServiceAccountToken: false on the ServiceAccount.

Guard result: 2 error(s), 1 warning(s) — FAILED.
```

---

## Customising rule levels

Create `.deployguard/config.yaml` in your project to change rule levels:

```yaml
guard:
  strict: true          # false = warnings only, never block
  explain: true
  rules:
    iam_least_privilege: error    # promote to error for your team
    no_privileged_containers: off # suppress if your workload requires it
```

The skill picks up this config automatically when `deployguard` is installed.
