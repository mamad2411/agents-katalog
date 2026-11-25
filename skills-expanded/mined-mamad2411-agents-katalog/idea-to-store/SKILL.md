---
name: idea-to-store
description: Take an app from idea to a live App Store and Play Store listing, in order, with a gate at each stage.
disable-model-invocation: true
---

# Idea to store

One app, eight stages, each ending on a checkable **gate**. The stage owners are existing skills; this file is the order, the gates, and the material none of them carry. Run the stages in sequence. A gate that is not met stops the run at that stage, and the report names the gate.

State lives in the repo, not in context. Two files, re-read both at the start of every session on the app; recalled state is untrusted.

- `docs/LAUNCH.md` holds one line per gate (`met <date> <evidence>` or `open <blocker>`).
- `CONTEXT.md` holds the app's glossary: the shared word for each thing the app deals in, and nothing else. It is not a spec and carries no implementation detail. `/domain-modeling` owns its format and updates it inline the moment a term settles. A launch runs over weeks and many sessions, so the glossary is what stops stage 5 calling a thing by a different name than stage 2 did.

Every `open` row written to `docs/LAUNCH.md` also appends one row to `~/.claude/BLOCKERS.md`, and clearing the gate clears both. Most of what blocks a launch is a step only Keith can take, and those steps carry the clocks: a Play closed test runs 14 days whoever starts it, store agreements wait on bank and tax details, a review queue is a queue. `/human-blockers` ranks them across every app, which a single app's `LAUNCH.md` cannot do.

Read `references/store-prereqs.md` before stage 0 finishes. Two of its items are wall-clock, not work: the Play closed test runs 14 days, and store agreements need Keith's bank and tax details. Start both on day one or they set the launch date.

## Stage 0. Demand

Owner: `/office-hours` or `/brainstorming` for candidate framings, then two passes on the pick, in this order.

1. `/grilling` builds it out. Work the decisions as a tree and ask the whole frontier in one round, each question numbered and carrying your recommended answer, then wait. Facts are yours to find, never Keith's to supply: dispatch a sub-agent for anything the filesystem or a store console can answer, and ask only the rest of the frontier while it runs. Done when the frontier is empty.
2. `/grill-me` attacks what survives. Name the weakest premise and what would falsify it. A framing that breaks here goes back to the candidate list.

Build, then break. Running only the attack pass leaves half the design tree unvisited, which is how a launch reaches stage 5 still carrying an unasked question.

The rule from the model-policy-engine memory holds for every app: three real demand conversations before code, with named people and what each said. An app for Keith alone counts as one conversation, and it needs the other two.

Gate: `docs/PRD.md` exists (via `/project-scaffold` or `/spec`) with the three conversations quoted, one success metric with a number, the monetisation decision (free, paid, subscription via RevenueCat, none yet), the platforms (iOS, Android, both), the one **native premise** the app depends on (background audio, push, health data, deep links) with the number that proves it, and the law the app's category touches (recording consent, health data, payments) in one paragraph.

Gate, second half: `CONTEXT.md` exists with every term the grill settled, and `docs/adr/` holds one ADR per stage-0 decision that passes all three of `/domain-modeling`'s tests: hard to reverse, surprising to a future reader without the context, and the result of a real trade-off. Monetisation, the native premise and the platform choice normally pass all three. The bundle id does not (it is a fact, not a trade-off): it belongs in `docs/LAUNCH.md`. Skip the ADR when any of the three tests fails; a directory of ADRs nobody needed is worse than none.

## Stage 1. Accounts, records, tracer

Owner: this skill, `references/store-prereqs.md` section 1. Everything a store needs from a human and takes days: developer accounts, agreements, bundle id and package name, App Store Connect record, Play app record, Codemagic signing.

