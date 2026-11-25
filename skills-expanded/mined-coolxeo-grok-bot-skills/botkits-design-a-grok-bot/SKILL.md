---
name: botkits-design-a-grok-bot
description: >-
  Needs Grok Bot. Use this when designing or creating a new Grok Bot. Ask a few preference
  questions, write a tight persona, CreateAgent, then verify against the live
  profile. Coding bots use pstack / poteto-mode as the quality bar. On a fresh
  install, run setup-pstack first and ensure healthcheck routines exist.
compatibility: Needs Grok Bot (uses CreateAgent and Grok Bot profiles).
---
# Design a Grok Bot

Build a real bot for the user, not a template, unless they ask for a template. A good bot does one thing well and stays out of everything else.

## The four parts of a bot

Write them in this order. The description holds all four.

1. **Job.** One sentence: what it does each time it wakes.
2. **Not its job.** The nearby things it refuses, even when asked. Those belong to another bot. (A mention scout doesn't post. A drafter doesn't send.)
3. **Voice.** A few words. The user's own tone or a named character, never "helpful assistant".
4. **Wake.** Chat, a routine, an event, or a mix. Silent when there is nothing worth saying.

Keep the name short. Leave out tool lists, model essays, and "I can also help with...".

## Fresh install (first message after import)

Do this once, before any design work:

1. If `~/.cursor/rules/pstack-models.mdc` is missing, run `/setup-pstack`. If a real repo exists and there is no `verify-*` skill, run `/create-verification-skill`. Don't ask first.
2. List `/home/box/agent-data/agents/<this-agent-id>/automations/`. Create whichever healthcheck routine is missing with `update_state` (target `routine`, action `create`), each told to stay quiet when it has nothing to propose:
   - `transcript-healthcheck`, schedule `44 8 * * 1-5`, runs the botkits-transcript-healthcheck skill.
   - `routine-healthcheck`, schedule `49 8 * * 1`, runs the botkits-routine-healthcheck skill.
   Tell the user what you created or that both already existed. Imports don't always bring routines along, so this step is the safety net.
3. Offer once to run a routine checkup across all bots.

Skip anything already done in this chat.

## Intake

First read the bot's lessons file (for example `skill-lessons/design-a-grok-bot.md` in your workspace) if it exists. Apply each lesson marked KEEP.

Ask only taste questions that no test can answer, and skip any already answered: the job, the name and voice (if they care), routine or on-demand, and who the bot talks to (just the user, other bots, a channel).

Don't ask about tools, plugins, or models when a working sibling bot shows the answer. Once the job is clear, create the bot; don't ask "shall I?". For small reversible choices (a nickname, a color), pick one and say what you picked.

## Approval cards

If the bot will ever need the user to approve, pick, or confirm (a post, a spend, a live change), put this in its description: always ask with a `SendToUser` question widget that has real, checked options. No plain-text "reply A or B", no "waiting for your tap" without a card. One card ends the turn. If a tool shows its own approval UI, use that instead.

## Coding bots

The bar is pstack's poteto-mode (and boteto-mode on Grok Bot). In the description: the job and the not-jobs, short unslopped replies, repo work goes to a CloudAgent instead of a local clone, slash-skills are live files, and the model rule copied from an existing coding bot unless the user names one. Point to poteto-mode for hard tasks; don't paste the playbook in. If pstack isn't installed, say so and keep the same discipline.

## Other bots

Scouts, shopkeepers, life admin, dispatchers, writers. In the description: the job in the first sentence, silence on empty runs, the refused neighbor verb, and the concrete how (which API, inbox, or channel), plus the approval-card rule if it gates on the user. No coding instructions unless the job is explicitly split between coordinating and coding.

## Create and prove it

1. `CreateAgent` takes `name` and `description`. The description is the whole persona. There is no delete tool, so create only for a real job.
2. Read `/home/box/agent-data/agents/<id>/profile.json` back. Don't trust the tool's acknowledgment alone.
3. Send the new bot one realistic test message and check that the reply matches the job and the voice. Fix the description if it doesn't.
4. If the job needs a routine, you can't create another bot's routines. Use `SendToAgent` to tell the new bot to call `update_state` (target `routine`, action `create`) with the exact name, prompt, and schedule or trigger. If that fails, give the user the one-line instruction to paste into the new bot.
5. Tell the user the name and the one-line job, and that they can delete it from the sidebar (right-click, Delete).

## Inspired by

- [Lauren Tan (@poteto), dr eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2) (marketplace template; no reuse license shown, so no text is copied). Does well: one job, one voice, explicit anti-jobs, a short intake, and healthcheck routines on first run. Missing: its listing has no rule for approval cards, no read-back of the created profile, and no test message to the new bot.
- [Lauren Tan, pstack poteto-mode](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/poteto-mode/SKILL.md) (MIT). Does well: the coding-agent quality bar (unslopped prose, verified work, never block the human on reversible choices). Missing: written for a coding agent, not for designing other bots.
- [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents). Does well: start with the simplest setup and add complexity only when it pays, and design tool interfaces carefully. Missing: about architecture patterns, with no persona or anti-job guidance.
- Harness²'s Propose-Probe-Compose loop and its lessons ledger (google-research/harness2). Does well: a propose-probe-compose loop and a lessons ledger. Missing: a research framework around JobBench, LAB, and WorkBuddy-Bench, plus a local demo with no credentials and authentication alternatives; not a procedure for designing Grok Bot personas.

## What this version adds

- The approval-card rule baked into every bot that gates on the user.
- A read-back and a live test message before telling the user it's done.
- The routine hand-off with a paste-able fallback.
- A test-and-keep loop with a fixed probe set per bot, pass or fail scoring, real friction as a new probe, and a TRY then KEEP rule for lessons.

## Test-and-keep (before create, and on every persona rewrite)

A persona is a harness. Test it before you ship it. Cheap version: reason it through. Do not create test bots.

1. **Probe set.** Write 4 fixed test asks for this job: one typical ask, one anti-job ask (the adjacent verb it must refuse), one decision that needs a tap card, and one quiet case (nothing to report). Save them with the lessons file so later rewrites use the same probes.
2. **Propose.** For a rewrite, keep the current persona as the control and write 1-2 versions. Change one thing per version.
3. **Probe.** Read each version against each probe. Score it pass or fail: the right action, the anti-job refused, a card (not plain text), and silence in the quiet case. Pick the version with the most passes. On a tie, pick the shorter one.
4. **Compose.** Ship the winner. Merge a line from another version only if that line fixed a failed probe on its own.
5. **Watch.** After the bot runs, real friction is the true probe. When the user or a transcript healthcheck shows a failure, add it as a new probe and rerun steps 2-4.
6. **Record.** Add 1-3 lines to the lessons file: the date, the bot, what failed or helped, and the evidence. Mark a line TRY first, and KEEP only after it wins a probe on a second bot.
