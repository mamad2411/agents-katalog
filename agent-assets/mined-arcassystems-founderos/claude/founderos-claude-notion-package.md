# Founder OS - Notion Package (Plan B sub-project CLAUDE.md)

## What this is
Public-facing Notion Package that non-technical founders can duplicate and start using the same day. Zero terminal required. Runs on a Claude subscription plus a free Notion account.

## What this is NOT
Not a workflow engine. Not a webhook server. Not a cloud service. Not the local Claude Code plugin. The local plugin lives in the public FounderOS repo root.

## Who this is for
A non-developer founder. Uses Claude and voice input (Wispr Flow or similar). Already lives in Notion or willing to. Runs the business alone or with one or two people. Day is chopped into thirty-minute pieces. Has tried productivity templates that quietly stopped getting used by week three.

## The two drivers (positioning)
Claude thinks. Wispr Flow speaks. Founder OS is the markdown layer in between that evolves with the user.

## File tree (target)
notion-package/
  CLAUDE.md                   <- you are here
  README.md                   <- public-facing intro to the package
  pages/                      <- Notion-page-ready markdown sources
    00-landing.md
    01-quickstart.md
    05-current-limits.md
  system-prompts/
    founder-os-project-prompt.md  <- Claude Project system prompt that runs the routing loop against Notion via the connector
  databases/
    schema.md                 <- Notion DB schemas (Profiles, Decisions, Priorities, Clients, Brain Log, Flags)
  announce/
    README.md                 <- launch and sharing notes
  test/
    sample-transcript.md      <- canned test transcript for first-run demo
    expected-routes.md        <- expected output for the sample

## Self-update protocol
This project must be able to evolve itself over time. Pattern:
1. Before adding any new file, read this CLAUDE.md and confirm scope fit.
2. After every session that modifies notion-package/, append a dated entry to the "Session log" section at the bottom of this file with: date, what changed, why, commit SHA.
3. If you are a new Claude session picking up this project cold, read this file first, then scan the most recent session log entries at the bottom of this file before changing anything.
4. Never add banned words or ARCAS leakage. Run pre-commit guard before suggesting writes.
5. If scope creep appears (someone asks to add workflows, webhooks, crons), refuse. Point at "What this is NOT" above. Direct them to the terminal version.

## Voice and style rules for this sub-project
- Plain English. Non-native English speakers are the primary audience.
- Calm founder authority. No hype. No emojis. No em dashes. No banned words.
- "The team" not "my team" when referring to founders using the package.
- Frame benefits as consequences of behavior, not aspirations.

## Session log
(appended by future sessions)

- 2026-04-22: Scaffold created. No pages, prompts, databases, or announce copy yet. Commit SHA: (set at commit time).
