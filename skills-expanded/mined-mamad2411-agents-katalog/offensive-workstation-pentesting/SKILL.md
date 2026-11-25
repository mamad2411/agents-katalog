---
name: offensive-workstation-pentesting
description: Safely select, explain, and use the offensive workstation's installed security tools for authorized testing. Use whenever the user mentions CyberStrike, cyberstrike commands or flags, HackBrowser, CyberStrike agents, models, providers, authentication, configuration, permissions, sessions, skills, MCP, Bolt, or asks Hermes to explain or run CyberStrike.
metadata:
  hermes:
    tags: [security, pentesting, reconnaissance, web, authorized-testing]
    category: cybersecurity
---

# Offensive Workstation Pentesting

## When to use

Load this skill when the user asks Hermes to inventory, select, explain, combine, or operate the security tools installed in this image for an authorized assessment.

## Mandatory safety procedure

Before active testing, load `references/SAFETY.md`, establish written scope, and confirm that the user owns the target or has explicit authorization. Container privilege is a technical capability, not permission. Default to passive and non-destructive checks.

## Workspace contract

Set `ENGAGEMENT` and keep targets, raw results, evidence, and reports under `/workspace`. Never write target data into immutable `/opt` paths. Never place credentials in commands or reports.

```bash
export ENGAGEMENT=owned-application-review
export OUTPUT_DIR="/workspace/reports/$ENGAGEMENT"
mkdir -p "$OUTPUT_DIR"/{raw,normalized,evidence,final}
```

## Routing

1. For every ethical-hacking or pentesting request, first run `workstation-kb search "$USER_INTENT" --limit 8`, then open only the highest-ranked relevant local sources. See `references/LOCAL-RAG.md` for the complete corpus, authority order, persistence, and retrieval procedure.
2. For every CyberStrike-related request, additionally run `cyberstrike-kb search "$USER_INTENT" --limit 6`, then load `references/cyberstrike/INDEX.md` and the highest-ranked matching concise topic page. Check installed help before using a retrieved command or flag. For informational questions, answer from local RAG without invoking `cyberstrike run` or requiring a CyberStrike model-provider credential. For live chat or session work, use the `cyberstrike_*` MCP tools described in `references/cyberstrike/VERIFIED-API.md`; do not invent HTTP routes.
3. Load `references/TOOL-INDEX.md` if another required command is not already known.
4. Load exactly one relevant `references/tools/<tool>.md` guide.
5. Load the matching workflow only when chaining tools:
   - Recon and assets: `references/workflows/reconnaissance.md`, `references/workflows/dns-subdomains.md`, `references/workflows/enrichment.md`
   - Network: `references/workflows/network-mapping.md`
   - HTTP/routes: `references/workflows/http-discovery.md`, `references/workflows/content-fuzzing.md`
   - URLs/JavaScript: `references/workflows/url-javascript.md`
   - Templates/CMS: `references/workflows/template-scanning.md`, `references/workflows/cms-testing.md`
   - XSS/injection: `references/workflows/xss.md`, `references/workflows/injection.md`
   - Git/secrets: `references/workflows/git-secrets.md`
   - Browser/media: `references/workflows/browser-screenshots.md`
   - CyberStrike delegation: `references/cyberstrike/INDEX.md`, `references/workflows/cyberstrike-orchestration.md`
   - Evidence: `references/workflows/reporting-pipelines.md`
   - Converted PDF guide index: `references/my-guides/converted-source-index.md`
   - Web pentest methodology: `references/my-guides/web-pentest-guide.md`
   - Bug bounty methodology: `references/my-guides/bug-bounty-methodology.md`
   - Recon and fuzzing: `references/my-guides/recon-and-fuzzing.md`
   - API security testing: `references/my-guides/api-security-testing.md`
   - Authentication and access control: `references/my-guides/auth-access-control-testing.md`
   - JWT security testing: `references/my-guides/jwt-security-testing.md`
   - SQL injection testing: `references/my-guides/sql-injection-cheatsheet.md`
   - XSS testing: `references/my-guides/xss-cheatsheet.md`
   - LDAP injection testing: `references/my-guides/ldap-injection-testing.md`
   - File upload testing: `references/my-guides/file-upload-testing.md`
   - Deserialization testing: `references/my-guides/deserialization-testing.md`
   - WordPress and CMS testing: `references/my-guides/wordpress-cms-testing.md`
   - Mobile application testing: `references/my-guides/mobile-application-testing.md`
   - AWS cloud review: `references/my-guides/aws-cloud-security-review.md`
   - Network and service testing: `references/my-guides/network-service-testing.md`
   - SMTP testing: `references/my-guides/smtp-testing.md`
   - DoS resilience planning: `references/my-guides/dos-resilience-testing.md`
   - Payload library usage: `references/my-guides/payload-library.md`
   - Active Directory lab review: `references/my-guides/active-directory-lab-review.md`
   - Tunneling and port forwarding: `references/my-guides/tunneling-port-forwarding.md`
   - LLM application security: `references/my-guides/llm-application-security-testing.md`
   - Secure coding review: `references/my-guides/secure-coding-review.md`
   - Lab environment building: `references/my-guides/lab-environment-building.md`
   - Linux and Windows command reference: `references/my-guides/linux-windows-command-reference.md`
   - Certification study map: `references/my-guides/certification-study-map.md`
   - Tool selection: `references/my-guides/tool-selection-reference.md`
6. Consult `references/ASSETS.md` for wordlists/templates and `references/TROUBLESHOOTING.md` for failures.

## Execution rules

- Read the installed help snapshot before advanced use; tools track current releases and flags can change.
- Use the loopback-only CyberStrike MCP bridge for live sessions. A normal AI reply needs a configured CyberStrike model provider; RAG lookup and `no_reply=true` transport checks do not.
- Show the user the proposed active-scan scope and rate before high-volume execution.
- Use harmless markers and test accounts. Exclude destructive, persistence, credential-attack, denial-of-service, and third-party testing.
- Preserve raw output and report only manually verified findings with redacted evidence.

## Verification

```bash
check-tools
check-knowledge
workstation-kb verify
cyberstrike-kb verify
COLUMNS=240 hermes skills list | grep offensive-workstation-pentesting
```
