---
name: security-scan
description: "Sweeps a whole repository with bandit, gitleaks, trivy and checkov, then reads up to 15 files for the authorization, data-exposure and injection gaps no scanner can decide, and reports findings by severity with file:line and a fix. Use when auditing a repository, before a release, or when inheriting an unfamiliar codebase. Not for a branch or pull-request diff (use /security-review or code-review-core:review); not for lint and secret findings on changed files only (use code-review-core:review-scan)."
when_to_use: "audit this repo, security sweep, is this repo safe to ship, scan the whole codebase for vulnerabilities, pre-release security check"
argument-hint: "[path, default: the current directory]"
allowed-tools: Read, Grep, Glob, Bash(command -v *), Bash(mktemp -d), Bash(bandit *), Bash(gitleaks *), Bash(trivy *), Bash(checkov *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Security scan

Target: `$ARGUMENTS` (the current directory when empty).

This is a whole-tree audit, so pre-existing debt is the point: report everything, not only what a
recent change touched. Scanners run first because they find pattern-shaped problems with a rule id
and severity for less context than reading code; the judgement pass then covers what patterns cannot
decide.

Shell variables do not persist between Bash calls, so write the target and the report directory
literally into every command.

## Workflow

Copy this checklist and tick it off:

```
- [ ] 1. Scope the tree
- [ ] 2. Run each scanner
- [ ] 3. Judgement pass (at most 15 files)
- [ ] 4. Report
- [ ] 5. Verify
```

### 1. Scope the tree

Use Glob on the target for `**/*.{py,ts,tsx,js,jsx,go,rb,java,tf,yaml,yml}` and set aside
`node_modules`, `vendor`, `dist`, `build`, `.terraform` and `__pycache__`. Note the file count and the
main languages; the count goes in the report so that "no findings" has a denominator.

If the target does not exist, stop and report `Target not found: <path>`.

### 2. Run each scanner

Create one report directory with `mktemp -d` and reuse its literal path. Then, for each tool, check it
with `command -v <tool>` and run it only if present:

| Tool | Command | Covers |
| --- | --- | --- |
| bandit | `bandit -r <target> -f json -o <dir>/bandit.json -q` | Python injection, weak crypto, unsafe deserialization |
| gitleaks | `gitleaks git <target> --redact --no-banner --report-format json --report-path <dir>/gitleaks.json` | committed credentials, including history |
| trivy | `trivy fs --scanners vuln,secret,misconfig --format json --output <dir>/trivy.json <target>` | dependency CVEs, secrets, IaC misconfiguration |
| checkov | `checkov -d <target> -o json --compact --quiet --output-file-path <dir>` (writes `results_json.json`) | Terraform, CloudFormation, Kubernetes policy |

Record a status for each tool, from this closed set:

| Status | Meaning |
| --- | --- |
| `RAN` | The report file exists and parses. |
| `SKIPPED` | Not installed, or no files of its kind in the tree. Say which. |
| `FAILED` | Installed but produced no usable report (for example trivy could not download its database offline). Quote the first error line. |

A non-zero exit code from these tools usually means "found something", so judge success by the report
file, not the exit code. If `gitleaks git` reports that the target is not a git repository, run
`gitleaks dir <target>` with the same flags; older gitleaks releases use `gitleaks detect --source <target>`.

Read each report and triage it. For secret findings, cite `file:line`, the rule id and what to rotate,
and leave the matched value out of the report: that value is the credential, and quoting it copies the
leak into a new place.

### 3. Judgement pass (at most 15 files)

Pick files from the scanner hits and from the authentication, authorization and entry-point code
found in step 1. Read them for:

- **Authorization gaps**: a handler with no permission check; a query scoped by id but not by tenant;
  a check that catches an error and proceeds.
- **Sensitive data exposure**: personal data in logs; credentials in error messages; data crossing a
  classification boundary.
- **Injection the tools missed**: SQL or shell built through a helper that hides the concatenation.
- **Dependency risk in context**: whether code this repo runs actually reaches a CVE's vulnerable path.

The cap keeps the pass finishing; list every file you read so the reader can see what was covered.

### 4. Report

Severities are a closed set: `BLOCKER` (exploitable now, or a live credential exposed), `MAJOR` (a real
weakness that needs a deliberate fix), `MINOR` (hardening or latent risk). Use this template:

```markdown
## Security scan: <target>

<N> files in scope (<languages>) · <b> BLOCKER · <m> MAJOR · <n> MINOR

| Scanner | Status | Note |
| --- | --- | --- |
| bandit | RAN | |
| gitleaks | RAN | |
| trivy | FAILED | could not download vulnerability DB |
| checkov | SKIPPED | no IaC files |

Files read in the judgement pass: <list>

### BLOCKER
- `path/to/file.py:42` [gitleaks: aws-access-token] AWS key committed in history. Fix: rotate the key, then purge it from history.

### MAJOR
- `api/orders.py:88` [judgement] Order lookup filters by id but not tenant, so any user can read any order. Fix: add the tenant filter.

### MINOR
(none)
```

Write `(none)` under an empty severity. A skipped or failed scanner stays in the table: "no findings"
from a tool that never ran reads exactly like a pass.

### 5. Verify

Before returning, re-read the report and confirm: all four scanners have a status row; every finding
has `file:line`, a source (scanner rule id or `judgement`) and a fix; the judgement-pass file list has
at most 15 entries; and no secret finding contains the matched value.

## Without a checkout

With no shell or files (for example on the web), ask for the relevant files or existing scanner
output to be pasted. Run step 3 over what was pasted, mark every scanner `SKIPPED (no shell)`, and use
the same report template.
