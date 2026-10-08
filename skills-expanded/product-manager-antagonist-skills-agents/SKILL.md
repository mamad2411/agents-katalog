# AGENTS.md

## Project Mission

This repository contains reusable `pant-` agent skills for pressure-testing product-management artifacts, decisions, proposals, and conversations.

The system helps product practitioners:

-   Find weak reasoning before consequential meetings
-   Surface assumptions and evidence gaps
-   Identify contradictions and hidden constraints
-   Test customer, strategic, commercial, technical, operational, and organizational logic
-   Prepare for likely stakeholder resistance
-   Rehearse difficult conversations
-   Improve artifacts before seeking approval, investment, sponsorship, commitment, or adoption
-   Learn how critical executives and other powerful stakeholders are likely to inspect the work
-   Practice managing up and influencing without authority before the real interaction carries consequences

The project must produce **structured dissent**.

It must not produce generic criticism, framework theater, executive cosplay, abusive role-play, or a larger quantity of objections mistaken for rigor.

The goal is not to build an antagonist that sounds impressive.

The goal is to help product practitioners make stronger decisions and enter consequential rooms considerably harder to knock over.

## Core Use Case

The core use case is preparation for first contact with a critical executive or other consequential stakeholder.

Less-experienced Product Managers and people entering product work from technical backgrounds may understand systems, delivery, and analysis while still being unfamiliar with managing up, organizational incentives, executive decision logic, and defending work under pressure. The system must help them strengthen both the substance of the work and their ability to navigate the room.

The practical source for this use case is `research/the-dangerous-animals-of-product-management.pdf`. Its recurring stakeholder and organizational patterns include executive opinion treated as proof, unsupported certainty, one-customer opportunities, optimistic schedules, metric theater, reactive firefighting, shallow assumptions, and feature-factory behavior.

Do not turn the Dangerous Animals into cartoon villains or a fixed persona taxonomy. They are memorable patterns that help users recognize pressure, incentives, and failure modes. Stakeholders are often well-intentioned and may hold information the Product Manager needs. The response should combine evidence, empathy, transparency, technical and product context, tiny acts of discovery, and influence without authority.

## Audience and Pedagogic Standard

The library serves Product Managers, Product Owners, Business Analysts, product operations practitioners, technical practitioners moving into product roles, and adjacent roles responsible for product decisions. It must remain useful across levels of competence.

Every scenario skill must support:

-   **Direct entry:** An experienced user supplies an artifact or compact context and receives useful feedback or enters rehearsal without an intake ceremony.
-   **Guided entry:** A user unfamiliar with the skill is walked through the minimum necessary setup, taught unfamiliar concepts in plain language, and shown why consequential challenges matter.
-   **Best-effort entry:** A user can begin with minimal context. The skill labels assumptions, lowers confidence where appropriate, produces useful work, and identifies what information could change the result.

These entry paths apply in both feedback and dialogue modes. The user may switch paths during a session.

Pedagogy and utility are equal product requirements. Skills should teach judgment, vocabulary, evidence expectations, stakeholder interpretation, and recovery—not only emit an answer. Teaching must remain proportional to the user's need: do not slow down experts, and do not treat newcomers like children.

Templates, worked examples, weak examples, short explanations, and helpful errors are part of the product when they materially reduce user effort or teach the decision logic.

## Governing Principle

Canvases, templates, frameworks, models, books, films, case studies, and research traditions are aids for guiding inquiry.

They are not scripts that dictate the conversation.

Use them to:

-   Open useful lines of inquiry
-   Reveal assumptions
-   Create shared language
-   Inspect relationships
-   Detect contradictions
-   Identify evidence expectations
-   Generate relevant questions

Do not use them to:

-   Replace judgment
-   Force a mandatory sequence
-   Turn the interaction into form completion
-   Override evidence emerging from the conversation
-   Treat every box as equally important
-   Treat the framework as exhaustive
-   Substitute authority for reasoning
-   Continue a weak line of inquiry after a stronger one appears

When the conversation exposes a more consequential weakness, leave the framework and pursue the weakness.

## Read Order

Before making changes, inspect only the material relevant to the task.

