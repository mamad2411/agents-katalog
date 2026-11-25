---
name: Build
description: Ship a feature fast and correctly. Use when starting any new build, feature, fix, or integration. Adapts to Claude Code, claude.ai, and Cowork.
---

# /build

Use this when you're ready to build something — a whole app, a new screen, a fix, or a feature. Before anything else, check which surface you're on. The skill adapts.

---

## Which surface are you on?

**Claude Code**
You have direct access to the file system. Read the relevant files before writing anything. Write code to disk, run it, check the output. Don't ask the user to paste code — go get it.

**claude.ai chat**
You don't have file system access. Ask the user to paste the relevant file or describe the current state. Generate code in full, in one block, ready to copy-paste. Tell them exactly which file it goes in and where.

**Cowork**
You have access to the files in the open workspace folder. Read them before writing anything. Write changes back to disk. Confirm with the user before overwriting a file that already has content.

---

## Before Claude writes anything

Answer these four questions and give them to Claude before saying "build this." They make everything that comes out better.

1. What is the user trying to do? (One sentence, from their perspective — not yours)
2. What does done look like? Describe it like you're watching someone use it on their phone. What do they see? What do they tap?
3. What's the smallest version that proves the idea? (Cut everything that isn't essential)
4. What could go wrong? (No internet, nothing to show yet, user types something unexpected, takes too long to load)

---

## The order Claude builds in

**Files and folders first.** Set up the skeleton before touching any logic. Don't skip this — it prevents a mess later.

**Data second.** What information needs to exist, and where does it live? (In Supabase? In the browser? Passed in from somewhere else?) Figure this out before building anything that uses it.

**The working part third.** Build the thing that actually does the work — the calculation, the API call, the save. Get this working before touching how it looks.

**The screen last.** Wire the working logic to something you can click. Ugly is fine. Working is the only requirement at this stage.

**Handle the "what ifs" throughout.** At every step: what shows if there's nothing to display? What happens if something fails?

---

## Non-negotiables

**API keys:** never in the code Claude generates. Always in a .env file that never goes to GitHub. Claude knows this — if it forgets, remind it.

**When something fails:** the user should see a clear message, not a blank screen. Every call to an API needs a fallback.

**While something is loading:** show a spinner or skeleton. Buttons should go grey while a request is in flight so users don't tap twice.

**When there's nothing to show:** the screen still needs to make sense. "No entries yet" beats a blank white void.

**Mobile:** test at 375px (iPhone SE). If it breaks, fix it before shipping.

**Privacy:** if using Supabase, row-level security must be on. That's the setting that ensures one user can't see another user's data. Claude will set it up — make sure it actually tested it with two accounts.

---

## Supabase checklist

- [ ] Table created with the right columns and types
- [ ] user_id column connected to auth.users (so every row is owned by someone)
- [ ] Row-level security turned on
- [ ] Policy set so users only see rows where user_id matches their own
- [ ] Tested: logged in as two different users, confirmed each only sees their own data

---

## When stuck

Stop. Don't keep asking Claude the same thing with slightly different wording. That doesn't work.

1. Describe what you were trying to do
2. Paste the exact error message (don't paraphrase it)
3. Share the relevant code or file
4. Say what you expected to happen, and what actually happened

**Claude Code:** run the file and paste the terminal output directly.
**Chat / Cowork:** screenshot or copy the error message in full.

---

## After shipping

- [ ] Walk through the whole thing yourself, as a real user would
- [ ] Try breaking it: what happens if you leave a field blank? If the connection drops?
- [ ] Update the spec so the next session starts with the right context
- [ ] Note what surprised you — that's the thing to ask Claude about next time.
