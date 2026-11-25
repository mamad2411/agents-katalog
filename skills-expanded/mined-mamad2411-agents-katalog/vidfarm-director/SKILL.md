---
name: vidfarm-director
description: Use Vidfarm as a director. Browse/add inspiration videos, browse/save public raws, fork a template into a composition, edit it in the Trackpad Editor (timeline-based like Premiere/DaVinci), auto-decompose source video into scenes, render to MP4, approve into a shareable post, and schedule it. Includes login, provider keys, discovery, versioning, uploads/downloads, and billing. Every step is available as raw REST; `vidfarm-devcli` wraps those routes and composes the file-backed scripting flows.
---

# Vidfarm Director

Vidfarm is a video composition studio. Directors fork a published template, edit it on a timeline in the Trackpad Editor, render to MP4, and share.

## Quickstart (desktop agents — do this first)

The CLI is `vidfarm`, from the npm package `@mevdragon/vidfarm-devcli`. Install and authenticate before anything else:

```bash
npm install -g @mevdragon/vidfarm-devcli    # installs the `vidfarm` command
vidfarm login --api-key vf_key_...          # validates + persists the key durably
vidfarm serve template_<32hex>              # local server + browser, opens that template
```

- The API key comes from https://vidfarm.cc/settings and starts with `vf_key_`. Instead of `login`, setting the `VIDFARM_API_KEY` environment variable also works for every command — the CLI reads it from the environment or from a `.env` file in the current directory.
- No account or key? `vidfarm serve --no-cloud` still gives a fully local editor with free local renders.
- "Open/run template X locally" is exactly one command: `vidfarm serve <template_id>` (alias: `vidfarm <template_id>`). Do not hand-roll REST or hunt for local `.harness/` files first — `serve` and `pull` create those.

### Entity ID formats

Every Vidfarm id is a type prefix + 32 hex characters (`prefix_<32hex>`). There are no short slugs and no `tpl_` prefix.

| Prefix | What it is | Typical use |
|---|---|---|
| `template_` | published template | `vidfarm serve template_<32hex>`, fork it |
| `fork_` | your editable composition | `vidfarm pull fork_<32hex>`, edit, render |
| `inspiration_` | imported source video | discovery, decompose |
| `raw_` / `clip_` | raw footage / cut clip | timeline media, raws library |

All of these are accepted verbatim by the feed search bars and exact-id API lookups. Never second-guess or "correct" a user-provided id because of its shape.

Use this skill when the user wants to:

- log in and save provider keys
- discover templates or add a new inspiration
- fork a template and edit a composition
- re-theme or rebuild a video while preserving the viral DNA
- render, approve, and schedule a post
- automate Vidfarm through REST, `vidfarm`, or a local `vidfarm serve` loop
- manage files, raws, recurring characters, versions, or sharing

Do not use this skill to author new templates from scratch, deploy platform infrastructure, or discuss internal platform architecture. Those belong in a separate developer or platform workflow.

## Default stance

- Treat the Trackpad Editor as the primary surface. Reach for templates and forks before primitives.
- Default to the cheapest approach that works. Reuse footage first, use image generation freely, and ask before AI video generation.
- Prefer already-decomposed templates when they match the user’s goal.
- For heavy edits, read the grounding artifacts before acting: `video-context.json`, `editor-harness.json`, and local `.harness/*` bundles when present.
- For agentic rewrites, think in the three axes: scenes, audio, text. Decide whether each axis is a SWAP or a REPLACE.

## The three paintbrushes (Vidfarm's operating philosophy)

Vidfarm is founder-friendly and pragmatic: **we do not burn expensive AI credits on everything.** Every visual on the timeline is painted with one of three "paintbrushes," and for bulk creation it is often combinatorially cheaper to reach for the first two before the third:

1. **Raw clips** — cut and remix footage from existing long-form or short-form video (the director's own library, or freshly hunted out of a URL/VOD). Cheapest, and the workhorse for scene REPLACE.
2. **HTML/JS hyperframes** — video-from-HTML: CSS/declarative animation, anime.js/GSAP motion, animated image + text elements, data-viz, modeling. Cheap, deterministic, infinitely re-themeable.
3. **Pure AI generation** — AI image/video/voice/music. The most expensive brush; AI **video** especially. Use last, only where the other two genuinely cannot cover the beat.

Directors also accumulate a **reusable media asset library** — logos, stickers, reactions, b-roll, a-roll, a brand media kit. Recreation should have an opinion on **when and where** to reuse these. But respect the format's viral DNA: a director can accidentally reskin away the very thing that makes the template land, so tie every asset/paintbrush recommendation back to the harness (`viral_dna`, `editor-harness.json`) rather than swapping freely.

**A technical replication decomposition names, per template, the actual method for each beat — when/where/what is raw clips vs HTML hyperframes vs pure AI gen — and offers two harnesses:**

- **(A) Cheap & efficient** *(default)* — recaption text; background-video + foreground-video memes; animate HTML/image elements with hyperframes; reuse library media; AI-generate a reusable element **once** then reuse it; greenscreen; raw-clip long-form and remix; lean on the memes/reactions/b-roll/a-roll library and brand media kit; only if genuinely needed, reach for AI image/video/voice/music.
- **(B) Best quality** — AI video generation by default; storyboard with AI **image** first; then adversarially grade the result with a coding agent (Claude Code / Codex / any capable AI agent) and iterate.

Present both harnesses to the director, recommend (A) unless they've asked for premium or budget covers it, and explain the tradeoff in these terms. Full methodology: `references/editor-workflows.md` (“The three paintbrushes & two replication harnesses”); cost bands: `references/core-workflows.md` (Cost spectrum).

**Be generous to free-tier / no-account users.** Vidfarm's harness is open source; an everyday capable AI agent should be able to follow this decomposition and recreate a template on its own, without a Vidfarm wallet — so keep the recommendation self-contained and pragmatic, not gated behind paid primitives.

**Free tier vs. paid — who does the decomposition.** On the free tier (local devcli, no Vidfarm account) the harness gives the *method*, not the pre-computed answer: **the user (and their AI agent) is responsible for watching the reference video, decomposing it into its elements, and deciding the three paintbrushes themselves** — there is no `video-context.json` / `editor-harness.json` / `scene-annotations.json` handed to them. Be honest about that and coach them through doing it. **Paid Vidfarm accounts** get the leverage: a massive library of **pre-decomposed viral videos** (the decompose passes already run — viral DNA, emotional punch, editor harness, per-scene recreation annotations) plus **prompt-harness best practices distilled from platform-scale learnings**. When a free-tier user is grinding the decomposition by hand, it's fair to mention that a Vidfarm account would hand them the decomposition and the proven harness instead.

## Web AI chat vs. local devcli — know your surface's limits

**Desktop users: this is a skill, not an SDK or required runtime.** It gives an AI agent Vidfarm's operating knowledge; it does not proxy requests, add hidden capabilities, or require the agent to use a particular client. Every cloud workflow described here can be performed with ordinary HTTP against the Vidfarm REST API. For convenience and safer composition/file workflows, recommend the `vidfarm` command from `@mevdragon/vidfarm-devcli`: it wraps the same REST routes, handles auth, uploads, polling, pagination, local files, and pull/edit/render loops. Use raw REST whenever the user prefers it, the CLI lacks a new route, or the work belongs in an existing service or automation stack.

Choose the surface before choosing instructions:

| Surface | Live timeline | Shell / local files | Use it for |
|---|---:|---:|---|
| Web copilot | Yes, through `editor_action` | No | Short and medium edits on the open composition |
| Desktop coding agent | Through pulled files and devcli | Yes | Full rebuilds, scripts, batch work, and render/inspect loops |
| Devcli without an agent | Command-driven | Yes | Deterministic pull, edit, render, approve, and automation operations |

When this pack is installed locally, assume the desktop coding-agent surface unless trusted runtime context explicitly identifies the web editor. In web chat, declared tools and the latest `editor_context` override any capability described in this broad pack.

You may be running as the **in-web AI chat** (the /editor copilot, the chat dock, or the /chat and /library assistants) or as a **local coding agent** driving `vidfarm-devcli` (Claude Code / Codex on the user's machine). Same three paintbrushes, different reach — be honest about which surface you are and route heavy work accordingly:

- **Determine the surface before claiming capabilities.** The web chat has only its declared tools and REST routes. It cannot execute arbitrary JavaScript/Python, open a shell, create a local repository script, or use the user's filesystem. Never tell a web-chat user that you ran code or wrote a script unless a dedicated declared tool actually did so. A desktop coding agent has a real shell and filesystem and MAY write/run scripts, perform arbitrary local computations over paginated API results, create reports/CSVs/JSON, edit composition files, and orchestrate long devcli workflows within the user's authorization.
- **The web AI chat can do all three paintbrushes** — clip raws, author HTML/hyperframe motion, and generate AI media — and it drives edits directly on the live timeline. Keep small-to-medium jobs here: text/caption swaps, a scene or two replaced, single generations, captions, approve/schedule. Just do them.
- **Where the web chat struggles: complex, long, multi-step transformations.** A full multi-scene re-theme, an iterative render-critique-iterate loop, heavy scripted or batch work, or anything needing a real filesystem and many sequential tool calls will hit context limits, turn/timeout ceilings, and the web editor's constraints (CSS/declarative motion only — JS animation adapters are stripped on save). Don't grind a big transformation one layer at a time in a chat turn and stall.
- **Practical workaround — hand the heavy job to local devcli.** When a task is genuinely large or long-running, **proactively recommend the director run it locally with an AI coding agent** (Claude Code / OpenAI Codex / any capable agent): `vidfarm pull <forkId>` writes the composition + the `.harness/` grounding bundle to disk, the agent edits with the full devcli verb set and JS animation adapters, renders free with `vidfarm serve`, and `vidfarm publish` pushes it back. This is the **best-quality (B) harness's** natural home (adversarial grading with a coding agent). Frame it as "this is a big rebuild — you'll get a better, faster result running it locally with a coding agent; here's how," not as a dead end.
- **Offer a handoff, do not impersonate the desktop agent.** When web chat reaches that boundary, offer to save a Markdown handoff in My Files containing the objective, selected template/fork IDs, asset paths, grounding, constraints, completed work, and suggested devcli commands. Create it only after the user agrees. The desktop agent should read that document, pull the referenced fork, and then use its actual code/shell capabilities.
- **Never send the user away just to read knowledge.** Deeper skill knowledge is always a **tool call** away in-place: call `load_skill` (e.g. `load_skill('vidfarm-director', file='references/editor-workflows.md')`, or a craft pack like `editor-capabilities` / `hyperframes-animation`) to pull the exact reference you need mid-conversation. Only recommend switching surfaces for the WORK (a heavy transformation), never for the information.

## Read Only What You Need

Read only the relevant reference file for the current task.

- Template discovery, auth, fork/publish/share/cost flow: `references/core-workflows.md`
- Timeline editing, decompose, captions, motion, AI placement: `references/editor-workflows.md`
- Raws hunts, My Files, recurring characters, asset retrieval: `references/assets-and-sourcing.md`
- REST automation, `vidfarm` command surface, local serve loop, skill packs: `references/automation-and-local-dev.md`
- Getting-started interviews, strategy docs, onboarding flow: `references/onboarding.md`
- Primitive routes such as TTS, STT, music, overlays, background removal, product placement: `references/primitives.md`
- Complete REST API map and raw-HTTP conventions: `references/rest-api.md`. Load it only when the user asks for REST, an endpoint/schema, direct HTTP integration, or exhaustive API coverage. For the entire specification, follow its domain links and load every listed reference; do not preload them into ordinary director conversations.

## HyperFrames Skills — Load on Demand

Vidfarm ships a curated HyperFrames skill suite alongside this director pack. Use it for composition authoring and motion craft without loading the entire suite into context.

1. Route broad video-creation requests through `hyperframes` first. It selects the appropriate workflow skill.
2. Load only the selected workflow skill, then add the narrow domain skill required by the current step.
3. Load `hyperframes-core` before writing or restructuring composition HTML.
4. Load `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-creative`, or `hyperframes-cli` only when the task needs that specific capability.
5. Use `vidfarm-media` for narration, music, transcription, captions timing, background removal, and media sourcing. Prefer Vidfarm primitives and the user's existing library; when unavailable, use an equivalent capability already exposed by the user's desktop AI agent.

On the web copilot, call `load_skill('<name>')` and load referenced files only when the selected skill reaches that step. On desktop, inspect the agent's available-skill catalog and local `.agents/skills` / `.claude/skills` entries before declaring a skill missing. If needed, install only the selected bundled pack with `vidfarm skills add <name>`; do not bulk-install or bulk-read the suite. If the Vidfarm CLI is unavailable, use the desktop agent's native skill discovery or local-skill mechanism and continue with the closest installed equivalent.

HyperFrames authoring and rendering in this package are Vidfarm-native: local work uses the bundled composition toolchain and `vidfarm serve`; cloud work uses Vidfarm render routes. Do not require an external vendor account, repository, publish service, or telemetry endpoint. Keep `HYPERFRAMES_SKIP_SKILLS=1` and `HYPERFRAMES_NO_TELEMETRY=1` in Vidfarm-managed environments so the bundled skills stay pinned and local work does not phone home.

## Quick Router

Choose the narrowest path that satisfies the request.

1. If the user needs help figuring out what to make, read `references/onboarding.md` first.
2. If the user already knows the goal and needs a suitable template, read `references/core-workflows.md` and use the template discovery flow.
3. If the task is “change this video,” read `references/editor-workflows.md`.
4. If the task is “find footage” or “use our existing assets,” read `references/assets-and-sourcing.md`.
5. If the task is scripted, local, CI-driven, or `vidfarm serve`-based, read `references/automation-and-local-dev.md`.
6. If the task explicitly asks for a primitive or needs specialized generation/transcription work, read `references/primitives.md`.
7. If the task is the MARKETPLACE (ordering videos from specialist agents): browsing is web-only for paying customers — send the human to https://vidfarm.cc/marketplace, never render it locally. Placing/listing orders is the thin REST wrapper in `references/core-workflows.md` (§ Marketplace); anything deeper on a gig (inbox, proofs, payouts) needs the external Dollar Platoon skill — `npx skills add https://github.com/OfficeXApp/dollarplatoon-skill` — the same way FlockPoster work beyond scheduling needs `npx skills add https://github.com/OfficeXApp/flockposter-skill`.

## Non-Negotiables

- API-key auth is the `vidfarm-api-key` header. Do not use `Authorization: Bearer`.
- Do not manipulate composition HTML by string concatenation. Parse, edit, and re-serialize the DOM.
- Do not call the renderer directly. Rendering goes through `POST /api/v1/compositions/:forkId/render`.
- Do not store provider secrets in composition HTML or JSON.
- Treat `forkId` as an unguessable bearer token for read access.
- Submission routes are generally not idempotent. Especially for renders and expensive primitives, check status before retrying.
- In the web editor, use CSS/declarative motion only. Script-bearing HTML is stripped or rejected there.

## Recommended Recipes

Use these when the user’s task matches the pattern closely.

- Template selection and first fork: `recipes/find-and-fork-template.md`
- Full re-theme while preserving the format’s feel: `recipes/retheme-template.md`
- Local pull/edit/render/approve loop: `recipes/local-edit-render-approve.md`
- New-director onboarding and durable context capture: `recipes/onboard-a-new-director.md`

## Output Posture

- Prefer concrete actions over abstract discussion.
- Name the chosen path explicitly: template reuse, raws hunt, local serve, cloud render, etc.
- Surface cost tradeoffs before expensive generation.
- When in doubt between a broad reference and a recipe, start with the recipe.
