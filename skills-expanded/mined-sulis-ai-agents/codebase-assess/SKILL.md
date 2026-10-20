---
name: codebase-assess
description: "Deprecated — use /sulis:code-health instead."
---

# Codebase Viability Assessment

When invoked, run an OODA-spiral assessment against a target repository (and
optionally a deployed URL). Clone the repo to an isolated temp directory,
run automated tools, interpret findings, chain results across primitives, and
produce a structured viability report under `.security/{project}/`.

The framework — 25 primitives, 5 categories, scoring rubric — is defined in
[`../../references/viability-framework.md`](../../references/viability-framework.md).
The primitive catalogue lives in [`references/primitives.md`](references/primitives.md).
Tool invocation commands are in [`references/tool-commands.md`](references/tool-commands.md).

---

## Input

Accept three arguments:

| Parameter | Required | Description |
|---|---|---|
| `project-name` | Yes | Short identifier — used for the output directory under `.security/{project}/` |
| `repo` | Yes | Either `owner/repo` (cloned via GitHub App if configured) or a full git clone URL (cloned with existing git credentials) |
| `deployed-url` | No | URL of the deployed application for non-invasive DAST checks. Staging preferred; production safe for header/TLS checks |

**Example invocations:**

```
/sulis:codebase-assess acme acme-corp/platform
/sulis:codebase-assess acme acme-corp/platform https://staging.acme.com
/sulis:codebase-assess acme https://github.com/acme-corp/platform.git
```

If arguments are missing, ask the user — do not invent.

---

## GitHub App Authentication (Optional)

If the user wants org-controlled, revocable access to a private repo, they
can configure a generic GitHub App. The skill reads three environment
variables:

| Variable | Purpose |
|---|---|
| `GITHUB_APP_ID` | The App ID |
| `GITHUB_APP_PRIVATE_KEY` | Path to the `.pem` private key file |
| `GITHUB_APP_INSTALLATION_ID` | The installation ID for the target org |

App permissions (minimal):
- `contents: read`
- `metadata: read`

**Authentication flow:**

1. Generate a JWT (valid 10 minutes):

   ```bash
   python3 -c "
   import jwt, time
   app_id = '${GITHUB_APP_ID}'
   key = open('${GITHUB_APP_PRIVATE_KEY}').read()
   payload = {'iat': int(time.time()) - 60, 'exp': int(time.time()) + 600, 'iss': app_id}
   print(jwt.encode(payload, key, algorithm='RS256'))
   "
   ```

2. Exchange JWT for an installation access token:

   ```bash
   INSTALL_TOKEN=$(curl -s -X POST \
     -H "Authorization: Bearer ${JWT}" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/app/installations/${GITHUB_APP_INSTALLATION_ID}/access_tokens" \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
   ```

3. Clone using the installation token:

   ```bash
   git clone --depth 1 "https://x-access-token:${INSTALL_TOKEN}@github.com/{owner}/{repo}.git" "$ASSESS_DIR/repo"
   ```

**Fallback:** if the env vars aren't set, fall back to direct clone with the
user's existing git credentials. This is the default mode.

**Never log or persist the token.** Tokens expire in 1 hour; treat them as
secrets within the skill's execution.

---

## Setup: Isolated Clone

Before running any checks:

1. Create a temp directory: `/tmp/security-assessment/{project}-$(date +%s)/`
2. Clone the repo into `$ASSESS_DIR/repo/`
3. Create an output directory: `$ASSESS_DIR/outputs/`
4. Create the user-facing output directory: `.security/{project}/`

```bash
ASSESS_DIR="/tmp/security-assessment/{project}-$(date +%s)"
mkdir -p "$ASSESS_DIR/repo" "$ASSESS_DIR/outputs"

# GitHub App auth (if env vars set) OR direct clone
if [ -n "$GITHUB_APP_ID" ] && [ -n "$GITHUB_APP_PRIVATE_KEY" ] && [ -n "$GITHUB_APP_INSTALLATION_ID" ] && [[ "{repo}" =~ ^[^/]+/[^/]+$ ]]; then
  # ... JWT + token exchange (see above) ...
  git clone --depth 1 "https://x-access-token:${INSTALL_TOKEN}@github.com/{repo}.git" "$ASSESS_DIR/repo"
else
  git clone --depth 1 {repo-url} "$ASSESS_DIR/repo"
fi

mkdir -p .security/{project}
```

