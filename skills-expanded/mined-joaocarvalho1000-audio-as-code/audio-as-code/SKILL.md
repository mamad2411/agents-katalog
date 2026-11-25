---
name: audio-as-code
description: Compose or revise original instrumental music with the local Audio as Code framework, delivering rendered WAV, MIDI, editable scores, and reproducible source. Use when a user wants music made with this framework or changes to an existing Audio as Code composition.
---

# Audio as Code

Turn the user's musical brief into actual local artifacts. You make the artistic
decisions; the framework validates, synthesizes, exports, and measures. A person
can describe the music without writing code. You need a shell, a writable project,
and Python 3.10+. No provider API key or language model is bundled or required by
the renderer. This is a portable instruction file, not a hosted API or MCP server.

## Get the local tool ready

Look for an existing Audio as Code checkout (`pyproject.toml` and
`src/audio_as_code/`) or an installed `aac --version` / `python -m audio_as_code
--version`. Reuse the project's environment.

To add the library to an existing Python project managed by uv, run from that
project's root:

```sh
uv add "audio-as-code==0.5.0"
uv run --locked aac --version
uv run --locked aac instruments
uv run --locked aac schema
```

This installs version 0.5.0 from PyPI. Keep the project's `pyproject.toml` and
`uv.lock` to record package and dependency versions. Use `uv run --locked` for
composition and rendering. Do not replace an existing application's lockfile
with the framework's lock. The wheel contains the engine and CLI; the portable
skill and bundled example scripts are available separately in the source project.

Without uv, create `.venv` with `python -m venv .venv`, then use
`.venv/Scripts/python.exe -m pip install audio-as-code==0.5.0` on Windows or
`.venv/bin/python -m pip install audio-as-code==0.5.0` on macOS/Linux. Invoke that
interpreter with `-m audio_as_code` and use it for composer scripts. No activation
is needed. Reuse an existing project environment rather than a global Python.

When a specific source revision is needed, Git must be installed. Use
`uv add "audio-as-code @ git+https://github.com/joaoCarvalho1000/audio-as-code.git@FULL_COMMIT_SHA"`,
replacing the placeholder with a verified full commit. Read the skill from that
revision; the installed catalog, schema and help describe its actual capabilities.

For a standalone workspace with the complete examples, download and extract the
source. From its root:

```sh
uv sync --locked --no-dev
uv run --no-dev aac --version
uv run --no-dev aac instruments
uv run --no-dev aac schema
```

For the standalone route, use the source ZIP URL supplied with the user's website
prompt, or the website's **Download source** link. Download and extract into the
working project, then run the commands above from the extracted folder containing
`pyproject.toml`. Read the bundled `skills/audio-as-code/SKILL.md` for that version.
Use the public repository above or a source location supplied by the user.
If source examples are needed and neither source route is accessible, ask for the
source ZIP or local checkout path.

For an editable source installation without uv, create `.venv`, then run
`.venv/Scripts/python.exe -m pip install -e .` on Windows or
`.venv/bin/python -m pip install -e .` on macOS/Linux. Use that interpreter with
`-m audio_as_code` in place of `uv run --no-dev aac`. No shell activation is necessary.
The `--no-dev` option installs only runtime dependencies. Initial dependency
installation needs network access or a populated cache;
rendering afterward is offline. Do not install into the user's global Python.

For a new composition workspace after installing the package, run
`aac init "my music"`, enter that folder, follow its README to create the local environment,
then run `aac doctor`. Init writes a composer, starter score and project files in
a new or empty directory; it does not install dependencies or overwrite existing
content. Doctor checks the imported runtime and a short synthesis without
writing audio; it cannot judge realism or check an audio device. See
[project setup](../../docs/project-setup.md).

## Compose the brief

Infer a useful first version from the requested mood, duration, instruments, use,
and form. Ask only for missing decisions that materially affect the result; do
not require a questionnaire or approval of a plan. State significant assumptions
briefly. Honor an existing composition and the scope of a revision.

Discover current playable IDs and each voice's `tone_controls` with
`aac instruments`; `--all` also includes planned voices. Read `aac schema` for the
accepted fields. Never claim an unavailable instrument is implemented or silently
substitute another voice. Sounds must come from the framework's procedural,
physical, or modal synthesis: no recordings, SoundFonts, sample-library backends,
or measured impulse responses as instrument sources.

