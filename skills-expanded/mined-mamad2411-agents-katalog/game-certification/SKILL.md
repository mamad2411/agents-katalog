---
name: game-certification
description: "Get a game through platform certification and store submission — the one-time review gate before players see it. Works backwards from the release date to a content lock, sorts the remaining work by whether it can fail cert rather than by visibility, and tests the behaviours nobody plays: suspend and resume, sign-out, controller disconnect, storage full. Covers ESRB, PEGI and IARC ratings, Nintendo lotcheck, Sony TRC and Microsoft XR requirements, Google Play's data safety form, Apple entitlements and notarisation, and what a rejection costs the schedule. Use whenever someone says \"our build was rejected\", \"what does lotcheck test\", \"do we need an ESRB rating\", or \"missing entitlement on upload\". Not for staged rollout after launch (release-strategy, or mobile-release for a mobile game's own store), a frame budget or stutter (game-performance), or build size (game-assets)."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(codesign:*), Bash(xcrun:*), Bash(apksigner:*)
---

# Game Ship

The game clears platform review on the first submission, and it reaches players on the date that was promised, because everything that could fail certification was run and fixed weeks before anything that merely polishes.

Certification is not a quality bar you can grind down at the end. It is a queue with a fixed entry cost and an expensive failure mode: a rejection does not cost you the fix, which is usually an afternoon, it costs another trip through a review that takes days or weeks, and it takes the marketing date, the storefront feature slot and the press embargo with it. Two mistakes produce almost every missed date. The first is ordering the remaining work by what is visible — the frame rate, the last content pass, the bug list — while the things that actually fail cert sit untouched, because they are invisible in normal play. The second is discovering the calendar late: a rating certificate, a platform account approval or a storefront's own release lead time is a number you do not control, and finding it out in the last week converts a finished game into a delayed one. The order below exists to put the uncontrollable and the disqualifying first.

## Scope

Use for: preparing a first submission to a console, mobile or PC storefront; building the cert checklist; the age rating questionnaire and content declarations; privacy and data-collection declarations; store metadata and assets; build signing, entitlements and notarisation; the platform behaviours in the technical requirements; working backwards from a release date; and recovering from a rejection.

Do not use for: getting a change out gradually once the game is already live — feature flags, percentage or ring rollouts, canaries, blue/green, bake times and promotion gates are `release-strategy`, and none of that is what a platform review is. A performance pass, a frame budget or a stutter, including the frame-rate floor a platform sets, is `game-performance`. Build size against a store ceiling and the texture and audio work underneath it is `game-assets`. Making the game, or its export pipeline for an itch.io or web release, is `game-builder`. The save write path itself is `game-save-system`, though the platform's rules about when it may run are here. A red build pipeline is `ci-triage`; a dependency vulnerability alert is `dependency-triage`; the notes that accompany a patch are `release-notes`.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Ownership (step 1) | The people who build the game work the checklist and compute the calendar themselves | A producer owns the calendar against a publisher's milestones | A dedicated certification team owns the calendar and the platform relationships |
| Resubmission budget (step 1) | Often none — a rejection is a real schedule hit | Usually one budgeted | Budgeted per platform, across a simultaneous multi-platform launch |
| Localisation and compliance (steps 4, 5) | Whatever the team can do itself, often none | A localisation vendor for the storefront's required languages | Dedicated localisation, legal and compliance teams reviewing every declaration |

Mobile F2P games carry the heaviest weight in steps 3 and 4's paid-random-item and privacy declarations. Competitive multiplayer and live-service games hit step 5's account sign-out, network-loss and save-data-messaging rows hardest, because those states occur constantly in play rather than rarely.

## Workflow

### 1. Work backwards from the date before touching the checklist

Four numbers decide everything else, and every one of them comes from the platform's own developer portal or your account manager rather than from a forum post that was true two years ago:

- **Review turnaround** for a first submission of this title on this platform, and whether a resubmission re-enters the queue at the back.
- **Rating lead time**, if a certificate is needed that the automated questionnaire does not produce.
- **The storefront's own release lead time** — the notice it needs before a release date, a pre-order or a feature slot.
- **How many resubmissions the schedule can absorb** before the announced date moves.

Then compute the content lock:

```text
content lock = release date
             − storefront release lead time
             − review turnaround × (1 + resubmissions budgeted)
             − your own final QA pass
```

Write that date down and circulate it. It is the number the team will argue about, and it is the only one that constrains anything.

Two facts shape the plan more than the arithmetic does. A rejection restarts the queue rather than resuming it, so the expected cost of a failed check is the whole turnaround, not the fix. And review queues lengthen before platform holidays and seasonal sales, which makes submitting in the run-up to a major sale event the most common self-inflicted delay in this discipline.

