---
name: offensive-security
description: >
  AI-powered offensive security testing patterns. Penetration testing methodology, vulnerability
  assessment workflows, CTF challenges, and security tool integration. Use for authorized security
  testing, CTF competitions, and defensive security research.
---

# Offensive Security

AI-powered security testing patterns for authorized engagements.

## how to use

- `/offensive-security`
  Apply offensive security methodology to the current engagement.

- `/offensive-security <target-context>`
  Plan a security assessment for the given context.

## when to apply

Reference these guidelines when:
- conducting authorized penetration tests
- participating in CTF competitions
- building security testing automation
- reviewing code for exploitable vulnerabilities
- designing red team exercises
- building honeypots or deception technology

## authorization requirements

**CRITICAL: All offensive security activities require explicit authorization.**

Before any engagement:
1. Verify written authorization (scope document, rules of engagement)
2. Confirm target scope boundaries
3. Establish communication channels with asset owners
4. Document all activities for audit trail
5. Integration: Use the operator's PostToolUse hook (audit.log) for activity logging

## methodology: PTES framework

### Phase 1: Pre-Engagement
- Define scope, rules of engagement, emergency contacts
- Legal review and authorization documentation
- Tool preparation and environment setup

### Phase 2: Intelligence Gathering
- **Passive OSINT**: See `osint-recon` skill for detailed workflows
- **Active scanning**: Nmap, Masscan for service enumeration
- **Web enumeration**: Directory brute-force, subdomain discovery
- Integration: Use `memory` MCP server to store findings as entities/relations

### Phase 3: Threat Modeling
- Map attack surface from gathered intelligence
- Identify high-value targets and likely attack paths
- Prioritize by impact × probability
- Integration: Use `sequential` MCP thinking for complex threat models

### Phase 4: Vulnerability Analysis
- Automated scanning (Nessus, OpenVAS, Nuclei)
- Manual code review (see `security-review` skill)
- Configuration audit
- API security testing

### Phase 5: Exploitation
- Proof-of-concept development
- Privilege escalation chains
- Lateral movement mapping
- Data exfiltration simulation (authorized only)

### Phase 6: Post-Exploitation
- Persistence mechanism analysis
- Credential harvesting assessment
- Impact demonstration
- Clean-up and evidence removal

### Phase 7: Reporting
- Executive summary with business impact
- Technical findings with CVSS scores
- Remediation recommendations with priority
- Evidence documentation (screenshots, logs, PoC code)

## AI-powered security testing patterns

### Automated Reconnaissance (from HexStrike-AI concepts)
```python
# Pattern: AI-driven target profiling
from typing import TypedDict

class ReconProfile(TypedDict):
    target: str
    open_ports: list[int]
    services: dict[str, str]
    technologies: list[str]
    potential_vulns: list[str]
    attack_surface_score: float  # 0.0 - 10.0

def ai_recon_pipeline(target: str) -> ReconProfile:
    """AI-enhanced reconnaissance pipeline."""
    # 1. Port scan → service detection
    # 2. Technology fingerprinting
    # 3. CVE correlation
    # 4. Attack surface scoring
    # 5. AI-generated attack path suggestions
    ...
```

### Vulnerability Prioritization
```python
# Pattern: ML-based vulnerability prioritization
def prioritize_vulns(vulns: list[dict]) -> list[dict]:
    """Prioritize vulnerabilities using CVSS + contextual factors."""
    for vuln in vulns:
        base_score = vuln['cvss_score']
        # Contextual adjustments
        if vuln['exploitable_remotely']:
            base_score *= 1.3
        if vuln['has_public_exploit']:
            base_score *= 1.5
        if vuln['affects_auth']:
            base_score *= 1.4
        vuln['priority_score'] = min(base_score, 10.0)
    return sorted(vulns, key=lambda v: v['priority_score'], reverse=True)
```

## web application testing checklist

### Authentication Testing
- [ ] Brute force protection (rate limiting, lockout)
- [ ] Password policy enforcement
- [ ] Session management (token entropy, expiration, fixation)
- [ ] Multi-factor authentication bypass attempts
- [ ] OAuth/OIDC misconfiguration
- [ ] JWT algorithm confusion (none, HS256/RS256 swap)

### Authorization Testing
- [ ] IDOR (Insecure Direct Object Reference)
- [ ] Privilege escalation (horizontal and vertical)
- [ ] Function-level access control
- [ ] API endpoint authorization

### Injection Testing
- [ ] SQL injection (union, blind, time-based, error-based)
- [ ] XSS (reflected, stored, DOM-based)
- [ ] Command injection
- [ ] SSTI (Server-Side Template Injection)
- [ ] LDAP injection
- [ ] XML/XXE injection

### Business Logic
- [ ] Race conditions (TOCTOU)
- [ ] Integer overflow/underflow
- [ ] Price manipulation
- [ ] Workflow bypass

## CTF patterns

### Common Challenge Categories
| Category | Techniques | Tools |
|----------|-----------|-------|
| Web | SQL injection, XSS, SSRF, deserialization | Burp Suite, sqlmap, ffuf |
| Crypto | RSA attacks, padding oracle, hash collisions | CyberChef, SageMath, hashcat |
| Pwn | Buffer overflow, ROP, format strings, heap | GDB, pwntools, Ghidra |
| Rev | Disassembly, decompilation, anti-debug | Ghidra, IDA, radare2 |
| Forensics | Memory analysis, disk forensics, PCAP | Volatility, Autopsy, Wireshark |
| OSINT | See osint-recon skill | Sherlock, theHarvester |

### Quick pwntools Template
```python
from pwn import *

# Connect
context.binary = elf = ELF('./challenge')
p = remote('target.ctf', 1337)  # or process('./challenge')

# Exploit pattern
payload = flat(
    b'A' * offset,
    p64(rop_gadget),
    p64(target_function),
)
p.sendlineafter(b'> ', payload)
p.interactive()
```

## social engineering awareness

Patterns to test (from SET concepts):
- Phishing email templates (for authorized awareness testing)
- Credential harvesting page detection
- Pretexting scenarios
- USB drop simulation
- Vishing call scripts

**Integration**: CoreMind GAOS output_validator (Layer 4) should detect and block phishing content in agent outputs.

## tool integration map

| Tool | Purpose | the operator's Integration |
|------|---------|---------------------|
| Nmap/Masscan | Port scanning | Bash tool |
| Nuclei | Vulnerability scanning | Bash tool |
| Burp Suite | Web app testing | Manual |
| sqlmap | SQL injection | Bash tool with caution |
| ffuf | Fuzzing | Bash tool |
| Ghidra | Reverse engineering | Manual |
| pwntools | Binary exploitation | Python scripts |

## cross-references

- **osint-recon** skill: OSINT investigation workflows
- **security-review** skill: Code-level security analysis
- **security-auditor** agent: Automated vulnerability scanning
- **security-engineer** agent: Compliance and hardening
- **SECURITY_PLAYBOOK.md**: 36 rules across 8 categories
- **SECURITY_ARSENAL.md**: Tool inventory reference
- **CoreMind GAOS**: 5-layer safety stack for agent security
