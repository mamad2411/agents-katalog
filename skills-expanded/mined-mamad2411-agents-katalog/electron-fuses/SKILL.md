---
name: electron-fuses
description: >
  Electron fuses hardening for owned release binaries: flip and verify RunAsNode,
  node options, embedded asar integrity, cookie encryption, and related fuse bits
  at package time. Use when @electron/fuses, electron-builder electronFuses, or
  post-build fuse inspection. Complements electron-asarsecurity and app security.
---

# Electron Fuses

## Scope And Authorization

- **In scope:** Build pipelines and release artifacts for Electron apps you control.
- **Out of scope:** Patching fuses on third-party applications users did not authorize you to modify.
- Fuses are **build-time** hard switches—test thoroughly before shipping; wrong flips break support tooling.
- Keep CI signing and fuse steps auditable.
- Pair with `electron-asarsecurity` and `electron-app-security`.

## When To Use

- Shipping production installers and need defense-in-depth beyond webPreferences.
- Disabling `ELECTRON_RUN_AS_NODE` style abuse and dangerous CLI option inheritance.
- Enabling asar integrity validation fuses.
- Verifying that published binaries actually have fuses flipped (not only config claimed).
- Aligning electron-builder/forge with `@electron/fuses` for your Electron major.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Isolation / preload design | `electron-context-isolation` |
| asar packaging details | `electron-asarsecurity` |
| Overall Electron review | `electron-app-security` |
| Implementation quality baseline | `code-quality-standards` |
| Code signing certificates | platform signing process |

## Domain Focus

| Area | Guidance |
| --- | --- |
| RunAsNode | Disable so binary cannot be reused as Node with app privileges |
| CLI options | Restrict node/inspect options according to current fuse set |
| asar | Enable integrity + only-load-from-asar when packaging allows |
| Cookies | Enable encrypted cookies storage fuse when available |
| Verify | Inspect **built** executable; config-only is insufficient |
| Version | Fuse names change—read docs for your Electron version |

## Workflow

### 1. Confirm scope and success criteria

1. Electron version, packager, OS targets (Windows/macOS/Linux).
2. Success: release checklist includes fuse dump; dangerous fuses off; app still starts and updates.

### 2. Inventory current fuse state

```bash
# After a local pack, inspect (tooling evolves—prefer official @electron/fuses flipFuses dump)
npx @electron/fuses read --app path/to/YourApp.app 2>/dev/null || true
rg -n "fuses|flipFuses|electronFuses" package.json electron-builder.* forge.config.*
```

1. Note any fuse currently left open for debugging (e.g. runAsNode in internal builds only).
2. Separate **dev** vs **prod** fuse profiles.

### 3. Baseline risk without fuses

| Abuse | Without fuse hardening |
| --- | --- |
| Run as Node | Adversary runs arbitrary JS with app’s file/identity access |
| Inspect flags | Easier runtime instrumentation of production |
| Loose asar | Swap or dual-load application code |
| Plain cookies | Session theft from disk easier |

### 4. Flip fuses in the build

```js
// Illustrative post-pack step using @electron/fuses — match API to your major
const { flipFuses, FuseVersion, FuseV1Options } = require('@electron/fuses');

await flipFuses(pathToElectronBinary, {
  version: FuseVersion.V1,
  [FuseV1Options.RunAsNode]: false,
  [FuseV1Options.EnableCookieEncryption]: true,
  [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
  [FuseV1Options.EnableNodeCliInspectArguments]: false,
  [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
  [FuseV1Options.OnlyLoadAppFromAsar]: true,
});
```

```yaml
# electron-builder may support electronFuses map — verify against current builder docs
electronFuses:
  runAsNode: false
  enableCookieEncryption: true
  enableNodeOptionsEnvironmentVariable: false
  enableNodeCliInspectArguments: false
  enableEmbeddedAsarIntegrityValidation: true
  onlyLoadAppFromAsar: true
```

1. Apply fuses **after** packaging the correct Electron binary for each arch.
2. Do not flip prod fuses on developer local `electron .` workflows if it blocks debugging—use separate channels.
3. Re-sign macOS/Windows binaries **after** fuse modification if required by the platform.

### 5. CI gate

1. Build → flip → sign → **read back** fuses → fail job if mismatch.
2. Store fuse dump as a release artifact.
3. Block publish when integrity fuses are false on prod channel.

### 6. Verify with evidence

```bash
# Expect RunAsNode disabled: launching with ELECTRON_RUN_AS_NODE should not yield node behavior
# (exact test varies by OS; document observed behavior in release QA)
npx @electron/fuses read --app dist/YourApp.app
```

1. Smoke test installers on each OS.
2. Auto-update path still works with integrity fuses on.
3. Support tooling that needed inspect must use separate **debug** builds, not prod.

### 7. Hand off

1. Document fuse matrix per channel (internal/beta/prod).
2. Owner for Electron upgrades that rename fuses.
3. Link asar skill for packaging prerequisites.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Prod fuses | RunAsNode off, integrity on | Defaults left open “for support” |
| Verification | Read fuses from artifact | Trust YAML only |
| Channels | Debug build vs prod build | One binary for all |
| Signing | Sign after flip if needed | Fuse flip invalidates signature unnoticed |
| Docs | Version-pinned fuse names | Copy-paste from old blog |

## Output Checklist

- [ ] Electron version and fuse API version recorded
- [ ] Prod fuse matrix defined and justified
- [ ] Build pipeline flips fuses per arch
- [ ] Read-back verification in CI
- [ ] Re-sign step correct for each OS
- [ ] Smoke tests on fused artifacts
- [ ] Debug channel documented separately
- [ ] Residual risk noted

## Rules

- Only modify binaries you own.
- Fuses are irreversible for that artifact—test before wide release.
- Never disable integrity fuses silently in hotfixes without security sign-off.
- Keep this skill focused on fuse bits; isolation/asar content have dedicated skills.
- Cite observed `fuses read` output as evidence.
