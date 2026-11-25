---
name: skills
description: The design, UX, UI and design-to-code skills Layerwright gives the agent - list them, read one, add the user's own from a link or pasted SKILL.md, write a new one with the user or edit one of theirs, turn one off or remove it. Use for /layer:skills, or when the user asks which skills there are or wants to add or write one.
argument-hint: "[<what a new skill should do> | add <link> | edit <id> | off <id> | on <id> | remove <id>]"
---

# Layerwright skills

Skills are guidance the agent reads before a job they fit: a design critique, a handoff spec with every state, layout, typography, colour, accessibility, motion. The library ships with Layerwright; the user's own live in `~/.layerwright/skills` and stay across updates. The same list is in the **Skills** tab of the Figma window. Its **Create a skill with Claude** button opens a new Claude Code session with `/layer:skills new <their words>` filled in (or asks a connected session), so `new` often arrives from there; the user can also write one there themselves (Write it yourself) or edit theirs, and `/skill <link>` in its chat box adds one.

- No argument: `layerwright_skills({ action: "list" })` and show a short table by category (name, what it's for, on or off, library or theirs), in the user's language.
- Words that aren't one of the commands below and aren't a link: a rule or what a skill should do ("don't use the playbook", "our buttons always have 8 px corners") is a new skill: do it as `new` below, with those words. A question about the skills ("which ones are for accessibility?") is answered from the list. Unsure which → ask.
- `add <link or text>`: `layerwright_skills({ action: "add", source })`. A GitHub folder, file or repository, a skills page that links to one (aiuxplayground.com/skills/…, skills.sh), or the pasted text of a SKILL.md. Say what was added and that sessions use it from their next step.
- `new <what it should do>`: write a skill with the user. `new` alone: ask in one short question what it should make sessions do or check, and for which jobs. Draft three parts from their words (and this project or its Design System when that helps): a short **name**, **when to use it** in one line (sessions pick skills by it, so name the jobs it fits), and the **instructions** in Markdown: concrete rules and checks a session can follow, not general advice. Write it in the user's language unless they ask otherwise. Show the draft, ask once (AskUserQuestion when you have it: Save / Change something), then `layerwright_skills({ action: "write", name, description, instructions })`. Say it's saved, on, and in the Skills tab.
- `edit <id>`: only the user's own. `layerwright_skills({ action: "read", id })`, make the change they ask for, show what changes, and save with `layerwright_skills({ action: "write", id, name, description, instructions })` (the instructions without the front matter).
- `off <id>` / `on <id>`: `layerwright_skills({ action: "disable" | "enable", id })`.
- `remove <id>`: only the user's own; a library skill can only be turned off. Ask once before removing.