Begin with:

1.  `README.md`
2.  `ROADMAP.md` when the task affects scope, sequencing, status, packaging, or release readiness
3.  `docs/CURRENT-STATE.md` when resuming implementation work
4.  This `AGENTS.md`
5.  `shared/antagonist-contract.md`
6.  The relevant mode specification:
    -   `shared/feedback-mode.md`
    -   `shared/dialogue-mode.md`
7.  The affected scenario skill
8.  Relevant shared lenses
9.  Relevant framework adapters
10. Related eval cases
11. Relevant material in `research/`

Do not load the entire repository by default.

Do not read every research output before making a narrow change.

Use progressive disclosure:

```
project rules
    ↓
scenario rules
    ↓
relevant lenses
    ↓
relevant frameworks
    ↓
targeted research
    ↓
evals
```

## Instruction Precedence

When sources conflict, use this order:

1.  User’s explicit request
2.  Safety, privacy, and legal requirements
3.  `AGENTS.md`
4.  `shared/antagonist-contract.md`
5.  Mode specification
6.  Scenario skill
7.  Shared lenses and framework adapters
8.  Accepted eval behavior
9.  Synthesized research
10. Raw research

Research informs implementation.

Research does not silently override repository contracts.

If a research finding should change the architecture or antagonist contract, make that change explicitly and add appropriate evals.

## The `research/` Directory

The top-level `research/` directory contains the research prompt and results gathered from one or more external research platforms.

Expected material may include:

-   The original deep-research prompt
-   Raw platform responses
-   Source catalogs
-   Framework and author analyses
-   Pressure-test lens taxonomies
-   Question primitive libraries
-   Dialogue move libraries
-   Scenario mappings
-   Failure-mode catalogs
-   Recommended MVP designs
-   Source notes
-   Bibliographies
-   Contradictions and intellectual tensions
-   Research gaps
-   Synthesized development notes

Research may arrive as Markdown, text, tables, PDFs, or other supported formats.

The directory is a **working evidence library**.

It is not a folder of instructions to execute blindly.

### Research Handling Rules

When using research:

1.  Identify the specific design question being answered.
2.  Search or inspect only relevant research files.
3.  Prefer primary and authoritative sources identified by the research.
4.  Distinguish sourced findings from platform-generated synthesis.
5.  Check whether multiple research outputs agree.
6.  Preserve meaningful disagreements.
7.  Verify important claims against cited sources when practical.
8.  Translate findings into reusable operating components.
9.  Add provenance to framework, lens, or dialogue reference files.
10. Add evals demonstrating the intended behavior.

Do not:

-   Copy research output wholesale into a skill
-   Assume a long response is a reliable response
-   Treat all authors or frameworks as mutually compatible
-   Flatten disagreements into artificial consensus
-   Treat platform-generated citations as verified merely because they look like citations
-   Rewrite raw research files merely to make them look tidy
-   Delete contradictory findings
-   Promote an idea into the antagonist contract without evaluation
-   Allow the research corpus to become runtime prompt sludge

### Raw and Synthesized Research

Preserve raw outputs separately from repository synthesis.

Prefer:

```
research/
├── deep-research-prompt.md
├── raw/
├── synthesized/
├── sources/
└── gaps/
```

Raw research should remain traceable to its source platform and date when that information is available.

Synthesis should state:

-   What sources were reviewed
-   What conclusions were drawn
-   Where sources agreed
-   Where they conflicted
-   What remains uncertain
-   What repository components were created or changed

Do not alter raw output to make later conclusions appear better supported.

### Research Provenance

Framework adapters, lenses, and dialogue mechanics informed by research should include a short provenance section or references file.

Record:

-   Originating author, work, institution, or research tradition
-   Primary source when known
-   Secondary sources used
-   Relevant research file
-   Interpretation or adaptation made by this project
-   Limitations or disputes
-   Date reviewed when useful

Do not claim that a repository implementation reproduces an author’s complete method.

Use language such as:

-   Informed by
-   Adapted from
-   Derived from
-   Combines ideas from
-   Consistent with

### Research Gaps

When evidence is incomplete:

