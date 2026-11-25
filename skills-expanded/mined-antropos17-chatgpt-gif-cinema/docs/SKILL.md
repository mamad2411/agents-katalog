# Multi-scene stories and motion-design GIFs

[Back to GIF Cinema](../README.md) · [Skill instructions](../.agents/skills/gif-cinema/SKILL.md)

GIF Cinema's current repository skill can plan a longer animated story, prepare
individual generation inputs, select hash-verified GIF takes, add local animated title
cards, and export MP4 and GIF. It is a production workflow with executable helpers,
not a new animation model or a promise of automatically smooth character motion.

## Two examples, two different claims

**Runnable source edit:** the bundled astronaut example uses three existing GIFs
and a locally animated title. It exports a 9.68-second silent MP4 at 512 × 512,
25 fps; the default 320 × 320 GIF is 9.70 seconds at 10 fps. The three character
clips still contain only 16 source drawings each. Output FPS is not new animation.
All steps below run locally with zero API calls.

**Long-story plan:** *The Lantern Delivery* has 14 distinct intended actions: discover,
open, lift, light, arrival, point, approach, test, cross, reach, place, settle, wave,
and leave. Its requested 14 × 2.56-second takes total 35.84 seconds. These scenes
have **not been generated**. The planner emits 14 individual request scripts and an
assembly template with missing media explicitly identified. It does not execute a
paid batch or present a storyboard as a finished cartoon.

## Try the current repository skill

Install the repository runtime using the main README, then run from the repository
root. `PYTHONPATH=.` lets the standalone skill helper import that checkout's runtime
without altering another Python environment (Windows: set the equivalent environment
variable, or use the installed runtime).

```bash
PYTHONPATH=. python .agents/skills/gif-cinema/scripts/story_project.py compile \
  .agents/skills/gif-cinema/assets/example/storyboard.json --out output/story-project
python -m gif_cinema render output/story-project/film.json --dry-run --max-api-calls 0
python -m gif_cinema render output/story-project/film.json --execute --max-api-calls 0 --out output/story-render
PYTHONPATH=. python .agents/skills/gif-cinema/scripts/story_project.py export-gif \
  output/story-render/film.mp4 --out output/story.gif --width 320 --fps 10
```

The project includes the editable storyboard, readable shot list, copied footage,
generated title GIF, runtime script and timing/source report. The runtime adds a
contact sheet, first/last frames, continuity review, SRT and verified MP4. Run render
again with the same arguments to check zero-call resume.

Prepare the longer plan without generating any shot:

```bash
PYTHONPATH=. python .agents/skills/gif-cinema/scripts/story_project.py compile \
  .agents/skills/gif-cinema/assets/example/long-story.plan.json --out output/lantern-plan
```

See [the exact helper schema and limits](../.agents/skills/gif-cinema/references/story-project.md).
The independent [existing-GIF story demo](GIF-STORY-DEMO.md) is a separate fixed edit,
not the generic planner or a newly generated long cartoon.

## From a brief to a finished story

1. **Plan changes, not padding.** Write the ending, causal beats, and first/action/last
   state of each short shot. A repeated clip with another caption is not a new action.
2. **Fix the visual bible.** Keep identity, materials, palette, costume, prop ownership
   and geography explicit. Preserve the requested style rather than forcing pixel art.
3. **Prepare only missing actions.** Compile existing sources or individual generation
   inputs. Check actual API/tool support and the authorized call budget before execution.
4. **Review and accept takes.** Inspect identity, contacts, incoming/outgoing poses,
   and cause/effect. A clean reference and an accepted last frame can guide another
   shot; they do not guarantee continuity.
5. **Select and preserve.** Record reviewed GIF paths, SHA-256 hashes and notes in a
   takes manifest. `compile --takes` fills generated slots, verifies those exact bytes,
   keeps original requests and replaces planned timing with actual source delays.
   Partial selection is supported; missing actions stay explicit.
6. **Edit and deliver.** Continue from the portable `storyboard.json` into a new project,
   preserving earlier sources and title GIFs byte-for-byte. Once all actions exist,
   assemble the MP4 with a zero-call cap, then export the GIF. Review final encoded
   files, not just source frames. Caller review notes do not prove visual acceptance.

