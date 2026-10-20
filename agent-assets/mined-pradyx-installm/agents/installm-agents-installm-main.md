# Project instructions

**Repository:** `PradyX/instaLLM` · Flutter / Dart local AI app.
**Goal:** Run AI locally, with privacy, offline use, and no mandatory cloud service.

## Project notes

- Start with [Project Status](</Users/prady/Vault/Projects/installm/Project Status.md>) and [shared Flutter conventions](</Users/prady/Vault/skills/flutter.md>).
- On Linux the same vault paths live under `/home/prady/Vault/...` instead of `/Users/prady/...` (macOS uses `/Users/prady/Vault/...`).
- Read only the relevant sections of [Roadmaps](</Users/prady/Vault/Projects/installm/Roadmaps.md>) and [Reference](</Users/prady/Vault/Projects/installm/Reference.md>). All phases are sections in one roadmap; all detailed designs, decisions and lasting outcomes belong in Reference.
- Keep current status and next work in Project Status; repair scoped section links when moving content. Do not add separate phase/topic notes or edit roadmap scope unless requested.
- Current code, architecture, tests and platform implementations take precedence over conceptual examples. Latest acceptance supersedes historical planning checklists. Project-specific rules below override shared defaults.

## Essential rules

- Keep local chat usable offline after resources are installed. Cloud features must be optional, explicitly enabled, separate, and documented. Network transmission must be intentional; never upload user content, model/device metadata, or benchmarks by default.
- Never unnecessarily log prompts, messages, private document text, audio, or credentials.
- Preserve user data and unrelated changes. Never reset, discard, stash, amend, delete unknown files, or overwrite configuration to simplify the task. Inspect Git status before destructive operations or staging.
- Version persisted structures. When changing storage, provide and test migrations, including partial/corrupt data; never migrate by deleting user data.
- Keep conversations independent of models, preserve history across model switches, and record the generating model on assistant messages.
- Keep UI separate from persistence and low-level inference. Prefer capability checks over model-name checks and incremental, testable services over rewrites.
- Read authoritative GGUF metadata where available. Distinguish managed files from external references; removing an external model record must not delete its source file without explicit permission.
- Use token-aware context with the system prompt preserved, output tokens reserved, and attachment/retrieval overhead counted.
- Consider Android, macOS, and Linux; isolate platform behavior. Avoid unnecessary model copies, large buffers, repeated parsing/tokenization, and simultaneous model loads. Support cancellation where feasible.
- Return actionable errors. Check dependency maintenance, platform support, size, license, and existing alternatives. Treat runtime/binding migrations as separate work and retain the stable path until verified.
- Keep defaults simple and advanced controls discoverable. Local APIs default to `127.0.0.1`; validate tool requests through permission boundaries. Do not introduce arbitrary execution, autonomous features, or unrelated redesigns without an explicit request; consult the Product Principles and Local API and Tools sections in `Reference.md` for scope limits.

## Running and building

