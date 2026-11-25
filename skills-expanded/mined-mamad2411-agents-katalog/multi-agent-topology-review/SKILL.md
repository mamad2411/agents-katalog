---
name: multi-agent-topology-review
description: Challenges and reviews proposals for multiple cooperating agents, arguing against unnecessary multi-agent designs with cost and failure-rate evidence. Use when a design proposes subagents, a swarm, an orchestrator or supervisor, agent handoffs, parallel agents, or agent-to-agent negotiation; when deciding how many agents to emit for a decomposed codebase; or when a single-agent design is being split up for reasons other than a named, measured constraint.
---

# Multi-agent topology review

> **Standing: v1, and its default position is now the v1 architecture.** `plan.md` OD-09 (2026-08-02)
> removed decomposition-into-agents from v1, so **"one agent" stopped being this skill's recommended
> default and became the shipped design** (D-11, D-21). Two consequences worth holding apart. **This
> skill still applies to v1** — it is the thing to reach for when someone proposes splitting the
> runtime, and its five-gate test is the right answer to that proposal. **But it did not win its
> argument; it won by forfeit.** The arm that would have tested one-agent-with-the-full-budget against
> the best multi-agent arm (`11` Phase 3, A5) never ran. Do not cite v1's shape as evidence for the
> default. **The `codebase-decomposition` skill it pairs with is v2.**

Source: `research/01-agent-anatomy.md` §7; standing per `research/14-architecture-synthesis.md`
D-11, D-21.

**Default position: one agent with an excellent tool layer.** Reach for multi-agent only when you
can name the specific property that makes it necessary. Most vendor framing has this backwards.

**One caveat OD-09 puts on the second half of that sentence:** v1 does not have an excellent tool
layer, it has a shell and a socket. The default holds; the reason it holds is now *nobody measured a
benefit*, not *the single agent's tools are good enough*.

When reviewing a multi-agent proposal, your job is to **argue against it** until the five-gate test
below passes. Emitting more agents is not evidence of a better design.

## The five gates

Multi-agent earns its keep only when **all five** hold. Fail any one and a single loop with a bigger
budget, a better model, and better tools beats it on cost, latency, *and* reliability
simultaneously.

```
- [ ] 1. The task decomposes into threads that are GENUINELY independent —
         no thread's output constrains another's.
- [ ] 2. The threads are READ-ONLY, or writes are partitioned so cleanly
         that merge is mechanical.
- [ ] 3. Total evidence EXCEEDS one context window and cannot be reduced by retrieval.
- [ ] 4. The task value ABSORBS a ~15× token multiplier.
- [ ] 5. There is somewhere to put a VERIFICATION PASS on the synthesis.
```

## The economics

| Configuration | Tokens vs. plain chat |
|---|---|
| Chat interaction | 1× |
| Single agentic loop with tools | **~4×** |
| Multi-agent system | **~15×** ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)) |

([Anthropic, *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system))

That is the *baseline*, not the tail. A subagent that recursively spawns subagents, or a tool
returning an oversized result into N contexts at once, multiplies again — and the published
architecture ships **no per-run circuit breaker**. If you build one, the cap is your job.

**The finding that reframes the whole decision**, in Anthropic's own words: *"Multi-agent systems
work mainly because they help spend enough tokens to solve the problem."* On BrowseComp, three
factors explained 95% of performance variance, and **token usage alone explained ~80%** — tool-call
count and model choice made up the rest. Coordination sophistication is not on the list.

So the correct control experiment is **not** "multi-agent vs. single agent." It is **"multi-agent vs.
single agent with a 15× larger turn/token budget."** ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)) Most published multi-agent wins never ran that
comparison. Ask for it. Anthropic further notes that *upgrading the model* beat doubling the token
budget — so the cheapest lever is usually neither architecture nor budget but a better model on a
single loop.

## The four costs worse than tokens

- **Context fragmentation.** A worker returns 200 tokens of conclusion; the 20k tokens of evidence
  and dead ends that produced it are gone. The lead cannot audit the conclusion or notice that two
  workers contradicted each other.
- **Implicit decision conflict.** *"Actions carry implicit decisions."* Two workers writing code each
  pick a naming convention, an error-handling style, an edge-case interpretation. Neither choice was
  in the spec. They collide at merge. **No amount of context sharing fixes this**, because the
  decisions were never articulated to be shared.
- **Error compounding.** Reliability multiplies. At 95% per-agent success, a 5-stage pipeline lands
  near 77% and a 10-stage pipeline near 60%. Lusser's Law does not care that the components are
  language models.
- **Debugging.** One agent produces one linear trace. An orchestrator with six workers produces
  seven interleaved traces plus a merge, and the bug is usually in the seam — the part no trace
  covers. Budget real engineering for distributed tracing *before* fanning out.

## The MAST failure data

