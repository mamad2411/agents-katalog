---
tags: [backend, jacoco, exclude, boilerplate, layers]
name: jacoco-exclude-boilerplate-layers
description: Configure JaCoCo + SonarQube to exclude generated/boilerplate layers (avro, config, dto, entity, kafka, *Dev) from coverage so coverage % reflects business logic only
category: backend
version: 1.0.0
source_project: lucida-topology
source_commit: 8729ca3
trigger: Spring Boot / Gradle project using JaCoCo where coverage is diluted by generated Avro classes, config wiring, DTOs, and dev-only controllers
---

# jacoco-exclude-boilerplate-layers

## When to use
Your JaCoCo / SonarQube coverage number is being dragged down (or artificially inflated) by
classes that have no meaningful branches to test: generated Avro stubs, Spring `@Configuration`,
request/response DTOs, JPA/Mongo entities, Kafka listener shells, and dev-only controllers
(`*Dev.java`). Excluding them makes the coverage metric track business logic only.

## Steps

### 1. Identify boilerplate packages in your project

Common patterns:
- `**/avro/**` — generated schema classes
- `**/config/**` — Spring configuration
- `**/constants/**` — static string holders
- `**/dto/**` — request/response records
- `**/entity/**` — persistence models
- `**/kafka/**` — listener plumbing (exclude if logic lives in a service, not the listener)
- `**/monitor/**` — metrics/actuator hooks
- `**/*Dev.java` — dev-profile-only endpoints
- `**/Application.java` — main class

Adjust the list to your actual layout.

### 2. Add to `jacocoTestReport` in `build.gradle`

```gradle
jacocoTestReport {
    dependsOn test
    reports { html.required = true; xml.required = true }
    afterEvaluate {
        classDirectories.setFrom(
            files(classDirectories.files.collect {
                fileTree(dir: it, excludes: [
                    '**/avro/**',
                    '**/config/**',
                    '**/constants/**',
                    '**/dto/**',
                    '**/entity/**',
                    '**/kafka/**',
                    '**/monitor/**',
                    '**/*Dev.java',
                    '**/Application.java'
                ])
            })
        )
    }
    finalizedBy 'jacocoTestCoverageVerification'
}
```

### 3. Mirror the list in `jacocoTestCoverageVerification`

The verification task reads its own `excludes` — duplicate the list there or hoist to a
shared `ext.jacocoExcludes` variable.

### 4. Mirror again in SonarQube properties

```gradle
sonar {
    properties {
        property 'sonar.exclusions', ['**/avro/**', '**/config/**', ...]
        property 'sonar.coverage.exclusions', ['**/avro/**', '**/config/**', ...]
    }
}
```

Sonar uses *two* exclusion keys: `sonar.exclusions` removes files from analysis entirely,
`sonar.coverage.exclusions` keeps them in analysis but not in coverage math. Usually you want
both for boilerplate.

### 5. Verify

```bash
./gradlew clean test jacocoTestReport
open build/reports/jacoco/test/html/index.html
```

Confirm the excluded packages no longer appear. Coverage % should jump if boilerplate
dominated the codebase.

## Gotchas
- Trailing whitespace in exclusion globs (`'**/avro/** '`) silently matches nothing on some
  JaCoCo versions. Trim them.
- `**/*Dev.java` won't exclude Kotlin files — add `**/*Dev.kt` if applicable.
- If a "boilerplate" package contains a handwritten mapper with real branches, don't exclude
  the whole package — exclude by specific class.
- Keep the three lists (JaCoCo report, JaCoCo verification, Sonar) in sync. Drift is the most
  common defect here.
