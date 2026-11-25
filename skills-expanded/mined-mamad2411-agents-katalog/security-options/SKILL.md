---
name: security-options
description: >
  Routes a security question to the right tool. Not for a concrete CI-mirror
  scan or an OWASP WSTG/DAST walkthrough — those trigger appsec-scan and
  appsec-dast-sim directly. Use for general asks: "what security tools do we
  have", "what are my security options", a deep vulnerability hunt with
  patches, automatic warnings while editing plus end-of-turn LLM review,
  fuzzing / Semgrep / CodeQL / crypto review, or vetting a third-party skill
  or plugin before installing it. Do NOT activate for "SAST scan", "dependency
  scan", "secret scan", "container scan", "scan before I push" (appsec-scan)
  or "DAST scan", "OWASP WSTG check", "audit my API", "is my login secure"
  (appsec-dast-sim).
---

# Security Options — Routing

Not a scanner. Read the table, then hand off to the tool that fits.

| Need | Tool | How to get it |
|---|---|---|
| CI-mirror scanners (SAST/dependency/secret/container) before push | `appsec-scan` | In `appsec`, an essentials dependency |
| OWASP WSTG design-time review | `appsec-dast-sim` | In `appsec`, an essentials dependency |
| Review of the current diff | built-in `/security-review` | Ships with Claude Code |
| Deep vulnerability hunt with patches | `claude-security` | Installed with essentials. Claude models only — proprietary Anthropic licence |
| Automatic warnings while editing + end-of-turn LLM review | `security-guidance` | Installed with essentials. Needs internet and the Anthropic API (sends each turn that changed code to the Anthropic API) |
| Fuzzing, Semgrep/CodeQL rule authoring, crypto review | `trailofbits-skills` | `/plugin install trailofbits-skills@platform-claude-marketplace` |
| Vetting a third-party skill/plugin before installing it | `skill-scanner` | `/plugin install skill-scanner@platform-claude-marketplace` |
