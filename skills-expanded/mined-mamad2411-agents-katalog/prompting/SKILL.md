---
name: prompting
description: "Design, write, review, audit, debug, revise, compress, or test AI-facing instructions, including prompts, repository instructions (AGENTS.md/CLAUDE.md), skills, agent/tool definitions, plans, memory/state/handoffs, and evaluators. Not for reader-facing prose or code comments."
license: MIT
metadata:
  author: Anbeeld
  version: '1.1.0'
---

# PROMPTING.md ruleset

Instructions for designing, writing, reviewing, and testing documents whose operational reader is an AI model.

Apply this standard to system and developer prompts, task prompts, repository instructions, skills, agent profiles, tool descriptions, plans, specifications, memory and state documents, evaluators, and other AI-facing control text.

Select the rules relevant to the artifact and deployment, using the surface overlays in section 20.

Do not apply this standard mechanically to ordinary reader-facing prose. Follow the current specification of the target product for syntax, loading, precedence, tools, and runtime behavior.

Evaluate each deployed artifact in its target configuration.

## Priorities

When requirements conflict, lower-numbered priorities win:

1. Correct authority, authorization, safety, privacy, and truth boundaries
2. Correct target behavior and factual grounding
3. Observable success and valid evaluation
4. Complete coverage of material routes, exceptions, and failure paths
5. Minimum sufficient control and context
6. Human reviewability, portability, cost, and style

Do not average a critical boundary failure into an otherwise good score. A prompt that is cheaper or more accurate on common cases is not better if it introduces a false permission for a high-impact action.

## Normative vocabulary

Use these semantic classes:

- Invariant: cannot be waived at this layer. Use `Invariant:` when this class is not already explicit from an authoritative interface. Wording intensity, including `must`, `must not`, and `never`, does not by itself establish non-waivability. Enforce the invariant outside prose where the runtime allows.
- Requirement: binding within its stated scope. An unqualified direct imperative, `do not`, `must`, `must not`, or `never` expresses a requirement unless an explicit semantic label assigns another class. A requirement yields only to a higher priority, higher authority, or a named exception. Evidence can justify authorized revision or retirement; it does not waive the active requirement during execution.
- Ask-first boundary: requires approval from a named actor before a named action. Use `Ask first:` or `Approval required from <actor> before <action>` when the class is not already explicit. State the action, impact, approving actor, and allowed fallback when approval is unavailable.
- Default: applies unless its named exception or an authorized higher-priority instruction overrides it. Use `Default:`, `by default`, `default to`, or `prefer`, and state the escape condition.
- Guideline: informs judgment without binding every case. Use `Guideline:`, `should`, `consider`, `may`, or `can`, and keep the relevant tradeoff visible.
- Runtime fact: records a verified mechanism from which policy follows. Use `Runtime fact:` when the statement could be mistaken for policy, and keep its product, harness, scope, or version next to it.
- Exposition: supplies rationale or an example without creating an action. Use `Rationale:` or `Example:` when the role is not clear from structure.

`When`, `if`, `unless`, and equivalent conditions limit whichever class follows. If two reasonable readers could assign different force to a statement, add the semantic label instead of relying on tone or emphasis. Invariant: Do not present a hypothesis as an established result until evidence meets its explicit promotion criterion. These classes also govern this standard's own statements: its directives are requirements unless labeled otherwise, and the Priorities section resolves conflicts among them.

## Core rule

Treat prompting as configuration engineering, not wordsmithing.

Behavior belongs to a configured system:

```text
behavior = f(model, harness, authority, rendered messages, placement,
             selected context, tools, permissions, state, task, parameters)
```

Do not call an instruction effective because it sounds clear, follows a template, contains emphatic language, matches a product guide, or worked once. Preserve the executing configuration and test the behavior the instruction is meant to cause.

Distinguish the authored artifact from the input the model receives:

```text
representation: source artifact -> templates/imports/parser -> rendered role-tagged messages
lifecycle: available -> selected -> loaded -> executed -> checked -> retained
```