The bundled `storyboard.pending.json` and `takes.example.json` exercise the entire
plan-to-selected-media workflow using the same three existing astronaut GIFs, with
zero requests. See [the selection format and commands](../.agents/skills/gif-cinema/references/story-project.md#select-reviewed-takes).
Each generated slot can receive a different reviewed action, so longer stories can
be completed progressively without replacing earlier shots. The 14-action plan still
requires its own footage; this update does not generate or claim a completed long cartoon.

The title renderer supplies a once-only text entrance and animated accent rule, with
an editable hold. It does not provide layered prop animation, generated poses,
interpolation, automatic transitions, sound generation or a rigged character engine.
For those requirements, use a genuinely available compositor or generation service
and describe its role. Source-only editing can proceed when generation is unavailable.

## Deliver longer stories as GIF chapters

Keep the verified MP4 as the master. To deliver smaller GIFs without cutting an
individual shot in half, group the completed film into whole-shot chapters:

```bash
PYTHONPATH=. python .agents/skills/gif-cinema/scripts/story_chapters.py \
  output/story-project/film.json --render output/story-render \
  --out output/story-chapters --width 320 --fps 10 --max-seconds 5 --dry-run
PYTHONPATH=. python .agents/skills/gif-cinema/scripts/story_chapters.py \
  output/story-project/film.json --render output/story-render \
  --out output/story-chapters --width 320 --fps 10 --max-seconds 5
```

The existing 9.68-second source edit becomes three GIFs: 4.6, 2.6 and 2.6 seconds.
The title stays with the first astronaut shot. Each GIF's final hold is rounded up
to a 100 ms frame, so their combined 9.8 seconds is slightly longer than the master.
No shots are duplicated or omitted; this is not newly generated animation.

Dry-run validates input hashes and measured GIF timing without output writes or
FFmpeg. Export verifies and snapshots the actual MP4, trims by source-frame boundaries,
checks every GIF, and publishes a new directory with a `chapters.json` receipt. The
completed render folder must retain its manifest and saved shots. One shot exceeding
the chosen budget fails with guidance instead of being split automatically.
[Exact limits, verification and timing](../.agents/skills/gif-cinema/references/story-project.md#export-whole-shot-gif-chapters).

## Package and verify the skill

The previously published `skill-v0.1.1` ZIP is an older skill. To package the current
repository version, including examples, scripts, references, license and notices:

```bash
python tools/package_skill.py --out dist/gif-cinema-story-skill.zip
python -m unittest discover -s tests -p 'test_story*.py' -v
```

The source-built skill version is 0.2.1, separate from the runtime's 0.5.0 version.
It adds full-frame review and offline sprite workflows to the maintained story
helpers. `runtime.json` pins the immutable runtime commit containing their required
interfaces. No release tag or release asset is created by the packaging command.

The ZIP is byte-reproducible, has a single `gif-cinema/` root, and contains only an
explicit resource allowlist. Stored ZIP entries avoid zlib-version differences;
timestamps, order and permissions are fixed. `package-manifest.json` records the
size/SHA-256 of every resource. Hashes are revision checks, not publisher signatures.
The CLI/runtime, Python, Pillow and FFmpeg are **not** bundled. Git/network access is
needed for the documented runtime install; no provider access is required for local
review, sprites or source-only film assembly. Extract it into the agent's skill folder. Follow its
runtime setup, then use the same compile/render/export sequence. The pinned runtime
is immutable; no API access or model availability is implied by a successful install.

The story workflow is informed by [GIF Factory](https://github.com/WoYun520/gif-factory),
particularly its separation of style/movement/purpose and once-only causal actions.
Its MIT notice is preserved in the skill's [third-party notices](../.agents/skills/gif-cinema/THIRD_PARTY_NOTICES.md).
No GIF Factory artwork, fonts or exporter code are bundled. GIF Cinema keeps its own
[source-available evaluation license](../LICENSE).

## Animated story-page layouts

Compose existing GIF actions with editable headings and body text, in landscape or
portrait, using the [offline story-page helper](STORY-PAGES.md). It preserves actual
source cadence, exports play-once GIF pages and a portable project, and emits a
zero-call film script. No new artwork or poses are generated.


### Check the actual extracted installation

From the extracted skill folder, follow its pinned-runtime installation, then:

```bash
python scripts/check_install.py
python scripts/smoke_media.py --out ../project/media-smoke
# With FFmpeg and ffprobe installed:
python scripts/smoke_test.py --out ../project/full-smoke
```

Use new output paths outside the installed skill. `check_install.py --files-only`
needs only Python and verifies packaged resource hashes. A source checkout without
a generated manifest is reported as such, not claimed hash-verified.
The media smoke test blocks network, checks both sprite commands and decoded
full-frame review, and leaves review/acceptance pending. The full smoke test also
checks film assembly and zero-call render/resume. These are synthetic behavioral
checks, not proof of generated character quality or human visual acceptance.

The Linux/Python 3.12 CI job also builds the ZIP twice, compares its bytes and
uploads the ZIP plus SHA-256 as the `gif-cinema-skill-0.2.1` workflow artifact
(retained for 14 days). An Actions artifact is not a permanent GitHub Release.

### 0.2.1 workflow fixes

Story/chapter/page GIF delivery now uses the same 512-frame, 64-Mi-pixel and 32-MiB
limits as full-frame review, rather than publishing an export that the next required
step cannot open. Direct MP4 export snapshots bounded regular local files, pins
the input hash, forces MP4 decoding and disables external data references. Chapters
and story-page readers explicitly preserve binary bytes on Windows. These are
workflow/correctness fixes; the pinned runtime and generation behavior are unchanged.
