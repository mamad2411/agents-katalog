---
name: appsec-scan
description: >
  Run the same security scanners as CI — locally, using identical container images —
  before pushing to GitLab, driven by admin-managed scanner preferences and the
  configured instance's CI/CD Catalog, per-component version pinning (~latest or
  exact tag), an optional glci engine, and optional GitLab-native dependency
  matching. Categories:
  SAST (Fortify SCA, multi-language: maven, gradle, python, javascript, go),
  Dependency Scanning (GitLab SBOM), Secret Detection (GitLab/Gitleaks),
  Container Scanning (GTCS). Single-command scan via run-scan.sh; normalized
  findings with verification statuses in findings.triaged.json; approval-gated
  fix loop (fix-branch.sh, ≤5 iterations) and guided triage plan (TRIAGE.md).
  Use when the user says: "appsec scan", "run security scanners", "run Fortify",
  "pre-push security check", "CI security pipeline locally", "mirror CI scanners",
  "security before merge", "scan profile", "catalog components", "triage plan",
  "fix security findings", "do all security scans", "full security scan",
  "scan everything", "is this safe to push".
  Also activate for a SINGLE category and scan only that one (Step 0 routes):
  SAST — "SAST scan", "static analysis", "run Fortify", "scan my code";
  Dependency — "dependency scan", "SCA scan", "check my dependencies",
  "any vulnerable libraries", "CVE check", "SBOM";
  Secrets — "secret scan", "secret detection", "any hardcoded secrets",
  "leaked credentials", "did I commit a key", "gitleaks";
  Container — "container scan", "image scan", "scan my Docker image", "GTCS".
  Do NOT activate for general code review, unit testing, or lint-only requests.
---

# AppSec Scan — Catalog-Driven CI Mirror

Run the same scanner images your GitLab CI pipeline uses, locally. `scripts/run-scan.sh` orchestrates all four scanners; `scripts/normalize.py` emits `.appsec-results/findings.triaged.json` with per-finding `verification_status`, driving the severity gate. `scripts/fix-branch.sh` guards the fix loop. **Config:** `config/scanner-preferences.yaml`. **Versions/pins:** `version:` in category block → UPDATE-GUIDE.md.

**Shell session:** shell contract in Step 1 — bash, one invocation per step; `run-scan.sh` self-locates/self-loads (incl. runtime), so Steps 3 and 5 are safe standalone.
**Exit-code contract:** `run-scan.sh` exits 0 (gate passed), 1 (gate failed / findings present), 2 (usage, or a `CONFIG-ERROR:` — exits 2 at any `fail_on`).

## Prerequisites

| Variable | Description |
|---|---|
| `APPSEC_PROFILE` | Active profile (`default_profile` from config) |
| `FORTIFY_VARIANT` | Fortify JDK variant (e.g. `jdk21-review`); auto-detected from the Java release, set only to override |
| `SOURCE_PATH`/`FORTIFY_LANGUAGE` | `maven`\|`gradle`\|`python`\|`javascript`\|`go`. Unset = every build tree found and scanned, one run each; either set pins a single unit |
| `CS_IMAGE` | Container image:tag for Container Scanning (opt.) |
| `APP_NAME` | App name (default: `basename $PWD`) |
| `GLCI_BIN` | Path to `glci` (optional; `engine: glci`) |

---

## Step 0 — Decide what to scan

Set `SCAN_SCOPE` from the user's words **before** running anything.

| The user asked about | `SCAN_SCOPE` |
|---|---|
| their code, SAST, static analysis, Fortify | `sast` |
| dependencies, libraries, packages, SCA, CVEs, SBOM | `dependency_scanning` |
| secrets, credentials, API keys, tokens, gitleaks | `secret_detection` |
| a container, an image, Docker, GTCS | `container_scanning` |
| everything, a full scan, pushing safely, or bare `/appsec-scan` | `all` |
| anything you are not sure about | **ask — below** |

