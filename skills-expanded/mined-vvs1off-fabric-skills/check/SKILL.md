---
name: check
description: Audit the current Fabric mod project (fabric.mod.json, build setup, dependencies, mixins, client/server separation, secrets) and output a prioritized report.
argument-hint: "[path to mod project]"
disable-model-invocation: true
---

# /fabric-skills:check - audit this Fabric mod

Audit the Fabric mod in `$ARGUMENTS` (or the current directory if empty). **Read-only**: do not
modify files. Produce a report; offer fixes afterwards.

Use the checklists from `fabric-project-setup`, `fabric-mixins`, `fabric-networking` and
`fabric-release`. For a deep mixin review, delegate to the `mixin-reviewer` agent.

## What to inspect

### 1. Era and versions
- `gradle.properties`, `build.gradle`, `settings.gradle`, wrapper version.
- Era: 26.1+ (plugin `net.fabricmc.fabric-loom`, no `mappings`) vs older (remap plugin +
  Yarn/Mojang mappings). Flag mixtures (e.g. a `mappings` line on 26.1+, `modImplementation` with
  non-remapping Loom, `implementation` for mods with remapping Loom).
- Compare versions with https://fabricmc.net/develop/ for that Minecraft version, if reachable;
  report outdated Loader/Fabric API/Loom (informational, not an error). When mentioning newer
  Minecraft versions, check whether they are **releases or snapshots** (Mojang's
  `version_manifest_v2.json` `latest.release`, or `stable` in meta.fabricmc.net); Fabric API
  Maven metadata also lists snapshot builds and must not be reported as a release.
- `-SNAPSHOT` / `+` dynamic versions (e.g. `loom_version=1.19-SNAPSHOT`) make builds
  non-reproducible; suggest pinning for release builds.
- Java release consistency: `options.release`, `sourceCompatibility`, mixin
  `compatibilityLevel`, `fabric.mod.json` `"java"`.

### 2. fabric.mod.json
- Valid JSON, `schemaVersion: 1`, id format, `"version": "${version}"` with
  `processResources` expansion.
- id matches `loom.mods`, `MOD_ID`, `assets/<id>/`, mixin config names.
- Every entrypoint class exists at that FQCN and implements the right interface
  (`ModInitializer`, `ClientModInitializer`, `DedicatedServerModInitializer`, `ModMenuApi`).
- `environment` matches reality (client-only mod with server code, or vice versa).
- `depends`: `minecraft` range not `"*"` and matches `minecraft_version`; `fabricloader`,
  `java`, `fabric-api` present when used. Optional integrations in `suggests`/`recommends`,
  not `depends`.
- Every mixin config listed exists; client configs have `"environment": "client"`.
- The `icon` path (if set) exists under `src/*/resources`.
- `accessWidener` file exists and is also set in `loom.accessWidenerPath`.

### 3. Client/server separation
- Is `splitEnvironmentSourceSets()` enabled? If not, flag as high severity for non-client-only
  mods.
- Search common code for client-only references:
  `grep -rnE "net\.minecraft\.client\.|com\.mojang\.blaze3d|ClientPlayNetworking|MinecraftClient|KeyMapping|KeyBinding" src/main`
- Client mixin targets (`net.minecraft.client.*`) listed in a common mixin config.
- Payload types registered only in a client initializer.

### 4. Mixins
- List every mixin class, its target and injector types.
- Flag: `@Overwrite`, `@Redirect`, `cancellable` HEAD injections on hot methods, `ordinal`,
  missing `@Unique`/mod-id prefixes, `defaultRequire: 0` or `require = 0`, mixins that could be
  a Fabric API event, non-mixin classes in mixin packages.
- For more than a few mixins, run the `mixin-reviewer` agent and include its findings.

### 5. Networking (if present)
- Payloads use the API generation matching the version; types registered in common init.
- Server receivers validate input (ranges, distance, entity existence, permissions).

### 6. Security and hygiene
- No secrets: grep for `token`, `secret`, `password`, `api_key`, `MODRINTH`, `CURSEFORGE` with
  values in tracked files; no `.env`, keystores, `*.key`.
- `.gitignore` covers `build/ .gradle/ run/ out/ .idea/ logs/ crash-reports/`.
- Gradle wrapper present and committed; `gradlew` has LF line endings.
- Release workflow (if any) uses `${{ secrets.* }}` only, minimal `permissions`, pinned actions.

### 7. Build
- Run `./gradlew build` (this writes only to `build/`) and include the result. If it fails, put
  the first error in the report.

## Report format

```
# Fabric mod audit - <mod name> (<mod id>)
Minecraft <v> | Loader <v> | Fabric API <v> | Loom <v> (<plugin id>) | Java <n> | Mappings <...>
Build: PASS / FAIL (<first error>)

## Critical (will crash or break)
- [file:line] problem -> fix

## Warnings (fragile, incompatible, or wrong-era)
- ...

## Suggestions
- ...

## Looks good
- short list of things checked and fine
```

Rank by severity; cite `file:line` for every finding; give a concrete fix for each. End by
asking which findings the user wants fixed.
