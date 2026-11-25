---
name: team-ai-quota
description: Query your team's Team AI Quota server for AI coding quota. Use when the user asks which Claude Code, Codex, Gemini or other AI coding account to use now, how much quota is left, which accounts will run out or waste quota, which machine uses which account, or how much weekly quota went unused. Runs the read-only `taq` CLI.
---

# Team AI Quota

Read-only access to the team's quota dashboard through the `taq` CLI (npm package `team-ai-quota`, Node 18+).
Nothing here changes any account or setting.

## Setup (once)

1. Check whether it is already set up: `npx -y team-ai-quota config`. If it prints a url and `key: set`, skip to "Commands".
2. Otherwise ask the user for their dashboard link (the URL they open in the browser, it ends with `?key=...`) and run:
   `npx -y team-ai-quota login "<link>"`
   The URL and key are stored in `~/.config/team-ai-quota/config.json` (mode 600).
3. `npx -y team-ai-quota health` should print `ok`.

Never print, log, echo or commit the key. `taq config` shows the key only as "set". Do not paste the dashboard link into files or messages.

## Commands

Add `--provider claude|agy|codex|gemini|copilot|cursor` (default `claude`) and `--json` for machine-readable output.

- `taq best` — the account to use now, plus the next best. Exit code 3 means no account is eligible (all locked, expired or out of quota). `--email` prints only the address. `--priority-mode 7d_first|5h_first|monthly_first` changes the ranking.
- `taq status` — every account: state, 5h and 7d usage, resets, and a note when quota will go unused at reset.
- `taq machines` — which machine is using which account right now.
- `taq waste` — closed weekly periods per account: average used and unused.
- `taq health` — whether the server answers.

Use `npx -y team-ai-quota <command>` if `taq` is not installed globally.

## How to answer

- "Which account should I use?": run `taq best` for the relevant provider and give the email and why (lowest weighted usage, 7-day headroom first).
- "Are we wasting quota?": run `taq waste` and `taq status`; point at accounts with a high `~N% unused at reset` note or high average unused share per week.
- "Who is using what?": run `taq machines`.
- Exit code 1 with "rejected the access key" or "no Worker URL" means setup is missing or stale: redo Setup, do not guess a key.
- State what you ran and quote the numbers from the output; do not invent values.
