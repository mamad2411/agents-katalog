---
name: webapp-nikto
description: Web server vulnerability scanner for identifying security issues, misconfigurations, and outdated software.
metadata:
  version: 0.2.0
  category: offsec
---
# Nikto Web Server Scanner

## Quick Start
```bash
# Scan single host
nikto -h http://example.com
# Scan with SSL
nikto -h https://example.com
```

## Workflow
1. **Authorization**: Obtain written permission and verify target scope.
2. **Reconnaissance**: Identify target web servers, ports, and protocols.
3. **Basic Scan**: Run Nikto with default settings or common flags (`-h`, `-p`, `-ssl`).
4. **Advanced Assessment**: Use tuning options (`-Tuning`) and plugins for depth.
5. **Output & Analysis**: Export results (`-o`, `-Format`) and categorize findings by impact.
6. **Reporting**: Document vulnerabilities and recommended remediations.

## Rules & Constraints
- **AUTH-1**: NEVER scan without explicit authorization.
- **OPSEC-1**: Nikto is noisy; expect detection by IDS/WAF.
- **SAFE-1**: Be mindful of scan impact on server performance; use `-Pause` if needed.
- **CLEAN-1**: Ensure no temporary artifacts remain on the target system.

## When to Use
- Identifying common misconfigurations and default files.
- Detecting outdated server software and known vulnerabilities.
- Performing compliance scans for web server hardening.

## When NOT to Use
- When stealth is a priority (use a quieter tool).
- Production environments where excessive logs are prohibited.
- When deep application logic testing is required (use a DAST tool).

## References
- [Skill Manual](references/webapp-nikto-manual.md)
- [Nikto Official Documentation](https://cirt.net/Nikto2)
- [Nikto GitHub Repository](https://github.com/sullo/nikto)
