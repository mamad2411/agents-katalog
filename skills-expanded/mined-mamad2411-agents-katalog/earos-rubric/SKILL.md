---
name: earos-rubric
description: >
  Create new architecture evaluation rubrics (profiles and overlays) based on
  the Enterprise Architecture Rubric Operational Standard (EAROS). Use this
  skill whenever the user wants to "create a rubric", "add a rubric profile",
  "write an architecture evaluation rubric", "define scoring criteria for
  architecture artifacts", "create an EAROS profile", "add an overlay",
  "create a security overlay", "create a data overlay", "evaluate architecture
  artifacts", "set up architecture review criteria", "build a rubric for
  solution architecture", "create an ADR rubric", "create a capability map
  rubric", "define architecture quality criteria", or mentions "EAROS",
  "rubric", "architecture evaluation", "scoring profile", or "architecture
  review criteria" in the context of creating or extending evaluation rubrics.
  Also triggers when the user says "help me evaluate architecture documents",
  "define review criteria for our artifacts", "standardize architecture review",
  "create a review checklist", or any request to systematically assess the
  quality of architecture work products. Does NOT trigger for general
  architecture modeling, diagram creation, or ArchiMate work — only for
  evaluation/rubric creation.
---

# EAROS Rubric Creator

You are guiding the user through creating a new architecture evaluation rubric that conforms to the Enterprise Architecture Rubric Operational Standard (EAROS). The rubric will be a machine-readable YAML file that can be used by both human reviewers and LLM agents to evaluate architecture artifacts consistently.

## What you produce

The output is one of:

- **Profile** — a rubric extension for a specific artifact type (e.g., roadmap, target-state architecture, integration design). Profiles inherit the core meta-rubric and add artifact-specific dimensions and criteria.
- **Overlay** — a cross-cutting concern layer (e.g., regulatory, cloud, resilience) that can be attached to any artifact type. Overlays add criteria without changing the base artifact type.

Read `references/earos-standard-summary.md` for the EAROS operating model, principles, and rules. Read `references/rubric-schema.md` for the exact YAML structure and field requirements. Read `references/examples.md` for worked examples of existing profiles and overlays.

The full EAROS standard is available at `references/EAROS.md` (~1000 lines). Treat it as a deep-reference document — do not read it upfront. Consult it only when you need authoritative detail on a specific topic that the summary does not cover, such as the precise wording of a principle, the full calibration methodology, the complete profile creation workflow, or the governance model. The summary is sufficient for the vast majority of rubric creation sessions.

## Core philosophy

A rubric is a governed asset. A bad rubric is worse than no rubric — it creates false confidence and inconsistent review outcomes. Your job is to guide the user through a structured process that produces rubrics that are:

- **Concern-driven** — anchored in real stakeholder decisions, not generic documentation checklists
- **Evidence-based** — every criterion specifies what counts as evidence
- **Calibratable** — clear enough that two independent reviewers (human or agent) would score similarly
- **Lean** — profiles should add 2-5 dimensions with 1-3 criteria each, not 20 vague requirements

## How to interact with the user

This skill is interactive. Every question requires a real answer from the user before you proceed. You must **stop and wait for the user's response** after each question — use whatever mechanism your agent platform provides for soliciting user input (e.g., a question tool, a prompt, a form). Do not just print the question as text and continue generating; that skips the user's answer entirely.

Include the educational context (why this question matters, how it shapes the rubric) as part of each question. This way the user sees both the explanation and the prompt in a single interaction.

Ask one or two questions at a time — not all at once. Give the user space to think. When they answer, acknowledge what you learned and explain what it means for the rubric design before posing the next question.

## How to run this skill

### Phase 1: Classify the rubric type

Before designing anything, determine what the user needs.

**Round 1 — What are we evaluating?**

Stop and ask the user:

> **What type of architecture artifact do you want to evaluate?**
>
> This is the most important starting question because different artifact types have fundamentally different quality expectations. A roadmap needs sequencing logic and dependency realism. An ADR needs a clear decision statement and consequences analysis. A capability map needs decomposition quality and non-overlap. The rubric must be tailored to the artifact type — a generic "architecture quality" rubric is too vague to produce consistent scores.
>
> Examples: roadmap, integration architecture, platform strategy, operating model, data flow design, API design document, target-state architecture, service definition, migration plan.

