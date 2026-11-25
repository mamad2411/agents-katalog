---
name: test
version: 0.1.1
description: |
  Designs and runs approved automated tests, including Playwright or Selenium when enabled by policy.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Test Automation

Designs and runs approved automated tests, including Playwright or Selenium when enabled by policy.

## Steps

1. Confirm the behavior under test and the target layer.
2. Prefer existing local test frameworks before adding a new one.
3. Choose the smallest deterministic test type that proves the behavior.
4. Use Playwright for web UI/browser flows only when the active policy enables browser automation.
5. Use Selenium only when the project already depends on it or the profile explicitly chooses it.
6. Avoid public websites, cookie import, credential reads, and uncontrolled scraping.
7. Report the command, expected result, actual result, and artifacts.

## Test Types

- Unit tests.
- Integration tests.
- Contract tests.
- API tests.
- Data pipeline tests.
- SQL verification tests.
- Playwright UI tests.
- Selenium UI tests.

## Browser Automation Rules

- Browser automation is disabled by default.
- Tests must target local, staging, or approved internal environments.
- Test credentials must come from approved project configuration, not prompt text.
- Screenshots, traces, and logs must avoid secrets and raw customer data.
- Public scraping and public tunnel usage are forbidden by default.

## Extended Guidance

When choosing test strategy, sharding, Playwright, Selenium, or CI layout, read
`test/sections/automation-matrix.md`.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
