---
name: game-platform-cert
description: Console / store certification specialist. Owns platform technical requirements (Sony TRC, MS XR, Nintendo Lotcheck), age ratings (ESRB/PEGI/CERO), localization compliance, and submission workflow. Auto-invoked when preparing or debugging a console or store submission.
---

# Game Platform Certification

A failed cert is a slipped launch. Platform requirements (Sony TRC, Microsoft XR,
Nintendo Lotcheck, store policies) are exhaustive, version-pinned, and unforgiving
— treat compliance as a tracked workstream, not a pre-submission scramble.

## When to reach for this

- Planning or preparing a console or store submission
- A cert failure came back and needs triage and a resubmission plan
- Scheduling age-rating questionnaires and regional variants
- Setting up build numbering and release branches for submission vs. day-1 patch

## Principles

1. **Read the current requirement doc — version-pinned.** TRCs/XRs/Lotcheck
   guidelines change between SDK releases; last project's notes and forum lore are
   how teams fail requirements that were updated a year ago.
2. **Internal cert pass first.** Run the full per-platform checklist internally
   before burning a vendor submission slot — vendor cert rounds cost one to two
   weeks each, and slots near launch windows are contended.
3. **Every requirement has an owner and an evidence link.** A checklist row that
   says "done" with no capture, log, or test result attached is not done.
4. **Plan ratings early.** ESRB/PEGI/CERO/USK questionnaires, rater builds, and
   regional variants take weeks; digital storefronts mostly route through IARC,
   but physical/console releases need the boards directly. Content changes after
   rating (added monetization, new violence) can force a re-rating.
5. **Two-track build numbers.** The submission build freezes while the day-1
   patch branch keeps moving — establish the branch/version scheme before content
   lock, and know each platform's patch-approval lead time.
6. **The usual suspects are systemic, not cosmetic.** Suspend/resume,
   out-of-storage and save-corruption handling, controller disconnect, user
   sign-out mid-session, and network-loss flows are the classic cert failures —
   they need engineering time, not a QA afternoon.

## Submission readiness checklist

- [ ] Current platform requirement doc version recorded; full checklist imported into the tracker with owner + evidence columns
- [ ] Internal cert pass executed on submission-candidate build, on retail-equivalent hardware/kits
- [ ] Suspend/resume, constrained-mode, and quick-resume flows tested at every game state (boot, load, save, purchase, online session)
- [ ] Save-data: corruption, out-of-space, and profile-switch handling verified; no data loss without warning
- [ ] All user-facing storefront/system terminology matches the platform's required nomenclature per locale
- [ ] Age ratings secured for every launch region; rating displayed where mandated; IARC vs. direct-board path confirmed per storefront
- [ ] Online features: required privacy/permission checks honored (child accounts, communication restrictions)
- [ ] Build numbering scheme covers submission build, resubmission increments, and day-1 patch; release branch locked
- [ ] Submission timeline mapped backwards from launch: internal pass → vendor cert → fix window → resubmission buffer (assume at least one failure) → release
- [ ] Risk log of fragile requirements with mitigation and a named decision-maker for waiver requests

## Pitfalls

- Testing on dev kits in dev mode only — retail-mode behavior (storage, accounts, suspend) differs
- Discovering localization mandates (terminology, age-rating display per region) at submission time
- Assuming the day-1 patch can fix cert failures — the submission build itself must pass
- Scheduling zero resubmission buffer; first-pass cert success is the exception, not the plan
- Letting a post-rating content change (lootboxes, chat) invalidate the existing age rating silently
- Treating store policy (Steam/Epic/console storefront) as separate from cert — a policy rejection slips the date just as hard

---
*Related: `game-liveops` (post-launch update cadence within platform patch rules),
`game-engine` (engine-level fixes cert failures demand), `game-audio` (platform
audio mandates) · domain agent: `game-architect` (platform-target strategy) ·
output/ADR format: `playbook-conventions`*
