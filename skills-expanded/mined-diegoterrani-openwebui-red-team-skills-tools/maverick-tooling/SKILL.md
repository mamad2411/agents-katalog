---
name: maverick-tooling
description: "MAVERICK Tooling Agent — Expert CLI usage for security scanning tools: nmap, nuclei, sqlmap, ffuf, katana, naabu, subfinder, semgrep, ast-grep, gitleaks, trufflehog, trivy, plus Kalli and Maverick project tools. Use when executing automated security scans with specific tool syntax and bounded execution controls."
---

# MAVERICK Tooling Agent

You are the **Tooling Agent** in the MAVERICK pentest pipeline. Your mission: execute security scanning tools with correct syntax, bounded execution parameters, and structured output for downstream analysis.

## Objective

Run automated security tools efficiently and correctly:
- Use proper CLI syntax and flags
- Bound execution (timeouts, rate limits, retries)
- Produce structured, reusable output
- Recover from failures gracefully
- Keep traffic reasonable and scope explicit

## Tool Sources

Tools come from three sources. **Always check availability before invoking** — if a tool is not installed, fall back to the next source or skip gracefully.

### 1. System Tools (PATH)
Standard security tools installed system-wide. Check with `which <tool>` before use.

| Tool | Purpose |
|------|---------|
| nmap | Port scanning, service detection |
| nuclei | Template-based vulnerability scanning |
| sqlmap | SQL injection detection and exploitation |
| ffuf | Web fuzzing (directories, params, words) |
| katana | Web crawling and endpoint discovery |
| naabu | Fast port scanning |
| subfinder | Subdomain enumeration |
| semgrep | Static analysis (SAST) |
| sg (ast-grep) | AST structural pattern matching |
| gitleaks | Secret detection in git history |
| trufflehog | Secret and credential detection |
| trivy | Container/dependency vulnerability scanning |
| httpx | HTTP probing and URL validation |
| amass | DNS enumeration |
| whatweb | Web technology fingerprinting |
| wafw00f | WAF detection |

### 2. Kalli Project Tools
Custom tools from the Kalli project. Check `/home/diego/kalli/` (or `which kalli`) for available executables.

**Discovery protocol:**
```bash
# Find Kalli tools
ls /home/diego/kalli/bin/ 2>/dev/null || ls /home/diego/kalli/tools/ 2>/dev/null
# Or check if installed globally
which kalli 2>/dev/null
# Check for any kalli-* executables
ls /usr/local/bin/kalli* 2>/dev/null
```

**Usage:** When a Kalli tool is available, prefer it over generic tools for the same task. Read its `--help` or README before first use to get exact syntax. Document the exact command used in findings.

### 3. Maverick Project Tools
Custom tools from the Maverick project at `/home/diego/Iron-maverick-agent-pentest/`.

**Available tools:**

| Tool | Path | Purpose |
|------|------|---------|
| xurlfind3r | `tools/xurlfind3r/bin/xurlfind3r` | Passive URL discovery from 15+ online sources (Wayback, AlienVault, crt.sh, Shodan, DNSDumpster, etc.) |
| Discovery Runner | `console/server/discovery_runner.py` | Fast URL discovery: xurlfind3r + live HTML/JS extraction (no LLM needed) |
| Chrome Burp | `scripts/chrome-burp.sh` | Launch Chrome routed through Burp proxy (127.0.0.1:8083) |
| Kali Proxy | `scripts/kali-proxy.sh` | Toggle system HTTP/HTTPS proxy to Burp (127.0.0.1:8083) |
| Strix Engine | `engine/strix/` | Multi-agent pentest engine with terminal, browser, proxy, python, web_search, file_edit, notes, todo, reporting, thinking, load_skill, finish tools |
| Strix Skill Library | `engine/strix/skills/` | 18 vulnerability playbooks, 9 tooling playbooks, 3 scan modes, 3 frameworks, 2 technologies, 1 cloud |
| Console Server | `console/server/` | FastAPI IRON GUARD Red Team Agent (discovery, LLM profiles, execution reports) |

**xurlfind3r usage:**
```bash
# Basic passive URL discovery
/home/diego/Iron-maverick-agent-pentest/tools/xurlfind3r/bin/xurlfind3r -d <domain> -o urls.txt

# Include subdomains
/home/diego/Iron-maverick-agent-pentest/tools/xurlfind3r/bin/xurlfind3r -d <domain> --include-subdomains -o urls.txt

# Specific sources
/home/diego/Iron-maverick-agent-pentest/tools/xurlfind3r/bin/xurlfind3r -d <domain> --sources-to-use wayback,alienvault,crt.sh -o urls.txt

# JSONL output
/home/diego/Iron-maverick-agent-pentest/tools/xurlfind3r/bin/xurlfind3r -d <domain> --jsonl -o urls.jsonl
```

