---
name: vow
description: Pre-commitment engineering — declare falsifiable vows before the work starts and audit every one before claiming done, discipline pledges distilled from the engaged skills' Done means plus scope pledges bounding the blast radius. Use when the user says "don't touch anything else", "only this file", "stay in scope", "no new dependencies", "don't tell me it's done until", "commit to your constraints", or "show me the failing test first"; when a previous attempt was declared done and was not; when a diff wandered into files nobody asked about; when en announces an engagement (the announcement is the vow moment); or when delegated work needs acceptance criteria the delegate can be audited against.
---

## Stance

制約と誓約 — Restriction and Pledge: an ability grows stronger through what its user swears not to do, and a broken oath forfeits the power itself. For an agent this law is not thematic, it is generation mechanics. An agent writes toward what already sits in its context: a constraint declared before the first action conditions every action after it, while the same constraint recalled at review time merely grades the damage. Stated up front, "no new dependencies" steers the fix away from the tempting library; remembered afterward, it is a rejection comment on a finished diff.

The stakes are the two chronic failures of agent work, visible in any week of transcripts. The wandering diff: asked for one fix, the agent "also cleaned up" four files nobody mentioned, and the review burden lands on the person who wanted one line changed. And the hollow done: "fixed" claimed with no run evidence, discovered unfixed by the next person to pull. The failures share a root — the constraints existed, in the request or in the engaged skill's own Done means, but nothing forced them into the transcript before the work began. A vow is that forcing, and its law is strict: falsifiable and visible, or it is not a vow. "I'll be careful" binds nothing; "the diff touches src/billing/ only" can be checked by anyone holding the diff.

## Boundaries

Vow binds work; it never selects it. Reading a request's problem shape and choosing which abilities engage is en's field — vow begins the moment en's engagement line is posted, turning that routing decision into pledges the work can be audited against. En announces which disciplines act; vow declares what the acting work swears not to do. Neither does the other's job.

When work is dispatched across agents, the acceptance criteria attached to each unit are that delegate's vows, and their form is this discipline: falsifiable, declared before the unit starts, audited on return. Manipulator owns the decomposition, the dispatch, and the verification — vow only defines what a criterion must look like for that verification to be possible. A delegate's "done" arriving without its audit is manipulator's to reject, in vow's format.

A restriction and a vow share one law but not one lifetime. The restriction hatsu writes into a skill's text is design-time and permanent: what the ability refuses to cover, forever. The vow this skill declares is run-time and expires with the engagement. The two meet at the forge — the same pledge breaking across sessions, transcripts attached, is exactly the recurrence evidence hatsu's method demands. Hand it over instead of re-swearing an oath the pack has proven it cannot keep.

Never vow what the runtime already enforces. A sandbox that blocks pushes needs no oath about pushing; pledging it is theater that pads the block and cheapens the pledges that bind. Vows cover the space the harness cannot see: scope judgment, evidence standards, claims.

## Method

1. **Distill discipline vows from each engaged skill's Done means — at most three in total.** Not a paste of every bullet: read the engaged skills' Done means and pick the checks THIS task is most likely to violate. Enhancer on a hot path → "no change ships without the re-measured number". Conjurer on a handler → "no fix claimed without the failure reproduced red then green". The selection is the work; a block that could have been written without reading the task is the tell that it wasn't done.

2. **Add scope vows from the task's blast radius — at most three.** What must this work NOT do: directories the diff stays inside, dependencies that stay absent, interfaces that keep their shape, files that stay byte-identical. Take them from the request's own limits AND from what the surrounding system silently assumes — the manifest nobody mentioned, the generated file that tracks the one you touch, the config that enumerates what you are adding to.

3. **Declare the block before the first action.** Under en, directly beneath the engagement line; invoked alone, still the first thing after the reading of the task. Fixed shape, each vow tagged with its source:

   ```
   Vows:
     V1 (conjurer/done): no fix claimed without the failing case red then green
     V2 (scope): diff touches src/billing/ and tests/billing/ only
     V3 (scope): no new dependencies — the manifest stays byte-identical
   ```

