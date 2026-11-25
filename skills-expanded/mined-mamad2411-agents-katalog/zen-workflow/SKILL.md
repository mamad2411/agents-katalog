# Zen Pentesting Workflow Skill

Complete end-to-end pentesting workflow using the Zen-Ai-Pentest platform.

## Quick Start

```bash
# 1. Start all services
docker compose up -d
# or: ./scripts/start-zen.sh

# 2. Run full audit via CLI
deep-audit --target example.com --phases recon,scan,exploit,report

# 3. View dashboard at http://localhost:8501
# 4. Export report: deep-report --scan-id wf-abc123 --format pdf
```

## Multi-Phase Workflow

### Phase 1: Reconnaissance
```bash
deep-recon --target example.com --output recon.json

# What happens:
# - Subdomain enumeration (subfinder, amass, dnsx)
# - Port scanning (nmap, masscan)
# - Technology fingerprinting (whatweb, wappalyzer)
# - Screenshot (gowitness, aquatone)
# - OSINT (shodan, censys integration)
```

### Phase 2: Scanning & Vulnerability Detection
```bash
deep-audit --target example.com --phases scan

# Tools engaged:
# - nuclei (community + custom templates)
# - web vulnerability (sqlmap, nikto, zap)
# - network (netexec, crackmapexec)
# - cloud (scoutsuite, prowler)
```

### Phase 3: Exploitation (requires --force)
```bash
deep-audit --target example.com --phases exploit

# Metasploit: auto-match CVEs to modules
# Custom payload generation (msfvenom)
# Credential testing via netexec
```

### Phase 4: Reporting
```bash
deep-report --scan-id YOUR-ID --format pdf
deep-report --scan-id YOUR-ID --format html
```

## Custom Workflow Script

```bash
#!/usr/bin/env bash
# custom-audit.sh
set -euo pipefail

TARGET="$1"
WORKSPACE="./workspace/${TARGET}"

mkdir -p "$WORKSPACE"

echo "=== Phase 1: Network Discovery ==="
nmap -sV -sC -oA "$WORKSPACE/nmap" "$TARGET"

echo "=== Phase 2: Web Recon ==="
gobuster dir -u "https://$TARGET" -w wordlist.txt -o "$WORKSPACE/gobuster.txt"

echo "=== Phase 3: Vulnerability Scan ==="
nuclei -u "https://$TARGET" -o "$WORKSPACE/nuclei.txt"

echo "=== Phase 4: AI Analysis ==="
python -c "
from agents.react_agent import ReActAgent
agent = ReActAgent(max_iterations=5)
print(agent.run(target='$TARGET', objective='Analyze findings in $WORKSPACE'))
"
```

## Docker Service Architecture

```
┌──────────────────────────────────────────────────┐
│                   Zen Network                    │
│  ┌──────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Terminal  │  │ WhatsApp Bot │  │ OmniRoute │ │
│  │ :23000   │  │ :23001       │  │ :20128    │ │
│  └──────────┘  └──────────────┘  └───────────┘ │
│  ┌──────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Hermes   │  │ VPN Proxy    │  │ WG Proxy  │ │
│  │ :23002   │  │ :23003       │  │ :23004    │ │
│  └──────────┘  └──────────────┘  └───────────┘ │
└──────────────────────────────────────────────────┘
```

## Runbook: Web Application Pentest

1. **Scope definition**: `agent_coordinator.create_workflow(target, phases=["recon"])`
2. **Passive recon**: WHOIS, DNS, Shodan, certificate transparency
3. **Active recon**: subdomain brute-force, port scan, tech fingerprint
4. **Vulnerability scan**: nuclei, custom template matching
5. **Manual testing**: ReAct agent-driven follow-up on findings
6. **Exploitation**: Metasploit + custom payloads (--force + admin approval)
7. **Reporting**: risk_engine scoring → PDF/HTML report generation
8. **Remediation**: CVSS-prioritized fix recommendations
