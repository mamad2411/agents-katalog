---
name: swarm-accept
description: Prepare a human acceptance decision in Swarm Oversight Harness — check the evidence behind an output, run an adversarial red-team pass on it (or on a SPEC), and present a short accept / reject / revise brief. The agent never accepts on the human's behalf. Use when the user says "is this ready to accept/merge", "review before I sign off", "red-team this spec/result", "what's in the accept queue".
---

# Swarm Oversight Harness · Accept gate

Acceptance moves an output across the trust boundary, from draft to accepted. Depending on the profile, that means branch → main, run → current best, or finding → accepted conclusion. Accepted content is trusted by default from then on, so this gate is where the human's attention is worth spending. Your job is to help the human decide quickly and with the right information. **You do not make the decision.**

Full rationale: [MANUAL.md](https://github.com/cogito233/swarm-oversight-harness/blob/main/MANUAL.md) §4.

## 1 · Collect the candidate

From STATE's accept queue (or whatever the user points to), gather the output, its SPEC/TASK, the RESULT, and the verification evidence.

## 2 · Check the evidence, not the story

- Does each acceptance criterion have evidence that someone other than the worker can re-check (command, observed output, path)? Re-run the cheap checks yourself.
- Are the six stage facts stated separately (edited / committed / launched / ran OK / verified / accepted)? Anything inferred is `unknown`.
- Was verification done by someone other than the worker?
- Could the proxy have been gamed, for example by deleted or weakened tests, skipped cases, hard-coded outputs, or a judge from the same source as the generator?
- Are headline numbers taken from the source of record rather than copied?

## 3 · Red-team

Spawn (or act as) an agent with **no stake** in the work. Its only job is to list concrete ways in which this output, or the SPEC behind it, is wrong, overclaims, or will break later. The agent exposes problems; the verdict stays with the human. Keep the 3 strongest findings.

## 4 · Brief the human (one screen)

```
Candidate: <what>          Profile gate: <tests / eval / red-team>
Criteria:  <n/m met, with evidence links>      Unknown: <list or none>
Strongest objections: 1) … 2) … 3) …
Reversibility: <cheap to undo? irreversible?>
Recommendation: accept | revise (what) | reject (why)
```

Depth follows reversibility: an irreversible change gets a deep check, and a change that is easy to revert gets a light one. Now and then, read a sample of raw code or data in depth to keep calibrating how much you trust the verifier.

## 5 · After the human decides

Only after the human has explicitly decided, record the decision (merge, promote the run, or mark the finding `tier: accepted`), add a DECISIONS entry if it was a real decision, and update STATE. A rejected output stays outside the boundary, and nothing already accepted is touched.

## Never

- Accept, merge, or promote on your own judgment.
- Present the planner's summary as the evidence.
- Hide an unknown to make the brief look clean.