**Discovery Runner usage (via Python):**
```python
# Fast discovery without LLM — combines xurlfind3r + live HTML/JS extraction
cd /home/diego/Iron-maverick-agent-pentest/console/server
python -c "from discovery_runner import run_discovery; run_discovery('<target>', output_path='discovery_urls.json')"
```

**Strix Engine tools (invokable via the engine):**
- `terminal` — Execute shell commands
- `browser` — Playwright-based browser automation (navigate, click, type, screenshot, network)
- `proxy` — Burp proxy integration (intercept, modify, replay requests)
- `python` — Execute Python code
- `web_search` — Search the web
- `file_edit` — Read/write/edit files
- `notes` / `todo` — Persistent notes and task tracking
- `reporting` — Generate structured reports
- `thinking` — Extended reasoning
- `load_skill` — Load a skill by name (e.g., `load_skill("sql_injection")`)

**Strix skill library (load via `load_skill`):**
- Vulnerabilities: sql_injection, xss, rce, ssrf, idor, auth_bypass, cors, csrf, deserialization, race_condition, file_upload, http_smuggling, jwt, oauth, sqli_blind, sqli_union, path_traversal, xml_injection
- Tooling: nmap, nuclei, sqlmap, ffuf, katana, naabu, subfinder, semgrep, httpx
- Scan modes: quick, standard, deep
- Frameworks: fastapi, nestjs, nextjs
- Technologies: firebase_firestore, supabase
- Cloud: kubernetes

**Usage:** Maverick tools are the primary execution engine. When a Maverick tool exists for a task, prefer it over manual tool invocations.

### Tool Resolution Order

For any given task, resolve tools in this priority:
1. **Maverick project tool** (if available and applicable)
2. **Kalli project tool** (if available and applicable)
3. **System tool** (nmap, nuclei, sqlmap, etc.)
4. **Manual HTTP/CLI** (curl, python one-liners) as last resort

Always log which tool source was used for each action.

## Nmap

### Syntax
`nmap [Scan Type(s)] [Options] {target specification}`

### Agent-Safe Baseline
```bash
nmap -n -Pn --open --top-ports 100 -T4 --max-retries 1 --host-timeout 90s -oA nmap_quick <host>
```

### Common Patterns
```bash
# Fast first pass (discovery)
nmap -n -Pn --top-ports 100 --open -T4 --max-retries 1 --host-timeout 90s <host>

# Small important-port pass
nmap -n -Pn -p 22,80,443,8080,8443 --open -T4 --max-retries 1 --host-timeout 90s <host>

# Service/script enrichment (after discovery)
nmap -n -Pn -sV -sC -p <comma_ports> --script-timeout 30s --host-timeout 3m -oA nmap_services <host>

# No-root fallback (TCP connect)
nmap -n -Pn -sT --top-ports 100 --open --host-timeout 90s <host>
```

### Key Flags
- `-n` skip DNS resolution
- `-Pn` skip host discovery (ICMP filtered)
- `-sS` SYN scan (root) / `-sT` TCP connect (no root)
- `-sV` detect service versions
- `-sC` run default NSE scripts
- `-p <ports>` explicit ports (`-p-` for all)
- `--top-ports <n>` quick common-port sweep
- `--open` show only hosts with open ports
- `-T<0-5>` timing template
- `--max-retries <n>` cap retransmissions
- `--host-timeout <time>` give up on slow hosts
- `--script-timeout <time>` bound NSE script runtime
- `-oA <prefix>` output normal/XML/grepable

### Rules
- Always set target scope explicitly
- Prefer two-pass: discovery, then enrichment
- Always set `--host-timeout`; add `--script-timeout` for NSE
- Keep discovery tight: explicit ports or small `--top-ports`
- Avoid exhaustive sweeps (`-p-`, wide ranges) unless required
- Use `-n` by default in automation
- Use `-oA` for reusable artifacts

### Failure Recovery
- Host down unexpectedly → rerun with `-Pn`
- Scan stalls → tighten scope, lower retries
- Scripts too long → add `--script-timeout`

## Nuclei

### Syntax
`nuclei [flags]`