**When unsure, ask — never guess.** Use `AskUserQuestion` with `multiSelect: true`;
label by what users recognise, not tool name:

- `Everything (recommended)` — all four; exactly what CI will run
- `My source code` — injection, unsafe calls, insecure patterns in code you wrote
- `My dependencies` — known CVEs in libraries you pull in
- `Hardcoded secrets` — keys, tokens, passwords committed by accident
- `My container image` — OS and package CVEs in the image you ship

Map the answer to the table's `SCAN_SCOPE` values; if several are picked but not
all four, run Step 3 once per category.

A scoped scan still reports the categories it did **not** cover. Never present a scoped result as "you are clear to push." Containers + >1 Dockerfile: ask scope AND Dockerfiles together, one `AskUserQuestion` (`multiSelect`, add "All") — never twice; pass picks as `APPSEC_DOCKERFILES=<paths>`.

---

## Step 1 — Locate the skill's directories

The scanner scripts live beside this file, not in the project being scanned. Its directory is `SKILL_DIR` — substitute the real absolute path below. Do **not** derive it from `$0`/`${BASH_SOURCE[0]}`: those resolve to your shell, yielding `/bin`.

```bash
export SKILL_DIR=/absolute/path/to/plugins/appsec/skills/appsec-scan
export SCANNERS_DIR="$SKILL_DIR/scanners"
export SCRIPTS_DIR="$SKILL_DIR/scripts"
[ -d "$SCANNERS_DIR" ] && [ -d "$SCRIPTS_DIR" ] || {
  echo "ERROR: wrong SKILL_DIR='$SKILL_DIR'" >&2; exit 1; }
```

**Shell contract — applies to every snippet here.** Run them with `bash`, not
your login shell, and send each step as ONE invocation. Both failure modes are
silent: exports do not survive between tool calls, and zsh (the macOS default)
does not word-split unquoted variables the way these snippets expect. Every
script self-loads what it needs, so a step that only invokes one is safe alone.

---

## Step 1.5 — Load scanner preferences and detect runtime

Run `scripts/load-prefs.sh` — it parses `config/scanner-preferences.yaml` and
prints ready-to-eval shell assignments. Do not parse the YAML yourself and do
not infer endpoints or images: everything the run needs is emitted by the
script, and the runner→`RUN_*` flag mapping table lives in its header comment.

```bash
PREFS_ENV="$(bash "$SCRIPTS_DIR/load-prefs.sh" "$SKILL_DIR/config/scanner-preferences.yaml")" || {
  echo "ERROR: failed to load scanner preferences — see the message above."
  echo "Fix config/scanner-preferences.yaml (or unset APPSEC_PROFILE) and re-run."
  return 1 2>/dev/null || exit 1
}
eval "$PREFS_ENV"
# Now set: APPSEC_PROFILE, APPSEC_AIRGAP, CONTAINER_RUNTIME, GITLAB_INSTANCE,
# CATALOG_AUTH_ENV, FORTIFY_SAST_IMAGE, SECRET_DETECTION_IMAGE, GITLAB_DS_IMAGE,
# GITLAB_CS_IMAGE (may be empty, see below), RUN_FORTIFY_SAST, RUN_GITLAB_DS,
# RUN_SECRET_DETECTION, RUN_GITLAB_CS, ENABLED_COMPONENTS ("component|version|
# runner|image|category" tuples), plus jq/python, registry, airgap settings,
# ENGINE_*, REMOTE_MATCH_PROJECT, CATALOG_GLAB_FALLBACK, DISABLED_CATEGORIES
# and CATEGORY_NOTE_* — all listed in load-prefs.sh's header.

# Detect the container runtime (docker or podman) — hard requirement.
RUNTIME="$(CONTAINER_RUNTIME="$CONTAINER_RUNTIME" bash "$SCRIPTS_DIR/detect-runtime.sh")" || {
  echo "ERROR: no container runtime (docker or podman) found"
  return 1 2>/dev/null || exit 1
}
export RUNTIME

echo "Profile: $APPSEC_PROFILE   GitLab: $GITLAB_INSTANCE   Runtime: $RUNTIME   Airgap: $APPSEC_AIRGAP"
```