`references/submission-calendar.md` has the backwards plan in full, the per-platform shape of the queue, and what each class of rejection costs in calendar time. Read it at this step.

### 2. Split the remaining work into what can fail cert and what cannot

Two lists, and the first one runs first regardless of how the second one looks.

**Can fail certification:** platform behaviour requirements, age rating and content declarations, privacy and data declarations, signing and entitlements, required platform features such as achievement or trophy metadata and save-data messaging, platform nomenclature, required localisations, a crash on any configuration in the test matrix, and store metadata that breaks a storefront rule.

**Cannot fail certification:** frame-rate work above the platform's stated floor, balance, extra content, and the large majority of ordinary bugs.

A bug that breaches no requirement is a business decision — ship it and patch it, or hold the date deliberately. A missing entitlement is not a decision; it is a rejection. Keeping the two lists separate is what stops a team from spending the last fortnight on a polish pass and submitting a build with an unsigned binary.

### 3. Start the age rating first, because it is the longest pole you do not control

For digital releases on most storefronts, one IARC questionnaire produces ESRB, PEGI, USK, ClassInd, ACB and GRAC ratings at once, at no cost and nearly immediately — Google Play, the Microsoft Store and the Nintendo eShop are among those that use it. Anything outside that route is a separate submission with its own fee and its own weeks: a physical release, a CERO rating for Japan, a USK rating on physical media in Germany, and the territories that run their own approval regime rather than a questionnaire.

Answer it accurately, particularly on the questions teams under-report without meaning to: gambling and simulated gambling including loot boxes, in-game purchases and whether randomised items are among them, user-to-user communication, user-generated content, and any link that leads out of the game to content you do not control. A rating obtained from wrong answers can be revoked after launch, which costs a storefront removal rather than a delay.

Several storefronts also require a separate disclosure of paid random items and their odds, independent of the rating. That is a store policy rather than a rating question, and it is checked. `references/ratings-and-declarations.md` covers the questionnaire's trap answers, the territories that need their own certificate, and the disclosure rules; read it at this step and the next.

### 4. Make every declaration match the build rather than the intention

Privacy and data declarations are written by someone who knows what the team meant to collect, and checked against what the binary actually sends. The gap is almost always a third-party SDK.

- Inventory every SDK in the build — analytics, crash reporting, ads, attribution, engine telemetry, the social or login library — and record what each collects by default, including advertising identifiers and coarse location. Default-on collection in a library nobody configured is the usual cause of a false declaration.
- Fill in the platform's form from that inventory: Apple's App Privacy details and App Tracking Transparency prompt where tracking happens at all, Google Play's Data safety form, and the console equivalents.
- Apple also requires privacy manifests from bundled SDKs and a declared reason for certain APIs; a missing manifest rejects at upload.
- Publish a privacy policy at a URL that resolves, since collecting anything makes it mandatory, and a dead link is a rejection on its own.
- Declare children's-audience status honestly. An advertising SDK inside a game declared for children is simultaneously a store policy breach and a legal exposure, and it is the single declaration mistake with consequences past the store.

### 5. Test the behaviours nobody plays, because that is where cert fails

Normal play never exercises any of this, which is exactly why it survives to submission. The specific checklists — Sony's TRC, Microsoft's XR requirements, Nintendo's lotcheck guidelines — live behind each platform's developer portal under NDA, so read the real document; the table below is the category list to plan and schedule against.

| Behaviour | What is being checked |
| --- | --- |
| Suspend and resume | The game returns to the same state with audio restored, no hang, and no assumption that time did not pass |
| Account sign-out or user switch mid-session | The profile can disappear under the game; it returns to a sensible screen and writes nothing to the wrong account |
| Controller disconnect and reconnect | Play pauses by itself and a reconnect prompt appears; input does not silently rebind to another pad |
| Storage full, or the save quota exceeded | A clear message, a retry path, and no lost data or crash |
| Network loss and recovery | No infinite spinner, no soft lock, and a stated outcome for anything in flight |
| Save data messaging | A visible indicator while writing, a warning against powering off, and no write inside the platform's restricted windows. The write path itself is `game-save-system` |
| Achievements and trophies | Complete and localised metadata, each unlock firing once, at the right moment, and offline |
| Boot to interactive | Some platforms cap the time from launch to a responsive screen |
| Nomenclature | Each platform's official names for its buttons, accounts, storage and hardware. Another platform's term is a plain rejection |
| Required localisations | Every language the storefront lists for the territory, for legal and system-facing strings at minimum |
| Hardware and display modes | Handheld and docked, each supported resolution, HDR, and every controller type the platform requires |
| Standard error wording | Some platforms specify the text of common errors |

Run these on retail-configuration hardware rather than only on a dev kit: dev kits have more memory, different storage behaviour and different timings, and several of the rows above are exactly the cases the difference hides. `references/platform-requirements.md` expands each row into what the test actually looks like and which ones commonly fail; read it before the test pass is scheduled.