-   State the gap
-   Avoid false certainty
-   Record it under `research/gaps/` when it affects future work
-   Build the smallest responsible implementation
-   Add an eval around the uncertainty when appropriate

Do not block every implementation until academic certainty arrives.

Do not smuggle guesses into the design as settled fact.

## Architecture

The repository separates:

-   **Scenarios:** The artifact, decision, or meeting being prepared for
-   **Modes:** Feedback or dialogue
-   **Pressure levels:** Constructive, skeptical, resistant, or hostile room
-   **Lenses:** Decision perspectives used to challenge the work
-   **Framework adapters:** Structured sources of inquiry
-   **Question primitives:** Reusable question patterns
-   **Dialogue moves:** Reusable conversational behaviors
-   **Evidence tracking:** Claims, assumptions, estimates, contradictions, and concessions
-   **Output contracts:** Feedback structures, verdicts, and debriefs

The standard composition is:

```
scenario
+ mode
+ pressure level
+ selected lenses
+ relevant framework adapters
+ stakeholder context
```

Do not create a separate skill for every combination of stakeholder, artifact, industry, and tone.

Avoid:

```
angry-healthcare-CFO-roadmap-reviewer
friendly-fintech-CTO-roadmap-reviewer
skeptical-SaaS-CEO-roadmap-reviewer
```

A stakeholder title is not sufficient reason to create a new skill.

Prefer reusable components.

## Skill Structure

Each skill lives in:

```
skills/pant-<skill-name>/
```

Every skill must include:

```
SKILL.md
```

Optional supporting material may include:

```
references/
scripts/
template.md
examples/
```

Keep `SKILL.md` focused.

Move reusable material into `shared/`.

Move lengthy scenario-specific reference material into the skill’s `references/` directory.

Do not paste entire research reports into a skill.

### Skill Package Quality

A repeatable artifact should ship with `template.md`.

Every active scenario skill should ship with at least one synthetic worked example. Add a weak or failed example when comparison materially teaches evidence quality, stakeholder interpretation, rehearsal behavior, or a common failure mode. Use examples from more than one business context when that helps prove the skill is not accidentally limited to one domain.

Examples must demonstrate the antagonist contract, not merely fill in a template. Show what survives scrutiny, what fails, why it matters, what the user can do next, and how the antagonist changes position when stronger evidence warrants it.

## Required Frontmatter

Canonical `SKILL.md` files use the rich metadata contract in [`docs/SKILL-SPEC.md`](docs/SKILL-SPEC.md). It includes trigger, category, status, modes, entry paths, pressure levels, audience, evidence, outputs, dependency, composition, provenance, timing, and license metadata.

Platform packages may reduce canonical metadata to the fields supported by that runtime. Do not weaken canonical metadata to satisfy the smallest platform schema.

Every installable skill name and folder must begin with `pant-`. Use the same identifier in folder names, frontmatter, catalog entries, package names, examples, and documented invocations. Shared internal components do not need the prefix unless they are independently installable.

The description must identify:

-   Triggering situation
-   Artifact, meeting, or decision handled
-   Supported modes
-   Important exclusions when ambiguity is likely

Avoid:

```
description: Helps Product Managers think better.
```

Prefer:

```
description: Pressure-test product roadmaps and rehearse roadmap review meetings. Use when a Product Manager needs criticism of strategic coherence, evidence, sequencing, tradeoffs, dependencies, adoption, or outcome orientation. Do not use for detailed sprint or backlog reviews.
```

## Mandatory Scenario Skill Contract

Every scenario skill must define:

1.  Purpose
2.  When to use
3.  When not to use
4.  Supported modes
5.  Decision being prepared for
6.  Typical audiences
7.  Default lenses
8.  Optional lenses
9.  Relevant framework adapters
10. Required context
11. Minimum viable context
12. Review workflow
13. Dialogue protocol
14. Output format
15. Failure modes
16. Evaluation requirements
17. Research provenance where relevant
18. Direct, guided, and best-effort entry behavior
19. Pedagogic support and supporting templates or examples

Do not hand-maintain the shared antagonist contract inside every skill. Synchronize generated copies into `references/runtime/`, reference those local copies, and add scenario-specific instructions. This preserves one authoring source while keeping every skill independently installable.

