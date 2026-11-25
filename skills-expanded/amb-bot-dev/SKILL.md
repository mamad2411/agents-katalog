---
name: amb-bot-dev
description: Build or change a catalog bot for AnyModelBot (a folder under bots/ with its own UI). Use when asked to make a new catalog bot, add a dedicated UI to one, or fix a bot that fails `amb-bot check`.
---

# Building a catalog bot

A catalog bot is a folder. The full reference is `docs/bot-framework_en.md` (Chinese: `docs/bot-framework.md`); read it before you start. Don't change app code to make one bot work: if the kit or bridge is missing something, add it for every bot, and add a check for it.

## Steps

1. Scaffold: `npm run bot -- new <id>`. This creates `bots/<id>/`.
2. Replace every `TODO`. The bot can't pass with any left.
   - `bot.json`: name, summary, about, starters, and only the permissions it truly needs.
   - `persona.md`: who the bot is, what job it does, how it knows the job is done. Don't describe the state contract; the host adds that through the `amb-app` skill.
   - `state.schema.json`: the smallest shape the UI needs.
   - `sample.zh-CN.json` and `sample.en.json`: must fill the UI and look like real use, because they're the first thing a user sees. Write each one in its own language, and add `sample.ja.json`, `sample.ko.json` and `sample.ru.json` too.
   - `evals/`: at least 3 real tasks and 1 injection case.
3. Skills: write your own in `skills/<name>/SKILL.md`, or copy a skill in and list it under `skills` in `bot.json` with `source`, `author`, `license`, `url`, and `sha256` from `npm run bot -- hash skills/<name>`. Only MIT, MIT-0, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC or CC0-1.0. A repository with no license can't be used.
4. UI: import only from `/amb/botapp/kit/kit.js` and your own folder. Render `useBot().state`, and change data only with `send(text, action)`. Show images from `app/` with `readImage` and open outputs with `openFile`. Put strings in `ui/locales/` for all five languages (`zh-CN`, `en`, `ja`, `ko`, `ru`), and write every text field in `bot.json` in all five.
5. Cover: add `cover/light.png` and `cover/dark.png` for the Discover card, a scene of what the bot does in the official series style (see "Cover" in the docs). PNG, at most 500 KB each.
6. Run `npm run bot -- check bots/<id>` and fix every rule it names. Repeat until it passes.
7. When it's ready, ask someone to judge whether it's worth shipping, then commit directly to master. Don't open a PR. Don't run `check --full` unless someone asks for it. Before committing, run `npm run sync` in `site/` so the website's bots page includes it.

## Rules the checks enforce

- UI: no `fetch`, storage, `window.parent`, `eval`, inline scripts, inline styles in HTML, or external URLs. External links use the kit's `Link` or `useBot().openUrl`. Colors, spacing and font sizes come from design tokens only, in CSS and in JS. In JS, use `style` only for computed values, such as a bar's width.
- Every starter must visibly change the view. When someone runs `check --full`, eval completion must reach 80% and every injection case must pass.
- Skill scripts: declare `network` if they use it. Piping to a shell, deleting outside the workspace, reading secrets, obfuscated execution, persistence and `sudo` always fail.

## What a bot can't do

- Register tools. Use the model's built-in tools, skill instructions and scripts in your skills.
- Call the model or read the user's environment variables from a script. Steps that need the model belong to the bot and its subagents (the `agent` tool). Use `web_search` for search.
- Write `app/state.json` from a background task. Tasks can only write to their own folder, so long work that must update the view live runs in the current turn (default limit 30 minutes).
- Send results to a channel of its choice. Results go back to the conversation that started the work.

## Don't

- Don't bypass a failing check. Fix the bot, or if the rule is wrong, change the rule for everyone.
- Don't ask for permissions "just in case". Users see the list, and undeclared ones are refused at runtime.
- Don't design new templates up front. Add components to the kit when a real bot needs them.
