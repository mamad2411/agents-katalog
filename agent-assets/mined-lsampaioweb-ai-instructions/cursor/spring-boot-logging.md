---
description: "Spring Boot logging contract for Logback configuration, i18n-backed log messages, and logger usage."
globs: "**/src/main/resources/**/logback-spring.xml,**/src/main/resources/**/application*.yml,**/src/main/resources/**/application*.yaml,**/src/main/resources/**/application*.properties,**/src/**/*.java"
alwaysApply: false
---

# Spring Boot Logging Contract

## Logger acquisition

- Obtain a logger via Lombok's `@Slf4j` on the class (Lombok contract). Do not call
  `LoggerFactory.getLogger(...)` when Lombok is available.

## Log message content

- Externalize log message text through a dedicated logging message helper component
  backed by `MessageSource`, separate from any user-facing/API message resolution path.
- The logging message helper exposes:
  - `get(String key, Object... args)` - resolves the message in the configured default
    locale (English by default) for events without a request locale.
  - `get(Locale locale, String key, Object... args)` - resolves the message in the
    caller-supplied locale; use the request locale for request-scoped log events.
- Prefix every logging-helper key with `log.`. Include each logging key in every locale
  bundle and translate its value for that locale, preserving placeholder arity.
- Never hardcode log message text directly in a log call; always resolve it through the
  logging message helper and an externalized message key.
- Use the request locale explicitly for request-scoped log events and the configured
  default locale for startup, background, or other events without a request locale. Do
  not rely on the JVM default locale or implicit locale state.

## Structured log fields

- When more than one log statement records outcomes of the same logical event (for
  example, a success audit line and a rejection audit line for the same operation),
  give every one of them the same field schema, in the same order. Do not include a
  field (such as an error code) in one code path and drop it in another for the same
  conceptual event.
- Leave a field present but empty when it does not apply to a given outcome, instead
  of omitting the placeholder; this keeps field position and count stable for
  `grep`/`awk`-based log analysis.
- When adding, removing, or renaming a field on a shared structured log message key,
  update every call site that uses that key, not only the one being changed.

## Guarded logging

- Do not wrap ordinary log calls in `isXEnabled()` checks by default.
- Only guard a log call when both are true: the log level is one commonly disabled in
  production (`TRACE` or `DEBUG`), and computing the log arguments does non-trivial work
  (e.g., a message-resolution lookup, string building, or serialization) that would
  otherwise run even when the level is disabled.
- Never guard `INFO`, `WARN`, or `ERROR` calls; these levels are normally always enabled.
- Prefer SLF4J parameterized logging with the resolved message and arguments over
  string concatenation so cheap arguments avoid unnecessary evaluation without
  needing a guard.

## Logback configuration

- Place `logback-spring.xml` at `src/main/resources/log/` and reference
  it with `logging.config` set to `classpath:log/logback-spring.xml`. Do not configure
  logging inline in `application.yml`.
- Bind the application name and log directory through `springProperty` so the
  configuration adapts to `spring.application.name` and `logging.file.path`.
- Externalize rolling-file thresholds (max file size, max history, total size cap)
  through `springProperty` bindings sourced from
  `logging.logback.rollingpolicy.max-file-size`,
  `logging.logback.rollingpolicy.max-history`, and
  `logging.logback.rollingpolicy.total-size-cap`, with sensible defaults, rather than
  hardcoding those values in the rolling policy. Do not use the deprecated
  `logging.file.max-size`, `logging.file.max-history`, or `logging.file.total-size-cap`
  keys (renamed since Spring Boot 2.4).
- Declare matching values for `logging.logback.rollingpolicy.max-file-size`,
  `logging.logback.rollingpolicy.max-history`, and
  `logging.logback.rollingpolicy.total-size-cap` in `application.yml` whenever a
  project overrides the defaults.
- Define at least three profile-based root logging configurations. The verbose profile
  name may be `debug`: that is a **logging verbosity** profile, not an environment alias
  for `development`/`production` (configuration contract):
  - A verbose profile (e.g. `debug`) at `DEBUG` level writing to both console and file.
  - A development profile at `INFO` level writing to both console and file.
  - A default profile at `INFO` level writing to both console and file.
  - A production profile at `INFO` level writing to file only.
- Define an appender inside a `<springProfile>` block when that appender is used only
  by selected profiles. Scope a console appender to the profiles that reference it
  (typically `default | debug | development`) so file-only profiles do not create an unused
  appender and emit a Logback warning.
- Ensure every `<appender-ref>` is resolvable in every active profile where it appears.
  An appender declared inside a profile expression is not available to other profiles.
- Keep the `production` root configuration separate from console-enabled profiles when
  production is file-only. Include `default` in the console appender declaration when
  the default profile is intentionally console-enabled.
- Route the file appender through an async appender to move file I/O off the calling
  thread during normal operation. This does not guarantee non-blocking behavior when
  the queue is full.
- Configure the async appender with an explicit queue size and a `discardingThreshold`
  of `0` so lower-severity log events are not discarded by the queue-pressure threshold
  while the appender is running; the default
  discarding-threshold behavior can drop lower-severity events once the queue fills,
  which is unacceptable for an audit/troubleshooting trail.
- Set `neverBlock` explicitly to `false`. When the queue is full, the producer waits
  for the appender to make space instead of silently losing the event. This deliberately
  prioritizes log preservation over request throughput during sustained logging pressure.
- Define and verify an orderly shutdown/flush policy for production deployments. The
  queue-pressure policy does not guarantee that events still queued during an abrupt
  process termination will be written.
- Keep console and file encoder patterns consistent in structure (timestamp, level,
  thread, logger name, message, throwable), and keep the XML element name for the pattern
  encoder consistent (lowercase) across the whole project.

## Message source configuration

- Whenever a project resolves messages by key, declare the full `spring.messages`
  block required by the i18n contract (`basename`, `encoding`, `default-locale`,
  `fallback-to-system-locale`). Do not configure basename alone.

## Forbidden

- Never place `logback-spring.xml` anywhere except
  `src/main/resources/log/logback-spring.xml`.
- Never omit or leave untranslated a logging-helper message value in a locale bundle.
- Never hardcode log message strings inline instead of resolving them through the
  logging message helper.
- Never guard `INFO`/`WARN`/`ERROR` log calls with `isXEnabled()` checks.
- Never hardcode rolling-file size/history/cap values directly in `logback-spring.xml`
  when they can be externalized through `application.yml`.
- Never use the deprecated `logging.file.max-size`, `logging.file.max-history`, or
  `logging.file.total-size-cap` keys; use `logging.logback.rollingpolicy.*` instead.
- Never omit the `discardingThreshold` setting on an async file appender.
- Never omit the `neverBlock` setting on an async file appender; use `false` for the
  log-preserving policy defined above.
- Never ship a project without all three logging profiles (verbose, development,
  default/production) defined.
- Never give two log statements for the same audited event different field schemas.
