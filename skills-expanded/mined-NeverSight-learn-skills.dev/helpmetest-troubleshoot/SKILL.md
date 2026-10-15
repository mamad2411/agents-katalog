---
name: helpmetest-troubleshoot
description: "Triage skill for when something stopped working and you don't know why. Use when user says 'what's wrong', 'it was working a minute ago', 'something broke', 'everything is down', 'why isn't this working', 'tests are failing', 'it stopped working after the deploy', or any vague 'something is off' signal. Gathers the full picture fast — failing tests, health checks, recent code changes, recent deployments — then correlates them to produce a specific diagnosis and handoff to the right fix. Do NOT use for: debugging a known specific test failure (use helpmetest-debugger), bulk-fixing many failing tests (use helpmetest-self-heal), or writing new tests (use helpmetest-test-generator)."
allowed-tools: mcp__helpmetest-*
---

> **Who you are:** If `.helpmetest/SOUL.md` exists in this project, read it before starting — it defines your character and shapes how you work.

> **No MCP?** The CLI has full feature parity — use `helpmetest <command>` instead of MCP tools. See the [CLI reference](../README.md#no-mcp-use-the-cli).

# Troubleshoot

Fast triage when something broke and you don't know what. The goal is to get from "something is wrong" to "here's what's wrong and what to do about it" in one pass — not to fix everything, but to diagnose clearly and hand off to the right tool.

## Philosophy

Don't investigate deeply. Investigate broadly and quickly, then narrow. You're looking for the signal that explains the most failures with the fewest assumptions. Once you have a plausible cause, stop gathering data and state your diagnosis.

## Step 1: Capture What the User Knows

Before gathering data, extract anything the user already mentioned:
- Specific error messages or symptoms → note them, they're your first leads
- A time when it last worked ("worked an hour ago", "broke after the deploy") → anchor for checking recent changes
- A URL, service, or feature ("the checkout page", "the login flow") → narrows scope
- Whether tests, the live site, or both are affected → determines where to look first

## Step 2: Check Current Failure State

Get the full picture of what's failing right now:

```
helpmetest_status({ verbose: true })
```

Look for:
- How many tests are failing? (1-2 suggests a specific breakage; many suggests a systemic change)
- Do the failing tests share a `feature:X` tag? (points to a specific feature regressing)
- Are health checks failing? (points to infrastructure/deployment)
- When did the failures start? (correlates with code changes)

## Step 3: Check Recent Changes

```bash
git log --oneline -10
git diff --stat HEAD~3..HEAD
```

Look for:
- Commits in the last few hours/days (especially deploys, dependency bumps, config changes)
- Which file paths changed → map to feature domains
- Whether the changed domains match the failing test tags

If no git repo or no recent commits, skip this step.

## Step 4: Correlate and Diagnose

Connect what you found in steps 2 and 3. The most common patterns:

| Observation | Likely cause |
|---|---|
| Many tests failing + recent deploy | Deployment broke something systemic (auth, DB, env config) |
| Tests failing in one feature + matching files changed | Regression from a specific code change |
| Health checks failing + server errors in tests | Infrastructure issue (down service, bad config) |
| Tests alternating pass/fail + no recent changes | Test isolation issue (shared state, ordering) |
| All tests failing + no code changes | Environment issue (proxy down, credentials expired, service outage) |
| One test failing + no pattern to other failures | Likely a selector change or timing issue in that specific test |

State your diagnosis explicitly:
```
Diagnosis: [one sentence on most likely cause]

Evidence:
- [X] tests failing, all tagged feature:checkout
- Last commit 2h ago changed checkout/OrderSummary.jsx
- Failure started around the same time as the commit

Confidence: high / medium / low
```

## Step 5: Propose Next Steps

Based on the diagnosis, hand off to the right skill:

**If it's a specific test failure** (1-3 tests, clear error):
→ "Let me debug this with `/helpmetest-debugger`"

**If it's many tests failing after a code change** (systemic regression):
→ "This looks like a regression from [commit]. Use `/helpmetest-self-heal` to fix the affected tests, or roll back the change."

**If it's infrastructure/health** (health checks down, server errors):
→ "The issue looks like it's at the infrastructure level — tests can't reach the app. Check [service/proxy/env]. Once the service is back, run the tests again."

**If it's a deployment issue**:
→ "The deploy at [time] likely introduced this. Consider rolling back [commit], or use `/helpmetest-debugger` on [specific failing test] to confirm."

**If the cause is unclear** (low confidence):
→ "I'm not certain, but the most likely lead is [X]. Want me to dig deeper into [specific area]?"

## Output

A triage report:

```
## Triage Report

**What's failing:** [N tests / health checks / both]
**Feature area:** [which features, if identifiable]
**Recent changes:** [key commits / file areas]

**Diagnosis:** [one sentence]
**Confidence:** high / medium / low

**Next step:** [specific action or skill to use]
```

Keep it short. This is a diagnosis, not an investigation report. If the user needs more detail, they can follow up with the appropriate specialist skill.
