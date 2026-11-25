---
name: scam-guards
description: >
  Real-time AI agent security guardian that protects OpenClaw from
  scams, malware, and prompt injection attacks. Scan ClawHub skills
  before installing to detect malicious patterns (341+ known threats).
  Verify URLs, domains, and crypto wallet addresses for phishing and
  fraud. Monitor agent behavior for psychological manipulation
  (Cialdini P1-P6) and agent-to-agent social engineering. Generate
  SHA-256 legal evidence chains for suspicious interactions. Works
  as a continuous bodyguard, not just a one-time scanner.
  "When OpenClaw works, Scam Guards watches."
  Triggers: "is this safe", "scan skill", "check URL",
  "verify wallet", "security audit", "detect scam",
  "protect agent", "scan for malware", "check this link".
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: ["python3", "curl"]
---

# Overview
Scam Guards is a real-time security engine designed to protect AI agents and their users within the ClawHub ecosystem. Unlike passive scanners, Scam Guards operates as a continuous bodyguard, providing deep behavioral analysis and evidence collection for every suspicious interaction.

# Core Capabilities

## 1. Skill Malware Scanning
Scans ClawHub skills before installation to identify malicious code, unauthorized API calls, and known threat patterns.
**Run:** `python3 {baseDir}/scripts/scan_skill.py <skill_name_or_path>`

## 2. Phishing & URL Verification
Real-time domain reputation check and phishing detection for any URLs processed or suggested by an agent.
**Run:** `python3 {baseDir}/scripts/verify_url.py <url>`

## 3. Crypto Wallet Audit
Checks crypto wallet addresses against global blacklists and known fraudulent patterns.
**Run:** `python3 {baseDir}/scripts/check_wallet.py <wallet_address>`

## 4. Real-time Behavior Monitoring (PHI Lite)
Analyzes agent interactions for psychological manipulation tactics (Cialdini's Principles) and social engineering patterns.
**Run:** `python3 {baseDir}/scripts/monitor_agent.py --input <text_content>`

## 5. Legal Evidence Chain
Generates SHA-256 hashed audit trails for security incidents, ensuring data integrity for potential legal or reporting needs.
**Run:** `python3 {baseDir}/scripts/evidence_chain.py --event <event_data>`

# When to Use
Activate Scam Guards when:
- Evaluating a new skill for installation.
- An agent requests sensitive data or provides a suspicious link.
- Dealing with financial transactions or crypto wallet addresses.
- You suspect psychological manipulation or unusual agent behavior.
- You need a secure, tamper-proof record of a security interaction.

# Safety and Privacy
Scam Guards is designed with a "Privacy First" architecture:
- **No Permanent Recording**: Analysis is performed in memory; no chat logs are permanently stored unless explicitly requested by the user for an evidence chain.
- **Local Shield Layer**: Pattern matching and initial analysis occur locally within the skill environment.
- **Transparency**: Every detection event is reported with a clear rationale and taxonomy.

# References
Detailed security documentation and taxonomies are available in the repository:
- [Scam Taxonomy](file://{baseDir}/references/scam-taxonomy.md)
- [Known Threat Patterns](file://{baseDir}/references/known-threats.md)
- [PHI Dimensions Summary](file://{baseDir}/references/phi-dimensions.md)
- [Response Playbook](file://{baseDir}/references/response-playbook.md)
