---
name: spin-macos-gemma
description: Boot the Zekra Flutter macOS app with a real Gemma .litertlm bundle (or swap between bundles) so you can drive end-to-end probes — agent loop, tool calls, persona responses — without flashing the Pixel. Covers single-instance and N-instance pools, picking which bundle to test (base E2B, base E4B, fine-tuned, runtime-LoRA variants), the DDS WebSocket hookup, and the common boot-time failures with their fixes.
user-invocable: true
allowed-tools: Read Bash Edit Write
---

# Spin a macOS Gemma instance for end-to-end probing

The Zekra macOS Flutter app loads the same `.litertlm` bundle, the same agent code, and the same ObjectBox store as the Pixel build — so you can probe model behavior (tool firing, persona, voice, regressions across exports) at desktop speed without going through `adb install` + logcat.

This skill covers:

1. One-time setup (cache, dylibs, model symlinks)
2. Picking which Gemma `.litertlm` bundle to load
3. Booting a single instance
4. Booting an N-instance pool for parallel scenario sweeps
5. Driving the running app via the Dart VM Service (DDS WebSocket)
6. Common failures and their fixes

Read this before you spawn an instance. A wrong cache state or a missed symlink will silently load the wrong model or fail with a SEGV that looks like a code bug.

## What you can swap between

**Canonical bundle directory: `/Users/amanie/Documents/zekra-ai/models/gemma4-e2b-care/`**

This is where current fine-tuned E2B exports land. Each export of an SFT run produces one or more `.litertlm` files here, named by quantization recipe. List the directory before picking one — the catalog evolves with each training run:

```bash
ls -lh ~/Documents/zekra-ai/models/gemma4-e2b-care/
```

Naming convention (suffix tells you the quant recipe):

| Suffix | Quant recipe | Size | Notes |
|---|---|---|---|
| `*-dyn-wi8.litertlm` | dynamic int8 weights, fp32 activations | ~3.8 GB | smaller, slight quality hit |
| `*-dyn-wi8-auto.litertlm` | dynamic int8 with auto-rounding | ~4.7 GB | balanced — typical first probe |
| `*-wo-wi8.litertlm` | weights-only int8 | ~3.8 GB | smaller, simpler quant |
| `*-wo-wi8-auto.litertlm` | weights-only int8 with auto | ~4.7 GB | balanced |
| `*-wi4.litertlm` | int4 (smaller variants from earlier runs) | ~2.5-3 GB | smallest; tone often degrades |

Read the file names in the directory at probe time — don't assume specific suffixes exist for a given training run.

