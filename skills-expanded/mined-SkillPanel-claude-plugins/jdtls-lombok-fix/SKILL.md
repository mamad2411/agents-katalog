---
name: jdtls-lombok-fix
description: Use when JDTLS diagnostics show false-positive Lombok errors — `log cannot be resolved` (@Slf4j), `builder() is undefined` (@Builder), `getX() is undefined` (@Getter/@Data), `blank final field may not have been initialized` (@RequiredArgsConstructor) — especially inside `<new-diagnostics>` reminders in Java projects. Root cause: Claude Code's `jdtls-lsp` plugin launches JDTLS without Lombok's javaagent (anthropics/claude-plugins-official#1000). Trigger proactively even without an explicit request. Do NOT trigger when `mvn compile`/`gradle build` also reports the same errors — those are real.
---

# jdtls-lombok-fix

Claude Code's `jdtls-lsp` plugin starts Eclipse JDT LS without the Lombok
javaagent. Lombok's compile-time magic (`@Slf4j`, `@Getter`, `@Builder`,
`@RequiredArgsConstructor`, `@Data`, …) never gets applied inside JDTLS, so
every Lombok-using class lights up with false errors in the language server's
diagnostics — while Maven/Gradle compile just fine because they have Lombok
on the annotation-processor path.

The noise is indistinguishable from real compile errors unless you know the
fingerprint, and it distracts from actual code review. This skill applies the
workaround documented in
<https://github.com/anthropics/claude-plugins-official/issues/1000>:
patch the official plugin marketplace's `marketplace.json` so that `jdtls-lsp`
starts JDTLS with `--jvm-arg=-javaagent:<lombok.jar>`.

## Preconditions

Run this ONLY when both are true:

1. You've seen one or more diagnostics matching the Lombok fingerprint below.
2. The build tool is not also reporting those errors. If you haven't run a
   build recently, run the project's normal build command (`./mvnw compile`,
   `./gradlew compileJava`, etc.) and confirm it succeeds. If it fails, the
   errors are real — do NOT apply this patch; fix the code instead.

### Lombok fingerprint

| Diagnostic message                                                    | Likely annotation                     |
|-----------------------------------------------------------------------|---------------------------------------|
| `log cannot be resolved` (often JDT code `[570425394]`)               | `@Slf4j`, `@Log4j2`, `@Log`, `@CommonsLog` |
| `The method builder() is undefined for the type X`                    | `@Builder`, `@SuperBuilder`           |
| `The method getX() / setX() is undefined for the type Y`              | `@Getter`, `@Setter`, `@Data`, `@Value` |
| `The blank final field X may not have been initialized` (`[33554513]`)| `@RequiredArgsConstructor`, `@AllArgsConstructor`, `@Data` |
| `The constructor X(...) is undefined`                                 | `@RequiredArgsConstructor`, `@AllArgsConstructor`, `@NoArgsConstructor` |
| `The method toBuilder() is undefined`                                 | `@Builder(toBuilder=true)`            |

The fingerprint is cumulative — one hit is suggestive, two or more across
different files is near-certain.

## Procedure

1. Run the idempotent patch script. It handles all cases internally (already
   patched, missing jar, missing plugin) and prints a single status line.

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/jdtls-lombok-fix/scripts/apply_patch.py"
   ```

2. Interpret the output:

   | Output                         | Meaning / next step                                                                                                   |
   |--------------------------------|-----------------------------------------------------------------------------------------------------------------------|
   | `already-patched`              | Nothing to do. The current diagnostic noise may have a different cause — investigate without this skill.              |
   | `patched: <path-to-lombok.jar>`| Patch applied. Tell the user to restart the Claude Code session (or reload the window) so JDTLS picks up the javaagent. Also warn them that plugin updates overwrite this patch — issue #1000 tracks the upstream fix. |
   | `no-lombok-jar`                | No Lombok jar in `~/.m2/repository/org/projectlombok/lombok/*/`. Ask the user to run `./mvnw dependency:resolve` (or equivalent) so Maven populates the local repo, then rerun the skill. |
   | `marketplace-missing`          | The `jdtls-lsp` plugin isn't installed in the expected location. Skip — nothing to patch. Mention this to the user so they can install the plugin if they want Java LSP support. |
   | `marketplace-invalid: <err>`   | The marketplace JSON failed to parse. Don't improvise — surface the raw error to the user and point at the timestamped `marketplace.json.bak-*` backup next to the original. |

   If the output doesn't match one of these rows, stop and surface the raw
   output to the user instead of improvising a fix.

## Scope

- Targets the `jdtls-lsp` plugin bundled with Claude Code's official
  marketplace. If the user uses a different Java LSP (e.g. a custom LSP
  config in their own `settings.json`), the fix path is different — don't
  use this skill blindly; tell them about the `--jvm-arg` flag and let them
  wire it up.
- Does NOT fix other JDTLS gaps (e.g. missing Kotlin support, MapStruct,
  Spring native image). The fingerprint check keeps it from overreaching.