### Agent-Safe Baseline
```bash
nuclei -l targets.txt -as -s critical,high -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 -silent -j -o nuclei.jsonl
```

### Common Patterns
```bash
# Focused severity scan
nuclei -u https://target.tld -s critical,high -silent -o nuclei_high.txt

# List-driven controlled scan
nuclei -l targets.txt -as -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 -j -o nuclei.jsonl

# Tag-driven run
nuclei -l targets.txt -tags cve,misconfig -s critical,high,medium -silent

# Explicit templates (use FULL PATH to template directories)
nuclei -l targets.txt -t /home/diego/.local/nuclei-templates/http/cves/ -rl 30 -c 10 -bs 10 -j -o nuclei_templates.jsonl
nuclei -l targets.txt -t /home/diego/.local/nuclei-templates/http/misconfiguration/ -rl 30 -c 10 -bs 10 -j -o nuclei_misconfig.jsonl
nuclei -l targets.txt -t /home/diego/.local/nuclei-templates/http/exposures/ -rl 30 -c 10 -bs 10 -j -o nuclei_exposures.jsonl

# Deterministic non-OAST run
nuclei -l targets.txt -as -s critical,high -ni -stats -rl 30 -c 10 -bs 10 -timeout 10 -retries 1 -j -o nuclei_no_oast.jsonl
```

### Key Flags
- `-u, -target <url>` single target
- `-l, -list <file>` targets file
- `-im, -input-mode <mode>` list/burp/jsonl/yaml/openapi/swagger
- `-t, -templates <path>` explicit template path(s)
- `-tags <tags>` run by tag
- `-s, -severity <sev>` severity filter
- `-as, -automatic-scan` tech-mapped automatic scan
- `-ni, -no-interactsh` disable OAST requests
- `-rl, -rate-limit <n>` global request rate cap
- `-c, -concurrency <n>` template concurrency
- `-bs, -bulk-size <n>` hosts in parallel per template
- `-timeout <seconds>` request timeout
- `-retries <n>` retries
- `-stats` periodic stats output
- `-silent` findings-only output
- `-j, -jsonl` JSONL output
- `-o <file>` output file

### Valid Template Directories (for `-t` flag)
Templates are at `/home/diego/.local/nuclei-templates/`. Use FULL paths:
| Directory | Content |
|-----------|---------|
| `/home/diego/.local/nuclei-templates/http/cves/` | Known CVEs |
| `/home/diego/.local/nuclei-templates/http/misconfiguration/` | Misconfigurations |
| `/home/diego/.local/nuclei-templates/http/exposures/` | Data/panel exposures |
| `/home/diego/.local/nuclei-templates/http/vulnerabilities/` | Vulnerabilities |
| `/home/diego/.local/nuclei-templates/http/default-logins/` | Default credentials |
| `/home/diego/.local/nuclei-templates/http/exposed-panels/` | Exposed admin panels |
| `/home/diego/.local/nuclei-templates/http/technologies/` | Tech detection |
| `/home/diego/.local/nuclei-templates/http/miscellaneous/` | Misc checks |
| `/home/diego/.local/nuclei-templates/http/takeovers/` | Subdomain takeovers |
| `/home/diego/.local/nuclei-templates/http/dast/` | DAST/fuzzing templates |
| `/home/diego/.local/nuclei-templates/dns/` | DNS templates |
| `/home/diego/.local/nuclei-templates/network/` | Network templates |
| `/home/diego/.local/nuclei-templates/cloud/` | Cloud misconfigs |
| `/home/diego/.local/nuclei-templates/javascript/` | JS-based checks |

### Valid Tags (for `-tags` flag)
Common tags: `cve`, `misconfig`, `exposure`, `vulnerability`, `default-login`, `exposed-panel`, `technology`, `takeover`, `dast`, `honeypot`, `osint`, `iot`

### Rules
- Provide template selection (`-as`, `-t`, or `-tags`); avoid unscoped broad runs
- **Use FULL paths for `-t`** — relative paths like `http/cves/` will FAIL
- **Use singular tag names** — `misconfiguration` not `misconfigurations`, `cves` not `cve`
- Keep `-rl`, `-c`, `-bs` explicit for predictable resource use
- Use `-ni` when OAST traffic is not expected/allowed
- Use structured output (`-j -o <file>`) for automation
- Start with severity/tags/templates filters
- Keep retries conservative (`-retries 1`)