Use `--depth 1` initially. If Gitleaks needs full history (SEC-07 across the
git past), fetch it on demand:

```bash
cd "$ASSESS_DIR/repo" && git fetch --unshallow
```

**After the report is written, clean up:**

```bash
rm -rf "$ASSESS_DIR"
```

---

## Workflow: The OODA Spiral

Run 3-5 cycles (5-7 with a deployed URL). Each cycle has four steps.

### Cycle 1: Reconnaissance

**Observe** — survey the cloned repo:

- Languages: `package.json` → JS/TS, `requirements.txt`/`pyproject.toml` → Python, `go.mod` → Go, `Cargo.toml` → Rust, etc.
- Frameworks: Rails, Django, Express, Next.js, Spring, FastAPI, etc.
- Database: ORM config files, connection strings, migration directories.
- Deployment: Dockerfiles, `docker-compose.yml`, k8s manifests, `.github/workflows/`, `.gitlab-ci.yml`.
- Test structure: test directories, file patterns (`*.test.*`, `*_spec.*`, `tests/`).
- Size: file count, LOC estimate.

Use Glob/Read/Bash to survey efficiently.

**Orient** — map to the 25-primitive framework:

- No Dockerfiles → skip INF-01 (container security).
- No deployed URL → skip DAT-02 (encryption in transit, deployed-side), INF-03 (HTTP headers).
- No user-facing web app → reduce weight on SEC-05 (XSS).
- No external API integration → reduce weight on SEC-06 (SSRF).

**Decide** — plan tool execution order. Broad-spectrum first:

1. Gitleaks (fast, high-signal — secrets in git history)
2. Trivy (dependency CVEs, container scan)
3. Semgrep (SAST — security patterns)
4. Language-specific checks as needed

**Act** — execute the first round of tools. Commands in [`references/tool-commands.md`](references/tool-commands.md).

### Cycle 2: Triage and Depth

**Observe** — read tool outputs.

**Orient** — prioritise:
- Critical/high severity → investigate immediately
- Patterns (e.g. five injection findings in one module → focused review)
- Surprises (e.g. zero test files → CQ-02 is critical)

**Decide** — plan targeted follow-up:
- Secrets found → check if they appear in deployment configs (INF-02)
- Injection found → check input validation elsewhere (SEC-04)
- High CVE count → check if vulnerable code paths are actually reachable

**Act** — run targeted checks. Update findings.

### Cycle 3: Cross-Primitive Chaining

**Observe** — look for findings that connect across primitives.

**Orient** — "Does finding A in primitive X make primitive Y worse?"

Examples:
- Secret in git (SEC-07) + API endpoint in code (SEC-01) → can the secret authenticate the API?
- No input validation (SEC-04) + SQL queries in same module (SEC-03) → injection chain
- Debug mode enabled (INF-04) + PII in logs (DAT-03) → data exposure chain
- No tests (CQ-02) + high complexity (CQ-01) → high regression risk
- Outdated dep with known RCE (SC-01) + reachable code path → exploitable supply-chain vuln

**Decide** — document the chains. These are the most compelling findings.

**Act** — write them up with evidence.

### Cycle 4: Deployed Surface (if URL provided)

**Observe** — non-invasive checks against the deployed URL:

```bash
# Security headers
curl -sI {url} | grep -iE "strict-transport-security|content-security-policy|x-frame-options|x-content-type-options|referrer-policy"

# Common exposure (read-only probes)
for path in .env .git/config .DS_Store robots.txt sitemap.xml .well-known/security.txt; do
  curl -s -o /dev/null -w "%{http_code} ${path}\n" "{url}/${path}"
done

# TLS version (if testssl.sh available)
testssl.sh --quiet --color 0 --severity HIGH {url} > "$ASSESS_DIR/outputs/testssl.log" 2>&1
```