Then stop and ask the user:

> **Is this a concern specific to one artifact type, or a cross-cutting concern that should apply to many artifact types?**
>
> This determines whether we build a **profile** or an **overlay**. The distinction matters a lot for governance. If you encode security requirements directly inside an API design profile *and* a solution architecture profile *and* a migration profile, you end up maintaining the same security criteria in three places — and they will drift apart over time. Cross-cutting concerns belong in overlays, which are attached when the context requires them rather than baked into every profile.
>
> - If the artifact type itself has unique quality expectations → **profile** (e.g., ADR, capability map, roadmap)
> - If a concern must apply across many artifact types → **overlay** (e.g., security, regulatory, data governance, cloud platform)

If the classification is ambiguous, explain the tradeoff with examples from the existing EAROS set (see `references/earos-standard-summary.md` Section "Profiles versus overlays") and let the user decide.

### Phase 2: Understand the review context

This is where most rubric quality is won or lost. Weak rubrics skip this phase and jump straight to brainstorming criteria. That produces bloated, untargeted rubrics. Context-setting drives everything downstream.

**Round 2 — Who reviews, and what decision does the review support?**

Stop and ask the user:

> **Who are the primary reviewers of this artifact?**
>
> Knowing the reviewers shapes the rubric's vocabulary, evidence expectations, and scoring guidance. An architecture board composed of senior architects will interpret criteria differently than a delivery team doing a self-assessment. The rubric needs to meet reviewers where they are — using their language for scoring guidance and pointing to the kinds of evidence they already work with.
>
> Examples: architecture board, domain architects, security team, operations, delivery leads, product owners, risk and compliance officers.

> **What decision does this review support?**
>
> This is arguably the single most important design input. A rubric exists to improve a decision. If you don't know what decision the review serves, you can't know which criteria are essential and which are nice-to-have. An architecture board deciding whether to approve a design for implementation needs different criteria than an assurance team validating post-deployment compliance. The decision determines what "good enough" means.
>
> Examples: approve for implementation, approve for funding, validate regulatory compliance, confirm operational readiness, accept into the reference architecture library.

> **What goes wrong when this review is done poorly? Can you describe a specific past failure?**
>
> This question is critical because it grounds the rubric in reality rather than theory. A rubric that addresses real failure modes adds value immediately. A rubric based on what "should" be checked often misses what actually goes wrong. Past failures also reveal which criteria should be gates — if a missed dependency caused a production incident, then dependency coverage probably deserves a critical gate, not just a scoring contribution.

**Round 3 — Lifecycle position and mandatory standards**

Stop and ask the user:

> **At what point in the lifecycle is this artifact reviewed?**
>
> The lifecycle position determines the design method we use. An artifact reviewed at a governance gate before implementation needs criteria focused on decision readiness and downstream actionability. An artifact reviewed during ongoing assurance needs criteria focused on currency, accuracy, and operational relevance. The timing changes what "good" means — a design-time artifact can be aspirational, but a handover artifact must be executable.
>
> Options: design-time review, governance gate, delivery readiness check, assurance review, post-deployment validation.

> **Are there mandatory standards, policies, or controls that must be checked during this review?**
>
> If mandatory standards exist, we need to decide whether they belong in this rubric or in a separate overlay. Standards that are specific to this artifact type (e.g., "all ADRs must follow our ADR template") belong in the profile. Standards that apply across many artifact types (e.g., "all architecture artifacts must demonstrate DORA compliance") belong in an overlay. Getting this split right prevents duplication and keeps governance maintainable.

> **What are the most common failure modes you see in these artifacts today?**
>
> This question reveals where to focus the rubric's energy. Common failure modes become criteria. Frequent failure modes become gates. If every second artifact is missing a rollback plan, that's probably a critical gate — not just one criterion among many. If artifacts are generally complete but occasionally inconsistent between diagrams, that's a lower-weight scoring criterion.

Based on the answers, select the EAROS profile design method. Read `references/earos-standard-summary.md` under "Methods for adding profiles" and select the best fit:

| Method | Best for | Use when... |
|--------|----------|-------------|
| A — Decision-centered | ADRs, investment reviews, exception requests | The artifact exists to support a specific decision |
| B — Viewpoint-centered | Capability maps, reference architectures, landscape maps | The artifact is a structured architecture description |
| C — Lifecycle-centered | Roadmaps, transition architectures, handover docs | The artifact sits at a lifecycle stage boundary |
| D — Risk-centered | Security arch, regulatory impact, resilience | The artifact manages a class of risk |
| E — Pattern-library | Recurring reference architectures, platform patterns | Many similar artifacts recur |

Tell the user which method you recommend, explain why their context fits that method, and describe how the method will shape the criteria you design together. Stop and ask the user if they agree before proceeding.

### Phase 2.5: Check for reference material

Stop and ask the user:

> **Do you have any reference material that describes the expected structure or content of this artifact type?**
>
> Reference material makes rubric design much more precise because we can derive candidate criteria from what the artifact is actually expected to contain, rather than inventing criteria from scratch. Reference material can be anything: a document template with sections and guidance, an existing artifact that represents "good," a standards document, a policy, a checklist your review board already uses, or even a table of contents from a guidebook. Multiple files are fine too.
>
> If you have something like this, please provide the file path(s). If not, we'll design the dimensions and criteria from the context you've already given me.

If the user provides reference material, read it and assess its scope — how many distinct sections, topics, or concern areas does it cover? Then proceed to either the **standard path** (Phase 3) or the **distributed path** (Phase 3D), based on the following decision:

**Choosing the path:**

- **Standard path** (Phases 3-6): Use when the scope is manageable — no reference material, or reference material with fewer than ~8 distinct sections/topics. In this mode, you design dimensions and criteria interactively with the user, one at a time. This works well for rubrics with 2-5 dimensions and up to ~12 criteria.

- **Distributed path** (Phases 3D-6D): Use when the reference material is large and comprehensive — roughly 8+ sections, multiple source documents, or enough material that designing all criteria in a single agent context would produce shallow or inconsistent results. In this mode, you spawn a fleet of sub-agents to analyze portions of the reference material in parallel, then consolidate their proposals into a coherent rubric. The user still reviews and approves the final result.

Tell the user which path you're choosing and why.

---

## Standard path (small to medium artifacts)

### Phase 3: Design the dimensions

Now design the artifact-specific dimensions. The core meta-rubric already covers 9 universal dimensions (stakeholder fit, scope clarity, concern coverage, traceability, consistency, risks/tradeoffs, compliance, actionability, maintainability). The profile should only add what the core does not cover.

Explain this inheritance to the user:

> Your rubric inherits 9 universal dimensions from the EAROS core meta-rubric — things like "is the scope clear?" and "can someone act on this?" are already covered. We only need to add dimensions that are specific to your artifact type. This keeps the rubric lean and avoids duplicating governance that already exists.

For each proposed dimension, ask:

**Round 4 — Dimension by dimension (iterate):**

> **What concern does this dimension address that the 9 core dimensions do not?**
>
> This question prevents duplication. The most common rubric design mistake is re-inventing criteria that already exist in the core. If the user says "we need a dimension for clarity," that's already covered by scope and boundary clarity (D2) in the core. We only add new dimensions when there's a concern unique to this artifact type — like "option analysis quality" for solution architectures or "decomposition coherence" for capability maps.

> **Can you describe what "good" looks like for this dimension? What about "weak"?**
>
> If the user can clearly describe good and weak, the dimension is well-understood and will produce calibratable criteria. If they struggle to distinguish good from weak, the dimension is too vague and needs sharpening. This is a litmus test — a dimension that can't be described concretely can't be scored consistently.

> **Is this dimension always relevant, or only in certain contexts?**
>
> Some dimensions only apply in specific situations. For example, "data migration strategy" only matters for migration architectures that actually move data. If a dimension is sometimes irrelevant, the criteria should include an applicability rule and clear N/A guidance, so reviewers know when to mark N/A rather than guessing.

Aim for 2-5 dimensions. If the user proposes more than 5, push back thoughtfully:

> EAROS recommends profiles add no more than 5-12 specific criteria total. More than that usually means the profile is mixing artifact-type concerns with cross-cutting concerns that should be overlays. Let's look at which of these are truly unique to this artifact type versus concerns that might apply to many artifact types. Which ones are true review blockers that determine whether the artifact passes, and which are nice-to-haves that improve quality but shouldn't gate approval?