4. **Work under the block, and stop the moment a vow is about to break.** Surface it before the violating edit, not after: name the vow, say why the clean path crosses it, and renegotiate in the open. An amended vow is rewritten in the transcript at the moment of approval — never silently, never retroactively.

5. **Audit before any done claim.** Every vow, a verdict — kept, amended, or broken — and one line of checkable evidence each: a test name with its red and green runs, a `git diff --stat`, a byte-identical manifest. The done claim rests on the audit, not on an adjective.

6. **A broken vow without renegotiation voids the claim.** Report the work as incomplete with the breach named. A done claim over a silent breach is worth less than no claim: it teaches the reader to re-verify every audit you will ever write.

7. **Route repeat offenders to the forge.** The same vow declared and broken across engagements is not a discipline problem to re-swear harder — it is hatsu's evidence that an ability needs forging or an existing one needs repair.

## Worked trace

Request: "Invoice totals drift by a cent on half-cent lines — fix it in billing, and I don't want another 'done' that turns out not to be. Nothing outside billing, please." The engagement and the pledges post together, before any file is opened:

```
En: conjurer — reproduce the half-cent drift, close it, prove it stays closed
Vows:
  V1 (conjurer/done): no fix claimed without the drift reproduced —
      failing case red, then green, in tests/billing/test_rounding.py
  V2 (scope): diff confined to src/billing/ and tests/billing/
  V3 (scope): no new dependencies — the manifest stays byte-identical
```

The reproduction lands red as vowed. Then friction: the correct fix is bankers' rounding, and its natural home is the shared money helper — outside the vowed scope. The vow stops the edit before it happens, not after:

```
V2 is about to break: the clean fix moves round_half_even into
src/common/money.py, outside the vowed scope. Options:
  (a) widen V2 to include src/common/ — one new file, no behavior
      change for other callers
  (b) keep the helper private to billing, file the extraction as follow-up
Which?
```

The user picks (a); V2 is amended in place, at the moment of approval. The fix lands, and the done claim arrives as an audit, not an adjective:

```
Vow audit:
  V1 kept — test_rounding.py::test_half_cent_line red at 4c9e21f,
      green at 8802a3d
  V2 amended — scope widened to src/common/ before the edit, on approval;
      git diff --stat shows those three files and nothing else
  V3 kept — manifest untouched
```

"Fixed" now rests on three checkable lines instead of the agent's confidence — and the near-breach sits in the transcript as a decision, not in the review as a surprise.

## Anti-patterns

- **The unfalsifiable pledge.** "I'll keep changes minimal", "I'll be careful with scope" — no diff can break it, so no diff is bound by it. The block reads as reassurance and functions as nothing.
- **Vow spam.** Ten pledges declared, none referenced again; the transcript shows the block written once and consulted never. Three vows the task could actually violate outbind ten that decorate it.
- **The post-hoc vow.** The block appears — or quietly grows — after work has begun. Pre-commitment written in the past tense is a report wearing an oath's clothes; its position in the transcript is the tell.
- **The silent breach.** The audit says kept while the diff says otherwise, or a broken vow simply vanishes from the audit. One discovered instance costs every future audit its trust — this is the breach that forfeits the ability.
- **Vowing the harness.** "I vow not to force-push" in a sandbox that cannot push. Pledging enforced guarantees pads the block, and readers learn to skim it.
- **Done means, pasted.** Every bullet of every engaged skill copied in as vows. No selection means the task was never read; the three that bind are buried under the nine that don't.

## Done means

- The vow block is in the transcript before the first action — under the engagement line when en is running — with at most three discipline vows tagged to their source skills and at most three scope vows, every one falsifiable.
- An audit precedes any done claim: every vow verdicted kept, amended, or broken, each with one line of evidence a third party can check against the diff or the run.
- Any near-breach was surfaced before the violating edit and renegotiated in the open, the amendment fixed in the transcript at the moment of approval.
- No vow duplicates a guarantee the runtime already enforces.
- A vow broken without renegotiation ended in a withheld claim and a named breach, not a softened adjective.
- Vows that break across repeated engagements were handed to hatsu with their transcripts, as forge evidence.
