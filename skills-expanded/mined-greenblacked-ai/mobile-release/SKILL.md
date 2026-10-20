---
name: mobile-release
description: "Ship a native iOS or Android build through the app store's own phased or staged rollout, where the binary itself cannot be recalled once installed. Gate every stage on an agreed crash-free-rate comparison between the new version and the previous one at the same install age, set the halt threshold before the rollout starts, and put every risky behaviour behind a server-side flag so a bad build can be defaulted off without a new binary. Design the API compatibility window and a server-controlled minimum-supported-version and force-upgrade check before old clients are years old, and triage a store rejection against the guideline it actually cites. Use when someone asks about phased release percentages, staged rollout, crash-rate halt criteria, or a rejected build. Not for a server-side canary or flag rollout (release-strategy), or a game's store submission (game-certification)."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Mobile Release

A mobile release is designed well when everyone agrees, before the first percentage
ships, what would stop it — and the thing that actually stops it is a server-side flag,
because the binary itself is the one part of this that cannot be pulled back.

The job is hard because `release-strategy`'s whole model assumes an operator can flip a
switch and every user is instantly back on the old path. A shipped binary breaks that
assumption: once a device installs it, pausing the store's rollout only stops the
schedule from advancing to more devices, it does nothing for the ones that already have
the code. The only lever that reaches an installed binary is one built into it in
advance — a server-side flag, a remote config check, a kill switch the app itself
consults. A team that treats a paused phased release as a rollback finds this out during
the incident, not before it.

## Scope

Use for: planning or running an iOS or Android phased/staged store rollout; deciding the
halt criterion and comparison basis before it starts; designing the server-side flag a
risky release rides on; the API compatibility window and minimum-supported-version and
force-upgrade path for old clients; store review lead time on the release calendar; and
triaging a rejected build against the guideline it cites.

Do not use for: a server-side canary, percentage rollout, blue/green or flag rollout
where the artefact itself can be pulled back — that is `release-strategy`, and its
mechanism-choice and bake-time guidance apply directly once a build is past the store and
the remaining risk is server-side. A game's platform certification and store submission
review is `game-certification`, which also owns the one-time submission process this
skill's store-rejection step assumes already happened. The build pipeline that produces
the binary is `ci-triage` if it is red; the notes describing what changed are
`release-notes`; and asset or package-size limits are `game-assets`.

## Workflow

### 1. State the binary's own limit before naming a percentage

Write down, in the release plan, that the build cannot be pulled back once a device has
installed it — only the store's phased or staged rollout can be halted going forward, and
a server-side flag is the only lever that reaches devices that already have the code.

*Gate:* the plan names at least one server-side flag for every change risky enough to
want a phased rollout in the first place. If there is none, the rollout is decorative —
it slows how many devices get the bad code, but it does not remove the bad code from any
device that already has it.

### 2. Read the store's current rollout mechanics before assuming last year's

On iOS, App Store Connect's phased release runs a fixed seven-day schedule for
automatic-update users. The only controls on top of it are pausing — up to 30 days in
total, any number of times, holding at the current percentage — or releasing to all users
immediately; there is no way to slow it to a custom curve or advance to an arbitrary
intermediate percentage. See the schedule in `references/store-mechanics.md`. On Android,
check the Play Console's current staged-rollout options directly rather than assuming a
specific schedule — what percentages it offers, whether you choose them, and what it lets
you change mid-rollout are details that change over time, and only the console itself is
authoritative.

*Gate:* the plan states, per platform, which parts of the schedule are fixed by the store
and which are chosen in the console at rollout time, checked against the console rather
than against what shipped last release.

### 3. Name the halt metric and its comparison basis before the rollout starts

Compare the new version's crash-free rate against the previous version's, at the same
age since each one's own release — not an absolute number, and not "today's rate" against
"yesterday's," which conflates the comparison with a different confound every time.

