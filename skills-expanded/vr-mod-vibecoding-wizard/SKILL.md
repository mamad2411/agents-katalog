---
name: vr-mod-vibecoding-wizard
description: Setup-wizard workflow for converting a flatscreen game into a full 6DoF motion-controlled VR mod, for total beginners or expert modders. Covers intake, game and framework research, build-on vs from-scratch, environment modes (agentic/desktop/chat), staged build with gates, stereo, camera, controllers, physics hands, holsters, reload, melee, IK, HUD/menus, in-VR settings, and a playtest/bug pipeline. Use whenever the user mentions a VR mod, VR port, playing a flat game in VR, adding motion controls or 6DoF to a game, OpenXR/SteamVR hooking, VR IK, or wants a plan or scaffold for any of these — even without saying "mod." Also use to triage bugs, resume, or package a VR conversion.
---

# VR Mod Vibecoding Wizard

A workflow for taking a flatscreen game and producing a **complete, playable, feature-rich VR conversion** — not a tech demo. The finished **Phase 1 release** means: stereo, 6DoF, motion controllers, physics hands, weapons and interaction, full-body IK, comfort options, HUD and cutscene handling, and an in-VR settings menu, all wired up and working. Tuning and polish come after.

Internally this skill uses **Stages** (0–10) for build steps so the word "phase" stays reserved for the user's release milestones.

## The flow at a glance

1. **Setup wizard** — four short screens; detect what you can, ask the rest.
2. **Research the game** — what it does that the user didn't mention; coverage check.
3. **Research what exists** — frameworks and prior mods; the user chooses build-on or from-scratch.
4. **Prerequisites** — runtime working, backups, version pinned, git.
5. **Scaffold** — folders, living docs, config schema, first status board.
6. **Stages 0–10** — each one: brief → build (implementation loop) → tests → gate → next.
7. **Package** — installer, README, uninstall; Phase 1 done.

Resuming a project starts at whatever step the docs say. Switching environments never changes the step.

## Who you're talking to

This skill serves both someone who has never opened a hex editor and someone who writes engine hooks for fun. Figure out which within the first exchange and adapt — never dumb down the engineering, only the explanation of it.

- **Beginner signals:** doesn't name an engine, asks "is this possible," mentions a headset but no tools, says "I just want to play X in VR."
  Respond by explaining each step's purpose in one plain sentence before doing it, defining terms on first use (see the glossary at the end), doing the technical work yourself, and never asking them to make a technical decision without a recommended default.
- **Expert signals:** names the engine, loader, or graphics API; talks about hooks, offsets, matrices, IL2CPP, pak files.
  Respond tersely, skip explanations, present decisions as options with trade-offs, and expect them to override your defaults.
- **In between:** most people. Explain once, then assume.

Whatever the level, the human is the only one who can wear the headset. Their time in it is the scarcest resource in the project — protect it.

## Operating principles

1. **Write the plan before the code.** Hooking a game engine is guesswork until proven. State a hypothesis, then test it.
2. **Keep an unknowns list.** Whenever you need something only the human can supply — a bone name, whether the game has a photo mode, what their controller is — add it to `docs/QUESTIONS.md` rather than interrupting. Ask in batches at natural pauses.
3. **Never silently downgrade.** Every fallback goes in the decision log with a reason. Quiet fallbacks are how conversions end up mediocre.
4. **Reuse before build.** If a maintained VR framework already exists for this engine, evaluate it before writing from scratch.
5. **Batch the human's headset time.** Playtest scripts, not one-at-a-time "does this feel right?"
6. **Structure is advisory.** If the user says "skip the profile, just hook the camera," do it — but say what's being skipped so the choice is informed.

## Session start: the setup wizard

Run this at the start of a new project, as a wizard: one numbered screen per message, plain language, every question with a *why we ask* and a *default if unsure*. Skip anything already answered or obvious from the conversation. The user should be able to get through the whole thing by answering in a sentence or two per screen, and "I don't know" must always be an acceptable answer that you can work with. Experts can answer all screens at once; offer that up front.

**Screen 1 of 4 — Your game and your gear**
1. Which game? Where did you get it (Steam, GOG, Epic, disc), and does it update itself, or is it a fixed old version? *Why:* the mod is built against one exact version. *If unsure:* tell me the store and I'll work it out.
2. Do you have any other mods installed on it? *Why:* two mods fighting over the camera is a common failure. *If unsure:* "no" is fine.
3. What engine do you think it runs on? *Why:* I'll verify it either way. *If unsure:* skip it — I'll find out.
4. Which headset and controllers? *Why:* button layouts and tracking differ. *Default:* whatever came in the box.
5. **How does your headset connect to your PC?** A cable, Meta Air Link, Steam Link, Virtual Desktop, ALVR, Steam Frame's wireless adapter, or Pico's streaming app? *Why:* this decides which VR software the mod actually talks to and how much performance headroom you have — see the table below. *If unsure:* tell me what app you open on the headset to see your PC.
6. Is your PC on Windows, or Linux/SteamOS? *Why:* the way the mod gets inside the game differs. *Default:* Windows.
7. Your graphics card, and roughly your CPU and RAM. *Why:* VR draws everything twice; wireless adds more load. *If unsure:* the graphics card name alone is enough.
8. Does the game have online play or anti-cheat? *Why:* see the warning below — this can affect your account. *If unsure:* I'll check when I research the game.

**Offer to detect instead of ask (agentic mode only).** Before asking questions 1, 6, and 7, and the VR software parts of 5, offer to look them up on the PC and have the user simply confirm. Say what you'll check, that every check is read-only, and that they'll see the tool's own "allow this command?" prompt for each one — it's a confirmation, not a system permission. If they say no, ask the questions instead; never run the checks without the offer being accepted. Checks worth offering:
- Operating system and version.
- Graphics card, CPU, and RAM.
- Whether SteamVR, Meta's PC app, Virtual Desktop Streamer, ALVR, or Pico Connect are installed, and which OpenXR runtime is currently active — this usually answers the connection question outright.
- Steam library folders and whether the named game is present, its install path, size, and any obvious mod loader files already in it.
- Nothing else. No browsing the user's documents, no reading saves, no network calls beyond what web research needs.
Present results as a short list and ask "does this look right?" Record confirmed values in TARGET_PROFILE.md as confirmed, not assumed.

**Connection methods and what they change**

| Connection | VR software the mod talks to | Latency | Watch out for |
|---|---|---|---|
| Native PCVR (Index, Vive, Reverb, Bigscreen, Pimax) | SteamVR or the vendor's runtime directly | Best; no encoder | Base stations or inside-out tracking must be working before you start |
| Meta Link cable / Air Link | Meta's PC runtime (often the OpenXR default) | Good / moderate | Meta's runtime may be the default instead of SteamVR — confirm which one the mod is actually reaching |
| Steam Link (Quest app) | SteamVR | Moderate | Bitrate and resolution are set in the Quest app, not on the PC |
| Virtual Desktop | Its own runtime (VDXR) or SteamVR, user-selectable | Moderate | Two possible runtimes; must work with whichever is set. Its own resolution/refresh settings override the game's |
| ALVR / open streamers | SteamVR | Variable | Community-maintained; version mismatches are common |
| Steam Frame wireless adapter | SteamVR (headset streams from PC) | Good | SteamOS on the headset; the PC may be Windows or Linux |
| Pico Connect / Streaming Assistant | SteamVR | Moderate | Similar to Steam Link; Pico's own controller profile |