**Control baselines (don't change between runs):**

| Path | Size | What it is |
|---|---|---|
| `models/gemma4-e2b-base/gemma-4-E2B-it.litertlm` | 2.4 GB | Google's official base E2B IT, byte-for-byte. A/B against this. |
| `models/gemma4-e4b-base/gemma-4-E4B-it.litertlm` | 3.4 GB | Google's official base E4B IT — for size-class comparison. |

Persona test (canonical "is this a working Zekra fine-tune?"): ask "Who are you?" → base says "I am a memory companion / AI assistant", a working Zekra fine-tune answers in-character (e.g., "I'm Zekra — I'm here to help you remember."). See memory `project_base_e2b_better_than_sft_for_tone` for the gotcha: a BAD SFT can be WORSE than base on persona, so always A/B against `gemma4-e2b-base` before declaring an export "good".

Tool-firing test: ask "What's today like?" — a working fine-tune should fire `<|tool_call>call:today_summary{}<tool_call|>`. Base usually answers in prose without firing.

## One-time setup (skip if you've already booted macOS Zekra once)

These three things must be true before any boot:

### 1. flutter_gemma native cache pre-populated

flutter_gemma 0.14.0+ has a broken macOS hook (`hook/build.dart` ships a stale SHA256). The hook fails silently and the `.app` ends up missing `LiteRtLm.framework` — boot dies on `dlopen` with no obvious error.

```bash
mkdir -p ~/Library/Caches/flutter_gemma/native/macos_arm64
curl -sL https://github.com/DenisovAV/flutter_gemma/releases/download/native-v0.10.2/litertlm-macos_arm64.tar.gz \
  | tar -xzf - -C ~/Library/Caches/flutter_gemma/native/macos_arm64
```

Verify 5 dylibs in the cache:

```bash
ls ~/Library/Caches/flutter_gemma/native/macos_arm64/
# expect: libLiteRtLm.dylib libLiteRtMetalAccelerator.dylib
#         libGemmaModelConstraintProvider.dylib libStreamProxy.dylib
#         libLiteRtTopKMetalSampler.dylib
```

### 2. ObjectBox host dylib

```bash
[ -f ~/Documents/zekra-ai/flutter/libobjectbox.dylib ] || {
  cd /tmp && curl -s https://raw.githubusercontent.com/objectbox/objectbox-dart/main/install.sh | bash
  cp /tmp/lib/libobjectbox.dylib ~/Documents/zekra-ai/flutter/libobjectbox.dylib
}
```

### 3. Symlink the model + ArcFace into `~/Documents/`

The macOS app is non-sandboxed, so `getApplicationDocumentsDirectory()` returns `~/Documents/`. The app reads `~/Documents/model.litertlm` and `~/Documents/w600k_r50.onnx`.

```bash
# ArcFace (same one Pixel uses)
ln -sf ~/Documents/zekra-ai/flutter/assets/models/w600k_r50.onnx ~/Documents/w600k_r50.onnx

# Model — pick which bundle from models/gemma4-e2b-care/ or a base.
# List what's available, then symlink one:
ls -lh ~/Documents/zekra-ai/models/gemma4-e2b-care/

# Pick a fine-tuned variant (replace <variant> with one from the listing):
ln -sf ~/Documents/zekra-ai/models/gemma4-e2b-care/model-dyn-wi8-auto.litertlm ~/Documents/model.litertlm

# Or the control baseline:
ln -sf ~/Documents/zekra-ai/models/gemma4-e2b-base/gemma-4-E2B-it.litertlm ~/Documents/model.litertlm
```

Verify the symlink before booting:

```bash
ls -lh ~/Documents/model.litertlm   # tells you which bundle is loaded
```

If you need an old run's state nuked: `rm -rf ~/Documents/zekra-objectbox`. Schema-UID mismatches on boot mean the store is from a different code revision — wipe it.

## Single-instance boot

```bash
cd ~/Documents/zekra-ai/flutter

# clean build state if you've been swapping macOS toolchains
# rm -rf build .dart_tool

# Optional: force HF backend instead of on-device.
# Default is on-device when /Documents/model.litertlm exists. To force HF,
# set ZEKRA_LLM=hf and have HF_TOKEN in .env.
flutter run -d macos --debug 2>&1 | tee /tmp/zekra-macos-run.log
```

What to watch for in `/tmp/zekra-macos-run.log`:

| Log line | Means |
|---|---|
| `[LiteRtLmFfi] Loading native libraries...` | flutter_gemma found the framework |
| `GemmaService: installed model from /.../Documents/model.litertlm` | the symlink resolved + installed |
| `GemmaService: model loaded` | engine init succeeded, warm-up session ready |
| `Dart VM Service on macOS is available at: http://127.0.0.1:NNNN/TOKEN=/` | DDS endpoint ready to drive |
| RSS ≥ 3 GB in Activity Monitor | weights actually resident |

Run boot is **~30-60s for E2B**, **~60-90s for E4B**. Don't probe before `model loaded` lands.

Toggle the LLM backend explicitly (resolved by `scripts/deploy_pixel.sh`-style env wiring in `lib/main.dart`):

```bash
ZEKRA_LLM=local flutter run -d macos --debug    # force on-device flutter_gemma
ZEKRA_LLM=hf    flutter run -d macos --debug    # force HF Inference (gemma-4-26B-A4B-it via featherless-ai)
```

If neither is set, default is on-device when a model file exists. Memory `project_zekra_hf_default_backend` covers the Pixel-side defaults (different — defaults to HF there because flutter_gemma 0.15 on-device is broken on Android).

## N-instance pool (parallel probes)

Use this when you want to run a scenario sweep across multiple profiles in parallel. The dispatch-pool flow we used today: 12 instances, each with its own ObjectBox dir + seeded profile, all sharing one model file.

See [[reference-macos-pool-spinup]] (memory) for the full pool-driver recipe — `scripts/flutter_pool.py` does the sequential-build then parallel-launch dance. The two critical bits:

- **`flutter run` builds serialize through xcodebuild's build.db** — N parallel `flutter run` calls cannot all build at once. `FlutterPool.start()` waits.
- **`ZEKRA_POOL_NO_GEMMA=1` skips Gemma load** — boots in ~10s instead of ~60s and saves ~3 GB RSS per instance. Use this when you only need `dispatchTool()` against ObjectBox (data generation), not the LLM agent. **Do NOT** set this if you're testing model behavior — it disables the very thing you're trying to probe.

For LLM probes across profiles, leave Gemma loaded and cap the pool at 2-4 instances (each is 3 GB+).

## Driving the running app from outside

`flutter run -d macos --debug` exposes a Dart VM Service on `127.0.0.1`. The plain HTTP surface rejects `evaluate` (`"No compilation service available"`); use the DDS WebSocket. `scripts/macos_chat_harness.py` wraps it.

Minimal probe — send a chat turn and capture the raw reply:

```python
import sys
sys.path.insert(0, "/Users/amanie/Documents/zekra-ai/scripts")
from macos_chat_harness import connect, run_future_capture, dart_string_literal

vm = connect()    # auto-discovers the latest /tmp/zekra-*-run.log
expr = (
    f"gemmaService.send({dart_string_literal('Who are you?')}).then("
    f"(r) => File('/tmp/probe.txt').writeAsStringSync(r.toString()))"
)
vm.evaluate(expr)
# Then poll /tmp/probe.txt
```

For end-to-end (with tool dispatch) use `chatAgent.send(...)` which runs the full agent loop:

```python
expr = (
    f"chatAgent.send({dart_string_literal('What is today like?')}).then("
    f"(r) => File('/tmp/probe.txt').writeAsStringSync(r.toString()))"
)
```

`chatAgent.send` returns the cleaned final prose (envelopes stripped). `gemmaService.send` returns the raw reply including `<|tool_call>...<tool_call|>` if any.

To probe across many scenarios reliably, use `scripts/zekra_macos_scenario_runner.py` — it manages session reset between scenarios, crash-safe per-turn JSONL appends, and parses envelopes via the canonical `zekra_envelope_parser`. The scenario master corpus is at `colab-upload/scenarios_from_sft_augmented.py` (900 scenarios, 275 multi-turn).

## Swapping bundles between probes

To compare two bundles on the same scenarios:

```bash
# Kill current run (DDS dies with it)
pkill -f "flutter run -d macos"

# Switch the model — pick a different variant from gemma4-e2b-care/
ln -sf ~/Documents/zekra-ai/models/gemma4-e2b-care/model-wo-wi8.litertlm ~/Documents/model.litertlm

# Optionally wipe ObjectBox if the new bundle has a different schema/UID
# rm -rf ~/Documents/zekra-objectbox

# Relaunch (logs go to a fresh file)
cd ~/Documents/zekra-ai/flutter
flutter run -d macos --debug 2>&1 | tee /tmp/zekra-macos-run.log
```

flutter_gemma caches the **last-installed model** under `~/Library/Application Support/com.zekra.zekra/` so subsequent `installModel(...)` calls become no-ops on the wrong file. After a symlink change you may need to wipe:

```bash
rm -rf ~/Library/Application\ Support/com.zekra.zekra/flutter_gemma/    # forces re-install
```

(If the rename of `.litertlm` files in `~/Library/Application Support/` doesn't happen on rebuild, that's why your "new bundle" tests still show old behavior. Always wipe and re-install when changing bundles.)

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `dlopen … LiteRtLm.framework` not found | flutter_gemma cache empty or hook failed silently | Repopulate `~/Library/Caches/flutter_gemma/native/macos_arm64/` (setup step 1) |
| `install_name_tool … can't be redone` for `libGemmaModelConstraintProvider.dylib` | Cached dylib was already relinked once | `rm -rf ~/Library/Caches/flutter_gemma/native/macos_arm64 flutter/build`, repopulate, rebuild |
| `Failed to foreground app; open returned 1` | Old `zekra.app` still alive | `pkill -f zekra.app` then relaunch |
| `Incoming property ID … does not match existing UID` | Schema bumped since last run | `rm -rf ~/Documents/zekra-objectbox` |
| `GemmaService: init failed: SEGV` after switching bundles | Loaded bundle is incompatible (wrong `cache_length` vs `maxTokens=4096` in `gemma_service.dart:50`, OR a bundle exported with `--experimental_lightweight_conversion` for GPU). | Confirm the bundle's `cache_length` matches `maxTokens`. Re-export without `--experimental_lightweight_conversion` if MUL(const,const) error appears. Memory `project_dont_second_guess_reverse_engineering`. |
| Model loads but persona says "I am an AI assistant" / generic | Loaded base, not fine-tune; OR the SFT model is regressing on persona (worse than base) | Check the symlink target. Compare against `gemma4-e2b-base` deliberately — bad SFT can be worse than base (memory `project_base_e2b_better_than_sft_for_tone`) |
| `chatAgent.send` returns empty/short reply | `tools: const []` is the current on-device contract; sending OpenAI-shape tools breaks `<|tool_call>` parsing | Don't pass tools to flutter_gemma 0.15.x on-device (memory `project_gemma4_no_openai_tools`). |
| KV cache wraps, replies degrade after 5-6 turns | Cache full, not a model bug | `chatAgent.resetSession()` between scenarios, or after long single sessions. Memory `feedback_kv_cache_not_window`. |
| `flutter run` drops "Lost connection to device" mid-probe | DDS dies when `flutter run` exits, but the underlying `zekra.app` keeps running on the model | Kill `zekra.app` and relaunch — the bare VM service is auth-token-gated and the token only prints at `flutter run` start. |

## Reference: file paths

| What | Where |
|---|---|
| Model symlink (single source of truth at boot) | `~/Documents/model.litertlm` |
| ArcFace symlink | `~/Documents/w600k_r50.onnx` |
| ObjectBox store | `~/Documents/zekra-objectbox/` |
| flutter_gemma's installed-model cache | `~/Library/Application Support/com.zekra.zekra/flutter_gemma/` |
| flutter_gemma native lib cache | `~/Library/Caches/flutter_gemma/native/macos_arm64/` |
| Fine-tuned bundle directory (current SFT exports) | `~/Documents/zekra-ai/models/gemma4-e2b-care/` |
| Control baselines | `~/Documents/zekra-ai/models/gemma4-e2b-base/`, `models/gemma4-e4b-base/` |
| Backend toggle | `flutter/lib/services/gemma_service.dart` line 51 (`PreferredBackend.gpu`/.cpu) |
| `maxTokens` (must match bundle's `cache_length`) | `flutter/lib/services/gemma_service.dart` line 50 |
| Single-instance log | `/tmp/zekra-macos-run.log` (by convention) |
| Pool log | `/tmp/dispatch_pool.log` |
| Scenario master (900 scenarios) | `colab-upload/scenarios_from_sft_augmented.py` |
| Scenario runner | `scripts/zekra_macos_scenario_runner.py` |
| DDS harness wrapper | `scripts/macos_chat_harness.py` |
| Envelope parser (canonical) | `/tmp/zekra_envelope_parser.py` |

## When you don't need this skill

- Just want to read scenario data on disk: nothing to spin, read the JSONL.
- Want to probe a fine-tune on the Pixel: use `deploy-zekra-bundle` skill instead.
- Want to compare against an HF-hosted model: set `ZEKRA_LLM=hf` and the bundle symlink doesn't matter.
- Want to test something that doesn't touch the model (UI flows, ObjectBox state, dispatch logic in isolation): use the `manual-qa-flutter-macos` skill or boot the pool with `ZEKRA_POOL_NO_GEMMA=1`.
