# AGENTS.md

# Core Engineering Principles

These principles are the highest-priority default for all project work. When they appear to conflict, prefer the earlier principle and the current target architecture.

- Start from first principles: derive conclusions from the actual code, product constraints, and basic facts. Stay skeptical, inspect the system, and research viable designs before applying industry conventions.
- Complete authorized work end to end: execute every planned and feasible step before handoff. A progress update never replaces continued execution; pause only for a genuine blocker that needs user action or a material discovery that invalidates the plan, then report it and replan. Otherwise continue through implementation, verification, and documentation, and hand off only when the task is complete.
- Delete obsolete paths. Ship only current code.
- Use the simplest code that meets current needs.
- Build in layers: ship the smallest working slice of the target architecture first, then extend a working product.
- Keep modules separate and responsibilities clear.
- Prefer mature libraries that simplify or stabilize the system.
- Check existing dependencies, documentation, and types before adding or changing code.
- Design for the long term.
- Study proven products and adopt their patterns where they fit Minos.

# Project Context and Navigation

Minos 是远程 AI 编码控制系统：用户通过 Mobile、Desktop 或 Web 协作界面操作，Hub 负责身份、协作消息与实时同步，Mac Host daemon 在用户机器上执行 codex、claude、gemini、opencode 等 CLI agent。协作消息的权威在 Hub；Host 是 agent runtime，不是第二个协作消息权威。

Read documentation selectively, starting from the change rather than mechanically reading an index:

- Start with [architecture-overview.md](docs/architecture-overview.md) for system boundaries and repository layout.
- Read the matching `docs/architecture-<surface>.md` for the subsystem being changed; read [architecture-messaging.md](docs/architecture-messaging.md) for any cross-end messaging, realtime, bot, or sync work.
- Read the applicable [ADR](docs/adr/) before changing a durable architectural decision, [ci-gates.md](docs/ci-gates.md) before verification, and `docs/ops/` only for operational work.
- Use `rg` to find a current contract or specification. A design spec is not automatically authoritative: prefer current architecture docs, accepted ADRs, types, code, and nearest tests; resolve disagreement at the ownership boundary.

# Current-State and Target-Architecture Policy

Minos is under active development and has no historical release that requires support. Code, schemas, protocols, data, generated bindings, tests, and documentation target the latest architecture only.

- Do not add compatibility layers, dual reads or writes, legacy migrations, old-shape feature flags, or adapters unless the user explicitly requires compatibility.
- Prefer a clean breaking change. Change the canonical schema, contract, and tests together; do not preserve obsolete rows, payloads, fixtures, or branches.
- Every plan and implementation describes the completed target architecture: module boundaries, data model, lifecycle or state machine, removal list, and acceptance invariants.
- A phased delivery is valid only when each phase is a releasable slice of that target architecture. It must compile, be verifiable, and leave no temporary behavior or migration debt behind.
- Fix shared-contract, lifecycle, and SSOT defects at their ownership boundary. Do not hide them with UI guards, retries, silent defaults, soft deduplication, placeholders, or other local workarounds.

# Code Language, Naming, and Comments

Code describes the current domain, not the history of how it was implemented.

