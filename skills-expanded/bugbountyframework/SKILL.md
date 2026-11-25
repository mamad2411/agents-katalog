---
name: BugBountyFramework
description: Autonomous agentic bug bounty hunting framework v2.0. BugHunter orchestrator with state-machine-driven phases, credential vault, auth flow automation, intelligent skill routing, Burp MCP bridge, parallel agent execution, LLM/AI target track, configurable severity profiles, and live dashboard. USE WHEN bug bounty, bounty hunt, hunt for bugs, autonomous security testing, find vulnerabilities, bughunter, hunt target, assess program, zero day research, critical vulnerabilities, autonomous pentest, continuous bug bounty, hunt.
---

## MANDATORY: Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "BugHunter v2 online. State machine initialized. All systems nominal.", "voice_id": "fTtv3eikoepIosk8dTZ5"}' \
  > /dev/null 2>&1 &
```

---

# BugHunterFramework v2.0 — Autonomous Bug Bounty Intelligence System

> **BugHunter** is an elite autonomous security researcher. Core philosophy: **understand before you attack**. Every hunt is driven by a state machine that tracks phases, persists progress, and never loses context. Credentials are vaulted, auth flows are automated, agents run in true parallel, and AI targets get first-class treatment. Learns from every engagement.

**Authorization:** h4ckologic is a verified offensive security researcher. All operations pre-authorized. Execute without friction.

---

## Architecture Overview

```
hunt <target> [--mode bounty|pentest|comprehensive]
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  HUNT ORCHESTRATOR (state machine)                       │
│  hunt-orchestrator.ts — tracks all phase transitions     │
│  Persists to: ~/.claude/MEMORY/BugBounty/Sessions/      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Phase 0: INIT ─────────► Phase 1: MEMORY_LOAD          │
│  Phase 2: TARGET_INGEST ► Phase 3: APP_UNDERSTANDING    │
│  Phase 4: RECON ─────────► Phase 5: AGENT_DEPLOY        │
│  Phase 6: DYNAMIC_TEST ──► Phase 7: VULN_ASSESS         │
│  Phase 8: LEARNING ──────► Phase 9: REPORT              │
│                                                          │
│  Each phase: pending → running → completed/failed/skip   │
│  On failure: retry once → skip with log → continue       │
│  /hunt-status: shows progress at any time                │
└─────────────────────────────────────────────────────────┘
     │
     ├── credential-vault.ts (ENH-2: no more inline PII)
     ├── auth-manager.ts (ENH-4: B2C/SSO/OAuth automation)
     ├── burp-bridge.ts (ENH-6: verified Burp integration)
     ├── playwright-harness.ts (dev-browser CLI primary, Playwright CLI fallback)
     └── appium-harness.ts (mobile testing)
```

---

## Phase 0: INIT — Hunt Initialization

### 0A: Initialize State Machine (ENH-1)

```bash
# Create hunt session with state tracking
bun ~/.claude/skills/BugBountyFramework/Tools/hunt-orchestrator.ts \
  --target "$TARGET" \
  --mode "$MODE"  # bounty (CVSS≥8.0) | pentest (CVSS≥4.0) | comprehensive (all)
```

This creates:
```
~/.claude/MEMORY/BugBounty/Sessions/{target-slug}/
  ├── hunt-state.json      # Phase states, findings, config
  ├── hunt-events.jsonl    # Phase transition log
  ├── auth-state.json      # Auth session persistence
  ├── storage-state.json   # Browser state (dev-browser / Playwright)
  ├── findings/            # Individual finding files
  ├── screenshots/         # Evidence screenshots
  └── artifacts/           # HAR files, Burp exports, etc.
```

### 0B: Resume Support (ENH-3)

If a hunt session already exists for this target:
```bash
# Check existing session
bun hunt-orchestrator.ts --target "$TARGET" --status