Berkeley's MAST study hand-annotated 200+ execution traces across seven open-source multi-agent
frameworks (MetaGPT, ChatDev, HyperAgent, OpenManus, AppWorld, Magentic, AG2) with six expert
annotators (Cohen's κ = 0.88) and found **failure rates of 41%–86.7%**, with ChatDev at 33.3%
correctness on their ProgramDev benchmark
([arXiv:2503.13657](https://arxiv.org/html/2503.13657v2)).

| Category | Share of failures | What it looks like |
|---|---|---|
| **Specification / system design** | ~37% | Bad role definitions, ambiguous decomposition, **missing termination conditions** |
| **Inter-agent misalignment** | ~31% | Format mismatch across the seam, context collapse, contradictory state |
| **Task verification** | ~31% | No check on intermediate outputs; a hallucination propagates downstream unchallenged |

**Roughly two-thirds of multi-agent failures are architecture and plumbing, not model quality.** A
better model does not fix a missing termination condition. The largest single sub-category is
missing termination conditions — which is why budgets and typed terminals are non-negotiable at the
promotion boundary (see `contract-derived-verification`).

Note: MAST's authors used an LLM-as-judge pipeline to scale annotation. Treat that tooling with the
caution documented for judge reliability.

## The read/write asymmetry — the most useful rule here

**Parallel read is nearly free of the failure modes above. Parallel write is where they all live.**

The asymmetry is structural, not incidental:

- A read has **no side effects to conflict**. Two workers writing the same file produce a merge
  conflict or a silent last-write-wins.
- Reads are **idempotent and retryable**. A half-applied write costs correctness and may not be
  safely retryable.
- A read worker's output is **a claim you can verify** against the source. A write worker's output is
  **a state change you must reconcile** with every other write.
- Reads carry **no implicit decisions**. Writes carry nothing but implicit decisions.

Cognition's position after ten months of shipping: *"multi-agent systems work best today when writes
stay single-threaded and the additional agents contribute intelligence rather than actions."*

**The rule:** fan out freely for retrieval, search, analysis, and review. **Funnel all mutations
through one writer.** If you truly need parallel writes, partition by disjoint resource — separate
files, tables, services — and treat any shared resource as requiring a lock, exactly as with
threads. The analogy is not loose; it is the same problem.

## Topology ranking

| Topology | Verdict |
|---|---|
| **Orchestrator-worker with read-only workers** | The only topology with a strong track record |
| **Sequential pipeline** | Really a workflow wearing an agent costume — and that is fine. Most debuggable option; reach for it before anything fancier |
| **Hierarchical** | Beginning to work at one vendor with a lot of dedicated context engineering. Cost explosion, no natural circuit breaker |
| **Network / peer** | A research aesthetic. *"Arbitrary networks of agents negotiating with each other is mostly a distraction. The practical shape is map-reduce-and-manage"* (Cognition, 2026) |

## The apparent Anthropic-vs-Cognition disagreement is not one

Anthropic measured **research** — read-heavy, wide, shallow, decomposable. Cognition measured
**coding** — write-heavy, deep, narrow, tightly coupled. Anthropic says so explicitly: *"most coding
tasks involve fewer truly parallelizable tasks than research."*

**The deciding variable is task coupling, not architecture taste.** When someone cites Anthropic's
multi-agent results to justify a code-writing swarm, that is the error.

## Steal the patterns without paying the multiplier

Three genuinely portable patterns from Anthropic's system, all runnable **inside a single agent**:

1. Externalize state to memory before context fills.
2. Give workers self-contained task descriptions.
3. Verify high-stakes outputs with a separate clean-context pass.

The clean-context reviewer is the strongest of the three: a reviewer sharing *no* context with the
coder catches ~2 bugs per PR on PRs Devin itself wrote, ~58% of them severe. Withholding context
helps — the reviewer reasons backward from the implementation and its short context dodges context
rot.

One that did **not** work: "smart friend" escalation from a weaker primary model to a frontier model
as a tool. A weaker model does not know when it is at its limits or what to ask — *"the quality
ceiling was set by the primary, and the primary wasn't strong enough."* It works frontier-to-frontier,
where it stops being a difficulty escalator and becomes a **capability router**.

## What this means for `function2agent`

- **A promoted function is a worker; build it to be a good one.** Self-contained task description in,
  distilled and token-bounded result out, no assumption of shared state with the caller.
- **`read_only` is first-class metadata on the promotion artifact, not a comment.** A `read_only:
  true` function is safe to fan out N ways. A writing function needs a declared resource scope so a
  scheduler can refuse to run two conflicting instances concurrently. You get this nearly free — the
  signature and body already tell you.
- **Do not build a swarm runtime.** Build a single-agent runtime with a great tool layer and let
  orchestrator-worker fall out of "a promoted function can call another promoted function."
- **Enforce budgets at the promotion boundary** — max tokens, max depth, max wall clock. MAST's
  largest failure category is missing termination conditions, and a system whose premise is turning
  functions into agents will otherwise let someone build unbounded recursion by accident.
