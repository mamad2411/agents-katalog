---
name: claude-code-mods-guide
description: What a Claude Code "mod" is (a plugin of function hooks that runs code inside Claude Code), how it differs from a skill, an MCP server and a hook, what it can do, the security catch (it runs with your permissions and is not sandboxed), and a review procedure before installing one. From an 8-slide PathionAI carousel, checked against two published articles. Use before installing or writing any mod or third-party Claude Code plugin, or when someone asks whether a mod, skill or MCP server is the right tool.
---

# Claude Code mods: explained and risk-checked

Source: @taha_pathionai (PathionAI), "Redesign Claude Code yourself", 8 slides dated 01.10.2026. I checked the central claims against two web articles (wavect.io on function hooks, pluto.security on their security). I did not install or write any mod. This session also lists a built-in `plugin-authoring` skill for writing mods; use it when you want to build one, and read this page first.

## The four things people confuse (slide 6)

| Thing | What it is | Runs code? |
|---|---|---|
| **Mod** | Code that changes Claude Code itself | Yes, inside the app |
| **Skill** | Instructions Claude reads | No; Claude follows text |
| **MCP server** | An outside service that gives Claude tools | Yes, outside the app |
| **Hook** | A command that runs on an event | Yes, on your machine |

One line from the carousel to keep: skills tell Claude what to do; mods change the app Claude runs in.

## What a mod can do (slides 2 and 3)

A mod is "a plugin that changes how Claude Code works": small bits of code that run when Claude uses a tool, when you send a prompt, or when the screen redraws. Slide 3 lists five powers: rewrite your prompt before Claude sees it; block or rewrite an action Claude tries; add panes, banners and buttons; add `/commands` that skip the model; send a request to a different model. Both articles describe the same mechanism (function hooks that intercept events). [Certain] for the mechanism, [Likely] for the exact list of five.

## The catch (slide 7), confirmed

A mod runs with **your** permissions. A bad one can read your files and API keys, see every prompt, approve actions for you and spend your usage. The pluto.security article adds that users are not warned at install time and that a mod's declared capabilities show only through a manual command. [Certain]

Slide 7's check: run `claude plugin validate` on the plugin before installing it; it lists the events a mod hooks and the calls it makes. If something is off, the slide says to restart with `--safe-mode`. I could not confirm the `--safe-mode` flag. [Guessing]; run `claude --help` first.

## Things I could not verify

- The version line (2.1.287 or later, on by default), "full mods only in Terminal and Desktop, VS Code gets behaviour only", and the names "Anthropic's 3 sample mods" (token-weather, blast-radius, replay-theater). Searches did not find them, and the slide itself says they are simplified mockups. [Guessing]
- The attributed quote ("No reason why everyone should have an identical Claude experience", Boris Cherny). Unverified.
- The community mods named on slide 5 (Next Steps, Cache Keeper, Recording Mode, Goal Meter, Collision Guard).

## Review procedure before any mod

1. Get the source, not just the install command. Read `plugin.json`, the hooks file and every script it loads.
2. Run `claude plugin validate` on the folder and read the events and calls it lists.
3. Look for: file reads outside the project, network calls, anything that touches environment variables or key files, and any hook on prompt submission or tool approval.
4. Prefer a mod you wrote yourself from a plain description (slide 5's idea) over an unknown one, and still read what Claude wrote.
5. Install in a throwaway project first. Keep your API keys out of that shell's environment.
6. Re-review after every update. A mod can change after you approve it. [Likely]
7. Never install a mod because a carousel named it.