Stay strictly read-only. **No active scanning, no payload injection, no auth probing.**

**Orient** — compare deployed state to code findings:
- Code says TLS 1.2 — does the server actually enforce it?
- Code has CORS restrictions — does the server emit `Access-Control-Allow-Origin: *`?
- Code has CSP headers configured — does the server actually emit them?

**Decide** — focus on discrepancies between code and deployment.

**Act** — document. Distinguish code issues from deployment-config issues.

### Cycle 5: Hypothesis Formation

**Observe** — review all 25 primitives. Which haven't been assessed?

**Orient** — for primitives that cannot be fully automated (DAT-01 encryption
at rest, DAT-05 audit logging, CQ-04 process signals, CQ-05 review practices),
form hypotheses from available evidence:

- DAT-01: "Found PostgreSQL config with no `pgcrypto` extension, no encryption
  helpers in the ORM. **Hypothesis: encryption at rest is not implemented.**
  Confidence: medium. To verify: confirm cloud-provider-level disk encryption
  or column-level encryption with the team."

- CQ-05: "Git log shows 60% of commits direct to `main`, no PR template in
  the repo, average PR has 0 reviewers. **Hypothesis: peer review is
  inconsistent.** Confidence: high. To verify: confirm branch protection
  rules and review policy with the team."

**Decide** — write each hypothesis with: statement, evidence, confidence,
verification question. Save under `.security/{project}/hypotheses.md`.

**Act** — complete the primitive assessment table.

### Termination

Stop when:
- All applicable primitives have a status (PASS / ADVISORY / CONCERN / CRITICAL / HYPOTHESIS / NOT ASSESSED)
- No productive lines of inquiry remain
- Typically 3-5 cycles for code-only, 5-7 with a deployed URL

---

## Cross-Plugin Integration

Before writing the report, check for sibling-plugin artifacts:

### If `.specifications/{project}/` exists (SRD output)

- Read `NFR.md`. Compare findings to documented NFRs.
- A finding that contradicts an NFR is **specification drift** — flag in
  the report's "Drift" section with the NFR ID.
- Example: "SEC-07 finding contradicts NFR-12 (secret management via vault required)."

### If `.architecture/{project}/` exists (SEA output)

- Read `hardening-deltas/INDEX.md` if it exists.
- For each Critical/Concern finding in the assessment, check if a Hardening
  Delta already covers it.
- Report's "Recommendations" section: for findings without an existing
  delta, recommend `/sulis:harden-codebase` to convert them into deltas; for findings
  with an existing delta, note its status (proposed/accepted/implemented).

This avoids double-counting between security review and architectural hardening.

---

## Report Format

Write the report to `.security/{project}/viability-report-{TIMESTAMP}.md` where `TIMESTAMP` is an ISO 8601 UTC timestamp generated at report-write time. This prevents same-day rerun collisions (e.g., running a security assessment twice in one day after applying fixes between runs).

```bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H%M%SZ)
# Produces: 2026-05-21T143052Z
# Example file: viability-report-2026-05-21T143052Z.md
```