## Antagonist Contract

All antagonists must:

-   Challenge the work rather than attack the person.
-   Ground findings in supplied material and available evidence.
-   Distinguish facts, reports, interpretations, estimates, assumptions, hypotheses, commitments, forecasts, aspirations, and unknowns.
-   Explain why each significant problem matters.
-   Separate blocking flaws from lesser concerns.
-   Identify what survives scrutiny.
-   Prefer probable and consequential objections over theoretical edge cases.
-   Surface missing context without refusing to begin useful work.
-   Remain capable of being persuaded.
-   Change position when stronger evidence warrants it.
-   Avoid false certainty.
-   Avoid praise sandwiches.
-   Avoid generic encouragement that dilutes the critique.
-   Avoid manufacturing objections merely to appear rigorous.
-   Avoid treating authority as evidence.
-   Avoid treating customer requests as automatic product strategy.
-   Avoid confusing activities, outputs, and outcomes.
-   Avoid continuing a framework after it stops producing useful insight.

Criticism should be proportional to:

```
consequence × likelihood × uncertainty × reversibility
```

Not every uncertainty is a blocker.

Not every flaw deserves equal attention.

Not every number becomes evidence because somebody put a percentage sign after it.

## Lens Rules

Lens definitions live under:

```
shared/lenses/
```

A lens should define:

-   Decision logic
-   Questions it provokes
-   Evidence it expects
-   Common failure patterns
-   Blind spots
-   Tensions with other lenses
-   Conditions under which another lens should take priority
-   Applicable scenarios
-   Relevant framework adapters
-   Research provenance

Do not encode tone or personality into a lens.

For example:

-   `commercial.md` defines economic scrutiny.
-   It does not require the antagonist to be aggressive.
-   Aggression and resistance are controlled by pressure level and scenario.
-   Stakeholder incentives are supplied separately.

Every lens must acknowledge its own limits.

A commercial lens does not automatically override customer, strategic, ethical, operational, legal, or technical considerations.

## Framework Adapter Rules

Framework adapters live under:

```
shared/frameworks/
```

Every adapter should follow the shared adapter schema.

It should define:

1.  Name
2.  Origin and attribution
3.  Purpose
4.  Decisions supported
5.  Core concepts or elements
6.  Relationships among elements
7.  Contradictions to inspect
8.  Evidence expectations
9.  Question primitives
10. Common misuses
11. Blind spots
12. Escape conditions
13. Compatible lenses
14. Relevant scenarios
15. Dialogue applications
16. Research provenance

### Framework Use

Use a framework adapter when it helps expose a meaningful decision risk.

Do not automatically activate every compatible framework.

Select the smallest useful set.

A framework adapter should provoke questions such as:

-   Which elements contradict each other?
-   What evidence supports this claim?
-   What assumption connects these two boxes?
-   Which stakeholder has been blurred together with another?
-   What must happen operationally for the economic story to work?
-   What would change the decision?
-   Which part is fact, inference, estimate, or aspiration?
-   What is missing because the framework does not cover it?

### Framework Escape Conditions

Stop or change frameworks when:

-   Another weakness becomes more consequential.
-   The user has persuasively addressed the current line of inquiry.
-   The framework encourages repetition.
-   The artifact lacks the information needed for meaningful use.
-   Another lens better fits the decision.
-   The conversation has moved outside the framework’s useful scope.
-   Continuing would become form completion.

Do not complete a framework for its own sake.

## Question Primitive Rules

Question primitives live under:

```
shared/questions/
```

Each primitive should define:

-   Trigger
-   Intended effect
-   Appropriate scenarios
-   Evidence expected
-   Example formulation
-   Follow-up logic
-   Stop condition
-   Misuse risk
-   Relevant research sources

Do not create a giant undifferentiated question bank.

Questions should be selected because they serve the conversation.

The antagonist should not hurl every available question at an unsuspecting Product Manager merely because the repository contains them.

## Evidence Model

Important claims should be classified as:

-   Observed fact
-   Reported statement
-   Interpretation
-   Estimate
-   Assumption
-   Hypothesis
-   Commitment
-   Forecast
-   Aspiration
-   Unknown

Assess evidence for:

-   Strength
-   Relevance
-   Freshness
-   Independence
-   Sample limitations
-   Selection bias
-   Survivorship bias
-   Confounding
-   Base rates
-   False precision
-   Sensitivity
-   Contradiction
-   Missing disconfirming evidence

Qualitative evidence is not automatically weak.

Quantitative evidence is not automatically strong.

A market estimate with six decimal places can still be numerology in a necktie.

The relevant question is whether the evidence supports the claim strongly enough for the decision being made.

## Feedback Mode

Feedback mode must produce a structured review.

When the user supplies an artifact or compact context, begin the review directly and treat supplied material as answered context. When the user requests guidance or arrives with only a rough situation, explain the review target in plain language and gather only information that could materially change the findings. Do not require a newcomer to know framework terminology before receiving value.

Unless a scenario specifies otherwise, include:

1.  Bottom line
2.  What survives scrutiny
3.  Blocking flaws
4.  Significant challenges
5.  Assumptions and evidence gaps
6.  Contradictions and tensions
7.  Likely stakeholder objections
8.  Difficult questions
9.  Recommended revisions or discovery actions
10. Readiness verdict

Each blocking flaw should include:

-   Finding
-   Why it matters
-   Evidence
-   Confidence
-   Recommended response

Do not merely rewrite the artifact.

Do not hide criticism inside a polished replacement.

The Product Manager should be able to see:

-   What is wrong
-   Why it matters
-   How serious it is
-   What evidence supports the judgment
-   What could improve it

## Dialogue Mode

Dialogue mode simulates a meeting or conversation.

An experienced user may provide only the stakeholder, decision, stakes, and artifact before entering the scene. A guided user may need help identifying the decision being requested, the stakeholder's authority and likely incentives, the evidence available, and the room's pressure level. Keep setup proportional; do not turn rehearsal into a questionnaire.

The antagonist must:

1.  Understand the stakeholder’s role, incentives, authority, knowledge, and concerns.
2.  Understand the decision or commitment being requested.
3.  Ask one meaningful question at a time.
4.  Respond to the user’s actual answer.
5.  Track claims, evidence, assumptions, contradictions, and concessions.
6.  Pursue evasions and unsupported certainty.
7.  Acknowledge persuasive answers.
8.  Update its position when warranted.
9.  Remain in character until the user pauses, requests coaching, switches roles, or ends the scene.
10. Avoid revealing the entire objection tree.
11. Avoid coaching while in character.
12. Avoid becoming abusive, theatrical, irrational, or impossible to satisfy.

Recognize:

-   `Pause`
-   `Debrief`
-   `Harder`
-   `Easier`
-   `Reset`
-   `Switch lens`
-   `Switch stakeholder`
-   `Coach me`
-   `Resume`
-   `End scene`

### Coaching Interrupt

When the user requests coaching:

-   Clearly leave the simulated role.
-   Identify the weakness in the answer.
-   Explain what the stakeholder likely heard.
-   Help improve the answer.
-   Do not continue the simulation until the user says `Resume`.

### Debrief

A debrief should include:

-   What worked
-   What did not
-   Unsupported claims
-   Contradictions
-   Missed opportunities
-   Stakeholder interpretation
-   Remaining risks
-   Recommended preparation
-   Improved answers to the most consequential questions

## Pressure Levels

Use:

-   `constructive`
-   `skeptical`
-   `resistant`
-   `hostile-room`

Pressure level affects:

-   Burden of proof
-   Patience with ambiguity
-   Frequency of interruption
-   Willingness to accept assumptions
-   Resistance to the requested decision
-   Follow-up intensity

Pressure level does not permit:

-   Personal abuse
-   Invented evidence
-   Impossible standards
-   Irrational objections
-   Refusal to update
-   Cartoon executive behavior

A hostile room may be difficult.

It must still be coherent.

## Router Rules

The `pant-antagonist-router` should select the smallest useful combination of:

-   Scenario
-   Mode
-   Pressure level
-   Lenses
-   Framework adapters
-   Stakeholder context

