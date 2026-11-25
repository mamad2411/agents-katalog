---
name: forgeax-engine-sdk
description: >-
  ForgeAX SDK onboarding, capability discovery, production, and acceptance. Use when
  receiving the SDK, choosing Engine features, building a ZIP, publishing a dev, rc
  or stable version, checking reproducibility, or diagnosing bootstrap.
---

# ForgeAX Engine SDK

## Start here for game work

The game-root `AGENTS.md` already gives the hard rules, default commands and routing.
Reach a first correct edit with this short path, not by reading large skills up front:

1. Signatures and import paths: the API index before
   searching `node_modules` READMEs or `.d.ts` files.
2. Effect recipes for an `empty` project: the effects cookbook (~2 KB index: water -> stock `single-layer-medium`, fog/beam -> `beam-pillar`, indoor emissive ->
   `runtime-light-emissive`, rain/snow/fire/sparks -> `particles-*`). Open ONLY the file you need.
3. Commands: the **Quick contract** at the top of
   [`forgeax-engine-cli`](../forgeax-engine-cli/SKILL.md); camera, lights and post
   effects: the Quick contract of
   [`forgeax-engine-render-pipeline`](../forgeax-engine-render-pipeline/SKILL.md).
4. Deeper needs: pick one row in the capability table below and read only that skill's
   relevant section. Project layout, assets and setup live in the
   game project guide; acceptance, release and
   blocked checks in the game delivery guide.
5. A Three.js effect: look up its native equivalent and gaps in
   `references/three-equivalents.md` before simplifying it.

Large skills (`forgeax-engine-cli`, `forgeax-engine-render-pipeline`,
`forgeax-engine-debug`, `forgeax-engine-material`, `forgeax-engine-app`) are references:
search them for the needed heading instead of reading them whole, and do not re-read a
file already in context.

## Visual self-review

For look-dev use `forgeax dev look --hide-ui true --json` after each lighting, material,
fog or camera edit (seconds against a running `dev start --headless true`; it waits for
your edit and reports luma, saturation, contrast, clipping and subject separation with
findings); use `project play` only for gameplay acceptance. After the first look, and
again before delivery, open the PNG and answer each question in one sentence; fix every
"no", then look again:

1. Brightness: does the frame read as the brief's time of day (daylight bright, night dark
   with lit pools), with no blown-out white or crushed black areas?
2. Saturation: are colours as vivid as the brief implies? A pale or grey frame usually
   means fog over the subject, a cool `Skylight` fill or AgX.
3. Contrast: does the subject stand out from its background? A flat slab or empty void
   behind it needs a `SkyboxBackground` with an authored sky asset or set dressing.
4. Mood: do palette and lighting match the brief's words (warm, eerie, neon, cosy)?
5. Framing: does the subject fill about half the frame, with nothing clipping the near
   plane or blocking the camera, and the HUD off the subject?

## First five minutes: understand before authoring

SDK `init` and project `new` return the local `AGENTS.md` and this skill in
`onboarding.read`. Read those entries, select the requested delivery scope in the
game's guide, and load only the focused skills/package contracts needed now.
Use the capability catalog on demand for discovery;
its historical audit snapshot is neither current-HEAD proof nor an enablement list.

For a new or resumed game task, read the game's local `AGENTS.md` before editing.
Its **Run, test, build, and release** section selects local playable delivery, game
release or a specialized task. Follow that selected scope and stop condition. SDK
archive verification does not replace game acceptance.

> [!IMPORTANT]
> Available is not enabled. A package in the SDK means the capability can be selected; a game enables it only through its `forge.json`, plugin composition, ECS components, assets, renderer features, or build configuration. Do not install or register every capability.

Translate the requested game into a small capability adoption plan before editing:

```text
Need: <player-visible or production requirement>
Use: <one ForgeAX capability and its owner>
Entry: <focused skill, CLI operation, or package README>
Proof: <test, asset verification, browser evidence, or package output>
Defer: <available capabilities not needed now>
```

| Need | Start with | Proof before claiming it works |
|:--|:--|:--|
| Frame loop, execution tier, input, plugin assembly | `forgeax-engine-app`, then `forgeax-engine-ecs` or `forgeax-engine-state` | Unit/system test plus real browser interaction |
| Scene, imported files, code-first packs, GUID loading | `forgeax-engine-assets`; discover operations through `forgeax-engine-cli` | `asset verify`, build catalog, runtime load by GUID |
| Code-authored props, hard-surface parts and kit meshes | `forgeax-engine-modeling` | `m.validate()` closed/volume facts, exported MeshAsset, browser pixels |
| PBR, textures, custom WGSL | `forgeax-engine-material`, then `forgeax-engine-shader` | Shader check, material readiness, browser pixels |
| Lighting, shadows, sky, fog, AA, post effects, custom passes | `forgeax-engine-render-pipeline` | Requested pipeline active and real GPU/browser evidence |
| Particles: rain, snow, sparks, dust, fire (`Points`, effects/particles-core.md); GPU particles, trails, ribbons, beams | `forgeax-engine-vfx` | Path choice; cooked effect, runtime playback, browser pixels |
| Bodies, colliders, character motion | `forgeax-engine-physics` | Fixed-step/collision test plus playable behavior |
| BGM, SFX, spatial audio | `forgeax-engine-audio` | Host playback, intent/cleanup evidence, user gesture handling |
| Black frame, wrong binding, GPU divergence | `forgeax-engine-rhi-debug`; use `forgeax-engine-debug` for symptom routing | One capture artifact, inspect/replay or paired differential |
| Create, inspect, develop; build/preview/package when requested | `forgeax-engine-cli` | The selected game delivery scope passes |