Practical consequences: every wireless path adds 20–60 ms and an encode cost, so the performance guardrail triggers earlier; the active OpenXR runtime is a system-wide setting the mod must detect and log at startup; and on any streamed setup the user can't see the PC desktop from inside the headset, so logs and the desktop simulator matter more.

**Screen 2 of 4 — You and how we'll work**
1. How comfortable are you with code? None / can follow instructions / can read it / can write it. *Why:* it sets how much I explain and how much I just do. *No wrong answer.*
2. Where are we working right now — a coding tool that can run things (agentic), the desktop app with your files (desktop), or a chat window (chat)? *Why:* it changes who presses the build button — you or me. See Environment modes. *If unsure:* describe what you're looking at and I'll tell you.
3. How long can you comfortably wear the headset for a test? *Default:* 15–30 minutes.
4. Have you modded this game, or any game, before? Is a mod loader already installed? *Default:* no, and that's fine.

**Screen 3 of 4 — What the game is like** *(I'll also research this myself, so rough answers are fine)*
1. Do you see through the character's eyes (first-person) or watch them from behind (third-person)? Or both?
2. How do you fight — guns, swords, bows, magic, fists, nothing?
3. Anything special about getting around: vehicles, horses, ladders, climbing, swimming, flying, taking cover?
4. Lots of cutscenes or conversations with their own camera? Lock-on targeting?
5. Is the screen busy with UI (minimap, markers, crosshair) or fairly clean?

**Screen 4 of 4 — What you want**
1. Should I wait for you to test each stage before building the next (*hard gate*), or keep building and mark untested work (*soft gate*)? *Default and recommendation:* hard gate for the first five stages — a bad camera makes every later test meaningless.
2. Anything you specifically don't want? (Some people hate teleport; some only want arcade reload.) *Default:* everything on, all switchable in the menu.
3. Will you mostly play seated, or standing/walking around? *Default:* standing, seated supported.
4. Left- or right-handed? *Default:* right; both supported.

After Screen 4, say back a one-paragraph summary of what they told you, record it in `docs/TARGET_PROFILE.md`, then move to game research.

**Anti-cheat and multiplayer.** If the game has anti-cheat or online play, warn plainly: injecting into a protected process can get the account banned, and a modified client is unwelcome in multiplayer regardless. Recommend single-player, offline, or an unprotected build. Then proceed if they accept the risk. Do **not** attempt to defeat, disable, or evade anti-cheat or DRM — if the only path forward requires that, say the conversion isn't viable on that build and stop that line of work.

## Working environment and tools

**Same machine, always.** The game, the headset connection, the project files, and the environment running this skill must all be on the same PC. The bug pipeline, hot reload, log reading, and the desktop simulator all assume it. If the user develops on one machine and plays on another, tell them at intake that the workflow won't hold together, and recommend consolidating before Stage 0.

**Environment modes.** Detect which one you're in from your available tools, confirm it with the user on wizard Screen 2, and record it at the top of `docs/PHASE_PLAN.md` as `Mode: agentic | desktop | chat`. Each mode changes how you behave, not what you build:

| | **Agentic** (Claude Code or comparable — shell + files) | **Desktop** (file access, no shell) | **Chat** (no file access) |
|---|---|---|---|
| Who builds and runs | You. Compile, launch, read logs, commit without asking. | User builds; you write files and read the logs they save into the project. | User does everything; you hand over complete files to paste, with exact paths. |
| Scaffold | Create it. | Create it. | Describe it once; ask the user to create it and confirm. Keep the four living docs anyway — ask them to paste each doc back at session start. |
| Verification | Run the desktop simulator and unit checks yourself before handing over a playtest. | Ask the user to run the simulator; read its log file. | Ask the user for build output and simulator log pasted in. |
| Bug intake | Read reports and screenshots from `docs/playtests/reports/` directly. | Same, once the user saves them there. | User pastes log excerpts and uploads screenshots. |
| Message shape | Terse progress against stages; you're doing the work. | Instructions for what to run, then what to send back. | Numbered steps, one file per message when files are long, and an explicit "reply with X" at the end. |
| Best for | The whole project. | Planning, docs, review, tuning. | Getting started, or a quick fix on the go. |

Tell chat and desktop users, once at setup, that agentic mode is where this workflow is designed to live, and why — in plain terms: "in that mode I can build and test the mod myself, so you only need to put the headset on." Then respect their choice and don't nag.

**Re-pitch on friction, not on a timer.** Bring it up again — briefly, with a specific reason — when any of these happen in chat or desktop mode:
- The same build error has gone back and forth three or more times.
- A single fix has needed more than two paste-and-retry cycles.
- A stall report is written (see *When a stage won't yield*).
- A playtest comes back with more than five bugs and each needs a log the user has to fetch by hand.
- The user says anything like "this is tedious," "I keep copying stuff," or asks why it's taking so long.

The re-pitch is one or two sentences tied to the thing that just hurt ("that last error took four rounds because I can't see your build output — in agentic mode I'd have read and fixed it directly"), plus an offer to walk them through installing it. If they decline, don't raise it again until the next trigger.

**Switching modes.** The user can switch at any time by saying so ("let's do this in chat for now," "I've moved to Claude Code"). When that happens:
1. Update `Mode:` in PHASE_PLAN.md.
2. State in one line what changes for them (e.g., "I'll build and test myself from here; you'll only hear from me at playtest gates").
3. If moving *into* agentic or desktop mode, read the living docs from disk and reconcile with anything discussed in chat since they were last written.
4. If moving *into* chat mode, ask them to paste the current PHASE_PLAN, open QUESTIONS, and open sev-1/sev-2 bugs so you have the state.
Never lose work over a switch — the docs are the source of truth, not the conversation.

Whatever the mode, the human still puts on the headset. No tool changes that.

**Supporting tools to have available** (install as needed, all are standard modding/dev tools):
- A decompiler or disassembler suited to the engine's runtime, for finding hook points.
- A graphics debugger/frame capture tool, essential for Stage 2 — it shows exactly what each eye's pass drew and which effect is single-view.
- A memory scanner for locating camera and player structures in engines without exposed scripting (single-player only).
- The runtime's binding UI (SteamVR's or the vendor's) and an OpenXR API-layer inspector for seeing what the mod actually sends and receives.
- A screen recorder that captures the headset mirror. Video of a bug is worth more than any description — and the model can look at frames from it.

## Prerequisites check

Before Stage 0, confirm each of these, and for beginners walk them through installing what's missing:

- A working VR runtime on the PC (OpenXR-capable; SteamVR or the headset vendor's runtime), verified by launching any native VR title.
- A backup of the untouched game install, and the ability to verify/restore files.
- A backup of save games. Camera and controller hooks can corrupt saves in games that serialize player state.
- The game version pinned: disable auto-updates or use a fixed branch, and record the exact version in TARGET_PROFILE.md. A surprise patch mid-project can break every hook.
- A glance at the game's EULA and modding policy. Most single-player games tolerate mods; a few publishers prohibit them, and the user should know before investing weeks.
- If other mods are installed: a note of which ones and their load order, since another mod hooking the camera or input will fight this one.
- A mod loader or injection path appropriate to the engine, or a decision (below) about which to use.
- A toolchain to build the mod (compiler/SDK for the engine's language, or an interpreter if the loader supports scripts).
- Git initialized in the project. Commit at the end of every stage; tag each gate. This is the undo button for a fix that made things worse.
- A place to run the game where you can read logs live — a second monitor or the headset's desktop view.

## Research the game

Right after the wizard, before touching code, research the specific game. The user's answers are a starting point; the point of this step is to catch what they didn't think to mention. Use web search and the game's wikis, modding communities, and store pages. Put findings in a **Game dossier** section of `docs/TARGET_PROFILE.md`, each marked confirmed or assumed.

Look for:
- **Engine and version history.** Confirm the engine. Note major patches, engine upgrades mid-life, beta branches or legacy versions available for pinning, and DLC that changes mechanics.
- **Everything the player's body and camera do.** Vehicles, mounts, swimming, climbing, gliding, grappling, cover, dodges, finishers, QTEs, photo mode, minigames, forced-perspective sections, boss sequences with scripted cameras, on-rails segments. Each one is a place the camera gets hijacked and needs handling in Stage 1 or 4.
- **Combat surface.** Every weapon class and ability type, dual wielding, shields, mounted weapons, turrets. This seeds the manifest and decides which parts of Stage 6 apply.
- **UI surface.** How prompts render (text, sprite, baked), HUD elements, menu style, whether the game already has a controller-glyph system, localization approach.
- **Modding landscape.** Existing mod loaders, script hosts, decompiled or documented internals, community tools, known camera or FOV mods (these reveal the camera hook point), and — most importantly — any prior VR mod attempt.
- **Known problems.** Anti-cheat, DRM behaviour, crash-prone systems, save-format fragility, whether the community reports the game being hostile to injection.
- **Accessibility features already present** (colorblind modes, remapping, subtitles) that the mod should preserve.

Then do a **coverage check**: compare what you found against the stage plan and say, in plain language, which of the game's mechanics are covered by the standard stages, which need a game-specific addition (add it to the relevant stage's exit criteria), and which can't be supported and will be listed as known gaps. Show this to the user as their first status board (below) and ask if anything's wrong or missing. This is the moment a beginner learns what "VR conversion" will actually mean for their game.

## Research what exists, then ask

Before Stage 0, do a real search — web search, the engine's modding communities, the game's mod sites, source hosts — for three kinds of prior work: VR injection frameworks for this engine, VR mods for this specific game (finished or abandoned), and general mod loaders or script hosts for the game. Don't rely on memory; this landscape changes monthly.

For each candidate, record in `docs/DECISIONS.md`:

- What it already provides (stereo? camera? input? hands? IK?) and what it doesn't.
- **License and permissions.** Open-source with a license that allows derivative work is a green light. Closed, "all rights reserved," commercial, or unlicensed code is not — you can study its *approach*, but not build on its code. If the license is unclear, say so and treat it as not permitted until the user confirms otherwise.
- Maintenance status: last update, whether it works on the current game version, open issue count.
- Community reputation, if findable.

Then present the findings to the user in a short table and ask — as a decision, not a suggestion — which path they want:

- **Build on top** of an existing framework (only offered if its license allows it). Fastest route to stereo and input; effort goes to interaction, IK, and game-specific work. Note the trade-off: you inherit its architecture and its bugs.
- **Start from scratch** with this skill's own scaffold, borrowing only ideas. Full control, more work, and clearer ownership of the result.
- **Hybrid** — from scratch, but vendoring specific permissively licensed components.

For beginners, recommend building on top when a maintained, permissively licensed framework exists, and say why in one sentence. For experts, present the options neutrally. Either way, record the choice as a decision entry, and if building on top, add the framework's version and license to `docs/TARGET_PROFILE.md` and note any attribution the license requires in the README.

If the search finds a finished VR mod for this exact game, tell the user before doing anything else — they may want to play it rather than build one.

## Resuming a session

A new session has no memory. On resume: read `docs/PHASE_PLAN.md` for current stage, gate state, and recorded mode; if the recorded mode doesn't match the tools you actually have now, run the mode-switch steps before anything else. Then `docs/QUESTIONS.md` for open unknowns, `docs/BUGS.md` for open sev-1 and sev-2 bugs, and the last three entries of `docs/DECISIONS.md`. Tell the user in two sentences where the project stands and what's next. Don't re-interview them.

## Scaffold

On first run, create the full layout. The docs are load-bearing — they're the project's memory across sessions.

```
<project>/
├── docs/
│   ├── TARGET_PROFILE.md      # game, engine, hooks, capabilities — confirmed vs assumed
│   ├── PHASE_PLAN.md          # stages, exit criteria, gate mode, status
│   ├── DECISIONS.md           # choices and fallbacks with reasons (append-only)
│   ├── BUGS.md                # the bug log
│   ├── QUESTIONS.md           # unknowns waiting on the human
│   └── playtests/             # PLAYTEST-<stage>.md scripts, results, auto-captured reports/
├── src/
│   ├── core/                  # entry, lifecycle, hooks, signature scanning, hot reload
│   ├── render/                # stereo, projection, culling, post-fx, HUD reprojection
│   ├── input/                 # runtime bindings, action map, handedness, haptics
│   ├── locomotion/            # movement, turning, comfort, vehicles, climbing
│   ├── interaction/           # hands, grab, holsters, weapons, melee, world objects
│   ├── body/                  # IK, calibration
│   ├── audio/                 # listener pose
│   ├── ui/                    # in-VR settings menu, virtual screen, overlays
│   ├── sim/                   # desktop VR simulator (keyboard/mouse head + hands)
│   └── diagnostics/           # logger, bug capture, in-VR report trigger
├── tests/                     # unit checks + simulator run scripts
├── config/
│   ├── schema.json            # every tunable: type, range, default, menu section
│   ├── defaults.json
│   ├── bindings.json          # action-to-control map, per controller family
│   └── manifest.json          # game-specific data (weapons, grab points, bones, HUD ids)
├── dist/                      # end-user package: installer/README/uninstall
└── README.md
```

## The living documents

**TARGET_PROFILE.md** — Engine and exact version; renderer and graphics API; process entry method; camera object and how its view/projection are produced; update and render loop locations; player controller and movement model; player skeleton and bone names; input path; HUD/UI system; audio listener; save-game location; known obstacles. Mark every entry **confirmed** or **assumed**. Assumed entries are the ones that break you later.

**PHASE_PLAN.md** — Stage list, one checkbox per exit criterion, gate mode, what's waiting on a playtest.

**Stage brief.** Before starting any stage, write a short brief at the top of its PHASE_PLAN section. This is how the model orders its thinking:

```markdown
#### Stage 2 brief
Goal: per-eye rendering from the runtime's projection matrices.
Unknowns: does the post chain read the view matrix once per frame? (Q-011)
Hypotheses: H1 view matrix set in RenderCamera::Setup at 0x…; H2 post pass
            uses a cached copy — must patch both.
Plan: patch H1 → verify stereo on geometry → enable post one effect at a time.
Verify: PLAYTEST-2 items 1–6.
Risk: reflections use a separate camera (see profile: "assumed").
```

**DECISIONS.md** — Append-only:

```markdown
### D-007 — Stereo: single-pass instanced rejected
Date: …  Stage: 2
Chose: dual-pass, per-eye view matrix override.
Rejected: single-pass instanced — post chain re-derives world position from
depth with one view matrix; SSR and volumetrics become eye-locked.
Cost: ~1.7x draw calls. Revisit if the post chain is disabled.
```

**The status board.** Whenever a stage completes, a gate opens, a playtest comes back, the user asks "where are we," or a session resumes, post this — and keep the same copy at the top of `PHASE_PLAN.md`. It's the single view a beginner needs to feel oriented, so it is always in plain language and always complete:

```markdown
## Status — <game> — <date>
Mode: agentic | Gate: hard | Stage 4 of 10

✅ Built and tested   Stereo, head tracking, controllers, handedness
🔧 Built, not yet tested   Smooth/snap turn, teleport, vignette  → PLAYTEST-4 waiting on you
🚧 In progress   Ladder climbing (game uses scripted animation — trying override)
⬜ Not started   Physics hands, weapons, body, HUD, settings menu, packaging
❌ Won't be in Phase 1   Horse riding — animation locks camera; see D-012
❓ Need from you   Q-007 Which end of the crossbow model is the front?
🐞 Open bugs   1 sev-2 (BUG-009 crouch collider), 3 sev-4
▶ Next   You: run PLAYTEST-4 (~15 min). Me: ladder override.
```

Every line answers a question a beginner would otherwise have to ask: what works, what's waiting on them, what's being worked on, what's coming, what's been dropped and why, and what to do next. Don't summarize it into prose and don't skip the ❌ line — hidden gaps are worse than known ones.

**QUESTIONS.md** — Numbered unknowns, each with why it matters and a default you'll assume if unanswered. Present them in batches; mark answered ones with the answer.

**BUGS.md** — See the bug pipeline.

## Stages

Each stage lists exit criteria. Compiling isn't done; meeting the criteria is. Effort labels are rough guides so beginners know what to expect.

### Stage 0 — Recon and entry *(small)*
Verify the declared engine against evidence: directory layout, library names, asset container formats, embedded version strings, scripting-runtime metadata. If evidence contradicts the claim, say so before writing code. Get code executing inside the process, a log line on screen, and config hot-reload if the platform allows. Set up signature scanning or equivalent so hooks survive game patches where possible; where they can't, record the exact game version the mod targets.
Set up the feature-flag system, safe mode, and config validation described in *The implementation loop* — they're small now and painful later.
*Exit:* mod loads, logs, launches flat when told to, and the game can be restored to stock.

**How to get in.** Prefer the least invasive entry that works, in this order, and record which one you used: (1) an official mod API or script host shipped with the game; (2) a community mod loader for the engine's managed runtime, if it has one; (3) a native plugin loader or proxy library that the game already loads by name; (4) a general injector as the last resort. Each step down loses stability and gains reach. Beginners should never be walked below rung 2 without a plain explanation of why.

**How to find things.** This is the method for every "where is the camera / player / input / HUD" question in an unknown engine. Work down the list and stop when something moves:
1. **Names first.** Dump every class, object, symbol, or string the runtime exposes and search for the obvious words — camera, view, projection, fov, player, pawn, controller, hud, canvas, listener. Engines reuse their own vocabulary; the game research step often tells you what it is.
2. **Existing mods as a map.** A community FOV, free-camera, or photo-mode mod has already found the camera. A no-HUD mod has already found the HUD. Read how they did it (approach, not code, unless the license allows).
3. **Frame capture.** Capture one frame in the graphics debugger and find the draw calls for world geometry; the constant buffer feeding them holds the view and projection matrices. That's a hook point even in a fully stripped binary.
4. **Value hunting.** Stand still, note the FOV or a coordinate the game displays, scan memory for it, move, scan again. Works for camera position, player position, health, ammo. Single-player only.
5. **Observation.** Change something and watch. Set a candidate matrix to identity for one frame — if the world snaps, you have the camera. A hook that produces no visible change is not a hook.
Write every confirmed location into TARGET_PROFILE.md with how it was found, so it can be re-found after a patch. Never record a location you haven't seen the game react to.

### Stage 1 — Camera ownership *(medium, high risk)*
Take control of the view transform before touching stereo. Decouple the camera from everything that drives it: animation tracks, head bob, camera shake, cinematic FOV changes, third-person orbit arms, root-motion animations, cover-system camera shifts, lock-on cameras, death and ragdoll cameras, respawn and loading transitions, dialogue cameras. Each of these is a place where game code will fight for the camera; find them all now.

For third-person games, relocate the view to the head bone or an offset from the player root, and hide or near-clip the player's own head mesh. Decide how animations that move the body (dodges, vaults, finishers) are handled: let the world move under a fixed head, or fade during the animation. Never yank the head.

This stage is where nausea is won or lost. Apply the head pose as late as possible in the frame, never smoothed, never overridden by game logic for even one frame, and never with roll from game code.
*Exit:* looking around is 1:1 with the headset at correct world scale, with no forced camera motion in any game state, including death, cutscene transitions, and vehicles.

### Stage 2 — Stereo rendering *(large, high risk)*
True per-eye rendering. Attempt the highest-quality path available and only descend the ladder when the higher rung is genuinely unworkable — writing the reason in DECISIONS.md when you do:

1. Native per-eye rendering with per-eye view and projection matrices from the runtime.
2. Single-pass instanced or multiview, if post-processing and culling can handle two views.
3. Dual full-scene passes.
4. Reprojection-based approaches are a last resort and must be labelled as such to the user.

Handle culling frustums (widen for the combined view), shadow and reflection passes that assume one camera, and screen-space effects that need per-eye derivation. Verify IPD, world scale, and depth by looking at an object of known size.
*Exit:* correct separation and convergence, no eye-locked artifacts, no doubled UI or post effects, objects feel the right size.

### Stage 3 — XR runtime, input, and the desktop simulator *(medium)*
OpenXR primary; OpenVR/SteamVR fallback only if OpenXR isn't viable. Build input on an **action-based abstraction** — never bind logic to a physical button. Every action gets a name, a default binding per controller family, and a rebindable entry in `config/bindings.json`.

**Left-handed support is built here.** Define dominant/off hand at the abstraction level so every downstream system asks "dominant hand," never "right hand." Retrofitting this after Stage 6 is a rewrite.

**Controller families.** Detect the active OpenXR interaction profile at runtime and load the matching default binding set from `config/bindings.json`. Ship defaults for every family below; fall back to the generic controller profile, then to Touch-style mapping, for anything unrecognized. Verify the exact profile paths against the current OpenXR spec and vendor extensions rather than trusting this list — they get added and revised.

| Family | Per-hand inputs | Notes |
|---|---|---|
| **Meta Touch** (Quest 2/3/3S/Pro, Rift S) | Thumbstick (click), two face buttons (A/B right, X/Y left), trigger, grip, menu (left), system (right), capacitive touch on stick/face/trigger, Pro adds pressure/stylus | The de-facto default layout; most VR titles are designed around it |
| **Valve Index** ("Knuckles") | Thumbstick (click), A/B, trackpad (force/touch), trigger, grip *force* sensor (analog squeeze), system, per-finger capacitive tracking | Grip is analog and strap-secured — support "let go" as a gesture, not a button release |
| **HTC Vive wands** (original, Pro) | Trackpad (click + touch, no stick), trigger, grip (digital, sides), menu, system | No thumbstick — locomotion needs trackpad-click or touch-region emulation; snap turn is essential |
| **Vive Focus / XR Elite / Cosmos** | Thumbstick, A/B or X/Y, trigger, grip, menu | Touch-like; treat as Touch with a Vive profile |
| **Pico 4 / 4 Ultra / Neo 3** | Thumbstick, A/B or X/Y, trigger, grip, menu, capacitive touch | Touch-like; own OpenXR profile via Pico extension |
| **Windows Mixed Reality** (Reverb G2 v1, Odyssey) | Thumbstick, trackpad, trigger, grip, menu; G2 v2 drops the trackpad for A/B–X/Y | Runtime is end-of-life on newer Windows; expect users on a bridge |
| **PSVR2 Sense** (on PC via adapter) | Thumbstick, two face buttons (○/× right, △/□ left), trigger, grip, options/create, capacitive finger sensing | Adaptive trigger and haptics are limited on PC; button glyphs are PlayStation shapes |
| **Steam Frame** | *Left:* thumbstick (click), D-pad (4 buttons), bumper, trigger, dual-stage grip, View, Steam. *Right:* thumbstick, A/B/X/Y, bumper, trigger, dual-stage grip, menu buttons. Capacitive finger detection on sticks; finger tracking via skeletal input. OpenVR type `frame_controller`; OpenXR profile via Valve's extension | Split-gamepad layout designed to double as a flat-game controller; the extra buttons mean more direct bindings and fewer chords than Touch. SteamVR remaps Touch bindings onto it automatically (Touch B/Y → the three top buttons), so a Touch default is a safe fallback |

Design the action map so the *minimum* controller (Vive wands: trackpad, trigger, grip, one menu button) can play the whole game, then let richer controllers get direct bindings for things the wands need chords or menus for. Record which family the user actually owns in TARGET_PROFILE.md and test on that first.

Build `src/sim/`: a desktop mode that drives head and hand poses from mouse and keyboard so you and the user can check logic without a headset. It won't tell you about comfort, but it catches most functional bugs before they cost headset time.

Wire haptics here as a general "pulse(hand, strength, duration)" call; later stages use it for grabs, hits, fire, and menu clicks.
*Exit:* both controllers tracked, all actions rebindable, handedness swap works end to end, the simulator drives the same code paths.

### Stage 4 — Locomotion and comfort *(medium)*
Smooth locomotion with head- or controller-relative direction (user-selectable), smooth and snap turning with configurable increments, and a teleport option. Physical movement is real: roomscale walking moves the player collider, physical crouch lowers the collider and triggers the game's crouch state, lean and prone are respected. Handle the roomscale/collision mismatch — fade, push back, or block — and document the choice.

Special movement, where the game has it: **ladders and climbing** by grabbing rungs/holds with the hands (fall back to the game's automatic climb with a faded camera if the animation can't be overridden); **swimming** with a strong comfort fade option; **mantling** as world-moves-under-fixed-head. **Vehicles and mounts**: switch to seated mode with a fixed cockpit or saddle frame, keep the head free, keep the hands able to grab a wheel/reins if the game exposes steering, and offer a cockpit-frame comfort option since a visible static frame reduces motion sickness.

Comfort options ship here and all appear in the settings menu: vignette/tunneling with strength, snap vs smooth turn, teleport toggle, seated/standing/roomscale with height offset, recenter binding, and per-mode fades. **Ship comfort-first defaults** — snap turn, vignette on at medium, teleport available — because the first person to launch the mod may be new to VR, and a veteran can flip them off in ten seconds. Respect the runtime's play-area boundary: never teleport or push the player's real body outside it, and never draw over the boundary warning.
*Exit:* all locomotion modes work, all comfort toggles function live, seated and standing playable, every special-movement type the game has is handled.

### Stage 5 — Physics hands and grabbing *(medium)*
Hands are physics-driven with collision — stopped by walls, able to push objects. Drive them toward the controller pose with a configurable spring/velocity drive and a break distance so they lag realistically instead of teleporting through geometry. Make hand physics frame-rate independent.

Grab is per-object, defined in the manifest: what's grabbable, grab points, hand pose, release behaviour. Throwing uses tracked velocity over the last few frames, not the instantaneous value.

World interaction: doors, levers, buttons, switches, pickups, and loot are physically touched or grabbed where the game exposes them, with a pointer-and-press fallback for anything that isn't a physical object.
*Exit:* hands collide with the world, objects can be picked up and thrown sanely, hands recover when stuck, doors and buttons work by touch.

### Stage 6 — Weapons and combat *(large)*
Build in this order; each part depends on the one before. Playtest at the end of each sub-stage.

**6A — Holsters and equipping.** Body-relative anchors: both shoulders, both hips, chest, optionally back. Grabbing at an anchor equips or stows. Shoulders default to long guns and bows; hips to sidearms, melee, and ammunition. Positions are calibrated per player in the settings menu, never hardcoded — torso proportions vary hugely.

**6B — Guns.** Aim decoupled from view: the gun points where the hand points, and the game's aim assist, crosshair raycast, and hit logic are rerouted to the muzzle transform. Recoil moves the weapon in the hands, never the camera, with an intensity slider from zero to full. **Two-handed** weapons have real grab points that pivot the weapon — the off hand steers the muzzle — with auto-grab, toggle, and hold modes. **Manual reload** by default: magazine from the hip holster, insert, rack the slide; support bolt, pump, break-action, and revolver variants where present. **Arcade reload** as a selectable alternative and as the automatic fallback when a weapon's model has no usable magazine geometry: hold near the hip for a moment. **Crosshair** off by default, toggleable, rendered at the muzzle raycast's hit distance, not in screen space. Haptic pulse on fire and on empty.

**6C — Melee, bows, and thrown.** Melee swings read controller velocity and arc, not a button; require a minimum velocity to avoid accidental hits, scale damage by speed if the game permits, and let a second hand stabilize the weapon (and modify damage if the model allows). Blocking by holding the weapon in a guard region. **Bows**: grab with one hand, nock and draw with the other, release to fire, draw distance sets power; arrows come from a shoulder or hip quiver. **Thrown**: grenades and knives use the physics-hand throw.

**6D — Magic, abilities, and gadgets.** Where the game has non-weapon powers, map them to hand gestures or holstered "items" so they follow the same equip logic — palm-forward casts, wrist-flick abilities — with a button fallback selectable in settings.

*Exit:* every weapon and ability in the manifest can be drawn, aimed, used, reloaded, and stowed with motion controls on either hand.

### Stage 7 — Full-body IK *(large)*
Retarget the game's existing player skeleton rather than spawning a parallel rig — it keeps animations, collision, and game logic intact. Drive head and hands from tracked poses; solve arms with two-bone IK and a configurable elbow hint; derive hip and chest from head position and horizontal velocity; solve legs against ground contact and blend with the game's locomotion animation where possible.

Calibration is mandatory and lives in the settings menu: a guided flow capturing height, arm span, and a neutral pose, writing scale and offset. Provide a mirror or body-view mode so the user can see the result. Use the game's own body-hiding logic where it exists (many first-person games already hide the head).

If a skeleton genuinely can't be retargeted — locked animation state machine, no exposed bones, procedural-only rig — fall back to **hands-only with a body-less presence** and record why. Don't take that fallback on the first difficulty.
*Exit:* body follows the player believably looking down and in a mirror, calibration persists, no limb inversion or shoulder popping in normal play.

### Stage 8 — HUD, UI, cutscenes, and audio *(medium)*

Run UI conversion as a procedure, not a judgement call per element. Four steps:

**Step 1 — Inventory.** Enumerate every UI element the game draws — from the Stage 0 dump, the game research, and a walk through the first hour with a debug overlay that labels each element on screen. Record each in the `ui` section of `config/manifest.json` with: id, what it shows, when it's visible, whether it's text/sprite/3D/video, and whether the game can hide it independently. A beginner should be able to read this list and recognize every item from playing the game.

**Step 2 — Classify** each element into exactly one type. The type decides the treatment:

| Type | Examples | VR treatment |
|---|---|---|
| Status | health, stamina, ammo count, mana | **Body- or weapon-anchored.** Ammo on the weapon; health/stamina on the wrist, forearm, or chest. Visible on a glance, hidden when not looking |
| Spatial | waypoints, enemy markers, damage direction, pickup highlights | **World-anchored.** Keep them at their world position; damage direction becomes a peripheral flash on the correct side |
| Reticle | crosshair, hit marker, interaction dot | **Muzzle- or hand-anchored** at hit distance; off by default for weapons, on for interaction pointing |
| Transient | subtitles, tutorial prompts, pickup toasts, kill feed | **Head-locked at depth**, low in the view, fading; subtitles anchored to the speaker when the game exposes that |
| Menu | pause, inventory, map, skill tree, dialogue choices | **Floating panel** in world space, spawned in front of the user, laser or touch interaction; large menus become a curved panel |
| Screen | cutscenes, video, loading, credits, full-screen minigames | **Virtual screen** with a neutral environment; head free |
| Ambient | vignette, blood on screen, low-health desaturation | **Rebuilt as a headset-space effect** at reduced strength, or dropped — full-screen overlays at zero depth are the worst offender for eye strain |

If an element genuinely fits none, it's a *Transient* until proven otherwise. Every element's type goes in the manifest.

**Step 3 — Build the rendering paths.** Each treatment above is one reusable component in `src/ui/`: a body-anchor slot system (wrist, forearm, chest, hip, weapon socket), a world-anchor projector, a head-locked layer with configurable depth and fade, the floating-panel system with input, the virtual screen, and the ambient-effect rebuild. Elements are bound to components through the manifest, so retreating one element is a config change, not code.

**Step 4 — Make it tweakable in-VR** (this is where Stage 9's *UI Layout* section comes from). Every anchored element and every panel supports a **layout mode**: the user opens it from the settings menu, every element shows a handle, and they grab and move, scale, rotate, or set opacity by hand; changes write back to the manifest immediately. Provide a per-element reset and a "reset all layout" button. Beginners will never type coordinates; this is how UI gets tuned.

Text legibility rules apply to every treatment: minimum angular size for body text, high-contrast backgrounds behind text, no text closer than about half a meter, no text farther than a few meters unless it scales with distance. Where the game's own font is too thin at VR resolution, allow a font-weight override.

Menus and inventory get a laser pointer or direct touch, whichever suits the layout. Loading screens go on the virtual screen with a neutral environment behind them so the user is never staring into a void.

**Controller-matched button prompts.** The game's tutorial and UI prompts say "Press E" or show an Xbox glyph; in VR they should show the actual button on the actual controller, resolved through the action map. Climb this ladder, stopping at the highest rung the game's UI system allows:

1. **Text substitution.** Hook the prompt's text or localization lookup and replace the key/button name with the bound control's name for the detected family ("Press E" → "Press A" or "Squeeze Grip"). Almost always achievable; do this first.
2. **Glyph substitution.** If prompts are sprites from an atlas, swap in a per-family glyph atlas (Touch, Index, Vive, Frame, PSVR2 Sense, generic) keyed by action, not by physical button. Requires the atlas to be replaceable at runtime or on disk.
3. **Controller diorama.** For the in-VR settings menu and first-run tutorial, render a 3D controller model of the detected family with the relevant input highlighted. Ship this for the settings menu regardless; extend to in-game prompts only if the game's prompt system is hookable.

Prompts must re-resolve when bindings change or a different controller connects, so drive them from the action map, never from a static table. Text substitution has to work in every language the game ships — substitute the token, not the English word, or non-English users get "Press [trigger]" mid-sentence in their own language. Whether the game's prompts are text, sprites, or baked textures is a Stage 0 recon question — add it to TARGET_PROFILE.md.

**Audio:** move the game's listener to the head pose, not the camera object it thinks it has. Spatialized game audio should follow head rotation; UI sounds should not.
*Exit:* every element in the UI inventory has a type and a working treatment, none at the wrong depth; layout mode moves and saves every anchored element; cutscenes watchable; all menus usable in-headset; sound comes from the right direction when turning the head.

### Stage 9 — In-VR settings menu *(medium)*
Everything tunable is exposed here, because the user can't alt-tab in a headset. Reachable from a dedicated binding at any time, pauses the game where possible, applies live, no restart.

Sections: **Calibration** (height, arm span, IK, holster anchors, mirror view), **Comfort** (vignette, turn mode and increment, teleport, play mode, recenter, fades), **Weapons** (reload mode, two-handed mode, recoil, crosshair), **Input** (handedness, rebinding, deadzones, haptic strength, controller diorama), **UI Layout** (enter layout mode; per-element position, scale, opacity, anchor, and visibility; virtual-screen size and distance; subtitle size; font weight; reset per element or all), **Rendering** (IPD, world scale, render scale), **Features** (the on/off flag for every feature, grouped by stage), **Diagnostics** (log level, report-a-bug, smoke-test result, reset all to defaults).

Support **multiple user profiles** — calibration, holster positions, handedness, and layout are per person, and a household sharing a headset should switch with one selection rather than recalibrate.

Two ways to reach it, both required: a dedicated controller binding that opens the mod's own overlay from anywhere, and — where the game's pause menu can be extended — a **"VR" entry injected into the game's own pause/options menu** that opens the same overlay, so a beginner finds it where they'd expect settings to be. The overlay is the source of truth; the injected entry is just a door.

Every setting reads type, range, default, and menu section from `config/schema.json` so the menu and the config file can't drift apart. Beginners in particular need **reset to defaults** and per-section reset.
*Exit:* every tunable in the schema appears in the menu, every feature flag is toggleable, layout mode is reachable from the menu, changes apply live, settings persist across restarts, and the menu is reachable from both the binding and (where possible) the game's own pause menu.

### Stage 10 — Sweep and package *(medium)*
Play the game's opening hour end to end. Fix what the bug log holds. Confirm left-handed play across Stages 4–9, not just where it was implemented. Confirm seated play across everything. Run the desktop simulator through every stage's playtest script as a regression pass.

Then package for other people: `dist/` gets an installer or clear install steps, an uninstall path that restores the game, a README covering requirements, controls per controller family, the settings menu, known issues, and how to report bugs. Never redistribute the game's own assets or executables — ship only your mod's files.

Performance is **out of scope for Phase 1** — but log every framerate observation as a sev-4 bug so the optimization pass has data.

## The implementation loop

Every feature inside a stage follows the same loop. Don't skip rungs to save time; skipped rungs are where regressions come from.

1. **Brief it.** One paragraph in the stage brief: what the feature does, the hook or system it depends on, how you'll know it works. If the dependency is still marked *assumed* in TARGET_PROFILE.md, confirming it comes first.
2. **Flag it.** Every feature gets an entry in `config/schema.json` with an on/off switch, default on. Nothing ships without a switch — a beginner's only debugging tool is turning things off until the problem goes away, and the settings menu's Diagnostics section lists every flag.
3. **Hook it.** Write the smallest change that proves the hook is real: log a value, move something one unit. A hook is not confirmed until the game visibly responds. Never write "hook confirmed" in the profile on the strength of reading code — only on the strength of the game doing something.
4. **Prove it in the simulator.** Run the desktop simulator through the feature's motions. Add an in-game assertion for anything that must always be true (below).
5. **Prove it in the headset.** Add it to the current stage's playtest script. It's *built* at step 4 and *tested* only after this.
6. **Commit it** with the flag name in the message so a bad feature can be found and reverted alone.

Two safety rails belong in Stage 0 and stay forever: a **safe mode** — if VR initialization fails or a flag file is present, the mod steps aside and the game launches flat, so a bad build never locks the user out of their game; and **config validation** on load, so a typo in a setting produces a logged warning and a default, not a crash.

## The test process

Four layers. The first three need no headset and run before every gate; the fourth is the human.

**1. Unit checks** on pure math — projection matrices, IK solutions, holster offsets, velocity estimation for throws. Small, fast, run on every build.

**2. Simulator runs.** The desktop simulator drives head and hands through scripted motions. Keep a short scripted run per stage (`docs/playtests/sim/<stage>.json`) that exercises everything the stage added; run all of them before every gate as the **regression suite**.

**3. In-game assertions.** The mod checks itself every frame in a debug build and logs a sev-1 bug automatically when a rule breaks. Start with these and add per feature:
- View matrix has zero roll.
- Head pose was the last writer to the camera this frame.
- Both eyes rendered, with different view matrices.
- World scale is within tolerance of the calibrated value.
- Every action in the map is bound for the active controller family.
- Every schema entry has a menu item and every menu item has a schema entry.
- Hand physics step is independent of frame rate.
Assertions are how the model tests without a headset; treat a firing assertion as a real bug, not noise.

**4. Headset playtests.** The scripts described in the bug pipeline. To make them repeatable, keep **fixtures**: a save game at a known spot for each stage (open area, ladder, vehicle, a fight with every weapon type), plus a written route. "Load `fixture-stage6.sav`, walk to the crate" beats "find a gun somewhere."

**Smoke test on every launch.** Before any playtest, the mod logs one line confirming: runtime detected, controller family detected, both eyes rendering, all flags loaded, no assertions fired in the first ten seconds. If the smoke line is missing, don't playtest — fix that first.

**Nausea protocol.** Tell the user before their first headset session: stop the moment they feel warm, sweaty, or dizzy; do not push through; wait an hour before trying again. A single bad session can set someone's tolerance back for days. Any playtest ended early for nausea is logged as a sev-1 bug against whatever was being tested, with the user's description of what they were doing.

**Before packaging** (Stage 10): all four layers green, then a second person if one is available — a fresh tester with a different headset or controller family finds what the developer's habits hide. Log their reports through the same pipeline.

## Performance guardrail

Performance work is deferred, with one exception: if framerate is so low that playtesting is physically impossible (reprojection thrash, nausea within a minute), do the minimum to make testing viable — a render-scale slider, and toggles for the most expensive post effects — then stop. Log it as a decision, not an optimization pass.

## Game-specific data: the manifest

`config/manifest.json` holds everything that's true of this game and no other: weapon list and types, grab points, magazine geometry, holster defaults, ability list, skeleton bone names, HUD element identities, interactable object classes, vehicle definitions. Populate in three passes, in order:

1. **Auto-discover.** Dump the game's classes, prefabs, or asset tables and pattern-match for weapons, sockets, bones, UI roots, interactables. This gets *what exists*.
2. **Template.** Emit a manifest with every discovered entry stubbed, with a comment wherever a human must decide (which end is the muzzle; is this a rifle or a pistol; is this door hinged or sliding). Hand it to the user with the questions batched in QUESTIONS.md. For beginners, propose an answer for each and ask them only to confirm.
3. **In-VR correction.** Positions and offsets get finalized by the player physically adjusting them in the settings menu, which writes back to the manifest. Never expect coordinates typed into a file to be right.

The shape, so every project uses the same one:

```json
{
  "game": { "name": "", "version": "", "engine": "" },
  "skeleton": { "head": "", "hand_l": "", "hand_r": "", "hips": "", "spine": [] },
  "weapons": [
    { "id": "", "class": "pistol|rifle|shotgun|bow|melee|thrown|ability",
      "grab_points": [{ "name": "main", "offset": [0,0,0], "rotation": [0,0,0] }],
      "two_handed": false, "muzzle": [0,0,0], "magazine": { "type": "box|tube|cylinder|none", "offset": [0,0,0] },
      "holster": "hip_r|hip_l|shoulder_r|shoulder_l|chest|back", "reload": "manual|arcade|auto" }
  ],
  "holsters": { "hip_r": { "offset": [0,0,0] }, "shoulder_r": { "offset": [0,0,0] } },
  "interactables": [{ "class": "", "kind": "door|lever|button|pickup|ladder", "grab": "handle|press|any" }],
  "vehicles": [{ "class": "", "seat_offset": [0,0,0], "steering": "wheel|reins|none" }],
  "ui": [{ "id": "", "type": "status|spatial|reticle|transient|menu|screen|ambient", "anchor": "wrist_l|weapon|world|head|screen", "offset": [0,0,0], "scale": 1, "opacity": 1 }]
}
```

`config/bindings.json` maps action names to controls per controller family, with one `"generic"` entry as the fallback: `{ "fire": { "touch": "trigger", "index": "trigger", "vive": "trigger", "frame": "trigger" }, "grab": { "touch": "grip", "index": "grip_force>0.6", … } }`. Actions, never buttons, everywhere else in the code.

## The bug pipeline

One pipeline, three intakes, one log.

**Intake 1 — the in-game logger.** `src/diagnostics/` writes a structured log with timestamps, stage tags, and severity. Every subsystem logs state transitions. Crashes capture a stack and the last 500 lines.

**Intake 2 — the in-VR bug trigger.** A binding the player hits the instant something goes wrong, without removing the headset. It snapshots timestamp, scene, player pose, held items, active settings, active runtime and connection method, and the recent log tail into `docs/playtests/reports/`, plus a screenshot of each eye — and, if a recorder is running, a marker so the last thirty seconds of video can be pulled. Images and video are things the model can actually look at; use them. This is the highest-value piece of the pipeline — a bug reported ten minutes later has lost every detail that mattered. Beginners should be told about this binding before their first playtest and reminded on the script.

**Intake 3 — the human's words.** Whatever the user says in chat, however vague. Reformat it into a log entry yourself; never make them fill a template. If it's too vague to act on, ask one specific question, not five.

**Log format** — append to `docs/BUGS.md`:

```markdown
### BUG-042 — Left-hand mag insert fails on the shotgun
Status: open | Severity: 2 | Stage: 6B | Reported: playtest-6b / auto-capture
Repro: equip shotgun from left shoulder, grab shell from right hip, insert.
Expected: shell loads. Actual: shell drops, no load event.
Evidence: reports/2026-09-06-1412.json, log lines 8802–8840
Hypothesis: shell socket test uses dominant-hand transform, not the
            inserting hand's. Suspect interaction/reload.cs:214.
Fix: …
Verified: playtest-6c ✓
```

**Severity.** 1 = crash, hard lock, or nausea-inducing. 2 = feature broken. 3 = wrong behaviour with a workaround. 4 = polish or performance note. Sev-1s preempt whatever stage you're in; nausea is always sev-1 because the user physically cannot keep testing.

**Triage discipline.** State a hypothesis before fixing — a fix without one is a guess, and guessed fixes are how VR mods accumulate contradictory patches. Group by root cause. Commit each fix separately so a bad one can be reverted alone. Never close a bug on your own authority; it stays open until a playtest verifies it, because the model cannot observe the failure mode. After three failed fix attempts on one bug, stop, write up what's been tried, and ask the user for a fresh capture rather than guessing a fourth time.

**Playtest scripts.** At each gate write `docs/playtests/PLAYTEST-<stage>.md`: numbered concrete actions ("draw the pistol from your left hip with your right hand, fire six rounds, reload manually"), each with an expected result and a blank for what happened. Every script includes a comfort check — nausea, eye strain, arm fatigue — since those are invisible in a log, and a reminder of the bug-trigger binding. Keep scripts under fifteen items; headset fatigue makes late results unreliable. For beginners, include how to launch, how to open the settings menu, and how to quit safely.

## What happens at a gate

A gate is the end of a stage. It's the same five steps every time:
1. Run the three no-headset test layers. Anything red gets fixed before the human is asked for time.
2. Post the status board and the playtest script. Tell the user roughly how long it will take.
3. Stop building. Answer questions, tidy docs, but don't start the next stage.
4. When results come in, log every item — passes and failures — through the bug pipeline. Triage: sev-1 and sev-2 reopen the stage; sev-3 and sev-4 go on the list and the stage can pass.
5. Say explicitly "Stage N passed" or "Stage N reopened, here's why," update the board, commit and tag. In soft-gate mode, steps 3 and 5 relax; steps 1, 2, and 4 never do.

## When a stage won't yield

Timebox. If a stage's core hypothesis has failed three times, stop and write a **stall report** in DECISIONS.md: what was tried, what the evidence says, the next rung on the fallback ladder, and what information from the human would unblock it. Then ask. Options in order of preference: a different hook point, a different technique on the same rung, the next fallback rung with the reason logged, or — for a genuinely blocked feature — shipping Phase 1 without it, clearly listed in README known issues. A conversion with an honest gap beats one with a hidden hack.

## Recurring failure modes

Check these before blaming the engine — they account for most of what goes wrong:

- **World scale wrong.** Dollhouse or giant's world. Fix world-to-meters first; most spatial complaints downstream are really this.
- **Head pose applied too early**, then modified by game logic — reads as "bad tracking."
- **Camera roll or forced motion from game code** in a state you didn't find in Stage 1 (death, vehicle, finisher, dialogue).
- **HUD at zero depth.**
- **Post-processing from a single view matrix** — motion blur, SSR, SSAO, volumetrics. Disable, then re-enable per-eye one at a time.
- **Shadow and reflection cameras** never told about the second eye.
- **Aim still driven by screen center** after moving the weapon to the hand.
- **Holsters calibrated to one body.**
- **Handedness assumed** deep in interaction code, found at Stage 10.
- **Frame-rate-dependent hand physics.**
- **Audio listener still on the game's camera object**, so sound rotates with the body instead of the head.
- **Game patch broke every hook** because offsets were hardcoded and no signature scan existed.
- **Settings menu and config drifted** because a tunable was added in code but not in the schema.

## Phase 1 done

Phase 1 is complete when every item below is verified by a human playtest, not by the model:

- Stereo, 6DoF, correct scale, no forced camera motion in any game state.
- Smooth, snap, teleport, physical crouch/lean, seated and roomscale, all comfort toggles.
- Physics hands, grab, throw, world interaction.
- Every weapon and ability class in the game usable with motion controls, both handedness.
- Full-body IK with calibration (or a logged hands-only fallback).
- Cutscenes, HUD, menus, and audio correct in-headset; button prompts show the user's actual controller.
- In-VR settings menu covering every tunable, with reset.
- Bug trigger and logger working; no open sev-1 or sev-2 bugs.
- Unit checks, simulator regression suite, and in-game assertions all green on the release build; safe mode verified.
- Packaged in `dist/` with README and uninstall.

## Glossary (use with beginners)

- **6DoF** — six degrees of freedom: the headset tracks where your head is, not just which way it faces, so leaning and crouching work.
- **Stereo rendering** — drawing the scene twice, once per eye, so depth is real.
- **OpenXR / OpenVR** — the software standards a VR mod talks to in order to reach the headset. OpenXR is the modern one.
- **Injection / mod loader** — how the mod's code gets run inside the game.
- **Hook** — intercepting a specific game function to change what it does.
- **IK (inverse kinematics)** — figuring out where elbows and knees should be from where the hands, head, and feet are.
- **IPD** — distance between your eyes; wrong IPD makes the world feel the wrong size.
- **Reprojection** — the headset faking frames when the game can't keep up; a comfort warning sign.
- **Interaction profile** — OpenXR's name for "which controller is plugged in"; the mod reads it to pick the right bindings and button pictures.
- **Diegetic UI** — interface elements that exist inside the game world (a watch on your wrist) instead of floating on the screen.
- **Manifest** — the file listing this specific game's weapons, bones, and objects so the mod knows what it's working with.

## Working with the user

Report progress with the status board, not with file lists. When a stage is gated, post the board, hand over the playtest script, and stop — don't fill the wait with work on the next stage, since a failed playtest may invalidate it.

Write for the least technical person who could plausibly be reading, unless they've shown they're an expert. Every technical term gets a plain-word gloss the first time it appears ("the runtime — the VR software that talks to your headset"). Never assume a reader knows what a hook, a matrix, or a bone is. The engineering stays exact; only the words around it get simpler.

Say plainly when something is a guess. "The camera transform is at this address" is a hypothesis until it moves the view. People can act on stated uncertainty; they can't act on false confidence.

Ask about feel in batches, always with a specific comparison ("closer to the flat game's recoil, or to a real weapon?"). Open-ended "how does it feel?" produces answers you can't act on.

For beginners, end each message with exactly one clear next action for them, and never more than one. For experts, end with the decision they need to make, if any.

Set expectations once, early: a full-feature conversion of a real game is weeks to months of work with many headset sessions, not an afternoon. Stages 0–2 alone can take days on a hostile engine. Saying this up front is kinder than letting someone discover it at Stage 4.
