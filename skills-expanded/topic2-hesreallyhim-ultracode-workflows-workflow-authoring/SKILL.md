---
name: workflow-authoring
description: Designs, authors, reviews, and improves reusable Claude Code Workflow scripts by composing proven orchestration patterns from the ultracode-workflows catalog. Use when a user asks to turn a recurring task into a workflow, create or revise a .claude/workflows script, choose a multi-agent topology, compare a proposed workflow with catalog precedents, or diagnose why an orchestration is wasteful, brittle, misleading, or unable to converge.
---

# Workflow Authoring

Treat the marketplace as a casebook of reusable orchestration designs. The built-in Workflow tool already supplies the execution model; this skill adds authorship judgment: deciding whether a workflow is warranted, selecting compatible patterns, adapting them without copying accidental details, and making the resulting script honest about cost, uncertainty, failure, and coverage.

Prefer a small script with one defensible idea over a miniature workflow framework. A workflow earns its overhead when several agents can contribute genuinely different evidence or when an explicit trust structure—independent verification, a completeness critic, falsification, or a bounded repair loop—materially improves the result. Recommend an ordinary prompt or one agent when the work is short, tightly sequential, or cannot be partitioned without duplicating context.

This skill also provides an optional user-facing design process. Its value is not that a user must out-author Claude; it makes Claude’s orchestration choices inspectable and revisable before the workflow is trusted. When the user invokes the skill or `/wf-new`, expose the major decisions, teach the few composition patterns that matter to this design, and show the static diagram rather than silently producing a script.

## Reference routing

Read only what the task needs, but read the selected reference completely.

| Reference | Use it for |
|---|---|
| `references/catalog-patterns.md` | Start here when selecting precedents, combining two catalog shapes, or deciding what *not* to copy |
| `references/patterns.md` | Read when reasoning about barriers, convergence, verification, diversity, sharding, composition, or human checkpoints |
| `references/api-contract.md` | Consult while drafting or debugging syntax, metadata, args, schemas, failure behavior, budget, and resume safety |
| `references/exemplar.md` | Use when a complete mid-sized script would be more useful than isolated rules |
| `${CLAUDE_PLUGIN_ROOT}/workflows/<name>.js` | Read the two or three nearest shipped examples before inventing a new topology |
| `${CLAUDE_PLUGIN_ROOT}/scripts/diagram-workflow.mjs` | Optionally render an advisory terminal view after static source review; Mermaid is an explicit artifact format |

## User-invocable design studio

Unless the user explicitly requests a direct implementation, conduct authoring as a short design studio with visible intermediate artifacts:

1. **Orchestration brief.** Restate the reusable input, desired structured result, reason to use multiple agents, highest-cost failure, and whether the workflow may mutate anything.
2. **Candidate shapes.** Present one recommended catalog composition and at most two meaningful alternatives. Name the borrowed patterns and concrete shipped precedents; explain the tradeoff in ordinary language rather than API terminology.
3. **Control points.** Surface only choices that materially change the result: breadth versus verification depth, default-to-refute versus default-to-keep, report-only versus opt-in mutation, the cost envelope, and any human checkpoint. Make a recommendation instead of turning the session into a questionnaire.
4. **Static draft and diagram.** Draft the smallest script that represents the selected shape, review it as inert source, and generate the static terminal diagram without running it. The diagram is the shared object the user can react to.
5. **Guided explanation.** Walk the diagram from input to result. Point out why work is pipelined or synchronized, where independent skepticism enters, how loops stop, which widths are exact/ranged/unknown, and where the user regains control. Teach only the patterns visible in this workflow.
6. **Revision pass.** Invite targeted changes such as “cheaper,” “more adversarial,” “report-only,” “add a checkpoint,” or “cover the long tail.” Translate them into topology changes and regenerate the diagram before final delivery.

Keep this planning dialogue outside the workflow itself. The authoring session can ask the user questions; a running workflow cannot pause for interaction and must return checkpoint data instead. Never present the diagram as proof that the workflow is safe or that its runtime cost is fully known.

### Budget and duration control

Offer a recommended **balanced** profile plus **quick** and **deep** alternatives when the topology has meaningful cost choices. Translate the profile into actual script structure rather than adjectives:

| Lever | Quick | Balanced | Deep |
|---|---|---|---|
| Discovery breadth | fewer, broader charters | distinct catalog-derived lenses | more modalities or rotating rounds |
| Verification | one skeptic on high-risk claims | one skeptic per material claim | severity-scaled or majority panels |
| Effort | low for mechanics, default for judgment | tiered by stage | high only for the hardest critics/judges |
| Iteration | one pass or a small cap | bounded convergence/repair | larger cap with the same honest stop rule |
| Mutation | report-only | opt-in, narrowly sharded | opt-in plus stronger pre/post evidence |

