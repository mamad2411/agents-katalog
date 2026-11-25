---
name: webapp-sqlmap
description: Automated SQL injection detection and exploitation tool for web application security testing.
metadata:
  version: 0.2.0
  category: offsec
---
# SQLMap - Automated SQL Injection Tool

## Quick Start
```bash
# Basic SQL injection detection
sqlmap -u "http://example.com/page?id=1"

# Test from saved request file
sqlmap -r request.txt

# Detect and enumerate databases
sqlmap -u "http://example.com/page?id=1" --dbs
```

## Workflow
1. **Authorization**: Verify written permission for SQL injection testing.
2. **Identification**: Identify potential injection points (GET/POST/Cookies).
3. **Detection**: Run sqlmap to detect vulnerabilities and DBMS type.
4. **Enumeration**: List databases, tables, and columns to map structure.
5. **Extraction**: Dump authorized data from targeted tables.
6. **Reporting**: Document findings with remediation guidance and clean up artifacts.

## Rules & Constraints
- **RULE-1**: MUST obtain explicit written authorization before any testing.
- **RULE-2**: NEVER dump full databases unless specifically authorized.
- **RULE-3**: Use `--delay` and `--threads` responsibly to avoid crashing production systems.
- **RULE-4**: Document all successful injection techniques and extracted data summaries.

## When to Use
- Testing web applications for SQL injection in authorized assessments.
- Demonstrating the impact of identified SQL injection flaws.
- Automating database enumeration and data extraction.

## When NOT to Use
- Systems without explicit written authorization.
- Network infrastructure testing (firewalls, routers).
- Cloud infrastructure misconfigurations.

## References
- [Skill Manual](references/webapp-sqlmap-manual.md)
- [Official Documentation](https://sqlmap.org/)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
