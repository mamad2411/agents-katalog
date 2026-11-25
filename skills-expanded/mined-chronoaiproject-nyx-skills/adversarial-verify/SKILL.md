---
name: adversarial-verify
description: "Subject a claim to two independent skeptical reviews pass only if neither refutes."
metadata:
  category: runtime-based
  tag:
    - "verification"
    - "quality"
  output-type: text
  runtime:
    - "aevatar-workflow"
version: "0.1"
---


# Adversarially verify before trusting

This skill runs a prebuilt aevatar workflow (`adversarial_verify`) that subjects one claim to
**two independent skeptical reviews** and lets it pass **only if neither reviewer can refute it**.

The core insight: a single reviewer (especially the same model that produced the output) shares
the biases and blind spots that created the error. Two reviewers attacking the claim from
**different angles** — one hunting logic/correctness flaws, one hunting evidence/assumption flaws —
break that shared failure mode. Both must fail to refute for the claim to pass.

A run does four things, in order:

1. **Capture** — the run prompt (the claim plus any supporting context) is snapshotted so every
   reviewer sees the *same* inputs.
2. **Logic review** — one `llm_call` plays a correctness adversary: it attacks reasoning, internal
   consistency, and edge cases, and defaults to **REFUTED** when uncertain.
3. **Evidence review** — a second, independent `llm_call` plays an evidence adversary: it attacks
   unsupported claims, fabricated facts, and unstated assumptions, and also defaults to **REFUTED**
   when uncertain.
4. **Converge + verdict** — a deterministic gate passes **only on unanimous "NOT_REFUTED"**; the
   terminal step emits the final verdict plus both reviewers' reasoning.

There are **no external calls** — verification is pure reasoning (`llm_call`) plus a deterministic
convergence gate. The run itself is the record, watchable in the observatory.


## Protocol (follow in order)

1. **Decide it is worth gating.** Use this for output that will be shipped, published, or acted on,
   where a wrong answer is costly. For internal drafts or anything a build/test/lint can check
   deterministically, skip this and use the deterministic check instead.
2. **Compose the run prompt as `claim + context`.** The prompt is the *whole* input both reviewers
   see, so make it self-contained: state the **claim/output under review** explicitly, then include
   the **supporting context** (the source material, the reasoning, the data) the reviewers should
   judge it against. A claim with no context will be refuted on principle — that is by design (the
   reviewers default to REFUTED when they cannot confirm).
3. **Run it.** Call `aevatar_start_workflow` with `workflow_id: "adversarial_verify"` and
   `inputs.prompt` set to the claim+context. It is **fire-and-observe**: a `run_id` with
   `accepted`/`streaming` is the structural pass — do not poll for `run_finished`; the run finishes
   asynchronously and is watchable in the observatory.
4. **Report honestly.** Return the verdict (PASS / REFUTED) and both reviewers' reasoning, plus the
   observatory link. State that this is an **adversarial reasoning** check — it catches logic and
   evidence flaws a single review misses, but it does **not** prove correctness (two reviewers can
   still share a blind spot). A PASS means "neither independent skeptic could refute it," not a
   guarantee.

> **Reading the verdict.** PASS requires *both* reviewers to return `NOT_REFUTED`. If **either**
> reviewer refutes, the verdict is REFUTED — because if only one skeptic catches an issue, that
> issue is real and the other reviewer's silence is exactly the blind spot this pattern exists to
> eliminate. A REFUTED verdict is a useful result, not a failure of the run.


## Inputs

| Input | Where | Purpose |
|---|---|---|
| `prompt` | `inputs.prompt` | The claim/output under review **plus** its supporting context. Required — it is the only thing both reviewers see. Make it self-contained; a context-free claim is refuted by design. |

## Output

A single text verdict block:

```
VERDICT: PASS | REFUTED
LOGIC REVIEW (correctness adversary):  <verdict + reasoning>
EVIDENCE REVIEW (evidence adversary):  <verdict + reasoning>
```

Also persisted as the run record in the observatory.


## Scope (what this draft deliberately does and does not do)

- **Does:** capture one claim, run two genuinely-different independent skeptical reviews, converge
  on a unanimous gate, emit a parseable PASS/REFUTED verdict with both rationales — no external
  calls, observatory-visible.
- **Does not (v1):**
  - **Generate or fix the claim.** This is a post-hoc *verification* layer, not a generator and not
    a fix-until-nice loop. The convergence loop (refute → fix → re-review until it passes) is a
    separate concern — verification just returns the verdict; the caller decides whether to fix and
    re-run.
  - **Use more than two reviewers.** Exactly two, with fixed distinct angles (logic vs evidence).
    Adding a third reviewer or a domain-specific angle is a clean extension, but two independent
    skeptics is the minimum that breaks single-reviewer blindness and the cheapest gate that does.
  - **Fetch external evidence.** Reviewers judge the claim against the context *given in the prompt*
    only — they do not browse or call connectors. If a claim needs live evidence, collect it first
    (e.g. with a collect/search skill) and pass it in as context.
  - **Compute counts or scores deterministically.** The reviewers return a categorical verdict
    (`REFUTED` / `NOT_REFUTED`), never a numeric score the LLM made up; the unanimity gate is the
    only arithmetic and it is done deterministically.

See `DESIGN.md` for the full ECC → aevatar mapping, why there is no connector, how the convergence
gate is built from documented primitives, and the verification checklist.
