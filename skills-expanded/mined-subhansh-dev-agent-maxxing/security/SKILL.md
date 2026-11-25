# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly. Do NOT open a public GitHub issue for security vulnerabilities. Open a private security advisory via GitHub Security tab.

## Response Timeline

- Acknowledgment: within 48 hours
- Initial assessment: within 7 days
- Fix or mitigation: depends on severity

## Scope

This repository contains Markdown-based skill definitions and UI component patterns.

### Skill files (.md)
- Non-executable prompt definitions
- No API keys, secrets, or credentials should be stored in skill files
- Skills are read by AI agents — never include instructions that could be exploited

### Component patterns
- CSS-only patterns with no executable JavaScript
- No external dependencies or CDN links
- Safe to use in any project

## Best Practices for Contributors

- Never commit API keys, tokens, or credentials
- Never add executable code inside skill Markdown files
- Never include instructions that could be used for prompt injection
- Report suspicious skill definitions that attempt to manipulate agent behavior
- Keep skills focused on their stated purpose
