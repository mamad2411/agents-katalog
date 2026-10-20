# CLAUDE.md - VoiceBabel Project Guidelines

## Project Overview

VoiceBabel is a macOS menu bar speech-to-text tool built with Swift. It supports two API modes:

- **Local** (WhisperKit) - offline on-device transcription
- **Cloud** (gpt-4o-transcribe) - HTTP API transcription

Both modes support transcription. Translation uses a two-step approach: first transcribe (using current API mode), then translate text via Apple Translation (local, macOS 15.0+) or Cloud GPT (gpt-4o-mini). The `translationEngine` setting in EngineeringOptions controls the strategy ("auto"/"apple"/"cloud").

## Architecture

```
main.swift -> AppDelegate (Composition Root)
                 |
                 +-- Config/SettingsDefaults (user preference defaults)
                 +-- Config/EngineeringOptions (engineering switches/constants)
                 +-- Config/SettingsStore (UserDefaults + ObservableObject)
                 +-- Config/KeychainHelper (API Key secure storage)
                 +-- UI/StatusBarController (menu bar UI)
                 +-- UI/SettingsWindowController -> UI/SettingsView (SwiftUI settings panel)
                 +-- Core/HotkeyManager (Option key gesture detection)
                 +-- Core/AppController (state machine / core dispatcher)
                 |       +-- Core/AutoSendManager (delayed send logic)
                 |       +-- Core/TranscriptionManager (audio → text, priority + fallback)
                 |       +-- Core/TranslationManager (text translation, engine fallback)
                 |       +-- Core/AudioRecorder (audio capture)
                 |       +-- Utilities/AudioEncoder (PCM → M4A/WAV encoding)
                 |       +-- Services/CloudOpenAIService (HTTP transcription + GPT translation; nested EngineErrorClassifier; @Published health)
                 |       +-- Services/LocalWhisperService (WhisperKit local)
                 |       +-- Services/LocalAppleTranslationService (Apple Translation local, macOS 15.0+)
                 |       +-- Utilities/TextInputter (text output to active window)
                 |       +-- Utilities/TextPostProcessor (tag filtering, Chinese script conversion)
                 +-- Utilities/LocaleManager (i18n locale management)
                 +-- Utilities/NetworkHealthMonitor (network recovery probe)
```

Components communicate via closures/callbacks, connected in `AppDelegate.setupComponents()`. Settings changes propagate in real-time via Combine publishers.

## Project Structure

### Directories

```
Core/                       — Core logic (state machine, hotkey detection, auto-send, transcription/translation managers, audio recorder)
Config/                     — Configuration (user prefs, engineering options, Keychain, settings store)
UI/                         — Menu bar controller, SwiftUI settings panel, settings window
Services/                   — Transcription & translation backends (Cloud / Local / Apple Translation)
Utilities/                  — Helpers (text input, text post-processing, audio encoding, network probe, logging, i18n locale manager)
VoiceBabel/                 — Resources (Assets, Storyboard, String Catalogs)
VoiceBabelTests/            — Unit tests
.dev-docs-private/          — Private dev docs (excluded from repo, separate local git).
                              Contains: .claude-tech-research/, .claude-commercial-research/,
                              .claude-plan/, .claude-code-review/, .human-learn/, .human-devlog/
```

### Root Files