**Build the wizard before walking Keith through any of it.** Every row of section 1 is a step only Keith can take, in a browser, on a console the agent cannot reach. Run `/wizard` and generate `scripts/store-setup.sh` from `references/store-prereqs.md` section 1: one stage per row, each opening its URL, saying what to click, capturing the value, and writing it to `.env` or a CI secret. Secrets use `ask_secret`, never a plain prompt, and nothing secret is echoed back into chat. Commit the script; it is the repeatable path for the next app, and re-explaining this procedure to an agent per app is the cost it removes. Eaves reached TestFlight and then sat on five human-only steps with no script to walk them, which is the shape this stage exists to stop.

The **tracer** is the first build: a bare shell with only the native premise from stage 0, through CI to TestFlight internal and Play internal, measured on a real phone against the PRD's number. Eaves built its store record, listing and five screenshots before the locked-phone test ran, so a failure there would have thrown all of them away. Every stage after this one assumes the tracer passed.

Gate: every row of the section 1 table is `met` or `open` in `docs/LAUNCH.md`, the Play closed test has a start date, and the tracer's measurement is written in `docs/LAUNCH.md` with the build id.

## Stage 2. System design

Owner: `references/system-design.md`. `/dev-framework` scaffolds the backend at its SCAFFOLD stage but its backend overlay stops at "health check endpoint" and "logging configured"; this reference carries the rest: the data model, auth, secrets inventory, the pipeline, alerts that reach a phone, cost ceiling, backup and restore, privacy data flow, and the 7-day post-deploy check.

Gate: `docs/ARCHITECTURE.md` answers every question in the reference, names the alert channel and the person who receives it, and names the event and the query that produce the PRD's success metric.

## Stage 3. Design

Owner: `/frontend-mix` for the variants and the board, with `DESIGN.md` locked first by `/design-consultation`. Mobile rules that the web pipeline does not carry: `references/mobile-design.md`. The mark and app icon are a real three.js render captured by Playwright, never a CSS or SVG fake; the recipe pointer is in that reference.

Gate: `DESIGN.md` committed, the board winner picked by Keith, every screen mocked including its empty, loading, error and offline state, and one icon producer script that writes every icon and splash size from the render.

## Stage 4. Build

Owner: `/dev-framework-rl`. One episode per slice, never one episode for the whole app: the backend, the app shell, the store shell (deep links, permissions, privacy manifest), and each feature are separate episodes with their own critics and rewards. The `mobile` and `backend` overlays load on detection; the two references above ride along as `[PROBATION]` briefs at the plan stage.

Gate: every episode finalised `shipped`, the real-device checks in the mobile overlay VERIFY stage done on a physical phone, and `docs/LAUNCH.md` updated with the build numbers.

## Stage 5. Store assets

Owner: this skill, `references/store-prereqs.md` sections 2 and 3. Listing copy, screenshots generated from the real app by a script, privacy labels and Play data safety answers that match `docs/ARCHITECTURE.md`'s data flow, review notes with a demo account, and the support and privacy URLs live.

Gate: `store-assets/APP-STORE.md` and `store-assets/PLAY.md` hold everything to paste, the screenshot script is committed, and both URLs return 200.

## Stage 6. Release

Owner: `references/release-and-launch.md` section 1. `/build-release` is the Phzse-specific version; the reference generalises it. Internal test track first on both stores, then the S-gate the app defines (for a recorder, a 60 minute locked-phone run), then external test, then submit.

Gate: a build installed from TestFlight and from Play internal testing on a real phone, the app's own S-gate passed with numbers, the **reviewer path** passed against production (fresh install, sign in with the demo credential, first action succeeds, screenshot in `docs/LAUNCH.md`), and both submissions pressed by Keith.

## Stage 7. Launch and after

Owner: `references/release-and-launch.md` sections 2 to 4, `/product-launch-video` for the film. Phased rollout, day-one watch, the rejection playbook, the 7 and 30 day review, and the memory writeback.

Gate: both listings live, the day-one watch recorded, and the post-deploy check scheduled.

## Leaving a session

Write `docs/LAUNCH.md`, then `hippo remember "<app> at stage N: <gate state>" --pin` from `~`, and update the app's memory file. Rotate any secret that appeared in chat before the session ends.