### 6. Fix build identity before a human reviewer ever sees it

This class rejects at upload, which makes it cheap to find early and humiliating to find on submission day.

- **iOS and macOS.** A valid signing identity and provisioning profile, entitlements matching the capabilities the build actually uses, and a macOS build notarised and stapled.
- **Android.** Signed with the upload key registered for that package name, targeting at or above the store's current API floor, with every permission justified by something in the game.
- **Console.** Correct title and content identifiers, a package built by the platform's own tool, and an SDK or firmware baseline at or above the platform's current minimum, which moves on a schedule you do not set.
- **Windows storefronts.** Package identity matching the reserved name, and a signing certificate where the store requires one.

Two traps sit alongside it. Debug logging, developer menus and profiling overlays left enabled are visible to a reviewer and are a rejection on several platforms. And a build still pointing at a staging or test endpoint passes local QA perfectly, because staging is up — check the shipped configuration rather than the intended one. `references/store-listing-and-signing.md` carries the verification commands per platform and what each failure message means.

### 7. Assemble store metadata from the build being submitted

Storefronts reject for metadata at least as often as for the build, and metadata is the part that gets delegated late to whoever is free.

- Screenshots and video captured from the build under submission, at every required size, with no debug overlay, no placeholder art and no footage of content that is not in the game.
- Icons and key art at each required size, including the ones only one platform asks for.
- Description, keywords and localisations, without competitor names and without a claim the game does not deliver — a stated feature that is not present is a reason for removal later, not just a rejection now.
- Pricing, territories, release date, pre-order configuration and any bundle.
- The rating artwork and content descriptors each territory requires, displayed as that territory specifies.

### 8. Submit with slack, and treat a rejection as exactly one requirement

Submit early in the week and with the budgeted resubmission still unspent. When a rejection comes back:

1. Read the requirement identifier the platform cites and reproduce it on the hardware they used, rather than arguing from the code.
2. Fix that requirement and nothing else. A resubmission carrying unrelated changes enlarges what the reviewer has to re-check, and it is the usual way a second rejection is earned.
3. Resubmit, and record the requirement, the cause, the fix, and whether a check in step 2 or 5 would have caught it. That record is the next release's checklist, and it is the only thing that makes the second submission cheaper than the first.

An approved build held back is cheap. An announced date without an approval is not, so treat approval well before the date as the goal rather than as slack wasted.

What happens once the build is live — who receives it first, at what percentage, behind which flag, with what bake time before the next ring — is `release-strategy`. A platform review is a gate passed once per build; a rollout is something run continuously, and they share no procedure.

## Anti-patterns

**Treating cert as launch-week work.** The requirements cover behaviours that never occur in normal play, so they are never accidentally satisfied, and finding them in the last week finds them after the content lock.

**Ordering the remaining work by what is visible.** The frame rate and the bug list are what everyone can see, and neither is what rejects the build.

**Learning the review turnaround after announcing the date.** The number is available on day one from the developer portal, and it is the largest term in the schedule.

**Answering the rating questionnaire optimistically.** A rating obtained on wrong answers is revocable after launch, and a removal costs more than a higher rating ever would.

**Writing the privacy declaration from what the team meant to collect.** The SDK inventory is the source of truth, and an ads or analytics library collecting an advertising identifier by default is what makes the declaration false.

**Testing only on a dev kit.** More memory, different storage timing and a different network path hide precisely the suspend, storage-full and boot-time cases the platform tests.

**Shipping a build pointed at staging.** Local QA passes because staging is up, and the reviewer sees a game that cannot connect.

**Bundling unrelated fixes into a resubmission.** It expands the surface the reviewer re-checks and converts one rejection into two.

**Leaving store metadata to the submission day.** Screenshots from an old build and a missing icon size are rejections earned for free.

**Confusing cert with rollout.** A build that has passed review has not been de-risked; that is a separate discipline and it starts afterwards.

## References

- `references/submission-calendar.md` — read at step 1: the backwards plan from a release date, the per-platform queue shape, what each class of rejection costs in days, and the account and entitlement approvals that have to start before the build exists.
- `references/platform-requirements.md` — read before the test pass at step 5: each requirement category expanded into the test a platform actually runs, the ones that commonly fail, and how to build a hardware and configuration matrix that covers them.
- `references/ratings-and-declarations.md` — read at steps 3 and 4: the rating routes by territory, the questionnaire answers that get under-reported, paid-random-item disclosure, and the privacy and data-safety declarations with the SDK inventory that backs them.
- `references/store-listing-and-signing.md` — read at steps 6 and 7: signing, entitlements and notarisation per platform with the verification commands, the upload-time rejections and what each message means, and the store listing asset and copy requirements.
