---
name: danikuse
description: Computer and browser use, split by surface. Use when the user invokes /danikuse, /danikuse-my (their own Brave), /danikuse-agent (the agent's browser), or /danikuse-desktop (Windows desktop with visible cursor), or asks for any browser or desktop work. Pick the surface skill that matches the surface named; /danikuse alone means read this index and choose.
---

# Danikuse — three surfaces, one module

Danikuse is one CLI (`bin/danikuse.mjs`) behind three named surfaces. The user chooses the surface by command name; flags never choose it.

| Surface | Skill | CLI | What it is |
|---|---|---|---|
| `/danikuse-my` | `skills/danikuse-my` | `danikuse my <verb>` | The user's own Brave: their tabs, their logins, always visible |
| `/danikuse-agent` | `skills/danikuse-agent` | `danikuse agent <verb>` | The agent's own browser: Brave engine, separate light profile, visible by default, `--hide` for background |
| `/danikuse-desktop` | `skills/danikuse-desktop` | `danikuse pc <args>` | Windows desktop apps with a visible cursor |

Every CLI call returns one JSON object `{status, browser, action, screenshot, error, next, durationMs, runDir}`. Act on `status` and `next`; never claim success without `ok` and, for visual claims, a screenshot in the run folder.

Standing rule: no user login needed → `/danikuse-agent`, never Personal Brave. Personal Brave steals screen focus; it is only for tasks that truly need the user's session.

## Modes (all surfaces)

Graded like the OpenAI computer-use confirmations policy, in Danikuse terms:

- **No confirmation**: reading, navigation, cookie consent, downloads, drafts.
- **Pre-approval works**: login to the site the user named, uploads, file moves — allowed when the user's opening request explicitly covers the specific data and destination; otherwise confirm at action time.
- **Always confirm at action time** (even if pre-approved): submit that transmits data, pay, publish, delete, create accounts or keys, save passwords, solve captchas, install software or extensions, change security or privacy settings.
- **Hand-off required**: final password change, bypassing HTTPS or paywall barriers — the user does it, not the agent.
- **Autonomous Mode** starts only on an explicit user instruction such as "do it fully yourself", covers one task, then expires. It waives the pre-approval tier only; always-confirm and hand-off still hold.
- A task defeated by a captcha after the persistent profile, the Personal Brave session, and your own attempts is `captcha-blocked` (report via `danikuse agent report-block`). Report it; never report it as done.
- Honest limit: modes are enforced by the agent following this skill, not by the CLI. The CLI records evidence and statuses; it does not classify page actions. Never present mode gating as a code guarantee.

## Standing rules

- Screenshots and run folders stay local; never commit them or any `.env` key.
- Zero paid keys are required. Firecrawl beyond keyless, captcha solvers, and Skyvern are opt-in layers with their own decisions; do not wire them in unasked.
- The lead agent orchestrates and owns the result. Workers of the lead's own harness (subagents, AGY) are development help, not part of Danikuse; their output is input, never the verdict.
