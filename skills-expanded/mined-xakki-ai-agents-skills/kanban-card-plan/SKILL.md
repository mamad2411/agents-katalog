---
name: kanban-card-plan
description: 'Groom a request or draft card into implementation-ready, measurable, dependency-safe cards and validate the grooming. Use when refining draft cards or planning cross-component work. RU: груминг, подготовить карточку, декомпозиция.'
---

# Kanban card planning

Use to turn a request or draft card into implementable work and to validate that planning change. Grooming never authorizes implementation or publication.

## Grooming

Use for turning a request or existing draft card into implementable work. Read the authoritative project contract, current card and board, existing decisions, dependencies, and applicable instructions before changing anything. Grooming alone does not authorize implementation or publication.

1. Reconcile requested work against a stage-aware inventory of active, completed and relevant ignored or untracked cards; follow legacy IDs to canonical successors. Separate genuine implementation from historical or organizational records and assign each candidate a disposition. Do not delete a discovery note or retire a duplicate until its unique scope and evidence have an authorized destination. Keep ownership boundaries, dependencies, exclusions, and controlled operations explicit.
2. Resolve facts through bounded discovery. Present material owner choices with their consequences and available alternatives; honor the user's requested question cadence and approval gates. Do not treat a timeout or empty answer as approval. Record the actual selection in the canonical decision record and reconcile affected active claims without erasing history. A partially answered choice remains open for its unresolved portion. Once a decision is recorded, continue the authorized queue unless the owner imposed a per-card stop.
3. Specify concrete scope, acceptance criteria, required inputs, verification method, dependencies, and stop conditions. Separate an unknown result that the task is meant to discover from a missing design decision needed to execute it. Trace source authority and consumer boundaries before asserting an existing behavior; distinguish static evidence from a live observation. Avoid inventing numeric requirements, project paths, runtimes, or agents.
4. Before promotion, reconcile unresolved questions, contradictory decisions, duplicate IDs, linked children, and any inherited safety or privacy requirements. A card is not implementation-ready while a required owner choice remains open.
5. Validate the exact changed records with available board checks and diff hygiene; require a nonzero checked-card count and report excluded stages, unrelated baseline failures and unrun checks separately. Independent review occurs at the authorized phase. Use only the requested lifecycle move and do not broaden Git or release scope.

For a decision that changes operational behavior or safety, use [decision recording](references/decision-recording.md), [queue and evidence](references/queue-and-evidence.md), and [security and operational boundaries](references/security-and-operational-boundaries.md) to check authority, the proposed mechanism, and acceptance boundaries before presenting options.

For an epic, interdependent cards, or an independent plan review, consult [dependency and scope planning](references/dependency-and-scope-planning.md). For measured performance, request-accounting, or experimental visual gates, consult [measurement contracts](references/measurement-contracts.md).

## Implementation-ready grooming of cross-component requests

Use to turn a cross-component request into cards that an implementer can execute without inventing unresolved product decisions. Respect the owner's planning and delegation mode; grooming does not itself authorize implementation.

1. Inspect the authoritative contract, generation path, affected producers and consumers, existing work, and current cards. Distinguish the requested delta from already-completed work; resolve source facts through bounded discovery before asking the owner. When code and product documentation give a field incompatible meanings, obtain the owner's decision on migration versus a separate field before deciding product semantics.
2. Split work by responsibility and real dependencies, not matching keywords. Specify the authority and meaning of each reused field, including producer, consumer, units, unavailable state, compatibility, and security boundaries where relevant.
3. Turn qualitative criteria into measurable observations with the applicable input, method, window, aggregation, cardinality, unavailable state, and pass conditions. For resource-efficiency claims specify the device/profile, observation window, budget and measurement source. Identify existing project verification commands, including shared cross-package harnesses, instead of inventing a runner or dependency.
4. Record dependency edges and completion gates on both parent and child records where the board supports them. Preserve exclusions, blocked predecessors, and integration criteria.
5. Present consequential choices and trade-offs, then record each accepted decision. An unanswered material choice remains unresolved unless the owner has explicitly delegated it; do not infer consent from a timeout.
6. Validate the actual changed cards and their source pins, including new or ignored files. Require a nonzero targeted checked-card count and run the relevant diff check. Distinguish targeted checks and unrelated whole-board failures. Review independently only when the task authorizes it; otherwise report the self-check. Stage or commit only within the authorized scope. When later independent review is explicitly deferred until implementation and its gates finish, preserve that order; do not mark unresolved choices as complete.

For each field, distinguish a reported claim from authoritative evidence; do not infer an unrelated target's network identity from the control connection. Specify sender, receiver, timing and feedback direction. Give round-trip measurements their correct meaning, and specify aggregation shape and percentile method rather than calling unbounded statistics bounded.

## Validating a grooming change

Use to validate a planning or grooming change without implying implementation acceptance.

1. Inspect the authorized board, relevant active and historical cards, decisions, and repository baseline if applicable. Check for exact, split, completed, and scope-overlapping duplicates before allocating an ID through the supported mechanism.
2. Check each card against the actual project template and owner decisions: scope, exclusions, dependencies, acceptance, verification, and unresolved questions must agree. Check reciprocal parent/child references and retain historical decisions without presenting them as current. A partial owner answer resolves only its approved portion; preserve remaining open decisions and gates. Verify named companion paths exist before editing them.
3. Use the project's canonical board validator on each changed card and verify the number of cards actually checked; use its supported exact path or basename rather than assuming short IDs resolve. Distinguish excluded stages, nonzero warnings, pre-existing board-wide failures, and checks not run. Inspect new or ignored files as well as tracked diffs. After an authorized move verify the actual destination and any maintained status field agree.
4. Report planning readiness separately from implementation, runtime, and production acceptance. Resolve only in-scope defects; do not create a commit, change unrelated cards, or widen the lifecycle scope without the applicable authorization.

Do not advance a grooming card with unresolved questions. If the user explicitly authorizes a bounded start while external evidence remains pending, record the authorized boundary and remaining closure gates without claiming external validation or expanding authority. If a helper staged an initial template or move before a substantive edit, inspect cached and working content separately and stage only the final owned body when staging is authorized.

See [card and decision validation](references/card-and-decision-validation.md), [targeted lint and staging](references/targeted-lint-and-staging.md), and [cross-card contract review](references/cross-card-contract-review.md).