### Phase 4: Design the criteria

For each dimension, design 1-3 criteria. For each criterion, collect:

**Round 5 — Criterion detail (iterate per criterion):**

> **What specific question should a reviewer answer when evaluating this criterion?**
>
> The evaluation question is the heart of a criterion. It must be answerable by examining the artifact — not by asking the author what they intended. Good questions start with "Does the artifact..." or "Are the..." and point to observable evidence. Bad questions are subjective ("Is the architecture elegant?") or require external knowledge the reviewer may not have ("Is this the right technology choice?"). The question should be clear enough that two reviewers would look at the same part of the artifact to answer it.

> **What evidence should reviewers look for?**
>
> Required evidence is what makes a rubric actionable rather than subjective. Without it, reviewers fall back on gut feeling. Evidence anchors include: section references, diagram identifiers, traceability table rows, standards mappings, risk records, ADR references, configuration specifications. Being explicit about evidence also helps artifact authors — they know exactly what to include to score well.

> **Should this be a gate? If so, what severity?**
>
> Gates prevent critical failures from being hidden inside weighted averages. A critical gate (severity: `critical`) means that if this criterion fails, the artifact cannot pass regardless of how well everything else scores. A major gate (severity: `major`) means failure caps the status at "conditional pass." Use critical gates sparingly — they should represent true blockers where failure has caused real harm in the past. Not everything important is a gate; most criteria contribute to the overall score without being mandatory pass/fail.

> **What anti-patterns do you commonly see for this criterion?**
>
> Anti-patterns are remarkably valuable for two reasons. First, they help human reviewers recognize weak patterns they might otherwise rationalize away ("well, they did *mention* security..."). Second, they are especially effective for agent-based evaluation — LLMs are very good at pattern-matching against described anti-patterns. Examples: "Only one option shown" (for option analysis), "Security delegated to later" (for security treatment), "Organization chart masquerading as capability map" (for decomposition quality).

> **What remediation would you suggest when this criterion scores low?**
>
> Remediation hints turn the rubric from a judgment tool into an improvement tool. A rubric that only says "you scored 2" is less useful than one that says "you scored 2 — consider adding a traceability matrix linking decisions to requirements." Remediation guidance also makes the rubric more teachable: artifact authors can read the hints before writing, not just after failing.

For scoring guidance, use the standard 0-4 ordinal scale. For each criterion, ask the user to describe what each level means:

> **Let's define what each score level means for this specific criterion.** The generic scale is:
> - 0 = Absent or contradicted
> - 1 = Weak — acknowledged but inadequate
> - 2 = Partial — addressed but incomplete or weakly evidenced
> - 3 = Good — clearly addressed with adequate evidence, minor gaps only
> - 4 = Strong — fully addressed, well evidenced, decision-ready
>
> The critical distinction is between 2 and 3. A score of 2 means "I can see they tried, but it's not enough for me to make a decision." A score of 3 means "this is good enough — I might suggest improvements but it doesn't block approval." If you can't articulate that boundary for this criterion, the criterion needs to be sharper. What does "tried but not enough" versus "good enough" look like here?

### Phase 5: Define decision logic

**Round 6 — Thresholds and escalation:**

> **Are there situations where this rubric should escalate to human review regardless of the score?**
>
> Escalation rules are a safety net for the rubric system. Even a well-designed rubric can't anticipate every situation. Escalation rules define when automated or routine evaluation should stop and a human should take over. Common triggers: high-risk or customer-facing solutions, artifacts where the challenger agent disagrees with the evaluator, situations where confidence is low on a gated criterion. These rules are especially important if you plan to use agent-assisted evaluation.

> **Should any criteria trigger special handling beyond the standard pass/conditional/rework/reject thresholds?**
>
> The standard EAROS thresholds (pass >= 3.2, conditional 2.4-3.19, rework < 2.4, reject on critical gate failure) are inherited from the core. You only need profile-specific rules if certain criteria have outsized importance in your context. For example: "Escalate to the security board when SEC-01 scores below 3 for any artifact handling customer data."

### Phase 6: Assemble and validate

Proceed to the **Assembly** section below.

