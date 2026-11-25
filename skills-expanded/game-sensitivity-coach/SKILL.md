---
name: game-sensitivity-coach
description: Discover a gamer's mouse settings, transfer sensitivity between games, and refine aim from passive gameplay video and mouse logs. Use for mouse sensitivity calibration, scoped or ADS tuning, cm/360 conversion, or applying and restoring game sensitivity settings. The agent handles settings discovery, image review, and evidence logging; the gamer plays normally.
metadata:
  version: "1.0.0"
  runtime: "Python 3.8+; FFmpeg; Windows desktop for bundled live capture; image-capable host agent for visual analysis"
---

# Game Sensitivity Coach

Deliver a concrete setting recommendation supported by the gamer's actual settings and gameplay. Handle discovery, capture, shot selection, visual tracking, calculations, and reports yourself. Do not ask the gamer to fill forms, label shots, mark targets, or calculate conversions.

Resolve script paths relative to this SKILL.md, regardless of the working directory. This folder is self-contained. The scripts capture and organize evidence; **the host agent performs image analysis**. Do not describe a pending report as already analyzed or imply that a background AI service exists.

## Choose the work

| User intent | Workflow and reference |
|---|---|
| Find or understand current sensitivity | Discover the active settings and their units; [settings-discovery.md](references/settings-discovery.md). |
| Carry a familiar setup into another game | Discover both games, choose a matching metric, calculate a conditional conversion; [conversion.md](references/conversion.md). |
| Fix overshoot, undershoot, tracking, or scoped aim | Discover current settings, capture ordinary play, inspect images and raw input, propose a measured next step; [observation.md](references/observation.md). |
| Apply, compare, or restore settings | Prepare an exact patch, use existing authorization or obtain approval of that patch, back up, apply, read back, and compare; [apply-and-rollback.md](references/apply-and-rollback.md). |

Read [game-examples.md](references/game-examples.md) for THE FINALS, Battlefield 6, and Holdfast examples, and [data-contracts.md](references/data-contracts.md) when authoring profiles, assessments, or iteration logs. Examples explain methods, not universal defaults.

## Establish context without forms

Infer the game, install path, profile, requested capture duration, and current authorization from the conversation and available local evidence. Start read-only discovery immediately. Game settings often live in a per-user directory rather than the install folder. Use `scripts/discover_settings.py`, focused filesystem searches, documented config keys, or a visible settings screen. Confirm which profile is active; file recency alone is insufficient.

Record each setting's native value, display unit, config representation, source, and observation date. Separate look, normal zoom, scoped zoom, per-optic multipliers, FOV, acceleration/raw-input options, and aim mode. Preserve unknown values as null. Do not copy another person's DPI or reuse old session values as verified current settings. A corrected user report supersedes an assumption in derived context; preserve original capture metadata and hashes.

DPI generally cannot be recovered from raw mouse deltas. Use available mouse-software evidence; otherwise keep it unknown and proceed with relative sensitivity analysis. Ask one focused question only if an essential fact cannot be discovered and actually prevents the requested result. A cloud-only agent cannot access an unrelated local monitor: use an existing session bundle or an explicitly available local execution connection.

## Observe and recommend

When gameplay capture is requested, start a bounded passive recording on the gaming computer. Prefer a duration stated by the user; otherwise announce a reasonable short baseline, such as 3–5 minutes. The bundled recorder uses standard Windows screen capture and mouse Raw Input. It does not read process memory, inject input, hook rendering, or automate aim. Settings-file inspection is a separate, authorized operation.

Use the capture CLI and monitor its reported state. Foreground loss pauses capture; elapsed capture coverage differs from video playback length. Extend an existing capture through its bounded control file when the user changes the duration, rather than running concurrent recorders. Honor stop requests promptly, finalize logs, and report meaningful capture failures. Do not silently keep recording beyond the agreed interval.

After capture, generate the review and exported frames. The default export samples only six click candidates and 12 overview frames; it does not screen every candidate. Explicitly select all candidate IDs or their full count before claiming full candidate screening, then inspect consecutive actual frames around useful acquisitions. Record any incomplete screening coverage. Sample other combat intervals too: automatic fire can generate several shots from one press. Inspect target-to-crosshair motion, scope transitions, visible discharge, recoil, target/player movement, occlusion, and correction timing. Keep exclusions and ambiguous examples. Mouse reversal counts alone are not overshoot; right-button state is not proof of ADS; a click is not proof of a shot.

Save your visual observations with frame references and, where useful, approximate target/crosshair pixel coordinates and uncertainty. Never invent an exact trajectory, hit rate, confidence percentage, current setting, or optimum. Crosshair pixels, raw counts, angular gain, and cm/360 are different quantities.

Give an answer first: the exact native setting to retain or test, what evidence supports it, and the main limit. Repeated comparable overtravel can support a small lower-gain test; unfinished acquisition or late tracking may point elsewhere. Change one relevant setting at a time. A successful hit does not prove optimality, and a single overshoot does not prove excessive gain. If the baseline is best supported, explicitly recommend retaining it and say what observation would change that judgment.

## Apply and continue the loop

Prepare the complete plan and backup location before seeking approval. A request to discover, observe, or recommend is not permission to change settings. A request to apply the proposed values, or a previously authorized bounded tuning loop, is authorization; do not ask again unnecessarily. Show the relevant file, keys, old/new values, and rollback path. Apply only within that authorization.

Use `scripts/settings_file.py` for supported INI, Frostbite text, and the narrowly supported THE FINALS save layout. Verify the game is closed before file mutation; wait rather than kill it. The helper requires a matching original hash, unique exact fields, a byte-identical backup, an atomic replacement, and readback. Its `--reviewed` and `--game-closed` flags record the agent's checks, not additional gamer forms or permission grants.

An exit-code-3 JSON result means a config write occurred but an audit update remains incomplete. Inspect the reported source state rather than assuming the intended value is still present. Read `status <receipt>` before further action; use `finalize <receipt> --game-closed` to recover an applied-but-prepared receipt without rewriting the config, or guarded rollback when appropriate. Preserve the returned artifacts and do not blindly repeat a patch after an audit failure; see [apply-and-rollback.md](references/apply-and-rollback.md).

An unknown game may require a new parser or settings-UI adapter. Inspect its format, implement and test the smallest reliable adapter on copies, and preserve unrelated values. Do not force a text patch into an encrypted, checksummed, ambiguous, or unsupported binary save. If safe file editing is unavailable, use a supported settings UI when authorized and available, or clearly report the unsupported application step while completing analysis and conversion.

After applying, verify the persisted value and, when possible, the game's displayed value on relaunch. Preserve the previous profile version and patch receipt. Compare another ordinary-play sample at the candidate setting, with similar weapon/optic conditions and unchanged DPI. Repeat only within the user's agreed time/change limits. Retain an improvement supported by comparison; rollback a regression; stop on inconclusive evidence, conflicting settings writes, capture failure, or the end of the authorized run.

## Handoff

Keep outputs outside this skill repository: versioned profiles, original session evidence, image annotations, recommendation, conversion assumptions, patch plans/receipts, and iteration journal. The gamer should receive a short verdict and an optional evidence report, not an analysis task list. Keep files local unless sharing is requested. The host agent's model/privacy settings govern any images it consumes.