Treat these profiles as presets, not locked bundles. Let the user override breadth, verification width, effort, or round caps independently. Before drafting, ask for or propose a token ceiling and desired wall-clock target when those constraints matter; if both are tight, ask which is the harder constraint and show the quality or coverage traded away. Recalculate the topology and estimate card after a control changes so “cheaper” or “faster” produces a visible structural difference rather than a verbal promise.

The session supplies `budget.total`; the script can scale fleets and stop launching new work relative to that target, but it cannot create the session budget itself. Likewise, deterministic workflow code cannot enforce a wall-clock deadline with runtime clock calls, so duration control comes from structural limits. Then show a small estimate card containing:

- **Agent calls:** exact count, bounded range, or unknown tail—never collapse `×N` into a point estimate.
- **Peak width:** the largest statically visible concurrent fan-out, subject to the harness queue.
- **Sequential depth:** the longest dependency chain; use this, not total agent calls, as the basis for a duration discussion.
- **Budget controls:** fleet size, batch size, verification panel width, loop/repair caps, and `budget.total`/`budget.remaining()` guards.
- **Assumptions:** expected tool latency, likely input population, and whether agents perform builds, tests, browsing, or other slow operations.

Duration and token figures are planning estimates, not guarantees. Agent output length, tool calls, model latency, queueing, and runtime-discovered work can dominate. Prefer honest categories or ranges when calibration data is absent. Never execute the workflow with sample args merely to manufacture an estimate. Once the real run begins, direct the user to the web viewer for observed token spend and elapsed time; use the completed artifact for the exact recorded total.

## Authoring procedure

### 1. Frame the reusable decision

State the workflow in one sentence as `input → judgment/work → trustworthy result`. Identify the recurring part, the reason multiple agents help, and the error that would matter most. Do not begin with the number of agents.

Write down four constraints before choosing a shape:

- **Population:** bounded inputs, or an unknown tail that needs a convergence rule?
- **Dependence:** can each item advance independently, or does the next step truly need the whole field?
- **Trust:** what evidence would refute a candidate result, and which error direction is more costly?
- **Mutation:** report-only, disjoint edits, or a destructive/overlapping operation that must be funneled?

If these answers do not justify orchestration, say so and stop. The authoring outcome may legitimately be “this should remain a prompt, not a workflow.”

### 2. Select precedents and extract invariants

Read `references/catalog-patterns.md`, then inspect two or three shipped workflows:

1. Choose a **structural donor** whose dataflow resembles the task.
2. Choose a **trust donor** whose verification bias matches the cost of being wrong.
3. Optionally choose a **scale donor** if coverage, batching, or convergence is the hard part.

Extract each donor’s invariant, not its surface form. For example, the useful idea in `dead-code-sweep` is not “three agents”; it is independent discovery modalities followed by a default-to-keep skeptic because false deletion is expensive. The useful idea in `docs-drift-audit` is not its phase names; it is per-item pipelines with no unnecessary cross-item barrier.

Name rejected patterns too. A short design note such as “pipeline, because each file’s checker needs only that file’s extraction” or “barrier, because semantic deduplication must see the entire candidate set before expensive verification” prevents cargo-cult fan-outs.

### 3. Design the dataflow before prompts

Sketch a compact stage table:

| Stage | Input | Judgment or mechanics | Output contract | Concurrency | Failure meaning |
|---|---|---|---|---|---|
| Example: inventory | scope args | judgment | disjoint groups | one agent | abort honestly |
| Example: inspect | one group | judgment | findings schema | pipeline per group | omit failed group and report it |
| Example: aggregate | all findings | mechanics | ranked list + remainder | plain code | preserve uncertainty |

Start from the final structured result and work backward. Every downstream branch must receive a schema field with a constrained value; every completeness claim must have a count, manifest, reverse check, or explicit remainder; every agent return may be `null`.

Keep mechanics in code: slicing, stable-key deduplication, counting, vote tallies, ranking arithmetic, and cap enforcement. Use agents for judgments that require reading or interpretation. Do not spend an agent on formatting or on arithmetic the script can perform deterministically.

### 4. Compose the smallest sufficient topology

Use `pipeline` by default when an item’s next step depends only on that item. Introduce `parallel` barriers only when the following step requires all prior outputs: global deduplication, cross-item ranking, a field-wide judge, a join between independent analyses, or a convergence decision.

Apply trust where a false answer would survive otherwise:

- Independent skeptic for factual findings.
- Default-to-keep review for deletion or other asymmetric harm.
- One falsifier per competing causal hypothesis.
- Reverse-direction coverage critic for omission risk.
- Fresh-eyes re-verification when producers already self-checked.
- Characterization or empirical evidence before mutations that claim behavior preservation.

