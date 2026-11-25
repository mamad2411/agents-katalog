---
name: higgsfield-studio
description: "Make images, video, audio, 3D and ads with Higgsfield, and spend the credits on purpose. Triggers: 'generate an image with higgsfield', 'make a video from this photo', 'animate this image', 'reframe this video to vertical', 'make an ad for my product', 'make a UGC video', 'score this video's hook', 'create a 3D model from these photos', 'how many Higgsfield credits are left', 'what have we spent on Higgsfield', 'higgsfield'. Every paid job is priced by Higgsfield first, never paid for twice, measured after, and written to a ledger in the project. A reserve stops a runaway loop from emptying the account. Built on Higgsfield's official skills and command line tool, which signs in through the browser, so no key is ever typed into the chat. Works on macOS, Windows and Linux."
license: MIT
compatibility: "Requires Node 18 or newer and the Higgsfield command line tool (npm @higgsfield/cli). Run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for both and install what is missing. Needs network access and a Higgsfield account. Generating spends that account's credits."
metadata:
  author: itqanlab
  version: 1.1.0
  category: media
  short: "Higgsfield images, video and ads, on a budget"
  starter: "make a short video from this product photo without wasting credits"
---

# Higgsfield Studio

Images, video, audio, 3D and ads from Higgsfield, through its official command line tool, `higgsfield`. Higgsfield is paid by the credit, so every paid job goes through one script, `scripts/hf.mjs`. It asks Higgsfield for the price before running, never pays twice for the same request, and records what each job really cost. Never start a paid `higgsfield` command any other way from this skill.

This plugin has more skills next to this one. Hand over to them when the request fits:

| Request | Skill |
|---|---|
| Train a person's face once, reuse it in images and video | `higgsfield-studio-soul-id` |
| Product photos: studio, lifestyle, Pinterest, hero banner, ad pack, try-on | `higgsfield-studio-product-photoshoot` |
| Marketplace listing images and A+ modules | `higgsfield-studio-marketplace-cards` |
| A brand identity: logo, palette, type, mockups, brandbook | `higgsfield-studio-brandkit` |
| YouTube thumbnail, Shorts or Reels cover | `higgsfield-studio-youtube-thumbnail` |
| A narrated explainer video from a topic or document | `higgsfield-studio-video-explainer` |
| A website, web app or browser game, built and hosted by Higgsfield | `higgsfield-studio-websites` |

They all spend through this skill's script, `scripts/hf.mjs`.

## Who you are doing this for

Assume the person has never opened a terminal. **You run the commands; they never do,** except signing in once. Report in plain words: "the clip is in `video/intro.mp4`, it cost 7.5 credits, 64 are left." No JSON, no job ids, no model ids unless they ask. Reply in the language they write in. Command flags stay in English.

## Before anything else

```
sh scripts/setup-deps.sh --check
node scripts/hf.mjs check
```

The first checks Node 18+ and the `higgsfield` tool. If either is missing, `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the install command and asks first; `--yes` skips the question.

The second checks the sign-in. If it says Higgsfield is not signed in, the user signs in once with `higgsfield auth login`. It opens the browser. Ask them to run it, or run it for them and tell them to finish in the browser. Never print the sign-in token, never open the CLI's credential file, and never ask for a password or key in the conversation.

## Commands

Free:

```
node scripts/hf.mjs account                      plan, credits, reserve, recent spends
node scripts/hf.mjs cost <model> [--param v]...  the price Higgsfield gives, nothing runs
node scripts/hf.mjs cost workflow <name> [...]
node scripts/hf.mjs ledger                       what has been spent, by kind and by tag
node scripts/hf.mjs run <higgsfield command>     any free command, for example:
     run model list --video        run model get seedance_2_5     run workflow list
     run preset list soul-v2       run voices list                run upload list --image
     run marketing-studio avatars list            run generate list --size 5
