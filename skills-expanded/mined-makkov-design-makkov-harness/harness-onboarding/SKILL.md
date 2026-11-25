---
name: harness-onboarding
description: First-run setup for makkov-harness. Use when a person has just installed this harness, says "set this up for me", "onboard me", or asks how to personalize it. Interviews them in a few short questions and writes their own private layer of instructions (language, role, tools, preferences) into the right place for their agent, without touching anything else.
---

# Harness onboarding

Turns the shared harness into the person's own setup. The shared part (skills, ROUTING.md) stays as installed; this skill adds a short personal layer on top.

## 1. Interview

Ask one question at a time, in the person's language, with suggested answers so they can reply in a word:

1. What do you mostly do? (designer, developer, product, marketing, student, other)
2. Which language should I answer you in? And for texts meant for other people (team, clients), which language?
3. Are you a programmer? (yes / a bit / no) — sets how detailed setup instructions should be.
4. Which tools do you use daily? (Figma, Notion, Linear, Jira, GitHub, Slack…) — only names, never logins or keys.
5. How do you want results delivered? (report pages, short chat answers, files)
6. Anything Claude or other agents keep getting wrong for you?

Stop early if they want to skip; use sensible defaults.

## 2. Draft the personal layer

Write 10-25 lines of plain instructions, for example:

```markdown
# Personal layer (makkov-harness)
- Answer in English; drafts for my team in German.
- I am a designer, not a programmer: give step-by-step instructions, one command per block.
- Deliver research and plans with rich-report (Claude) or html-report (other agents).
- Daily tools: Figma, Notion, Linear.
```

Rules: no secrets, tokens, emails of others, client names or company-internal details. Show the draft and get a clear yes before writing.

## 3. Write it to the right place

Write it where the harness itself was installed, so it lives and goes with that install.

1. **Find the install.** Look for an install manifest, `.makkov-harness/install-<agent>.txt`, first in the current project folder, then in the home folder. Its `rules=` line names the instructions file the installer wrote the routing map into, and `scope=` says whether the routing covers all work or design only.
   - A manifest in the project folder (a project install): write into that project's file from `rules=`. The layer then applies to this project only; say so. Do not write to a user-level file unless the person asks for it by name.
   - A manifest in the home folder (a user-level install): write into the file from `rules=`.
   - Cursor (`rules=` ends in `makkov-harness.mdc`): that file is rewritten on every install, so write `makkov-harness-personal.mdc` next to it instead, starting with the same front matter (`description: makkov-harness personal layer`, `alwaysApply: true`).
   - No manifest, running in Claude Code with the makkov-harness plugin: `~/.claude/CLAUDE.md`.
   - No manifest anywhere else: ask the person how they installed the harness (installer for which agent and folder, or by hand) before writing anything.
2. **Write it between markers**, on lines of their own, so updates and the uninstaller find exactly this block:

   ```markdown
   <!-- makkov-harness:personal:start -->
   # Personal layer (makkov-harness)
   - …
   <!-- makkov-harness:personal:end -->
   ```

   Never overwrite other content. If the markers are already there, replace what is between them. If an earlier run left the `# Personal layer (makkov-harness)` heading without markers, replace that section (from the heading to the next `#` heading or the end of the file) with the marked block. Back up the file first (`<file>.bak-<date>`).
3. **Keep to the install's scope.** With `scope=design`, write only what concerns design work; leave out preferences for research, installs and general coding, and say why.

`install/uninstall.sh` and `install/uninstall.ps1` remove this block (and Cursor's `makkov-harness-personal.mdc`) together with the routing map. A Claude Code plugin install has no uninstaller for it: to remove it, delete the marked block from `~/.claude/CLAUDE.md`, or run harness-onboarding and ask to remove it.

Cloud sessions do not read the user-level file from the person's computer. Tell them: to have the layer in the cloud too, keep it in a private GitHub repository of their own and add it as a plugin marketplace in their claude.ai account (see the harness README).

## 4. Confirm

Say in 2-3 lines what was written and where, and how to change it later ("run harness-onboarding again").
