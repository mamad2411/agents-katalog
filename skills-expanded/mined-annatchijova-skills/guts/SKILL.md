---
name: guts
description: Investigate what happens to untrusted data after the system processes it, especially when its derived artifacts (summaries, memory entries, caches, logs, error text, tool results) are consumed again. Use when a finding is confirmed or a hunt stalls at the sink; when an agent or pipeline summarizes, stores, retrieves, or forwards external content; when one component trusts data because another already handled it; or on mentions of provenance loss, memory poisoning, re-ingested logs, cache reuse, fecal, caca, mierda, or shit residue, or trust labels that exist but are not enforced. Requires the chain source, transformation, by-product, consumer, trust boundary, observable effect, with evidence per link under a stated threat model. NO FINDING and ABSTAIN are legitimate results. Not conventional source-to-sink taint analysis and not severity escalation of a known bug; variants of one invariant go to variant-analysis.
---

# GUTS — Gastrointestinal Untrusted-data Tracing System

**Central question:** What happens to untrusted data after the system processes it, especially when its derived artifacts are consumed again?

Do not assume the vulnerability ends where the observable failure ends. Trace what entered, what changed, what circulated, what survived, and what was discarded.

## Scope

- **Not conventional source-to-sink taint analysis.** GUTS follows derived artifacts beyond the first sink, including subsequent transformations, consumers, and re-ingestion. It builds on established ideas (taint and label propagation; stored or second-order injection is the usual name for part of it) and claims no new technique, only an order of investigation.
- **Not severity escalation.** GUTS does not ask how to make a known bug worse (that is the gate in `dont-fall-in-love-with-the-bug`). A result that matters only as "the original bug, but worse" is out of scope. A GUTS finding stands on its own chain.
- **The metaphor generates hypotheses; it is never evidence.** Apart from the two named patterns below, reports use plain vocabulary: trust boundary, provenance, derived artifact, consumer. A concept that cannot be stated as a computational mechanism is dropped.

## Two mechanisms, investigated separately

- **Provenance loss.** The data changes representation (summary, embedding, cache entry, log line, rewritten file) and loses its origin or trust label. Test: compare the label on the producer's output with the label on the next consumer's input. If no label was ever assigned at entry, that is the first result, and downstream loss cannot be shown.
- **Provenance enforcement failure.** The label is preserved, but a downstream consumer does not apply the restrictions it implies. Example: a tool result keeps its UNTRUSTED label, yet another component uses it to authorize a privileged operation. Test: change only the label and check whether the consumer's decision changes.

A provenance label is not a control. Its existence shows that someone tracked origin, not that any policy depends on it.

## Procedure

Seven phases. Record for each what was examined and what was not. With limited budget, start at phase 6.

1. **Entry.** Entry points, parsers, deserializers, size and type limits. Record the trust level assigned at entry.
2. **Transformation.** Normalization, decoding, truncation, summarization, coercion. Per step: which properties of the input are preserved, lost, or created, including its origin label.
3. **Storage.** Where derived artifacts settle: memory, agent context, shared state, caches, vector stores, temp files. Who can write, who reads, and what label travels with the artifact.
4. **Amplification.** Chained transformations that multiply size, cost, or meaning. GUTS owns the chain and its by-products; a finding that is purely about cost goes to `resource-exhaustion-review`. Amplification of meaning (a summary that turns quoted text into an instruction-shaped statement) stays here.
5. **Residue (Fecal Analysis).** Inspect the by-products the system discards or emits outside its main output: logs, error text, traces, partial outputs, cleanup leftovers. Ask what attacker-influenced or sensitive content leaves through a channel nobody classified as output, and who reads it afterwards. What should have been recorded: `forensic-logging-design`.
6. **Re-ingestion.** Derived artifacts or residue that come back as input: summaries reused as context, tool results fed to another component, logs read by an agent, caches reprocessed, exports re-imported. This is the distinguishing phase of the skill.
7. **Survival.** Derived artifacts that cross a lifetime boundary (session, user, restart, rollback, retry) and are read again on the other side under a different trust assumption. In scope only if some consumer reads them. Whether state restores correctly or is tamper-free belongs to `recovery-integrity`.

## Second-hand shit

**Second-hand shit:** component B trusts data because component A already processed it, but A's processing never removed its untrusted character.

Look for derived artifacts that gain authority they did not have by passing through another component: B treats them as instructions, as authorization, as verified, or as safe to render or execute. Re-ingestion is not a vulnerability by itself. Before reporting, state:

1. the trust guarantee B relies on (for example "operator-authored" or "passed validator V");
2. why A's processing does not establish that guarantee for the derived artifact (a validator that checks format establishes format only);
3. the observable consequence if the guarantee is false.

