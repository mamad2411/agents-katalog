# Skill: Tool Integration

## When to Use
Activate when connecting Claude Code to external tools, APIs, or services. This includes
MCP server setup, API integrations, webhook configurations, and any workflow where Claude
needs to interact with systems beyond the local filesystem.

## Core Principle
Every integration is a contract. Define what it does, what it expects, how it fails,
and how you verify it works. Undocumented integrations become time bombs.

## Process

### 1. Define the Integration
Before writing any code:
- What tool/service are you connecting to?
- What specific operations does Claude need? (read, write, search, execute)
- What authentication is required? (API key, OAuth, service account)
- What are the rate limits, quotas, or costs?

### 2. Design the Interface
Keep integrations simple and scoped.
- One tool per MCP server when possible. Don't create monolithic tool servers.
- Define clear input/output schemas for each operation
- Include error responses -- what does the tool return when it fails?
- Write the tool description so Claude knows when to use it and when not to

### 3. Implement and Test
Build the minimum viable integration first.
- Start with a single operation (e.g., "read" before "read + write + delete")
- Test with real credentials against a sandbox/test account
- Verify error handling: what happens with bad input? Network timeout? Auth failure?
- Log the first successful call as proof of life

### 4. Configure and Document
Make the integration reproducible.
- Store config in `.claude/settings.json` or equivalent
- Document: what it does, how to set it up, what credentials are needed
- Never hardcode secrets -- use environment variables or secure storage
- Add the tool to CLAUDE.md skill triggers so Claude knows it's available

### 5. Monitor and Maintain
Integrations break silently.
- Check tool health at session start if it's critical to workflow
- When an integration fails, diagnose before retrying (auth expired? endpoint changed? rate limited?)
- Keep a fallback plan -- if the tool is down, what's the manual alternative?

## MCP Server Checklist
When building a new MCP server:
- [ ] Server starts without errors
- [ ] Tool descriptions are clear and specific
- [ ] Input validation catches bad parameters before API calls
- [ ] Error messages are actionable ("API key expired" not "request failed")
- [ ] Rate limiting is respected
- [ ] Credentials are loaded from environment, not hardcoded
- [ ] README explains setup in under 5 minutes

## Anti-Patterns
- **God server:** One MCP server with 20 tools. Split by domain.
- **Silent failure:** Tool returns empty result instead of an error. Always surface failures.
- **Retry storms:** Looping retries on a failed API call. Fail fast, diagnose, fix.
- **Missing docs:** Integration works on your machine. Nobody else can set it up.
- **Credential sprawl:** API keys in config files, environment, and hardcoded in 3 places.

## Rules
- Test every integration with real credentials before documenting it as "working."
- Never store API keys, tokens, or secrets in tracked files.
- If an integration costs money per call, add a warning to the tool description.
- When an integration breaks, check the changelog of the external service first.
