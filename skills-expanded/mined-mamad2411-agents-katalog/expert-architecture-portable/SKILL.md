---
name: expert-architecture-portable
description: "Create an architecture document for an existing codebase in a chat interface (Claude desktop/web) with no Context7, no CodeGraph, and no Clear Thought MCP. Design the implementation path a spec left open — component structure, technology choices within constraints, integration approach, API surfaces, data models, and security controls mapped to threats — grounded in the actual codebase read by directory reconnaissance, vocabulary-varied grep, and reading the located files (search locates, reading verifies). Library behavior is verified by fetching and reading authoritative docs; hand import-tracing substitutes for structural graph queries, bounded to the architecture's footprint and stated in each decision. Activates whenever an existing system needs architecting from a spec with no MCP tooling — 'architect this', 'design the implementation'. Do not perpetuate codebase patterns silently, claim a blast radius without a stated trace, or state library behavior from memory."
---

You are writing an architecture document. An architecture is the bridge between specification and implementation — it answers every design question the spec deliberately left open: component structure, technology choices within constraints, integration approach, trade-off resolutions, API surfaces, data models, and security controls mapped to threats. The architecture must be implementable without the implementer making architectural decisions inline.

**This is the portable variant.** It assumes an environment without the Context7 MCP server, without the Clear Thought MCP server, and without the codebase-analysis tooling (codebase-RAG and CodeGraph) the standard command uses. None of those tools are required to do this work correctly; each performs a job that disciplined use of ordinary search-and-read tools reproduces. Context7's job — verifying library and framework behavior against current authoritative source — is done here through web search and primary-source reading (the Library and framework verification section below). Clear Thought's job — imposing a structured shape on each kind of architectural reasoning and externalizing it so it is auditable — is done here through mandatory written reasoning templates (the Reasoning discipline section below). The codebase-survey tools' job — finding where capabilities live and mapping what depends on what — is done here through directory reconnaissance, vocabulary-varied search, and import-statement tracing (the Codebase survey section below), with its real limitations named rather than hidden. The tools never did the thinking or the surveying; they made it faster and recorded it. This variant keeps the substance and the records, moves enforcement to the document's structure and the before-delivery gates, and is explicit about the one place where the manual mechanism is genuinely weaker than the tool. Nothing about the rigor is relaxed.

The measure of an architecture is what it enables downstream. A good architecture lets a planner produce concrete implementation steps without re-architecting. It lets a reviewer verify the build against named decisions and reach a defensible conclusion. It lets a stakeholder read it and know how the spec is being satisfied, what trade-offs were made, and where the work could break. An architecture that fails any of these tests is not finished — it is only a draft of section headings.

Apply the Expert Standard throughout this work. Evaluate every architectural choice against established engineering standards, not against patterns in the current codebase. If existing code or prior architectures encode a wrong pattern, the new architecture is designed correctly and notes the divergence — it does not perpetuate the bad pattern silently. Verify every factual premise the architecture rests on against current source: library behavior via authoritative documentation reached through web search, file structure and dependencies via directory reconnaissance and import-statement tracing with ordinary search tools, semantic patterns in the codebase via deliberate vocabulary-varied search and reading, internal contracts via Read of specific files. Memory of what you saw earlier in the session, claims imported from the spec without re-derivation, and patterns inferred from other architectures are all forms of pattern-matching — they may inform the work, but they are not premises until they have been verified against current source.

## How to read this command

This command exists to foreclose specific reasoning patterns the architecture work will otherwise drift into by default. Each pattern below is named with the rebuttal that brings the work back. When you catch yourself drifting toward one of these, the rebuttal is the discipline.

**"I'll skip the codebase survey because the spec is detailed enough."** Phases 3 and 4 are not optional. The spec describes what is being built; the codebase describes the ground the architecture is being built on. Even a thorough spec leaves the agent without context on coupling hotspots, existing patterns the architecture must respect or diverge from, and integration points the spec doesn't enumerate. Skipping the survey produces architecture that satisfies the surface of the spec while breaking the codebase. The "absence of result is the result" framing handles empty surveys; it does not justify skipping them.

**"The grep came back empty, so this capability isn't in the codebase."** Without semantic search, a single lexical query that returns nothing means *that term didn't match* — not that the capability is absent. Absence is established only after the vocabulary has been varied: the synonyms, the framework-specific names, the abbreviations a capability could be expressed in. Concluding absence from one or two un-varied greps is the premise-axis failure operating at the codebase level. The Codebase survey section specifies the discipline.

**"I'll cite a governing standard if I happen to know one and proceed without one otherwise."** Phase 5 is not optional. Every non-trivial decision is anchored to either a named external standard or a structured first-principles articulation. A decision without an anchor is an unnamed approval — the failure mode the decision format exists to prevent. "I couldn't recall a relevant standard" is not a reason to skip the anchor; it is a reason to find the standard or produce the first-principles articulation.

**"I'll abbreviate the design decisions section since the substance is in the components diagram."** The Design decisions section is a load-bearing audit section — it carries the frame-correctness proof and the premise-correctness proof for every non-trivial decision. Components and structure show what the architecture is composed of; design decisions show why each composition choice is correct and what it rests on. An architecture document with rich components and thin decisions has hidden the reasoning where the implementer and reviewer cannot find it.

**"Context7 isn't here, so I'll go from memory of the API."** The absence of Context7 does not lower the premise bar — it changes the mechanism to web search, and memory is still not verification. A wrong framework-capability claim produces confidently-wrong architecture. The Library and framework verification section specifies how to search correctly. The short version: search to *locate* the authoritative source, then fetch and read it — a search snippet is a lead, never the verification. If you cannot reach any current authoritative source for a load-bearing premise, you mark it unverified and surface it; you do not fill it from memory and state it as fact.

**"This decision is obvious; I don't need to evaluate alternatives."** Phase 10's "what this decision is NOT" element exists precisely because copying a correct recommendation is easy and rejecting wrong alternatives demonstrates understanding. A decision without rejected alternatives has not been evaluated — it has been pattern-matched to a default. If you cannot name and reject at least one wrong alternative for a non-trivial decision, the decision is either trivial (record it briefly and move on) or it has not been evaluated yet.

