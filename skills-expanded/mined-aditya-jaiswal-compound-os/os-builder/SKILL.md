---
name: os-builder
description: Set up the user's own Compound OS in a new folder. Use when the user says "set up my Compound OS", "set up my OS", "make this mine", "onboard me", "build my team OS", "customize this", or opens Compound OS for the first time. One-sentence front door: interview briefly, then scaffold a working OS in a NEW folder, leaving the Compound OS demo intact as a reference. Do NOT use for daily work (individual commands like /morning-briefing) or the team-sharing split alone (say "share my OS with my team").
---

# os-builder

The single front door for a new user. In one sentence this builds the user's own working OS **in a new folder**, so the Compound OS demo stays untouched as a reference. Interview briefly, do all the file work yourself, end on a win that needs no connectors. Keep it dead simple.

## Constraints (read first, these override convenience)
- **Build in a NEW folder. Never wipe or convert the Compound OS template/demo in place** - the demo is the user's reference for what a populated OS looks like, keep it intact.
- Do ALL file work yourself. The user never edits a file, runs a command, or reads a doc.
- Confirm ONCE before creating the folder (one-line summary). Otherwise do not interrogate.
- Drafts and proposals only for anything external. Never send. Never use em dashes.
- Privacy wall: never create content in `people/`; it stays empty and gitignored.
- Minimal first. Ask only what is needed to produce a working OS.

## Step 0 - Locate the framework and pick the target folder
- **Template present here** (this folder has `CLAUDE.md` + the domain tree): you will COPY the framework from here into a new folder and leave this one as the reference.
- **Plugin-only** (skill installed, no domain tree here): `git clone https://github.com/aditya-jaiswal/compound-os` into a temp location to get the framework (the public repo stays the reference).
- **Target:** ask for a folder name, default `<company-slug>-os` (e.g. `nimbus-os`), created as a sibling. This becomes the user's OS (and later, their own git repo).

## Step 1 - Ask only the essentials (one short batch)
Required: name, email, role, company + one line on what it does, teammates (names + roles, or "solo").
Optional, can add later, do not block on them: Slack ID, GitHub handle, connecting Gmail/Slack/Calendar/GitHub.

## Step 2 - Build the user's OS in the new folder (do it all)
1. **Copy the framework** into the target (see `docs/reset.md` "What to KEEP"): `.claude/` (commands, skills, agents, sources.md), `views/build_team_pending.py`, `CLAUDE.md`, `INDEX.md`, `docs/`, `.gitignore`, `me.local.example.*`, `LICENSE`, and each domain's `CLAUDE.md` + header-only `rules.md`/`knowledge.md`/`hypotheses.md` with empty working subfolders. Do NOT copy the Acme demo content, so the new folder starts clean. (If you cloned in plugin mode and the demo came along, clear it per `docs/reset.md`.)
2. Write `me.local.md` + `me.local.json` from the answers (gitignored).
3. Put their roster in `CLAUDE.md` + `team/roster.md`; set the internal email domain; the CLAUDE.md that you copy should have no demo banner.
4. Create the private layer: `open-loops.md`, `waiting-on.md`, `daily/`.
5. Seed one real thing if they offered a customer or current sprint.
6. Empty `team/accountability/team-loops.md` table (header only); `feature-index.yaml` = `features: {}`.
Leave the source template/demo folder completely untouched.

## Step 3 - First win (no connectors needed)
From the NEW folder: open `views/team-pending.html`, answer a question about the seeded item, or run `/suggest-plan`. Do NOT lead with `/morning-briefing` (needs a connected inbox).

## Step 4 - Offer the optional next steps
Briefly: "Want to connect your inbox/Slack so `/morning-briefing` and `/triage-inbox` work? Or add teammates and share it?" Proceed only on yes (connectors: `personal.md`; sharing: `team.md`).

## Output template (end every run with this)
```
Your Compound OS is set up in <folder>.
- You: <name>, <role> at <company>
- Team: <n> people in team/roster.md
- Built fresh (framework only); the Compound OS demo stays intact as your reference
- Seeded: <the one real thing, or "nothing yet">
- Try it now: <the exact first-win action you ran>
Next (optional): connect tools, add teammates, or run /log-call on a real call.
```

## Worked example (one run, condensed)
> User: "set up my Compound OS"
> You: "Welcome. I'll build your OS in a new folder and keep this demo as your reference. Quick setup: your name, email, role? Company + one line? Teammates (names + roles) or solo? (Slack ID, GitHub, inbox are optional, add later.)"
> User: "Sam Okafor, sam@nimbus.io, Senior PM. Nimbus, a B2B scheduling tool. Team: Lee (eng), Mia (design), Ravi (QA)."
> You: "Got it. I'll create `nimbus-os/` next to this repo, copy the framework (commands, skills, structure, rules), set you + your team, and leave this Compound OS demo untouched as a reference. Confirm?"
> User: "yes"
> You: [create nimbus-os, copy framework only, write me.local + roster, private layer, stub board/index] then: "Done, your OS is in nimbus-os/. Opening its (empty) board. Try: 'log my last customer call' to start the memory. Want your inbox connected next?"

## Shortcuts you take (do not)
| Shortcut | Why it is wrong |
|---|---|
| Wiping or converting the template/demo folder in place | Destroys the user's reference; build in a NEW folder instead |
| Telling the user to edit a file or run `cp`/`git` themselves | The point is one sentence; you do the file work |
| Asking for Slack ID / connectors before scaffolding | Blocks a new user on question one; these are optional |
| Ending with `/morning-briefing` as the proof | Needs connectors a new user lacks; the "win" fails |
| Populating `people/` with the roster | `people/` is private notes only, never the team list |

## Exit checklist (all must be true)
- [ ] The user's OS is a NEW folder; the original Compound OS demo is untouched and still populated.
- [ ] `me.local.md` has real values, no "Jordan Rivera" anywhere in the new folder.
- [ ] Roster in the new folder's `CLAUDE.md` + `team/roster.md` is theirs.
- [ ] No demo residue in the new folder: `grep -rIn -iE 'acme|globex|initech|hooli|umbrella|datenwerk|insighto|jordan rivera' <folder> --include='*.md' --include='*.yaml' | grep -vE 'README|docs/|DEMO-GUIDE|skills/os-builder'` returns nothing.
- [ ] `open-loops.md`, `waiting-on.md`, `daily/` exist in the new folder.
- [ ] The first-win action actually ran and returned something.
- [ ] No em dashes in anything written.

## Next
Daily use (from the new folder): `/morning-briefing`, `/log-call`, `/sprint-board`. Sharing with the team: load `team.md`.