The source and rendered input may be identical, but do not assume they are. Evidence for one state does not establish the next. A skill can exist but never be selected. A rule can be loaded but skipped. A tool call can occur without its result being used correctly. A self-audit can report no issue while a later run exposes one.

## Load references

The sections not reproduced below live in `references/`. Numbering is the standard's own, so a cross-reference to a section number resolves whether or not that section is loaded.

- Read `references/authority-and-trust.md` (section 3) when instructions can conflict, when untrusted content reaches the model, or when deciding who may override, approve, or waive a rule.
- Read `references/task-routing.md` (section 4) when one artifact serves neighboring jobs, modes, or branches.
- Read `references/state-and-lifecycle.md` (section 5) for long, multi-stage, compacted, or handed-off work.
- Read `references/calibration.md` (sections 9 and 14) when choosing degrees of freedom and altitude, or when deciding whether a reason, example, prohibition, emphasis, or checklist earns its place.
- Read `references/context-and-density.md` (sections 10 and 11) when selecting what to load, or when added rules coincide with omissions or false activation.
- Read `references/input-representation.md` (section 12) when the artifact's markup, formatting, roles, or rendered messages are in question.
- Read `references/compression.md` (section 13) before shortening a durable instruction, context packet, handoff, or state record.
- Read `references/tools-and-security.md` (sections 15 and 16) when defining tool interfaces, permissions, secrets, privacy, or untrusted-content defenses.
- Read `references/evaluation.md` (section 17) when designing behavioral tests, baselines, graders, or comparisons.
- Read `references/revision.md` (sections 18 and 19) when running an audit and repair pipeline or revising from an observed failure.
- Read `references/anti-rules.md` (section 22) before adopting any prompting convention as a universal law.

## 1. Establish the target configuration

Before drafting or materially revising an instruction, identify:

1. Artifact: the prompt, file, description, schema, profile, plan, state packet, or evaluator.
2. Operational reader: the target model, model tier, or supported model range.
3. Harness: the product, message roles, loading and discovery rules, templates, imports, parsing, rendering, precedence, context lifecycle, compaction behavior, tool semantics, and output channels.
4. Representation: the authored source, required interface syntax, exact rendered messages, role placement, answer contract, output parser, and constrained-decoding settings.
5. Authority: who may set, override, waive, approve, or delete each class of instruction.
6. Task population: representative tasks, neighboring non-tasks, edge cases, and adversarial cases.
7. Outcome: observable success, acceptable failure, and prohibited side effects.
8. Runtime resources: selected context, tools, permissions, schemas, storage, and external dependencies.
9. Evaluation: baseline, graders, trials, thresholds, protected slices, instruction density, placement, and regressions.

Verify non-inferable runtime facts. Do not invent discovery behavior, precedence, context limits, tool capabilities, persistence, permissions, model settings, or local conventions.

If the artifact must work in more than one harness, separate:

- a portable semantic core;
- harness-specific adapters for syntax, loading, scope, precedence, permissions, and lifecycle.

Do not force one file format or local runtime policy into every deployment. A rule derived from a blocking tool call, automatic skill loader, path-scoped file, or particular permission model remains bound to that premise.

### Resolve material user intent before design

After initial evidence gathering and before defining the behavioral contract, drafting an instruction, or writing a plan or specification, run an intent checkpoint scaled to the requested scope. For a narrow revision of an artifact whose intent is already recorded, verify the recorded decisions and proceed instead of rerunning discovery. Determine whether authoritative user statements and available evidence establish a coherent objective, scope, user-visible behavior, non-goals, constraints, acceptance criteria, and authorized tradeoffs at the level of specificity the requested artifact requires. If ambiguity prevents useful investigation or affects authority, authorization, or safety, clarify it earlier.

First try to resolve gaps and apparent contradictions, according to source authority and relevance, from authoritative user statements, supplied context, existing artifacts and behavior, interfaces, tests, established conventions, and safe reversible investigation. Distinguish user-owned choices about intent, preference, policy, product behavior, and authorized tradeoffs from technical or domain judgments assigned to the system. Do not transfer an assigned judgment back to the user merely because several implementations are possible.