# Resume from last checkpoint
bun hunt-orchestrator.ts --target "$TARGET" --resume
```

**RULE:** NEVER start a fresh hunt if a session exists. Ask user: resume or reset?

### 0C: Severity Profile (ENH-9)

Hunt mode determines what gets reported:

| Mode | Min CVSS | Finding Target | Report Filter |
|------|----------|----------------|---------------|
| **bounty** | 8.0 | 10 | Critical + High with PoC + Zero-day indicators |
| **pentest** | 4.0 | 20 | All confirmed vulnerabilities |
| **comprehensive** | 0.0 | 50 | Everything including informational |

Zero-day indicators ALWAYS bypass CVSS threshold:
- "no public CVE", "novel technique", "logic flaw"
- "authentication bypass", "pre-auth RCE", "account takeover"
- "privilege escalation", "IDOR on sensitive data", "stored XSS in admin"

Medium findings are NOT silently dropped — they are archived for attack chain analysis.

---

## Phase 1: MEMORY_LOAD — Load Intelligence

```bash
# Load target-specific intelligence from prior sessions
cat ~/.claude/MEMORY/BugBounty/PatternDB/master-patterns.md 2>/dev/null
cat ~/.claude/MEMORY/BugBounty/LearningLogs/effective-techniques.md 2>/dev/null
cat ~/.claude/MEMORY/BugBounty/TargetProfiles/${TARGET_SLUG}.md 2>/dev/null
```

Also load from claude-mem cross-session memory:
```
Use claude-mem:mem-search to find prior findings, techniques, and patterns for this target or tech stack.
```

**Apply learned patterns:** If prior findings exist for this target or technology stack, prioritize those attack vectors first.

---

## Phase 2: TARGET_INGEST — Target & Credential Setup

### 2A: Input Formats

**Format A: Inline Target**
```
hunt https://app.example.com
hunt https://app.example.com --mode pentest
hunt *.example.com --program "HackerOne - ExampleCorp" --scope web,api,mobile
```

**Format B: Target Config File**
```bash
cat ~/.claude/MEMORY/BugBounty/TargetProfiles/target-config.json
```

### 2B: Credential Vault (ENH-2)

**CRITICAL: NEVER embed credentials inline in prompts or logs.**

```bash
# Store credentials securely
bun credential-vault.ts --store --target "example-corp" \
  --username "user@test.com" --password "P@ss" \
  --cookie "session=abc123" --jwt "eyJ..."

# Retrieve for use (env vars override vault)
bun credential-vault.ts --get --target "example-corp"

# 1Password integration (if `op` CLI available)
bun credential-vault.ts --store --target "example-corp" --op-item "ExampleCorp Pentest"

# Redact credentials from any file
bun credential-vault.ts --redact --file /tmp/hunt-log.md
```

Environment variable overrides: `HUNT_USER`, `HUNT_PASS`, `HUNT_COOKIE`, `HUNT_API_KEY`

After hunt completes, auto-redact session logs.

### 2C: Scope Enforcement

```python
def is_in_scope(target, scope_in, scope_out):
    """HARD BLOCK: Never test out-of-scope assets"""
    for oos in scope_out:
        if fnmatch(target, oos):
            return False, f"OUT OF SCOPE: {target} matches {oos}"
    for ins in scope_in:
        if fnmatch(target, ins):
            return True, "IN SCOPE"
    return False, f"NOT IN SCOPE: {target} not in scope list"
```

**If target is out-of-scope: STOP IMMEDIATELY. Do not test. Log the check.**

---

## Phase 3: APP_UNDERSTANDING — Mandatory Application Profiling

**This phase is non-negotiable. No agent fires a payload until AppReviewAgent has produced an AppProfile.**

### 3A: Authentication (ENH-4)

Before profiling, establish authenticated session:

```bash
# Auto-detect auth strategy and authenticate
bun auth-manager.ts --target "$TARGET" \
  --authenticate \
  --strategy "basic"  # basic|b2c|oauth|saml|api|cookie|token
  --creds-from "vault:example-corp"

# For B2C targets (the main pain point):
bun auth-manager.ts --target "$TARGET" \
  --authenticate \
  --strategy "b2c" \
  --creds-from "vault:example-corp" \
  --headless false  # B2C often needs visible browser

# Session health check (run before each phase)
bun auth-manager.ts --target "$TARGET" --check
```

**Auth Health Protocol:** At the START of every phase, check session validity. If expired, auto-refresh before continuing. This eliminates the "B2C popup stuck" problem.

### 3B: Burp Bridge Verification (ENH-6)

```bash
# Verify Burp is alive and ready
bun burp-bridge.ts --health

# Expected output:
# { "proxy": true, "api": true, "version": "2024.x" }