- Comments explain non-obvious current invariants, ownership, concurrency, protocol boundaries, or reasoning; never narrate a plan, ticket, phase, review, tool, prompt, or ADR. Remove comments that merely restate code or became stale. A runtime state-machine may use its own locally defined terms.
- Name files, modules, types, APIs, and variables for their current responsibility. Do not preserve temporal, migration, compatibility, or tool-specific vocabulary as a domain name; rename active paths or delete obsolete ones.
- Use the [architecture glossary](docs/architecture-overview.md#glossary) for shared system terms. Add or revise a term there when it needs a stable definition; do not create a private synonym or encode a terminology decision in a source comment.
- Apply terminology changes cohesively across declarations, call sites, tests, generated bindings, and documentation. Do not keep aliases merely to preserve an old name.

# Documentation Lifecycle

Documentation is a maintained product surface, not a record of agent activity. Keep only material that helps a future engineer safely operate, understand, or change the current system. Git and the PR retain historical working notes.

## Document classes

- **Long-lived reference:** `README.md`, `docs/architecture-*.md`, accepted `docs/adr/`, and `docs/ops/`. These describe the current system, a durable decision, or a runnable operation. Update or delete affected content in the same change as the code.
- **Current design specification:** a narrowly scoped target contract that is still needed to guide work across multiple changes or ownership boundaries. It has one canonical owner/topic, states its status, and must be folded into the long-lived reference or deleted when its work is complete or superseded.
- **Temporary work artifact:** implementation plans, investigation notes, review reports, checklists, and PR-specific task tracking. Keep these in the issue/PR by default, not in the repository. If collaboration requires a committed temporary file, label it `Temporary`, state its removal condition, and delete it before the PR is opened or merged.

## Rules

- Do not create a document merely to narrate work, restate code, preserve a chat transcript, or prove that a task was completed. Do not add dated plans, reviews, or task logs as permanent repository content.
- Before adding a document, search for an existing canonical document and extend it when the subject is the same. One fact has one source of truth; replace duplicate text with a link or delete it.
- A new long-lived document needs a durable audience and maintenance reason. New ADRs are for consequential, long-lived decisions, not routine implementation choices.
- When a feature, migration, or refactor completes, promote only its lasting contract, operational procedure, or decision into the relevant architecture document, runbook, or ADR. Delete its temporary plan, review, task list, stale examples, and superseded specification in the same change.
- When changing an existing document, remove invalid sections and links rather than appending another historical layer. Mark an ADR as superseded only when its decision has actually been replaced; ADRs remain the concise historical decision record.
- Before handoff, account for every documentation file added or touched: why it remains useful after the PR, what canonical document it updates, and which temporary artifacts were removed. If that cannot be stated plainly, do not keep the file.

# Agent Workflow

## Before changing code

- Read the relevant types, dependencies, architecture documentation, existing implementations, and nearest tests before designing a change.
- For non-trivial work (three or more steps, cross-module changes, or architectural decisions), create a plan that includes its verification and deletion work. If evidence invalidates the plan, stop and revise it.
- Use established product patterns when they suit Minos, but adopt them through the existing architecture rather than copying unnecessary complexity.
- Choose mature dependencies only when they materially simplify or stabilize the system; check existing dependencies first.

## Implementing changes

- Keep responsibilities and ownership boundaries explicit. Prefer direct code and the smallest correct change over a small diff that leaves a broken invariant.
- Remove code, tests, fixtures, documentation, polling, fallbacks, or decision branches made obsolete by the change in the same change set.
- For a bug report, trace the full affected path: caller and callee, contracts, persistence, runtime lifecycle, UI projection, and existing evidence. Fix the root cause autonomously and add a focused regression test for the corrected invariant.
- Use parallel agents for independent research or isolated phases when that reduces total work without splitting ownership. Give each agent a bounded outcome and integrate its result against the same target architecture.
- Reconsider non-trivial designs before implementation. If a solution feels like a workaround, identify the correct layer and implement the clean design instead.

## Documentation and observability

- Treat code as the source of truth. After a material implementation change, update every affected document, example, command, path, configuration, and behavior description; remove stale or duplicate documentation.
- State when the relevant documentation was checked and already accurate.
- Comment only non-obvious control flow, protocol boundaries, data-shape conversion, and concurrency decisions.
- Add structured logs at lifecycle and failure boundaries. Include stable identifiers (for example `project_id`, `session_id`, workspace path, method, and error) without logging secrets or sensitive payloads.

## Verification and completion

- Use the project [minos-quality-gate](.agents/skills/minos-quality-gate/SKILL.md) skill as the mandatory final phase of every code, test, schema, codegen, dependency, configuration, documentation, comment, rename, or deletion change. Before any commit, push, PR update, or handoff, classify the complete changed surface, run every selected CI-equivalent local gate, repair failures, and re-run to green. CI confirms this evidence; it must not be the first place an agent discovers formatting, lint, codegen, contract, file-size, or test failures.
- Do not declare work complete without evidence. Compare behavior with the base branch when relevant, run the applicable quality gates, inspect meaningful logs or errors, and report the exact commands and results. Explicitly mark only path-based non-applicable gates; a missing toolchain/platform or an unrun required gate is a blocker, not a passing result.
- Review completed work adversarially: trace the broader call chain, state, lifecycle, and failure modes for unexpected behavior. Find the root cause rather than only the reported symptom, then proactively inspect and correct analogous paths to preserve whole-codebase correctness.
- Unit tests cover isolated business rules, state changes, parsing, validation, serialization, and error handling. Mock external systems; do not label UI, network, database, filesystem, device, or end-to-end flows as unit tests.
- Keep integration and UI coverage separate, and run the relevant test command before handoff.
- Treat CI failures in the changed area as work to resolve, not as optional follow-up.