Ask before the affected design commitment when all of the following hold:

- a material required fact, preference, constraint, or acceptance criterion remains unknown, more than one plausible interpretation remains, or authoritative inputs materially conflict;
- the unresolved matter could materially change the objective, scope, user-visible behavior, non-goals, constraints, acceptance criteria, compatibility, persistence, cost, risk, or substantial downstream work;
- resolving the matter requires the user or another named decision owner because either the preference or decision has not been explicitly delegated within the system's verified expertise, authority, and stated scope, or that actor is the only authoritative source for the missing fact.

Scale clarification to the unresolved decision surface: the number, materiality, and dependency of unresolved user-owned decisions, not the size or technical complexity of the implementation.

- Ask no question when evidence resolves the intended outcome and the remaining choices are assigned technical judgments or low-risk reversible details.
- Ask one focused question when one answer resolves the material ambiguity.
- Ask one coherent batch when several material decisions are independent and can be answered without earlier answers.
- Enter multi-round design discovery when a broad or greenfield request lacks substantial product or behavioral design, several material user-owned decisions would otherwise be invented, or material contradictions make the intended outcome incoherent. In each round, ask only the highest-leverage questions whose prerequisites are resolved; use the answers to determine which dependent questions remain relevant.

Guideline: Keep each batch small enough to answer coherently, often three to five questions. This is an interaction default, not a quota. Ask independent questions together, defer dependent questions, and do not split or combine questions merely to hit a count. Before asking a question, identify how its answer could change the artifact. Explain the practical consequence of a choice and recommend an option when evidence supports one; allow the user to delegate judgments within the system's expertise and authority.

End clarification when the intended behavioral contract is coherent and every remaining uncertainty is evidence-resolvable, explicitly delegated under the criteria above, or low-risk and reversible. Record each material answer as a user statement, decision, delegation, or unresolved question, with its source. Do not reopen it unless the user changes the relevant intent, new authoritative evidence materially conflicts with it, or a later discovery creates a new material ambiguity. When an answer is reopened, rerun the intent checkpoint before the dependent commitment. Ask a targeted follow-up only when the criteria above still require clarification; otherwise resolve the matter from evidence or assigned judgment.

If required clarification is unavailable, stop before the affected commitment or provide explicitly provisional, conditional branches without presenting any branch as decided or executable. For nonmaterial missing information, state a low-risk assumption and produce the smallest reversible draft.

## 2. Define the behavioral contract before the prose

Build the contract from the resolved intent and recorded decisions established in section 1. Do not silently convert an unresolved user-owned choice into a requirement.

State the governed behavior in operational terms:

```text
goal + scope + authority + inputs + routes + actions + outputs
+ success + failure + stopping
```

For each material requirement, determine:

- what event makes it applicable;
- which actor must or may act;
- which prerequisites must already hold;
- which action or decision is required;
- which result makes compliance observable;
- which exceptions apply;
- what happens when information, permission, or capability is missing;
- what ends the procedure.

Do not start from preferred phrasing. Start from the decision the model must make differently.

Separate outcome requirements from process requirements. Specify a process only when order affects correctness, safety, compatibility, auditability, or an external interface. When several safe paths exist, specify the outcome and boundaries and leave the method open.

Treat a high-cost safety hazard as sufficient reason for a proactive control. Ordinary behavior rules should respond to an observed failure, a required capability, or a credible pre-mortem hazard. Every rule still needs an observable consequence or a clearly labeled role as rationale, default, or guideline.

## 6. Diagnose the failure before choosing the form

Classify the need before adding text. For each observed failure, consider the listed mechanism first. The groups below aid retrieval; they do not make the failure classes mutually exclusive.

Knowledge, selection, and judgment:

- Missing fact or domain knowledge: use context, a reference, retrieval, or another data source.
- Wrong source selected: adjust the trigger, routing description, selection policy, or taxonomy.
- Genuine scope overlap: change the architecture rather than rewriting the instruction again.
- Ambiguous applicability: define the partition, precedence, non-trigger, and fallback.
- Wrong default judgment: use a principle, decision criterion, short rationale, or example.

Execution and state:

- Skipped action: use an event-bound prerequisite, state transition, hook, or gate.
- Wrong-time action: add a state lock, phase transition, or capability boundary.
- Repeated question or forgotten choice: record explicit state, source, lock, and reopening rule.

Output and authorization:

- Generic filler under missing information: define a null path that permits inspection, asking, marking unknown, omission, deferral, or stopping.
- Wrong abstraction level: name the audience and target altitude.
- Invalid machine structure: use a strict schema, constrained output, parser, and validator.
- Semantically invalid output: use a domain validator, test, rubric, or independent evaluator.
- Unsafe or unauthorized action: use least privilege, a sandbox, confirmation, or a transaction boundary.

Lifecycle, activation, and load:

- Late-session omission: use lifecycle hydration, a compact state record, or harness reinjection.
- Excessive activation: narrow the trigger, define an explicit non-trigger, or use a softer default.
- Context overload: use selection, deduplication, progressive disclosure, or loss-aware compression.
- Instruction-density failure: measure the density curve, reconcile rules, or redesign routing and controls.

Representation, validation, and maintenance:

- Source/render mismatch: inspect templates, imports, parsing, role splitting, and exact rendered messages.
- Parse success mistaken for task success: score loader, parser, schema, and semantic outcomes separately.
- Presentation syntax with no operational job: remove it or run a matched rendered-input ablation.
- Stale local policy: recheck the runtime premise, then narrow or remove the policy.
- Repeated attempted fix: require new evidence and a root-cause diagnosis, re-decide between prose and runtime control, or stop.

Do not repair a routing failure by expanding the skill body, a permission failure by adding a warning paragraph, a state failure by rewriting one sentence, or a schema failure by asking the model to be more careful.

Group related symptoms before editing. A patch per symptom creates duplicate rules, stale branches, and unclear ownership. Change the smallest coherent mechanism that covers the diagnosed failure. When dependent changes must ship together, label them as one bundle and do not attribute the result to an individual feature without an ablation.

## 7. Match control strength to failure cost

Match each requirement to a suitable control:

- Goal, judgment, tone, or tradeoff: natural-language guidance.
- Auditable action or result: a named operation, artifact, decision, or state transition.
- Exact structure or typed input: a schema, constrained output, parser, or typed tool.
- Required order: a state machine, wrapper, transaction, or precondition gate.
- Access or side-effect boundary: a permission, sandbox, allowlist, or scoped credential.
- Irreversible or external action: action-specific human approval and a transaction boundary.
- Mandatory validation: a hook, CI rule, validator, or application gate.

Choose the weakest control that safely meets the cost of failure. Stronger control adds latency, false refusals, and user friction. Harmless reversible work should not inherit approval rituals designed for destructive or external actions.

Do not leave secrets, payments, destructive changes, permission expansion, external messages, production changes, or public publication to prose alone.

Remember each mechanism's boundary:

- a schema can enforce supported syntax, not truth, authorization, or good judgment;
- a valid tool call can still be the wrong tool call;
- a hook only guarantees what its trigger, exit behavior, and override rules actually enforce;
- a tool trace proves an action occurred, not that its output was interpreted correctly;
- a final statement that checks ran is not the check result.

Observable prose is useful because it creates a denominator. It is not enforcement.

## 8. Write decidable semantic units

Write one canonical statement per requirement. For an action rule, use the fields that matter:

```text
actor + trigger + modality + action + object + scope
+ prerequisite + result + exception/fallback
```

Not every rule needs every field. Every material field in the intended behavior must remain recoverable.

Prefer:

Before editing a generated file, identify its generator, edit the source, regenerate the output, and compare the generated diff. If the generator is unavailable, stop and report the gap.

Avoid:

Be careful with generated files.

