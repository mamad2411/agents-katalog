---
name: mcp-ship-checklist
description: Pre-publish and release checklist for MCP family packages and control-plane. Use before npm publish, tagging, or claiming client install commands work.
---

# MCP Ship Checklist

## All packages

- [ ] `npm test` (and `npm run check` / integration if present) passes
- [ ] README limitations and coverage claims match code
- [ ] No secrets in repo (`.env`, keys, live SQLite)
- [ ] Protocol versions documented honestly
- [ ] Privacy: no unexpected network/telemetry
- [ ] License present (MIT for public tools)
- [ ] Version bumped intentionally (`0.1.0` MVP until ready)

## Tool servers (npm)

- [ ] Confirm npm **name ownership** before documenting `npx -y <name>` (skip if already published — e.g. security-guard)
- [ ] `files` field / pack contents reviewed (`npm pack --dry-run`)
- [ ] Absolute-path local install still documented as primary **pre-publish** path
- [ ] Example MCP client JSON uses placeholders, not machine-specific secrets
- [ ] Tool descriptions without instruction-injection patterns

## mcp-security-guard extras

- [ ] `npm run build` + `npm test` (+ bench if rules changed)
- [ ] CHANGELOG + PRIVACY.md match new egress
- [ ] Plugin/Cowork: optional keys keep empty defaults when required for load
- [ ] Cloud/Team still fail open; admin actions remain CLI-only
- [ ] Release workflow / Registry / Action inputs still accurate

## Control plane

- [ ] `ADMIN_TOKEN` not default/committed; length ≥32 enforced
- [ ] Production notes: HTTPS proxy, rate limit, volume, backups
- [ ] Product ID list matches all shipped family tools
- [ ] Quota defaults labeled as testing defaults, not commercial pricing

## After publish

- [ ] Update READMEs to enable `npx` / install snippets only for published artifacts
- [ ] Tag release; note breaking MCP protocol or tool schema changes in changelog if present
