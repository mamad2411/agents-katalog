---
name: fix-promotion-gate
description: >-
  Decide whether a candidate security patch may leave the sandbox, pass QA and
  become a merge request against the mainline. Use when an agent or a developer
  proposes a fix for a confirmed finding, when a green CI run is being treated
  as proof a vulnerability is closed, or when deciding what a security fix must
  prove before review.
allowed-tools: Read, Grep, Glob, Bash
---

# What must a fix prove, and where, before anyone is asked to review it

A green pipeline says the tests that exist still pass. For a security patch
that is the wrong question, because the tests that exist were written by people
who did not know about this bug — if they had, it would not be here.

There are three ways to make a finding stop firing and only one of them is a
fix: **fix the vulnerability**, **delete the feature**, or **evade the
detector**. All three turn CI green, and an autonomous loop optimising for
green finds the second and third on its own, because they are cheaper.

The pipeline has something a static workflow does not: Phase 4 already built a
**working exploit**, and C2.6 already built a **replica** to run it against. So
the fix has somewhere to be proven before anybody is asked to look at it, and
the promotion path is three environments with a different question at each:

| where | the question | what it catches |
|---|---|---|
| **sandbox replica** | does the exploit still work? | the patch that only moved the pattern |
| **QA** | does the application still do what it did? | the patch that closed the bug by breaking the feature |
| **merge request** | is this the mechanism we want? | the design question no gate can answer |

Skipping the first is the common failure, and it is always justified the same
way: the fix is obvious.

## When to use this

On every patch for a confirmed finding, whether an agent or a person wrote it,
before the merge request exists. Also when reviewing a remediation workflow that
opens merge requests directly from a scanner going quiet.

## Procedure

**1 — Re-run the exploit against the patched build, in the replica.** Not the
scanner. The exploit is the only acceptance test that cannot be satisfied by
editing the code around a detector. A patch that leaves the exploit working has
failed regardless of what the scan says.

**2 — Prove the exploit still works against the *unpatched* build.** Same run,
same harness. Without this you cannot distinguish "the fix worked" from "the
probe broke", and a probe that silently stopped asserting reports every patch
as a success.

**3 — Run the regression suite in QA, against real-shaped data.** Behaviour
preserved is a separate claim from vulnerability closed, and the patch that
closes a SQL injection by returning an empty list satisfies the first gate
perfectly.

**4 — Diff the findings, both directions.** The target finding must be gone and
nothing new may appear. A patch that closes one injection and opens a path
traversal has a net score of zero and a merge request that says "fixes CVE".

**5 — Only now open the merge request, and put the evidence in it.** The
exploit run before and after, the regression result, the finding diff. A
reviewer's remaining job is the question no gate can answer — whether this is
the mechanism the codebase should use — and they can only get to it if the
first three are already answered on the page.

## Example

**Input** — the fixture committed at the top of [`scripts/fix_promotion_gate.py`](scripts/fix_promotion_gate.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
the exploit, against the unpatched build in the replica
   reproduces: True   <- if this were False the probe is
               broken and every result below would be meaningless

      CI   exploit  behaviour  new  promoted to
   A  ok   blocked  same       0    merge-request
   B  ok   blocked  CHANGED    0    rejected  <- qa: behaviour changed
   C  ok   WORKS    same       0    rejected  <- sandbox: exploit still works
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "candidates": [{"id": "str", "ci_green": true, "exploit_blocked": true,
                  "behaviour_preserved": true, "new_findings": 0,
                  "promoted_to": "rejected|qa|merge-request", "died_at": "str"}],
  "would_merge_on_ci_alone": 0,
  "merge_requests_opened": 0,
  "evidence_attached": ["str"]
}
```

`would_merge_on_ci_alone` against `merge_requests_opened` is the number this
procedure exists to produce. If they are equal, the gates changed nothing and
one of them is not actually running.

## Failure modes

- **Treating a green scan as proof.** It is proof the detector is quiet, and
  three of the four ways to quieten a detector are not fixes.
- **Skipping the replica because the fix is obvious.** The obvious fixes are
  where evasion hides, because nobody re-reads them.
- **Omitting the proof-of-fix run against the old build.** A broken probe then
  passes every patch.
- **Opening the merge request without the evidence.** The reviewer re-derives
  it, badly, or approves on the strength of the description.
