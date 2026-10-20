---
name: product-verification
description: >
  Drive the running product and verify it works end-to-end. Use this skill
  after a deploy, before a release, or when the user says "verify", "smoke
  test", "does it work", "test the flow", "check staging", "end-to-end test",
  or "drive the product". Also use when the user wants to verify a specific
  user journey (signup, checkout, onboarding, upgrade). Even if the user just
  says "make sure it works", use this skill — unit tests pass doesn't mean
  the product works.
---

# Product Verification

You verify that the product works by driving it like a real user. Unit tests
check code. You check the product.

Read `config.json` in this skill directory for project-specific verification
config (endpoints, credentials, flows to test). If it doesn't exist or says
NOT_CONFIGURED, ask the user to set it up first (see Setup section below).

## What you verify

Identify the critical user journeys for this project and drive each one.
Common patterns — adapt to what the project actually does:

**Web app / Landing page**: Load the page, verify key elements render, check
all navigation links, verify forms submit, check responsive breakpoints.

**API**: Hit each public endpoint with valid and invalid inputs. Verify status
codes, response shapes, and error messages.

**Discord/Slack bot**: Send real commands to a test server. Verify responses,
embeds, and error handling.

**Billing flow**: Drive signup → plan selection → checkout → verify access
changes. Use test credentials.

**Onboarding**: Complete the first-run experience. Verify each step is
reachable and functional.

For each journey, capture: what you tested, what happened, and whether it
matches expectations.

## How to verify

Use the tools that match the project's technology. The skill doesn't prescribe
specific tools — choose based on what's available and appropriate:

- `curl` or `requests` for API endpoints
- Playwright or Puppeteer for browser-based flows
- Discord/Slack API for bot commands
- Shell scripts for CLI tools
- Direct database queries to verify state changes

If verification scripts exist in `scripts/`, use them. If you find yourself
writing the same verification code twice, save it as a script for next time.

## Output

Save results to the location the caller expects (e.g., `monitoring/deploy-validation-*.md`
if called from a scheduled task, or sprint directory if called during a sprint).

```markdown
# Product Verification — [date or sprint]

## Environment
[staging/production URL, version deployed]

## Flows tested

### [Flow name] — ✅ Pass / ❌ Fail
- **Steps**: [what was done]
- **Expected**: [what should happen]
- **Actual**: [what happened]
- **Evidence**: [response code, screenshot path, output snippet]

## Summary
X/Y flows passing
[Any critical failures that need immediate attention]
```

## Setup

If this is the first run, create `config.json` in this skill directory:

```json
{
  "project_type": "web|api|bot|cli",
  "staging_url": "https://...",
  "test_credentials": {
    "note": "Use env vars for secrets, not this file"
  },
  "critical_flows": [
    "signup → first action",
    "upgrade → verify access",
    "core command → response"
  ]
}
```

Ask the user which flows are critical. Don't guess — every project is different.

## Gotchas
- Unit tests passing doesn't mean the product works. A deploy can break things that tests don't cover.
- Always verify on the actual deployed environment, not localhost.
- If you can't access the environment (auth, network), say so immediately — don't fake results.
- Check what the USER sees, not what the code does. An API returning 200 with wrong data is worse than a 500.
- Save verification scripts for reuse. The second run should be faster than the first.

## Memory
Append results to `${CLAUDE_PLUGIN_DATA}/verification.log` if available,
otherwise to `tasks/verification-history.log`:
```
[YYYY-MM-DD] [env] X/Y flows passing — [clean/issues: brief description]
```