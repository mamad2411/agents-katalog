---
name: version-bound-cleanup
description: Gating migrations and clean-up code behind an update milestone. Use when writing code that moves, renames, rewrites or deletes data left by an earlier version, reads an old format, or backfills a new field for existing data, in Noodle, Hub, Applet, Computer, Browser or Mobile; and when asked what clean-up code can be removed.
---

# Version-bound clean-up

A migration runs only for people who install the release that ships it. Sparkle lets
people skip releases, so every migration is tied to an update milestone: a release
people must run before any later one. The code lives until the release after the
milestone, then goes.

The milestone mechanism is described in [`docs/releases.md`](../../../docs/releases.md),
under Update milestones. Read it first.

## When writing a migration

1. Find the app whose release ships the code: its `VERSION` and changelog. Shared code
   under `Sources/` ships with every app that runs it; gate it for each one.
2. The milestone is that app's next release: the dated section still being prepared,
   otherwise the next version after `VERSION`. Ask if unsure which.
3. Add the milestone to the app's `Support/update-milestones.json`, in ascending order.
   Create the file for an app that has none; release packaging picks it up.
4. Mark the code, its call site and its tests with the release that may delete it,
   the one after the milestone:

   ```swift
   // TODO(Hub 0.7.0): remove with its call in HubBots.init and
   // HubTests.testBotsFromBeforeGetTheirOwnerWhenTheHubOpens. Milestone: Hub 0.6.0.
   ```

   Name the app unless it is Noodle; version numbers differ between apps. Name every
   call site and test so removal is one pass.
5. Never write `TODO(NEXT_VERSION)` or a TODO without a milestone behind it.
6. Mention the milestone in the report to the user; it forces an upgrade step on them.

Mobile ships through the App Store, which has no milestones. Ask the user how long
a Mobile migration stays.

Where skipping the milestone could damage data, keep a startup check that names the
release to run first instead of deleting the code outright.

## When asked what can be removed

- `grep -rn 'TODO(' --include='*.swift'` outside `.build`, and compare each with its
  app's `VERSION` and milestones file.
- Removable: the named release is at or below the next one, and the milestone it
  depends on is listed and published.
- Flag anything overdue, and any `TODO(NEXT_VERSION)` or migration with no milestone.
- Removing it follows the TODO: the code, its call sites and its tests, together.