### Failure Recovery
- "no such path found" → you used a wrong/relative path. Use full path: `/home/diego/.local/nuclei-templates/http/<category>/`
- "no templates provided" → you didn't specify `-t`, `-tags`, or `-as`. Add one of these.
- Performance degrades → lower `-c/-bs` before `-rl`
- Empty findings → verify template selection and target reachability
- Duration grows → reduce target set, stricter filters

## SQLMap

### Syntax
`sqlmap [options] -u <url> | -r <raw> | -d <db>`

### Agent-Safe Baseline
```bash
sqlmap -u "https://target.tld/page?id=1" --batch --level=2 --risk=2 --random-agent --output-dir=./sqlmap --flush-session
```

### Common Patterns
```bash
# Basic injection check
sqlmap -u "https://target.tld/page?id=1" --batch --random-agent

# Aggressive with tamper
sqlmap -u "https://target.tld/page?id=1" --batch --level=3 --risk=3 --random-agent --tamper=space2comment,randomcase

# Specific injection type
sqlmap -u "https://target.tld/page?id=1" --batch --technique=BEUSTQ --random-agent

# Data extraction
sqlmap -u "https://target.tld/page?id=1" --batch --dbs --random-agent
sqlmap -u "https://target.tld/page?id=1" --batch -D <db> --tables --random-agent
sqlmap -u "https://target.tld/page?id=1" --batch -D <db> -T <table> --dump --random-agent

# With cookies/headers
sqlmap -u "https://target.tld/page?id=1" --cookie="session=abc" --header="X-Custom: val" --batch

# POST data
sqlmap -u "https://target.tld/login" --data="user=admin&pass=test" --batch --random-agent
```

### Key Flags
- `-u, --url` target URL
- `-r, --raw` raw HTTP request
- `-d, --dbs` database connection string
- `--batch` never ask for user input
- `--level=<1-5>` tests level (higher = more tests)
- `--risk=<1-3>` risk level (higher = more aggressive)
- `--random-agent` random User-Agent
- `--technique=<BEUSTQ>` specific techniques
- `--tamper=<list>` tamper scripts
- `--dbs` list databases
- `-D <db>` target database
- `--tables` list tables
- `-T <table>` target table
- `--dump` dump data
- `--cookie` HTTP cookie
- `--header` custom HTTP header
- `--data` POST data
- `--output-dir` output directory
- `--flush-session` flush session
- `--proxy` use proxy
- `--time-sec` time-based delay
- `--threads` concurrent threads

### Rules
- Always use `--batch` for automation
- Start with `--level=2 --risk=2`; escalate if needed
- Use `--random-agent` to avoid fingerprinting
- Keep traffic reasonable (default threads)
- Use `--output-dir` for reusable artifacts
- Verify injection manually before full extraction
- Use `--flush-session` when changing parameters

### Failure Recovery
- WAF blocking → add `--tamper`, increase `--level`
- False positives → verify with manual requests
- Slow execution → reduce `--level` or add `--threads`

## FFUF

### Syntax
`ffuf [options]`

### Common Patterns
```bash
# Directory brute-force
ffuf -u <url>/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -mc 200,301,302,403,500 -o ffuf_dirs.json -of json

# Parameter discovery
ffuf -u <url> -H "X-Custom: FUZZ" -w /usr/share/seclists/Discovery/Web-Content/param-discovery.txt -mc 200,301,302,403,500

# POST fuzzing
ffuf -u <url> -X POST -d "user=admin&pass=FUZZ" -w /usr/share/seclists/Passwords/Leaked-Databases/rockyou-75.txt -mc 200,302

# Range fuzzing
ffuf -u <url> -g id=FUZZ -rf "not found" -r 1-1000

# File extension fuzzing
ffuf -u <url>/FUZZ.php -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403,500

# With authentication
ffuf -u <url>/FUZZ -w wordlist.txt -H "Authorization: Bearer TOKEN" -mc 200,301,302,403,500
```

### Key Flags
- `-u, -url` target URL (use `FUZZ` placeholder)
- `-w, -wordlist` wordlist file
- `-X, -method` HTTP method
- `-d, -data` POST data
- `-H, -header` custom header
- `-g, -g` fuzz position in URL
- `-mc, -match-code` match status codes
- `-fc, -filter-code` filter status codes
- `-ms, -match-size` match response size
- `-fs, -filter-size` filter response size
- `-rf, -filter-regex` filter by regex
- `-o, -output` output file
- `-of, -ofmt` output format (json, csv, ecsv, jsonl)
- `-t, -threads` concurrent threads
- `-r, -range` numeric range (for FUZZ)
- `-ext` file extensions

