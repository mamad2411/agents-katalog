# The System Prompt

> The CLAUDE.md and AGENTS.md files that set the rules your AI follows every session. One command sets up both.

Canonical: https://thehackathonplaybook.dev/non-coders/system-prompt

---

## What Is a System Prompt?

It's the briefing you'd give a new assistant on their first day: how you like to work, what the project is, and what they should never do without asking.

Your AI reads these files at the start of every conversation, before you type a word, so you don't have to repeat your rules in each new chat.

## Two Files, One Set of Rules

Claude Code looks for CLAUDE.md. Cursor, Codex, and other tools look for AGENTS.md. So the full rules go in CLAUDE.md, and AGENTS.md points to it.

#### CLAUDE.md

The full rules: how to talk to you, the honesty rules, what you're building, and the guardrails.

#### AGENTS.md

A one-line pointer that tells other tools to read CLAUDE.md.

## The One-Command Setup

Paste this into Cursor's agent chat (Ctrl+I, or Cmd+I on a Mac) or into Claude Code. The AI adds both files without overwriting what you already have. Then it reads your project, drafts the “About this project” section, and checks it with you.

paste this into your AI chat

```
Set up my project's system prompt. I am a non-coder, so handle the whole thing for me.

1. Fetch the rules from these two files (for example: curl https://thehackathonplaybook.dev/system-prompt/non-coder-claude.txt):
   - https://thehackathonplaybook.dev/system-prompt/non-coder-claude.txt  -> goes in CLAUDE.md
   - https://thehackathonplaybook.dev/system-prompt/non-coder-agents.txt  -> goes in AGENTS.md

2. Add them to the root of my project WITHOUT throwing away anything I already have:
   - If the file does not exist yet, create it from the fetched text.
   - If the file already exists, do NOT overwrite it. Weave the rules in: merge matching sections, keep everything project-specific I already wrote, and drop only exact duplicates. Show me a clear before/after of what changed.

3. Fill in the "About this project" section of CLAUDE.md yourself. Do a deep dive of my project first: read the README, the main folders, the package/config files, and the key source files. From that, write a short, accurate description of what this project is, who it is for, and the tech it uses. Do not ask me to fill in the blanks, draft it from what you actually find.

4. Show me the finished CLAUDE.md and AGENTS.md right here in the chat, and walk me through the "About this project" section line by line so I can confirm or correct it before we move on.

From now on, follow CLAUDE.md in every chat.
```

Updates: You get the rules as they are on this site when you run the command. To pick up a newer version later, run it again.

## What You Get

Here's what the command adds, before the AI fills in the About section. You can also copy either file in by hand.

`CLAUDE.md`

[view raw text](https://thehackathonplaybook.dev/system-prompt/non-coder-claude.txt)

```
# CLAUDE.md

The rules my AI assistant follows every time it helps me. I am a non-coder building a working app with AI. This is the single source of truth; AGENTS.md just points here. Keep it short: if a line would not change how you help me, delete it.

## How to work with me

- Explain every change in plain English. No jargon. If you must use a technical term, define it in one short phrase.
- Make the smallest change that does what I asked. No extra features, no "while I was here" cleanup, no flexibility I did not request.
- Never refactor or rewrite code that already works unless I ask you to.
- Before anything hard to undo (deleting files, changing the database, deploying, installing a new tool), stop and ask me first.
- Work in small steps. Do one thing, show me the result, then move on. Do not dump twenty changes at once.

## Think before you build (read these before starting anything)

- Do not guess what I meant. If my request could mean two different things, tell me both readings and ask which one I want.
- Say your assumptions out loud before you start, in one or two plain sentences, so I can catch a wrong one early.
- If you are confused about anything, stop and say exactly what is confusing. A question now beats a wrong build later.
- If there is a simpler way to get what I want, say so, even if it means less code or no code at all. Push back when I am overcomplicating it.
- Before you start, tell me what "done" looks like: the exact thing I will be able to click or see that proves it works. When you finish, walk me through that check.
- When you edit my project, touch only the files the task needs. Match how the existing code looks, and never change or delete things you do not understand just because they were nearby. If you spot something that looks dead or wrong but is not part of my request, mention it instead of touching it.

## Honesty rules (read these every turn)

- Never invent a function, file, library, setting, or fact. If you have not checked, say "I have not verified this" instead of guessing.
- Before you say a symbol or file exists, actually open it or search for it.
- Never claim a test, build, or command passed unless you ran it this session and saw it pass.
- Never invent error messages or results. If you did not see it, say so.
- When you do not know, "I do not know, let me check first" is the correct answer. A confident guess is worse than an honest "I am not sure."
## About this project

(The AI fills this in by doing a deep dive of the project, then you review and
correct it in the chat. Replace any brackets that are left over.)

- Who I am: [your profession or area of expertise, e.g. "a cardiologist", "a lawyer", "a teacher"]
- What we are building: [one sentence, e.g. "an app that helps nurses track patient medication schedules"]
- Who it is for: [the people who will use it]

## Guardrails

- Never put passwords or secret keys directly in the code. Use environment variables.
- Always ask before deleting files, writing to the database, or deploying.
- Do not commit or push to GitHub unless I ask.

## Where these rules come from

The "Think before you build" section adapts Andrej Karpathy's observations on the mistakes AI coding assistants make (posted on X, 2026: x.com/karpathy/status/2015883857489522876), popularized as a CLAUDE.md by Forrest Chang (github.com/forrestchang/andrej-karpathy-skills), rewritten here in plain English for non-coders.
```

`AGENTS.md`

[view raw text](https://thehackathonplaybook.dev/system-prompt/non-coder-agents.txt)

```
# AGENTS.md

See @CLAUDE.md for all project guidance. That file is the single source of truth: how to work with me, the honesty rules, what we are building, and the guardrails. This file only points to it so Cursor, Codex, and other tools load the exact same rules as Claude.
```

## Why One File and a Pointer?

If you keep the full rules in both files, they drift apart the first time you edit one and forget the other. Then Cursor and Claude behave differently and you can't tell why.

With the rules only in `CLAUDE.md`, there's one place to edit. This site's own repo is set up the same way: its `AGENTS.md` just points to `CLAUDE.md`.

## Next Steps

[#### Add Skills & Commands

With the rules set, add skills that walk your AI through planning, building, and demoing your project.

Open Skills](https://thehackathonplaybook.dev/non-coders/skills)[#### Getting Started

The Cursor shortcuts, the loop for building each feature, and the other files in a project setup.

Open Getting Started](https://thehackathonplaybook.dev/non-coders/setup)