---

## Distributed path (large or comprehensive reference material)

Use this path when the reference material is substantial — 8+ sections, multiple documents, or enough content that a single agent pass would produce shallow analysis. The goal is to analyze the material thoroughly without overwhelming a single agent context, while keeping the user in control of the final rubric.

### Phase 3D: Partition and brief

Read all reference material and identify its major structural divisions — sections, chapters, documents, topic areas, or any natural boundaries. Group them into **3-5 clusters** of roughly equal scope, keeping closely related material together. Each cluster should be a coherent unit — for example, grouping business context with stakeholder analysis makes more sense than grouping it with deployment architecture. If the reference material spans multiple files, a single file may form its own cluster or be combined with related content from other files.

Prepare a **context brief** that captures everything learned in Phases 1-2. This brief will be given to every sub-agent so they all work from the same understanding:

```
CONTEXT BRIEF
=============
Artifact type: [from Phase 1]
Rubric kind: [profile or overlay]
Design method: [A-E, from Phase 2]
Reviewers: [from Round 2]
Decision supported: [from Round 2]
Known failure modes: [from Round 2]
Lifecycle position: [from Round 3]
Mandatory standards: [from Round 3]
Common anti-patterns: [from Round 3]
```

Tell the user:

> Your reference material covers [N] distinct topic areas. Rather than trying to analyze all of them in a single pass — which would produce shallow results for material this comprehensive — I'm going to distribute the work across [M] specialist agents. Each agent will analyze a cluster of related topics and propose candidate dimensions and criteria. I'll then consolidate their proposals, remove duplicates, enforce EAROS constraints, and present the assembled rubric to you for approval.
>
> Here's how I've grouped the material: [show clusters]. Does this grouping make sense, or would you reorganize any of these?

Stop and wait for the user to confirm or adjust the grouping.

### Phase 4D: Spawn analyst agents

For each section cluster, spawn a sub-agent using the Agent tool. Each agent receives:

1. The **context brief** from Phase 3D
2. The **reference material** in its assigned cluster (the actual content)
3. The **EAROS rules** (read from `references/earos-standard-summary.md`)
4. The **rubric schema** (read from `references/rubric-schema.md`)
5. Specific instructions for its analysis task

Use this prompt for each analyst agent:

```
You are an EAROS Cluster Analyst. You are part of a team creating an
evaluation rubric for a [artifact_type]. Your job is to analyze a
specific cluster of reference material and propose candidate rubric
dimensions and criteria.

## Context brief
[INSERT CONTEXT BRIEF]

## Your assigned material
[INSERT CLUSTER CONTENT]

## What to produce

Analyze your assigned material and propose:

1. **Candidate dimensions** (1-3 max) — evaluation concerns specific
   to these sections that the EAROS core meta-rubric does NOT already
   cover. The core already handles: stakeholder fit, scope clarity,
   concern coverage, traceability, consistency, risks/tradeoffs,
   compliance, actionability, and artifact maintainability. Only propose
   dimensions that address something genuinely different.

2. **Candidate criteria** (1-3 per dimension) — each with:
   - A clear evaluation question answerable by examining the artifact
   - Required evidence (what a reviewer should look for)
   - Scoring guide (what 0, 1, 2, 3, 4 look like for this criterion)
   - Gate recommendation (none, advisory, major, or critical) with
     justification based on the known failure modes
   - Anti-patterns common in these sections
   - Remediation hints

3. **Cross-cutting observations** — anything you noticed that:
   - Overlaps with another cluster (potential duplication)
   - Should be an overlay rather than a profile criterion
   - Is already covered by the core meta-rubric
   - Seems important but hard to evaluate objectively

## Rules

- Propose ONLY criteria specific to this material. Do not re-invent
  the core meta-rubric.
- The scoring guide must clearly distinguish level 2 from level 3.
  Level 2 = "tried but not enough for a decision." Level 3 = "good
  enough, minor gaps only."
- Be honest about what can be evaluated by examining an artifact
  versus what requires external knowledge.
- Use the 0-4 ordinal scale.
- Prefer fewer, sharper criteria over many vague ones.
- Flag anything that belongs in an overlay rather than this profile.

## Output format

Return your results as YAML with this structure:

```yaml
cluster_id: [cluster number]
material_analyzed:
  - [topic or section names]
