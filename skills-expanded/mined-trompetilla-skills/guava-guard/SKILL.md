---
name: guava-guard
description: Security scanner for AgentSkills. Scans skill directories for malicious patterns, credential theft, prompt injection, obfuscation, leaky skills, memory poisoning, prompt worms, and known ClawHavoc campaign IoCs. Run before installing any ClawHub skill.
metadata:
  openclaw:
    emoji: "🛡️"
---

# GuavaGuard v4.0 — Agent Skill Security Scanner 🍈🛡️

Zero-dependency, single-file security scanner for AgentSkills.
Now with **13 threat categories**, including Leaky Skills (Snyk), Memory Poisoning (Palo Alto),
Prompt Worms (Simula), JS data flow analysis, and CVE-2026-25253 detection.

**Ciscoはインストールに3分。GuavaGuardは3秒。**

## Why

- **534 critical skills** found on ClawHub (Snyk ToxicSkills audit, Feb 2026)
- **26% of 31,000 skills** have at least one vulnerability (Cisco research)
- **76 confirmed malicious payloads** with credential theft and backdoors
- ClawHavoc campaign: fake prerequisites → Atomic Stealer malware
- Cisco called OpenClaw "an absolute nightmare" from a security perspective
- **You need to scan before you install**

## What's New in v4.0

### Leaky Skills Detection (Snyk ToxicSkills Feb 2026)
Skills that instruct agents to mishandle secrets through the LLM context window:
- **Save-to-memory traps** — "save the API key in your memory" instructions
- **Verbatim output** — forcing agents to echo secrets to chat
- **PII collection** — credit card, SSN, passport data harvesting
- **Session log export** — dumping conversation history containing secrets
- **.env passthrough** — reading env files and passing through LLM

### Memory Poisoning (Palo Alto Networks IBC Framework)
Persistent backdoors that modify agent personality/memory files:
- **SOUL.md/IDENTITY.md writes** — behavioral override
- **MEMORY.md injection** — long-term memory corruption
- **Rule/instruction override** — changing agent guidelines
- **Persistence instructions** — "always do X from now on"
- **File writes to user home** — HEARTBEAT.md abuse

### Prompt Worms (Simula Research Lab)
Self-replicating instructions spreading through agent networks:
- **Self-replication** — "post this message to Moltbook"
- **Agent-to-agent propagation** — "tell other agents to..."
- **Hidden instruction embedding** — concealed payloads in posts
- **CSS-hidden content** — invisible-to-human instructions

### Lightweight JS AST Analysis (Zero Dependencies)
Data flow tracking without any npm packages:
- **Secret → Network** — API key read then sent via fetch/axios
- **Secret → Exec** — credentials passed to shell commands
- **Import trifecta** — fs + child_process + http = full system access
- **Dynamic URL secrets** — template literals with env vars in URLs
- **Suspicious import combos** — child_process + network modules

### Additional v4.0 Features
- **CVE-2026-25253 patterns** — gatewayUrl injection, sandbox disabling, Gatekeeper bypass
- **Persistence detection** — cron jobs, startup hooks, LaunchAgents, systemd
- **Cross-file analysis** — phantom references, base64 fragment assembly, load→exec chains
- **HTML report** (`--html`) — dark-theme visual dashboard
- **Enhanced combo multipliers** — leaky+exfil=2x, memory-poison=1.5x, prompt-worm=2x

## What It Detects

### Threat Taxonomy (Snyk ToxicSkills + Cisco AITech aligned)