Use one stable term per concept. Name concrete actors, objects, files, fields, operations, states, and owners. Replace vague quality words with criteria that can be assessed.

Preserve control operators deliberately:

- actor and authority;
- `must`, `may`, `must not`, and priority;
- negation and quantity;
- `if`, `when`, `unless`, `except`, and non-trigger scope;
- `before`, `after`, `only once`, and dependency;
- exact identifiers, values, units, and thresholds;
- observable success;
- fallback and stopping behavior.

Do not convert `may` to `will`, `some` to `all`, `prefer` to `must`, `after` to `and`, or `not retrieved` to `nonexistent` for cleaner prose.

Do not invent numeric thresholds solely to make a rule measurable. Use numbers when they represent a real interface, limit, budget, quorum, or acceptance threshold. A countable proxy can be easier to score while becoming a worse requirement.

Put a required action before the event it governs. A check that must produce a result before a completion transition creates observable evidence that a late reminder does not.

Every prohibition that can encounter missing information needs a safe path. `Do not invent` is incomplete when the model does not know whether to inspect, ask, mark unknown, omit, defer, save a draft, or stop.

## 20. Surface-specific overlays

Treat the categories below as composable overlays, not mutually exclusive routes. First select the primary surface from the interface the artifact must satisfy. Then apply every secondary overlay whose operational reader, loader, lifecycle, or output contract materially applies. Mentioning a surface in the artifact does not by itself activate that overlay.

The primary surface controls delivery format, required interface syntax, and loader constraints. Compatible secondary overlays add their distinct requirements without replacing it. If overlays conflict, apply the priorities and authority rules in this standard; at equal authority, the narrower interface-specific rule wins. Resolve a remaining material conflict before drafting rather than silently choosing one rule.

If no category fits, use the applicable shared rules and define a deployment-specific adapter rather than forcing the artifact into the nearest category. Do not apply unrelated overlays merely because they are present in this section.

### Task prompt

Include the goal, relevant context, scope, hard boundaries, success evidence, output shape, and missing-data behavior. Specify a process only when it matters. Do not import repository-wide policy into one task.

### System or developer prompt

Define authority, trust treatment, default behavior, permission boundaries, tool policy, and failure handling. Keep durable cross-task behavior here. Move exact contracts and safety invariants into runtime controls when possible. Use native role fields and preserve their authority semantics; a text heading that names a role does not create that role.

### Repository instruction file

Verify discovery, nesting, concatenation, precedence, and size limits in the target harness. Include project-specific commands, architecture facts, constraints, verification, and local workflow that the model cannot safely infer. Keep path-specific guidance near its scope. Do not turn personal or harness-specific policy into a universal repository rule. Preserve syntax required for discovery or imports, then inspect the exact merged or rendered content that reaches the model.

### Skill or on-demand procedure

Treat discovery metadata and body execution as separate interfaces. Make the description a high-recall router that states what the skill does, when to use it, and enough distinctive positive and negative scope to separate neighbors. Keep the body focused on procedures, decisions, references, scripts, outputs, and failure handling. State which decision each reference or resource supports so its routing can be tested against that decision.

Test discoverability, trigger precision and recall, retrieval, body execution, and bundled-code security separately. Preserve loader-required metadata exactly; use the semantic plain-text baseline inside the model-facing body unless a tested need justifies richer syntax. A genuinely overlapping skill taxonomy needs an architecture change.

### Plan or specification

Make the artifact usable from a cold context. Name the objective, current state, exact files and interfaces, dependencies, non-goals, decisions, open questions, acceptance criteria, and terminal end-to-end verification.

Resolve material user-owned intent before presenting the artifact as an executable plan. Do not hide an unresolved product or behavioral decision in `open questions` while committing dependent work. If clarification is unavailable, label the plan provisional and represent the affected alternatives conditionally. Implementation unknowns may remain when their owner, decision point, and resolution method are explicit and they do not conceal unresolved intent.

Separate stable intent from implementation choices when either can change independently. Match the state representation to the data: schemas for structured facts, prose for nuance, and versioned artifacts for history. Skip or scale down planning when the task is already small and decidable.