| File | Description |
|------|-------------|
| **main.swift** | App entry point, creates NSApplication and AppDelegate |
| **AppDelegate.swift** | Composition root — initializes all components, connects callbacks, subscribes to settings changes via Combine |
| **Makefile** | Build/run automation (`make dev`, `make build`, `make run`, `make release`, `make clean`) |
| **voicebabel.log** | Runtime log file (auto-generated, not checked into git) |
| **VoiceBabel.xcodeproj/** | Xcode project bundle (directory displayed as a file in Finder). Contains `project.pbxproj` (build targets, file references, settings) |
| **CLAUDE.md** | This file — project guidelines for Claude |

## Coding Principles

These three principles apply to all code in this repository. Subdirectory `CLAUDE.md` files may add stricter, domain-specific rules (e.g. `Services/CLAUDE.md`), but must not contradict these.

1. **Log generously.** Use `Log.i` / `Log.w` / `Log.e` at decision points and boundaries — transcription/translation inputs and outputs, mode switches, fallback triggers, network failures, user-visible state changes. Favor one log line too many over one too few. Past bugs (silent language fallback, translation hang) were traceable only because logs existed; silent paths are the hardest to debug after the fact.

2. **Defensive, but not paranoid.** This is production code — validate at boundaries where bad input is plausible (user preferences, network responses, framework callbacks). Don't validate what internal code already guarantees. Never catch-and-silently-ignore errors or substitute fabricated defaults to "keep things running" — surface the error (via `Log.e` + propagate `Result.failure` / throw). A loud failure is a fixable bug; a quiet wrong-answer bug ships.

3. **Good craftsmanship, not over-engineering.** Follow Swift conventions, clear naming, small focused types. But: don't add abstractions for hypothetical second callers, don't build configuration knobs nobody asked for, don't wrap single-use logic in protocols. Three similar lines beat a premature generic. YAGNI applies — if the feature/flexibility isn't requested today, don't ship it today.

## Background Mode

All tasks should run in the background by default. Only report to the user in these cases:

1. Encountered an error that cannot be resolved independently
2. Need to request permissions
3. Task is complete

## Default Workflow

### Code Change -> Build -> Launch (Standard Flow)

After every code change, use the project Makefile:

```bash
make dev    # Build Debug + quit old process + launch new version
```

Other useful targets:

```bash
make build    # Build Debug only
make release  # Build Release
make run      # Quit old process + launch (without rebuilding)
make clean    # Clean build artifacts
make check    # Verify prerequisites
make help     # Show all targets
```

If build fails, debug and fix it yourself.

### When to restart the app

- **Behavioral changes** (new features, bug fixes, changed logic, modified UI): use `make dev` to rebuild AND restart so the running app reflects the changes.
- **Non-behavioral changes** (renames, comments, docs, CLAUDE.md, formatting, refactors that don't change behavior): `make build` is sufficient to verify compilation. No need to restart.

## Keeping CLAUDE.md Files Up-to-Date

CLAUDE.md files are distributed across the project — one in the root and one in each subdirectory.

- **Subdirectory CLAUDE.md**: When a subdirectory has significant changes (files added/deleted/renamed, major refactoring), update that subdirectory's CLAUDE.md to reflect the current state.
- **Root CLAUDE.md**: When the overall architecture changes significantly (new modules, removed components, changed communication patterns), update the root CLAUDE.md accordingly.

## Git Commit & Push

When the user asks to commit, follow this workflow:

### 1. Analyze changes
```bash
git status                    # Overview of all changes
git diff --stat               # Changed files summary
git log --oneline -5          # Recent commit style reference
```

### 2. Group commits by logical unit

Do NOT put everything into one commit. Group by purpose:

| Category | Example |
|----------|---------|
| Docs (research/plan/review) | Research docs, plan files, code reviews |
| Feature code | New service, controller changes, config |
| Config/meta | CLAUDE.md updates, Makefile, Xcode project |
| Tests | Unit tests |

### 3. Stage and commit each group

```bash
git add <specific files>      # Stage by group, never use `git add -A`
git commit -m "$(cat <<'EOF'
Short summary (imperative mood)

Optional body with details.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

### 4. Push only when explicitly asked

```bash
git push
```

### Commit message conventions
- Imperative mood: "Add feature" not "Added feature"
- First line under 72 chars
- Body explains "why" not "what" (the diff shows "what")
- Always include `Co-Authored-By` trailer
- Follow existing commit style in `git log`

### File naming conventions (for docs commits)
- `.dev-docs-private/.claude-tech-research/`: `01_topic_name.md` (sequential numbering)
- `.dev-docs-private/.claude-code-review/`: `01_review_name.md` (sequential numbering)
- `.dev-docs-private/.claude-plan/`: `01_plan_name.md` (sequential numbering)
- When renumbering files (e.g., after deletion), keep all numbers sequential with no gaps

## Internationalization (i18n)

- UI strings are localized via String Catalogs (`VoiceBabel/Localizable.xcstrings`), supporting 20 languages
- Log strings use a separate catalog (`VoiceBabel/LogStrings.xcstrings`), supporting en + zh only
- `Utilities/LocaleManager.swift` manages runtime locale switching (instant, no restart)
- AppKit code uses `LocaleManager.shared.localized("key")`, SwiftUI uses `Text("key")` with `.environment(\.locale)`
- Log messages use `LocaleManager.shared.logLocalized("key")`
- Log language is controlled by `EngineeringOptions.logLanguage` ("en" or "zh")

## Writing Style for User-Facing Markdown Documents

Applies to any markdown written *for the user to read* — docs under `.dev-docs-private/` (research, plans, reviews, devlogs, learning notes). Does not apply to source-code comments or CLAUDE.md files.

**Target reader**: between a layperson and a professional programmer. Knows basic programming concepts but not macOS internals, framework-specific jargon, or the acronyms in the Apple doc you just read. Default assumption: the reader does not know what you know.

Rules:
1. Keep jargon density low — introduce at most one new term per paragraph. Split the paragraph if more stack up.
2. On first use, expand every abbreviation and give a one-line plain-language gloss. Use the abbreviation freely after that.
3. Define each core concept plainly ("what it is") before discussing behavior, cost, or edge cases. Don't assume an API name is self-explanatory.
4. Favor analogies and contrasts when explaining non-obvious design (e.g. "narrow declarative door vs. wide passive listener").
5. Avoid stacking 3+ parenthetical asides, terms, or clauses in one sentence. Two short sentences beat one dense one.
6. After stating a fact, add the *why* or the *cost* when it helps understanding.
7. Keep citations rigorous (file:line, URLs, accurate terminology) — only the prose softens, not the precision.
8. End with a concrete action list when applicable; don't trail off where the reader still feels lost.