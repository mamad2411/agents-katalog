# SpendSense — Android App

## Build & Install

```bash
./gradlew assembleDebug
/mnt/d/Apps/Android/Sdk/platform-tools/adb.exe install app/build/outputs/apk/debug/app-debug.apk

./gradlew assembleRelease
cp app/build/outputs/apk/release/app-release.apk /mnt/c/Users/vuong/Downloads/SpendSense.apk
```
Note: Adjust the `adb` path for your environment (e.g., `/mnt/d/Apps/Android/Sdk/platform-tools/adb.exe` on WSL with Windows).

## Project Structure

- **Platform:** Android (Kotlin, Jetpack Compose, Material 3)
- **Architecture:** Clean Architecture with Hilt DI, Room database
- **Modules:** Single-module Android app (`app/`)

## GitNexus — Code Intelligence

This project is indexed by GitNexus as **spend-sense** (1077 symbols, 2377 relationships, 73 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

### Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.

### CLI

| Task | Skill File |
|------|------------|
| Understand architecture | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius analysis | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Debug/tracing | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename/refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **spend-sense** (2226 symbols, 4676 relationships, 113 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/spend-sense/context` | Codebase overview, check index freshness |
| `gitnexus://repo/spend-sense/clusters` | All functional areas |
| `gitnexus://repo/spend-sense/processes` | All execution flows |
| `gitnexus://repo/spend-sense/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
