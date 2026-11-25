---
name: automate-game-publishing
description: Automate headless cross-platform game builds, Steamworks SteamPipe depot uploads, itch.io Butler CLI deployments, and web/mobile release packaging. Use when setting up CI/CD release pipelines, Steam/itch.io deployment scripts, or reproducible build artifacts.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Automate Game Publishing

Architect reproducible, headless CI/CD build and release pipelines that compile cross-platform game binaries, verify artifact integrity, and deploy delta patches to Steam, itch.io, Web, and mobile storefronts.

## Core Rules

- **Reproducible Headless Builds**: Every release artifact must be built exclusively from clean version-controlled source via headless CLI runners (`godot --headless --export-release`, Unity `-batchmode -quit`, Unreal `RunUAT BuildCookRun`), never exported manually from a developer's local editor state.
- **Secret & Credential Isolation**: Never commit Steamworks credentials, itch.io Butler API keys, or code-signing certificates into repository files (`app_build.vdf`, export presets). Inject secrets exclusively via CI environment variables.
- **Pre-Publish Smoke & Integrity Gate**: Block store deployment unless automated headless unit tests pass, binary executables exist with non-zero pak/pck archives, and debug symbols are archived separately from stripped shipping binaries.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when completing build and publishing automation pipelines.

## Suggested Process

### 1. Semantic Versioning & Build Metadata Injection
Stamp every build artifact deterministically with version and Git commit metadata (`vMAJOR.MINOR.PATCH+sha`) inside the engine configuration before invoking the export compiler so runtime crash logs identify the exact commit.

### 2. Multi-Platform Headless Export Matrix
Configure matrix build stages across Windows (`x86_64`), Linux (`x86_64`), macOS (universal binary + notarization), and WebAssembly (`SharedArrayBuffer` COOP/COEP headers verified):
- Strip editor-only tools, debug consoles, and unreferenced test scenes from release `.pck` / `.pak` bundles.

### 3. Steamworks SteamPipe Depot Configuration
Author declarative `app_build.vdf` and per-OS `depot_build_*.vdf` manifests:
- Exclude `*.pdb`, `*.debug`, and local save directories via `FileExclusion` rules.
- Execute `steamcmd +login $STEAM_USER +run_app_build app_build.vdf +quit` to upload binary delta chunks to a staging beta branch (`staging` / `rc`) before manual live promotion.

### 4. itch.io Butler CLI & Web Deployment
Push incremental binary patches via `butler push build/windows user/game:windows-stable --userversion $VERSION` and validate channel manifest status via `butler status`.

## Output Contracts

When completing game publishing automation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Headless CLI export scripts produce deterministic release binaries across target platforms
- [ ] Build version and Git commit SHA are automatically injected into game metadata
- [ ] Debug symbols (`.pdb`, `.dSYM`) are stripped from shipping depots and archived as build artifacts
- [ ] SteamPipe `.vdf` manifests and Butler scripts read credentials strictly from CI environment variables
- [ ] Automated smoke test verifies executable launch and asset archive integrity prior to upload
- [ ] Store deployments target a staging or release-candidate channel before public promotion

## Failure Modes

- **Credential leakage**: Steamworks passwords, Butler API keys, or code-signing certs are committed inside `app_build.vdf` files or export presets. Mitigation: inject credentials exclusively via CI environment variables; scan manifests before commit.
- **Non-reproducible export**: a release binary is exported manually from a developer's local editor state instead of a clean checkout, shipping local-only changes. Mitigation: build exclusively via headless CLI runners (`godot --headless --export-release`, Unity `-batchmode -quit`, `RunUAT BuildCookRun`) from version-controlled source.
- **Direct-to-live promotion**: a depot upload bypasses staging and lands on the public branch before validation. Mitigation: target `staging`/`rc` beta branches first and require manual live promotion.
- **Broken artifact shipped**: a zero-byte or corrupt `.pck`/`.pak` archive passes through because the integrity gate was skipped. Mitigation: block deployment unless automated tests pass, archives verify non-zero, and executable launch is smoke-confirmed.
- **Debug symbols in depot**: `.pdb`/`.dSYM` files ship to players, bloating downloads and exposing internals. Mitigation: enforce `FileExclusion` rules and archive symbols separately as build artifacts.
- **Untraceable crash logs**: shipped builds lack version/commit metadata so player crash reports cannot be mapped to source. Mitigation: stamp `vMAJOR.MINOR.PATCH+sha` into engine metadata before invoking the export compiler.
- **Broken web headers**: the WebAssembly build uploads without `SharedArrayBuffer` COOP/COEP headers and fails at runtime. Mitigation: verify response headers before the web deployment stage.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Steam and Butler credentials are the publishing identity; their misuse pushes builds under the studio's store presence. Mitigation: scope secrets to deploy jobs only, never print them in CI logs, and rotate them on pipeline change.
- **ASI04 Supply Chain**: `steamcmd`, `butler`, engine export templates, and CI runner images are external tooling in the release path. Mitigation: pin exact tool versions, verify checksums/provenance before use, and reject unpinned downloads.
- **ASI05 RCE Guard**: never interpolate untrusted values (branch names, channel tags, version strings) directly into `steamcmd` or `butler` command strings. Mitigation: validate all parameters against allowlist patterns before shell construction.
- **ASI07 Inter-Agent Communication**: release metadata is consumed by DevOps and store-operations roles for promotion decisions. Mitigation: emit the schema-valid `implementation-result.json` contract with version, channel, and integrity results so downstream roles act on validated state.
- **ASI09 Human-Agent Trust Exploitation**: never auto-promote a staging build to the live public branch. Mitigation: require explicit human confirmation for live promotion and surface failed gates honestly.

## Related Skills

- **integrate-game-engine**: headless engine export templates and cross-platform build profiles
- **profile-game-performance**: pre-release performance certification and bundle size validation