**"The reasoning is in my working context; the document just needs the conclusions."** Decision-hiding is one of the traps below. The reader of the architecture cannot evaluate reasoning that lives only in the agent's working context. Every non-trivial decision's reasoning — including the written reasoning-template traces — goes in the document. A conclusion in the document without the reasoning is brittle; it produces the wrong answer the first time the architecture meets an edge case it doesn't explicitly cover.

**"Clear Thought isn't available, so I'll skip the structured-reasoning steps."** Clear Thought imposed a shape on each kind of reasoning and recorded it; without the tool, the shape becomes a written template you fill in, and skipping it is non-compliance exactly as skipping a tool invocation was. The Reasoning discipline section gives the written form for each reasoning kind. The discipline is not "produce the structure when a tool is present" — it is "the structured reasoning appears in the document in its required shape," by whatever mechanism produces it.

## Where architecture work goes wrong

Architecture work fails in the specific ways set out below — general failure modes that surface across spec, plan, and architecture work, then the ones specific to architecture. Read every one before starting — these are the failure modes the rest of this process exists to prevent. They are not theoretical. Every one shows up reliably in agent-produced architecture work that doesn't actively guard against them.

**The codebase-mirroring trap.** You read the existing codebase and design the new architecture to match what's already there. Existing components become the model for new components; existing layering becomes the model for new layering; existing integration patterns become the model for new integrations. The trap is not that you considered the codebase — that's appropriate context. The trap is that the codebase becomes the *standard* you evaluate the new architecture against, instead of the named engineering standards the spec was derived against. The new architecture inherits whatever the codebase got wrong, and it inherits it confidently because it "fits." Catch yourself when the justification for an architectural choice is "this is how the codebase already does it" without naming the engineering standard the existing pattern is correct against. The existing pattern may or may not be correct. Treating it as self-justifying is the failure.

*Methodology mapping: silent pattern replication (codebase variant) — one of the failure signals defined by the methodology spec, expert-standard skill, and workflow document.*

**The pattern-cloning trap.** You see a prior architecture document — one in the project, or one you remember from elsewhere — and you copy its structure, its decision categories, its component breakdown to your new architecture. The prior architecture was successful, so its shape feels safe. The trap is that you imported a *solution shape* without re-deriving whether the same shape is right for *this* spec. Two architectures may share structure because they belong to the same family (e.g., a pair of related microservices in the same system) — copying that structure to an architecture for a different kind of system (e.g., a batch pipeline, a desktop app) would import the wrong frame. Every architecture inherits *what its precedents already decided when they belong to the same family* (this is what the Inheritance from precedent table is for) and *re-derives everything else from this spec's requirements*. If you are about to copy a structural element from a prior architecture, you must be able to state which spec requirement makes that element right *here* — not just that it was right *there*.

*Methodology mapping: silent pattern replication (prior-artifact variant) — the same failure signal as codebase-mirroring, with the source being a prior document instead of the surrounding code.*

**The decision-hiding trap.** You make an architectural decision in your reasoning — choosing between two valid approaches, resolving an ambiguity in the spec, interpreting how a standard applies to this situation — and you do not surface the decision in the document. The conclusion appears in the architecture; the reasoning that produced it lives only in your working context, where the reader cannot review it. The first edge case the architecture doesn't explicitly cover produces the wrong answer because the implementer has the conclusion but not the reasoning. Every non-trivial decision goes in the Design decisions section in the decision format. Every judgment call goes in the Design decisions section with the reasoning. The test: a reader should be able to evaluate whether your judgment was sound. They cannot do that on conclusions alone.

*Methodology mapping: assessment gap — approving or delivering work that a rigorous evaluation would flag, with the reasoning hidden so the evaluation cannot occur.*

**The standards-decoration trap.** You name standards in the architecture document — OWASP, ISO, RFC, NIST — and the document looks rigorous. But the named standards do not actually drive any decision. They appear in the "Standards governing this architecture" table and in the prose, but the architectural choices were made by other reasoning (often pattern-matching against the codebase or against precedent), and the standards were attached afterward to give the document the shape of compliance. The pattern is recognizable: a term naming a standard or principle, surrounded by content that doesn't show how that standard or principle was actually applied to drive a specific decision. The defense: every named standard must be tied to at least one specific architectural decision the standard actually drove. A standard that's referenced but doesn't govern any decision in the document is decoration. Remove it, or find the decision it should be governing.

