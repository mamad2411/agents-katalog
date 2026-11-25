---
name: claude-checklist
description: A 9-section Claude usage checklist (setup, skills not folders, prompting, connectors, Cowork, projects, design and code, writing, token economy) with every item as printed, a verification note for each claim, and an audit command. Use when the user wants to set up or tune their Claude workflow, cut token use, or check their habits against the list. Source @aisimplified23 infographic "Claude Checklist" (Batch 103). Several items are the author's opinion or depend on product behaviour that changes; they are tagged below.
---

# Claude checklist (as printed)

Run `/claude-checklist [section]` to audit your own setup against it. Tags: [Certain] documented or arithmetic, [Likely] plausible and consistent with how the tools work, [Guessing] unverified claim or product detail I could not confirm.

**Setup.** Pay for Pro at $20/month [Likely: price as printed, check current plans] / Download the desktop app / Start hard chats with Fable 5 on High effort / Switch to Opus 5 after two turns [Guessing: the model names and the two-turn rule are the author's workflow; this environment names Opus 5.5 and Fable 5.1] / Turn off training in Settings, Privacy [Likely] / Keep your memory off by default / Delete your global instructions / Run /setup-cowork with the word "start" [Guessing: not verified here].

**Skills, not folders.** Turn your about-me.md into a skill / Skill anything you've explained twice / Build with /skill-creator natively in Claude / Turn a good chat into a skill from the title menu / Test the skill with five different phrasings / Keep skills away from creative work / Share skills to your workspace / Zero folders: Skills + Projects replaced them. The "explained twice" rule and the five-phrasing test are good practice [Likely]; this repo already has `skill-creator` and `/write-a-skill`.

**Prompting.** Give goals, not tasks / Add "use AskUserQuestion before you start" to every prompt [Likely: it makes Claude ask clarifying questions first] / Never end a prompt with "right?" [Likely: it invites agreement] / Drop "think step by step", add a role instead [Guessing: reasoning models already reason; a role helps less than clear criteria, so test it] / Three rules max per prompt / Delete your examples, zero-shot wins [Guessing: examples often help format-sensitive tasks; test both] / Edit your message instead of sending a follow-up [Certain: it avoids growing the context] / Batch three tasks into one message.

**Connectors.** Connect Gmail for email drafting and reading; Gamma for pitch decks; Google Drive for document access; Notion for workspace pages; Granola for meeting transcripts; Calendar for scheduling; GitHub for code projects. Turn off connectors you do not need for the task [Certain: fewer tools means fewer tokens and less exposure]. In this session Gmail, Google Drive, Notion, Calendar and Gamma are connected; Granola and GitHub are not (the GitHub tools here are scoped to one repo).

**Cowork.** Give Cowork big tasks: deck + email + checklist at once / Let it use its agent to actually do the task / Sessions run 8-30 minutes, walk away / Pick your model first, no switching mid-session / Use "restart from here" instead of correcting / Redo only the section that's wrong / Ask for the top 10 assumptions before any Excel build / Export to Google Sheets in one click.

**Projects.** Create one Project per recurring deliverable / Upload the emails, agreements, past campaigns / Leave Project instructions blank [Guessing: blank instructions work for pure context, but a short instruction block usually helps] / Never write creative work inside a stuffed Project / Put a skill inside a Project for the best combo / Share from Chat, not Cowork / Onboard new hires with a Project + /answer-onboarding / Rule: ask the Project before a colleague.

**Design and code.** Make infographics in the home tab, on Opus / Upload reference images before anything / Demand DESIGN_SYSTEM.md + tokens-preview.html first [Likely: matches `design-system-setup` and `the-design-system-prompt`] / Add "fidelity to my references beats your taste" / In Code: clean folder, bypass permissions, Netlify + Supabase [caution: bypass-permissions removes the safety prompts; use it only in a disposable folder or sandbox] / Use the CTO prompt: "You're the CTO, I'm the CEO who won't read code" / Build one piece at a time / Hand off with a HANDOFF.md [this repo has `/handoff`].

**Writing.** Use "ASD-STE100" (never for creative) [Certain: ASD-STE100 is the Simplified Technical English standard] / No tolerance of em dashes / Do not write with "it's not X, it's Y" / Ban delve, leverage, seamless, pivotal, tapestry / Force burstiness: one sentence under 6 words, one over 25 / Add human markers: $43, 4:30am, a mild complaint [caution: do not invent specifics; use real ones] / Dictate the mess, then "ask me clarifying questions" / Go incognito for creative work. Matches `avoid-ai-writing`, `humanizer`, `/anti-ai`.

**Token economy.** Message 30 costs 31x message 1 [Likely: each turn re-sends the whole conversation, so late messages cost far more; the exact 31x is the author's] / New chat every 30-50 turns / Summarize, copy, restart in a fresh session / Fable plans, Opus executes, Sonnet formats [Likely: a sound pattern] / Point Claude at files, don't paste walls / Ask for a plan before any big change / Skip peak hours: 5-11 AM Pacific weekdays [Guessing: not verified] / last item hidden by a watermark in the source image (starts "Te...") and not reproduced.

## Using it
Pick the three items that would change your week most (usually: Edit instead of follow-up, Summarize and restart in a fresh session, Turn off connectors you do not need). Do those for a week before adding more.