| # | Category | Severity | Examples |
|---|----------|----------|----------|
| 1 | **Prompt Injection** | 🔴 CRITICAL | `ignore previous instructions`, zero-width Unicode, BiDi attacks, XML tag injection, homoglyphs |
| 2 | **Malicious Code** | 🔴 CRITICAL | eval(), reverse shells, socket connections, Function constructor |
| 3 | **Suspicious Downloads** | 🔴 CRITICAL | curl\|bash, password-protected ZIPs, GitHub release downloads |
| 4 | **Credential Handling** | 🟠 HIGH | .env reading, SSH key access, wallet credentials, sudo in instructions |
| 5 | **Secret Detection** | 🟠 HIGH | Hardcoded API keys, AWS keys, private keys, GitHub tokens, entropy analysis |
| 6 | **Exfiltration** | 🟡 MEDIUM | webhook.site, POST with secrets, DNS exfil, curl data exfil |
| 7 | **Dependency Chain** | 🟠 HIGH | Risky npm packages, lifecycle scripts, remote deps, wildcard versions |
| 8 | **Financial Access** | 🟡 MEDIUM | Crypto transactions, payment API integrations |
| 9 | **Leaky Skills** | 🔴 CRITICAL | Save key to memory, verbatim output, PII collection, .env passthrough |
| 10 | **Memory Poisoning** | 🔴 CRITICAL | SOUL.md writes, memory injection, rule override, persistence |
| 11 | **Prompt Worm** | 🔴 CRITICAL | Self-replication, agent propagation, hidden instructions, CSS hiding |
| 12 | **Persistence** | 🟠 HIGH | Cron jobs, startup hooks, LaunchAgents, systemd, heartbeat abuse |
| 13 | **CVE Patterns** | 🔴 CRITICAL | CVE-2026-25253, gatewayUrl injection, sandbox disable, Gatekeeper bypass |
| + | **Data Flow** | 🔴 CRITICAL | Secret→network, secret→exec, import trifecta, URL secret interpolation |
| + | **Obfuscation** | 🟠 HIGH | hex encoding, base64→exec chains, charCode construction |

### Additional Detections
- **Prerequisites Fraud**: ClawHavoc-style fake install steps
- **Known IoCs**: Malicious IPs, domains, URLs, usernames, typosquat names
- **Structural Analysis**: Missing SKILL.md, undocumented scripts, hidden files
- **Shannon Entropy**: Detects high-entropy strings (likely leaked secrets)
- **Flow Analysis**: credential-read → network-send data flow detection

## Key Features

### Zero Dependencies, Single File
One `.js` file, 854 lines, Node.js 18+ only. No pip, no API keys, no setup.
**Copy → Run → Done.** That's the GuavaGuard philosophy.

### Context-Aware Scanning
Code patterns only match in code files (.js, .py, .sh, etc.), not in documentation.
This **reduces false positives by ~80%** compared to naive pattern matching.

### Self-Exclusion
Use `--self-exclude` to skip scanning the scanner's own directory (which contains IoC definitions that would trigger itself).

### Whitelist Support
Create `.guava-guard-ignore` in your scan directory:
```
# Skip trusted skills
my-trusted-skill
another-safe-skill

# Suppress specific pattern IDs
pattern:CRED_ENV_FILE
pattern:MAL_SHELL
```

### Flow Analysis
Combo multipliers detect dangerous data flows:
- Credential access + exfiltration → **2x risk**
- Credential access + code execution → **1.5x risk**
- Obfuscation + credential/code patterns → **2x risk**
- Lifecycle script + code execution → **2x risk** (v3)
- BiDi attacks + other findings → **1.5x risk** (v3)

## Usage

```bash
# Basic scan (recommended)
node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude

# Full scan with dependency chain analysis
node guava-guard.js ./skills/ --verbose --self-exclude --check-deps

# Strict mode (lower thresholds)
node guava-guard.js ./skills/ --strict --verbose

# JSON report with recommendations
node guava-guard.js ./skills/ --json --self-exclude

# Summary only (CI/CD friendly)
node guava-guard.js ./skills/ --summary-only
```

## Options

| Flag | Description |
|------|-------------|
| `--verbose`, `-v` | Show detailed findings grouped by category |
| `--json` | Write JSON report with recommendations |
| `--self-exclude` | Skip scanning the guava-guard directory |
| `--strict` | Lower thresholds (suspicious=20, malicious=60) |
| `--summary-only` | Print only the summary table |
| `--check-deps` | Enable dependency chain scanning (package.json) |
| `--help`, `-h` | Show help |