- An empty `*_IMAGE` is normal: `image:` is optional, and under the default
  `image_policy: follow-component` Step 3 derives it from the component template.
  A `*_IMAGE` env var set before the run still wins; an image neither derived nor
  configured stops the scan (never a silent skip).
- load-prefs.sh exits nonzero (unknown profile, or `airgap: true` with a
  `gitlab.com` `gitlab_instance`): show its stderr verbatim and stop.
- `GITLAB_INSTANCE` still `*.example`, or images still `jfrog.internal/...`: not
  configured yet — stop and point the user to `config/PREFERENCES.md`.

---

## Step 2 — Preflight: validate required environment

Runs `scanners/preflight.sh` in its own process — shellchecked, runnable standalone.

```bash
CATALOG_AUTH_ENV="$CATALOG_AUTH_ENV" APPSEC_AIRGAP="$APPSEC_AIRGAP" \
  APPSEC_PROFILE="$APPSEC_PROFILE" CONTAINER_RUNTIME="$CONTAINER_RUNTIME" \
  bash "$SCANNERS_DIR/preflight.sh" || { return 1 2>/dev/null || exit 1; }
```

If preflight fails, show its output and stop — error lines name which
variables to set. Never scan against an incomplete environment.

---

## Step 2.5 — Resolve CI/CD Catalog components (every run)

For every **enabled** category component, resolve against the catalog and check
drift. `scripts/catalog.sh` is the only thing that talks to the network here,
only to `$GITLAB_INSTANCE`.

```bash
bash "$SCRIPTS_DIR/resolve-components.sh"
```

Resolves every enabled component, checks drift, and prints a resolution table —
one row per component, e.g. `| lobster-thermidor/devops/ci-catalogue/fortify-sast/fortify-sast
| 25.2.0 | online | — |`. Show it to the user verbatim before scanning, then act
on any prefix lines below.

Components are always resolved live; a failed fetch falls back to the vendored
snapshots in `reference/catalog/`. The two causes differ: an unreachable
`$GITLAB_INSTANCE` is the airgap guarantee working — say so, continue on the
snapshot. A `$CATALOG_AUTH_ENV` PAT rejected, expired, or lacking `read_api` is
a `CONFIG-ERROR:` — stop, never let it read as live (same rule as re-vendoring).

Scripts signal everything else with five prefixes. Surface the line verbatim,
then:

| Prefix | Required action |
|---|---|
| `ADVISORY:` | informational: newer tag, additive input, unsupported engine, or fallback taken — report it, change nothing |
| `DRIFT:` | a configured `image:` differs from the component's; report, never auto-bump it |
| `CONTRACT-DRIFT:` | the component's inputs or reports changed vs `scanners/<runner>.contract`; explain what it affects and ask before scanning |
| `NEEDS-MAPPING:` | the component supports something no runner implements; stop and ask |
| `CONFIG-ERROR:` | your configuration is wrong; stop that category, surface the line verbatim, attempt no alternative |

`template.yml` is the only machine source of truth; `AGENTS.md` is cached for
guidance (offer to summarize) but lags it — never derive behaviour from AGENTS.md.

---

## Step 3 — Run the scan

```bash
bash "$SCRIPTS_DIR/run-scan.sh"                        # SCAN_SCOPE=all
bash "$SCRIPTS_DIR/run-scan.sh" --only "$SCAN_SCOPE"   # one category from Step 0
```

