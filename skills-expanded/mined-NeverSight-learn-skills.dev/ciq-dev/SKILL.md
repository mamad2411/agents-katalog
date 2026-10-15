---
name: ciq-dev
description: Develop Garmin Connect IQ apps and watch faces in Monkey C with this toolkit — build with strict type checking (level 3), write and run unit tests, verify changes in the simulator, run the publish-readiness gate, and find the right Garmin SDK docs and design guidelines. Use whenever writing or changing Monkey C code (.mc), watch faces, data fields, widgets, or device apps; when a build has type/warning errors; or when preparing an app for the Connect IQ Store. Routes to the build/test/check scripts and the simulator-control and setup skills.
---

# Developing Garmin Connect IQ apps (Monkey C)

Build strictly, test, run in the simulator, and stay publish-ready — for any watch face /
data field / widget / device-app.

> **Uses the `ciqkit` command.** If it isn't on PATH: clone
> https://github.com/bayville/garmin-connectiq-devkit and run `./install.sh` once (or call
> the repo's `scripts/*.sh` directly). Run from your project dir, or set `CIQKIT_PROJECT`.

## Core loop

```sh
ciqkit build [device]        # strict build: type-check level 3 + warnings (default)
ciqkit test  [device]        # unit tests -> PASSED (…failed=0, errors=0)
ciqkit sim reload            # push latest build into a running simulator
ciqkit check                 # full publish gate: strict release (all devices)+tests+.iq
```

Builds are **strict by default** (`-l 3 -w`) so type errors surface immediately, not at
submission. Don't lower it; fix the types. (`CIQKIT_TYPECHECK` / `CIQKIT_WARN` exist only
as escape hatches.)

## Where things live

- **Write tests** for pure logic behind the `(:test)` annotation; run with `ciqkit test`.
  Cover boundaries (0/100 battery, C/F, 12/24h, null vs present data). For draw/AOD code,
  use a mock `Dc`. → [TESTING.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/TESTING.md)
- **See it render / reproduce device state** → skill **`ciq-sim-control`** and
  [SIMULATOR_CONTROL.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/SIMULATOR_CONTROL.md).
  Prefer a screenshot to confirm any visual change.
- **Set up / fix the environment** → skill **`ciq-setup`**.
- **Prepare for the Store** → [PUBLISHING.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/PUBLISHING.md)
  (`ciqkit check` gate + the manual checklist: minimal permissions, assets, on-device soak).
- **Language + platform best practices** (typing, null/`has`, memory, power, AOD,
  resolution independence, localization) →
  [BEST_PRACTICES.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/BEST_PRACTICES.md).
  Read it before writing non-trivial Monkey C.
- **Official APIs, device capabilities, design/UX & watch-face guidelines** →
  [REFERENCES.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/docs/REFERENCES.md).
  Consult these for anything version-specific rather than guessing.

## Good habits this toolkit assumes

- Resolution-independent geometry; handle nullable Garmin APIs and unit prefs (12/24h, C/F).
- Keep string IDs in parity across every `resources*/strings`.
- Watch faces: keep the always-on/AOD view separate, sparse, shifted, mostly black.
- Verify visual changes with a screenshot; verify logic with a unit test.

## Rule

Changing toolkit script behavior REQUIRES updating the matching skill + docs and verifying
on a real simulator ([CONTRIBUTING.md](https://github.com/bayville/garmin-connectiq-devkit/blob/main/CONTRIBUTING.md)).