```

Paid, quoted first:

```
node scripts/hf.mjs create <model> --prompt "..." [--param v]... [--image FILE] --out FILE
node scripts/hf.mjs workflow <name> [--param v]... --out FILE
node scripts/hf.mjs photoshoot ...   node scripts/hf.mjs cards ...   node scripts/hf.mjs dtc ...
```

Outward or not undoable, only after the user says yes:

```
node scripts/hf.mjs act <higgsfield command...> --yes
```

`act` covers Soul training, every website create, deploy, publish, rename, contest and secret change, `repo-access` (it prints a scoped token: never show it), and changing the billing workspace. `run` refuses all of these and every paid command, and names the right one.

Every paid command also takes `--dry` (show the price and the request, run nothing), `--max N` (refuse above N credits), `--fresh` (skip the cache, needs `--why`), `--yes` (allow a job Higgsfield cannot price), `--tag NAME`, `--why "..."`, `--out PATH` and `--prompt-file FILE` (read a long prompt from a file, so quotes and line breaks survive).

Parameters pass straight through to Higgsfield, so `--aspect_ratio 9:16 --duration 5 --resolution 720p` work as the model defines them. Check a model's parameters with `run model get <model>` once, before guessing. A local file in any flag is uploaded once, for free, and reused by id after that.

## Reading the official guides in `references/`

The files in `references/` are Higgsfield's own guides. They show commands as `higgsfield generate create ...`. Run the paid ones through the script instead:

| The guide says | Run |
|---|---|
| `higgsfield generate create X ... --wait` | `node scripts/hf.mjs create X ...` |
| `higgsfield generate workflow X ...` | `node scripts/hf.mjs workflow X ...` |
| `higgsfield generate cost ...` | `node scripts/hf.mjs cost ...` |
| `higgsfield product-photoshoot create ...` | `node scripts/hf.mjs photoshoot ...` |
| `higgsfield marketplace-cards create ...` | `node scripts/hf.mjs cards ...` |
| `higgsfield marketing-studio dtc-ads generate ...` | `node scripts/hf.mjs dtc ...` |
| `... < prompt.txt` (prompt on stdin) | add `--prompt-file prompt.txt` |
| anything else that only reads | `node scripts/hf.mjs run ...`, or `higgsfield ...` directly |

`--wait` and `--json` can be left in or out. The script adds what each command needs.

## How credits are protected

1. **Price first.** Higgsfield prices any model or workflow for free (`generate cost`), DTC ads with `--cost-only`, and photoshoot and marketplace-card runs by planning them first with `--enhance-only` (free, measured: the balance did not move) and pricing each planned image. The price is shown before anything runs. A job Higgsfield cannot price (Virality Predictor, Soul training, website actions) needs `--yes`, which means the user said yes.
2. **Never pay twice.** The cache key is the command, every parameter and a hash of every local file used. The same request returns the files already paid for, at 0 credits. `--fresh` is the only way past it, and it needs a reason in `--why`.
3. **Measure after.** Higgsfield's transaction list shows what each job cost but not which job it was. The script counts the spends that appear after the newest one it saw before the job, and falls back to the balance before and after. A job run at the same time from another place on the same account also counts. The ledger's `measured_by` says which method was used.
4. **Keep a reserve.** A job that would leave fewer than `HF_RESERVE` credits (default 5) is refused. Basic plans hold tens of credits, so the default is small on purpose. Change it only when the user says so.
5. **Spend from the right account.** The sign-in is machine-wide, and a free account looks just like the paid one. A project that names its account in `.higgsfield/config.json` (`{"account": "...", "reserve": 10}`, or `HF_ACCOUNT`) has paid jobs on any other account refused before they run. Offer to write that file when a project has a paid account.
6. **One paid job at a time.** Jobs in the same project wait for each other, so each one's measured cost is its own.
7. **Never wait blind.** `create` saves the job id the moment it exists and polls with a deadline (`--timeout`, 900 seconds by default). If it stops early, run the same command again: it picks the job up and does not pay twice.
5. **A failed job is still recorded.** If Higgsfield fails after starting, the script still measures and writes the row, with `ok: false`.

The cache, the upload list and the ledger live in `.higgsfield/` in the folder the command runs from, so each project keeps its own record. `HIGGSFIELD_HOME` moves it. `ledger.jsonl` is worth keeping in version control. `cache/` holds the media files: tell the user to add `.higgsfield/cache/` to `.gitignore`.

## What things cost

Prices Higgsfield quoted on 2026-10-12 at each model's default settings. Settings change the price a lot (Seedance 2.5: 35 credits at its default length, 84 at 12 seconds), so always quote the real request.

| Kind | Model | Quote |
|---|---|---|
| Image, draft | `z_image` | 0.15 (measured: 0.15) |
| Image, Soul | `text2image_soul_v2`, `soul_cinematic` | 0.12 |
| Image, default | `gpt_image_2_5` | 0.25 |
| Image, edit with references | `nano_banana_2_lite` | 1 (measured: 1, with one image) |
| Image, cartoon and characters | `nano_banana_flash` | 1.5 |
| Image, vector and logos | `recraft_v4_1` | 1.25 |
| Image, faces and character sheets | `seedream_v5_pro` | 2.5 |
| Image, top Nano Banana | `nano_banana_pro` (alias `nano_banana_2`) | 2 |
| Image, used by product photoshoot | `gpt_image_2` at 2k | 6.5 each |
| Audio | `seed_audio` | 0.1 |
| Video, fast | `kling3_0_turbo` | 7.5 |
| Video, 4K | `seedance_2_0` | 22.5 |
| Video, default | `seedance_2_5` | 35 |
| Video, Veo | `veo3_1` | 32 |
| Workflow | `reframe`, 5 s at 720p | 25.5 |

Only the two rows marked measured were paid for and checked. The rest are Higgsfield's own quotes.

## Picking a model

Higgsfield's guide, `references/model-catalog.md`, has the full list. Its defaults:

- **Image:** `gpt_image_2_5` for most work, design, UI, banners and text in the image. `nano_banana_flash` (Nano Banana 2) for cartoon and illustrated characters. `text2image_soul_v2` for editorial and lifestyle people, with a Soul from `higgsfield-studio-soul-id`. `soul_cinematic` for cinematic stills. `seedream_v5_pro` for character sheets and face edits. `soul_location` for places with no people. `recraft_v4_1` for logos, icons and vector-like art. Cheaper or faster when asked: `nano_banana_2_lite` for reference edits, `z_image` for drafts.
- **Video:** `seedance_2_5` by default (modes `t2v`, `omni_reference`, `video_edit`, `video_extension`; 4 to 30 seconds, up to 1080p). `seedance_2_0` only for 4K. Cheaper or faster when asked: `kling3_0_turbo`, Veo 3.1 Lite, Seedance 1.5 Pro. Reframing or sketch edits of an existing video are workflows (`reframe`, `draw_to_video`): see `references/workflows.md`.
- **Ads, UGC, unboxing, product demos, TV spots:** Marketing Studio (`marketing_studio_video`, `marketing_studio_image`). See below.
- **Audio:** `seed_audio` for sound effects, ambience, voice-like audio and music-like audio. `sonilo_music` and `mirelo_text_to_audio` only when named.
- **Voice-over, voice changing and dubbing:** Higgsfield resells ElevenLabs for these (text to speech on Eleven v4, and the `voice_change` and `dubbing` workflows). When the `elevenlabs-studio` skill is installed, use it instead: it goes to ElevenLabs directly and measures each voice-over's exact cost. Use Higgsfield's only when that skill is missing or the user asks for Higgsfield by name.
- **3D:** `multi_image_to_3d` with 1 to 4 photos of the object (`--image` repeated, `--should_texture true` for texture).
- **Scoring a finished video:** Virality Predictor, `brain_activity`, with `--video`. It returns a text report, not media. It cannot be priced in advance, so ask first and pass `--yes`.

Note: `nano_banana_2` is an alias for Nano Banana Pro. Nano Banana 2 is `nano_banana_flash`.

## The working order: cheap first

1. **Look before you pay.** Lists, model parameters, presets, voices and previous jobs are free. `run generate list` shows past jobs: the result may already exist.
2. **Price the real request** with `--dry`, with every parameter the final job will use. Show the user the price for anything over about 5 credits.
3. **Draft cheap, then render.** Try an idea on `z_image` or a Soul model (well under 1 credit) before a 6-credit image. For video, settle the first frame as an image first, then animate it with `--start-image`. A frame costs far less than a re-rendered clip.
4. **Short before long.** A 5-second test before a 12-second video. Duration and resolution drive video prices.
5. **One variant, then more.** Make one, look at it, then ask for more. Never use a count above 1 on the first run.

## Marketing Studio

For ads: avatars (presenters), products (from a URL or photos), hooks and settings (reusable openings and scenes), ad references (a video to follow), brand kits (a brand's look, from its website) and ad formats. The free lists:

```
node scripts/hf.mjs run marketing-studio avatars list
node scripts/hf.mjs run marketing-studio products list
node scripts/hf.mjs run marketing-studio hooks list
node scripts/hf.mjs run marketing-studio ad-formats list
```

Importing a product from a URL: `run marketing-studio products fetch --url <url> --wait`. A video ad: `create marketing_studio_video --prompt "..." --product_ids @ids.json --mode ugc --duration 15 --aspect_ratio 9:16`. A branded ad image from the DTC Ads Engine: `dtc --prompt "..." --format-id <id> --brand-kit-id <id>` (the format is required, so ask the user to pick one from `ad-formats list`). Each part has a guide: `references/marketing-modes.md`, `references/marketing-avatars.md`, `references/marketing-products.md`, `references/marketing-setup-items.md`, `references/marketing-ad-references.md`, `references/marketing-brand-kits.md` and `references/marketing-dtc-ads.md`.

## Rules

- **Cache first.** Check the ledger and `run generate list` before changing a word of a request that was already made.
- **`--dry` before any batch,** and tell the user the total.
- **`--max N` on every paid job,** set a little above the quote.
- **Tag every job** with `--tag` and `--why`. A ledger row with no reason cannot be learned from.
- **Ask before a large spend.** Anything over about 10 credits, or 10% of what is left, needs the user's yes first.
- **Ask before anything outward.** Deploying, publishing, renaming a site, entering a contest, training a Soul or changing the billing workspace: say what will happen, wait for yes, then use `act ... --yes`.
- **Truthful content.** Never generate a real person's likeness without their consent, and never invent claims, results or reviews for an ad.
- **Disclosure.** Generated images, video and voice count as AI-generated material on most platforms. Tell the user to use each platform's AI label when they publish.

## Failure messages

Errors are rewritten for people. Not signed in says how to sign in. A wrong parameter says what Higgsfield rejected and that nothing was charged. A refusal by the reserve or `--max` says nothing was spent. Keep that habit for anything added here.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first, for this skill and every other skill in the plugin.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.

`references/ATTRIBUTION.md` credits the material adapted from Higgsfield's official skills.