run-scan.sh invokes `"$RUNTIME" run`/`pull` per scanner; `resolve-jq.sh`, `detect-sast-units.sh` and `container-target.sh` run internally (`GITLAB_FEATURES=dependency_scanning` for DS). **Fortify fans out**: `detect-sast-units.sh` finds every build tree; each gets its own run, report and coverage row. DS does not — its analyzer walks the worktree once. A scanner with no report becomes a HIGH coverage finding (HAS_MISSING_REPORT). Stdout: summary from `normalize.py`. **Branch on exit code AND `coverage_complete` (`scan-coverage.json`), never the code alone**: exit 1 → findings, Step 4; exit 0 + complete → done; exit 0 + incomplete → NOT an all-clear: name each `missing_report` category and why (`evidence.why`), then require a full scan before pushing; exit 2 → name each `CONFIG-ERROR:` line and its fix, never present the run as a pass. `fail_on: none` always exits 0 for findings, but not over a config error — that still exits 2. Flags: `--dry-run`; `--only <category>` (sast|dependency_scanning|secret_detection|container_scanning) — Step 0 scope or Step 5 rescan. `--only` narrows what RUNS, never what is EXPECTED, so a scoped verdict needs the same rule plus a full scan before pushing. **Engines:** `engine: glci` runs secret_detection/container_scanning live (sast/DS: docker); unavailable/failed ⇒ `ADVISORY:`+docker or a gap. **Dockerfiles:** `$DOCKERFILE`>`$APPSEC_DOCKERFILES`>`detect-dockerfiles.sh`; >1 ⇒ one report each; disabled ⇒ not-covered, never clean.

Dependency Scanning produces only an SBOM locally (GitLab matches it server-side behind a `CI_JOB_TOKEN`-only API), so run-scan.sh matches it offline with the Trivy bundled in the container-scanning image. **Those findings and their `fixed_version`s are Trivy's, not GitLab's** — say so: a pre-push signal that will not match the post-push Vulnerability Report exactly. If that match cannot run it becomes a coverage skip. `remote_match_project` set ⇒ GitLab-native match instead (manifests/lockfiles only); state the source (`gitlab-native` vs `offline-trivy`, caveat) from `scan-coverage.json`; `APPSEC_REMOTE_MATCH=off` forces offline.

---

## Step 4 — Review findings

Read `.appsec-results/findings.triaged.json`. Present each finding: severity, name, scanner, location, `verification_status`, `triage_reason` (override with explicit reasoning if warranted). Secret Detection: show only the redacted list from the summary (`Secret Detection findings (redacted)`) — never read raw values from `gl-secret-detection-report.json`.

---

## Step 5 — Fix loop

```bash
bash "$SCRIPTS_DIR/fix-branch.sh" --init --approved
```

Names the branch `appsec/fix-<YYYYMMDD>-<shortsha>`. Ask for approval once before making changes — it will create a new branch; `--init` needs `--approved` (pass only once approved). Offer a choice: fix all actionable (≤5 iter) or review one by one (ask per fix). **Skip every finding whose `remediation_status` is `blocked_registry_gap`** — the upgrade is not in the mirror, so attempting it burns an iteration and cannot succeed; it belongs in TRIAGE.md §3b. Loop maximum **5 iterations**: apply fixes → rescan ONLY the affected category (`bash "$SCRIPTS_DIR/run-scan.sh" --only <category>`; for secret findings, rerun only GitLab Secret Detection first) → `bash "$SCRIPTS_DIR/fix-branch.sh" --check-progress <prev_count> <curr_count>` — the two `ACTIONABLE C+H` **counts**, not file paths (exits 1 on cap/no-progress → stop). When the loop ends, run the app's relevant tests. Never push or open an MR without the user explicitly asking. Never rewrite git history.

---

## Step 6 — Generate the triage plan (TRIAGE.md)

After the loop, write `.appsec-results/TRIAGE.md` for every finding not fixed —
the user's guided companion for GitLab's Vulnerability Report triage after they push.

