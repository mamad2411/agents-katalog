---
name: frame-judge
description: Command-only. Runs only when the user invokes it by name (/frame-judge, $frame-judge, @frame-judge, or "use frame-judge"). Never load it on your own for ordinary UI, animation or video work. When invoked, you build or fix the frontend, animation or video, render it, capture screenshots and frame sheets, and a separate code-blind critic subagent judges only the pixels against the user's original words, checking every ask in the request, with evidence for every finding, inside a capped revise loop. Works in Claude Code, Cursor, Codex, ChatGPT, Antigravity and Claude apps.
license: Apache-2.0
compatibility: Needs Node 18+ and ffmpeg. Page capture uses Playwright, or with Node 22+ an installed Chrome, Edge or Chromium (no install). Critic: a fresh subagent (Claude Code, Cursor, Codex, ChatGPT desktop, Antigravity) or a sandboxed claude / agy process. Chat apps (claude.ai, ChatGPT web) use relay mode.
metadata:
  version: "0.7.0"
---

# frame-judge

You don't get to grade your own visual work.

You build it and render it. Then a separate critic judges what actually came out on screen against what the user actually asked for. The critic never sees your code, your reasoning or your opinion of the result. Until it passes the work, or the round cap hits, you don't call it done, polished, smooth or beautiful.

Why: the model that wrote the code reads its intent into the output. It "sees" the walk cycle it meant to write, not the one that renders. A critic that only gets pixels plus the user's words can't do that. It has to look.

`<skill>` below means the folder this file is in (in Claude Code: `${CLAUDE_SKILL_DIR}`). Scripts are plain Node 18+ with no install step. They keep state in `.frame-judge/` under your working directory.

## Before you start: the doctor

```bash
node <skill>/scripts/judge.mjs doctor
```

It prints the app you're in, what can capture pages (Playwright, or your installed Chrome/Edge with no install), whether ffmpeg is there, and which critic runners exist. Then read **only your app's section** of [references/platforms.md](references/platforms.md):

| You are running in | Critic | Section |
|---|---|---|
| Claude Code: CLI, Claude desktop app (Code tab), IDE extension | `critic-sandbox.mjs` (enforced isolation), else the `frame-critic` subagent | Claude Code |
| Cursor: IDE or Cursor CLI | `critic-sandbox.mjs` if the doctor found `claude` or `agy`, else the `frame-critic` subagent (read-only) | Cursor |
| Codex: CLI, IDE extension, ChatGPT desktop app in Codex mode | `critic-sandbox.mjs` if the doctor found `claude` or `agy`, else the `frame_critic` agent | Codex |
| Antigravity: app, IDE, `agy` CLI | `critic-sandbox.mjs --runner agy`, or `invoke_subagent` | Antigravity |
| Claude Cowork, ChatGPT Work | a fresh subagent | Claude app / ChatGPT app |
| claude.ai chat, ChatGPT Chat | relay: the user runs the critic in a fresh chat | Chat apps |

## The loop

| Step | What | Who |
|---|---|---|
| 0 | Lock the user's request, verbatim | you |
| 0b | Ask "unsloppy?" and "pick from directions?". If yes, a scout researches the AI defaults to avoid | you, the user, a scout |
| 1 | Build (or build 2 to 3 directions, and a blind critic picks one) | you, then a critic |
| 2 | Render and capture: screenshots, audit overlays, frame sheets, motion paths and curves | scripts |
| 3 | Mechanical self-check: it renders, nothing blank, no runtime errors | you |
| 4 | Bundle a code-free review packet | script |
| 5 | Ask which model the critic runs on, if the platform allows it (once) | you, then the user |
| 6 | Critic reviews the bundle | a fresh critic: sandboxed process, or subagent |
| 7 | Gate validates the review and decides | script |
| 8 | Answer every must-fix finding, then back to step 2 | you |
| 9 | Report the critic's verdict, not your opinion | you |

Default cap: 3 critic rounds.

## 0. Lock the brief

```bash
node <skill>/scripts/judge.mjs init --brief-file request.txt --kind frontend,motion
```
Use `--brief "..."` for inline text, or `--brief-file -` to read stdin.

