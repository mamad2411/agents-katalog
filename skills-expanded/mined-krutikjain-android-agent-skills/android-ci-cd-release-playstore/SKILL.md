---
name: "android-ci-cd-release-playstore"
description: "Automate Android CI, versioning, signing boundaries, release channels, and Play-ready delivery workflows."
metadata:
  version: "0.1.0"
  category: "quality-release"
  tags: ["android", "ci", "cd", "release"]
  triggers:
    include: ["android ci cd pipeline", "play store release automation", "android signing and release", "canary stable release android", "github actions android build"]
    exclude: ["compose semantics only", "fragment back stack only", "datastore migration only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android CI CD Release PlayStore

## When To Use
- Use this skill when the request is about: android ci cd pipeline, play store release automation, android signing and release.
- Primary outcome: Automate Android CI, versioning, signing boundaries, release channels, and Play-ready delivery workflows.
- Handoff skills when the scope expands:
- `android-gradle-build-logic`
- `android-security-best-practices`

## Workflow
1. Scope the risk surface: correctness, security, performance, test depth, or release automation.
2. Pick the narrowest verification strategy that still catches the likely regressions.
3. Instrument the workflow so failures are actionable rather than just red.
4. Run the relevant checks on the showcase apps and packaging outputs.
5. Capture any residual risk with explicit follow-up work and owner skills.

## Guardrails
- Prefer reproducible checks in CI over one-off local heroics.
- Fail with a precise remediation path instead of a vague quality gate.
- Keep secrets, signing material, and production credentials out of examples and fixtures.
- Treat performance and security work as engineering tasks with evidence, not folklore.

## Anti-Patterns
- Adding more tests without increasing signal.
- Shipping benchmarks or security scans that no one can reproduce.
- Hard-coding release credentials into build logic.
- Using synthetic metrics with no user-impact interpretation.

## Examples
### Happy path
- Scenario: Validate the repo CI workflow, adapter generation, and version metadata flow.
- Command: `python3 scripts/validate_repo.py`

### Edge case
- Scenario: Check canary and stable release script behavior before tagging.
- Command: `python3 scripts/release.py --channel canary --dry-run`

### Failure recovery
- Scenario: Avoid routing pure build-logic or security work into release automation.
- Command: `python3 scripts/eval_triggers.py --skill android-ci-cd-release-playstore`

## Done Checklist
- The implementation path is explicit, minimal, and tied to the right Android surface.
- Relevant example commands and benchmark prompts have been exercised or updated.
- Handoffs to adjacent skills are documented when the request crosses boundaries.
- Official references cover the chosen pattern and the main migration or troubleshooting path.

## Official References
- [https://developer.android.com/build/build-for-release](https://developer.android.com/build/build-for-release)
- [https://developer.android.com/studio/publish](https://developer.android.com/studio/publish)
- [https://developer.android.com/studio/publish/app-signing](https://developer.android.com/studio/publish/app-signing)
- [https://developer.android.com/google/play/publishing/multiple-apks](https://developer.android.com/google/play/publishing/multiple-apks)