### Rules
- Always specify match/filter criteria (`-mc`, `-fc`, `-ms`, `-fs`)
- Use JSON output for automation
- Keep threads reasonable (default 40)
- Use appropriate wordlists for context
- Filter out noise (404, 500 unless intentional)

## Katana

### Syntax
`katana [flags]`

### Common Patterns
```bash
# Basic crawl
katana -u <url> -jc -kf -d 3 -silent

# With JavaScript parsing
katana -u <url> -jc -kf -d 3 -js -silent -o crawl_js.txt

# Aggressive crawl (deeper, more params)
katana -u <url> -jc -kf -d 5 -js -aff -silent -o crawl_deep.txt

# With authentication
katana -u <url> -jc -kf -d 3 -H "Authorization: Bearer TOKEN" -silent

# API discovery
katana -u <url>/api/ -jc -kf -d 3 -silent -o api_crawl.txt
```

### Key Flags
- `-u, -url` target URL
- `-jc, -js` include JavaScript files
- `-kf, -kf` keep fragments
- `-d, -depth` crawl depth
- `-js, -js` parse JavaScript for endpoints
- `-aff, -aff` include all forms
- `-silent` findings-only output
- `-o, -o` output file
- `-H, -header` custom header
- `-c, -cookie` cookie string
- `-t, -threads` concurrent threads
- `-timeout` request timeout
- `-exclude` exclude patterns
- `-include` include patterns

### Rules
- Use `-silent` for automation
- Set appropriate depth (3 for standard, 5 for deep)
- Use `-js` for SPA/JS-heavy applications
- Output to file for reusable artifacts
- Keep threads reasonable

## Naabu

### Syntax
`naabu [flags]`

### Common Patterns
```bash
# Top ports scan
naabu -host <host> -top-ports 1000 -silent -o ports.txt

# Port range scan
naabu -host <host> -p 80-10000 -silent -o ports_range.txt

# Specific ports
naabu -host <host> -p 22,80,443,8080,8443,3306,5432,6379 -silent

# All ports (use sparingly)
naabu -host <host> -p- -silent -o all_ports.txt
```

### Key Flags
- `-host` target host(s)
- `-p, -port` port(s) or range
- `-top-ports` top N ports
- `-silent` findings-only output
- `-o, -o` output file
- `-t, -threads` concurrent threads
- `-rate-limit` rate limit
- `-timeout` connection timeout
- `-exclude` exclude ports
- `-c, -c` concurrent connections

### Rules
- Prefer `naabu` for broad port discovery
- Use `-silent` for automation
- Output to file for reusable artifacts
- Keep rate limit reasonable

## Subfinder

### Syntax
`subfinder -d <domain> [flags]`

### Common Patterns
```bash
# Basic subdomain enumeration
subfinder -d <domain> -all -silent -o subdomains.txt

# With specific sources
subfinder -d <domain> -sources crtsh,github,wayback -silent -o subdomains.txt

# Aggressive (all sources, no dedup)
subfinder -d <domain> -all -no-dedupe -silent -o subdomains_all.txt
```

### Key Flags
- `-d, -domain` target domain
- `-all` use all sources
- `-sources` specific sources
- `-silent` findings-only output
- `-o, -o` output file
- `-no-dedupe` no deduplication
- `-timeout` request timeout
- `-t, -threads` concurrent threads

### Rules
- Use `-all` for comprehensive enumeration
- Cross-reference with other sources (crt.sh, Shodan, DNS)
- Output to file for reusable artifacts
- Check for wildcard DNS before brute-forcing

## Semgrep

### Syntax
`semgrep [options] <target>`

### Common Patterns
```bash
# Quick security scan
semgrep --config auto --json --output semgrep.json <repo>

# Specific rule sets
semgrep --config p/security-audit <repo>
semgrep --config p/python-attack-surface <repo>
semgrep --config p/insecure-defaults <repo>

# Custom rules
semgrep --config rules/ <repo>

# With error exit code
semgrep --config auto --json --output semgrep.json --error <repo>
```

### Key Flags
- `--config` rule set or file
- `--json` JSON output
- `--output` output file
- `--error` exit with error code on findings
- `--include` include file patterns
- `--exclude` exclude file patterns
- `--lang` language filter
- `--severity` severity filter
- `--max-target-bytes` max file size
- `--timeout` per-file timeout

### Rules
- Use `--json` for automation
- Use `--error` to fail on findings
- Filter by language for focused scans
- Exclude vendor/node_modules directories

## ast-grep (sg)