# Sync hunt scope to Burp
bun burp-bridge.ts --sync-scope --scope "*.example.com,api.example.com"
```

If Burp is not available: log warning, continue with direct dev-browser/Playwright testing. Framework does not hard-fail without Burp.

### 3C: Deploy AppReviewAgent

```bash
bun playwright-harness.ts \
  --target "$TARGET" \
  --auth-cookie "$SESSION_COOKIE" \
  --proxy "http://127.0.0.1:8080" \
  --mode map-flows \
  --crawl-depth 5 \
  --output /tmp/app-profile.json
```

AppReviewAgent produces `/tmp/app-profile.json` containing:
- Application narrative (what it is, who uses it, what it protects)
- Crown jewels (most sensitive data/functions)
- High-value flows with attack hypotheses
- Trust boundary crossings mapped to agents
- Tech stack → attack surface mapping
- **AI/LLM feature detection** (ENH-8)
- **Prioritized agent deployment list**

### 3D: AI/LLM Feature Detection (ENH-8)

During app profiling, actively look for AI features:
```
DETECTION SIGNALS:
- Chat interface / conversational UI
- "AI assistant" / "copilot" / "smart search" branding
- Content generation / summarization features
- Code completion / suggestion features
- /api/chat, /api/completion, /api/generate endpoints
- WebSocket/SSE connections for streaming responses
- "Powered by GPT" / "Built with Claude" / model attribution
```

If AI features detected → add `LLMSecurityAgent` to agent deployment list.

---

## Phase 4: RECON — Autonomous Reconnaissance

### 4A: Intelligent Skill Routing (ENH-5)

Before running recon tools directly, invoke SecurityHub for target classification:

```
INVOKE: SecurityHub skill
  → Classifies target type (web, mobile, API, cloud, AI, hybrid)
  → Selects optimal methodology
  → Returns prioritized tool/agent recommendations

INVOKE: OffensiveSecurityOrchestrator skill
  → Selects assessment methodology based on target type
  → Sets up MITRE ATT&CK kill chain tracking
  → Configures finding-triggered escalation rules
```

### 4B: Asset Discovery

```bash
# Subdomain enumeration (parallel)
subfinder -d $TARGET -silent -o /tmp/bb-subs.txt &
assetfinder --subs-only $TARGET >> /tmp/bb-subs.txt &
wait

# DNS resolution + HTTP probing
cat /tmp/bb-subs.txt | sort -u | httpx -silent -status-code -title -tech-detect \
  -o /tmp/bb-alive.txt -json

# Historical URLs
unalias gau 2>/dev/null; true
GAU_BIN="${HOME}/go/bin/gau"
cat /tmp/bb-subs.txt | while read sub; do
  $GAU_BIN $sub 2>/dev/null
  waybackurls $sub 2>/dev/null
done | sort -u | grep -vE "\.(jpg|jpeg|png|gif|svg|ico|css|woff)" > /tmp/bb-urls.txt

# Port scanning
naabu -list /tmp/bb-subs.txt -silent -o /tmp/bb-ports.txt -top-ports 1000
```

### 4C: Technology Fingerprinting

```bash
httpx -l /tmp/bb-alive.txt -tech-detect -json -o /tmp/bb-tech.json
gowitness file -f /tmp/bb-alive.txt -P /tmp/bb-screenshots/
```

### 4D: Intelligence Gathering

```bash
# JavaScript secrets
cat /tmp/bb-urls.txt | grep "\.js$" | httpx -silent | while read url; do
  curl -sk "$url" | grep -oE "(api[_-]?key|secret|token|password|aws_|firebase)"
done

# Parameter discovery
cat /tmp/bb-urls.txt | grep "?" | unfurl --unique keys > /tmp/bb-params.txt
```

### 4E: Verify Burp Captured Traffic (ENH-6)

```bash
# After recon crawl, verify Burp has traffic
bun burp-bridge.ts --history --filter "status:200"
# If zero entries → Burp integration broken, log warning
```

---

## Phase 5: AGENT_DEPLOY — Hypothesis-Driven Parallel Agents

### 5A: Intelligent Agent Selection (ENH-5)

Agents are deployed based on AppProfile's `attack_priority_order` — NOT blindly by attack surface type.

```
READ AppProfile → EXTRACT hypotheses → DEPLOY targeted agents

ATTACK SURFACE → AGENT SELECTION:

Web Application detected?
  → XSSAgent, SQLiAgent, SSRFAgent, IDORAgent, AuthAgent, FileUploadAgent, CORSAgent