```markdown
# Codebase Viability Assessment: {Project Name}

**Date:** {YYYY-MM-DD}
**Repository:** {repo-url}
**Deployed URL:** {url or "Not provided"}
**Languages:** {detected}
**Frameworks:** {detected}
**Related artifacts:**
- SRD: `.specifications/{project}/` ({present|absent})
- SEA: `.architecture/{project}/` ({present|absent})

---

## Executive Summary

**Overall Viability Score: {X}/100**

{2-3 sentence narrative — what's strong, what needs attention, what's critical}

| Category | Score | Status |
|---|---|---|
| Security | {X} | {PASS / ADVISORY / CONCERN / CRITICAL} |
| Data Protection | {X} | {status} |
| Code Quality | {X} | {status} |
| Supply Chain | {X} | {status} |
| Infrastructure | {X} | {status} |

---

## Critical Findings

{Only critical-severity items. Each: primitive ID, description, evidence (file:line or tool output), recommendation, related SEA Hardening Delta if exists}

---

## Attack Chains

{Cross-primitive chains discovered in Cycle 3. Each chain explains how multiple findings combine into an exploitable path}

---

## Specification Drift (if SRD exists)

{Findings that contradict documented NFRs. Each row: finding, NFR ID, severity of mismatch}

---

## Category Detail

### Security

| ID | Primitive | Status | Findings | Key Evidence |
|---|---|---|---|---|
| SEC-01 | Broken access control | {status} | {count} | {one-line summary} |
| ... | ... | ... | ... | ... |

{Repeat per category}

---

## Hypotheses (Manual Primitives)

{One entry per HYPOTHESIS-status primitive:}

### {Primitive ID}: {Name}

**Hypothesis:** {what the agent believes from evidence}
**Evidence:** {what was found in code/config/git}
**Confidence:** {high / medium / low}
**To verify:** {question for the team}

---

## Recommendations

### Immediate (production-blocking)
{Critical and high-severity items. If SEA is installed, recommend `/sulis:harden-codebase` to convert to Hardening Deltas.}

### Near-term (before next major release)
{Medium-severity items. Group by category. Estimate effort.}

### Ongoing (process improvements)
{Low-severity items, hypothesis-confirmed process gaps.}

---

## Methodology

**OODA cycles completed:** {N}
**Tools used:** {list with versions}
**Tools unavailable:** {list — explains coverage gaps}
**Excluded paths:** {vendor, node_modules, generated code, etc.}
**Assessment duration:** {time}
**GitHub App used:** {yes / no — direct clone}
```

---

## Cleanup

After the report is written:

1. Verify the report file exists and is readable.
2. Write `SEC.yaml` metadata to `.security/{project}/SEC.yaml`.
3. Move raw tool outputs to `.security/{project}/tool-outputs/`.
4. Move hypotheses to `.security/{project}/hypotheses.md`.
5. Remove the temp directory: `rm -rf "$ASSESS_DIR"`.
6. Summarise top findings to the user in conversation.
7. If applicable, suggest `/sulis:harden-codebase` as the next step.

---

## Adapting Depth

- **Quick** ("smoke check before merge") — Cycle 1 + Cycle 2 only, on the diff being merged rather than the whole repo. Focus SEC + SC categories. ~10 minutes.
- **Full** (default) — all 5 cycles, all 25 primitives, full report.
- **Compliance-focused** ("are we ready for SOC2 audit?") — full assessment with extra weight on DAT (encryption, PII, audit logging), CQ-05 (review practices), and explicit mapping to control families in the report.

---

## Gotchas

- **Stay non-invasive on deployed surfaces.** No active vuln scanning, no
  auth probing, no payload injection without explicit user authorisation
  for active testing.
- **Don't double-count with SEA.** If a Hardening Delta already documents
  a gap, your report cross-references it instead of proposing a new finding.
- **A `NOT ASSESSED` primitive is not a failure.** Tool unavailability is
  a coverage gap; document it in Methodology so the reader can judge the
  verdict's trustworthiness.
- **Hypotheses ≠ findings.** A hypothesis is evidence-backed speculation a
  human can confirm or reject. Don't inflate hypotheses to findings.
- **Tokens are secrets.** Never log, never write to report, never persist
  beyond the skill's execution scope. The temp directory is deleted on
  cleanup; the token expires anyway.
- **Score is a heuristic.** A 75/100 with one critical is worse than a 75/100
  evenly distributed. Lead the report with Critical Findings, not the score.
- **PII patterns produce false positives.** A grep for SSN-shaped strings
  may hit test fixtures. Verify before flagging.

---

## See Also

- [`references/primitives.md`](references/primitives.md) — full 25-primitive catalogue
- [`references/tool-commands.md`](references/tool-commands.md) — Docker/binary invocations for each tool
- [`../../references/viability-framework.md`](../../references/viability-framework.md) — OODA spiral, scoring, evidence discipline