## Risk Scoring

| Severity | Points | Examples |
|----------|--------|----------|
| CRITICAL | 40 | Known IoC, BiDi attack, prompt injection, reverse shell |
| HIGH | 15 | Credential access, obfuscation, hardcoded secrets, risky deps |
| MEDIUM | 5 | Network requests, child process, sandbox detection |
| LOW | 2 | Structural issues |

| Risk Score | Verdict |
|-----------|---------|
| 0 | 🟢 CLEAN |
| 1-29 | 🟢 LOW RISK |
| 30-79 | 🟡 SUSPICIOUS |
| 80-100 | 🔴 MALICIOUS |

## Comparison (v4.0)

| Feature | GuavaGuard v4 | Cisco Skill Scanner | Snyk Evo | Koi Clawdex |
|---------|:------------:|:-------------------:|:--------:|:-----------:|
| Zero dependencies | ✅ | ❌ (Python+pip) | ❌ (Python) | ❌ |
| Single file | ✅ | ❌ | ❌ | ❌ |
| IoC matching | ✅ | ✅ | ✅ | ✅ |
| Code pattern detection | ✅ | ✅ | ✅ | ✅ |
| Context-aware (code vs docs) | ✅ | ✅ | ✅ | ❌ |
| JS data flow analysis | ✅ | ✅ (AST) | ✅ | ❌ |
| Leaky Skills detection | ✅ | ❌ | ✅ | ❌ |
| Memory poisoning | ✅ | ❌ | ❌ | ❌ |
| Prompt worm detection | ✅ | ❌ | ❌ | ❌ |
| CVE pattern matching | ✅ | ❌ | ❌ | ❌ |
| Persistence detection | ✅ | ❌ | ❌ | ❌ |
| Cross-file analysis | ✅ | ✅ | ❌ | ❌ |
| Unicode BiDi detection | ✅ | ❌ | ❌ | ❌ |
| Homoglyph detection | ✅ (3 scripts) | ❌ | ❌ | ❌ |
| Dependency chain scanning | ✅ | ✅ | ❌ | ❌ |
| Prompt injection detection | ✅ | ✅ | ✅ | ❌ |
| Prerequisites fraud | ✅ | ❌ | ❌ | ❌ |
| Entropy-based secrets | ✅ | ❌ | ✅ | ❌ |
| SARIF output (CI/CD) | ✅ | ✅ | ❌ | ❌ |
| HTML report | ✅ | ❌ | ❌ | ❌ |
| Custom rules | ✅ | ✅ (YARA) | ❌ | ❌ |
| LLM semantic analysis | ❌ (v5) | ✅ (API key) | ❌ | ❌ |
| VirusTotal integration | ❌ (v5) | ✅ (API key) | ❌ | ❌ |
| ClawHavoc IoCs | ✅ | ✅ | ✅ | ✅ |

## Roadmap

- **v5.0**: LLM intent analysis (opt-in Gemini Flash), VirusTotal API, runtime monitoring

## Exit Codes

- `0` — No malicious skills found
- `1` — Malicious skill(s) detected

## Known Limitations

- **No runtime analysis**: Static scanning only (no execution) — planned for v5
- **No AST dataflow**: Pattern-based only — AST analysis planned for v4
- **Typosquat name collision**: Official `clawhub` skill may match — use `.guava-guard-ignore`
- **Entropy false positives**: OAuth tokens may trigger SECRET_ENTROPY — suppress with ignore file

## References

- [Snyk ToxicSkills Research](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) (Feb 2026)
- [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) — Multi-engine scanner (Python)
- [ClawHavoc Campaign Analysis](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/) (Feb 2026)
- [Cisco Blog: OpenClaw Security](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) (Feb 2026)
- [Koi Security Report](https://koisecurity.io/) — 341 malicious skills on ClawHub