Write a UTF-8 JSON score directly or write a reproducible Python composer using
`Note`, `Pattern`, `Song`, and `Track`. Keep the composer when you use one. Save
scores with `Song.save()` or an explicit UTF-8 writer; PowerShell 5.1 `>` can write
unsupported UTF-16. Use a fresh folder such as `output/my-piece/v1/` per candidate.

Make an original motif, develop it through rhythm, harmony, register or texture,
and provide an intentional ending (or a loop seam when requested). Give parts
musical roles and use rests, accents and changing density. A short identity sting
needs less development than a full piece. `aac demo` is an installation check or
starting reference, not an original answer to an unrelated musical brief.

Score essentials:

- `schema_version` is `"1"`; time is quarter-note beats from zero. BPM is 20–300.
  With no `tempo_map`, seconds = `beats * 60 / bpm`; otherwise tempo changes are
  ordered `{beat, bpm}` steps. Plan a WAV of at most 300 seconds including tails.
- Notes have `pitch`, `start`, `duration`, `velocity`; `start + duration <= beats`.
  Pitch is MIDI 0–127 or a name such as `C4` (= 60). Velocity is greater than 0
  and at most 1. Omit a note for a rest. `release_seconds` (0–10) can extend the
  sound after note-off; a note inherits its track release unless overridden.
- Thirteen bowed-string and wind voices accept optional `soft` or `accented`
  `articulation` on a track or note; the note overrides its track. Check each
  catalog entry's `articulations` list. Version 0.3.0 also adds
  acid-bass accent, bass-guitar slap/pop/muted and electric-guitar muted gestures;
  unsupported instrument/value pairs are rejected.
  These are designed source gestures, not recorded samples; MIDI omits them.
  See [articulations](../../docs/articulations.md).
- For disco, techno, trance or drum & bass, discover the installed catalog first.
  Version 0.3.0 adds electronic voices and effects documented in
  [electronic instruments](../../docs/electronic-instruments.md).
  Tone glide is explicit and note-local, not automatic legato.
  `Ducker` uses beat triggers, not an audio sidechain. Open hats need explicit gates.
- Tracks have unique `name`, playable `instrument`, `notes`, and optional `gain`,
  `pan`, `tone`. Gain and master gain are 0–1; pan is -1 to 1. Tone is per track
  and accepts only that voice's supported controls. Omit it for basic voices.
- Use 1–64 tracks and at most 100,000 notes. The format forbids extra fields;
  express sections, meter and swing through explicit notes and timing. Piano-only
  `pedal` accepts ordered `{beat, down}` events (`down` is a boolean), alternating
  down/up starting with down. The `piano` voice supports this binary damper gate;
  other instruments, including `electric_piano`, reject nonempty pedal lists.
  An open pedal lifts at song end and can add a damper tail, so check rendered
  duration. Read `docs/piano-sustain.md` for release precedence and limitations.
  Optional automation lanes target track `gain`/`pan` or song
  `master_gain`, using ordered `{beat, value}` points with `linear` or `step`
  interpolation. Values are absolute, not multipliers. Song and track `effects`
  accept ordered procedural `delay`/`reverb` chains; inspect the schema before
  writing their parameters. Release and effect tails extend the rendered WAV.
- For MIDI, use at most 15 melodic tracks, one track per individual drum ID,
  no overlapping same-pitch notes on a channel, and durations of at least one
  tick (1/480 beat). A `drum_machine` track shares channel 10 with individual drums;
  consult its catalog pitch map and avoid collisions.
- Keep the seed fixed across revisions unless changing stochastic excitation is
  intended. Reproducibility requires the same score, runtime and platform.