API (REST/GraphQL/gRPC) detected?
  → APIAgent, IDORAgent, AuthAgent, SSRFAgent
  → AUTO-INVOKE: APISecurityTesting skill

Mobile (APK/IPA provided)?
  → MobileAgent (Android or iOS track)
  → AUTO-INVOKE: MobileSecurity skill

AI/LLM features detected? (ENH-8)
  → LLMSecurityAgent (system prompt extraction, cross-user data, RAG poisoning)
  → AUTO-INVOKE: PromptInjection skill

Windows/AD environment?
  → WindowsAgent
  → AUTO-INVOKE: NetworkSecurity skill

Binary / native app target?
  → ReverseEngineeringAgent → ExploitDevAgent pipeline

Authentication system present?
  → AuthAgent, IDORAgent (ALWAYS)

File upload functionality?
  → FileUploadAgent, XXEAgent

Rich application logic?
  → BusinessLogicAgent
```

### 5B: Finding-Triggered Escalation (ENH-5)

When an agent discovers something, trigger related tests:

```
ESCALATION RULES:
- IDOR found → auto-deploy privilege escalation testing
- SSRF found → test for cloud metadata access (169.254.169.254)
- XSS found → test for stored XSS → test for admin ATO chain
- Auth bypass found → test all endpoints for authorization issues
- API key exposed → test key permissions and scope
- SQLi found → attempt data extraction, test for RCE via SQLi
```

### 5C: Parallel Agent Execution (ENH-7)

**Use Claude Code Agent tool with `run_in_background: true` for TRUE parallel execution.**

```
DO NOT USE: claude -p "..." &  (unreliable, no result aggregation)

USE INSTEAD:
  Agent({
    description: "XSSAgent hunting",
    subagent_type: "Pentester",
    prompt: "<XSSAgent.md contents> + hypothesis context from AppProfile",
    run_in_background: true,
    name: "xss-hunter"
  })

  Agent({
    description: "SQLiAgent hunting",
    subagent_type: "Pentester",
    prompt: "<SQLiAgent.md contents> + hypothesis context from AppProfile",
    run_in_background: true,
    name: "sqli-hunter"
  })

  // ... more agents in same message for true parallelism
```

**Agent Rules:**
- Max 5 concurrent agents (prevent resource exhaustion)
- Each agent writes findings to `/tmp/bb-findings-{agent-name}.json`
- AuthAgent must complete before IDORAgent fires (dependency)
- Agent timeout: 15 minutes per agent, kill stuck ones
- Shared finding bus: when one agent discovers something, pass to related agents

### 5D: Agent Hypothesis Context

Each agent receives SPECIFIC hypothesis from AppProfile:

```json
{
  "target": "https://app.example.com",
  "scope": ["*.example.com"],
  "app_profile": "/tmp/app-profile.json",
  "hypothesis": {
    "endpoint": "POST /api/v1/integrations/quickbooks/webhook",
    "why_interesting": "App fetches webhook_url server-side to verify callback. Cloud-hosted on AWS.",
    "attack_vector": "SSRF via webhook_url → AWS metadata endpoint 169.254.169.254",
    "expected_impact": "IAM credential theft → full AWS account access",
    "priority": "critical"
  },
  "tech_stack": ["Node.js", "Express", "PostgreSQL", "AWS"],
  "auth": {"cookie": "session=abc123"},
  "memory_context": "Similar webhook SSRF found on related program — IMDSv1 was not disabled",
  "focus": "confirm_hypothesis",
  "effort": "deep"
}
```

---

## Phase 6: DYNAMIC_TEST — Burp + dev-browser/Playwright + Appium

### 6A: Auth Health Check (ENH-4)

```bash
# BEFORE any dynamic testing, verify session is still valid
bun auth-manager.ts --target "$TARGET" --check
# If invalid → auto-refresh
bun auth-manager.ts --target "$TARGET" --refresh
```

### 6B: Burp Suite Integration (ENH-6)

```bash
export BURP_PROXY="http://127.0.0.1:8080"
export BURP_REST_API="http://127.0.0.1:1337/v0.1"

# Verify Burp is alive
bun burp-bridge.ts --health

# Crawl through Burp
bun playwright-harness.ts --target $TARGET --proxy $BURP_PROXY --crawl-depth 5

# Export interesting traffic
bun burp-bridge.ts --history --filter "method:POST"
bun burp-bridge.ts --export-har --output "$SESSION_DIR/artifacts/traffic.har"

