---
name: integrate-game-engine
description: Bridge game architecture across engines, manage headless test runners, configure export pipelines, and enforce asset normalization. Use when configuring Godot, Unity, Unreal, or Web game engine builds and headless test runners.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests, run_linter, execute_command]
version: "1.0.0"
---

# Integrate Game Engine

Manage engine-level lifecycles, cross-platform export presets, headless automated verification, and asset importer pipelines across production game engines.

## Core Rules

- **Headless-First Verification**: Every gameplay module or system must be verifiable without launching a graphical window (`godot --headless --run-tests`, Unity `-batchmode -nographics`, Unreal `-nullrhi`). Headless test suites must return standard OS exit codes ($0 = \text{success}$).
- **Deterministic Asset Import**: Asset import settings (texture compression, sprite slice rectangles, audio sample rates, 3D glTF mesh optimizations) must be codified in version-controlled config files (`.import`, `.meta`, `.uasset` manifests), never edited ad-hoc.
- **Strict Frame Budgeting**: Configure target engine frame limits (e.g. $16.6\text{ms}$ budget for $60\text{FPS}$, $8.3\text{ms}$ for $120\text{FPS}$). Enforce maximum draw call ceilings ($\le 250$ on mobile, $\le 2000$ on desktop).
- **Engine-Agnostic Core Boundary**: Structure game state, data models, and business logic into pure libraries or decoupled modules that interact with engine nodes exclusively through thin adapter interfaces.

## Suggested Process

### 1. Engine Detection & Project Fingerprinting
Inspect project root signals to identify the active engine:
- Godot: `project.godot`
- Unity: `Assets/` and `ProjectSettings/ProjectVersion.txt`
- Unreal: `*.uproject`
- Web: `package.json` with `phaser`, `pixi.js`, or `three`
- Other: `Cargo.toml` (`bevy`), `conf.lua` (`love2d`), `*.py` (`pygame`)

### 2. Headless Test Runner Integration
Set up an automated CI test harness:
```bash
# Example Godot 4.x headless runner
godot --headless --path . -s tests/run_suite.gd --quit-after 500
```
Verify stdout parses test assertions and exits with non-zero on failure.

### 3. Asset Pipeline & Texture Optimization
Enforce automated texture compression:
- Desktop: BC7 / DXT5
- Mobile: ASTC (4x4 or 6x6) / ETC2
- Web: KTX2 / Basis Universal
Verify texture sizes are power-of-two (POT) to ensure mipmap generation and GPU alignment.

### 4. Build Pipeline Automation
Configure export profiles for targeted platforms (Windows, Linux, macOS, WebAssembly/HTML5, Mobile). Ensure debug symbols are stripped in release builds and assets are packed into binary archives (`.pck`, Addressables bundles, `.pak`).

## Output Contracts

When completing engine integration or build automation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Headless test runner executes in CI with exit code $0$ on passing suites
- [ ] Texture compression and import settings are committed to version control
- [ ] Target framerate budget and VSync configurations are explicitly set
- [ ] Export templates strip editor code and debug asserts in release configurations
- [ ] Binary package size complies with platform store distribution limits

## Failure Modes

- **Graphical-only verification**: tests can only run with a window open, so CI never executes them and failures ship silently. Mitigation: enforce headless-first verification (`godot --headless`, Unity `-batchmode -nographics`, Unreal `-nullrhi`) for every module.
- **Swallowed test failures**: the runner prints assertion failures but still exits $0$, so CI goes green over broken suites. Mitigation: verify stdout parsing maps failures to non-zero OS exit codes before trusting a pass.
- **Ad-hoc import drift**: import settings edited locally instead of in version-controlled `.import`/`.meta`/manifest files produce nondeterministic, machine-dependent builds. Mitigation: codify all compression, slicing, and optimization settings in committed configs.
- **Wrong platform compression**: ASTC shipped to desktop or DXT to web yields garbled or black textures on target devices. Mitigation: enforce per-platform profiles (BC7/DXT5 desktop, ASTC/ETC2 mobile, KTX2/Basis web) and verify POT sizes.
- **Draw call ceiling blown**: scenes exceed draw call budgets ($\le 250$ mobile, $\le 2000$ desktop) and collapse the frame rate post-integration. Mitigation: enforce ceilings in CI profiling against the explicit frame budgets.
- **Engine lock-in**: business logic entangled with engine nodes makes porting or headless testing impossible. Mitigation: keep game state and logic in pure libraries behind thin adapter interfaces.
- **Editor code in release**: debug asserts, editor-only tools, or symbols survive into shipping builds. Mitigation: configure export templates to strip editor code and debug symbols in release configurations.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: engine binaries, export templates, and engine plugins/addons are external executables in the build path. Mitigation: pin exact engine and template versions, verify checksums against official releases, and reject unverified plugin downloads.
- **ASI05 RCE Guard**: CI constructs engine CLI commands (`godot --headless`, `RunUAT`, `-batchmode`) from project paths and arguments. Mitigation: validate paths and flags against allowlist patterns; never interpolate untrusted branch or asset names into shell invocations.
- **ASI08 Cascading Failures**: a failing import or asset step must not let the build continue with half-applied presets. Mitigation: fail the pipeline explicitly at the first non-zero exit and report the failing stage to the coordinator.
- **ASI07 Inter-Agent Communication**: engine configuration is consumed by gameplay and game-feel roles downstream. Mitigation: emit the schema-valid `implementation-result.json` contract with runner, budget, and export settings so peers integrate against validated configuration.
- **ASI09 Human-Agent Trust Exploitation**: do not report "headless suite passing" without the run evidence. Mitigation: cite the actual exit code and suite output; disclose skipped or flaky tests.

## Related Skills

- **develop-gameplay-systems**: core gameplay loops and fixed-timestep execution
- **tune-game-feel**: audiovisual feedback calibration and accessibility settings