Apply scale patterns only when needed: manifest sharding for provable coverage, calibrate-then-shard for a shared classification vocabulary, leads-then-reads for expensive sources, waves with early abort for repeated mutations, and loop-until-dry only for populations with a real unknown tail.

Every loop needs a convergence signal, a hard cap, a budget guard, and a result field that distinguishes “dry” from “stopped.” Every cap must disclose its remainder. Workflows cannot ask the user questions mid-run; return open questions and accept answers on a later invocation.

### 5. Draft against the harness contract

Consult `references/api-contract.md` while writing. Do not reproduce the built-in tool documentation in the delivered explanation; apply the few contract rules that affect the script:

- Put a pure literal `export const meta = {...}` first, with `meta.name` matching the filename.
- Use only the injected workflow bindings and standard JavaScript built-ins.
- Define schemas for cross-agent data and `enum` values that code branches on.
- Make every prompt self-contained, including its charter, anti-charter, upstream data, and honesty valve.
- Pass thunks to `parallel`; use phase options inside concurrent pipeline stages.
- Treat `agent()` and child-workflow results as nullable.
- Avoid resume-breaking time and randomness calls.
- Make mutation opt-in, narrow, and followed by global evidence.
- Return queryable data, including uncertainty, dropped work, stop reason, and failed stages.

Prefer adapting a nearby shipped workflow over drafting from a blank file. Delete donor-specific fields, phases, and agent calls that do not defend an invariant in the new task.

### 6. Review statically—never run merely to inspect

Read the completed source without evaluating, importing, compiling, or executing it. Check metadata purity and filename agreement; declared versus used phases; injected-scope references; nullable paths; barrier justifications; loop termination; cap disclosure; deterministic behavior; and one-level child composition.

The repository parser/lint gate is a development aid for this checkout, not a general validator and not a substitute for the contract review. Always pass the actual authored file or directory. From this repository’s root, examples are:

```bash
node scripts/lint-workflows.mjs .claude/workflows/<name>.js
node scripts/lint-workflows.mjs plugins/ultracode-workflows/workflows/<name>.js
```

Do not recommend bare `npm run lint:workflows` for a project-local script; that npm command checks the marketplace’s shipped catalog by default. Outside this repository checkout, perform the source review manually instead of pretending the development dependency is installed.

### 7. Render an optional advisory diagram

When a visual will help the user understand the shape, run:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/diagram-workflow.mjs" path/to/<name>.js
```

Relay the terminal diagram inside a fenced plain-text code block so its columns remain aligned. The diagrammer parses source statically and never runs the workflow body. Treat its output as an explanatory sketch: runtime-dependent fan-out remains unknown, conditional calls may be optional, and a partial analysis must never be described as an exact execution plan. Do not execute a workflow, supply sample args, or invoke a JavaScript runtime compiler merely to improve a diagram.

Use `--md` only when the user explicitly requests Mermaid for a document, GitHub, or another Mermaid-capable destination. Claude Code's TUI does not render Mermaid notation, so never select `--md` merely to show the diagram conversationally.

### 8. Deliver with provenance and limits

Save a named project workflow at `<repo>/.claude/workflows/<name>.js` unless the user requested a marketplace contribution elsewhere. Then report:

- What reusable decision the workflow automates.
- Which catalog patterns and examples informed it, and why.
- Its args, report-only/mutation defaults, approximate agent-cost shape, and invocation example.
- What makes its result trustworthy and what remains uncertain.
- Any caps, prerequisites, local agent-type dependencies, or non-portable assumptions.
- The advisory diagram when it materially improves comprehension.

## Review heuristics

Reject or revise these common designs:

- **Decorative fan-out:** identical prompts with different labels. Replace with distinct charters and anti-charters or use one agent.
- **Barrier by habit:** collect every stage before starting the next even though items are independent. Convert to a pipeline.
- **Self-certification:** the same agent proposes and approves a claim. Add independent evidence or make the result explicitly provisional.
- **False completeness:** a top-N result silently presented as exhaustive. Return the remainder and the reason for the cap.
- **Fixed exhaustive sweep:** a fixed number of finders used for an unknown population. Use a bounded convergence loop or state that the result is a sample.
- **Parallel destructive writers:** agents can overlap or invalidate one another. Shard disjointly or funnel mutation through one stage.
- **Human question hidden as model judgment:** the workflow guesses a product decision. Return a checkpoint object and accept the decision in later args.
- **Generated abstraction for one use:** helper frameworks obscure a short workflow. Inline the orchestration until repetition is real.

When debugging, map symptoms back to these invariants first: sequential performance usually means promises were passed instead of thunks; duplicated findings indicate missing anti-charters or stable-key deduplication; brittle resumes indicate nondeterminism; crashes after a skipped agent indicate unguarded `null`; misleading progress usually indicates phase drift or an unjustified static assumption; endless rounds indicate a bad `seen` set, no convergence state, or an unguarded infinite budget.
