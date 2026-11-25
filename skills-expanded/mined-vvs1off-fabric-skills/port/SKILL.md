---
name: port
description: Port the current Fabric mod to another Minecraft version and keep building and fixing until it compiles and starts.
argument-hint: "<target minecraft version>"
disable-model-invocation: true
---

# /fabric-skills:port - port this mod to Minecraft $ARGUMENTS

Port the mod in the current project to Minecraft **$ARGUMENTS**, following the
`fabric-version-porting` skill step by step. Use `fabric-mixins` for broken mixins and
`fabric-crash-debugging` for runtime failures.

If `$ARGUMENTS` is empty, ask for the target version. If it is "latest", resolve it to the latest
**stable** release from https://fabricmc.net/develop/ and confirm with the user.

## 0. Preconditions

- The working tree must be clean (`git status`). If not, ask the user to commit or stash.
- The project must build on its **current** version first (`./gradlew build`). If it does not,
  report that and ask whether to fix it before porting - porting a broken build hides causes.
- Create a branch: `git switch -c port/$ARGUMENTS`.

## 1. Analyse and plan (show the plan before editing)

Report to the user:

- Current Minecraft, Loader, Loom, Fabric API, Java, mappings (Yarn / Mojang / none).
- Target versions looked up from fabricmc.net/develop (never from memory).
- Whether a Yarn -> Mojang migration is required (target >= 26.1 and project uses Yarn).
- Third-party mod dependencies and whether each has a build for the target (check Modrinth).
- Number of mixins and which targets look risky (rendering, networking, entity ticking).
- Links to the relevant porting guide / Fabric blog post for the target.

Wait for the user's go-ahead if any dependency is missing or a mappings migration is needed.

## 2. Execute in separate commits

1. (If needed) Yarn -> Mojang mappings migration **on the old version**; build; commit.
2. Build-system bump (wrapper, `gradle.properties`, plugin id, dependency configurations,
   Java level, `fabric.mod.json` ranges); commit even if code does not compile yet only if the
   user prefers small commits - otherwise continue.
3. Fix compile errors, common code first, then client code. Look up every new name in the
   rename list or `./gradlew genSources` output; never guess.
4. Fix mixins: re-derive every target against the new sources.

## 3. Build loop

```bash
./gradlew build
```

Repeat: read the **first** error, fix its root cause, rebuild. If the same error survives two
attempts, stop guessing: read the relevant sources/docs again, and explain the blocker to the
user if it persists.

## 4. Runtime check

- `./gradlew runClient` and, unless the mod is client-only, `./gradlew runServer`. If you
  cannot run them interactively, at least start them long enough to pass mixin application and
  entrypoint initialization, and check `run/logs/latest.log` for mixin warnings and errors.
- List anything you could not verify.

## 5. Report

- Final versions, files changed, renames applied, mixins changed or removed (and why).
- Features that could not be ported, with reasons. Never drop a feature silently.
- Suggested `mod_version` bump and `CHANGELOG.md` entry (see `fabric-release`).
- Do not push or publish.
