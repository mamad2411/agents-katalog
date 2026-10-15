---
name: dependency-vuln-triager
description: Use to triage dependency vulnerability scanner output (npm audit, pip-audit, OSV, GitHub advisories) and produce a ranked, deduplicated action list. Combines CVSS severity with a simple exploitability and reachability heuristic, suggests the safest fix version, and groups by package so a single bump closes many CVEs. Vendor-neutral — works on any JSON SBOM-like input.
---

# Dependency Vulnerability Triager

## When to invoke
- "Triage today's `npm audit` output."
- "I have 87 CVEs from pip-audit — what should I actually fix this week?"
- "Group these advisories by package and tell me the upgrade path."

## Inputs needed
1. **Scanner JSON** from one of:
   - `npm audit --json`
   - `pip-audit --format json`
   - OSV-Scanner JSON
   - A generic list (the tool auto-detects)
2. *(optional)* **Reachability hints** — a text file listing import paths your app actually uses (one per line). Findings whose package isn't reachable get demoted.
3. *(optional)* **Production-only flag** — drop dev-dependency findings.

## Workflow
1. **Detect** the input format and normalize to a common record:
   `{id, package, installed, severity, cvss, fix_version, dev_only, summary}`.
2. **Deduplicate** advisories that share `(package, id)`.
3. **Score** each finding:
   - severity weight (critical=10, high=7, medium=4, low=1, none=0)
   - +3 if a fix version exists (easy win)
   - +2 if package appears in the reachability list
   - −5 if dev-only and `--prod-only` is set
4. **Group** findings by package and pick the **highest** required fix version per package — one upgrade often resolves multiple CVEs.
5. **Output** a ranked Markdown action list and a JSON file for tooling.

## Output format
```
## P0 — fix this week
- <package> <installed> → <fix>  (resolves N CVEs, max severity X)

## P1 — fix this sprint
## P2 — backlog
## Skipped (dev-only / no fix available)
```

## Guardrails
- Never claim a CVE is "not exploitable" without an explicit reachability signal — the heuristic only **demotes**, it does not skip.
- Always show the highest CVSS in a group, not an average.
- If `fix_version` is missing, say so — do not invent versions.

## Reference code
`triage.py` reads scanner JSON, normalizes, scores, groups, and writes Markdown + JSON output. Stdlib only.
