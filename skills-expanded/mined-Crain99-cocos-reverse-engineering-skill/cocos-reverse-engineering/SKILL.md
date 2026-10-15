---
description: Reverse engineer Cocos Creator 2.x / 3.x game builds. Detect the engine version, decrypt XXTEA-encrypted .jsc scripts, recover settings/config metadata, rebuild the asset graph (scenes, prefabs, sprite frames, audio, animations, Spine, DragonBones) and emit an editable Cocos project. Use when the user wants to decompile, unpack, or inspect a compiled Cocos Creator game (H5, web-mobile, mini-game, native build).
trigger: reverse engineer cocos|decompile cocos creator|unpack cocos|cocos creator reverse|extract cocos assets|decrypt jsc|xxtea jsc|cc-reverse|cocos-js reverse|rebuild cocos project|cocos game reverse engineering|extract cocos sprites
---

# Cocos Creator Reverse Engineering

Recover the editable project (scripts + scenes + assets + meta) from a compiled Cocos Creator build. Supports **Cocos Creator 2.3.x / 2.4.x** (the `src/project.js` + `res/` layout and the `main.js` + `assets/` layout) and **Cocos Creator 3.x** (the `assets/main/` bundle layout with `config.json` + `import/` + `native/` + `cocos-js/`). Handles XXTEA-encrypted `.jsc` scripts via auto key extraction.

