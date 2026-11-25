# Working in this repo

Pocket is a **native iOS** app (Swift / SwiftUI, iOS 17+). This is not a web
project — there is no `npm`. The build is defined as code via XcodeGen
(`project.yml`); regenerate the Xcode project with `xcodegen generate` after
changing files or targets.

## Apple frameworks evolve — verify, don't assume

SwiftUI, SwiftData, MusicKit and AVFoundation change meaningfully between OS
versions, and APIs may differ from training data. **SwiftData especially has a
set of device-only footguns this project has already hit — read
`docs/swiftdata-gotchas.md` before touching a `@Model`, `#Predicate`, or
model-driven sheet.** Before writing against an
Apple framework, check the current API (Xcode docs / developer.apple.com) and
heed deprecations. Pin the deployment target in `project.yml` and write to it.

**Audio source reality:** Apple Music streaming audio is DRM-protected and
cannot be tapped for raw PCM (waveform / time-stretch). The practice engine is
built on DRM-free **local / iCloud files**; Apple Music is browse/metadata only.
See `docs/decisions/0001-audio-source-local-first.md`. Do not reintroduce an
Apple-Music-as-waveform-source assumption without revisiting that ADR.

# Pre-push checklist

Run these before every commit that touches app code. Do not push until all pass.

> **Automated:** `./scripts/install-hooks.sh` installs a `pre-push` hook that
> mirrors CI (lint `--strict` + Swift-6 strict-concurrency build) so failures
> surface locally instead of as a follow-up "Fix CI" commit. Tiers via
> `POCKET_PREPUSH`: `fast` (default) · `full` (runs the `PocketAll` plan) ·
> `skip`. Bypass once with `git push --no-verify`. The steps below are the
> manual equivalent. Note CI runs an **older** toolchain (Xcode 16 / macOS-15)
> that is stricter than local Xcode 26.5 — the hook narrows but can't fully
> close that gap.
>
> **Docs-only changes are nearly free.** If a push touches only `**/*.md`,
> `docs/**` or `LICENSE`, the hook and CI skip lint/build/test (~20s instead of
> ~7min). One rule, `scripts/docs-only.sh`, serves both — change it there or not
> at all. Anything else, including `.github/workflows/**` and `*.xctestplan`,
> runs the full set. **Never add `paths-ignore` to `ci.yml`**: the required check
> would stop reporting and every docs PR would become unmergeable (ADR 0133).
>
> **One check runs regardless: `scripts/check-manual.py`** (ADR 0165), in the
> hook *above* the tier logic and in CI *inside* `lint-build-test` with no `if:`.
> It holds `docs/manual/` to what the app actually says, so the state that turns
> everything else off — a docs-only push — is the state it exists for. It is
> stdlib Python over markdown and takes a fraction of a second. Do not move it
> into `scope`, and do not give it a job of its own; see 0165 D8 for why both
> break the required check.

1. **Lint** — `swiftlint`. Fix all errors. Suppress only with
   `// swiftlint:disable:next <rule>` on the exact line, never file-wide.
   Two of the rules are this project's own invariants rather than style
   (`.swiftlint.yml` → `custom_rules`), and both exist because the thing they
   catch already shipped: analytics events may take no free `String`, and
   **user-facing copy says Red Moon, never Pocket** — `Pocket` is the target and
   bundle id, not a name the app goes by. A path or bundle-id literal that
   legitimately contains it takes a line-scoped suppression.
2. **Build** — `xcodebuild build -scheme Pocket -destination 'generic/platform=iOS Simulator'`.
   Fix all errors and warnings. This catches breakage in files with no test
   coverage — do not skip it.
3. **Tests** — `xcodebuild test -scheme Pocket -destination 'platform=iOS Simulator,name=iPhone 17'`.
   (Use `-testPlan PocketAll` to include `PocketUITests`, as CI does.)
   When adding or changing a feature, update the relevant test. When adding a
   new module with non-trivial logic, add a test under `PocketTests/`. Pure,
   UI-free logic (tempo math, slider mapping, automator stepping, planner
   weighting, identity) MUST be unit-tested — that's the logic that breaks
   silently otherwise.
4. **Docs** — after any significant change, review the table below and update
   every affected file. Do not skip this step.

   | File | Update when… |
   |---|---|
   | `CHANGELOG.md` | Any user-visible change — add an entry to `[Unreleased]` |
   | `PROJECT.md` | New/changed screen, data model, service, entitlement, env/config, or architecture decision |
   | `docs/architecture.md` | New/changed module, audio pipeline stage, persistence/sync change, or third-party service |
   | `docs/decisions/` | Any decision that closes off an alternative (new ADR, numbered) |
   | `docs/decisions/` (the **target**) | An ADR supersedes or amends another — see the backlink rule below |
   | `docs/design-brief.md` | Changes to the design system/tokens, screen inventory, or the design working protocol |
   | `docs/manual/` | A screen gains or loses a control, a control is renamed, a navigation path changes, or what's free vs Pro moves |
   | `README.md` | Changes to project structure, build/CI, or the "How it works" summary |

   **ADRs are a graph — write the back edge in the same commit.** When a new ADR
   supersedes, amends, or changes the status of an older one, **edit the older
   file too, in that same change**: a line in its header saying what was
   superseded, by which ADR and which decision, and what still stands. Saying it
   only in the new ADR's Consequences does not do it — that sentence describes
   an edit, it does not perform one. This already went wrong once: ADR 0187
   recorded that 0092 *"moves from Proposed to Accepted"* and superseded parts of
   0002, 0144 and 0112, and none of the four files mentioned 0187 at all, so
   0144 went on stating a price that had been replaced. A reader lands on the
   old ADR, not the new one, which is exactly when the pointer has to be there.

   **Declare it in a header field**, not only in prose: `- **Supersedes:** … ADR
   NNNN …` or `- **Amends:** … ADR NNNN …` (26 ADRs already do). `check-manual.py`
   **C16** reads those fields and fails if the named ADR does not refer back —
   prose alone is invisible to it, which is the deal: the field is what buys you
   the check. The 31 back edges already missing when C16 landed are listed in
   `KNOWN_MISSING_BACK_EDGES` and reported on every run; that number is a backlog
   to burn down, and repairing a pair means writing the note **and** deleting the
   line, which C16 also checks.

   **What counts as significant:** new screen, new model/service, schema or
   persistence change, removed behaviour, new entitlement or permission string,
   new build config / env var, infrastructure change. Pure refactors that don't
   change observable behaviour need only `CHANGELOG.md`.

# Conventions

- **Branches:** `pocket-0XX-short-title` (zero-padded, incrementing). Create the
  branch before editing; don't work on `main`.
- **Permissions:** never add an `Info.plist` usage string or entitlement the app
  doesn't actually exercise — over-broad permissions cause rejection.
- **Secrets:** no API keys in the client, ever. The Claude API key lives only in
  the backend proxy (see `infrastructure/`). The app talks to a base URL chosen
  by build configuration (Debug → local/dev proxy, Release → prod).
- **Pure logic stays pure:** keep tempo/identity/planner logic free of SwiftUI
  and AVFoundation imports so it stays unit-testable.

# Commit / PR

- Don't push or open PRs unless asked. If on `main`, branch first.
- After push/PR, wait for CI to be confirmed green before merging; don't poll in
  a loop.