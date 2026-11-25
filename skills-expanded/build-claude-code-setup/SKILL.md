---
name: build-claude-code-setup
description: Sets up a safe room for a prototype in Claude Code and writes a Claude Code Setup Record with a separate folder outside company code, the permission mode that asks first, a short CLAUDE.md of rules, an approve and decline list and the request for an engineer's written yes. Use for "run build-claude-code-setup", "I have never opened Claude Code", "set up a prototype folder", "which permission mode should I pick", "what should I approve in Claude Code", "write a CLAUDE.md for my prototype", "can I link our company code", "is it safe to let Claude run commands", part of the Claude for Product Builders Pack by 90n.
---

# Claude Code Setup

## When To Use
The clickable version is not enough to test the belief, and you have never opened Claude Code. Run this once, before any code exists. It answers: where does the prototype live, what may Claude do there without asking, and what will you say no to?

## When Not To Use
If a click-through tests the belief, stay with Clickable Prototype and skip this. If you want to tell Claude what your product is and how it speaks, that is Product Context File; this skill only sets the room and its rules.

## Inputs
- The belief on your test card and the line in your Prototype Brief that says a working version is needed
- Where you can run Claude Code: the desktop app, the web or a terminal
- Anything company-owned you think the prototype needs (code, a design system, an account)
If you have none of this, I start from a one-line description of the prototype and mark the output as a first draft.

## Approach
The method is the permission and project memory setup in the Claude Code docs (code.claude.com/docs/en/permission-modes, /security and /memory), held to least privilege as the NIST glossary defines it (csrc.nist.gov/glossary/term/least_privilege): the minimum access the task needs. You are the one who approves, so the room is built so that every approval is small enough to read. The failure it prevents: Claude Code started inside a folder that also holds company code, in a mode that does not ask, and a command you could not explain has already run.

## Workflow
1. Ask up to three questions: where will you run it (the desktop app's Code tab, which needs a paid subscription, the web with no local setup, or a terminal, for which the docs carry a guide for people who have never opened one), which belief needs a working version, and does anything company-owned need linking?
2. Make a new, empty folder for the prototype, outside any company code, and start Claude Code in that folder. Name it so nobody takes it for the real thing: [idea]-prototype.
3. Choose Manual mode on purpose. It starts read-only and asks before it edits a file or runs a command. Some sessions start in a mode that does not ask, so look at the mode selector before the first prompt. When asked, approve once; do not choose "allow from then on".
4. Write what you approve and what you decline. Claude asks before its file tools go outside the start folder, but a shell command you approve can still write anywhere your account can. So read every command, and decline anything you cannot explain. The docs put it plainly: "You're responsible for reviewing proposed code and commands for safety before approval." If you are unsure about a command, check with your engineering or security lead.
5. Write a short CLAUDE.md, well under 200 lines, with four rules: sample data only, no keys in files, never touch production, ask before installing anything. It is context, not enforcement: Claude reads it each session and can still get it wrong, so you keep reading what it proposes.
6. Apply least privilege to everything else. No company code, design system or account is linked without an engineer's written yes. I draft that request; you send it and wait. The finished record stays in the folder, so anyone who opens it later can see the rules it was built under.

## Output Format
```markdown
# Claude Code Setup Record
Prototype: [name] | Set up by: [role] | Date: [date] | Runs in: [desktop app / web / terminal]
## Folder and permission mode
| Item | Entry |
|---|---|
| Folder | [path, outside any company code], empty when started: [yes / no, and what was in it] |
| Company code, design system or account linked | [none / what, agreed in writing by [engineer role] on [date]] |
| Mode shown in the selector before the first prompt | [Manual / other, changed to Manual] |
| "Allow from then on" chosen | [no / yes, for what and why] |
## Rules file
CLAUDE.md, [n] lines: sample data only; no keys, passwords or tokens in any file; never touch production or any company system; ask before installing anything.
## What I approve and what I decline
| Claude asks to | My answer | Why |
|---|---|---|
| [edit a file inside the folder] | [approve once] | [I can see the change] |
| [run a command I cannot explain] | [decline and ask what it does] | [a command can write outside the folder] |
## Request to the engineer
[Draft message: what I want to link, why the prototype needs it, read only, and the date I need an answer.]
## Decision
[Engineering lead, by role] says yes or no in writing to any link to company code or a design system by [date]; until then [builder, by role] works in the empty folder only.
```

## Done When
- The folder is new, outside company code, and the record says so
- The mode was read off the selector, not assumed, and CLAUDE.md holds the four rules
- Any link to company property has a written yes or is marked "not linked"

## Quality Bar
- One approval at a time. A standing approval is recorded with its reason or it does not exist.
- A command you cannot explain is declined, however sure Claude sounds.
- The rules file is context, never a lock; the record says who still reads each proposal.
- No customer data and no key enters the folder, including in a pasted screenshot or log.
- The prototype folder never touches production or company code without an engineer's written yes; security points: check with your engineering or security lead.

## Next
Run build-first-working-version (First Working Version) to build one flow in the folder.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