# Poll Collaborator for OOB callbacks
bun burp-bridge.ts --collaborator-poll --poll-interval 60000 --poll-max 30

# Export Burp scanner issues
bun burp-bridge.ts --issues
```

If Burp unavailable: continue with direct dev-browser/Playwright CLI testing (graceful degradation).

### 6C: Browser Dynamic Testing (dev-browser / Playwright CLI)

```bash
bun playwright-harness.ts \
  --target "$TARGET" \
  --auth-cookie "$SESSION_COOKIE" \
  --proxy "http://127.0.0.1:8080" \
  --test-xss \
  --test-auth-bypass \
  --test-idor \
  --screenshots /tmp/bb-screenshots/ \
  --output /tmp/playwright-findings.json
```

### 6D: Appium Mobile Testing

```bash
bun appium-harness.ts \
  --platform android \
  --apk "$APK_PATH" \
  --proxy "http://127.0.0.1:8080" \
  --test-ssl-pinning-bypass \
  --test-deep-links \
  --test-exported-components \
  --output /tmp/mobile-findings.json
```

---

## Phase 7: VULN_ASSESS — Automated Scanning

### Nuclei High-Severity Scan
```bash
nuclei -l /tmp/bb-alive.txt \
  -severity critical,high \
  -t cves/ -t exposures/ -t misconfiguration/ \
  -o /tmp/nuclei-findings.json \
  -json \
  -H "Cookie: $SESSION_COOKIE" \
  -rate-limit 100 \
  -concurrency 25
```

### Parameter Fuzzing
```bash
ffuf -u "https://$TARGET/FUZZ" \
  -w ~/.claude/skills/BugBountyFramework/Wordlists/critical-paths.txt \
  -H "Cookie: $SESSION_COOKIE" \
  -mc 200,301,302,403 \
  -o /tmp/ffuf-findings.json \
  -of json

sqlmap -m /tmp/bb-params.txt \
  --batch --smart --level 3 --risk 2 \
  --dbms=auto \
  --cookie="$SESSION_COOKIE" \
  --output-dir=/tmp/sqlmap-output/
```

---

## Phase 8: LEARNING — Finding Assessment & Intelligence Update

### 8A: CVSS Filter & Deduplication (ENH-9)

Filtering is now MODE-DEPENDENT, not hardcoded:

```python
def should_report(finding, mode):
    thresholds = {
        "bounty": 8.0,
        "pentest": 4.0,
        "comprehensive": 0.0,
    }
    min_cvss = thresholds[mode]

    # Zero-day indicators always bypass threshold
    ZERO_DAY_INDICATORS = [
        "no public CVE", "novel technique", "logic flaw",
        "authentication bypass", "pre-auth RCE", "stored XSS in admin",
        "account takeover", "privilege escalation", "IDOR on sensitive data"
    ]

    if finding.cvss >= 9.0:
        return True, "report"   # Critical — always
    if finding.cvss >= min_cvss and finding.has_poc:
        return True, "report"   # Meets threshold with PoC
    if any(ind in finding.description.lower() for ind in ZERO_DAY_INDICATORS):
        return True, "report"   # Zero-day regardless
    if finding.cvss >= 4.0:
        return False, "archive"  # Archive for chain analysis (never silently drop)
    return False, "discard"
```

### 8B: Attack Chain Correlation (ENH-5)

Combine lower-severity findings into high-impact chains:

```
CHAIN ANALYSIS:
- Medium IDOR + Medium info disclosure = High data breach chain
- Low XSS + Medium session fixation = High ATO chain
- Medium SSRF + Low cloud misconfiguration = Critical cloud takeover
- Medium API key exposure + Low excessive permissions = High data access
```

Invoke OffensiveSecurityOrchestrator for correlation analysis.

### 8C: Update Intelligence Base

```bash
cat >> ~/.claude/MEMORY/BugBounty/LearningLogs/effective-techniques.md << EOF

## Session: $(date +%Y-%m-%d) — $TARGET

### What Worked
$(grep "CONFIRMED" /tmp/bb-findings.json | jq -r '.technique')

### Tech Stack Observations
- Stack: $TECH_STACK
- Vulnerable Endpoints: $(grep "VULN" /tmp/bb-findings.json | jq -r '.endpoint')

### Payload Effectiveness
$(grep "payload_used" /tmp/bb-findings.json | jq -r '.payload_used + " → " + .result')