### Syntax
`sg run -p <pattern> [options]`

### Common Patterns
```bash
# Find function definitions
sg run -p 'def $NAME($$$)' -l python <repo>

# Find HTTP routes
sg run -p '@app.route($$$)' -l python <repo>

# Find SQL queries
sg run -p 'execute($$$)' -l python <repo>

# Find file operations
sg run -p 'open($$$)' -l python <repo>

# Find command executions
sg run -p 'subprocess.$METHOD($$$)' -l python <repo>

# Find deserialization
sg run -p 'pickle.loads($$$)' -l python <repo>
sg run -p 'unserialize($$$)' -l php <repo>
```

### Key Flags
- `-p, -pattern` pattern to match
- `-l, -lang` language filter
- `-r, -replace` replace pattern
- `-U, -update` update files
- `-j, -json` JSON output
- `-q, -quiet` quiet mode
- `-v, -verbose` verbose output
- `--no-ignore` don't respect .gitignore
- `--include` include file patterns
- `--exclude` exclude file patterns

### Rules
- Use for structural pattern matching
- Combine with semgrep for comprehensive coverage
- Use JSON output for automation
- Scope to relevant paths first

## gitleaks

### Syntax
`gitleaks detect [flags]`

### Common Patterns
```bash
# Working tree scan
gitleaks detect --no-git -v --report-format json --report gitleaks.json <repo>

# Git history scan
gitleaks detect -v --report-format json --report gitleaks_history.json <repo>

# With custom config
gitleaks detect -c gitleaks.toml -v --report-format json <repo>
```

### Key Flags
- `--no-git` scan working tree (not git history)
- `-v, -verbose` verbose output
- `--report-format` report format (json, sarif, etc.)
- `--report` report file
- `-c, -config` config file
- `--exclude` exclude files
- `--include` include files
- `--log-opts` git log options
- `--pre-commit` pre-commit mode

### Rules
- Scan both working tree and git history
- Use JSON output for automation
- Cross-reference with trufflehog for comprehensive coverage
- Check for false positives (test data, placeholders)

## trufflehog

### Syntax
`trufflehog [command] [flags]`

### Common Patterns
```bash
# Git repository scan
trufflehog git file:///<repo> --fail --json > trufflehog.json

# Working directory scan
trufflehog filesystem <repo> --fail --json > trufflehog_fs.json

# With custom rules
trufflehog git file:///<repo> --rules custom.yaml --json
```

### Key Flags
- `git` scan git repository
- `filesystem` scan filesystem
- `--fail` exit with error on findings
- `--json` JSON output
- `--rules` custom rules file
- `--exclude-paths` exclude paths
- `--include-paths` include paths
- `--no-update` don't check for updates
- `--concurrency` concurrent scans

### Rules
- Scan both git history and working tree
- Use JSON output for automation
- Cross-reference with gitleaks
- Check for false positives (test data, placeholders)

## trivy

### Syntax
`trivy [command] [flags]`

### Common Patterns
```bash
# Full filesystem scan
trivy fs --scanners vuln,secret,misconfig <repo>

# Vulnerabilities only
trivy fs --scanners vuln --severity CRITICAL,HIGH <repo>

# Misconfigurations only
trivy fs --scanners misconfig <repo>

# Secrets only
trivy fs --scanners secret <repo>

# With JSON output
trivy fs --scanners vuln,secret,misconfig --format json <repo> > trivy.json
```

### Key Flags
- `fs` filesystem scan
- `--scanners` scanner types (vuln, secret, misconfig, license)
- `--severity` severity filter
- `--format` output format (table, json, sarif)
- `--output` output file
- `--exclude-files` exclude files
- `--include-files` include files
- `--timeout` scan timeout
- `--no-progress` no progress bar

### Rules
- Scan for vuln, secret, and misconfig
- Use JSON output for automation
- Filter by severity for focused scans
- Check dependency versions against CVEs

## General Rules

1. **Scope explicitly** — Always specify targets, don't scan everything
2. **Bound execution** — Set timeouts, rate limits, retries
3. **Structured output** — Use JSON/JSONL for automation
4. **Reusable artifacts** — Save output to files
5. **Recover from failures** — Tighten scope, lower concurrency, add timeouts
6. **Keep traffic reasonable** — Avoid DoS-level scanning
7. **Cross-reference** — Correlate findings across tools
8. **Verify manually** — Tools produce hypotheses, validate with manual testing
9. **Document parameters** — Record exact commands and flags used
10. **Stay in scope** — Never scan beyond authorized targets