The workflow is driven by [`cc-reverse`](https://github.com/Crain99/cc-reverse), a Node.js CLI that this skill wraps and extends with engine detection and decryption helpers.

## Prerequisites

This skill requires **Node.js 16+** and the `cc-reverse` CLI installed. Run the dependency checker to verify:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/check-deps.sh
```

If anything is missing, follow `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/setup-guide.md`, or let the install helper handle it:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/install-dep.sh cc-reverse
```

## Workflow

### Phase 1: Verify and install dependencies

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/check-deps.sh
```

The output contains machine-readable lines:
- `INSTALL_REQUIRED:<dep>` — must be installed before proceeding (`node`, `cc-reverse`).
- `INSTALL_OPTIONAL:<dep>` — nice-to-have (`7z`, `unzip`, `ffmpeg` for audio format conversion).

If required dependencies are missing (exit code 1), install them:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/install-dep.sh <dep>
```

Re-run the check until everything passes. Do not proceed to Phase 2 until all required dependencies are OK.

### Phase 2: Detect the project layout

Cocos Creator ships three distinct build layouts. Before anything else, identify which one you're looking at — the rest of the workflow branches on this.

**Action**: Run the detector script.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/detect-project.sh <path-to-build>
```

It prints `ENGINE=<version>` (`2.3.x`, `2.4.x`, or `3.x`), followed by key paths (settings, bundles, script entry, asset roots, native dirs) and a list of encryption markers. Machine-readable keys:

- `ENGINE=` — detected engine series.
- `ENCRYPTED=yes|no` — are `.jsc` files present?
- `BUNDLES=<csv>` — detected bundle names (3.x only; `main,internal,resources,<subpackages>`).
- `WEB_MOBILE=yes|no` — is this the web-mobile build (has `index.html`)?

The detector looks at:
- `src/settings.js` + `src/project.js` + `res/` → **2.3.x**
- `main.js` + `settings.js` + `assets/` + optional `subpackages/` → **2.4.x**
- `index.html` + `data/` + `assets/main/config.json` + `cocos-js/` + `application.js` + `src/settings.json` → **3.x**
- Web-mobile games packed inside an `index.html` at the root also work — treat the build dir as the root.
- HTML5 builds from a ZIP/WAR need to be extracted first (use `unzip`/`7z`).

See `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/cocos2x-format.md` and `cocos3x-format.md` for detailed layout maps.

### Phase 3: Decrypt JSC (if encrypted)

If Phase 2 reported `ENCRYPTED=yes`, recover the XXTEA key and decrypt before the main reverse pass.

**Action**: Try auto-extraction first; fall back to manual key if the user has one.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/find-jsc-key.sh <path-to-build>
```

This greps `main.js`, `src/main.js`, `application.js`, and `cocos-js/` for known key patterns:
- `xxteaKey = "…"` / `encryptKey = "…"` / `XXTEA_KEY = "…"`
- `key: "<16+ hex>"` (Cocos 2.x default is a UUID-shaped string)
- In 3.x, search `src/settings.json` → `assets.encrypted` and `application.js` for the `xxteaKey` variable
- Keys embedded as arrays of bytes (`[0x61, 0x62, ...]`) — the script normalises these back to a string

Expected output: one or more `KEY=<value>` lines. If the key is obvious, `cc-reverse` will find it automatically too; the script is for confirmation and for the cases where cocos-engine ships it as a byte array.

If no key is found, ask the user — **don't guess**. Unauthorized decryption of encrypted game assets may be restricted by the software's licence.

Reference: `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/jsc-decryption.md`.

### Phase 4: Run the reverse pass

Drive `cc-reverse` to rebuild the project.

**Action**: Run the unpack wrapper, passing the key if one was found.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/unpack-cocos.sh [OPTIONS] <path-to-build>
```

Options:
- `-o <dir>` — output directory (default: `<build-name>-extracted`).
- `-k <key>` — XXTEA key (if Phase 3 produced one).
- `--version-hint 2.3.x|2.4.x|3.x` — force engine version when auto-detection fails.
- `--bundle <name>` — 3.x only; unpack a specific bundle (`main`, `internal`, `resources`, subpackage name). Default: all bundles.
- `--assets-only` — skip the script pass, only recover assets.
- `--scripts-only` — skip the asset pass, only recover scripts.
- `--verbose` — show per-file progress.

The wrapper runs `cc-reverse` under the hood and then:
1. Copies the recovered `assets/` tree into the output directory.
2. Generates a minimal editor-compatible `project.json` / `package.json` at the root so the result opens in Cocos Creator.
3. Writes a `RECOVERY_REPORT.md` listing engine version, bundle count, script count, and any assets that failed to decode.

For 3.x projects, each bundle is unpacked into its own subdir (`assets/main/`, `assets/resources/`, …) — matching the editor's folder layout when a project is re-imported.

See `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/cc-reverse-usage.md` for the full CLI reference and troubleshooting matrix.

### Phase 5: Inspect and catalogue assets

With the project recovered, navigate and document what's inside.

**Actions**:

1. **Read the entry point(s)**:
   - 2.x → `assets/Scripts/<main scene>.ts` (game bootstrap) and the first entry under `scenes` in `settings`.
   - 3.x → `assets/main/` scripts (bundled application) plus `scene/` for `.scene` files. Look at `application.js` / `settings.json` for the launch scene UUID.

2. **Survey the asset tree**:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/scripts/find-assets.sh <output>/assets
   ```
   Prints counts of each asset kind (Scene, Prefab, SpriteFrame, AudioClip, AnimationClip, Spine, DragonBones, Material, Mesh, EffectAsset, …) plus total size and any unrecognised file types.

3. **Map scene → prefab → component dependencies**. The `.fire`/`.scene` files reference prefabs and components by UUID; the recovered meta files list each asset's UUID. Trace from the scene root down.

4. **Identify third-party SDKs**. Cocos games commonly bundle analytics/ads SDKs (AppLovin, Unity Ads, Bugly, GameAnalytics). These usually sit in `assets/Scripts/` as large `.ts` files with recognisable API names.

See `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/asset-recovery-patterns.md` for library-specific search patterns and the asset documentation template.

## Output

At the end of the workflow, deliver:

1. **Recovered project** in the output directory, structured as a regular Cocos Creator project (`assets/`, `project.json`, per-asset `.meta`).
2. **Engine summary** — detected version, bundle count, encryption status, key (if any).
3. **Asset catalogue** — counts by type, total size, list of any assets that couldn't be decoded.
4. **Script inventory** — recovered `.ts`/`.js` files grouped by package prefix, with SDK dependencies called out.

## References

- `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/setup-guide.md` — installing Node, `cc-reverse`, and optional tools.
- `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/cc-reverse-usage.md` — `cc-reverse` CLI reference and `cc-reverse.config.js` options.
- `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/cocos2x-format.md` — 2.3.x and 2.4.x build layout, `CCSettings`, compressed-type array format, `res/` tree.
- `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/cocos3x-format.md` — 3.x build layout, bundle `config.json` schema, `import/`/`native/` paths, CCON and packed formats.
- `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/jsc-decryption.md` — XXTEA key locations, byte-array keys, gzip post-processing, why decryption sometimes fails.
- `${CLAUDE_PLUGIN_ROOT}/skills/cocos-reverse-engineering/references/asset-recovery-patterns.md` — grep patterns for scenes, prefabs, sprite frames, Spine, DragonBones, and the per-asset documentation template.
