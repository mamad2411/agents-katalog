---
name: apple-dev-conductor
description: Orchestrator for the swift-tothemax plugin — routes any Apple-platform development task (building an iOS/macOS app, adding a feature, preparing a release, fixing a rejection) to the right combination of skills in the correct order. Use this skill FIRST whenever a task spans more than one facet of Apple development — e.g. "build me an app that…", "get my app ready for the App Store", "add a subscription", "my app was rejected", "audit my app" — or when unsure which Swift/Apple skill applies. It coordinates swift-language, swiftui-max, apple-hig-ux, app-review-max, apple-legal-max, and apple-release-ops, plus well-known ecosystem skills when installed.
---

# Apple Dev Conductor

You are orchestrating a suite of skills that each own one facet of Apple-platform development. Your job: decompose the task into facets, invoke the right skills in the right order, and keep their outputs consistent.

## The suite (this plugin)

| Skill | Owns | Typical trigger |
|---|---|---|
| `swift-language` | Swift 6.x language, concurrency, performance, SwiftPM, interop, testing | any Swift code |
| `swiftui-max` | SwiftUI implementation: state, layout, animation, platform integration | building UI |
| `apple-hig-ux` | Design judgment: HIG, platform idioms, accessibility, "feels native" | designing screens/flows, UX review |
| `app-review-max` | Passing App Review: rejection playbook, QC checklist, monetization compliance | submission, rejection, IAP rules |
| `apple-legal-max` | Legal & privacy: manifests, nutrition labels, ATT, GDPR/COPPA/DMA, documents | privacy/legal anything |
| `apple-release-ops` | Shipping mechanics: signing, TestFlight, App Store Connect, CI/CD | build/upload/release |
| `ui-crawler-max` | Autonomous UI crawl: explore every screen, capture errors/crashes with repro steps, Haiku data labeling | "test the app", QA sweep, "find crashes" |

## Lifecycle routing

Work through stages in order; skip stages the task doesn't touch. At each stage read the named skill's SKILL.md and follow it.

1. **Shape** — what are we building? → `apple-hig-ux` (platform idioms, navigation pattern, screen patterns).
2. **Architect & build** — `swift-language` (types, concurrency, data flow) + `swiftui-max` (views, state). These two always load together for app code: language owns everything below the view layer.
3. **Feature compliance gates (do EARLY, not at submission):**
   - Collects data / has accounts / tracking / kids / subscriptions? → `apple-legal-max` (privacy manifest, labels, required documents) and `app-review-max` → `references/monetization-compliance.md` for anything paid.
   - Account creation ⇒ account deletion (5.1.1(v)); tracking ⇒ ATT; these are cheaper to design in than retrofit.
4. **Quality pass** — `apple-hig-ux` → `references/accessibility.md` audit; `swift-language` review checklist; tests per `swift-language` → `references/testing.md`; then a `ui-crawler-max` sweep — crawl every screen, harvest console errors/crashes/unlabeled controls, and feed the findings back to `swiftui-max` (implementation), `apple-hig-ux` (design/accessibility), or `swift-language` (logic) for fixes.
5. **Ship** — `apple-release-ops` (signing, TestFlight, CI) then `app-review-max` → `references/submission-checklist.md` as the final gate.
6. **Rejected / incident** — `app-review-max` → `references/rejection-playbook.md`; crash spikes → `apple-release-ops`.

## Ecosystem companions (use when installed, suggest when not)

Check the available-skills list for these before working; they deepen specific facets. If one is present, prefer its specialized workflow for that sub-task and keep this plugin's skills for current-2026 facts and cross-facet flow.

| If installed | Delegate | Pairs with |
|---|---|---|
| `swiftui-expert-skill` (avdlee) / `swiftui-pro` (twostraws) | deep SwiftUI review, Instruments traces | `swiftui-max` |
| `swift-concurrency` (avdlee) / `swift-concurrency-pro` (twostraws) | concurrency-correctness review of diffs | `swift-language` |
| `swift-testing-pro` (twostraws) / `swift-testing-expert` (avdlee) | test-suite review | `swift-language` |
| `swiftdata` (dpearson2699) / `swiftdata-pro` | persistence layer | `swift-language` |
| `swiftui-performance-audit` (dimillian) | hitch/perf audits | `swiftui-max` |
| `xcode-build-fixer` + siblings (avdlee) | build failures, build-time optimization | `apple-release-ops` |
| `apple-appstore-reviewer` (github/awesome-copilot) | adversarial pre-review simulation | `app-review-max` |
| `app-store-optimization` / `aso` | store listing growth (keywords, conversion) | `app-review-max` (compliance) — ASO owns growth, review-max owns compliance |
| `asc-metadata-sync` etc. (rudrankriyam ASC CLI suite) | scripted App Store Connect metadata ops | `apple-release-ops` |
| `apple-hig` (nexu-io) | extra HIG lookups | `apple-hig-ux` |

Install commands live in the plugin README (`npx skills add <owner/repo@skill>`).

## Conflict resolution rules

Skills overlap; that's by design. When two sources disagree:

1. **Facts about versions, policies, legal requirements**: this plugin's skills win — they are dated (mid-2026) and research-verified. Companions may predate policy changes.
2. **Workflow depth** (how to run a review, how to structure a test suite): the specialized companion wins.
3. **Style**: match the codebase first, then `swift-language` defaults.
4. Never apply two overlapping checklists blindly — merge, dedupe, and run once.

## Handoff conventions

- When a stage produces decisions (chosen navigation pattern, data types collected, monetization model), carry them forward explicitly — later skills need them (data types → nutrition labels; monetization → review guidelines).
- Anything marked beta (iOS 27 / Swift 6.4) in one skill stays beta-flagged in all downstream output.
- The final deliverable of a multi-facet task should state which facets were checked and which were consciously skipped.