*Gate:* a written halt threshold exists, agreed before the first percentage ships, the
same discipline `release-strategy` step 1 already asks of a server-side rollout. Nothing
here asserts what threshold either store expects or enforces — that is a decision this
skill's procedure asks the team to make and write down, not a platform requirement to
look up.

### 4. Design the API compatibility window and the force-upgrade path

A client installed today may still be calling the API in two years, because nothing
compels an update. Decide, before the first release that needs it: how many API versions
are supported at once, what a client on an unsupported version sees, and the
server-controlled minimum-supported-version check that turns "please update" into "you
must update before this works."

*Gate:* the plan names the deprecation window in API versions or months, not "we'll
figure it out."

### 5. Put store review lead time on the release-train calendar, not on the day you need it

Both stores' review queues are a number you do not control; measure it from your own
recent submissions well before a release needs it.

*Gate:* the release calendar shows a review-lead buffer before the date anyone external
was told.

### 6. Triage a rejection against the guideline it actually cites

Quote the exact guideline number or line from the rejection notice, and check the fix
against that text before resubmitting — resubmitting a guess costs another full trip
through the queue. Read `references/rejection-playbook.md` for how to read a rejection
notice back to its guideline, common causes per category, and the resubmission
checklist.

*Gate:* the rejection response names the guideline quoted, and the fix is checked
against it before the resubmission goes in.

### 7. Close the loop like any other rollout

Record the comparison at each stage — percentage, crash-free rate, the decision — and
note in the runbook when the flag protecting this release is safe to remove. This step
deliberately mirrors `release-strategy` step 9 rather than reinventing it.

## Hard gates

1. No stage past the first advances without a written halt threshold agreed before the
   rollout started.
2. No risky release without at least one server-side flag capable of defaulting the
   behaviour off, because the binary itself is the one part of this that cannot be rolled
   back.
3. No resubmission after a rejection without the guideline it cited quoted in the fix.

## Output format

```markdown
## Release
[Platform(s), what is changing, and why it needs a phased/staged rollout rather than a
flat ship.]

## Binary limit and flag
[What cannot be recalled once installed, and the server-side flag that can still be
turned off.]

## Schedule
[What the store fixes and what the console lets you choose, with the source checked for
this rollout rather than assumed from the last one.]

## Halt criterion
Metric:    [crash-free users/sessions, against which comparison basis]
Threshold: [agreed before rollout start]
Action:    [pause / hold / flag off]

## Compatibility window
[Supported API versions or client ages, and the minimum-supported-version /
force-upgrade behaviour.]

## Calendar
[Review lead time, and the date it was booked against.]

## Rejection response (if applicable)
[Guideline cited, the fix, and confirmation the fix answers that clause.]
```

## Anti-patterns

**Treating a paused phased release as a rollback.** Pausing stops the schedule advancing;
it does not remove the build from a single device that already has it. Every behaviour
risky enough to need a phased release needs a flag that can be flipped independently of
the binary.

**Copying `release-strategy`'s bake-time table onto a store rollout.** iOS's schedule is
fixed by the platform. Design the flag and the halt criterion, and check the console for
what is actually adjustable rather than assuming a bake time nobody can change.

**A halt threshold picked during the rollout.** Exactly the failure `release-strategy`
names for server-side rollouts, and it is worse here: there is no fast rollback to fall
back on if the number was too generous.

**No compatibility plan until an old client breaks something.** By the time a two-year-old
client is the one causing an incident, the fix is a server change nobody tested against
that client, made under pressure.

**Resubmitting on a guess.** Guideline-driven rejections quote a specific clause;
answering the rejection's tone instead of its citation is how a second rejection happens.

## Reference files

- `references/store-mechanics.md` — read at step 2, when designing the schedule: Apple's
  verified phased-release schedule and pause limit, and how to read the Play Console's
  own staged-rollout options rather than assuming a fixed schedule for Android.
- `references/rejection-playbook.md` — read at step 6, when triaging a rejection: how to
  read a rejection notice back to its guideline number, common causes per guideline
  category, and the resubmission checklist.
