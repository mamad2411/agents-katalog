<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-bogdanticu88
description: CTF writeups and security challenges by bogdanticu88.
---

# Writeups by bogdanticu88

Source repository: `/repos/bogdanticu88`

## Repository Index

- ReqReaper/CHANGELOG.md
- ReqReaper/README.md
- ReqReaper/ROADMAP.md

## Writeup Content


### File: ReqReaper/README.md

# ReqReaper

ReqReaper is a modular orchestration framework designed for automated API security
testing. It integrates industry-standard security tools into a unified workflow,
providing standardized data models, normalized CSV exports, and comprehensive
audit trails for authorized red-team engagements.



## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Perform a safe preflight check
python3 reqreaper.py --config config/example.yaml --dry-run

# 3. Execute the full assessment
python3 reqreaper.py --config config/example.yaml

# 4. Run a simulated demo (no tools required)
python3 reqreaper.py --demo
```

## CLI Flags

| Flag | Description |
|------|-------------|
| `--config` | Path to YAML configuration file |
| `--dry-run` | Validate config and check tool availability without executing |
| `--demo` | Run a simulated execution for preview purposes |
| `--full` | Enable all non-destructive modules in one pass |
| `--safe` | Restrict `--full` to passive modules only |
| `--enable-fuzz` | Enable fuzzing modules (`ffuf`, `kiterunner`) |
| `--enable-sqli` | Enable SQL injection testing (`sqlmap`) |
| `--enable-load` | Enable load testing (`k6`) |
| `--quiet` | Suppress console output |
| `--no-color` | Disable color output |
| `--version` | Print version and exit |

## Configuration

All scan behaviour is controlled through a YAML config file. See `config/example.yaml` for a full reference.

Key fields:

```yaml
targets:
  - https://api.example.com

allowed_hosts:
  - api.example.com        # Allowlist enforced — targets not listed here are rejected

auth:
  header_name: "Authorization"
  header_value: "Bearer <token>"   # Passed to httpx, nuclei, ffuf, and OpenAPI fetches

openapi_url: "https://api.example.com/openapi.json"   # JSON or YAML specs supported

timeout: 30
```

## Modules

### Implemented

| Category | Tools |
|----------|-------|
| Reconnaissance | `httpx`, `nmap` |
| Vulnerability Scanning | `nuclei`, `testssl.sh`, `zap-cli` |
| JWT Analysis | Native Python — no binary required |
| Fuzzing & Enumeration | `ffuf`, `kiterunner` |
| Injection | `sqlmap` |
| Load Testing | `k6` |
| API Parsing | OpenAPI (JSON + YAML) |

### JWT Analysis

The JWT module runs as part of the vulnerability group without requiring any
external binary. It collects tokens from configured auth headers, HTTP response
headers, and response body fields, then checks for:

- Algorithm `none` (critical — token is unsigned)
- Weak symmetric algorithms (`HS256`, `HS1`)
- Missing `exp` claim (token never expires)
- Missing `aud` / `iss` claims

Findings are written to the `findings` table and exported to `jwt_findings.csv`.

### Planned

For upcoming integrations and features, see [ROADMAP.md](ROADMAP.md).

## What it generates

Every execution produces a timestamped artifact directory:

```
artifacts/run_<timestamp>/
├── raw/                  # Unmodified output from each tool
├── normalized/           # Standardized CSV exports per table
│   ├── endpoints.csv
│   ├── findings.csv
│   ├── jwt_findings.csv
│   ├── tls_findings.csv
│   └── ...
├── report/
│   └── report.html       # High-level HTML summary
└── reqreaper.db          # Full SQLite audit database
```

## Example output

### Startup Banner
```text
██████╗ ███████╗ ██████╗ ██████╗ ███████╗ █████╗ ██████╗ ███████╗██████╗
██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝█████╗  ██║   ██║██████╔╝█████╗  ███████║██████╔╝█████╗  ██████╔╝
██╔══██╗██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║  ██║███████╗╚██████╔╝██║  ██║███████╗██║  ██║██║     ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

                        v0.2.0 | by Bogdan Ticu