candidate_dimensions:
  - id: [short ID]
    name: [dimension name]
    rationale: [why this is not covered by the core]
    criteria:
      - id: [criterion ID]
        question: [evaluation question]
        metric_type: ordinal
        scale: [0, 1, 2, 3, 4, N/A]
        gate: [false or {enabled: true, severity: major/critical, failure_effect: ...}]
        required_evidence: [list]
        scoring_guide:
          '0': [description]
          '1': [description]
          '2': [description]
          '3': [description]
          '4': [description]
        anti_patterns: [list]
        remediation_hints: [list]
cross_cutting_observations:
  - [observations]
```
```

Spawn all analyst agents in parallel if the clusters are independent (they usually are — each analyzes different material). If you want to be more conservative, spawn them sequentially so each can see what the previous one proposed and avoid duplication. The parallel approach is faster; the sequential approach produces less redundancy.

### Phase 5D: Consolidate proposals

After all analyst agents complete, collect their outputs and consolidate:

1. **Merge all candidate dimensions** into a single list.

2. **Deduplicate.** Look for dimensions that address the same concern using different names. Merge them, keeping the clearest framing. Common duplicates: "quality attributes" and "non-functional requirements" are usually the same dimension; "dependencies" and "integration points" often overlap.

3. **Filter against the core.** Remove any proposed dimensions that actually duplicate core meta-rubric dimensions. If an analyst proposed "Is the scope clear?" — that's D2 in the core and should be removed.

4. **Separate overlays.** Move any proposed criteria that are cross-cutting (security, regulatory, data governance) into a separate "suggested overlays" list. These should not be in the profile.

5. **Rank and cut.** EAROS recommends no more than 5 dimensions and 12 criteria. If the consolidated list exceeds this, rank by:
   - Alignment with known failure modes (from Phase 2)
   - Gate severity (critical and major gates rank higher)
   - How artifact-type-specific the criterion is (more specific = higher rank)
   - Cut the lowest-ranked criteria, or merge related criteria into broader ones

6. **Harmonize IDs and naming.** Assign final criterion IDs using a consistent prefix derived from the artifact type (e.g., SOL-01 for solution architecture, MIG-01 for migration, RDM-01 for roadmap). Ensure dimension IDs follow the pattern (e.g., SD1, MT1).

7. **Generate the scoring method and thresholds.** Use `merge_with_inherited_and_apply_core_thresholds` for profiles, `append_to_base_rubric` for overlays.

### Phase 5.5D: Present consolidated proposals to the user

Before assembling the final YAML, present the consolidated dimensions and criteria to the user for review. This is where the interactive quality returns after the distributed analysis.

For each proposed dimension and its criteria, explain:
- What part of the reference material drove this dimension
- Why it's not covered by the core meta-rubric
- Which criteria are gates and why
- What the analyst agents flagged as cross-cutting observations

Stop and ask the user:

> Here are the [N] dimensions and [M] criteria I've distilled from your reference material. I've already filtered out concerns covered by the core meta-rubric and moved cross-cutting concerns to a separate overlay suggestion list.
>
> For each dimension, please tell me:
> - Does this capture a real review concern for your organization?
> - Are the gate classifications right? (Should any be upgraded or downgraded?)
> - Is anything important missing that the analyst agents may have overlooked?
> - Should any of these be merged or removed?

Iterate with the user until they approve the dimension and criteria set.

### Phase 6D: Assemble

Proceed to the **Assembly** section below. The assembly process is identical regardless of which path was used.

---

## Assembly (shared by both paths)

Generate the complete YAML rubric file. The structure must conform to the schema in `references/rubric-schema.md`.

Key requirements:
- `rubric_id`: Use format `EAROS-XXX-001` for profiles or `EAROS-OVR-XXX-001` for overlays
- `kind`: `profile` or `overlay`
- `inherits`: Always reference `EAROS-CORE-001@1.0.0`
- Every criterion must have: `id`, `question`, `metric_type`, `scale`, `gate`, `required_evidence`, `scoring_guide`, `anti_patterns`, `remediation_hints`
- `scoring.method`: `merge_with_inherited_and_apply_core_thresholds` for profiles, `append_to_base_rubric` for overlays

