---
name: mcp-agent-security-auditor
description: Red-team security auditing skill for AI Agents, Model Context Protocol (MCP) servers, hook migration scripts, and Firebase/Firestore security rules. Use when auditing repositories for bug bounties or pre-release security reviews.
---

# AI Agent & MCP Red-Team Security Auditor Skill
> Author: **HM Shihabuddin Jashory (Shihab)** — [Vision Flow](https://visionflowgroup.com)

## Mandatory Audit Checklist for AI Agents & MCP Servers
1. **Cross-Scope & Resolved `${ENV_VAR}` Persistence Check (`CWE-312`)**:
   - Inspect all config/hook migration commands (`settings.setValue`, `writeFileSync`) to ensure they read raw `originalSettings` for the target scope rather than `settings.merged` (where `${ENV_VAR}` secrets and global user hooks are already expanded in memory).
2. **MCP Tool Execution Sinks (`CWE-78`)**:
   - Flag any MCP tool handler passing model-controlled strings into `child_process.exec`, `execSync`, or Python `subprocess` with `shell=True`.
3. **SSRF & Local File Inclusion in Agent Tools (`CWE-918` / `CWE-22`)**:
   - Verify URL-fetching tools block `127.0.0.1`, `localhost`, `169.254.169.254`, and RFC1918 ranges, and file tools enforce `os.path.realpath()` prefix containment.