Infer these when the request provides enough information.

Ask a clarifying question only when the answer would materially change the pressure test.

Do not force the user through an intake ceremony before producing value.

When context is incomplete:

1.  State important assumptions.
2.  Begin useful work.
3.  Surface missing context as part of the review or rehearsal.

Prefer a specialized scenario skill over the general skills when specialization materially improves the work.

Use `pant-artifact-pressure-test` or `pant-meeting-rehearsal` when no specialized scenario is necessary.

## Readiness Verdicts

Use only:

-   `Ready`
-   `Ready with caveats`
-   `Needs another evidence pass`
-   `Needs material revision`
-   `Not ready for this decision`

A verdict must refer to:

-   Audience
-   Decision
-   Context
-   Consequence
-   Available evidence

Do not describe an artifact as universally good, bad, or ready.

## Writing Style

Use clear, direct language.

Prefer:

-   Specific findings
-   Concrete questions
-   Evidence references
-   Explicit consequences
-   Prioritized revisions
-   Visible uncertainty
-   Short explanations attached to consequential findings

Avoid:

-   Consultant fog
-   Generic leadership language
-   Artificially dramatic objections
-   Overlong introductions
-   Repeating the artifact back to the user
-   Empty phrases such as “consider diving deeper”
-   Excessive headings
-   Excessive bullet nesting
-   Fake stakeholder quotations
-   Certainty unsupported by evidence
-   Framework name-dropping
-   Author imitation

Do not automatically sanitize the user’s language.

Preserve domain terminology and intentional tone unless clarity, privacy, or safety requires otherwise.

## Attribution and Intellectual Property

Do not:

-   Reproduce copyrighted canvases, books, or proprietary training materials in full
-   Copy extensive question lists
-   Claim endorsement
-   Impersonate living authors
-   Generate “the Marty Cagan response”
-   Manufacture quotations
-   Present an adaptation as an official implementation
-   Assume a diagram found in research is freely reusable

Do:

-   Attribute ideas accurately
-   Paraphrase principles
-   Cite sources in reference files
-   Record adaptations made by this project
-   Identify licensing or trademark concerns
-   Separate public concepts from proprietary implementation details

Films and narrative works may inform scenario dynamics.

They are not evidence for management effectiveness.

Do not reproduce copyrighted dialogue or scenes.

## Technical Defaults

The skill library is Markdown-first.

Python supports:

-   Structural validation
-   Link validation
-   Research-reference validation
-   Packaging
-   Evaluation
-   Test fixtures

Use:

-   Python 3.12 or later
-   `uv` for environments and dependencies
-   `pytest` for tests
-   UTF-8
-   YAML for structured eval cases

Do not introduce a:

-   Web application
-   Database
-   Service layer
-   Vector store
-   Agent framework
-   External model dependency
-   Telemetry system

unless the current issue explicitly requires one.

The skill specifications are the primary product.

Infrastructure exists to improve quality, portability, traceability, and evaluation.

## Commands

Install dependencies:

```
uv sync
```

Validate skill structure:

```
uv run python scripts/validate_skills.py
```

Validate internal links:

```
uv run python scripts/validate_links.py
```

Validate research references:

```
uv run python scripts/validate_research_references.py
```

Validate neighboring skill trigger boundaries:

```
uv run python scripts/validate_trigger_boundaries.py
```

Validate generated runtime copies and standalone portability:

```
uv run python scripts/sync_skill_runtime.py --check
uv run python scripts/validate_skill_portability.py
```

Build individual skill folders and ZIP files:

```
uv run python scripts/build_individual_skills.py
```

Run tests:

```
uv run pytest
```

Validate eval definitions or run configured behavioral evals:

```
uv run python scripts/run_evals.py
```

Run all required checks before completing a change:

```
uv run python scripts/validate_skills.py
uv run python scripts/validate_links.py
uv run python scripts/validate_research_references.py
uv run python scripts/validate_trigger_boundaries.py
uv run python scripts/sync_skill_runtime.py --check
uv run python scripts/validate_skill_portability.py
uv run pytest
uv run python scripts/run_evals.py
uv run python scripts/build_individual_skills.py
```

