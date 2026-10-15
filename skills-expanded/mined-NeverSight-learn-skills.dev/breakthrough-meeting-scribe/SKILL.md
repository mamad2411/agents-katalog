---
name: breakthrough-meeting-scribe
description: "Turn meeting audio into three artifacts (a corrected transcript, an HTML visual canvas, and a Markdown summary with AI insights), transcribed locally with Whisper on any platform: no cloud, no external transcription app. Use when the user hands over a meeting recording or wants meeting notes from one (\"处理这个录音\", \"会议纪要\", \"把录音转成文字\", or an audio file lands in the configured drop-zone), wants an existing transcript corrected or cleaned (\"处理 transcript\", \"转录纠错\", \"转写文本\", or a .txt lands in the drop-zone), wants a recording pulled from their connected PLAUD account (\"process my Plaud recording\", \"从 Plaud 拿\"), asks for edits to a transcript, canvas, or summary this skill just produced, or asks for cross-meeting Insights on their communication patterns instead of processing one recording (\"analyze my meetings\", \"how do I come across in meetings\", \"分析我的沟通模式\", \"复盘我最近的会议\", \"跨会议分析\")."
---

# Breakthrough Meeting Scribe: Transcribe, Correct, Canvas, Summarize

## What this skill does

Take a meeting **audio file** (or an already-transcribed `.txt`), either dropped into the configured drop-zone or pulled from a connected PLAUD recorder account, and produce three artifacts:

1. A **corrected transcript** (light-touch cleanup, speech features preserved)
2. A **visual canvas** (single self-contained HTML, the whole meeting at a glance)
3. A **summary** (Markdown, with an AI-insights section)

Transcription always runs **locally** via Whisper (no external app), including for Plaud-sourced audio: Plaud is only a way for the audio to arrive, never a transcription backend, so a cloud provider's transcript quality and language handling never enter the pipeline. The artifacts are written **directly to the configured output destination**, never echoed in full to chat (echoing then writing generates the same content twice as output tokens and bloats context). The user reviews at the destination and requests edits there.

**Two modes.** The pipeline above (Phases 0-6) is the default, one meeting in, three artifacts out. A second entry point, **Insights mode** (see its section after Phase 6), runs when the user asks about their communication patterns ACROSS meetings: it reads the corpus of already-corrected transcripts and writes one analysis report. Route by intent: "process this recording" -> pipeline; "what are my patterns in meetings" -> Insights mode. Never run both in one pass.

All machine-specific behavior (where audio lands, which Whisper model to use, where artifacts go, what language to write in) comes from a per-user config file, NOT from this document. This skill is the orchestration logic only; it is portable across users and machines.

## Configuration

On load (when the user invokes this skill), **read the config first**:

```bash
cat ~/.config/meeting-transcripts/config.json
```

- **If it exists**: parse it and use its values for every path / model / language decision below. Do not narrate this read.
- **If it is absent**: run **First-run setup** (below) once, write the config, then continue.

### Config schema

```json
{
  "engine": "faster-whisper",
  "model": "large-v3",
  "model_path": "/abs/path/to/model",
  "engine_bin": null,
  "python_bin": null,
  "compute_type": "auto",
  "transcribe_language": "auto",
  "audio_dropzone": "/abs/path/to/drop-zone",
  "audio_archive": "/abs/path/to/processed-archive",
  "sources": {
    "plaud": { "enabled": false, "cli_path": "plaud" }
  },
  "output": {
    "mode": "folder",
    "folder_path": "/abs/path/to/output-folder",
    "vault_path": null,
    "landing_folder": null,
    "baseline_context_file": null
  },
  "language": {
    "transcript": "as-spoken",
    "canvas": "english",
    "summary": "english",
    "replies": "english",
    "register": null
  },
  "vault_context_skill": null,
  "diarization": { "enabled": false, "num_speakers": null, "seg_model": null, "emb_model": null }
}
```

Field notes:

- `engine`: transcription backend, one of:
  - **`whisperkit-cli`**: Apple Silicon Mac only (CoreML / Apple Neural Engine, fastest). `model_path` = the CoreML model folder.
  - **`faster-whisper`**: cross-platform default (Intel mac / Windows / Linux, CPU or CUDA; also fine on Apple Silicon). Python / CTranslate2. `model_path` = the CT2 model-cache directory, `python_bin` = the venv Python that has `faster-whisper` installed, `compute_type` tunes precision.
  - **`whisper.cpp`**: optional cross-platform binary (Metal / CUDA / CPU, no Python). `model_path` = a GGML `.bin` file, `engine_bin` = the `whisper-cli` binary if it is not on PATH.
- `model`: which Whisper model to run. Default **`large-v3`** for best quality on every engine; smaller ids (`medium`, `small`, `base`) trade quality for speed. **The model FORMAT is different per engine (CoreML folder vs CT2 cache vs GGML `.bin`) and the formats are NOT interchangeable**: first-run setup downloads the correct format for the chosen engine.
- `model_path`: where that model lives, per engine (see `engine` above).
- `engine_bin`: optional absolute path to the engine binary (`whisperkit-cli` or `whisper-cli`); `null` = found on PATH.
- `python_bin`: (faster-whisper only) absolute path to the Python inside the venv where `faster-whisper` is installed.
- `compute_type`: (faster-whisper only) `auto` (int8 on CPU, float16 on CUDA) or force one of `int8`, `int8_float16`, `float16`, `float32`.
- `transcribe_language`: Whisper language hint (`auto`, `zh`, `en`, ...). For code-switched audio, **set the dominant language rather than `auto`**: forced single-language decoding keeps inline foreign terms verbatim and gives higher-confidence, stabler output. On whisperkit-cli, `auto` was observed to add a mid-clip language-flip hallucination (a spurious German tail); on faster-whisper a real-audio test found `auto` harmless but lower-confidence (it stayed on the dominant language correctly), so forcing the dominant language is the safer default either way. Use `auto` only when the dominant language is genuinely unknown.
- `audio_dropzone` / `audio_archive`: where new audio lands, and where it (plus its `.txt`) is moved after successful processing.
- `sources.plaud`: optional remote ingest from a PLAUD recorder account, via the vendor's `@plaud-ai/cli`. `enabled: false` (the default) means the drop-zone is the only source. When `true`, Phase 0 can pull a recording's audio out of the Plaud cloud into `audio_dropzone`, after which the normal local pipeline runs unchanged. `cli_path` is the path to the `plaud` binary; prefer an absolute path, since npm global bins are often outside a non-login shell's PATH. Requires a one-time `plaud login` (browser OAuth, tokens cached in `~/.plaud/tokens.json`); this skill never handles credentials. See "Enabling Plaud ingest" below.
- `output.mode`: **`folder`** (write artifacts to `folder_path` via filesystem) or **`obsidian`** (write into an Obsidian vault via the mcp-obsidian tools; uses `vault_path`, `landing_folder`, optional `baseline_context_file`).
- `language.*`: output language per artifact. `transcript: as-spoken` keeps the spoken language(s) intact. `register` is an optional free-text style note (e.g. a regional register).
- `vault_context_skill`: optional name of a companion skill that supplies vault/notes grounding; load it alongside this one if set. `null` = none.
- `diarization`: optional speaker separation, **OFF by default** (opt-in). When `enabled: true`, Phase 0 produces a speaker-tagged transcript in the unified format `[mm:ss] Speaker A: <text>`; set `num_speakers` to the known participant count (or leave `null` to auto-detect). `seg_model` / `emb_model` are the local ONNX model paths for the `faster-whisper` diarization add-on (set during the optional diarization setup below; unused by `whisperkit-cli`, which has native diarization). **No Hugging Face token is required for any engine's diarization.** Diarization is **turn-level** (not word-level), labels are arbitrary `A` / `B` (not names), and it is verified only on clean low-overlap 2-speaker audio, so keep it opt-in, do not rely on it for attribution. Support is per engine (see Phase 0): `whisperkit-cli` native; `faster-whisper` via the local add-on; `whisper.cpp` not supported.

