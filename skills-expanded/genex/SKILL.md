# Genex in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's own guide, with the
passages of advice Studio does not ship taken out. Where it disagrees with this preface, this preface wins.

## What does not apply in Studio

- Setup. The game's folder is already the workspace, Studio ships and pins the Genex CLI, and the
  user signs in to Genex once in Studio.
  Never check or install Node, never run `npx genex`, `npm i -g` or `npm i -D @genex-ai/cli-demo`,
  and never run `auth`, `tools` or `init`.
- Skill cards are never copied into the game: no `.claude/skills`, `.agents/skills` or `AGENTS.md`
  is written. The Genex cards Studio carries are this plugin's skills, listed in your brief; read
  one with `genex__skill {"name":"<skill>"}`. The lane cards the "Use it" section points to are
  `genex-tool-model`, `genex-tool-character`, `genex-tool-texture`, `genex-tool-audio` and
  `genex-tool-image`, one per lane.

## Commands, as Studio tools

- Generation (`image`, `model`, `model segment|rig|animate`, `texture`, `sfx`, `music`, `voice`,
  `character`, `animations search`) and `wait`: `genex__asset`. Its operation `status` reports
  the account, credits and live lanes that `doctor` would. Its description lists
  the operations and which provider each lane is; its `options` parameter lists each lane's
  options. Studio passes `--out-dir` and `--no-wait` itself, and delivered files land in the game,
  so wire in those local paths. In a Godot game they land in its project (`godot/assets/...`),
  which the game loads as `res://assets/...`.
- `doctor`, `budget`, `llm models`, `llm status`, `llm cancel`, `shop list`, `shop add`,
  `items list` and `items search`: `genex__cli`. `budget --assets` is not available: Studio's own
  asset allowance and the user's approval govern asset spending. `shop add` asks nobody: it makes
  a store item's draft, which spends nothing and sells nothing until Studio puts it on sale with the game's publish,
  and it needs the item's picture (`image`, a square PNG of at least 768 × 768), at any time, with or
  without a build.
  So do `shop set` and `shop remove` on a local draft (`local_…`).