For a fixed video cut or presentation sting, convert the requested seconds to
beats, place cues explicitly, and plan the ending inside that duration. Check
`Song.render_seconds` as well as `Song.seconds`: releases and effects can extend
the WAV. At constant tempo a 30-second piece at 96 BPM is 48 beats and a cue at
20 seconds is beat 32. Keep section/cue metadata in a sidecar; custom score fields
are rejected. Check the exported WAV's actual frames against the target seconds
times sample rate, allowing one sample only when the target cannot be represented
exactly. Do not assume trimming an active tail creates a settled ending.
Across tempo changes, use `beat_at_seconds` or `place_at_seconds` for timestamp
cues. `Arrangement` and `Section` can revise named beat ranges while preserving
untouched score data. These helpers do not add section fields to score JSON; see
[arrangement](../../docs/arrangement.md).

For a loop, choose a musical period first. A dry arrangement with duration-gated
notes and intentional rests at the bar line is one supported approach. Measure
the saved PCM join and neighboring sample steps, export two unchanged cycles,
and audition their middle join when possible. Endpoint agreement alone does not
prove a convincing musical loop. `render_loop_preview` can repeat a chosen region
and report boundary measurements, but it renders the full song first and does not
make a wet loop seamless. Effect tails, releases and sustained textures still
need deliberate boundary handling. See [arrangement](../../docs/arrangement.md).
The source example `examples/creative_workflows.py` implements three original
briefs and constrained revisions; `docs/creative-workflows.md` explains the checks.

For finite releases and generated Delay/Reverb chains, source revisions with
`render_periodic_loop` can fold full tails into one periodic cycle. Automation,
pedal, mastering and other effects are rejected. See `docs/arrangement.md` and
`examples/pending_audio_experiments.py`; join statistics still require listening.
Use `examples/listening_evaluation.py OUTPUT --baseline BASELINE` to preserve
instrument comparisons with score/WAV hashes and a separate human rubric.
The experimental piano depth API uses sidecars only; never put depth in version
1 score JSON or claim that standard MIDI exports it. The experiment rejects more
than 300 seconds including its tail, 4,096 notes or 20,000,000 synthesized voice
frames. Its comparison writes sidecars, WAV hashes, release energy and local tuning
estimates; these measurements do not replace human listening. See
`docs/half-pedal-proposal.md` for event ordering and the pending compatibility decision.

## Render, inspect, revise

Use your chosen environment prefix. These commands assume the composer already
saved `output/my-piece/v1/score.json`:

```sh
uv run --no-dev aac validate output/my-piece/v1/score.json
uv run --no-dev aac inspect output/my-piece/v1/score.json
uv run --no-dev aac render output/my-piece/v1/score.json -o output/my-piece/v1/song.wav --report output/my-piece/v1/report.json
uv run --no-dev aac analyze output/my-piece/v1/song.wav
uv run --no-dev aac midi output/my-piece/v1/score.json -o output/my-piece/v1/song.mid
```

Default WAV is 16-bit PCM. Use `aac render ... --format pcm24` or
`aac render ... --format float32` when requested. Optional `--target-lufs -18` needs the
`audio-as-code[loudness]` extra and uses one constant gain subject to a sample
peak ceiling; it is not true-peak limiting. Use `--progress-file progress.jsonl`
for live UTF-8 JSON Lines without changing the final JSON stdout contract.
`aac preview score.json -o excerpt.wav --start 12 --duration 8` extracts exact
frames only after rendering the complete score, so it does not reduce synthesis
cost. See [production output](../../docs/production-output.md).

Add `--stems output/my-piece/v1/stems` when separate parts help or are requested.
Output paths overwrite existing files; keep score, WAV, MIDI and report distinct.
Success is JSON on stdout and exit 0; failure is JSON on stderr and exit 2. Help
is plain text. Fix `invalid_score` using `issues[].path` and `message`; cross-field
errors may have an empty path. For `operation_failed`, inspect `message` and
`hint`. A passing validator does not guarantee WAV duration or MIDI compatibility.
Use `aac inspect` before rendering to check export readiness and locate blockers
without synthesizing audio. Inspection exits 0 for a valid score even when an
export is blocked; read its `readiness` and structured `issues`, not only the exit code.

Read `warnings`, `gain_applied`, and `wav` peak/RMS/silence/full-scale counts in the
report. Correct unintended silence, clipping, timing errors and inaudible parts.
Attenuation below 1 is not itself a failure; balance gains when it obscures the
intended arrangement. Listen if audio perception is available. Measurements do
not establish musical quality, acoustic realism or a good loop seam.

