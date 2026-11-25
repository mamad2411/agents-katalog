---
name: "android-local-persistence-datastore"
description: "Persist lightweight user and app preferences with DataStore, schema-safe models, and migration-aware defaults."
metadata:
  version: "0.1.0"
  category: "data-platform"
  tags: ["android", "datastore", "preferences", "local-storage"]
  triggers:
    include: ["android datastore setup", "replace sharedpreferences android", "typed local preferences android", "datastore migration", "persist user toggle android"]
    exclude: ["room relation only", "compose focus order", "agp compatibility only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Local Persistence DataStore

## When To Use
- Use this skill when the request is about: android datastore setup, replace sharedpreferences android, typed local preferences android.
- Primary outcome: Persist lightweight user and app preferences with DataStore, schema-safe models, and migration-aware defaults.
- Handoff skills when the scope expands:
- `android-room-database`
- `android-modernization-upgrade`

## Workflow
1. Confirm the data source, persistence boundary, sync model, and device capability involved.
2. Model contracts explicitly before wiring network, storage, media, or background APIs.
3. Apply the recommended AndroidX or platform pattern with migration-safe defaults.
4. Validate offline, retry, and process death behavior against the sample apps and scenarios.
5. Escalate security, performance, or release risk to the linked supporting skills when needed.

## Guardrails
- Prefer typed models and explicit serializers over ad-hoc maps or bundles.
- Keep background work idempotent and cancellation-aware.
- Do not leak storage, media, or networking details into presentation code.
- Treat user data durability, privacy, and migration paths as part of the implementation.

## Anti-Patterns
- Blocking the main thread with disk or network calls.
- Treating retryable sync failures as terminal user-facing errors.
- Mixing cache models and wire models without a mapping layer.
- Requesting broad storage or notification capabilities when a narrower API exists.

## Examples
### Happy path
- Scenario: Store reminder and filter preferences for OrbitTasks safely.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:testDebugUnitTest`

### Edge case
- Scenario: Migrate old preference keys without breaking the XML fixture.
- Command: `cd examples/orbittasks-xml && ./gradlew :app:testDebugUnitTest`

### Failure recovery
- Scenario: Avoid mixing lightweight preference storage requests with Room persistence work.
- Command: `python3 scripts/eval_triggers.py --skill android-local-persistence-datastore`

## Done Checklist
- The implementation path is explicit, minimal, and tied to the right Android surface.
- Relevant example commands and benchmark prompts have been exercised or updated.
- Handoffs to adjacent skills are documented when the request crosses boundaries.
- Official references cover the chosen pattern and the main migration or troubleshooting path.

## Official References
- [https://developer.android.com/topic/libraries/architecture/datastore](https://developer.android.com/topic/libraries/architecture/datastore)
- [https://developer.android.com/codelabs/android-preferences-datastore](https://developer.android.com/codelabs/android-preferences-datastore)
- [https://developer.android.com/training/data-storage/shared-preferences](https://developer.android.com/training/data-storage/shared-preferences)
- [https://developer.android.com/topic/libraries/architecture/datastore#proto-datastore](https://developer.android.com/topic/libraries/architecture/datastore#proto-datastore)