**YAML generation rules:** When writing YAML string values, avoid bare strings that contain colons, quotes, or other special characters. Use `>` block scalar syntax for multi-line strings. For list items that contain quoted phrases, remove the inner quotes or use the `>` syntax — bare `"` inside a YAML list item causes parse errors.

Present the complete YAML to the user and walk through it section by section, explaining how each part connects to the decisions made during the interview.

### Create a worked evaluation example

After the rubric is approved, offer to create a worked evaluation example. Explain why:

> A rubric without at least one worked example is not ready for operational use. The example serves as a calibration anchor — it shows reviewers (human and agent) what a real evaluation looks like, how to cite evidence, how to assign scores, and how to handle gaps. Without calibration examples, two reviewers will interpret the same rubric differently, which defeats the purpose.

Stop and ask the user:
- Do you have a real or realistic artifact we can use as a test case?
- If not, should I create a hypothetical evaluation showing how the rubric would be applied?

Generate the evaluation record using the template structure from `references/examples.md`.

### Save and summarize

Save the rubric YAML file to the location the user specifies (suggest the `tmp/profiles/` or `tmp/overlays/` directory based on rubric type).

Summarize:
- Rubric ID, type, and version
- Number of dimensions and criteria added (and how they complement the 9 core dimensions)
- Gate criteria and their severity, with reasoning
- Any suggested overlays that were separated out during consolidation
- Any unresolved ambiguities or open questions
- Recommended next steps:
  - **Calibrate** with 3+ real artifacts (at least one strong, one weak, one ambiguous)
  - **Get a second reviewer** to score the same artifacts independently
  - **Measure agreement** and tighten criteria where reviewers disagree
  - **Pilot for 6-8 weeks** before treating the rubric as an enterprise standard

## Anti-patterns to watch for

Push back when you see these, and explain *why* they cause problems:

- **Criteria without evidence anchors** — "Is the architecture good?" is not evaluable. Without specifying what evidence proves quality, reviewers fall back on subjective judgment and scores become inconsistent.
- **Too many criteria** — More than 12 profile-specific criteria usually means the profile mixes artifact-type concerns with cross-cutting domain concerns. The rubric becomes expensive to apply, hard to calibrate, and prone to reviewer fatigue (where late criteria get less attention).
- **Vague scoring guidance** — If a reviewer can't distinguish score 2 from score 3, they'll default to 3 to avoid conflict. This inflates scores and hides real quality problems. The 2-vs-3 boundary is the most important thing to get right.
- **Hidden gates in averages** — If something is truly mandatory (like security control coverage), make it an explicit gate. Hidden in a weighted average, a score of 0 on a critical criterion can be masked by 4s elsewhere — producing a "pass" verdict on an artifact with a fatal flaw.
- **Org-chart criteria** — "Does the architecture follow our team structure?" is usually a smell. Conway's Law is real, but encoding organizational structure as architectural quality criteria produces rubrics that resist beneficial reorganization.
- **No failure modes described** — If the user can't name what goes wrong with these artifacts today, the rubric is being designed in a vacuum. Theory-driven rubrics miss what actually matters in practice.
- **Mixing profile and overlay** — Security, regulatory, and data concerns should be overlays, not baked into every profile. When these are duplicated across profiles, they drift apart and create inconsistent governance.

## Review checklist

Before presenting the final rubric, verify:

- [ ] Rubric type (profile vs overlay) is justified
- [ ] Profile design method (A-E) was selected and applied
- [ ] Core meta-rubric is inherited, not duplicated
- [ ] All criteria are artifact-specific (not generic)
- [ ] Each criterion has: question, evidence, scoring guide, anti-patterns, remediation
- [ ] Gates are limited to true review blockers with real-world justification
- [ ] Scoring guidance clearly distinguishes each level, especially 2 vs 3
- [ ] Profile adds no more than 5 dimensions / 12 criteria
- [ ] At least one escalation rule is defined
- [ ] User has reviewed and approved each dimension
- [ ] Cross-cutting concerns are separated into overlay suggestions
- [ ] Ambiguities are logged and presented
- [ ] YAML uses safe quoting (no bare strings with special characters in list items)

If any item fails, work with the user to resolve it before finalizing.
