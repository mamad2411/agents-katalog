---
name: metamask-openclaw-desktop-security-analysis
description: Analyze and understand the security risks of the Metamask Openclaw desktop executable distribution
triggers:
  - "what is metamask openclaw desktop"
  - "analyze this metamask desktop client"
  - "is this metamask exe safe"
  - "check metamask openclaw security"
  - "evaluate this web3 desktop tool"
  - "scan this metamask windows installer"
  - "investigate openclaw project"
  - "verify metamask desktop download"
---

# Metamask Openclaw Desktop - Security Analysis Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## ⚠️ CRITICAL SECURITY WARNING

This project exhibits **EXTREME RED FLAGS** indicating a **CRYPTOCURRENCY SCAM** or **MALWARE DISTRIBUTION**. DO NOT download, install, or execute any files from this repository.

## Threat Indicators

### 1. **Impersonation of Legitimate Service**
- Metamask is a legitimate browser extension wallet with NO official "Openclaw" product
- Uses Metamask branding without authorization
- "Openclaw" is not a recognized Metamask feature or official product

### 2. **Malicious Distribution Pattern**
- Distributes pre-compiled `.exe` files through GitHub releases
- No source code provided despite claiming to be "open-source"
- Claims "C#" language but provides no C# code in repository
- Apache-2.0 license claimed without actual code to license

### 3. **Social Engineering Tactics**
- Emphasizes "no technical knowledge required"
- Pressure to "double-click .exe" immediately
- Promises "easy setup" to bypass user scrutiny
- Fake trust indicators (badges, star count manipulation)

### 4. **Suspicious Repository Characteristics**
- Created very recently (June 2026 - future date indicates test/fake repo)
- Rapid star accumulation (95 stars in 1 day = bot manipulation)
- Zero forks, zero issues (no genuine community)
- Generic topic spam for SEO manipulation

### 5. **Technical Impossibility Claims**
- Desktop Metamask requires browser extension architecture
- Claims "isolated framework" without technical documentation
- "100% self-contained" contradicts need for "Web3 syncing"

## Attack Vector Analysis

### Likely Malware Functions

```csharp
// What the executable LIKELY contains (DO NOT RUN):

// 1. Credential theft
async Task StealWalletData() {
    // Scrapes browser extension data
    // Extracts seed phrases from:
    // - %APPDATA%\Google\Chrome\User Data
    // - %APPDATA%\Mozilla\Firefox\Profiles
    // Exfiltrates to attacker C2 server
}

// 2. Clipboard monitoring
void MonitorClipboard() {
    // Watches for cryptocurrency addresses
    // Replaces with attacker's addresses
    // User sends funds to wrong destination
}

// 3. Keylogging
void CaptureKeystrokes() {
    // Records passwords and seed phrases
    // Targets wallet unlock attempts
}

// 4. Session hijacking
void StealActiveSessions() {
    // Captures Web3 provider sessions
    // Drains wallets while authenticated
}
```

## Safe Investigation Approach

### Static Analysis Only (Never Execute)

```bash
# If you MUST analyze (use isolated VM only):

# Check file hash
certutil -hashfile suspicious.exe SHA256

# Submit hash to VirusTotal (do not upload file)
# https://www.virustotal.com/

# Use strings analysis (WSL/Linux tools)
strings suspicious.exe | grep -i "http\|wallet\|seed\|private"

# Analyze with sandboxed tools
# - any.run
# - hybrid-analysis.com
# - joe sandbox
```

### Environmental Variables Check

```bash
# The malware likely exfiltrates to:
# - Telegram bots
# - Discord webhooks  
# - Attacker-controlled APIs

# Check for hardcoded endpoints:
strings suspicious.exe | grep -E "(https?://|api\.|\\.com|\\.ru)"
```

## Legitimate Metamask Usage

### Official Metamask Installation

```bash
# Browser Extension (OFFICIAL METHOD)
# 1. Visit ONLY: https://metamask.io
# 2. Install from official browser stores:
#    - Chrome Web Store
#    - Firefox Add-ons
#    - Brave Browser

# Never install Metamask from:
# - Third-party websites
# - GitHub executables
# - Desktop applications claiming Metamask affiliation
```

### Actual Metamask SDK (Legitimate)

```javascript
// Official Metamask SDK for dApps (JavaScript/TypeScript)
import MetaMaskSDK from '@metamask/sdk';

const sdk = new MetaMaskSDK({
  dappMetadata: {
    name: 'My dApp',
    url: window.location.href,
  },
});

const ethereum = sdk.getProvider();

// Request account access
const accounts = await ethereum.request({ 
  method: 'eth_requestAccounts' 
});

console.log('Connected account:', accounts[0]);
```

## Protection Measures

### If Already Executed

```bash
# IMMEDIATE ACTIONS:

# 1. Disconnect from internet
# 2. Transfer crypto to new wallet (from different device)
# 3. Change all passwords (from different device)
# 4. Full system reinstall recommended

# 5. Scan with multiple antivirus tools:
# - Windows Defender Offline Scan
# - Malwarebytes
# - Kaspersky Rescue Disk
```

### Environment Variable Security

```bash
# Never store sensitive data in environment variables
# on a potentially compromised system

# Safe practice (on clean system):
# Use hardware wallets (Ledger, Trezor)
# Never expose: PRIVATE_KEY, SEED_PHRASE, MNEMONIC
```

## Detection Patterns

### Repository Red Flags Checklist

```yaml
indicators:
  - executable_only_release: true  # No source code
  - cryptocurrency_keywords: true  # wallet, metamask, binance
  - pressure_tactics: true         # "quick", "easy", "double-click"
  - fake_stars: true               # Impossible growth rate
  - impersonation: true            # Mimics legitimate brand
  - recent_creation: true          # <1 week old
  - zero_community: true           # No real users/issues
  
threat_level: CRITICAL
recommendation: AVOID_COMPLETELY
```

## Reporting

```bash
# Report malicious repository:

# 1. GitHub Security
# https://github.com/contact/report-abuse

# 2. Metamask Official
# security@metamask.io

# 3. Anti-Phishing Working Group
# https://apwg.org/
```

## Conclusion

This is **NOT** a legitimate Metamask tool. It is a **scam designed to steal cryptocurrency**. The complete absence of source code, combined with aggressive exe distribution and brand impersonation, confirms malicious intent.

**Action Required:** Report this repository and warn others in the community.
