---
name: claude-surfaces-playbook
description: Five ready-to-use prompts, one per Claude "surface" (Chat, Cowork, Projects, Code, Dispatch), for turning a vague task into a specific ask — interviewing yourself before writing a post, drafting a newsletter from a context folder, mining recurring team deliverables into named Projects, building a website from a screenshot with no code, and dispatching a background task (like posting a freelance job and following up on replies) from your phone while Claude works on your computer. Use when the user knows roughly what they want from Claude but not how to phrase it, or is choosing which Claude product surface fits a task.
---

# Five Ways to Use Claude (one per surface)

Original content compiled from a "5 ways to use Claude you never tried" social
carousel — the prompts below are reproduced as-is; the framing/marketing
language around them is not.

## 1 — Chat: interview yourself before writing anything

Use when facing a blank page for a LinkedIn post, email, or memo. Let Claude
extract the content by asking one question at a time instead of you staring
at an empty draft.

> I need to write a [LinkedIn post / email / memo] about [topic].
>
> Interview me.
> Ask me ONE question at a time about:
> 1. What happened
> 2. Why it matters
> 3. Who needs to hear this
> 4. What I want them to do after reading
>
> When you have enough, write the first draft.

## 2 — Cowork: write in your own voice from a context folder

Cowork (Claude reading/writing files on your computer) can follow your
writing rules and produce an actual document, not just chat text, if you
point it at a folder of your own writing/examples first.

> I want to write my next newsletter on [topic].
>
> First, explore my CLAUDE COWORK folder.
>
> Then, ask me questions using the AskUserQuestion tool.
>
> I want to refine the approach with you before you execute.

## 3 — Projects: let Claude find which Projects your team actually needs

Rather than guessing what to name a Project, have Claude interview you about
your team's real recurring output first, then propose Project names.

> I work at [company + industry]. My team specifically helps [clients]
> [achieve goals].
> We need to identify the 3-5 recurring deliverables my team produces.
> Interview me.
> Ask me ONE question at a time about:
> 1. What my team does day-to-day
> 2. What we deliver to clients, leadership, or each other
> 3. What tasks feel repetitive every week or month
> 4. What work someone always ends up redoing
>
> When you have enough context, give me a numbered list of 3-5 recurring
> deliverables with a suggested Project name for each.

## 4 — Code: build a website from a screenshot, no coding required

"Vibecoding" — describe what you want in plain English (optionally attaching
a reference screenshot), Claude writes the code, builds it, and can push it
live.

> Create a GitHub repo named "[project-name]".
>
> I do not know how to code.
>
> Code everything for me.
> Do not ask for permissions.
>
> Build me something that looks like this [screenshot attached], but for
> [your project].
>
> Read the files in my folder first. Use my tone and style for the website
> copy.

Treat "do not ask for permissions" as the carousel's own framing, not a
default to actually run with — for anything beyond a personal throwaway
project, keep normal review of what gets pushed where.

## 5 — Dispatch: hand off a task while you're away from your computer

Dispatch (Claude Code on your phone, acting on your Mac) lets you text a task
and walk away; Claude keeps working on your computer.

> Go to my Fiverr account on Chrome. Post a job offer for a [job title].
>
> Then, send a message to the best 10 [talent].
>
> Check if I have any unanswered DMs, and follow up until one accepts for
> [budget] maximum.

## Picking a surface

| Need | Surface |
|---|---|
| A quick answer, no setup | Chat |
| A document that follows your existing writing rules/examples, working in the background | Cowork |
| A standing workspace with your standards baked in, reused across many chats | Projects |
| A working website/app/dashboard, described not coded | Code |
| A task run on your computer while you're away from it | Dispatch |