Sort every unfixed finding into exactly one section. Only section 4 is a GitLab
dismissal — elsewhere a dismissal reason points at something not in the
Vulnerability Report.

```markdown
# AppSec Triage Plan — <APP_NAME> @ <shortsha> (<date>, profile: <profile>)

## 1. Fixed on this branch
| Finding | Severity | Location | What changed |
|---|---|---|---|
(Then: "Verify with <command>". Omit the section if nothing was fixed.)

## 2. Must fix before push — NOT dismissible
Real findings still present, with no GitLab dismissal reason: fix them, or
consciously defer with an owner and date.
### <n>. [<severity>] <title> — <scanner>
- Location: <file:line> · Why not fixed here: <reason> · Owner / by when: <...>

## 3. Coverage gaps — NOT dismissible
A scanner that did not run produces no GitLab vulnerability — nothing to
dismiss; restore coverage instead. Copy the `why` text verbatim from each
`APPSEC-REPORT-*` finding — it names the fix.
### <n>. <category> did not run
- What to do: <the finding's evidence.why>

## 3b. Blocked — the fix is not in the mirror — NOT dismissible
Every `remediation_status: blocked_registry_gap` finding — the fix exists
upstream but the internal registry doesn't carry it. ONE batched table per kind
(one platform-team request, not one per finding); omit an empty table, the
section if both are empty.
| Package | Have | Need | Ecosystem | CVE |
|---|---|---|---|---|

| Base image | Tag to mirror | Dockerfile line | Findings it blocks |
|---|---|---|---|
- What to do: ask the platform team to mirror the packages and images above, then re-run.

**Suggestion only — hardened base images.** Include ONLY when `hardened_repo`
returned a hit; nothing was applied, no status changed. A hardened image is a
*different* image (different libc, often no shell/package manager, non-root
UID) — a human decides whether this build can take it.
| Current base | Hardened candidate | What to check before swapping |
|---|---|---|

## 4. Dismiss in GitLab
Secure → Vulnerability report → open the finding → **Dismiss vulnerability** →
pick a reason below → paste the justification (a comment is mandatory).
### <n>. [<severity>] <title> — <scanner>
- Location: <file:line or image:layer>
- Dismissal reason: `<one of the five below>`
- Justification (paste-ready): "<2-3 sentences: what was assessed, why this
  reason applies, compensating controls, review-by date if temporary>"
```

Section 4 only: use exactly one of GitLab's five dismissal reasons — never in
sections 2 or 3.

| Reason | Use when |
|---|---|
| `false_positive` | The scanner is wrong — the flagged pattern is not exploitable |
| `used_in_tests` | The finding lives in test code/fixtures, never in production |
| `acceptable_risk` | Real but consciously accepted — name the owner + review date |
| `mitigating_control` | A compensating control (WAF, network policy, authz) neutralizes it |
| `not_applicable` | The affected code path is unused/unreachable/being decommissioned |

Findings the branch will fix (once merged) don't belong in TRIAGE.md — they
resolve in the next default-branch pipeline.

---

## DAST (web + API)

Use **appsec-dast-sim** (same plugin) for design-time DAST (no running app required).

---

## What NOT to do

- **Do not work around a `CONFIG-ERROR:`.** Stop that category, report the line
  verbatim, try no alternative image, registry, credential, endpoint, profile
  or invocation — only the admin can fix config; routing around it hides the
  cause behind a result that reads clean
- Do not edit scan mechanics or scanner commands here — edit `scripts/run-scan.sh`/`scanners/*.sh` instead
- Do not add `fortifyclient` upload steps — scan-only is the local model
- Do not print raw secret values from `gl-secret-detection-report.json`
- Do not treat removing a detected value from source as credential rotation
- Do not commit `.appsec-results/` to git
- Do not contact any network endpoint other than the active profile's
  `gitlab_instance` (catalog metadata) and the configured image registries
- Do not rewrite git history, and do not push or open MRs without the user
  explicitly asking