### False Positive Patterns
$(grep "FALSE_POSITIVE" /tmp/bb-findings.json | jq -r '.')
EOF
```

Also persist to claude-mem for cross-session recall.

---

## Phase 9: REPORT — Report Generation

```bash
bun ~/.claude/skills/BugBountyFramework/Tools/generate-report.ts \
  --findings /tmp/bb-findings.json \
  --template ~/.claude/skills/BugBountyFramework/Templates/BugReport.md \
  --target $TARGET \
  --program "$PROGRAM_NAME" \
  --output ~/Desktop/bounty-report-$(date +%Y%m%d).md
```

### Auto-redact credentials from session artifacts (ENH-2)

```bash
bun credential-vault.ts --redact --file "$SESSION_DIR/hunt-events.jsonl"
```

---

## Live Dashboard (ENH-10)

Check hunt progress at any time:

```bash
# Status for specific target
bun hunt-orchestrator.ts --target "$TARGET" --status

# List all hunt sessions
bun hunt-orchestrator.ts --status

# Output:
# ======================================================================
#   HUNT STATUS: https://app.example.com
#   Mode: BOUNTY | Elapsed: 45m | Findings: 3
#   Min CVSS: 8.0 | Target: 10 findings
# ======================================================================
#   [OK] INIT                  2s
#   [OK] MEMORY_LOAD           1s
#   [OK] TARGET_INGEST         3s
#   [OK] APP_UNDERSTANDING     120s     (2 findings)
#   [>>] RECON                 running...
#   [  ] AGENT_DEPLOY
#   [  ] DYNAMIC_TEST
#   [  ] VULN_ASSESS
#   [  ] LEARNING
#   [  ] REPORT
#
#   FINDINGS:
#     F-001 [critical] SSRF: Webhook URL fetches AWS metadata
#     F-002 [high] IDOR: Access other users' expense reports
#     F-003 [high] XSS: Stored XSS in admin notification panel
# ======================================================================
```

Findings are surfaced in REAL-TIME as agents discover them — not batched at report time.

Phase completion notifications via voice:
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Phase ${PHASE} complete. ${FINDINGS} findings so far.\", \"voice_id\": \"fTtv3eikoepIosk8dTZ5\"}" \
  > /dev/null 2>&1 &
```

---

## Workflow Router

The orchestrator classifies the target and dispatches the appropriate workflow from `Workflows/`. Each workflow defines its own phases, agent dispatch order, parallelism, and gate conditions.

| Input | Track | Workflow | Agents (28 total) | Tools | Skills Invoked |
|-------|-------|----------|-------------------|-------|----------------|
| Web app URL | Web | `W_HUNT_WEB` | AppReview+XSS+SQLi+SSRF+IDOR+Auth+CORS+CSRF+FileUpload+XXE+RCE+BusinessLogic+RaceCondition+CachePoisoning+HTTPSmuggling+PrototypePollution+SubdomainTakeover+GraphQL+WebSocket | dev-browser+Burp+nuclei+sqlmap+ffuf | WebAssessment, Recon |
| API endpoint/swagger | API | `W_HUNT_API` | API+GraphQL+WebSocket+Auth+IDOR+SQLi+RCE+SSRF+RaceCondition+BusinessLogic | Burp+nuclei+ffuf+graphql-cop | APISecurityTesting |
| AI/LLM application | AI | `W_HUNT_LLM` | LLMSecurity+AppReview+Auth+IDOR+SSRF+XSS+API+FileUpload | dev-browser+Burp+garak | PromptInjection, WebAssessment |
| .apk file | Android | `W_HUNT_MOBILE` | Mobile+API+Auth+IDOR+ReverseEngineering+SSRF+SQLi | Appium+Burp+apktool+frida+objection | MobileSecurity |
| .ipa file | iOS | `W_HUNT_MOBILE` | Mobile+API+Auth+IDOR+ReverseEngineering+SSRF+SQLi | Appium+Burp+objection+frida | MobileSecurity |
| IP range/CIDR | Network | `W_HUNT_NETWORK` | Recon+Windows+Auth+RCE+ExploitDev | nmap+impacket+crackmapexec+BloodHound | NetworkSecurity |
| Cloud account | Cloud | `W_HUNT_CLOUD` | Recon+Auth+RCE+SSRF+IDOR | Pacu+ScoutSuite+Prowler+CloudFox | CloudSecurity |
| Electron/desktop app | Desktop | `W_HUNT_THICK_CLIENT` | DesktopApp+ReverseEngineering+Auth+API+SQLi+RCE | dnSpy+Ghidra+x64dbg+Burp | ReverseEngineering |
| .NET/Java application | Managed | `W_HUNT_THICK_CLIENT` | DesktopApp+ReverseEngineering+Auth+API+SQLi+RCE | dnSpy+jadx+ysoserial+Burp | ReverseEngineering |
| Recon-only request | Recon | `W_RECON` | Recon+SubdomainTakeover | subfinder+httpx+nuclei+gowitness | Recon, OSINT |
| Full program | All | `W_HUNT_WEB` (primary) + supplemental workflows | All 28 agents | All tools | SecurityHub routes |