- `llm bench`, `shop set|remove` on an item in the store, `shop test` and `items add|remove`:
  `genex__cli-paid`. The user
  approves each call, because it spends Nex (Genex's currency, which the cards call coin) or changes
  what the game sells. A store item's `image`, `model` and `package` name paths inside this game,
  and `items add` writes `genex-items/<id>/` into it; `shop publish` is not available, because Studio puts
  a game's items on sale when it is published. Read the `genex-items` skill first. A thing priced in Nex is a store item; coins, gold or gems are the game's own currency unless the person says they are
  for real money.
- `publish` and `promote`: `genex__publish {"operation":"gallery"}`, which also updates the draft;
  use it when the user wants the game published. `preview` alone: `genex__publish
  {"operation":"draft"}`, a test build that leaves the public version as it is. Follow a publish
  with `genex__publish-status` for the job and the links.
- `cover`, and the frame `preview` picks up from `.genex/scratch/cover.png`: `genex__cover
  {"image":"<path in the game folder>"}` keeps the picture (and an optional clip) of the game as
  its cover, and its answer says who chose the cover on Genex, as `npx genex cover` with no file
  does. Publish (`genex__publish`) sends the kept picture and `genex__cover-set` sends it now; the
  `cover` skill has the requirement. Never save a frame in `.genex/scratch`.
- `npm i @genex-ai/multiplayer`: `genex__package {"package":"@genex-ai/multiplayer"}`, and
  `npm i @genex-ai/embed-sdk`: `genex__package {"package":"@genex-ai/embed-sdk"}`. Studio picks
  the version and installs it without asking anyone. In a game made from Studio's template it maps
  Studio's copy in the import map instead, and Studio calls `initEmbed()` for the game.
- A card Studio shows for a paid command waits for the person even after your turn ends, and the
  call runs once they approve. Never record it as declined or blocked while it waits; when you come
  back, check whether it ran and ask again only if the person declined it.
- A `genex__cli` call carries the words of the command, its positional argument and its flags by
  name without dashes: `npx genex llm cancel <id>` is
  `genex__cli {"command":"llm cancel","args":"<id>"}`, and `--all` is `"options":{"all":true}`.
- Any other `npx genex` command is not available in Studio. Say so rather than work around it.

## When credits run short

Building the game never uses Genex credits: it runs on the user's own plan. A generation Genex
refuses for too few credits keeps its card in Studio, which says so and offers Get credits, then
Make it. So never relay the balance, price or refill date, and never retry: add at most one short
sentence saying what waits for credits, and carry on.

<!-- upstream https://genex.games/SKILL.md v1.40.0 sha256 df89029d58e8ecccd6333fde4dfadf1b5072f18ccf31d67294a3df626c486f85 -->
---
name: genex
version: 1.40.0
description: >-
  Game-dev asset generation for your agent: 3D models (segment/rig/animate), images, video,
  textures, sound effects, music, voice, and rigged characters - generated from
  the terminal, downloaded as files the user owns. Exception: if the user
  already has a dedicated pipeline or asset source for that need, use it -
  Genex fills the gaps, it doesn't replace their tools.
---

# Genex

## What this is

Genex Tools is the asset toolkit for a game the user is building themselves. One package gives you, the coding agent, every gamedev AI generation tool from the terminal: 3D models (plus segment, rig and animate), images, video, textures, sound effects, music, voice, and rigged animated characters. One sign-in, one meter, no provider accounts and no API keys of the user's own. Genex generates the assets; the user's code and project stay exactly as they are.

## Never delete or overwrite anything in this folder

**This is the one mistake the user cannot undo.** Whatever is already here is THEIRS: their code, reference images, notes, sketches, an earlier attempt, files you don't recognize. For some of them there is no undo - no trash, no backup, no git history. So: you may add files, and edit the ones you created. You may never delete, empty, move, rename, or overwrite anything you didn't create yourself - not to "start clean", not to make a tool's prompt go away, not because a file looks like junk to you. **A non-empty folder is normal and is never something to fix.** That rules out `rm`/`rm -rf`, `git clean`, `git checkout -- .`, `git reset --hard`, moving things to the trash, and every setup tool's offer to empty the directory (**"Remove existing files"**, `--force`, `--overwrite`). If something genuinely can't continue without removing something of theirs, **stop and ask first** - name the exact files and wait for their yes; your own "it's probably nothing" is not that yes.

## Use it

```
npx genex doctor                                   # sign-in, credit balance, which lanes are live
npx genex image "<what it should show>"            # posters, sprites, icons, UI art (--transparent for alpha)
npx genex model "<what it is>"                     # props, vehicles, buildings (--image to work from a photo)
npx genex model segment|rig|animate <id> ...       # split a mesh into parts, rig any body plan, retarget preset clips
npx genex texture "<the surface>" --terrain        # tiling ground, walls, rock
npx genex sfx "<the sound>"  ·  npx genex music "<the track>"  ·  npx genex voice "<the line>"
npx genex character "<who they are>"               # a rigged, animatable body
npx genex character --image ./front.jpg --image ./back.jpg  # Meshy from your own references (1-4 views)
npx genex animations search "<verb>"               # the 680-action catalog for characters
```

Every asset **downloads into `./assets` as a file the user owns** - wire that local path into their code, exactly like art they drew themselves. The URL printed beside it is where it came from; never fetch it at runtime.

`./assets` is only the default: pass `--out-dir <dir>` to land a file in the folder the game already loads assets from (Vite `public/`, Unity `Assets/`, and so on), so it ships in the build without a second copy.

- **Enqueue in parallel.** Add `--no-wait` to fire several generations at once, keep building, then `npx genex wait --all` for status and `npx genex wait <id>` to pick each one up. `wait` never costs anything.
- **Never re-run a generate command to check on one that is running** - that starts and bills a second asset. `wait` is the only status check.
- `npx genex wait --all` lists every generation and its state; a generation nobody wires in still cost its credits.
- **Treat every warning line as work**, not noise - the CLI only prints defects it actually measured.
- Each lane has a skill card (`genex-tool-...`). `npx genex --help` lists everything with typical costs.

## Models at play time

If what the user wants needs a language model running while somebody **plays** the finished game - an NPC that answers in its own words, a quest written from what the player typed, a prompt box inside the game - that is a Genex platform feature, and the **player** pays for it: their Genex credits or their own Claude/ChatGPT subscription, approved on a sheet Genex draws, with the game just calling `generate()`. The `genex-tool-llm` card owns the rest: it checks the lane with `npx genex llm models` first, then runs `npx genex init --convert` (a hosted game is a static browser build, so a local server holding a key can never ship).

Never wire a model into a shipped game on a key or an account of the user's own - every visitor would spend their money with nobody approving it. And player-funded generation returns text or JSON only: 3D models, images, video and audio stay the asset lanes above, generated by you on the user's meter.

## Costs

`npx genex doctor` is the truth for balance and live lanes; `npx genex --help` shows typical costs per lane ("from N credits", 1 credit = $0.01). A 402 means the balance ran out: "When credits run short" above says what follows. Failed generations refund automatically.

## When NOT to use it

- The user already has a dedicated pipeline or asset source for that need - use theirs; Genex fills gaps, it does not replace their tools.
- An asset already landed - never re-generate what you have; wire it in.
- Anything that is not an asset: Genex does not touch the user's code, build, or hosting unless they ask.

## The end

When the game is done, Genex can also put it live on the web at its own address - free, and only if the user asks.