- Look in `scripts/` before running or building the app, and use the script for that target instead of an ad-hoc `flutter run`/`flutter build` command.
- macOS: launch with `scripts/run_macos.sh`. It renews the development provisioning profile and then hands over to `flutter run -d macos`, because Apple issues free Personal Team profiles for only seven days and Flutter's macOS build path never passes `-allowProvisioningUpdates`; a bare `flutter run -d macos` therefore fails with "No profiles for 'com.prady.installm' were found" roughly once a week. `--ensure-only` checks or renews signing without launching; `--force-refresh` renews even when the profile still looks valid.
- Packaging and native runtime: `scripts/build_mac_dmg.sh` (release build plus DMG; that DMG is signed with the local Apple Development identity, so it is a testing artifact — distributing one needs a Developer ID signature and notarization), `scripts/build_linux_archive.sh`, and `scripts/build_llama_native_libs.sh`, each with its matching `scripts/BUILD_*.md` notes.
- Android APK: `scripts/build_android_apk.sh` builds debug by default; pass `--release` for a configured release-signing build.
- Linux: launch with `scripts/run_linux.sh`. The bare `flutter run -d linux` skips two prerequisites that fail quietly: `.env` is gitignored but read at startup, and `linux/lib` (the llama.cpp runtime this repository builds) is gitignored too — without it the app opens but no model can load. The script creates `.env` from `.env.example` and reports a missing `linux/lib` with the build command; `--check-only` checks without launching, and remaining arguments pass through to `flutter run`.
- macOS compile-only validation: `scripts/check_macos_build.sh` compiles without signing into `build/macos_validation` when provisioning is unavailable; it does not launch the app or change signing configuration.
- Branding: `scripts/generate_brand_icons.py` rasterizes `InstaLLM_llama_vector.svg`; launcher/splash regeneration and explicit desktop data migration are documented in `README.md`.
- macOS release builds sign with the same team, so if one fails on provisioning, run `scripts/run_macos.sh --ensure-only` first instead of changing signing settings.
- macOS native tests: `scripts/test_macos.sh integration_test/<test>.dart` checks signing and refuses a second app instance. Native tests leave a test-entrypoint bundle; rebuild/open the normal app afterwards with `scripts/open_macos_app.sh`.
- macOS: to hand the app to the user rather than hot-reload it, use `scripts/open_macos_app.sh`. It rebuilds from `lib/main.dart` and opens the bundle through LaunchServices, the way Finder and the Dock do, which is also the only way macOS attributes a privacy prompt (such as device recognition) to the app instead of to a terminal; a bundle left over from `flutter test integration_test/... -d macos` starts blank, and `--no-build` opens an existing bundle. It refuses to start a second copy, because two instances write the same conversations, settings and model directory.
- When a platform's run or build step has no script yet, add one to `scripts/` and list it here, rather than leaving the next agent to rediscover the command.
- This Mac pops "The \"python3\" command requires the command line developer tools" from time to time. It is not this project and not a plain `python3` or `git` run from a terminal: the desktop app runs its helpers inside a sandbox, Apple's `git`/`python3` toolshim cannot read `/private/var/select/developer_dir` there, and so it concludes the Command Line Tools are missing and asks to install them (verified by reproducing the denial with `sandbox-exec` and reading the sandbox log). `DEVELOPER_DIR` is set in the GUI session to the directory `xcode-select -p` reports, which is what the shim checks first, so newly launched GUI apps no longer trip it. If the dialog returns, check `launchctl getenv DEVELOPER_DIR` and re-apply `launchctl setenv DEVELOPER_DIR "$(xcode-select -p)"`, then relaunch the app so it inherits the value; `launchctl unsetenv DEVELOPER_DIR` reverts it.

## Work and validation

- For any user-requested visual redesign, present four meaningfully different mockups first and wait for the user's approval before editing the app UI. Once a mockup is approved, implement that choice without requesting the same approval again. Routine bug fixes that preserve the accepted design do not need a new mockup cycle.
- Preferred design language: the approved [compact bot settings mockup](mockups/bot_settings_compact.html). Use compact neutral surfaces, clear typography and hierarchy, generous but controlled spacing, subtle single dividers, flat rows and restrained accent colour. Group avatar/name with a quiet Change image action and right-aligned Edit control; avoid oversized controls, decorative nested cards, long explanatory text and prominent outlined destructive pills. Reserve red emphasis for Delete; keep Clear chat neutral. Adapt this language to light/dark themes, narrow layouts and large text using the app's theme tokens. Treat the mockup as a visual reference, not a replacement for existing functionality or persistence safeguards.
- Inspect the owning modules, data flow, persistence, runtime APIs, platform code, and tests before proposing changes.
- Before significant implementation, give a concise plan covering affected files, data/migrations, platforms, risks, and tests. For large architecture changes, stop after the plan for approval; small scoped fixes need no extra approval cycle.
- Implement the smallest coherent change. Avoid unrelated cleanup, whole-file formatting, and needless public-interface changes.
- For implementation changes, run `dart format .`, `flutter analyze`, and `flutter test`, preserving unrelated edits. Validate affected native platforms as far as possible; report unavailable checks and never claim untested behavior works. Use the Engineering Workflow section in `Reference.md` for the required tests by change type.
- Before every commit, launch the current app from its normal entrypoint with the appropriate `scripts/` launcher and smoke-test the affected flows in the running app. Builds, analysis, unit/widget tests and `--check-only` are not substitutes. Record the platform, launch command, interactions and result. Do not commit until this runtime check passes; if launch or interaction is unavailable, report the exact blocker and stop before committing. Preserve user data and avoid a second app instance.
- A roadmap unit is complete only when implemented, validated, documented, committed, and pushed. Stage only relevant files, commit before the next unit, and report the hash/message or exact blocker. Record completion in task/project notes; preserve roadmap content unless explicitly asked to edit it.
- Commit and push whenever a phase is worked on or finished, including the steps inside one phase: work that exists only in the working tree is not progress. Push the branch as part of the work, and report the commit hash and the push result, or the exact blocker.
- Never add a co-author trailer, a "Generated with" line, or any other agent signature to a commit (`Co-Authored-By: Codebuff`, `🤖 Generated with Codebuff`, and the like). The commit message describes the change and nothing else: the user owns the history, and no tool is a co-author of it.
- Report the changes, validation, limitations, and next step concisely; include the Git commit for completed roadmap work.