### Tool description

Specify selection, arguments, results, errors, side effects, and boundaries as an interface. Keep neighboring tools semantically distinct. Enforce types, permissions, and invariants in code.

### Agent or subagent profile

Assume a cold or isolated context unless the harness guarantees otherwise. Define purpose, eligibility, available context, tools, authority, permissions, state and memory scope, handoff artifact, completion test, and residual work that stays elsewhere. Define dispatch and synchronization points, ownership of shared mutable state, failure and cancellation behavior, and how late or stale results are handled.

State runtime facts that derive delegation policy. Do not prescribe agent counts, concurrency, or isolation independently of the harness. A single agent may be useful for context isolation even when it provides no parallelism.

### Memory or persistent context

Define what is stored, source, confidence, freshness, conflict resolution, retention, privacy, update authority, and deletion. Separate facts, preferences, inferences, and summaries. Test stale, contradicted, and sycophantic memory effects.

### AI-to-AI handoff or state packet

Transmit the current authoritative goal, scope, completed work, exact artifacts, evidence, open decisions, blockers, constraints, and executable next action. Prefer structured state and deltas to conversation history; include history only where a decision depends on it. Expand any local shorthand that crosses the boundary.

### Reference index

Treat the artifact as navigation, not execution. Use stable identifiers, short descriptions, explicit scope, and optionality markers. Keep indexed sources authoritative for their own content. Publication or placement in an index does not guarantee selection, trust, or correct interpretation.

### Normative or constitutional document

Separate binding rules, defaults, and explanatory rationale. State precedence and conflict behavior. Use principles for generalization and exact boundaries where risk demands them. Treat the artifact as a normative design, not proof that its phrasing causes compliance.

### Evaluator or review prompt

Define what counts as a finding and allow an empty finding set. Require output evidence, scope, expected consequence, severity, and falsifier. Prevent test weakening and metric gaming. Keep authorship, evaluation, acceptance, and repair distinct when stakes justify it.

## 21. Required audit before delivery

Audit the completed instruction against every applicable item.

After a representation change, rerun Input representation against the complete artifact, not only the edited passage.

### Purpose and scope

- The artifact, reader, harness, task population, and authority are identifiable.
- The primary surface, applicable secondary overlays, overlap rules, and fallback are identifiable.
- The governed behavior, non-goals, and completion condition are explicit.
- Optional processes have skip or scaled-down routes where appropriate.
- Internal procedure and user-visible output are not accidentally mixed.

### Intent and clarification

- The objective, scope, user-visible behavior, constraints, non-goals, and acceptance criteria trace to authoritative user statements, evidence, recorded decisions, or explicit delegations within the system's verified expertise, authority, and stated scope.
- Material missing facts, contradictions, and user-owned choices were resolved before the behavioral contract or executable plan; provisional branches are labeled and do not masquerade as decisions.
- Each clarification question could materially change the artifact and could not be answered from available evidence or assigned expertise.
- The number and grouping of questions match the materiality and dependency of unresolved decisions: independent questions are batched, dependent questions are deferred, and ordinary implementation choices are not transferred to the user.
- Clarified decisions record their source; a reopening condition reruns the intent checkpoint instead of automatically triggering another question.

### Logic

- Each control statement is identifiable as an invariant, requirement, ask-first boundary, default, or guideline.
- Runtime facts and exposition are distinguishable from controls; an ambiguous class has an explicit semantic label.
- Terms are stable, defined before use, and actors are unambiguous.
- Routes cover material cases, resolve overlap, and include a fallback.
- Triggers, prerequisites, actions, results, exceptions, fallbacks, and exits are present where needed.
- Missing information has an allowed null path.
- Decisions have owners; approval names the approving actor.
- Defaults have escape conditions; requirement scopes are identifiable; invariants do not masquerade as guidelines.
- There are no stale, duplicated, time-relative, or mutually inconsistent instructions.

### State and lifecycle

