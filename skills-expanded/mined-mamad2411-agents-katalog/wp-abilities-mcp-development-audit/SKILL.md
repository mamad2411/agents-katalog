---
name: wp-abilities-mcp-development-audit
description: Audits WordPress Abilities and MCP Adapter source patterns without executing the project. Use when inventorying registrations, exposure flags, permission callbacks, annotations, custom servers, dependency constraints, or possible secrets.
---

# Static Audit

## Process

1. Run the scanner with `--help`.
2. Scan the narrowest relevant root.
3. Review inventory findings before treating warnings as defects.
4. Inspect each registration block, permission callback, schema, annotation, and exposure flag manually.
5. Compare custom server calls with the installed MCP Adapter release.
6. Review Composer and client configuration for version and secret handling.
7. Run runtime tests; static scanning cannot prove authorization or behavior.
8. Follow `workflows/audit-abilities-mcp-workflow.md`.
9. Use `resources/scanner-finding-reference.md`.

## Commands

```powershell
python .\.agents\plugins\wp-abilities-mcp-development\skills\wp-abilities-mcp-development-audit\scripts\abilities-mcp-scan.py --root . --format text
```

```powershell
python .\.agents\plugins\wp-abilities-mcp-development\skills\wp-abilities-mcp-development-audit\scripts\abilities-mcp-scan.py --root . --format json --fail-on warning
```