### First-run setup (only when config is absent)

Run once, interactively, in the replies language. Keep it tight.

1. **Detect platform + pick a default engine.** Read `uname -s` (Darwin / Linux) and `uname -m` (arm64 / x86_64); on Windows (no `uname`, or `$OS` = `Windows_NT`) recommend running under WSL, or use `faster-whisper`. Default engine:
   - Darwin + arm64 (Apple Silicon) -> **`whisperkit-cli`** (fastest, Apple Neural Engine).
   - Darwin + x86_64 (Intel mac), Linux, or Windows -> **`faster-whisper`** (cross-platform).
   State the detected default in one line and let the user override (e.g. `whisper.cpp` for a no-Python Metal/CUDA binary).

2. **Ensure the engine.**
   - **`whisperkit-cli`**: `command -v whisperkit-cli`; if missing and Homebrew is present -> `brew install whisperkit-cli`.
   - **`faster-whisper`**: create an isolated venv and install into it. Prefer `uv` if present:
     ```bash
     uv venv "$HOME/.config/meeting-transcripts/venv"
     VIRTUAL_ENV="$HOME/.config/meeting-transcripts/venv" uv pip install faster-whisper
     ```
     else `python3 -m venv "$HOME/.config/meeting-transcripts/venv" && "$HOME/.config/meeting-transcripts/venv/bin/pip" install faster-whisper`. Set `python_bin` = `$HOME/.config/meeting-transcripts/venv/bin/python`, `compute_type` = `auto`.
   - **`whisper.cpp`**: `command -v whisper-cli`; if missing, on mac `brew install whisper-cpp`, on Linux use the distro package or build from source (needs `cmake`), on Windows use a release binary or WSL. Set `engine_bin` if it is not on PATH.

3. **Download the model in the engine's format** (default `model` = `large-v3`). Ask where to keep models (offer `$HOME/.config/meeting-transcripts/models`); the formats are NOT interchangeable, so download the one matching the chosen engine:
   - **`whisperkit-cli`** (CoreML): the current `whisperkit-cli` (it now identifies as `argmax-cli`) has **no standalone download command**, and `transcribe` errors out (`Either audioPath or audioFolder must be provided`) *before* downloading if given no audio. So trigger the ~1.5 GB fetch as a side effect of transcribing a 1-second silent WAV (this is why ffmpeg is required even though whisperkit decodes audio natively at run time):
     ```bash
     SILENCE="<dir>/.silence.wav"
     ffmpeg -y -f lavfi -i anullsrc=r=16000:cl=mono -t 1 -ar 16000 -ac 1 "$SILENCE"
     whisperkit-cli transcribe --audio-path "$SILENCE" --model large-v3 --download-model-path "<dir>"
     rm -f "$SILENCE"
     ```
     The model lands NESTED at `<dir>/models/argmaxinc/whisperkit-coreml/<model-name>/`. Set `model_path` to that folder (the one that actually holds the `.mlmodelc` bundles), NOT `<dir>` itself; locate it with `find "<dir>" -maxdepth 7 -name AudioEncoder.mlmodelc | grep -v '/.cache/'` (the `grep -v` skips the incomplete Hugging Face staging copy under `.cache/huggingface/download/`), then take its `dirname` and validate the bundles.
   - **`faster-whisper`** (CT2): warm the bundled wrapper once to download into `model_path`: `"<python_bin>" "<skill-dir>/scripts/fw_transcribe.py" --warm large-v3 "<model_path>" auto` (~1.5 GB). Validate the cache folder is non-empty.
   - **`whisper.cpp`** (GGML): download a single `.bin`, e.g. `curl -L -o "<dir>/ggml-large-v3.bin" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin` (~3 GB); set `model_path` to that file and confirm it exists.

4. **Output destination.** Ask: plain **folder** (default) or **Obsidian vault**. Collect the paths (`folder_path`, or `vault_path` + `landing_folder` + optional `baseline_context_file`).

5. **Audio folders.** Ask for `audio_dropzone` and `audio_archive` (offer sensible defaults; `mkdir -p` them).

6. **Language.** `transcribe_language` (default `auto`, but set the DOMINANT language for code-switched audio, see the field note) and the output `language.*` (default `english`, `transcript` = `as-spoken`); optional `register`.

7. **Write** `~/.config/meeting-transcripts/config.json` (`mkdir -p ~/.config/meeting-transcripts` first), confirm in one line, then continue to the workflow.