Without all three it is an observation, not a finding.

## Evidence contract

Every finding is written as the chain:

`source → transformation → by-product → consumer → trust boundary → observable effect`

Each link needs evidence suited to its kind: code inspection, instrumentation, trace, contract or schema, test, or state diff. A separate runnable reproduction per link is not required. Say which kind of evidence each link rests on and pin version and configuration. Then label each link:

| Link status | What earns it | Ladder label |
|---|---|---|
| Structural | Read from the code. Shows the path exists, not that attacker input can traverse it. | CODE FACT |
| Observed | Seen in a pinned trace, execution, or state diff. Shows what happened in that run, not what the code necessarily guarantees. | OBSERVED BEHAVIOR (cite the run) |
| Unverified causal | Inferred from architecture or behavior; not executed. | PLAUSIBLE HYPOTHESIS |
| Effect confirmed | A prediction stated beforehand was executed and held for this link. | CONFIRMED BY INDUCTION, link scope |
| Chain confirmed | The whole chain reproduced end to end under an explicit threat model, prediction fixed before the run. | CONFIRMED BY INDUCTION, chain scope |

A chain is confirmed only when reproduced end to end. Otherwise report it at the level of its weakest link, never as confirmed exploitation. Epistemic classification and how claims travel: `claim-provenance-discipline`. Threat model, reproducibility contract, and the right to write CONFIRMED: `red-team-auditing`. GUTS restates neither.

## Results

Recorded per phase and per hypothesis:

- **CONFIRMED BY INDUCTION**: chain or link, with its scope.
- **FALSIFIED**: one concrete prediction failed under stated conditions. Record the hypothesis and prediction (written before the run), configuration and conditions, observed result, exact scope of the refutation, and conditions not examined. It does not rule out the class: another representation, boundary, consumer, or configuration can still hold it.
- **NO FINDING**: a phase or surface was examined and no hypothesis survived. State coverage and what was not examined.
- **ABSTAIN**: no conclusion is possible: insufficient evidence, no access, or a probe not shown able to detect the effect.

NO FINDING versus ABSTAIN depends on probe sensitivity. If you have not shown the probe can see a planted positive, the honest result is ABSTAIN. Design canaries to survive the transformation under test (a summarizer can drop an exact string); experiment design is `discriminating-proof`.

Never produce a finding to justify the run. "Nothing found under this strategy, context, and budget" is not "nothing exists"; say which one you are claiming.

## Boundaries

| Skill | It owns | GUTS does not |
|---|---|---|
| `agent-trust-boundaries` | Design-time rules: channel authority, labels that stay attached, deterministic policy, the mitigation ladder | Prescribe controls. GUTS tests whether an existing system meets those rules |
| `variant-analysis` | The same invariant at sibling sinks and other code | Sweep call sites. GUTS follows one artifact downstream; "same invariant elsewhere" is handed over |
| `red-team-auditing` | Epistemic ladder, threat model, reproducibility; also who can alter memory state | Confirm adversarially. GUTS asks what trust label memory carries when read back |
| `dont-fall-in-love-with-the-bug` | The gate before any report | Skip it. A GUTS finding passes that gate before writing up |
| `data-provenance-mapping` | Where data lives and flows across the organization | Map copies. GUTS reuses such a map if one exists and asks what authority derived artifacts gain |
| `resource-exhaustion-review` | Cost asymmetry and unbounded work | Analyze cost (phase 4) |
| `recovery-integrity` | Restorability and tamper-freedom of recovery | Analyze recovery (phase 7) |
| `beyond-the-fix` | Auditing patches | Audit the causal role of a patch. Delegate a correction that remains incomplete, or a vulnerability introduced by the patch, when that relationship is established; a pre-existing defect stays with the skill that owns its mechanism. GUTS retains downstream re-ingestion analysis when the artifact chain, not the patch's causal role, is the mechanism |
| `discriminating-proof` | Cheapest experiment that can kill a hypothesis | Design experiments, beyond the canary caveat above |
| `claim-provenance-discipline` | Level, scope, and falsifier of every claim | Classify claims |

Also: a validator or filter that exists but may not resist the threat belongs to `control-effectiveness-vs-existence`; input handling at entry (paths, names, encodings) belongs to `validate-at-the-boundary`.

## Output

Per phase: examined, not examined, hypotheses, result. Then each confirmed or open chain with a status for every link, and one class-level question: what does this architecture assume about derived data, and where else does it make that assumption? A worked example of filling the link table when most of the chain is still unexamined: `references/memory-reingestion-example.md`.
