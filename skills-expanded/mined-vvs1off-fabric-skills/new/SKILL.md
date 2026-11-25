---
name: new
description: Scaffold a new Minecraft Fabric mod project (asks for name, mod id, Minecraft version and whether it is client-only, then generates a project that builds).
argument-hint: "[mod name]"
disable-model-invocation: true
---

# /fabric-skills:new - scaffold a new Fabric mod

Create a new, buildable Fabric mod. Follow the `fabric-project-setup` skill for every file you
write; this command only decides the order and asks the questions.

## 1. Ask, then confirm

Ask the user for (use `$ARGUMENTS` as the mod name if it was given):

1. **Mod name** (display name, e.g. "Better Pings").
2. **Mod id** - propose one derived from the name (lowercase, `a-z0-9_-`, starts with a letter,
   2-64 chars, e.g. `betterpings`) and let the user accept or change it.
3. **Java package** - propose `com.example.<modid>` (strip `-`/`_`); remind them to use a domain
   or `io.github.<username>` they actually control.
4. **Minecraft version** - default to the latest **stable** release (see step 2). Mention if the
   chosen version is before 26.1 (Yarn/remapping era) and what that implies.
5. **Client-only?** (HUD/minimap/QoL mods: yes; anything adding blocks, items, entities or
   gameplay rules: no).
6. **Target directory** - default `./<modid>`; refuse to write into a non-empty directory
   without explicit confirmation.

Show a one-screen summary and wait for confirmation before writing files.

## 2. Look up versions (do not use remembered numbers)

- https://fabricmc.net/develop/ for Loader, Loom and Fabric API matching the Minecraft version.
- `https://meta.fabricmc.net/v2/versions/game` (stable flag) and `/v2/versions/loader`.
- https://github.com/FabricMC/fabric-example-mod for the current `build.gradle`, Java release
  and Gradle wrapper version.

If the network is unavailable, stop and tell the user; do not invent versions.

## 3. Generate

Prefer copying the Gradle wrapper (`gradlew`, `gradlew.bat`, `gradle/wrapper/*`) from the
official fabric-example-mod (or running `gradle wrapper --gradle-version <v>` if Gradle is
installed). Never write `gradle-wrapper.jar` by hand.

Then write, per `fabric-project-setup`:

- `settings.gradle`, `gradle.properties`, `build.gradle` for the right era
  (26.1+: `net.fabricmc.fabric-loom`, no mappings; older: `net.fabricmc.fabric-loom-remap` +
  `loom.officialMojangMappings()`).
- `splitEnvironmentSourceSets()` always.
- `src/main/resources/fabric.mod.json` with `"environment": "client"` for client-only mods.
- Entrypoints: a `main` `ModInitializer` for normal mods; client-only mods may have only the
  `client` entrypoint.
- Mixin config(s) with **no mixins yet** (`"mixins": []`), `defaultRequire: 1`, and the right
  `compatibilityLevel`. Do not add example mixins the user did not ask for.
- `assets/<modid>/lang/en_us.json`. Only add `"icon"` to `fabric.mod.json` if you actually
  create `assets/<modid>/icon.png` (e.g. the user provides one); otherwise omit the field and
  tell the user how to add an icon later. Never reference files that do not exist.
- `.gitignore` (at least `.gradle/ build/ run/ out/ .idea/ *.iml .vscode/ logs/ crash-reports/
  .env *.key *.jks`) and `.gitattributes` (`gradlew text eol=lf`, `*.bat text eol=crlf`).
- A short `README.md` and, if the user wants, a `LICENSE` (ask which one; do not assume).

Use `YOUR_NAME` placeholders for authors/URLs unless the user gives real values.

## 4. Verify

```bash
./gradlew build
```

Fix every error until it passes. Report the build result honestly. Offer (do not auto-run)
`./gradlew runClient` as the next step, and `git init` if the directory is not a repository.

## Done when

- `./gradlew build` succeeds.
- `fabric.mod.json` id == `loom.mods` key == `MOD_ID` == `assets/<modid>`.
- No hardcoded versions came from memory; no credentials or personal paths in any file.