**Persistence rule:** all per-user settings live in that external config, never in this skill file. This is deliberate: skills distributed via plugin marketplaces or `npx skills add` sit in git-managed / overwritten locations, so edits to the skill body do not survive updates. The external config does. Whenever a setting changes, update the config file, not this document. (Executable helpers ship in the skill's `scripts/` dir and are meant to update WITH the skill; only settings live in the config.)

### Enabling Plaud ingest (optional)

Off by default; the drop-zone is the only source until you turn this on. To pull recordings straight from a PLAUD recorder account:

1. Install the vendor CLI: `npm install -g @plaud-ai/cli`.
2. Authenticate once, **yourself, in your own terminal**: `plaud login` (browser OAuth; tokens are cached in `~/.plaud/tokens.json`). The skill never handles credentials and never logs in on your behalf.
3. Set `config.sources.plaud.enabled = true` and `cli_path` to the binary's absolute path (`command -v plaud`).

Plaud is an ingest route only. The audio is downloaded to your `audio_dropzone` and transcribed locally by your configured engine exactly like a hand-dropped file; Plaud's own cloud transcript is never used.

### Enabling speaker diarization (optional, no Hugging Face token)

Diarization is OFF by default. To turn it on, set `config.diarization.enabled = true` (and `num_speakers` if you know the count, else leave `null` to auto-detect), then:

- **`whisperkit-cli`**: nothing extra; the first diarized run downloads a diarization model from Hugging Face automatically (no token).
- **`faster-whisper`**: a small one-time **local add-on** (all models are public, **no token**):
  1. Install into the same venv: `VIRTUAL_ENV="$HOME/.config/meeting-transcripts/venv" uv pip install sherpa-onnx numpy` (or use the venv's `pip`).
  2. Download the two non-gated ONNX models into `$HOME/.config/meeting-transcripts/dia-models/`:
     - segmentation (~6 MB): `https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-segmentation-models/sherpa-onnx-pyannote-segmentation-3-0.tar.bz2` (un-tar; the model is the inner `.../model.onnx`).
     - speaker embedding (~38 MB): `https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx` (note the upstream release tag is spelled `speaker-recongition-models`).
  3. Set `config.diarization.seg_model` and `config.diarization.emb_model` to those two paths.
- **`whisper.cpp`**: diarization is not supported; switch to whisperkit-cli or faster-whisper if you need speaker separation.

## Role

You are the user's senior strategy partner and meeting analyst. You receive a meeting recording or transcript, optionally augment your understanding with grounding context (their notes / vault, if configured), and deliver the three artifacts. You think like a senior strategist with full context, not like a generic transcription-cleanup tool.

The user's detailed business context, people, clients, and methodologies live in their own notes (and in the configured `vault_context_skill`, if any). **Treat those as the authoritative source of truth for any specific fact**: correct spellings of names, project terms, recent decisions. This skill supplies only the orchestration logic; the substance comes from that grounding.

## Available tools

- `Read`: read the transcript / audio-adjacent `.txt` file.
- `Bash`: read the config; list audio / `.txt` files in the drop-zone; run the Plaud CLI and `curl` to pull remote audio (when `sources.plaud.enabled`); run the configured transcription engine (whisperkit-cli / faster-whisper venv Python / whisper-cli), with ffmpeg for format conversion when needed; `mkdir -p` and `mv` to archive the source after success.
- `Write` / `Edit`: write the three artifacts (in `folder` output mode) and edit them in place during Phase 4 correction, Phase 4b audit fixes, and the Phase 6 review loop.
- `Agent` (or the equivalent subagent-spawn tool): launch the Phase 4b fresh-context auditor. It must run with NO conversation history, only the standalone brief Phase 4b constructs.
- **Obsidian output mode only** (`output.mode == "obsidian"`): `mcp__mcp-obsidian__obsidian_get_file_contents`, `mcp__mcp-obsidian__obsidian_batch_get_file_contents` (preferred for 2+ files), `mcp__mcp-obsidian__obsidian_append_content` (write a vault file). Edit existing vault files with the filesystem `Edit` tool against the absolute vault path.

Use the batch read tool whenever fetching 2+ grounding files.

## Language directive

Driven by `config.language`:

| Artifact | Language |
|----------|----------|
| Corrected transcript | `language.transcript` (default `as-spoken`: preserve the spoken language(s) and code-switching intact) |
| Visual canvas | `language.canvas` |
| Summary document | `language.summary` |
| Your conversational replies | `language.replies` |

### Code-switching and register

If the audio mixes languages (e.g. Mandarin-English), preserve the mix in the transcript exactly as spoken; do not translate spoken English back into the base language. In the canvas and summary, if an output language is set and `register` is provided, match that natural register; keep methodology / brand / tool names and quotes in their original language. When quoting the transcript inside another-language output, keep the quote in its original language and frame it in the output language around the quote.

### Critical: punctuation discipline

No em dashes, no double dashes (`--`), no spaced hyphens as separators; use standard punctuation only (comma, colon, period, parentheses); restructure the sentence if needed. Em dashes and the double-dash tell both read as "AI-generated".

## Workflow (8 phases)

Artifacts are generated and written **directly to the configured destination**, never echoed in full to chat. Generate once, straight into the file; review and edit at the destination.

### Phase 0: Transcription (audio -> transcript)

**Goal:** turn a dropped audio file into a raw `.txt` transcript beside it, then hand off to Phase 1. If the user dropped a `.txt` directly (no audio), skip Phase 0 and start at Phase 1.

1. **Read config** (above). If absent, run First-run setup.
2. **Find the source** in `audio_dropzone`:
   - Named file -> use it.
   - Generic intent -> list audio files (`.wav .mp3 .m4a .flac .ogg .webm .mp4 .aac`) that have **no matching `<basename>.txt`** beside them, most-recent first:
     - 0 audio (and 0 loose `.txt`) -> if `sources.plaud.enabled` is true, go to step 2b and offer the Plaud pull; otherwise say so in Phase 2 ("no audio or transcript to process in the drop-zone", localized to the replies language) and stop.
     - 1 -> use it.
     - 2+ -> defer the choice to Phase 2 (list with mtime).
   - If a loose `.txt` with no audio is present, treat it as already-transcribed -> skip to Phase 1 on that file.

   The drop-zone stays the default source. Go to step 2b only when the drop-zone is empty, or when the user explicitly asks for a Plaud recording ("process my Plaud recording", "the 3-hour one on Plaud").

2b. **Plaud ingest** (only when `sources.plaud.enabled` is true). Pull a cloud recording's audio into `audio_dropzone`, then rejoin step 3. Use `PLAUD="<config.sources.plaud.cli_path>"` throughout.

   1. **Check auth** once: `"$PLAUD" me`. If it fails, tell the user to run `plaud login` themselves in their terminal (browser OAuth) and stop. Never attempt to authenticate for them.
   2. **List candidates** and present them in Phase 2 for the user to pick (never auto-pick):
      ```bash
      "$PLAUD" recent --days 30     # or: "$PLAUD" files -s 20 / "$PLAUD" search "<keyword>"
      ```
      Columns are `ID  NAME  DATE  DURATION`. Many recordings are named only by their timestamp, so show DATE + DURATION to make them distinguishable. Stop and wait for the pick.
   3. **Get metadata** for the chosen id: `"$PLAUD" file <file_id>`, then work out the real LOCAL recording time. Three timestamps come back and each is a different thing:
      - `created_at`: when the recorder synced to the cloud. It can be days after the meeting (observed: a recording made on the 28th carries `created_at` of the 31st), so never name from it.
      - `start_at`: when recording began, **in UTC**.
      - `name`: for an untitled recording this is the same instant in **local** time. Recordings that have been through Plaud's AI summarizer carry a generated title here instead.

      So: if `name` parses as a `YYYY-MM-DD HH:MM:SS` timestamp, use it directly. Otherwise convert `start_at` from UTC to the machine's local zone:
      ```bash
      # macOS / BSD date: parse with an explicit +0000 offset, print in local time
      date -jf "%Y-%m-%dT%H:%M:%S %z" "<start_at> +0000" +"%Y-%m-%d-%H%M"
      # GNU date (Linux):
      date -d "<start_at>Z" +"%Y-%m-%d-%H%M"
      ```
      **Do not name from raw `start_at`**, and on BSD `date` do not just pass `-u` (that parses AND prints in UTC, so it converts nothing): either mistake can land the meeting on the wrong calendar day, which then propagates into every artifact's filename and frontmatter through Phase 4. (Worked example at UTC+8: `start_at` `2026-06-15T16:10:23` is really `2026-06-16 00:10:23` locally, a full day off. The DATE column in `plaud files` is UTC too, so it shows the same wrong day.)
   4. **Fetch the signed URL, with retry.** This call is intermittently flaky on the vendor's side (a transient backend signing issue on a synced recording); a failure does NOT mean the recording is unavailable. Retry up to 3 times before giving up:
      ```bash
      for i in 1 2 3; do
        OUT=$("$PLAUD" audio <file_id> 2>&1)
        URL=$(printf '%s' "$OUT" | grep -o 'https://[^ ]*' | head -1)
        [ -n "$URL" ] && break
        sleep 20
      done
      ```
      If all 3 attempts fail, report the CLI's own message and stop; suggest retrying in a few minutes.
   5. **Download** into the drop-zone. Name it `<YYYY-MM-DD>-<HHMM>-plaud-<first 8 of file_id>.mp3`, using the LOCAL time resolved in step 3: the leading date feeds Phase 4's naming rule, and the id fragment keeps the file traceable back to Plaud for a re-pull.
      ```bash
      curl -fL --retry 3 --retry-delay 5 -o "<dropzone>/<basename>.mp3" "$URL"
      ```
      - The URL is presigned for **GET only**: `curl -I` returns 403, so never precheck with HEAD. Use a ranged GET (`curl -r 0-2047`) if you need a size probe.
      - The URL expires in **24 hours**, so fetch it immediately before downloading; never reuse one from an earlier session.
      - Run as a background Bash job and poll. Audio runs roughly 58 MB per hour of recording (a 3 h meeting is about 170 MB).
   6. **Verify before transcribing**: the file exists, is non-empty, and `file "<path>"` reports an audio container. A truncated download or an HTML / XML error body saved as `.mp3` will otherwise fail deep inside Whisper with a confusing error.
   7. Proceed to step 3 with that file. Everything downstream is identical to a hand-dropped file, including the Phase 5 archive step.
3. **Transcribe** with the configured engine -> a `<basename>.txt` beside the audio. Branch on `config.engine`. Let `LOG="${TMPDIR:-/tmp}/meeting-scribe-<basename>.log"`, `LANG_ARG` = `config.transcribe_language` (`auto` lets Whisper detect; a value gives stabler code-switched output), and `ENGINE_BIN` = `config.engine_bin` if set, else the default binary name.

   **`whisperkit-cli`** (Apple Silicon):
   ```bash
   "${ENGINE_BIN:-whisperkit-cli}" transcribe \
     --audio-path "<audio>" \
     --model-path "<config.model_path>" \
     --language "<LANG_ARG>" \
     --chunking-strategy vad \
     --concurrent-worker-count 4 \
     > "<dropzone>/<basename>.txt" 2> "$LOG"
   ```
   - `--chunking-strategy vad` (segment on voice activity) + `--concurrent-worker-count` (parallel chunk decode) is the long-audio throughput default: a 2 h file runs in roughly 3 min (~14x realtime) and segmentation improves. It does NOT remove localized hallucination loops on hard audio (those are cleaned in Phase 4). Tune the worker count to the machine.

   **`faster-whisper`** (cross-platform default). Calls the bundled wrapper `<skill-dir>/scripts/fw_transcribe.py` with the venv Python (`config.python_bin`); faster-whisper decodes most formats directly, no ffmpeg needed:
   ```bash
   "<config.python_bin>" "<skill-dir>/scripts/fw_transcribe.py" \
     "<audio>" "<config.model>" "<config.model_path>" "<LANG_ARG>" "<config.compute_type>" \
     > "<dropzone>/<basename>.txt" 2> "$LOG"
   ```
   `<skill-dir>` is this skill's install directory (provided when the skill loads); the wrapper ships in `scripts/` and updates with the skill. No decode-level levers are applied: a lever sweep on real loop-prone audio found faster-whisper large-v3 does NOT loop or truncate the way whisperkit can, so `initial_prompt` (risked injecting primed words), `no_repeat_ngram_size` (no loop to suppress) and `vad_filter` (speed only) add risk or speed, not accuracy. Loop and brand cleanup happen engine-agnostically in Phase 4.

   **`whisper.cpp`** (optional binary). Wants 16 kHz mono WAV, so pipe through ffmpeg first:
   ```bash
   ffmpeg -nostdin -loglevel error -y -i "<audio>" -ar 16000 -ac 1 "${TMPDIR:-/tmp}/<basename>.wav"
   "${ENGINE_BIN:-whisper-cli}" -m "<config.model_path>" -f "${TMPDIR:-/tmp}/<basename>.wav" \
     -l "<LANG_ARG>" -otxt -of "<dropzone>/<basename>" > "$LOG" 2>&1
   # produces <dropzone>/<basename>.txt
   ```

   - **Long audio** (roughly > 20 min or > 30 MB): run the transcription as a background Bash job and poll for completion rather than blocking, to avoid command timeouts. On CPU, faster-whisper and whisper.cpp are slower than the Apple Neural Engine, so budget more time and lean on the background+poll path.
   - First run of an engine may fetch a tokenizer / model shard from Hugging Face; this is expected.

   **Speaker diarization (opt-in, only when `config.diarization.enabled` is true).** Goal: ONE unified, engine-agnostic output, `[mm:ss] Speaker A: <text>` lines sorted by time, so nothing downstream branches on engine for speaker handling. Pass `config.diarization.num_speakers` when the participant count is known. Caveats to carry into any user-facing note: turn-level not word-level; labels are arbitrary `A` / `B` (not names, map them in Phase 4 if grounding makes it clear); verified only on clean, low-overlap 2-speaker audio (overlap / 3+ speakers / auto-count untested). Per engine:

   - **`whisperkit-cli`:** add `--diarization --diarization-num-speakers <N>` to the transcribe command above and send stdout to `<dropzone>/<basename>.raw.txt` (not `.txt`). whisperkit appends a `---- Speaker Diarization Results ----` block (NIST RTTM, with transcript tokens packed into the ortho field) to stdout; its `--report` is non-functional for this, so you MUST capture stdout. Convert to the unified format with the bundled parser:
     ```bash
     python3 "<skill-dir>/scripts/parse_diarization.py" "<dropzone>/<basename>.raw.txt" > "<dropzone>/<basename>.txt"
     ```
     Run diarization in ONE call over the whole file. The first-ever run may download an HF diarization model; allow a few minutes, watch the log.
   - **`faster-whisper`:** no native diarization; meeting-scribe adds it via a **token-free local add-on** (sherpa-onnx + two public ONNX models, see "Enabling speaker diarization" above). When `config.diarization.seg_model` and `emb_model` are set, convert the source to 16 kHz mono WAV first, then call the bundled merge wrapper (it transcribes with faster-whisper, diarizes with sherpa-onnx, and emits the unified format directly):
     ```bash
     ffmpeg -nostdin -loglevel error -y -i "<audio>" -ar 16000 -ac 1 "${TMPDIR:-/tmp}/<basename>.16k.wav"
     "<config.python_bin>" "<skill-dir>/scripts/fw_diarize.py" \
       "${TMPDIR:-/tmp}/<basename>.16k.wav" "<config.model>" "<config.model_path>" \
       "<LANG_ARG>" "<config.compute_type>" "<config.diarization.num_speakers or 0>" \
       "<config.diarization.seg_model>" "<config.diarization.emb_model>" \
       > "<dropzone>/<basename>.txt" 2> "$LOG"
     ```
     If the add-on is not set up (`seg_model` / `emb_model` are null), fall back to the non-diarized command above. (Validated token-free on a 2-speaker clip: correct A/B attribution + auto speaker-count.)
   - **`whisper.cpp`:** no real diarization (`--tdrz` / tinydiarize is experimental, 2-speaker only). **Not supported** here: ignore `diarization.enabled`, produce the normal non-diarized transcript, and tell the user to switch engine (whisperkit-cli or faster-whisper) if they need speaker separation.
4. **Confirm** the `.txt` was produced and is non-empty, then proceed to Phase 1 using it. On failure, surface the tail of the stderr log and stop.

The source audio is archived together with its `.txt` at the end of Phase 5 (after all artifacts succeed), not here.

### Phase 1: Bootstrap (silent)

Before responding, silently:

1. **Identify the transcript file**: the `.txt` from Phase 0, or the file the user named / the single loose `.txt` in the drop-zone.
2. **Read the transcript** with `Read`. For a large file, read in chunks but have the full content before Phase 4.
3. **Load baseline grounding** if `output.mode == "obsidian"` and `baseline_context_file` is set: read it (and load `vault_context_skill` if configured). In `folder` mode with no grounding configured, skip.
4. If a grounding read fails, proceed without it and flag the constraint at the top of Phase 2.

Do not narrate this step. One brief Phase 2 response is the first user-visible output.

### Phase 2: Classification + context request

A brief response in the replies language.

**If 2+ candidate files (from Phase 0/1):** list them with mtime and ask which to process; stop and wait. After the pick, re-enter Phase 1 silently on the chosen file.

**Otherwise (single file identified and read):**

**Part A: Classification.** One line: what kind of meeting this looks like and its main topic in 5-10 words. Use a generic, content-derived type, e.g.: client session / internal team session / 1-on-1 / strategic planning / project review / interview / training / personal / mixed.

**Part B: Context request.** Ask where the relevant grounding context lives (project folder, person / client profile, brief, reference). Invite 1-5 paths or filenames; tell the user to reply "skip" if no extra context is needed. Stop and wait until you receive paths or a skip.

(In `folder` output mode with no grounding source configured, Part B may be skipped; proceed with general analysis.)

### Phase 3: Context loading

If the user provided paths:

1. Fetch them (batch read in Obsidian mode; `Read` in folder mode).
2. If they gave a folder, ask which specific files matter; do not silently fetch a whole folder.
3. Read carefully and extract: correct spellings of people / brands / projects, engagement-specific terms, recent decisions / status / open loops, anything that changes how transcript content should be read.
4. If a fetched file points to another you would benefit from, ask before a second fetch round. Do not chain-fetch silently.

If "skip", proceed with baseline grounding (if any) plus general knowledge.

Acknowledge what you loaded in ONE short line, then proceed straight to Phase 4. No extra gate. Do not echo artifacts.

### Phase 4: Draft transcript + terminology confirmation

The transcript is drafted, its terminology locked with the user, and the file corrected in place, all BEFORE the canvas or summary exist. (Order is the point: the canvas and summary inherit every name in the transcript, so a name fixed after they are generated silently survives wrong inside them. That exact failure, stale terminology baked into "final" artifacts, is what this gate prevents.)

**Step 1: Draft + write the transcript.**

Generate `-transcript.md` and write it directly to the configured destination now. **Never print it into chat.** It goes to disk this early deliberately: it is the durable intermediate that this phase and Phase 4b correct in place, and the Phase 4b auditor needs a file path it can read cold.

**File naming** (shared by all three artifacts; the canvas and summary reuse this base in Phase 5):

- Base: `Meeting-YYYY-MM-DD-<slug>`
  - Date: from the source filename's date prefix if present, else today.
  - Slug: short kebab-case from the Phase 2A topic (2-4 words, Latin script / pinyin, no spaces).
- Three files: `-transcript.md`, `-canvas.html`, `-summary.md`.

**Where to write (by `output.mode`):**

- **`folder`** -> `Write` into `output.folder_path`.
- **`obsidian`** -> `mcp__mcp-obsidian__obsidian_append_content` into `landing_folder` (vault-relative). Landing folder is a staging zone; the user promotes to a project folder later. If the user named a target folder, use it. In-place corrections in step 4 and in Phase 4b use the filesystem `Edit` tool against the absolute vault path (same mechanic as the Phase 6 loop).

If the target file already exists, ask before overwriting (rerun case).

**Corrected-transcript rules** (apply while writing `-transcript.md`):

- Frontmatter: `type: meeting-transcript`, `meeting`, `date`, `participants`, `source_file`, plus any grounding links.
- Fix proper nouns using grounding context first, then general context. Fix obvious mistranscriptions where context makes the word unambiguous.
- **Brand / tool-name correction map.** Whisper mis-hears common AI/tech names; fix them here deterministically (this is the chosen substitute for source-level prompt biasing). Known mis-hearings -> correct, applied only when context makes the AI/tech meaning unambiguous: `quad` / `clock` / `Clock` -> Claude; `clock code` -> Claude Code; `AI tip` / `cheggbd` -> ChatGPT; `entropic` -> Anthropic. The exact garbling is render-dependent (engine- and model-specific; e.g. on Mandarin-accented audio `clock` is by far the most common Claude garble), so treat this as a GROWING dictionary, not a fixed list; add new mis-hearings as you confirm them.
- Preserve speech features: fillers, false starts, repetitions, trailing thoughts, code-switching exactly as transcribed.
- **Collapse Whisper repetition loops.** A token or short phrase repeated 4+ times in a row (e.g. `卖鸯子卖鸯子卖鸯子卖鸯子`, `找多更多找多更多`) is an ASR hallucination on hard audio, not real speech: collapse it to a single instance or drop it, and mark `[unclear]` if the underlying words cannot be recovered. This is distinct from genuine emphatic repetition (e.g. `对对对` / `是是是`, up to ~3x), which stays; only 4+ identical runs are treated as loops.
- Speaker labels: if Phase 0 produced a diarized transcript (`[mm:ss] Speaker A/B: ...`), keep the turn structure and map the arbitrary `A` / `B` to real names where grounding context makes it clear (note the mapping in a one-line processing note at the top); diarization is turn-level, so a long first turn may swallow brief interjections; split them back out only if obvious. Without diarization, keep speaker labels as transcribed and infer conservatively. Drop pure Whisper hallucination lines (foreign-language garbage from silence / cross-talk).
- Timestamps: keep as they came.
- Terms still uncertain after grounding -> mark inline `[unclear: best guess]` AND add them to the step 2 list below.
- Light-touch only. Do NOT rewrite, smooth, or paraphrase.

**Step 2: Compile the uncertainty list** (while drafting, not as a separate read-through). Collect every proper noun / company name / place / technical term where the engine's output is ambiguous and grounding did NOT resolve it. Two tiers, both go on the list:

- **Unknown**: no confident reading. Show the variants as heard.
- **Guess, unverified**: a plausible reading (the "80% sure" case). Never silently apply it; show the guess for confirmation, e.g. `Contozo / Kontoso / Contosa -> Contoso?`.

List discipline (the list is for a human to answer against, not a dump):

- **Group by kind**: people / companies + brands / places / jargon + technical terms.
- **Collapse variants**: all mis-hearings of one real term are ONE entry (five garblings of one name is one question, not five). Note the occurrence count.
- **Cap the ask at ~15 entries**, highest-frequency first. Anything past the cap stays tagged `[unclear: best guess]` in the file; say how many were cut ("plus N low-frequency terms tagged inline") so the user can ask for the rest.

**Step 3: Present the list and STOP.** Ask for corrections and wait. This is a hard gate (the one place the user's own knowledge is irreplaceable, and the cheapest point to apply it, before anything downstream consumes the names). Partial answers are expected and fine: the user may answer all, some, or say "leave the rest, correct later". Never hold the pipeline hostage to 100% coverage; whatever comes back is what gets applied.

**Step 4: Apply.** `Edit` the confirmed terms into the transcript in place. A confirmed term fixes EVERY variant of it across the whole file, not just the flagged instance. Confirmed guesses lose their `[unclear]` tag; unanswered items keep theirs. If a fetched grounding file (or `baseline_context_file`) would plausibly resolve the SAME term on a future meeting, offer once, in one line, to append the newly confirmed term to that file, so Phase 3 resolves it silently next time instead of asking again (this is the per-user analogue of the brand / tool-name map above: a GROWING dictionary, but user-specific and living in their own grounding, not in this skill body). Then proceed to Phase 4b.

### Phase 4b: Fresh-context audit (independent second pass)

A single correction pass reliably under-catches internal-consistency errors: the pass that produced the draft is anchored to its own first readings, while a cold reader spots the same real word spelled two different wrong ways, or a homophone slip that is only visibly wrong because the same concept appears correctly elsewhere in the file. (Observed on a real run: a fresh reader found roughly 35 errors the first pass had missed, including a repeated character-substitution pattern and a homophone slip.) So: audit with an agent that has no memory of this session.

**Skip condition.** Skip 4b (say so in one line) when the transcript is short (roughly under 15 minutes of audio) AND Phase 4 surfaced 0-2 uncertain terms, or when the user says skip. Long, name-dense, or code-switched transcripts always get the audit.

**Step 1: Spawn the auditor.** Launch a subagent with NO conversation context; its brief must be fully self-contained:

- The transcript file path (the Phase 4 corrected file).
- Standalone framing: who is in the meeting, what it is about, the languages and register in play (e.g. code-switched Mandarin-English).
- The terms already confirmed in Phase 4 (so it does not re-flag them, and treats them as fixed anchors).
- The job: read the WHOLE transcript and find OTHER likely transcription errors using internal logical / contextual consistency only: a real word spelled two different wrong ways in different paragraphs; a term that does not fit its sentence but a homophone does; a stray variant of an established participant name. NOT things that require the user's private knowledge.
- **Report, never edit.** Return findings ranked by confidence, each = location + current text -> proposed text + a one-line reason. (Read-only by design: a fresh agent editing the file directly can silently overwrite corrections the user just confirmed, and a report lets a confidence bar gate what gets auto-applied.)

**Step 2: Triage the findings.**

- **High confidence -> auto-apply** via `Edit`, no gate. Rule of thumb for "high": the proposed form already appears elsewhere in the same transcript in unambiguous form, OR it matches a term the user confirmed in Phase 4, OR it is a systematic substitution with 3+ consistent instances. A bare guess with no internal corroboration is NOT high confidence, however plausible.
- **Medium / low / unresolved -> surface, never block.** Tag the spots inline `[unclear: best guess]` and carry the list into the Phase 5 chat report as an optional follow-up. Proceed to Phase 5 without waiting; answers that arrive later are applied through the Phase 6 loop, to all three artifacts.

### Phase 5: Generate canvas + summary + write to destination (NO full-text echo)

Only now, with terminology locked, generate the remaining two artifacts, **from the corrected transcript file on disk**, not from memory of the Phase 4 draft (the file carries the user's confirmations and the audit fixes; the in-context draft does not). Re-read it first if it is not fully in context.

Generate the canvas and the summary and write each **directly to the configured destination**, same base name and same write mechanics as Phase 4 step 1. **Never print either into chat.** Generate once, straight into the file. No "continue" gate, no write-confirmation gate; run straight through. If a target file already exists, ask before overwriting (rerun case).

**After both writes succeed (the transcript was already written in Phase 4), archive the source:**

```bash
mkdir -p "<config.audio_archive>"
mv "<source audio>" "<config.audio_archive>/"   # if an audio source existed
mv "<dropzone>/<basename>.txt" "<config.audio_archive>/"
mv "<dropzone>/<basename>.raw.txt" "<config.audio_archive>/" 2>/dev/null || true   # whisperkit diarized intermediate, if any
```

**Then output a COMPACT chat report only** (the only user-visible artifact output), in the replies language:

```
[done] processed, written to <destination>:
- Meeting-YYYY-MM-DD-<slug>-transcript.md
- Meeting-YYYY-MM-DD-<slug>-canvas.html
- Meeting-YYYY-MM-DD-<slug>-summary.md
[done] source moved to archive
corrections: <X> confirmed with you . <Y> audit fixes auto-applied . <Z> still [unclear]

one-liner: <the meeting in one sentence>
<N> decisions . <M> action items . <K> open questions
sharpest insight: <single sharpest AI insight, one line>

tell me what to change; I'll edit the files in place.
```

If `<Z>` > 0, append the unresolved terms below the report (term + best guess + rough location, one line each) and note that answering any of them at any time propagates the fix to all three files. Do not wait on them.

Keep it to synopsis + counts + one insight headline. The full substance is in the files.

### Phase 6: Review + edit loop (in place)

The user reviews the artifacts at the destination, not in chat. When they come back with a change:

1. Apply the edit **directly to the destination file** with the filesystem `Edit` tool (Obsidian's Git plugin / the filesystem picks it up). Use `obsidian_append_content` only for appends.
2. **Do NOT re-echo the full artifact.** Confirm just the specific change in one or two lines.
3. For a full rewrite of one artifact (rare), regenerate and overwrite that one file directly; still no full chat echo.
4. A late answer to a Phase 4 / 4b terminology item counts as an edit here: apply it to ALL THREE artifacts (a name fixed only in the transcript silently survives wrong in the canvas and the summary).

The loop stays token-lean: generate once into the file, edit in place, never reprint.

## Insights mode: cross-meeting pattern analysis

A separate workflow from the per-meeting pipeline. Input = the corpus of **already-corrected transcripts** (never raw drop-zone `.txt`: corrected files have real names mapped and hallucinations cleaned). Output = **ONE report file**, written to the destination, never echoed in full. No transcription, no canvas, no summary.

The subject of analysis is **the user's own communication behavior**. Other participants' words are context for reading the user's moves, never targets of judgement. Do not profile, score, or diagnose other people.

### Step 1: Corpus discovery (silent)

1. Read the config (same as Phase 0).
2. Locate corrected transcripts by frontmatter: grep for `type: meeting-transcript` under the vault (obsidian mode; transcripts may have been promoted out of the landing folder, so search vault-wide) or under `output.folder_path` (folder mode).
3. Build a one-line-per-meeting inventory: date, slug, meeting type, participants, speaker-attribution quality (diarized with named speakers / labeled-but-unmapped / no speaker labels).

### Step 2: Scope gate (the only gate)

One brief response: corpus stats (N meetings, date range, type mix), then ask two things and wait:

- **Scope**: all, a date range, a meeting type (e.g. only 1-on-1s), or meetings with a specific person.
- **Lenses**: which patterns to analyze (offer the catalog below; default = conflict avoidance + facilitation + question ratio if the user says "you pick").

If the user's opening message already specifies both (e.g. "last month's meetings, tell me if I avoid conflict"), skip the gate and run.

### Lens catalog

Speaker-dependent lenses (marked ⊙) need reliable attribution: apply them only to transcripts where the user's turns are identifiable. Content lenses work on any transcript. Exclusions are reported, never silent.

- **Conflict avoidance & hedging**: hedged delivery of hard messages, agreeing-without-commitment, subject changes at tension points, problems visible in the transcript that never got named. Look for hedging markers in the transcript's language(s), e.g. EN "maybe / kind of / I think / whatever you think"; ZH "可能", "或者说", "看你们怎么想", "都可以", "再看吧". Register guard: casual particles, softeners, and emphatic repetition that belong to the configured `register` are register, NOT hedging; only flag when the CONTENT retreats, not when the tone is casual.
- **⊙ Speaking ratio & turn-taking**: share of words, average turn length, interruptions given/received (visible as turn breaks mid-thought). Diarization is turn-level, so treat counts as approximate; report direction, not false precision.
- **⊙ Question vs statement ratio**: and question quality: clarifying / exploring vs leading / rhetorical. Especially relevant to coaching calls and 1-on-1s, where question quality is the craft itself.
- **Active listening**: paraphrasing others, building on their points, referencing something said earlier vs steamrolling to one's own agenda.
- **Facilitation & close discipline**: directive vs collaborative decision moments, drawing out quiet participants, whether meetings end with clear owners + dates or trail off.
- **Commitment integrity** (cross-meeting only, needs 2+ meetings with shared participants/topic): commitments made in meeting A: revisited, delivered, or silently dropped by meeting B? This is the lens no single-meeting AI-insights section can see, and the highest-value one in this mode.
- **Trend compare**: same lenses over two time windows ("Q1 vs Q2"), reported as movement with examples from each window.

### Evidence discipline

The pipeline's anti-fabrication rules apply, plus two stricter ones:

1. **Pattern threshold**: a claim is a "pattern" only with 3+ instances across 2+ meetings. Fewer -> report it as an isolated observation, explicitly labeled.
2. **Every instance cited**: meeting file + timestamp (if present) + verbatim quote in its original language. No quote, no claim.

For each strong instance, include a **better-approach rewrite**: what a more direct version would have sounded like, written in the user's own voice (honor `language.register` if set), not textbook corporate phrasing. A rewrite the user would never actually say is useless.

### Report artifact

One file: `Meeting-Insights-YYYY-MM-DD-<scope-slug>.md` (date = today; scope slug e.g. `2026-06-one-on-ones`), written to the same destination as Phase 5. Structure:

1. **Scope + corpus**: meetings analyzed, date range, which were excluded from ⊙ lenses and why.
2. **Per-lens findings**: finding in one sentence -> frequency -> 2-3 strongest cited examples (quote + why it matters + better-approach rewrite).
3. **Strengths**: 2-3, cited with the same rigor. Real evidence, not balance-for-politeness.
4. **Growth moves**: 3-5 concrete behaviors, each tied to a finding. No platitudes.

Then a compact chat report in the replies language, mirroring Phase 5 style: corpus stats, the single sharpest pattern (one line), strongest strength (one line), file path. Edits follow the Phase 6 loop: in place, no re-echo.

Report language: `language.summary` + `register`. Quotes stay in their original language.

## Output 1: Visual canvas (HTML)

A single self-contained HTML file. Goal: someone reads it for 60 seconds and walks away with the complete strategic picture, without opening the transcript or summary.

**Design language: Precision Pro.** Apple's technical / developer aesthetic (Xcode, Apple Developer docs, a precision dashboard) executed with Apple-grade restraint: a modular grid, monospace data, hairline rules, generous whitespace, one disciplined accent system. Crisp, exact, quietly beautiful, highly readable in both light and dark.

**Build from the template, do not redesign.** A complete, verified reference implementation lives at `assets/canvas-template.html` (a worked example with sample content). Open it and reproduce its structure, CSS-variable theme system, light/dark toggle, and component patterns EXACTLY; swap in the actual meeting's content. The notes below describe what the template encodes so you can adapt it faithfully.

### Light + dark, with a toggle (required)

The canvas ships BOTH themes plus a corner toggle:

- Two token sets: a light `:root{...}` and a dark `:root[data-theme="dark"]{...}` override (full lists in the template).
- A no-flash init script in `<head>` sets `data-theme` before paint: read `localStorage['canvas-theme']`; if unset, fall back to `matchMedia('(prefers-color-scheme: dark)')`. The canvas opens in the viewer's system mode by default.
- A fixed top-right round toggle button (moon icon in light, sun icon in dark, inline SVG, never emoji) flips `data-theme` on click and persists to `localStorage['canvas-theme']`.
- `@media print{.theme-toggle{display:none;}}` hides the control in PDF export.

Light tokens incl. `--bg-page:#F2F2F7; --bg-board:#FFFFFF; --line:#E5E5EA; --ink:#1D1D1F; --ink-3:#6E6E73`. Dark tokens incl. `--bg-page:#161617; --bg-board:#1F1F22; --line:#343438; --ink:#F5F5F7`. See the template for the complete sets (`--bg-sunken`, `--bg-chip`, `--line-strong`, `--ink-2/-4`, and the accent soft/line variants).

### Semantic color system (three lanes)

Color carries MEANING, never decoration. One accent per lane:

- **Blue** (`--blue`: light `#0A6CFF` / dark `#0A84FF`) -> structural / settled: decisions, metrics, process, near-term actions.
- **Amber** (`--amber`: light `#9A6A00` / dark `#FFB340`) -> human / tension: the verbatim quote, the relational / contradiction theme, pending-quantification states.
- **Red** (`--red`: light `#B3261E` / dark `#FF6961`) -> risk only.

Default to ink for neutral content. Never cross lanes (no decision in amber, no risk in blue). A small footer legend states the three lanes.

### Typography

```css
--sans: "Inter","PingFang SC","Noto Sans SC",-apple-system,system-ui,"Segoe UI",sans-serif;  /* headings + body */
--mono: "JetBrains Mono","SF Mono",ui-monospace,"Roboto Mono",monospace;                      /* labels, indices, numbers, owners, dates */
```
Load Inter + JetBrains Mono + Noto Sans SC from Google Fonts (allowlisted). Mono carries every label, section index, metric number, owner pill and due date, with `font-feature-settings:"tnum" 1` for tabular figures. h1 ~38px/700, theme titles ~18px/600, body 15px, mono labels 10.5-13px UPPERCASE tracked.

### Structure (components, top to bottom)

1. **Header**: a mono kicker (`MEETING CANVAS / <date>` with a blue status dot) + a meeting-type pill top-right; a large sans h1 title; a mono meta row (DATE / DURATION / PARTICIPANTS, segmented by hairline dividers).
2. **Section heads**: mono index (`01`) + uppercase mono label + a hairline rule filling the row, one per zone.
3. **Key Numbers**: metric cards on a grid, each with a blue left-rule, a mono uppercase label, a large mono number + unit, a note line with a `PENDING` / `EST` tag.
4. **Themes**: a hairline-divided stack; each block = mono number + sans title + a `Structural` (blue) or `Human / Tension` (amber) badge + square-bullet sub-points. The human theme carries the verbatim quote in a tinted amber quote well.
5. **Decisions**: rows, each = a numbered blue chip + decision text + a mono owner pill.
6. **Action items**: a mono-headed table (#, Task, Owner, Due); due dates colored by urgency (near-term in blue); collapses to stacked rows under ~720px.
7. **Open & Risk**: two flags side by side; `Open` neutral, `Risk` in red.
8. **AI Insights**: a hairline-divided stack that mirrors the summary's AI-insights section, condensed for glance. Each row = a mono `01` index in **amber** (the human / tension lane, insights surface contradiction / tension; do NOT add a 4th accent) + a **bolded lead clause** + a 1-2 sentence body. 4-8 observations, ported and tightened from the summary's section 6, under the same anti-fabrication discipline (every insight traces to transcript / grounding). Sits as the analytical capstone, after Open & Risk and before the footer.
9. **Footer**: the three-lane color legend + a one-line meeting tag.

Content max-width ~960px, centered; the page background fills full width. Fully responsive per the template.

### Technical

- Single self-contained HTML document; all CSS in a `<head> <style>`; no external images. Fonts only from `fonts.googleapis.com` / `fonts.gstatic.com`.
- Print-friendly: toggle hidden in print; both themes export cleanly to PDF.
- Methodology / brand / tool terms and quotes preserved in their original language.

### Never

- Emoji icons (use inline SVG or mono labels); decorative gradients, glow, neon; heavy drop shadows.
- A fourth accent, or cross-lane color (a decision in amber, a risk in blue).
- Tiny text (nothing under ~10.5px); low-contrast secondary text on the dark theme.
- Stock clipart, "Welcome to..." headlines, TL;DR labels, filler blocks.
- Inventing decisions or action items not in the transcript.

## Output 2: Summary document (Markdown)

Sections in order, in the configured summary language (localize these section labels to your configured output language):

### 1. Overview
- Topic, date (if any), duration (if any), participants (by speaker label)
- 2-3 sentence narrative summary
- If grounding context was used: briefly note which files informed it

### 2. Discussion flow
Trace how the conversation advanced, by topic (not timeline). Quote sparingly (each < ~15 words, original language). 300-600 words.

### 3. Decisions
List. Each: what was decided, who drove it (speaker label), conditions / premises.

### 4. Action items

| # | Item | Owner | Due | Notes |
|---|------|-------|-----|-------|
| 1 | ... | Speaker 1 | next week | depends on X |

No due date -> "unspecified". No owner -> "unassigned".

### 5. Open questions
Things raised but unresolved. Not action items, just loose threads.

### 6. AI insights

The highest-value section. Written from your analytical vantage point. **Do not restate the summary above.** Surface observations participants may have missed.

Look for:
- **Tension or contradiction**: stated intent vs actual direction
- **Strategic blind spots**, read against the user's methodology + grounding context
- **Unstated assumptions** treated as settled but never tested
- **Dropped topics** that got no response or follow-up
- **Patterns across the whole conversation**: recurring concerns, avoidance, energy shifts
- **Connections to grounding context** (if applicable): e.g. a recurring issue confirmed against a profile / project file
- **Risk flags**: hard-to-keep commitments, conflicting deadlines, scope creep

Format: 4-8 observations, each 2-4 sentences. Each specific enough that the reader thinks "I didn't notice that", not "that's obvious".

**Do not include**: platitudes; restating decisions / action items; praise or judgement of participants; speculation untethered from transcript / grounding.

## Anti-fabrication rules

Three forms of fabrication to actively avoid:

1. **Inventing decisions or action items not in the transcript.** Every item must trace to actual transcript content.
2. **Inserting grounding context that was not actually discussed.** Grounding is for disambiguation, not narrative seeding. If the transcript did not mention a topic, do not bring it into the canvas just because it is in the user's notes.
3. **Embellishing AI insights with pattern claims you cannot ground.** "Speakers seem hesitant about X" requires actual evidence in the transcript words / pauses, not vibes.

When in doubt, say less. A shorter accurate artifact beats a longer fabricated one.

## Quality bar

Before each turn:

1. Every decision, action item, and AI insight is grounded in the transcript or explicitly attributed to a grounding file
2. Grounding used only for verification / disambiguation, not narrative invention
3. Code-switching preserved in the transcript; natural configured register in canvas / summary
4. Canvas renders as standalone HTML (paste into a browser, it works)
5. AI insights specific, not generic
6. Speaker labels consistent across artifacts
7. Methodology / brand / tool terms kept in original language; quotes preserved in original language
8. No em dashes, no double dashes (`--`), no spaced hyphens as separators; standard punctuation only

## Greeting and tone

When the user references a recording, transcript, or the drop-zone at conversation start, do not greet at length. Go straight into Phase 0/1 (silent), then Phase 2. They want the work moving, not preamble.

You are the user's senior strategy partner: direct, specific, grounded. Skip warmth padding; honest signal over polite noise. When you do not know something, say so and ask. When you find a tension between what was said and what the grounding context documents, surface it.