- **Verbatim.** Save the user's message as written: typos, caps, everything. Never paraphrase, summarize or "clarify" it. The critic judges against their words, not your reading of them.
- **Later clarifications** from the user go in with `judge.mjs brief --add "<their exact words>"`. Your own assumptions never go in.
- **Reference images** the user gave you: add `--ref mock.png` (repeatable) so the critic can compare against them.
- **`--kind`** picks the rubrics: `frontend` for pages and UI, `motion` for any animation, `video` for clips and edits. Leave it out to auto-detect from the captures.
- **`--critic-model`** if the user already named one.
- **`--bar`**, the quality bar, from 1 (off) to 5. Default `3`: every rubric criterion the critic scores must reach "acceptable", or it becomes a must-fix. Use `--bar 4` when the user asks for production quality, "polished", "professional" or similar: then "not broken" isn't enough, and every criterion has to reach what a picky senior designer would defend. Change it later with `judge.mjs set bar N`.

This creates `.frame-judge/` (it git-ignores itself) with `brief.md` and `ledger.json`. The ledger survives context compaction. If you lose track, run `judge.mjs status`.

## 0b. Ask about unslop mode (before building)

Ask the user once, in these words:

> Do you want it unsloppy? (experimental: may decrease quality and will spend more tokens)

When the brief leaves the design open (a landing page, a hero, a logo animation, "make it look good"), also ask:

> Want me to build 2 or 3 different directions first and have a blind critic pick the strongest? (more tokens, usually a better starting point)

Skip that question when the user specified the design or gave reference images, or for a fix to existing work.

On Claude Code, ask with AskUserQuestion, and put the critic-model question from step 5 in the same prompt, so the user is interrupted once and step 5 is already done when you get there. Elsewhere, ask them all in one chat message. Skip whichever the user already answered.

- **No:** carry on. Unslop is off by default.
- **Yes:**
  1. Run `judge.mjs set unslop on`, then `judge.mjs scout`. It prints a message for a **slop scout**: a fresh subagent with web search that finds out how AIs typically get this kind of request wrong.
  2. Send the scout that message and nothing else. The same rules as for the critic apply: fresh agent, no fork, nothing added. Use the critic's model if one is set.
  3. Save its reply, then run `judge.mjs avoid --file <reply>`. That rejects lists without real sources.
- **No web search available:** tell the user unslop can't run here, and continue without it.

The avoid list lands in `.frame-judge/avoid.md`, and it's included in every review bundle, so the critic checks the work against it too.

"Experimental" because steering away from defaults can push a build toward odd choices, and the scout costs an extra agent run with web searches.

## 1. Build

If unslop is on, read `.frame-judge/avoid.md` first.
- Design around each pattern. Don't just invert it: the goal is work that fits the brief, not work that's merely different.
- Anything the user explicitly asked for beats the list.

Before building, read the section of [references/craft.md](references/craft.md) for your medium, once per session. It covers what critics flag most: spacing, type, AI-template tells, easing, walk cycles, video pacing.

For anything animated, make time an explicit input: a timeline you can seek, or a `window.frameJudgeSeek(ms)` hook. That makes capture frame-exact, and it turns HTML into video for free.

### Directions first: the blind pick (if the user said yes)

The first idea anchors everything after it, and polishing the wrong direction for three rounds wastes them. So:
1. Build 2 or 3 **genuinely different** directions (layout, type, color or motion concept: not one design in three colors), each in its own folder or file.
2. Capture each one the same way, with fewer images than a full round: one viewport set (`--viewports desktop,mobile --slices 2`), or one motion capture each.
3. `node <skill>/scripts/judge.mjs pick --variant .frame-judge/cap/dir-a --variant .frame-judge/cap/dir-b [--variant ...]` builds a blind bundle: labels are shuffled, and folder names never reach the critic.
4. Run the critic exactly as in step 6, on the pick: `critic-sandbox.mjs --pick`, or a fresh subagent with the message `pick` printed. Gate it with `judge.mjs pick-gate --review .frame-judge/pick/pick.json` (add `--transcript auto` on Claude Code).
5. Build on the winner, fold in its `carry_over` items, and delete or set aside the others. Then the normal loop starts at step 2. A `tie` goes to the user.

