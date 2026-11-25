name: coupon-java25-gradle-validation
description: Use when validating or triaging build, test, lint, or JDK issues in this coupon system. Covers `./gradlew`-first Java 25 validation, module selection, ktlintFormat before validation, and the smallest useful proof command for each module. Trigger on prompts about 빌드, 테스트, ktlint, lint, compile, validation, or Java 25.
metadata:
  short-description: Validate coupon-system changes with Java 25 and Gradle
---

# Coupon Java 25 Gradle Validation

Use this skill when you need the smallest validation command that proves a change is safe.

## Workflow

1. Read `./AGENTS.md` and [docs/agent/validation.md](../../../docs/agent/validation.md).
2. Prefer plain `./gradlew ...` commands.
3. If the Java environment is unclear, check `./gradlew -version` before adding `JAVA_HOME=...`.
4. Run the narrowest `ktlintFormat` task that matches the changed modules.
5. Choose the smallest validation command that exercises the changed behavior.
6. Escalate to the broader API build only when module-local checks are insufficient.

## Commands

- `./gradlew :coupon:coupon-domain:test`
- `./gradlew :storage:db-core:compileKotlin`
- `./gradlew :storage:redis:compileKotlin`
- `./gradlew :coupon:coupon-api:compileKotlin`
- `./gradlew :coupon:coupon-api:build --no-daemon`

If `./gradlew -version` shows a non-Java-25 launcher, rerun the same command with `JAVA_HOME=$(/usr/libexec/java_home -v 25)`.

## Resources

- [docs/agent/validation.md](../../../docs/agent/validation.md)
- [validation.md](./references/validation.md)