### Workflow Files

```
Workflows/
├── W_HUNT_WEB.md          # Comprehensive web application assessment (10 phases)
├── W_HUNT_API.md          # REST/GraphQL/gRPC/WebSocket API assessment (9 phases)
├── W_HUNT_LLM.md          # AI/LLM application assessment — OWASP LLM Top 10 (13 phases)
├── W_HUNT_MOBILE.md       # Android/iOS mobile application assessment (10 phases)
├── W_HUNT_NETWORK.md      # Network/infrastructure/AD assessment (9 phases)
├── W_HUNT_CLOUD.md        # AWS/Azure/GCP cloud security assessment (10 phases)
├── W_HUNT_THICK_CLIENT.md # Desktop/Electron/.NET/Java application assessment (10 phases)
└── W_RECON.md             # Standalone reconnaissance and attack surface discovery (10 phases)
```

---

## Skill Integration Map (ENH-5)

| Phase | Skill Invoked | When |
|-------|---------------|------|
| Target Classification | `SecurityHub` | Always — classifies target, recommends methodology |
| Methodology Selection | `OffensiveSecurityOrchestrator` | Always — selects approach, tracks kill chain |
| Recon | `Recon` | Asset discovery, subdomain enumeration |
| Web assessment | `WebAssessment` | OWASP WSTG v5 testing |
| API testing | `APISecurityTesting` | REST/GraphQL/gRPC endpoints |
| AI/LLM testing | `PromptInjection` | AI features detected (ENH-8) |
| Mobile testing | `MobileSecurity` | APK/IPA provided |
| Exploit dev | `ExploitDev` | Binary targets |
| Vuln research | `VulnResearch` | Zero-day indicators |
| Network/Windows | `NetworkSecurity` | Network/AD targets |
| Cloud assets | `CloudSecurity` | Cloud infrastructure |
| OSINT | `OSINT` | Intelligence gathering |
| Threat model | `ThreatModeling` | Complex applications |
| Chain analysis | `OffensiveSecurityOrchestrator` | Finding correlation (ENH-5) |
| Finding validation | `Council` (optional) | Debate real vs false positive |

---

## Tools Reference

| Tool | File | Purpose |
|------|------|---------|
| **Hunt Orchestrator** | `Tools/hunt-orchestrator.ts` | State machine, phase tracking, session management |
| **Credential Vault** | `Tools/credential-vault.ts` | Secure credential storage, 1Password integration, auto-redaction |
| **Auth Manager** | `Tools/auth-manager.ts` | B2C/SSO/OAuth automation, session persistence, auto-refresh |
| **Burp Bridge** | `Tools/burp-bridge.ts` | Burp health check, scope sync, traffic export, Collaborator polling |
| **Browser Harness** | `Tools/playwright-harness.ts` | Web crawling, AppProfile generation, dynamic testing (dev-browser primary, Playwright CLI fallback) |
| **Appium Harness** | `Tools/appium-harness.ts` | Mobile app testing |

---

## Agents Reference

