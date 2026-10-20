---
name: snyk-scanning
description: Run Snyk scans across code, open source dependencies, containers, and IaC, then triage findings by severity. Use when the user wants to find vulnerabilities in their own project.
---

# Snyk scanning

All scans run locally via the Snyk CLI (`snyk`, v1.1298.0+ recommended) or through
the Snyk MCP server this plugin ships. Authenticate first (see `snyk-setup`).

## The four test commands

```bash
snyk test                 # Open Source: dependency vulnerabilities (SCA)
snyk code test            # Code: static analysis of first-party code (SAST)
snyk container test IMAGE # Container: base image + OS package vulns
snyk iac test             # IaC: Terraform, CloudFormation, K8s, ARM misconfigs
```

Run them from the project root. Useful variants:

```bash
snyk test --all-projects            # scan every manifest in a monorepo
snyk test --file=package-lock.json  # target one manifest
snyk test --dev                     # include devDependencies (npm/yarn)
snyk container test node:20 --file=Dockerfile  # link image to its Dockerfile
snyk iac test infra/                # scan a directory of IaC files
```

## Severity triage

```bash
snyk test --severity-threshold=high   # only report high and critical
snyk code test --severity-threshold=medium
```

Triage order: critical > high > medium > low. Within a severity band, prioritize:

1. Findings with known exploits (check `exploit maturity` in JSON output).
2. Direct dependencies (you control the version) before transitive ones.
3. Code paths that handle untrusted input (auth, parsers, deserialization).

## Machine-readable output

```bash
snyk test --json > snyk-oss.json
snyk code test --sarif-file-output=snyk-code.sarif
snyk iac test --sarif > snyk-iac.sarif
```

JSON gives `vulnerabilities[]` with `id`, `severity`, `CVSSv3`, `upgradePath`,
`isUpgradable`, `isPatchable`. SARIF loads into any SARIF viewer and most code
review tooling.

## Exit codes (script and CI logic)

- `0`: no issues found
- `1`: issues found (this is a finding, not a crash)
- `2`: failure, rerun with `-d` for debug output
- `3`: no supported projects or manifests detected

CI pattern: run `snyk test --severity-threshold=high` and fail the build on
exit code 1. Use `snyk ignore --id=SNYK-XX-YY` sparingly, with `--reason` and
`--expiry`, so ignores stay auditable in `.snyk`.

## Continuous monitoring

```bash
snyk monitor                 # snapshot deps to the Snyk UI, alerts on new vulns
snyk container monitor IMAGE
```

`monitor` does not fail builds; it records the dependency tree so Snyk can alert
you when a new vulnerability is disclosed against an already-shipped version.
Run it on the default branch after merge, not on PRs.

## Via the MCP server

The bundled MCP server (`snyk mcp -t stdio`) exposes the same scans as tools
(SCA, Code, IaC, container). Point it at an absolute project path. First run may
prompt for folder trust; set the documented disable flag for headless runs.
