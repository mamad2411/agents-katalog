---
name: app-factory
description: >
  Take an app idea from one spoken sentence to a submitted App Store build.
  Runs the whole pipeline with subagents: requirements, architecture, Xcode
  project scaffolding, implementation, review, simulator QA, screenshots,
  App Store Connect metadata, TestFlight and submission. Trigger on
  "build me an app", "I want an app that...", "build me an app",
  "new app", "/app-factory", or any request to create and ship an iOS app.
---

# App Factory

**App name.** `{{app}}` and `{{bundle_id}}` in the references stand for the app being built: use the name and bundle id passed to `scripts/new-ios-app.sh`.

A pipeline for turning an idea into a shipped iOS app. The point is that the
owner describes what they want once, in their own words, and everything after
that runs without them having to specify stages.

## Before anything else

Ask at most three questions, and only ones whose answers change the build:

1. Scope of v1, with a recommendation.
2. Anything the app must talk to that needs credentials (Google OAuth, a paid
   API, a backend).
3. Whether it publishes under the existing Apple team or a new one.

If she has already answered these in the conversation, do not ask again. Never
ask about stages, tooling, or whether to proceed.

## Hard truths to state up front, before building

iOS forbids several things people assume an assistant app can do. Say which
parts of the idea are impossible before writing code, not after:

- **No API for Mail, iMessage or SMS on iOS.** A Mac companion can read
  `~/Library/Messages/chat.db` with Full Disk Access; the iPhone cannot.
- **No WhatsApp read API** for personal accounts, on any platform.
- **No per-event colour via EventKit.** Categories must be encoded another way,
  such as an emoji prefix in the title.
- Email means a direct OAuth integration per provider, not the system Mail app.
- Telegram works through TDLib; Slack and Google through their own APIs.

## Pipeline

Run the stages in order. Each stage hands its artefact to the next. Use the
`Workflow` tool when the user has opted into multi-agent orchestration;
otherwise run the subagents named below one at a time with `Agent`.

| # | Stage | Agent | Artefact |
|---|-------|-------|----------|
| 1 | Requirements | `sdlc:requirements-analyst` | User-visible behaviour, edge cases, acceptance criteria; contradictions flagged |
| 2 | Architecture | `sdlc:architect` | File-level plan, data flow, third-party choices |
| 3 | Scaffold | none, run `scripts/new-ios-app.sh` | Xcode project that builds on first try |
| 4 | Implementation | `general-purpose`, one per module | Swift source |
| 5 | Review | `reviewers:swiftui-reviewer` | file:line findings, fixed before moving on |
| 6 | QA | `sdlc:qa` driving the simulator | Real flows exercised, screenshots |
| 7 | Store assets | `biz:aso-optimizer` | Title, subtitle, keywords, description, screenshot copy |
| 8 | Ship | none, run fastlane | TestFlight build, metadata upload, submission |

Do not skip stage 1 or 5. Skipping requirements is what produces an app that
builds and does the wrong thing; skipping review is what produces the crash
found by the App Store reviewer.

## Scaffolding

`scripts/new-ios-app.sh <Name> <bundle-id>` creates a project laid out the way
Chip is: XcodeGen spec, SwiftUI app, `Models/ Views/ Services/` folders, a
Keychain helper, a `JSONValue` type for tool schemas, and an `LLMClient` that
speaks both the OpenAI and Anthropic dialects so any cheap model can be plugged
in. Copy from `~/Projects/chip` rather than writing these from scratch again.

Every generated app gets the `<NAME>_UI_PREVIEW=1` environment flag that skips
permission prompts, because the simulator cannot dismiss a TCC dialog
programmatically and App Store screenshots need clean frames.

## Verification gates

Nothing advances past a stage that has not actually passed:

- Stage 3 is done when `xcodebuild ... build` prints `BUILD SUCCEEDED`.
- Stage 6 is done when the app has been launched in the simulator, driven
  through the main flow, and screenshotted. A build that compiles is not a
  build that works.
- Stage 8 is done when App Store Connect shows the build in the state you
  claimed. Never report "submitted" from a fastlane exit code alone.

## Shipping

See `references/app-store.md` for the full checklist: certificates, the
App Store Connect API key, metadata fields Apple rejects builds over, privacy
nutrition labels, and the fastlane lanes.

Two things always need the owner in person and cannot be automated:

- The first App Store Connect app record for a brand-new bundle id, if the API
  key lacks the App Manager role.
- Apple's review decision, which takes one to three days.

Everything up to and including "submitted for review" is automated.

## Reporting

At the end, say which stages ran, what the app actually does, what was left
out, and the App Store Connect link. If a stage failed, say so plainly instead
of describing the pipeline as complete.