## 2. Render and capture

**Pages and UI.** This uses Playwright if it's installed. Otherwise, with Node 22+, it drives the Chrome, Edge or Chromium already on the machine over DevTools, with nothing to install. Setup and options: [references/capture.md](references/capture.md).
```bash
node <skill>/scripts/capture-page.mjs http://localhost:5173 --out .frame-judge/cap/page
```
Defaults are desktop 1440×900, tablet 768×1024 and mobile 390×844, captured screen by screen. Options:
- `--actions states.json` for hover, menu and error states
- `--color-scheme dark`
- `--reduced-motion`
- local files work as well as URLs

Each screen is also **audited** from the live page: text contrast below WCAG AA, touch targets under 44×44 px on touch viewports, text cut off by its container, and elements sticking out past the viewport edge. Screens with hits get an `audit-*` overlay image with the boxes drawn on; the critic decides which matter. The selectors behind each box are in `capture.json` under `builder_only.audit`, for you. `--no-audit` turns it off.

**Animation on a page.** This is frame-exact (fake clock plus Web Animations seeking) and encodes to MP4:
```bash
node <skill>/scripts/capture-page.mjs scene.html --out .frame-judge/cap/anim --animate 3000 --fps 30 --selector "#hero"
```
It also **measures motion**: every frame, it records the box and opacity of the elements that move (`--track auto`, the default, picks up to 4; or `--track "#robot,.leg-left"`), then draws `motion-paths.png` (each element's path, one dot per frame, so spacing shows easing) and `motion-curves.png` (distance, speed, opacity and scale over time). Easing and pops stop being a guess from filmstrips. Canvas and WebGL motion isn't tracked; for that, rely on the strips.

**Any video**, including that MP4:
```bash
node <skill>/scripts/video-frames.mjs .frame-judge/cap/anim/animation.mp4 --out .frame-judge/cap/anim-views --as motion
```

What you get:
- **Viewport slices** instead of one giant full-page image, which would get downscaled into mush.
- **State shots** from your actions file.
- **A timestamped contact sheet.**
- **Filmstrips**: frames sampled at 12 fps by default, plus full-rate strips around any sudden jump or stall the script detects (`--motion-fps source` gives every frame everywhere). Sampled means a one-frame glitch can fall between tiles, which is why the event detection exists.
- **Motion trails**: whatever should stay still stays sharp, and whatever slides smears.
- **Objective numbers**: duration, fps, black or frozen segments, horizontal overflow, broken images.

Capture what the user will experience: every viewport they'd use, the states that matter, the whole animation. The critic can't flag what you didn't show it. Leaving out the ugly parts is exactly the cheating this skill exists to stop.

## 3. Mechanical self-check

Before you spend a critic round, check and fix the binary stuff:
- it renders
- no blank or black frames
- nothing in `builder_only` in each `capture.json` (console errors, failed requests, screens that couldn't be reached)
- the right duration and size
- `horizontal_overflow_px` and `broken_images` are zero, and no `unreachable_screens`
- the `audit` counts: fix what's plainly a bug (body text at 2:1 contrast, a nav of 18 px icons) before the critic sees it. Leave judgment calls to the critic.

That's the whole list. You don't get to decide it looks good and skip the critic.

## 4. Bundle

```bash
node <skill>/scripts/judge.mjs bundle .frame-judge/cap/page .frame-judge/cap/anim .frame-judge/cap/anim-views
```
Pass the animation capture folder too (`cap/anim`): that's where the motion paths and curves are.

This writes `.frame-judge/round-N/bundle/`. It holds only visual files (png, jpg, webp, gif, plus video if you pass `--include-video`) and these text files:
- `brief.md`, with code blocks stripped
- the rubrics
- `CRITIC.md`, the critic's instructions
- `manifest.json`, with citable artifact IDs
- `prior.json`, from round 2 on: open findings *without* your "fixed" claims, so the critic checks for itself
- from round 2 on, `zoom-*` close-ups: where an open finding boxed a region, the same region of this round's capture, enlarged

The script won't open a new round while must-fix findings are unanswered, or past the round cap. It prints the exact message to send the critic.

**Image budget:** aim for 20 images or fewer per round. Claude tightens per-image limits past 20 images in one request. Every image costs about ⌈w/28⌉×⌈h/28⌉ tokens; a 1440×900 shot is around 1.7k. Contact sheets and filmstrips pack 12 to 16 frames into one image, so lean on them. `--slices 3` trims long pages.

## 5. Choose the critic's model (only where the platform supports it)

Ask only if your app lets you pick the critic's model, and only once, before round 1. If you asked it together with the unslop question in step 0b, or the user already named a model, don't ask again. Save the answer with `judge.mjs set critic-model <alias>` and reuse it every round.

- **Claude Code, Claude apps:** AskUserQuestion, in the same prompt as the unslop question: Sonnet (balanced, recommended), Opus (sharpest eye, most quota), Haiku (cheapest, misses subtle issues), Same as me.
- **Cursor, Codex, ChatGPT desktop:** ask in chat; offer the models the app lists, or "same as me".
- **Antigravity:** with `critic-sandbox.mjs --runner agy`, any id from `agy models` (its Claude Sonnet is the recommendation). With `invoke_subagent`, there's no per-spawn choice: tell the user it runs on the agent file's setting.

Be straight about the trade-off. A weaker critic is cheaper, but it hallucinates more defects and misses subtle ones. The gate catches fake evidence; it can't catch bad taste. Exact syntax per app: [references/platforms.md](references/platforms.md).

## 6. Run the critic

Use a **fresh** critic every round, so it has no memory beyond `prior.json` and no stake in its earlier calls. Send it the message `bundle` printed, and nothing else:

> You are the frame critic. Your bundle is `<abs path>`. Read `<abs path>/CRITIC.md` and follow it exactly. Open nothing outside that folder. Reply with the review JSON only.

- **Add nothing.** No summary of what you built, no "focus on the header", no "I fixed the legs". Your opinion is the one input the critic must never get. If the user wants something checked, it's already in the brief, in their words.
- **No forks.** Never run the critic as a fork or anything else that inherits context. It would see your whole conversation, code included.

Which critic to run: take the first of these that the doctor says you have.

1. **The sandbox**, when the doctor found the `claude` or `agy` CLI. `node <skill>/scripts/critic-sandbox.mjs --model <the chosen model>` runs the critic as a separate headless process on a private copy of the bundle, records its real tool calls, saves the review and gates it itself. **Skip step 7** and go by the decision it prints.
   - `--runner claude` (default): only the Read tool, plus a hook that blocks any read outside the copy. Code-blindness is **enforced**.
   - `--runner agy`: its reads are audited afterwards, and a peek outside the copy voids the review. Code-blindness is **verified**.
2. **The installed `frame-critic` agent**, as a subagent. It's limited to reading files. Its name is `frame-judge:frame-critic` when the skill came in as a Claude Code plugin, and `frame_critic` in Codex.
3. **A general-purpose subagent** with the same message.

With 2 and 3, code-blindness rests on the critic's instructions. On Claude Code, the transcript audit in step 7 still catches a critic that peeked. In Cursor, Codex and Antigravity subagents nothing checks it, so say so in your report. Save the subagent's reply, untouched, to `.frame-judge/round-N/review.json`.

No subagents and no CLI? See "When the platform can't do it" below.

## 7. Gate

```bash
node <skill>/scripts/judge.mjs gate --review .frame-judge/round-N/review.json --reviewer subagent --transcript auto
```
On Claude Code, `--transcript auto` finds the critic subagent's transcript, so the gate counts the images it really opened (not the ones it claims) and voids the review if it touched anything outside the bundle. Elsewhere, leave the flag off; coverage is then self-reported, and the report says so. (`critic-sandbox.mjs` passes its own transcript automatically.)

The gate decides, not the critic's mood and not you. It:
- **Rejects** findings that cite artifact IDs that don't exist or that the critic never opened, findings with no evidence, brief quotes that aren't in the brief, and bad severity or confidence values.
- **Checks coverage:** a pass only counts if the critic opened every image, verified from its transcript where one exists, otherwise from its own `opened` list.
- **Checks the brief, ask by ask:** the critic must list every explicit ask and constraint in the brief, quoted verbatim and marked `met`, `partial`, `missing`, `contradicted` or `cannot_tell`, with evidence. Quotes that aren't in the brief are dropped. An unmet ask without its own finding becomes a must-fix; a `cannot_tell` ask becomes a verify item (capture it). A pass without this list is sent back. From round 2 on, an ask an earlier critic listed and this one left out counts as `cannot_tell`, not as met.
- **Holds the quality bar:** any rubric criterion scored below the bar (default 3, see step 0) becomes a must-fix **lift**, `R1-L1`, even when nothing is broken. Its fix is the critic's own `elevate` entry for that criterion: what would raise it, in visual terms, with a boxed frame. A lift resolves itself once a later critic scores that criterion at the bar. Elevate entries for criteria already at the bar are printed as optional upgrades.
- **Draws the findings for you:** every finding the critic boxed is drawn onto a copy of its frame, plus an enlarged crop, in `round-N/annotated/`. The gate prints the paths under each finding. Look at them before you fix: "the nav icons" is vague, a red box isn't.
- **Hands back what pixels can't show:** asks the critic marks `not_visual` ("no frameworks", "one HTML file", "loads in under a second") are listed for you. No critic checked them. Check each one yourself, with a command or by reading the file, before you report.
- **Checks isolation:** with a transcript, any read outside the bundle voids the review (`RERUN_CRITIC`).
- **Sorts** the rest:
  - **must-fix**: blocker or major, confidence 0.6 or higher
  - **verify**: blocker or major below 0.6. Recapture closer; don't blind-fix.
  - **polish**: minor
  - **ignored**: nits
- **Checks** that `CRITIC.md` and the rubrics were not edited, so nobody softened the judge.
- **Updates** the ledger and prints one decision:

| Decision | Meaning | You |
|---|---|---|
| `PASS` | No must-fix left, nothing from the brief missing, every scored criterion at the bar | Report (step 9) |
| `SELF_PASS` | Same, but from a self-review fallback | Report, and say it wasn't independent |
| `REVISE` | Must-fix items exist | Step 8, then a new round |
| `RETHINK` | Critic says the approach is wrong at the root | Tell the user before rebuilding |
| `STOP_MAX_ROUNDS` | Cap hit, still failing | Report what's open, ask whether to continue |
| `STOP_PLATEAU` | This round resolved nothing | Stop circling. Report, ask |
| `RERUN_CRITIC` | Review unusable (no JSON, mostly bogus evidence), a pass from a critic that skipped images or skipped the asks list, or a critic that read outside its bundle | Run a fresh critic on the same bundle |
| `STOP_CRITIC_UNRELIABLE` | Second unusable review | Suggest a stronger critic model or a fallback |

## 8. Revise

Work through the must-fix items by ID, blockers first. Answer every one before the next round:
```bash
node <skill>/scripts/judge.mjs respond R1-F2 fixed "contact foot planted for 4 frames"
node <skill>/scripts/judge.mjs respond R1-F4 disputed "gutters are equal on both sides" --evidence crop.png
node <skill>/scripts/judge.mjs respond R1-F6 wont-fix "user asked for this gradient" --quote "purple to blue gradient"
```
- **`disputed`** needs **visual** evidence, such as a crop or extra frames. It goes into the next bundle and the next critic rules on it. "The CSS says 16px" is not evidence; pixels are.
- **`wont-fix`** needs a verbatim quote from the brief that the fix would violate.
- **Fix causes, not captures.** Never change the capture to dodge a finding: no cropping out the broken footer, dropping the mobile viewport, or trimming the clip.
- **Verify items and critic `requests`:** run `judge.mjs requests`. It turns each one into a capture command: a re-render of the boxed region at 3x (`capture-page --zoom`), a full-frame-rate strip of a time window, or another viewport. `--run` runs them. Add the folders it prints to the next `bundle`, next to your full recapture. A request it can't turn into a command (a state shot) tells you what to add to your actions file.
- **Lifts:** they're how "fine" becomes "good". Apply the critic's elevate change, not a token tweak; the next critic re-scores the criterion from scratch.
- **Don't regress** what the critic listed under `keep`.
- **Polish and nits:** fix polish if it's cheap. Ignore nits unless they're trivial.

Then recapture **everything**, not just the part you touched, because fixes break other things. Then bundle, critic, gate. From round 2 on, `bundle` adds the previous round's frames behind each open must-fix finding (`before-*`), so the critic compares before and after instead of taking your word for it.

## 9. Report

Lead with the verdict. `judge.mjs status` prints the block for you:

```
Critic: PASS on round 2 of 3 (subagent, model sonnet, code-blind)
Brief: 6 of 6 explicit asks met, each checked by the critic against the captures
Scores (critic, bar 4/5): layout 3→4 · typography 4 · motion 2→4
Round 1 gut reaction: "The legs scissor like a broken folding chair."
Fixed: R1-F1 foot sliding · R1-F2 hero text clipped at 390px · R1-F5 unrequested testimonials removed
Open: R2-F3 (minor) nav icon sits 2px low
Disputed: R1-F4, upheld by the critic, fixed in round 2
```

- If it didn't pass, say so first and list what's still open.
- Never describe your own output as great, smooth, polished, clean or pixel-perfect. Quote the critic.
- If the block has a "Not visual" line, those asks were outside what the critic can see. For each one, say how you checked it ("no framework: `index.html` loads no scripts but its own"), or that you didn't. Never fold them into the critic's count.
- If the review wasn't independent (self-review), or ran on a different model than the user chose, say so.

## When the platform can't do it

Step 6 covers the normal cases: the sandbox, then a subagent. When neither exists, or the subagent can't run on the model the user chose, use the first of these that works, and tell the user which one you used:

1. **Subagent on the default model.** The platform can't choose per subagent; say so.
2. **Another headless critic.** `codex exec` (or any CLI agent that can read images) started inside the bundle folder; gate with `--reviewer headless`. The command is in platforms.md.
3. **Human relay** (also how chat apps such as claude.ai and ChatGPT Chat work). `bundle` also writes `packet.md`. The user pastes it and the images into any fresh chat with a vision-capable model, then hands you the JSON. Run `gate --reviewer human`.
4. **Self-review**, last resort. Re-read nothing from the project and play the critic from the bundle alone. `gate --reviewer self` can only ever return `SELF_PASS`, and your report must say the work wasn't independently reviewed.
5. **No vision at all.** You can't judge visuals. Say so, hand over the captures, and let a human look.

## Files

| File | When |
|---|---|
| [references/craft.md](references/craft.md) | Before building (the section for your medium) |
| [references/capture.md](references/capture.md) | Capture setup, states files, frame-exact animation, HTML to video, ffmpeg recipes |
| [references/platforms.md](references/platforms.md) | Spawning the critic, the model question and fallbacks, per platform |
| `scripts/judge.mjs` | doctor, init, brief, set, scout, avoid, pick, pick-gate, bundle, gate, requests, respond, status |
| [references/pick-brief.md](references/pick-brief.md), `references/pick.schema.json` | The blind pick's instructions and output format. The critic reads them itself. |
| `bench/run.mjs` (repo only, not installed) | Seeded-defect benchmark: known planted problems plus clean controls, through the real pipeline. Measures what the critic catches. |
| `scripts/capture-page.mjs`, `scripts/cdp.mjs` | Page capture: Playwright, or an installed Chrome/Edge over DevTools |
| `scripts/critic-sandbox.mjs`, `scripts/critic-guard.mjs` | The sandboxed critic (claude or agy), and the guard pinned to the claude critic |
| `scripts/install.mjs` | Installs the skill and critic agents for every app on the machine; `--zip` builds the chat-app upload |
| [references/scout-brief.md](references/scout-brief.md) | The slop scout's instructions (unslop mode). The scout reads them itself. |
| [references/critic-brief.md](references/critic-brief.md) | Copied into every bundle as `CRITIC.md`. Don't edit it to go easier on yourself; the gate checks it. |
| `references/rubric-*.md` | What the critic scores. Copied into bundles automatically. |
| [references/review.schema.json](references/review.schema.json) | The critic's output format, usable with `--json-schema` / `--output-schema` |
| `agents/` | Critic agent definitions for Claude Code, Cursor, Codex and Antigravity |