- Facts, preferences, inferences, decisions, approvals, unknowns, and completed actions are distinguishable.
- Lock, reopening, supersession, compaction, and handoff behavior are defined where state persists.
- Boundary records are self-contained enough for a new context or reviewer.
- Repeated next actions without progress are detectable.

### Mechanism

- Exact requirements use schemas, validators, permissions, hooks, or gates where available.
- Observable operations are not described as guarantees.
- Retrieval selection and body execution can be tested separately.
- Tool and model capabilities were verified, not invented.
- Reasoning effort, verbosity, and other runtime controls use the proper interface when available.

### Context and compression

- Always-on context is sufficient without generic padding.
- Active instruction count is distinguished from tokens, lines, sections, and context length.
- Density is measured with both per-instruction and all-instructions-correct results where relevant.
- Role placement preserves authority and is tested when more than one placement is valid.
- Rare constraints, control operators, and exact identifiers survive compression.
- Optional detail has a reliable route and a retrieval-failure path.
- Main-file size is not confused with effective selected load.
- Control remains explicit; where the control-plane and work-plane split is in use (section 13), transient work state uses stable fields, identifiers, and deltas.
- A human reviewer can reconstruct the intended decision.

### Input representation

- The authored source and exact rendered role-tagged messages are both identifiable. If the authored source reaches the model byte-for-byte, audit it as rendered input.
- Inventory every optional syntax class in both representations, including heading markers, emphasis, list markers, numbering, line wrapping, table notation, fences, inline quoting, blockquotes, links, comments, tags or serialization, and meaningful whitespace.
- For each optional class that reaches the model, record its warranted job: required interface syntax, literal task data, an information-bearing relation, or a matched deployment result. Human navigation warrants richer source markup only when that markup does not pass through to the model. Remove or replace an unwarranted marker while preserving labels, line boundaries, order, literals, and real data relations.
- For each table, identify the row schema and task-relevant row-column relation; justify the notation separately. Replace a table that fails either test with labeled records or plain semantic pairs.
- Native roles are not imitated with fake headings.
- Delimiters are not treated as authority or security boundaries.
- Syntax comparisons freeze semantic content and the output contract, and separate parseability from semantic correctness.

### Security and privacy

- Trusted instructions and untrusted data are separated.
- Secrets, personal data, external actions, destructive actions, dependencies, and prompt injection have controls proportionate to risk.
- Installed or adapted instruction packages were treated as supply-chain inputs.
- Logs and state records preserve accountability without exposing secrets.

### Evaluation

- Success criteria, baseline, graders, trials, target cases, non-trigger cases, exceptions, regressions, and adversarial cases are defined proportionately.
- The full configuration, rendered input, placement, and selected context are recorded.
- Objective checks are deterministic where possible; subjective judgments have a named owner.
- Opportunity counts and fresh-session tests support any claim of retention.
- Critical regressions are not hidden by averages.
- The final report states what ran, the actual results, and what remains unverified.
- Public, README, changelog, and release claims trace to evaluated versions, tasks, evaluators, and comparators.

If a critical item cannot be satisfied, do not conceal the gap with stronger wording. Report the missing control, information, authority, or evaluation — in the audit report when auditing at the user's request; otherwise record it internally, per section 23.

## 23. Delivery contract

When asked to create or revise an AI-facing instruction artifact, the default user-visible deliverable is the artifact or requested outcome in the target product's valid format. Keep the working audit and configuration record internal unless the user asks for it or it changes a decision.

Behavioral-validation obligations apply to claims that an instruction artifact causes behavior. An ordinary answer or completed task is validated by its own checks; do not append efficacy or unverified disclaimers to it.

Add concise delivery metadata only when requested or needed for safe use, approval, handoff, or a limitation that changes a decision the user must make. Relevant metadata can include:

- decision-changing assumptions or unresolved risks;
- validation performed and its actual results;
- runtime controls, schemas, references, or tests required outside the prose;
- a semantic change summary when another reader needs to review or continue the revision.

Lead with the artifact or outcome, not a narration of the drafting process.
