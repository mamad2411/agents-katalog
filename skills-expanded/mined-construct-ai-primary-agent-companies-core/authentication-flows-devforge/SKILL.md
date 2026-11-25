---
name: authentication-flows-devforge
description: >
  Use when authentication issues occur including OAuth to API key migration, session
  caching problems, CLI auth in authenticated deployment mode, or agent 401 errors.
  Handles Anthropic OAuth expiration, API key configuration, and auth token refresh.
---

# Authentication Flows - DevForge AI

## Overview
Handles authentication and authorization issues in the Paperclip codebase. Resolves OAuth-to-API-key migration issues, session caching problems, CLI authentication in authenticated deployment mode, and agent run 401 errors caused by stale auth tokens.

## When to Use
- When agents return 401 with "OAuth token has expired" after API key is configured
- When CLI commands fail with "Unauthorized" in authenticated deployment mode
- When session ID is reused across runs with stale OAuth tokens
- When `deploymentMode: "authenticated"` breaks CLI heartbeat/agent-list commands
- **Don't use when:** It's an API permissions issue (use gatekeeper-devforge-access-control)

## Core Procedures
### Auth Migration Workflow
1. **Identify Auth Method** - Check config.json for llm.provider, llm.apiKey, OAuth settings
2. **Check Session Cache** - Look for cached OAuth sessions in instance data
3. **Clear Stale Sessions** - Remove cached auth sessions that reference expired tokens
4. **Verify API Key** - Confirm API key is correctly set and valid via doctor check
5. **Test Agent Run** - Trigger agent run and verify API key is used (not OAuth)
6. **CLI Auth Support** - Add email/password or session token support for authenticated mode

### Common Auth Issues
- OAuth session cached in `~/.paperclip/instances/*/sessions/` — clear to force API key use
- CLI has no auth credential passing in authenticated mode — needs `--email/--password` flags
- Agent JWT secret not set — causes 401 on all agent runs

## Agent Assignment
**Primary Agent:** devcore-devforge-core-development
**Company:** DevForge AI
**Role:** Authentication Specialist
**Reports To:** devcore-devforge-core-development
**Backup Agents:** gatekeeper-devforge-access-control, interface-devforge-api-integration

## Success Metrics
- API key auth works immediately after configuration
- No OAuth session reuse after API key switch
- CLI works in authenticated mode with proper credentials
- Agent runs succeed with configured auth method

## Error Handling
- **Error:** API key invalid after config
  **Response:** Validate key format, check provider, test with direct API call
- **Error:** CLI auth credentials not available
  **Response:** Add credential storage, env var support, or interactive prompt

## Cross-Team Integration
**Gigabrain Tags:** devforge, authentication, oauth, api-key, session, cli-auth
**Related Skills:** devcore-devforge-core-development, gatekeeper-devforge-access-control, interface-devforge-api-integration
**Last Updated:** 2026-04-07