Instrument source trims only reduce selected level outliers; they do not make
every voice equally loud. Balance the arrangement with track gains before choosing
master peak attenuation or LUFS targeting. Compare dry notes in useful registers
and short mixes, preserving velocity and transient differences. The contributor
audit is `examples/instrument_balance.py`; see
[instrument balance](../../docs/production-output.md#instrument-and-mix-balance).

With Audio as Code 0.4.0 or later, use `MixEdit`/`apply_mix` or `aac mix` for precise
group level/pan revisions. `trim_db` preserves gain envelopes; absolute automated
controls require `replace_automation`. Mute wins over solo. Keep the original
audition source. See [mix revisions](../../docs/mixing.md).

For fast bowed-string or brass figures, audition a short phrase first: normal
attacks can occupy much of a 60–110 ms note. Use supported `accented` articulation,
change the rhythm, or assign rapid figures to faster-speaking voices. Extra gain
does not restore a missing onset. Give different sections distinct lead/support
roles; reserve octave/unison doubling for deliberate emphasis. Compare stems
within each section and during their entrances, not only by whole-song RMS or
energy share. A sparse bell or cymbal can have low total energy and still be audible.

Compose short candidate scores for expensive arrangements, then render the
complete requested piece. An excerpt preview is useful to inspect a time range
but costs a complete render. Revise when the brief, listening, or diagnostics
justify it; do not run an unbounded optimization loop. For user feedback, preserve the previous version and
edit only what the request warrants. Stop when the requested artifacts are valid
and the stated brief is addressed; report unresolved limitations honestly.

Before rendering a revision, compare the preserved notes or whole tracks with
the original data, plus seed, tempo, cue positions and duration where requested.
Keep track names and unchanged note ordering stable because they affect seeded
excitation. After rendering, check actual duration and any loop seam again. A
revision that preserves score length can still change the WAV length via tails.

## Custom instruments and mastering (source revision)

These capabilities are newer than published 0.4.0. Check the installed schema and
help before using them; use a verified source commit containing the additions.

Define `Song.custom_instruments` using `CustomInstrument` and oscillator, noise,
modal or FM layers. Reference a definition by its `custom:` name in a Track.
Use `aac instruments --score score.json` to discover user-defined metadata.
Patches are bounded JSON data, never code or sample/IR paths. Existing Delay,
Reverb and other track/master effects work normally. Custom voices reject Tone,
pedal and articulations. MIDI needs an explicit approximate `midi_program`.
Read [custom instruments](../../docs/custom-instruments.md) for controls and limits.

Opt into `Mastering(compressor=BusCompressor(), limiter=TruePeakLimiter(),
target_lufs=-14)` on the song or render call, or pass `--target-lufs -14
--limiter-ceiling-dbtp -1`. Full settings are available via `--mastering FILE`.
Do not combine the limiter with `--peak-ceiling-dbfs`. Targeting needs the
loudness extra. Inspect `target_reached`, gain reduction, reconstructed true peak
and `encoded_measurements`; the ceiling wins if the target is unreachable.
Large reduction may sound undesirable. Stems omit bus dynamics. Exact preview
cuts can create new boundary peaks. Defaults remain the legacy rendering path.
Numerical tests do not establish perceptual realism; state whether listening occurred.

## Deliver

Link the actual WAV, MIDI, editable JSON score, render report, and composer source
if one was used. Include a brief musical description, duration, important warnings,
and whether audio was actually auditioned. Keep the score, seed, report and project
lockfile for reproduction. MIDI uses the receiving synthesizer's sounds; it does
not contain these voices, articulations, tone controls, automation, effects or audio releases.
Tempo changes and piano pedal CC64 do export; pedal release behavior depends on
the receiver. Stems omit master effects, so their sum differs from a
mix with master processing. Invite concrete revisions such as
“keep the melody, soften the drums, and make the ending longer.” Do not claim a
render was listened to or completed unless it was.

Optional source-tree reading: `docs/site/composition.md` for musical/API examples,
`docs/site/reference.md` for field details, and `docs/agents.md` for CLI integration.
The installed CLI and schema remain the authority if this file was copied alone.