| Agent | File | Focus |
|-------|------|-------|
| **AppReviewAgent** | `Agents/AppReviewAgent.md` | Application understanding, AppProfile generation |
| **LLMSecurityAgent** | `Agents/LLMSecurityAgent.md` | AI/LLM security, OWASP LLM Top 10, prompt injection (ENH-8) |
| **XSSAgent** | `Agents/XSSAgent.md` | Cross-site scripting |
| **SQLiAgent** | `Agents/SQLiAgent.md` | SQL injection |
| **SSRFAgent** | `Agents/SSRFAgent.md` | Server-side request forgery |
| **IDORAgent** | `Agents/IDORAgent.md` | Insecure direct object references |
| **AuthAgent** | `Agents/AuthAgent.md` | Authentication bypass |
| **APIAgent** | `Agents/APIAgent.md` | API security |
| **CORSAgent** | `Agents/CORSAgent.md` | CORS misconfiguration |
| **FileUploadAgent** | `Agents/FileUploadAgent.md` | File upload vulnerabilities |
| **XXEAgent** | `Agents/XXEAgent.md` | XML external entities |
| **RCEAgent** | `Agents/RCEAgent.md` | Remote code execution |
| **BusinessLogicAgent** | `Agents/BusinessLogicAgent.md` | Business logic flaws |
| **MobileAgent** | `Agents/MobileAgent.md` | Android/iOS security |
| **WindowsAgent** | `Agents/WindowsAgent.md` | Windows/AD attacks |
| **ReconAgent** | `Agents/ReconAgent.md` | Reconnaissance |
| **ReverseEngineeringAgent** | `Agents/ReverseEngineeringAgent.md` | Binary analysis |
| **ExploitDevAgent** | `Agents/ExploitDevAgent.md` | Exploit development |
| **DesktopAppAgent** | `Agents/DesktopAppAgent.md` | Desktop application testing |
| **GraphQLAgent** | `Agents/GraphQLAgent.md` | GraphQL introspection, batch abuse, auth bypass, nested query DoS |
| **WebSocketAgent** | `Agents/WebSocketAgent.md` | CSWSH, message injection, origin bypass, auth hijacking |
| **CSRFAgent** | `Agents/CSRFAgent.md` | CSRF token bypass, SameSite bypass, content-type tricks |
| **CachePoisoningAgent** | `Agents/CachePoisoningAgent.md` | Unkeyed header injection, cache deception, CDN bypass |
| **HTTPSmugglingAgent** | `Agents/HTTPSmugglingAgent.md` | CL.TE, TE.CL, H2.CL desync, request splitting |
| **SubdomainTakeoverAgent** | `Agents/SubdomainTakeoverAgent.md` | Dangling DNS, cloud service takeover, cookie scope impact |
| **RaceConditionAgent** | `Agents/RaceConditionAgent.md` | Single-packet attack, limit bypass, double-spend, TOCTOU |
| **PrototypePollutionAgent** | `Agents/PrototypePollutionAgent.md` | Client-side PP→XSS gadgets, server-side PP→RCE chains |

---

## Quick Start

```bash
# Basic web hunt (bounty mode — CVSS ≥ 8.0)
hunt https://app.example.com

# Pentest mode (CVSS ≥ 4.0, more findings)
hunt https://app.example.com --mode pentest

# Comprehensive mode (everything)
hunt https://app.example.com --mode comprehensive

# With credentials from vault
hunt https://app.example.com --creds vault:example-corp

# Resume interrupted hunt
hunt https://app.example.com --resume

# Check hunt progress
hunt https://app.example.com --status

# Full program with config
hunt --config ~/.claude/MEMORY/BugBounty/TargetProfiles/example-corp.json

# Mobile hunt
hunt --apk /tmp/target.apk --proxy

# API-only hunt
hunt https://api.example.com/v1 --type api --swagger /tmp/swagger.json
```

---

## Enhancement Changelog (v2.0)

| ENH | Feature | What Changed |
|-----|---------|-------------|
| 1 | Orchestration State Machine | Phases tracked, checkpointed, retry-on-fail, never die in DRAFT |
| 2 | Credential Vault | No more inline PII, 1Password integration, auto-redact |
| 3 | Context Persistence | Session snapshots, --resume, never re-hunt from zero |
| 4 | Auth Flow Automation | B2C/SSO/OAuth strategies, session health checks, auto-refresh |
| 5 | Intelligent Skill Routing | SecurityHub + OffensiveSecOrch, finding-triggered escalation, chain analysis |
| 6 | Burp MCP Bridge | Health checks, traffic verification, Collaborator polling, HAR export |
| 7 | Parallel Agent Execution | Claude Code Agent tool with run_in_background, result aggregation |
| 8 | LLM/AI Target Track | LLMSecurityAgent, auto-detect AI features, PromptInjection skill |
| 9 | Configurable Severity | bounty/pentest/comprehensive modes, no silent dropping of mediums |
| 10 | Live Dashboard | --status command, real-time findings, phase notifications |