For the public-preview release gate, use the orchestrated commands:

```
uv run python scripts/test_library.py
uv run python scripts/build_release.py
```

`build_release.py` reruns the canonical gate, builds deterministic canonical, starter-pack, and individual archives, verifies safe members and checksums, and reruns the gate from a clean canonical extraction. Do not edit `dist/` directly.

When a command cannot be run, report:

-   Which command was not run
-   Why it was not run
-   What remains unverified

Do not claim validation that did not occur.

Until a scenario skill and model runner exist, `scripts/run_evals.py` validates eval definitions and explicitly reports that no model executions were performed.

## Adding a Scenario Skill

Before adding a skill:

1.  Confirm that an existing scenario cannot handle the use case.
2.  Confirm that the need cannot be addressed by adding a lens, framework adapter, question primitive, or dialogue move.
3.  Define the decision being pressure-tested.
4.  Define the unique failure modes exposed.
5.  Identify the likely audience and stakeholder incentives.
6.  Define feedback and dialogue behavior.
7.  Identify relevant research.
8.  Add positive, negative, and edge-case evals.
9.  Validate triggering against neighboring skills.
10. Synchronize runtime contracts and validate the skill outside the repository.
11. Build and inspect the individual package.
12. Update `README.md`.

Every new skill must include eval cases for:

-   Correct invocation
-   Incorrect invocation
-   Minimal context
-   Rich context
-   Feedback mode
-   Dialogue mode when supported
-   Pressure-level behavior
-   Grounding
-   Framework escape behavior
-   Ability to be persuaded
-   Non-abusive challenge
-   Appropriate readiness verdict

## Adding or Updating a Framework Adapter

Before adding an adapter:

1.  Confirm that it contributes a distinct decision capability.
2.  Locate the relevant research.
3.  Identify primary sources when possible.
4.  Describe its purpose and limits.
5.  Define relationships and contradictions, not only component names.
6.  Define evidence expectations.
7.  Define common cargo-cult misuse.
8.  Define escape conditions.
9.  Connect it to lenses and scenarios.
10. Add evals showing useful and inappropriate use.

When changing a shared adapter:

-   Identify every skill that uses it.
-   Run associated evals.
-   Check for duplicated or conflicting instructions.
-   Verify that it remains a guide to inquiry.
-   Verify that it has not become a rigid workflow.
-   Update research provenance.

## Adding or Updating a Lens

When changing a shared lens:

1.  Identify every skill that uses it.
2.  Inspect relevant research.
3.  Run associated evals.
4.  Check whether the change creates duplicated or conflicting instructions.
5.  Verify that the lens remains a decision perspective rather than becoming a stakeholder caricature.
6.  Update its blind spots.
7.  Update its framework mappings.
8.  Update provenance.

Shared-lens changes require broader regression testing than changes to one scenario skill.

## Evaluation Standards

Behavioral evals should measure:

-   Trigger precision
-   Trigger recall
-   Artifact grounding
-   Challenge relevance
-   Consequence awareness
-   Prioritization
-   Evidence discipline
-   Lens fidelity
-   Framework selection
-   Framework escape behavior
-   Scenario fidelity
-   Dialogue realism
-   Follow-up quality
-   Role consistency
-   Contradiction tracking
-   Ability to update beliefs
-   Debrief usefulness
-   Absence of fabricated facts
-   Absence of personal abuse
-   Absence of generic criticism
-   Appropriate use of research-informed concepts

Do not evaluate a skill only by checking whether certain phrases appear.

Prefer rubric-based evals that assess whether the behavior exposes a meaningful weakness or improves readiness for a decision.

## Eval Fixtures

Fixtures should include deliberately imperfect product-management work such as:

-   Output-heavy roadmaps
-   Strategies without choices
-   Business cases with magical revenue
-   TAM/SAM/SOM estimates built from unrelated percentages
-   Discovery claims based on weak samples
-   Executive requests without an explicit ask
-   Customer advisory decks that invite feature hostage negotiations
-   Tactical plans that confuse activity with progress
-   Root-cause analyses that blame individual error
-   Presentations with claims stronger than their evidence
-   Proposals that ignore adoption, enablement, and operations
-   Business models that blur buyer, user, and beneficiary
-   Experiments that cannot change the decision
-   Pricing proposals without willingness-to-pay evidence

