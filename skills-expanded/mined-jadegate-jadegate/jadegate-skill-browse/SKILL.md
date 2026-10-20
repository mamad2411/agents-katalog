---
name: jadegate-skill-browse
description: Browse and search the JadeGate verified skill registry with 150+ security-checked skills for MCP servers.
---

# Skill Registry Browser

Browse and search the JadeGate verified skill registry with 150+ security-checked skills for MCP servers.

## When to Use

- User wants to find available MCP skills
- User asks what skills JadeGate offers
- User wants to search for a specific type of skill

## Usage

```bash
jadegate list                          # Browse all 150+ skills
jadegate list github                   # Search by keyword
jadegate list --category network       # Filter by category
```

## Skill Categories

- **Network**: DNS lookup, IP geolocation, HTTP health check, WHOIS, SSL cert check
- **Data**: CSV analysis, JSON transform, PDF parsing, QR code generation
- **Git/GitHub**: Clone repo, diff summary, create issue
- **Communication**: Slack, Telegram, Discord, email
- **Web**: Search, screenshot, content extraction, RSS feed
- **System**: Docker, SSH remote exec, SQLite query
- **Security**: Hash verification, base64 encoding
- **NLP**: Text sentiment, translation
