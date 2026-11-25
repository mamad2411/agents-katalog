# Skill: Supply-Chain Sentinel (Security Auditor)
Source: google/mcp-security-auditor (Vercel/Google Backed)

## Purpose
Specifically scans for "Abandoned Project" flags or "Malware Injection" in npm packages. Rejects low-quality or high-risk dependencies to ensure project safety.

## Core Instructions
1. **Giant-Only/10k+ Policy**: Automatically reject any library with < 10k weekly downloads unless it is from a "Verified Giant" (Google, Meta, Microsoft, Vercel, Amazon).
2. **Slop Factor Scan**: Run a security scan on every new dependency. If a package has a high 'Slop Factor' (unmaintained, poor documentation, or unusual commit patterns), reject it.
3. **Vanilla Alternative**: If a package fails the audit, proactively find or build a vanilla HTML/JS/TS alternative.
4. **Malware Detection**: Scan for active CVEs and recent history of supply-chain attacks.

## Logic Rules
- Reject any dependency that doesn't meet the "Giant" or "10k+" criteria.
- Prioritize custom, high-fidelity implementations over small, unverified third-party utilities.