```

### Console Execution
```text
[*] Initialization complete. Run ID: 550e8400-e29b-41d4-a716-446655440000
[*] Target Scope: 2 hosts
[*] Running OpenAPI Analysis...
[*] Executing Discovery:HTTPX...
[+] Discovery:HTTPX completed
[*] Executing Discovery:Nmap...
[+] Discovery:Nmap completed
[*] Executing Vulnerability:Nuclei...
[+] Vulnerability:Nuclei completed
[*] Executing Vulnerability:TLS...
[+] Vulnerability:TLS completed
[*] Executing Vulnerability:JWT...
[+] Vulnerability:JWT completed

Execution Summary
Artifacts Directory: /home/user/ReqReaper/artifacts/run_20260221_120000

Findings by Severity
Severity  Count
CRITICAL      1
HIGH          3
MEDIUM        5
LOW           9
```

## Legal

**AUTHORIZED USE ONLY.** This tool is intended for use by security professionals
during authorized security assessments. Unauthorized testing against systems
without explicit permission is illegal. The author assumes no liability for
misuse or any damages caused by this software.



### File: ReqReaper/CHANGELOG.md

# Changelog

All notable changes to ReqReaper will be documented in this file.

## [0.2.0] - 2026-02-21

### Fixed
- **XSS vulnerability in HTML report**: All database-sourced values are now escaped with
  `html.escape()` before being written into the report template.
- **SQLMap module always skipping**: Removed an internal `enable_sqli` config gate that was
  never set and caused the module to return early on every execution. Module gating is handled
  exclusively by the orchestrator via CLI flags.
- **Silent error swallowing in `run_command()`**: Timeout, missing binary (`FileNotFoundError`),
  and unexpected exceptions are now logged at the appropriate level (`warning`, `error`) instead
  of being silently discarded.
- **TLS module not parsing findings**: `testssl.sh` JSON output is now fully parsed. Findings
  are extracted with severity mapping (`CRITICAL` → `critical`, `HIGH` → `high`, etc.) and
  written to the database. Informational `OK` results are filtered out.
- **Auth headers not passed to tools**: `httpx`, `nuclei`, and `ffuf` now append the configured
  `auth.header_name` / `auth.header_value` as a `-H` flag when building tool commands.
- **No timeout on OpenAPI HTTP requests**: `requests.get()` in the OpenAPI module now uses the
  configured `timeout` value, preventing indefinite hangs.
- **OpenAPI module only supported JSON specs**: Both URL-fetched and file-based specs now try
  JSON first and fall back to YAML, covering the majority of real-world API specs.

### Added
- **JWT module**: Native Python module for JWT security analysis. Collects tokens from configured
  auth headers, response headers, and response body. Flags weak algorithms (`none`, `HS256`),
  missing `exp`, `aud`, and `iss` claims. Findings are written to the `findings` table and a
  local `jwt_findings.csv`. Registered under the `Vulnerability` module group.
- **Auth header passthrough in OpenAPI module**: OpenAPI spec fetches now include the configured
  auth header for specs served behind authentication.

### Changed
- **Refactored module selection logic**: Extracted a `select_modules()` function to replace
  duplicated conditional blocks in both the dry-run and execution paths. Ensures consistent
  behaviour and a single place to update when adding new modules.
- **requirements.txt**: Removed unused `sqlite-utils` dependency. Added minimum version pins
  for all dependencies (`rich>=13.0.0`, `pyyaml>=6.0.0`, `requests>=2.28.0`,
  `jsonschema>=4.0.0`, `pytest>=7.0.0`).

## [0.1.0] - 2026-02-20

### Added
- Initial release of the ReqReaper API Security Framework.
- Modular plugin system for tool orchestration and data normalization.
- Integration with standard security tools:
  - Discovery: `httpx`, `nmap`
  - Vulnerability: `nuclei`, `testssl.sh`, `zap-cli`
  - Fuzzing & Enumeration: `ffuf`, `kiterunner`
  - Injection: `sqlmap`
  - Load Testing: `k6`
  - API Specific: `OpenAPI` parsing
- Centralized DataManager with SQLite backend and automated CSV exports.
- Robust configuration validation with JSON schema and allowlist enforcement.
- Safe preflight mode (`--dry-run`) for validation and tool discovery.
- Professional console UI with rich progress indicators and execution
  summaries.
- Basic HTML report generation for high-level findings.
- Unit test suite for parsers and data normalization logic.
- Comprehensive documentation: README.md, ROADMAP.md, and CHANGELOG.md.



### File: ReqReaper/ROADMAP.md

# ReqReaper Roadmap

## Completed

### v0.1.0
- **Core Orchestration Engine:** CLI interface, configuration management, and
  modular plugin system.
- **Data Normalization Layer:** Standardized SQLite backend with automated
  CSV exports.
- **Allowlist & Preflight:** Robust host enforcement and tool availability
  validation.
- **Reporting:** Basic HTML report generation with severity summaries.
- **Testing:** Unit test suite for parsers and data management.
- **Functional Modules:**
  - `httpx`: Discovery and tech fingerprinting.
  - `nmap`: Port scanning and service detection.
  - `nuclei`: Template-based vulnerability scanning.
  - `testssl.sh`: TLS/SSL configuration auditing.
  - `zap-cli`: OWASP ZAP baseline security scans.
  - `ffuf`: Directory and endpoint fuzzing.
  - `kiterunner`: API endpoint discovery.
  - `sqlmap`: Automated SQL injection testing.
  - `k6`: Performance and stress testing.
  - `OpenAPI`: Definition parsing and extraction.

### v0.2.0
- **JWT Analysis Module:** Native Python implementation. Collects tokens from
  auth headers, response headers, and response body. Flags weak algorithms
  (`none`, `HS256`), missing `exp`/`aud`/`iss` claims. No external binary required.
- **TLS Finding Extraction:** Full parsing of `testssl.sh` JSON output with
  severity mapping. Actual findings are now stored in the database rather than
  a placeholder path reference.
- **Auth Header Passthrough:** Configured auth headers are now forwarded to
  `httpx`, `nuclei`, `ffuf`, and OpenAPI spec fetches.
- **OpenAPI YAML Support:** Spec fetches and file inputs now support both JSON
  and YAML formats.
- **Error Visibility:** `run_command()` now logs timeouts, missing binaries, and
  unexpected errors rather than silently returning `None`.
- **XSS Fix in HTML Report:** All database-sourced values are HTML-escaped before
  being written into the report template.
- **Code Quality:** Extracted `select_modules()` to eliminate duplicated module
  selection logic across dry-run and execution paths.

## In Progress

- **Database Deep Integration:** Full per-request/response storage for all
  modules for auditing.
- **Artifact Consolidation:** Improving evidence linking in HTML reports and
  cross-referencing findings across modules.

## Planned

- **Extended Discovery:** Integration of `katana`, `gau`, and `waybackurls`.
- **Advanced Fuzzing:** Support for `wfuzz` and `arjun` for parameter discovery.
- **Load Testing Expansion:** Integration of `vegeta`, `wrk`, and `hey`.
- **Dynamic HTML Reports:** Interactive reporting dashboard with severity
  filtering and search.
- **Nmap Result Parsing:** Extract open ports and service banners from nmap XML
  output into the database.

## Future Ideas

- **GraphQL Interrogation:** Specialized module for GraphQL schema introspection
  and testing.
- **Mass Assignment Detection:** Automated testing for object injection and mass
  assignment vulnerabilities.
- **IDOR Testing:** Semi-automated module for identifying potential IDOR
  endpoints through multi-user session analysis.
- **Authentication Proxy:** Integration with Burp Suite or ZAP proxy for manual
  and automated traffic interception.