Create a game only after selecting its template: `forgeax project new <dir> --template game-3d` for every
3D game; use `--template empty` otherwise. Missing selection is `sdk-template-required`.

> [!IMPORTANT]
> `game-3d` is a runnable, contentful third-person reference, not an empty 3D scene. It copies
> authored scene/physics, character/animation, material/mesh, and UI examples into the new project;
> those examples affect visible composition, collision space, and asset closure. After creation,
> read the generated project's `README.md` and keep, adjust, replace, or remove starter content by
> game goal; update scene, runtime, and pack references together when removing it.

Use the full capability catalog for less common areas such as animation/skinning, UI/font/video, picking, networking, intelligence, profiler, Remote, custom RenderGraph/RHI work, and source-mode Engine development. Then read only the focused skill and owning package README. The catalog is a discovery index, not a substitute for those precise contracts.

For browser-compositor screenshots, software/hardware backend selection, Engine frame readiness, repeated play-test checkpoints, and local Engine binding, use the browser capture and local-Engine guide.

The default game-consumer route is:

```mermaid
flowchart LR
  A[SDK init] --> B[Read onboarding paths]
  B --> C[Create external game]
  C --> D[Choose smallest capability set]
  D --> E[Author code and assets]
  E --> F[Test and asset verify]
  F --> G[Browser dev and visual proof]
  G --> H["Deliver local playable game"]
  H -. "User requests release" .-> I["Game release route"]
```

Run `forgeax help --tree --json`, then `forgeax help <command-path> --json`, before guessing authoring-operation inputs. Use the CLI skill for the command boundary. Start the seven-stage ForgeAX closed loop only when the user explicitly authorizes it for the current task.

Successful `new` also performs a two-second, best-effort check of the configured npm registry's `@forgeax/engine-sdk` channel tag (`next` for a development SDK, `latest` for stable; an rc SDK compares both `rc` and `latest`, so it is offered the promoted stable). Only a strictly newer semantic version produces a text warning; JSON always records `sdkUpdate` as `available`, `current`, `skipped`, or `unavailable`. Offline mode and `FORGEAX_DISABLE_UPDATE_CHECK=1` skip the query, and registry failure never rolls back a created game. Treat the warning as information, not migration authority: install the newer SDK in another directory, read its release notes, then migrate and test each existing game explicitly. Games remain pinned and are never rewritten by SDK discovery.

## SDK production and publication

For SDK carrier path failures, compare canonical download and resolver-selected
Engine roots at the existing containment owner. Qualify aliased parents and
out-of-download package redirects through the same installer; retain version,
digest, writable-output and empty-target checks. Follow
[SDK consumer diagnostics](../../scripts/ci/README.md#sdk-consumers).

Both SDK transports include editable `source/engine/` with the same release's
prebuilt package outputs. For a focused Engine change, install source dependencies,
rebuild the changed owner and bind through `project engine use-local`; unchanged
owners reuse their delivered builds. Follow the local-Engine guide
for binding and the SDK README for the partial rebuild commands.

Archive and post-consumer integrity stages reread byte counts and SHA-256 through
the existing bounded file-I/O owner. A canceled integrity tail is unverified;
retain every artifact and the SQLite-only mutable-store exclusion. See
[SDK consumer diagnostics](../../scripts/ci/README.md#sdk-consumers).

For a source-consumer job cancellation, compare complete stage timings first.
After the independent cold Engine rebuild, Preview and View use that rebuild's
shared manifest. Preserve the source-edit proof, full Browser journeys and
integrity checks; duplicate input production does not justify a longer deadline.

If a source consumer with precompiled Rapier unexpectedly requests Rust, compare
its `SDK_SOURCE_WASM` closure with the complete producer receipt, including the
3D SIMD glue and declarations. Follow [native artifact admission](../../scripts/ci/README.md#native-rapier-artifact-admission);
repair missing exported files without bypassing source, inventory or digest checks.

For an explicitly requested Engine/SDK change, SDK archive verification or SDK
publication, read SDK production. Its exact-ZIP
subject is the SDK distribution. Game ZIP packaging belongs to the game's release
route; ordinary game creation does not enter Candidate, Promotion or SDK consumers.
For channel/source and publication ordering, read the
release contract: `main` publishes `next`,
the weekly `rc` test line publishes `rc`, and `stable` publishes `latest`. GitHub
and npm publish independently after source qualification of mirrored channels;
the source mirror retains its formal GitHub Release identity check and advances
public `main` (development) or `stable` (stable). Stable Promotion then copies the
original verified Release assets to the public repository through `sdk-release-public.yml`;
use that workflow with an existing stable version to backfill or retry. Delivery
requires the public Release and every other enabled stage.

> [!IMPORTANT]
> Every SDK publication starts with
> Select the release flow first:
> name the flow (development, rc cut/fix, rc promotion or stable hotfix), version,
> source SHA and npm tag before pushing a release branch or dispatching a workflow.
> If the user's request leaves any of them open, ask the user; never guess a
> channel or version.

## Plugin asset authoring

Create functional Packs: export small native behaviors from the same file, and split
complex implementations into ordinary TypeScript modules. Follow the
[Plugin contract](../../packages/plugin/README.md): persistent definitions live in
Pack, and schema-v3 project `roots` select their GUIDs. Use `asset plugin inspect`
to check sourceKey and definitions, then inspect native Fiber state to confirm
activation. Verify a new session after code or configuration changes; engine and
frontend effects own scene and DOM cleanup respectively. For source reuse, read
`help asset source import` or `help asset source clone` and transfer the author closure.