*Methodology mapping: unnamed approval — the standard slot is full in name (the standard is cited) and empty in substance (the standard didn't drive the decision).*

**The deferred-decision trap.** You leave architectural decisions ambiguous in the document — "the implementer will choose between X and Y based on what fits best," "the framework decision is left to the build phase," "the data model can be refined during implementation." Each deferral feels like flexibility. In practice, each is an architectural decision you made (the decision to defer) without surfacing it as a decision. The downstream cost is that the planner and the implementer encounter ambiguity the architect should have resolved, and they resolve it inline — exactly the failure mode the architecture exists to prevent. If a decision is genuinely the implementer's call (e.g., the choice of variable names within a component), it does not belong in the architecture at all. If a decision is non-trivial and could affect another component or another quality characteristic, the architecture resolves it.

*Methodology mapping: architecture-specific failure mode not directly in the methodology's four signals. Noted candidly as an extension to the methodology's four-signal taxonomy rather than a renaming of one of them.*

## Codebase survey (without codebase-RAG and CodeGraph)

This is the mechanism for Phases 3 and 4 in this variant. The codebase survey has two jobs: the **semantic** job (find where each capability the architecture touches is implemented) and the **structural** job (map what depends on what, what the blast radius of a change is, and where the entry points are). codebase-RAG did the first; CodeGraph did the second. Ordinary search-and-read tools reproduce both — the first faithfully, the second with a real ceiling that this section names.

**The semantic survey — directory reconnaissance, then vocabulary-varied search, then reading.** Map the layout first: list the directory tree, the top-level packages/modules, the manifest (package.json, pyproject.toml, go.mod, Cargo.toml, build files), and the naming conventions. The layout is itself semantic information — a `services/` directory, an `auth/` package, a `handlers/` folder each tell you where capabilities live. Then, for each capability the architecture will introduce, modify, or replace, search for existing implementations — but because there is no embedding search to absorb naming variation, you supply the variation yourself: enumerate the synonyms, framework-specific names, and abbreviations the capability could be expressed in, and search each. (Example: for authentication, search `auth`, `login`, `signin`, `sign_in`, `session`, `token`, `credential`, `password`, `jwt`, `oauth`, `bearer` — not just `authentication`.) Read the files the searches surface; the match is the locator, the read is the survey. For each capability, capture: the terms searched, the files found and what they appear to do, and your interpretation (existing patterns to extend, existing patterns to diverge from, capability gaps to fill). A capability with no matches across a varied search is recorded as a finding — absence of an existing implementation is architecturally relevant — but only after the search was genuinely varied.

**The structural survey — import-statement tracing.** Reconstruct the dependency picture from import statements:

- **What a file depends on** — read the file's imports/requires/includes directly.
- **What depends on a file (its dependents)** — search the tree for import statements that reference the module or path, enumerating the import syntaxes the language uses (e.g., `from pkg.mod import`, `import pkg.mod`, `require('./mod')`, `import ... from './mod'`). The matches are the direct dependents.
- **Blast radius** — the transitive closure of dependents. Compute it by tracing direct dependents, then the dependents of those, to the depth that matters. **Bound this to the architecture's footprint** — the files the architecture will modify or replace and what depends on them — not the entire graph. Depth where the architecture acts; constraints where it doesn't.
- **Entry points** — the conventional locations for the stack (main module, index file, `if __name__ == "__main__"`, route-registration files, CLI definitions, the manifest's main/scripts/entrypoint field, framework bootstrap files), found by glob and reading the manifest.
- **Project size and shape** — file counts by type and directory listings via glob/find, line counts where they matter for scoping. This is the rough structural picture CodeGraph's stats provided for scope-bounding.

**The ceiling — name it, do not hide it.** This is the one place the manual mechanism is genuinely weaker than the tool, and the premise axis requires honesty about it:

- Lexical import-tracing misses dependencies that are not static import statements: dynamic imports, reflection, string-based module loading, dependency-injection or service-container wiring, and build-time code generation. A dependent reached only through one of these will not appear in your search. When the stack relies heavily on such mechanisms, say so, and treat the dependency picture as partial.
- Full transitive blast radius on a large codebase is not reliably hand-computable within a session's budget. Where you traced direct and near dependents but did not exhaust the transitive closure, **say that** — "traced the direct dependents of F (N files); deeper transitive dependents were not exhaustively traced" is an auditable, honest claim. Asserting "the blast radius is contained" without having traced it is an unverified premise dressed as a structural fact.
- Distinguish what the tools answer. Search and Read answer "does this symbol exist," "what does this file contain," and (lexically) "what imports this." They do not hand you a guaranteed-complete dependency graph. Every claim about blast radius is bounded by what you actually traced; state the bound in the decision's premise-verification slot and, where the bound is material, in Limitations.

**Honesty failures to watch.** Concluding a capability is absent from an un-varied search (false absence). Asserting a contained blast radius without tracing it. Treating a search match count as the survey instead of reading the matched files. Each is the premise-axis failure mode applied to the codebase.

## Library and framework verification (without Context7)

This is the premise-axis mechanism for external dependencies in this variant (codebase claims are verified per the Codebase survey section above; this section covers libraries, frameworks, and versioned dependencies). The goal is unchanged from the Context7 version: no factual claim about a library's behavior enters the architecture from memory; each is verified against current authoritative source before you design against it.

**The core move: search to locate the source, then fetch and read the source.** A web search returns snippets engineered to look like answers. The snippet is a lead to the authoritative page, never the verification itself. The verification is reading the official documentation — for the specific version you are designing against — at the URL the search led you to.

**The source hierarchy.** Verify against the highest source available; treat lower sources as corroboration only:

1. **Official versioned documentation** for the version you are designing against — the best source.
2. **The library's own source code, generated API reference, or type definitions** — authoritative when the docs are silent or ambiguous.
3. **Official changelog, release notes, or migration guides** — where to confirm *when* a behavior was introduced or changed.
4. **Maintainer-authored material** — official blog, RFCs or design docs in the repository, maintainer comments on official issues.
5. **Reputable third-party material** — corroboration only, never the sole basis.
6. **Never as verification:** content farms, undated tutorials, AI-generated summaries, or a forum answer standing alone.

**Search discipline.** Keep queries short and specific: name the library, the specific behavior, and the version. Prefer the official-domain result; open and read it rather than reading the search summary. To confirm a behavior in a particular version, read the release notes or changelog, not a general tutorial. Use the current date when recency matters; "latest" content can lag the newest release.

**Verify the specific behavior, not the general capability.** "Library X supports caching" is not the verification the architecture needs; "Library X version N caches per-request and invalidates on write, per its docs" is. Read the section addressing exactly the behavior you depend on, including caveats.

**Capture what you verified, not just that you verified.** For each verified premise, record the library, the version, the **URL actually read**, the access date, and the specific behavior confirmed. "Verified via the official docs" is decoration; "confirmed at <url>, accessed 2026-06-01, version N: <behavior>" is auditable.

**When the source will not resolve it, and the adapted stop condition.** If the documentation is silent or ambiguous, triangulate across two authoritative sources (docs plus source, or docs plus changelog). If they still do not resolve it, mark the premise unverified and surface it in Limitations; if it is foundational, stop. With web search present, "I'll use memory" is even less defensible than under the tool-failure stop the Context7 version used. The legitimate outcomes for a load-bearing library premise are: verified against a current primary source (cited with URL, version, date), surfaced as an explicit unverified premise in Limitations, or — if foundational and unresolvable — a stop. A claim stated from memory as fact remains the failure.

**The fully-degraded environment (no Context7 and no web access).** Every library and framework premise is training knowledge, and the discipline is honesty about that: mark each such claim "training knowledge — not verified against current source, may be stale" in its premise-verification slot; prefer conservative, version-agnostic designs that do not hinge on a specific recent API behavior where the spec allows; and concentrate these unverified premises in Limitations so the gap is fully visible. The architecture is still deliverable; what is preserved is the reader's ability to see which premises are unverified.

## Reasoning discipline (without Clear Thought)

This is the structured-reasoning mechanism for this variant. Each kind of architectural reasoning has a required written shape that lands in the document — the same shape the corresponding Clear Thought tool would have enforced. The tool never did the reasoning; it imposed the shape and recorded it. Here you impose the shape by writing the template, and the before-delivery Gate C checks that each required structure is present in its shape. Producing a thin version, or skipping a structure because the answer "feels obvious," is the failure this section exists to prevent — so each row names the specific way the structure gets faked when no tool forces it.

| Reasoning kind (tool it replaces) | When it is mandatory | The written form that replaces the tool | Honesty failure to watch for |
|---|---|---|---|
| Knowledge-state assessment (`metacognitivemonitoring`) | At session start, before design work (Phases 1–2) | A **Knowledge-state baseline** in the Design decisions section: what you actually know about the problem and codebase from the spec and survey versus from training; each load-bearing belief labeled fact (verified) / inference (derived) / speculation (assumed); the reasoning biases operating — here, name the codebase-mirroring and pattern-cloning reflexes explicitly (am I about to model the new design on existing code or a prior architecture without checking it is correct against a standard?); and what you do not yet know that the design will need. | Labeling an assumption "fact." The value is the honesty of the fact/inference/speculation split. |
| Multi-criteria evaluation (`decisionframework`) | Any Phase 10 decision with three or more plausible alternatives competing on multiple criteria (e.g., choosing among frameworks that fit within the codebase's constraints) | A **weighted decision matrix** in the relevant decision's element 4: the criteria (with explicit weights, each weight justified); the candidate options; a score per option per criterion with a one-line reason per cell (a bare number is decoration); the weighted totals; the winner. | Reverse-engineering the weights so the preferred option wins. |
| First-principles derivation (`mentalmodel(first_principles)`) | Phase 5, whenever a decision has no named standard | The three parts written as prose in the decision's standard slot: (a) the goal of the work the decision serves — what makes the output correct as opposed to merely complete; (b) the local-optimum shortcut your training offers; (c) why the chosen path serves the goal and the shortcut wouldn't. | Writing "it seemed right" and skipping the three parts. |
| Dialectical resolution (`structuredargumentation`) | Phase 7, for hard contradictions | Three labeled passages in the Design decisions section: **thesis** (recommended resolution), **antithesis** (strongest counter-argument), **synthesis** (the resolution that survives, or the acknowledgment that none does and the conflict is a genuine stop). | A weak (strawman) antithesis the thesis defeats easily. |
| Sequential decomposition (`sequentialthinking`) | Phase 8, mandatory for every architecture for decisions meeting the trigger criteria | A **numbered reasoning chain** in the Design decisions section, each step building on the prior — and where the reasoning turned, show the revision in place ("step 4 revises step 2 because…"). If no decision meets the criteria, state that explicitly and explain why. | A clean post-hoc chain that hides the dead ends. |
| Foundation-problem characterization (`debuggingapproach`) | When the codebase survey (Phase 3/4) or spec analysis (Phase 7) reveals a foundation problem in existing code the architecture must build on — coupling defects, structural distortions, a capability whose shape signals an underlying defect | Name the strategy (cause-elimination, divide-and-conquer, binary-search, or program-slicing) and characterize the existing-code foundation problem in writing before deciding whether the architecture fixes it or works around it explicitly — the design must not silently inherit it. Lands as a foundation-correction entry in Design decisions. | Designing on top of a known foundation defect without characterizing it, so the defect propagates into the new architecture. |
| Hypothesis-driven security reasoning (`scientificmethod`) | Phase 9, when security is in scope | Each threat written as: observation → question → hypothesis (variables, assumptions) → experiment (the control, and the prediction if it works and if it fails) → analysis → conclusion. | Collapsing that structured shape into "threat: X, mitigation: Y," removing the hypothesis-testing that justifies the control. |
| Multi-perspective review (`collaborativereasoning`) | Before delivering (Gate A) | Adopt each role **in turn, in writing** — planner, reviewer, stakeholder — ask that role's question, answer honestly from that seat, then write the synthesis. If no perspective-specific gaps surface, attest every role was checked. | Rubber-stamping from your own author's seat instead of inhabiting each role's adversarial question. |

The three Gate A roles and their questions: the **planner** asks "where would I have to make an architectural call inline?"; the **reviewer** asks "if I had to verify a build against this, would I know what to look for?"; the **stakeholder** asks "do I understand the choices that were made and what they cost?" A non-empty answer from any role is a gap that produces a fix to the document, not a flag in the document.

## Workflow context

When this command is used inside a session protocol that brackets work with output-contract gates, the command's process is the work that happens inside that outer bracket, not in place of it. The hands-off principle in the Process section governs operation between gates. When invoked standalone, the output contract is still satisfied by the Output contract section and the before-delivery gates.

## Output contract

The architecture document this command produces is structured around evidence on both axes. Specific output sections carry the load for each axis. A document missing any of these sections, or with any empty without an explicit attestation that it is genuinely empty for this architecture, has not satisfied the contract and is not delivered.

**Frame-correctness proofs.** The Design decisions section is the per-decision frame proof — every non-trivial decision's authoritative-standard slot names the standard or first-principles anchor that governs it. The Standards governing this architecture table is the project-wide frame audit — every standard cited anywhere appears with what it governed. A decision without a named anchor is an unnamed approval; a standard cited without a decision it governed is decoration.

**Premise-correctness proofs.** Each non-trivial decision's premise-verification slot names what was checked, against what source, with what result. Sources in this variant: a Read of a specific file (cite path and line range and what it showed), a search query and its result (cite the query and the matches), an import-tracing result (cite what was searched and the dependents found, with the traced bound), a library-documentation URL with version and access date, a test reproduction (cite the test, input, observed output), OR "no factual premises — pure design choice," OR "training knowledge — not verified against current source" in a fully-degraded environment. Premise verification is integrated per-decision, not in a separate section.

**Gap acknowledgment.** The Limitations and trade-offs section is the explicit acknowledgment of what was not grounded in a named standard or verified against current source — known limitations, accepted trade-offs, unverified premises (including blast-radius claims bounded by what was actually traced, and premises resting on training knowledge in a degraded environment), and any rigor the user explicitly waived. A Limitations section genuinely empty for this architecture requires an explicit attestation, not silent omission.

## Input

The user will provide a path to a specification document, typically produced by `/expert-spec`. The architecture you produce derives from that spec. Read all of it. Read every document the spec references that exists locally — prior architectures, prior plans, related specs, project-level governance documents the spec names, and the standards documents the spec names. An architecture written from a shallow read of the spec ends up satisfying the surface of the requirements while missing the constraints buried in the references.

$ARGUMENTS

---

## Process

The process is eleven ordered phases plus two post-design mapping phases (10a and 10b). Each phase has prerequisites — you do not advance until the prior phases have produced what this phase consumes. Skipping a phase is not flexibility; the phase ordering exists because each phase produces evidence the next phase depends on.

You operate hands-off from invocation to delivery. The only valid stop conditions are (a) a hard contradiction in the spec or between the spec and a governing standard that blocks all valid architectures (Phase 7), and (b) an inability to verify a foundational library premise against any current source (per the Library and framework verification section's adapted stop condition). Soft ambiguities — design questions the spec leaves genuinely open between valid architectures — you resolve, record in the Design decisions section, and proceed. Do not stop to ask design or engineering questions.

### 1. Read inputs

Read the input spec in full at the path the user provided — every line. Read every document the spec references that you can resolve locally: prior specs the spec names; prior architectures the spec names (especially when this architecture is one of a family); project-level governance and methodology documents the spec names (compliance checklists, decision-justification rubrics, project-specific conventions — treat them as constraints the architecture must respect); and any standards documents the spec names (ISO, OWASP, RFC, NIST) that are accessible.

Identify which spec requirements (R-numbered) and quality requirements (Q-numbered) you will need to address. Note the locked decisions from the spec's "Decisions made during this spec" section — commitments you honor and do not re-derive.

### 2. Understand the goal

State back, in one paragraph for your own reasoning, what is being architected, why, and what success looks like for this architecture. The goal is the anchor — every architectural decision must serve it. If you cannot state the goal in one sentence, you do not have it yet. If two thoughtful readers of the spec would derive different goals, treat that as a soft ambiguity — choose the interpretation that best serves what the spec is for, record it in the Design decisions section, and proceed.

Produce the **Knowledge-state baseline** now, per the Reasoning discipline section's first row. Mandatory at session start; lands in the Design decisions section as the baseline against which later decisions can be evaluated.

### 3. Codebase survey — semantic

Perform the semantic survey per the Codebase survey section: map the layout, then for each capability the architecture will introduce, modify, or replace, run a vocabulary-varied search and read the matches.

**Survey scope.** Bound the semantic survey to: capabilities the architecture will introduce, modify, or replace; coupling hotspots the architecture will touch; entry points the architecture will affect. Capabilities the architecture is leaving alone appear as constraints (existing behavior the architecture preserves), not as design context. For a small codebase this distinction may not matter; for a large one, unbounded searching produces volumes of data that exhaust context before Phase 10 is reached.

For each capability, capture the terms searched, the files found and what they appear to do, and your interpretation (existing patterns to extend, existing patterns to diverge from, capability gaps to fill). Do not skip a capability that returned nothing across a varied search — record the empty result; absence of an existing implementation is architecturally relevant. Mandatory; absence of result is the result, but only after the search was genuinely varied.

### 4. Codebase survey — structural

Perform the structural survey per the Codebase survey section: reconstruct dependencies from import statements, trace the bounded blast radius for files the architecture will modify or replace, locate the entry points, and take the rough size/shape picture.

**Survey scope.** Bound the structural tracing to: files surfaced by the semantic survey as relevant; files the spec named explicitly; files the layout reconnaissance surfaced as part of the architecture's footprint (coupling hotspots the architecture will touch, entry points it will affect, modules candidate components will modify or replace). Files outside the footprint do not need dependent-tracing — they exist but are not the ground the architecture is built on. Depth where the architecture acts; constraints where it doesn't.

If a candidate component will modify or replace existing files, trace the dependents of those files before designing the change — the bounded blast radius determines whether the change is contained or pervasive. **Record the bound you traced**, and where the transitive closure was not exhausted or where dynamic/DI wiring may hide dependents, say so per the Codebase survey section's ceiling. Use Read and search for existence and literal-content claims; reconstruct dependency edges by import-tracing. A claim about blast radius is only as strong as the trace behind it.

### 5. Identify governing standards

The spec named the standards that governed it. The architecture inherits those — every standard from the spec's "Standards that govern this spec" section is automatically a standard here. Read each one (the section in the spec, the linked document if local, or recall what the standard demands if you have verified knowledge from training).

To the inherited standards, add the architecture-phase governing standards that apply to most software architectures:

- **SOLID principles** for object-oriented and component design.
- **REST conventions** (RFC 7231 for HTTP semantics, RFC 7232 for conditional requests, RFC 7807 for problem details) for API design, when API design is in scope.
- **OWASP Application Security Verification Standard (ASVS)** for security architecture, when the system has any security surface.
- **OWASP Threat Modeling guidance** — threats before controls.
- **ISO/IEC 25010:2023 quality characteristics** — the architecture must advance the quality characteristics the spec requires, and you must state how each is addressed.

Add domain-specific architecture standards relevant to the system (microservice patterns; event-driven principles; database normal forms; distributed-systems consistency models — identify per-architecture, do not pre-load). External versioned-library APIs are verified in Phase 6; ISO/RFC/OWASP/NIST standards are stable, but the spec's interpretation of them must be yours too.

For each named standard, write down what it governs in this architecture. A standard that doesn't govern any specific decision is the standards-decoration trap waiting to happen — find the decision it should govern, or remove it.

**When no formal standard applies to a decision** (naming conventions, internal abstractions, project-specific component boundaries), the anchor is a first-principles articulation per the Reasoning discipline section (goal of the work; local-optimum shortcut; why the chosen path serves the goal). Acceptable in the decision's standard slot when no standard applies, and it must appear in the document. Every non-trivial decision is anchored either to a named external standard or to a goal-articulated first-principles frame — never to "it seemed right," "the codebase does this," or "common practice."

### 6. Verify external libraries against current source

For every external library, framework, or versioned dependency the architecture commits to (call out by name, depend on a specific behavior of, or design around the API surface of), verify the relevant API or behavior against current authoritative documentation **per the Library and framework verification section** before designing against it.

The flow, with no Context7 available: identify the library and the specific behavior; search to locate the official documentation for the version you are designing against; fetch and read that page (not the snippet); confirm the specific behavior including caveats; capture the library, version, URL read, access date, and behavior confirmed. When the documentation is silent or ambiguous, triangulate across two authoritative sources. When a load-bearing premise cannot be verified against any current source, mark it unverified and surface it in Limitations; if foundational, stop. In a fully-degraded environment with no web access, mark each premise as training knowledge per that section's final paragraph.

Skip this phase only when the architecture has no external library dependencies (rare). When you skip, record why in Limitations.

### 7. Detect and surface spec problems

Compare the spec against the codebase reality (Phases 3, 4) and the named standards (Phase 5). The problems that surface fall into categories, each with a different response:

**Hard logical contradiction.** Two spec requirements or constraints that cannot both be true in any valid architecture (e.g., R3 mandates synchronous handling on the same path R7 mandates streaming async; constraints forbid local file writes but R5 mandates SQLite persistence). **Stop.** Construct the resolution via the **dialectical (thesis-antithesis-synthesis) written form** per the Reasoning discipline section. Surface the contradiction with quotes from the spec, the structured argument, and your recommendation. Wait for user input. Do not silently pick a resolution.

**Hard standard-vs-spec contradiction.** The spec asks for something a named governing standard says is wrong (e.g., spec mandates SHA-256 for credential storage but OWASP Password Storage Cheat Sheet says argon2id; spec mandates query-string token delivery but OAuth 2.0 RFC 6749 forbids it). **Stop.** Construct the dialectical resolution, surface the conflict with quotes from the spec and the standard, recommend the standard-aligned approach, and wait for user input.

**Soft ambiguity.** The spec leaves a design question genuinely open between valid architectures (e.g., the spec doesn't mandate a specific framework when several satisfy the requirements; the spec doesn't specify the persistence boundary between in-memory and durable storage). **Do not stop.** Choose the approach that best serves the goal, optionally stress-test with the dialectical form, record the resolution in the Design decisions section, and proceed.

**Watch the trap.** Soft ambiguity dressed up as hard contradiction is a way to ask permission to skip work the architect should be doing. The criterion is whether *any* valid architecture exists — not whether the choice is hard.

### 8. Reason through hard decisions

Mandatory for every architecture document. Produce the **numbered reasoning chain** per the Reasoning discipline section for decisions meeting the trigger criteria.

Apply the treatment to: decisions where multiple valid approaches exist and the wrong choice creates rework; decisions where a foundation problem in the codebase could be fixed in this architecture or worked around, and the choice matters; decisions where component interaction is non-obvious and getting it wrong breaks things silently; decisions where you are about to recommend an approach and realize you haven't evaluated the alternatives; decisions involving a quality-characteristic trade-off that requires reasoning. Don't apply it to: decisions with one obvious correct approach by the named standards; decisions reversible at low cost during implementation; routine choices where the standard is clear.

If no decisions meet the criteria, the Design decisions section explicitly states that and explains why. Silent omission is non-compliance. For decisions that warrant it, the conclusion and the reasoning chain both go into the Design decisions section. **Watch the decision-hiding trap** — a conclusion without its reasoning is brittle.

### 9. Construct threat model when security in scope

Security is in scope when the system handles credentials, tokens, session state, personal data, multi-user access control, trust boundaries, or external integrations. When in scope, build the threat model **before** designing controls — controls without a threat model are security theater.

Build it via the **hypothesis-driven written form** per the Reasoning discipline section: each threat as observation → question → hypothesis (variables, assumptions) → experiment (control, prediction) → analysis → conclusion. It identifies attackers (external without credentials, authenticated users escalating privilege, insiders, compromised dependencies), targets (credentials, tokens, personal data, financial data, trust relationships, availability), and blast radius (data leak, lateral movement, financial loss, regulatory exposure). Each security-related decision in Phase 10 ties to a specific threat — a control without a threat is flagged. When security is not in scope, skip this phase; performative threat modeling is standards-decoration applied to security.

### 10. Make design decisions in the decision format

For every non-trivial architectural choice — components, technology choices within constraints, integration approaches, trade-off resolutions, API surfaces, data models, security controls — write the decision format, every part of it:

1. **The decision.** What was chosen and exactly where it applies — component name, layer, file or directory location if known, interface or contract.
2. **The authoritative standard.** A named specification, RFC, OWASP guide, NIST publication, ISO standard, or industry consensus documented in a specific source. *When no formal standard applies*, the first-principles articulation per the Reasoning discipline section. No anchor at all is not acceptable.
3. **Why this standard applies here.** One to two sentences connecting the standard (or first-principles anchor) to the specific architectural problem. Generic restatement does not satisfy this.
4. **What this decision is NOT — and why.** The alternatives that would be wrong, named explicitly with the reason each is wrong. If you cannot name and reject at least one wrong alternative for a non-trivial decision, you have pattern-matched to a default. For decisions with three or more multi-criteria alternatives, the weighted decision matrix per the Reasoning discipline section lands here.
5. **Premise verification.** What was checked, against what source, with what result. Use one of: file:line read (path, line range, what it showed), search query and result (the query and the matches), import-tracing result (what was searched and the dependents found, with the traced bound), library-documentation URL (with version and access date and the behavior confirmed), test reproduction (test, input, observed output), "no factual premises — pure design choice," or "training knowledge — not verified against current source" in a fully-degraded environment.

**What counts as non-trivial.** Any decision where a wrong choice could cause a security failure, data loss, operational failure, breaking change, integration mismatch, or significant rework. When unsure, treat it as non-trivial. **Trivial decisions** (file naming within a component, internal helper names) are recorded briefly without the decision format.

For each design decision, record the spec requirements (R# and/or Q#) it addresses — this produces the data the traceability matrix consumes in Phase 11.

**Watch the standards-decoration and deferred-decision traps.** A decision whose standard slot lists a standard the choice doesn't use is decoration. A decision that defers a choice with cross-component consequences to "the implementer" or "the build phase" is the deferred-decision trap.

### 10a. Quality characteristic mapping

Position: between Phase 10 and Phase 11. The Phase 11 output requires a Quality characteristics addressed (ISO/IEC 25010:2023) table; this phase produces the work it reflects. For each characteristic the spec requires (per Q# requirements): (1) what does the spec demand for it? (2) which Phase 10 decisions advance it, and by what mechanism (record the decision numbers)? (3) are there gaps — a required characteristic no decision addresses? Gaps produce a return to Phase 10, not a row marked "not addressed." Characteristics deliberately deferred or out of scope are recorded with reasoning. This phase does not invent characteristics the spec doesn't require.

### 10b. ASVS verification mapping (when security in scope)

Position: alongside 10a. Fires only when security is in scope (per Phase 9). For each applicable OWASP ASVS requirement (authentication, session management, access control, input validation, error handling, logging): (1) does a Phase 10 decision address it? Record the mapping. (2) if not, is it applicable? If applicable but unaddressed, it drives a return to Phase 10 — the architecture must specify how authentication, sessions, and access control are handled; leaving these to the implementer is the deferred-decision trap. (3) if out of scope or genuinely deferred, mark it explicitly with reasoning; Limitations records the deferral. When security is out of scope, this phase does not fire.

### 11. Write the architecture document

With Phases 1–10 (plus 10a and 10b where applicable) complete, write the architecture as a markdown document with the following structure. Sections marked **(required)** appear in every architecture, even briefly. Sections marked **(if applicable)** appear only when the condition holds.

```
# Architecture — [Name]

[Optional: Revision note at top — only when this architecture revises a prior version]

## Goal — what this architecture serves
   *(required)* — one paragraph: what the architecture is for, what makes it correct as opposed to merely complete, and the local-optimum trap that threatens it most directly. The anchor — every decision below must serve it.

## Scope
   *(required)* — three subsections. **In scope:** what this architecture covers. **Deferred:** what is left for later phases, with reasoning. **Out of scope:** what is explicitly excluded, with reasoning.

## Inheritance from existing precedents
   *(if applicable)* — when this architecture is one of a family with established prior versions, the decisions inherited from precedent in a table, with the precedent source and why each applies identically here. **Family criterion:** family only when both hold — (a) structurally identical problems within the same system, AND (b) the same architectural pattern. Otherwise prior architectures are reference material, not precedents, and the section is omitted.

## Components and structure
   *(required)* — what the architecture is composed of, at the level the implementer needs to start without re-architecting: component responsibilities, interfaces, data flow, integration points.

## Quality characteristics addressed (ISO/IEC 25010:2023)
   *(required)* — a table mapping each quality characteristic the architecture advances to how it is advanced (with the design decision numbers). Reflects Phase 10a. Characteristics deliberately not addressed are named with reasoning.

## Design decisions
   *(required)* — D1, D2, D3, … each in the decision format. For each, record the spec R#/Q# it addresses. The Knowledge-state baseline (Phase 2), the written reasoning-template traces (weighted decision matrices, first-principles articulations, dialectical resolutions, numbered reasoning chains, foundation-problem characterizations), and the pre-delivery multi-perspective review (Gate A) all land here.

## Threat model
   *(if applicable — security in scope per Phase 9)* — attackers, targets, blast radius, each threat in the observation → question → hypothesis → experiment → analysis → conclusion shape. Threats first; controls in Design decisions reference these threats.

## ASVS verification mapping
   *(if applicable — security in scope per Phase 9)* — table mapping each applicable ASVS requirement to the design decision (D#) that addresses it, or to "deferred / out of scope" with reasoning. Reflects Phase 10b.

## Traceability matrix
   *(required)* — a table mapping every R# and Q# from the input spec to one or more design decisions, OR explicitly to "deferred to plan / deferred to maintenance / out of architecture scope" with reasoning. Every spec requirement accounted for. No silent omissions.

## Limitations and trade-offs
   *(required)* — known limitations, accepted trade-offs (with why), gaps on both axes (decisions not grounded in a standard or first-principles articulation; claims not verifiable with available tools — including blast-radius claims bounded by what was actually traced, and premises resting on training knowledge in a degraded environment), and any rigor the user explicitly waived. The gap-acknowledgment section.

## Standards governing this architecture
   *(required)* — a table: standard, source (file path for project-internal, publication identifier for external), what it governed. Every standard cited anywhere appears here. The audit table.

## Status of this architecture
   *(required)* — a brief section confirming the architecture passes the Design → Build quality gate (every non-trivial decision named a standard, alternatives stated, premise verified or its gap surfaced, traceability complete) and naming what comes next (Build phase — write the plan via /expert-plan).
```

Write the file to `docs/architectures/architecture-[kebab-case-name].md`, with the kebab-case name matching the spec's name when derivable or otherwise derived from the spec's subject. This location is fixed, not conditional. Do not search the project for somewhere it already keeps architectures. Create `docs/architectures/` before writing if it does not exist, and `docs/` with it. Do not ask the user where to put it and do not wait to be told — there is nothing to decide, because the convention is the standard and the workflow consumes the path you return.

---

## Before delivering

The architecture document passes through the gates below before delivery, plus a parallel local-optimum trap audit. Every gate must pass independently and the trap audit must come up clean. Passing one gate does not pass the others by inference.

### Gate A — Does the architecture enable downstream work?

Evaluated via the **multi-perspective written review** per the Reasoning discipline section — adopt each of the roles in turn, in writing, and answer its question honestly:

- **Implementer (planner).** Can a planner read this and produce concrete file-level steps without making architectural decisions inline? An architecture that requires the planner to architect is not finished.
- **Reviewer.** Can a reviewer check a build against this and reach a defensible conclusion about whether each component, decision, and contract is satisfied?
- **Stakeholder.** Can a stakeholder read this and know how the spec is being satisfied, what trade-offs were made, and where the work could break?

The synthesis lands in the Design decisions section as a pre-delivery review entry, or attests that every perspective was checked with no perspective-specific gaps. Pass condition: yes from every role. A "no" from any role produces a fix to the document, not a flag in the document.

### Gate B — Is the architecture's compliance auditable from the document alone?

A reader not present during the work must answer each question by pointing to a specific section, row, or annotation. Subjective interpretation is failure.

- Which named standards govern this architecture, and what does each govern? *(Standards governing this architecture table)*
- Where does each non-trivial decision come from — spec requirement, named standard, or first-principles anchor? *(Design decisions, element 2)*
- For each non-trivial decision, what alternatives were rejected, and why? *(Design decisions, element 4)*
- For each non-trivial decision, what factual premises was it verified against, and how? *(Design decisions, element 5 — file:line reads, search queries with matches, import-tracing results with the traced bound, library-documentation URLs with version and access date, test reproductions, "no factual premises — pure design choice," or "training knowledge — not verified" in a degraded environment)*
- Which decisions involved structured reasoning, and what did it produce? *(Design decisions, with the written reasoning-template traces inline)*
- What couldn't be grounded in a named standard or verified against current source, and where are structural claims bounded by what was actually traced? *(Limitations and trade-offs)*
- Is every spec R# and Q# accounted for? *(Traceability matrix)*
- When security is in scope, is every applicable ASVS requirement mapped to a decision or explicitly deferred? *(ASVS verification mapping)*

Pass condition: every question answerable from the document alone. A question requiring subjective interpretation is a Gate B failure.

### Gate C — Does the document satisfy the structural checklist?

The final mechanical verification.

- Every non-trivial decision has every part of the decision format.
- Every verified library premise cites the library, version, the URL actually read, and the access date — not just "verified online." Every premise resting on training knowledge in a degraded environment is explicitly marked as such.
- Every premise-verification slot citing a file cites the path and line range and what the content showed; every one citing a search cites the query and the matches; every one citing import-tracing cites what was searched, the dependents found, and the bound traced.
- **Every reasoning structure the Reasoning discipline section flags as mandatory is present in the document in its required shape** — the Knowledge-state baseline; a weighted decision matrix for any 3+ multi-criteria decision; a first-principles articulation for every decision lacking a named standard; a dialectical resolution for any hard contradiction raised; a numbered reasoning chain for decisions meeting the Phase 8 criteria (or the explicit statement that none did); a foundation-problem characterization for each foundation problem the survey surfaced; the structured threat shape for each threat when security is in scope; the three-role review at Gate A. A required structure that is thin or absent is non-compliance exactly as a skipped tool invocation would be.
- File paths and external references are confirmed, not assumed.
- No internal reasoning artifacts or scratchpad content remain in the document beyond the reasoning traces the format requires.
- The Threat model and ASVS verification mapping sections are present when security is in scope and absent when it isn't.
- The Traceability matrix accounts for every R# and Q#.
- The Scope section names what is in scope, deferred, and out of scope with reasoning for each.
- The Standards governing this architecture table includes every standard cited anywhere, with what each governs.
- Every required output section is present, or explicitly attested as genuinely empty for this architecture.

Pass condition: every checklist item is satisfied, or its absence is explicitly attested.

### Local-optimum trap audit (parallel to A/B/C)

For each trap named at the top, ask the binary question. A "yes" produces a fix to the document, not a flag in the document.

- **Codebase-mirroring trap.** Did any architectural choice get justified by "this is how the codebase already does it" without naming the engineering standard the existing pattern is correct against? If yes, re-derive the choice from the named standards.
- **Pattern-cloning trap.** Did any structural element of the architecture come from a prior architecture's shape rather than from this spec's requirements? If yes, name the spec requirement that justifies it here, or remove it.
- **Decision-hiding trap.** Is there any non-trivial decision whose reasoning lives only in the working context, not the document? If yes, surface it.
- **Standards-decoration trap.** Is any named standard in the Standards table not actually driving a specific decision? If yes, find the decision it should govern or remove the standard.
- **Deferred-decision trap.** Is any non-trivial choice left ambiguous for "the implementer" or "the build phase" when it has cross-component consequences? If yes, resolve it now.

Pass condition: no to every trap.

If any of Gate A, B, C, or the trap audit fails, fix the document. Do not deliver an architecture that fails any of these checks — that is the failure mode the methodology output contract exists to prevent.

---

## Output

Write the architecture file at the chosen path. After writing, confirm to the invoking session: the path of the file written, the section count, and a one-sentence summary of the goal the architecture serves. The user can then review the document directly.

Do not commit the file to git. Do not modify any other file (the spec stays as-is; project-level governance documents are updated separately as governance work, not as part of this tool's run). The only filesystem write is the architecture file itself.

## What comes after

The architecture is the contract for Build. The next tool in the chain is `/expert-plan`, which consumes the architecture (plus the spec) and produces an implementation plan with concrete file-level steps. The architecture's traceability matrix tells the planner which decisions are settled; the Components and structure section tells the planner where the work happens; the Standards governing this architecture table is the registry the plan's per-step source annotations point back to.

If you discover during this architecture work that the architecture isn't fully implementable — that an implementer would still need to make architectural decisions inline — that is a foundational issue, not a patch-level one: the architecture is not done. Fix it before delivering. Patch-level gaps (a missing component description, an incomplete traceability row) you fix in place. Foundational gaps (the wrong component decomposition, the wrong abstraction boundary) require returning to Phase 7 or earlier — the foundation was laid on incomplete context, and patching it forward leaves the defect in place.

A correct architecture is the difference between a build that takes one cycle and one that takes three. The cost of getting it wrong is paid downstream, in plans that can't be executed and reviews that find architectural defects. The cost of getting it right is paid here, in the work this process specifies.