Include strong artifacts.

An antagonist that always finds catastrophic flaws is not rigorous.

It is broken.

## Testing Dialogue

Dialogue evals must verify that the antagonist:

-   Asks one question at a time
-   Uses the previous answer
-   Tracks claims and contradictions
-   Does not reveal its entire objection tree
-   Does not coach while in character
-   Responds correctly to controls
-   Becomes more persuaded when given strong evidence
-   Remains skeptical when answers are evasive
-   Leaves a framework when another issue becomes more important
-   Produces an evidence-based debrief
-   Does not become personally abusive at higher pressure levels

## Security and Privacy

Do not commit real confidential:

-   Customer information
-   Employee information
-   Financial data
-   Incident data
-   Product plans
-   Credentials
-   Internal URLs
-   Proprietary numbers
-   Unreleased product information

Use synthetic fixtures.

When adding research outputs, inspect them for:

-   Personal information
-   Embedded credentials
-   Private URLs
-   Proprietary source documents
-   Material that should not be committed
-   Copyright-sensitive reproductions

Do not add telemetry or external model calls without explicit approval.

## Change Discipline

Keep changes focused.

Do not:

-   Rewrite unrelated skills
-   Reformat the entire repository
-   Add speculative abstractions
-   Introduce dependencies without need
-   Change shared behavior without regression evals
-   Add skills solely to increase catalog size
-   Create every proposed directory before it is needed
-   Treat repository neatness as user value
-   Claim that a scenario was tested when only structural validation ran
-   Promote raw research directly into runtime instructions

When requirements conflict, prioritize:

1.  Safety, privacy, and legal constraints
2.  User intent
3.  Antagonist contract
4.  Scenario correctness
5.  Evidence grounding
6.  Evaluation quality
7.  Consistency
8.  Convenience

## Distribution and Release Lifecycle

Canonical skills live under `skills/`. Platform plugins, individual ZIP files, starter packs, themed packs, catalogs, and other release artifacts must be built from or validated against that canonical tree. Do not maintain a second hand-edited copy of a skill for another platform.

Every canonical skill folder must also be independently portable. Required runtime behavior travels under `references/runtime/`; links may not escape the skill directory. `depends_on` declares hard dependencies included by packaging, while `combine_with` names optional companions that are never required.

The repository begins private and becomes public only after the core experience has been vetted. Public-release readiness requires:

-   Structural, link, research-reference, and package validation
-   Behavioral evals for direct, guided, and best-effort entry
-   Feedback and dialogue coverage at relevant pressure levels
-   Strong-artifact fixtures that test false-positive control
-   Synthetic-data and confidentiality review
-   Source, attribution, trademark, and licensing review
-   Representative clean-install tests for each supported distribution path
-   Human cold-start sessions with both experienced and less-experienced product practitioners
-   Public-facing documentation that clearly states what has and has not been validated

Private practitioner feedback may change the antagonist contract, pedagogy, catalog, or packaging. Make those changes explicitly, preserve the evidence for the decision, and update `ROADMAP.md`.

Do not publish, tag, release, or change repository visibility unless the user explicitly requests it.

## Definition of Done

A change is complete when:

-   The requested behavior is implemented.
-   Relevant research was inspected when needed.
-   Research-derived behavior has provenance.
-   Skill frontmatter validates.
-   Generated runtime references match the canonical shared sources.
-   The individual skill passes standalone portability and package inspection.
-   Relevant tests pass.
-   Relevant behavioral evals pass.
-   Neighboring triggers were checked.
-   Framework escape behavior was considered.
-   Documentation is current.
-   No confidential data was introduced.
-   Remaining limitations and research gaps are reported plainly.

The purpose of this repository is not to help an agent sound smarter than the Product Manager.

It is to help the Product Manager discover weaknesses, gather better evidence, make stronger choices, rehearse consequential conversations, and improve the odds that the real room discusses the decision rather than dismantling the preparation.
