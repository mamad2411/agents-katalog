---
name: vibe-coding-architecture-at-scale
description: "Knowledge base from \"Vibe Coding Architecture at Scale\" by Peter Isberg (2026). Use when applying Isberg's Vibe Architecture frameworks for keeping AI-generated code structurally sound — context diets and the agent configuration surface (CLAUDE.md, skills, subagents, hooks, memory), annotation-driven guardrails (VibeTags/@AILocked), ArchUnit architectural tests and test topology, spec-driven development, concurrency/schema/supply-chain/prompt-injection hazards, adversarial review (Inquisitor/Two-AI Gripe), CI enforcement, prompt lineage, model routing and Git save states — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter ID like 3d / 20b / App A] -->

# Vibe Coding Architecture at Scale
**Author**: Peter Isberg | **Pages**: ~570 | **Chapters**: 54 + 2 appendices | **Generated**: 2026-10-13

## How to Use This Skill
- **Without arguments** — use the core frameworks below
- **With a topic** — e.g. `hooks`, `ratchet`, `prompt injection`; I find and read the chapter via the Topic Index
- **With a chapter ID** — `ch03d`, `ch20b`, `app-a`; IDs follow the book (1, 1b, 2, 2b … 24b, 25, 26)
- For a topic not covered below, read the chapter file before answering. Decision rules and thresholds: [cheatsheet.md](cheatsheet.md).

---

## Core Frameworks & Mental Models

**Thesis — Vibe Architecture.** "Vibe coding gives you speed, but Vibe Architecture gives you scale. When syntax is free, structure is your only asset." One repeated pattern: **human intent in, automated machine enforcement out, zero tax on the flow**. Accept a guardrail only if it is written once, enforced by a machine inside the loop the AI already watches, and adds no friction (JPMS failed the last test). **"If a principle cannot fail a build, the agent will eventually violate it."**

**Why AI erodes architecture (Ch 1, 1b, 2).** The generator optimizes "make this prompt work by the shortest path": *Local Optimization*, *Shortest Path Bias*, *No Friction Awareness*. Expect the **Tipping Point** between the 10th and 50th file. The **Jevons Effect** means cheaper code raises demand; the backlog never drains. The **Enforcement Gap** (generation at thousands of lines/hour vs. fixed reading speed) plus **Beautifully Deceptive Code** (fluency ≠ correctness) make human review insufficient: every violation category AI makes more likely must be "not reviewed, not discussed, caught" by a machine at AI speed. Never slow the AI to manage risk.

**Shift Left, Guide Right (Ch 2).** *Shift Left*: the architectural decision exists as an enforceable artifact (ArchUnit rule, contract, annotation) **before** the prompt that could violate it. *Guide Right*: prompts specify **the box** (package, allowed dependencies, types) and **the invariant**, not syntax. Third time you type the same guidance → move it into source. Your role shifts from code monkey to **systems director**; the new failure is specifying the wrong box.

**Context discipline (Ch 3–3e).** **Context Diet**: Tier 1 root file = 10–20 project-wide invariants (one screen); **Tier 2** directory-scoped rules; **Tier 3** per-element annotations; fix bloat by *cut, scope, relocate*. **Prefix determinism**: static first, dynamic last (cache ≈ 10× cheaper). **Configuration Surface**: instruction (always-on, costly) vs. skill (on-demand, description is the trigger) vs. subagent (isolation, own allowlist) vs. **hook — the only slot that enforces**; install key rules at three depths: instruction + hook (exit 2) + CI test. **Memory** is the one primitive with no review gate: a *lead, not a citation*; age-stamp, verify before asserting, promote via human review. **Instruction evals** measure *binding power* (adherence with rule − baseline); rules stuck below floor get promoted to hooks/tests.

**Annotation-Driven Design (Ch 4, 4b).** Put intent on the element it protects (`@AILocked`, `@AIContract`, `@AIThreadSafe`, `@AIPrivacy`…); VibeTags generates per-tool config at compile time (`RetentionPolicy.SOURCE`, opt-in by file existence, managed block). Close the **Regeneration Gap**: check mode (regenerate + diff) as a required status check, one BOM version, `@AILocked` enforced by CI/hook — a check that cannot block a merge is documentation.

**Architectural Unit Testing (Ch 5, 5b, 5c).** Architecture as an executable **fitness function**: ArchUnit/Spring Modulith, package-private by default, package by feature. Loop: *Define → Violate → Trigger → Correct* (paste the failure back). Static analysis (Error Prone, NullAway, PMD, CPD) with **suppression discipline** and the **Ratchet Pattern** for legacy. Behavioral tests first; "do not modify the test." **Test topology**: inner loop < 30 s, full suite < 5 min, tag contract enforced by ArchUnit, isolate before parallelizing, ~65% meaningful coverage, patch coverage informational. AI-native patterns: spec/impl separation, interface-first, self-documenting exceptions, feature locality.

**Make the system legible (Ch 6, 6b, 6c).** Diagrams are a build output (Modulith Documenter, Mermaid/PlantUML as text) — telemetry, not enforcement. Logs are the agent's second feedback channel: log decisions, not positions; correlation IDs; DEBUG on in dev/CI/agent profile; ship the missing log line with the fix. Docs are now **input**: one file one job, claims a build can check, generated regions fenced.

**Spec-Driven Development (Ch 7–16).** Truth moves from the volatile context window to versioned **`.specs/`** (the repository as constitution): plan, then execute; requirements → design → tasks, each approved; Gherkin authored by humans; OpenAPI as hallucination suppressant; EARS. **Spec tools order work; tests enforce** — "a spec without tests is a wish with good grammar." Tools (Spec Kit, Kiro, Zenflow, GSD, Superpowers, Kanban, Skill Forge) are examples of shapes; judge successors on durable spec, human gates, context diet, honesty about not enforcing. **Risk asymmetry**: autonomy is a function of blast radius, not model capability (no AI crypto primitives; humans sign production migrations). At org scale: read-only org standards tier, cross-repo contract registry, platform vs. domain Inquisitor (stricter, never weaker). Measure **outcomes**: escaped defects, CI catches, review-hours, tokens per accepted change; anti-metrics are activity.

**Hard stuff (Ch 17–20d).** *Concurrency*: AI can't see happens-before; force collisions (≥ 20 threads, barrier), run on ARM. *Performance as a contract*: count queries/allocations in the inner loop, time only nightly. *Schema drift*: expand/migrate/contract, frozen OpenAPI + consumer contracts. *Supply chain*: slopsquatting; deny by default, frozen lockfiles, cooldown. *Load-bearing bugs*: "does correct data exist under the old behavior?" *Prompt injection*: every byte you didn't write is untrusted; you cannot prompt your way out — capability limits (sandbox) + authorization (policy) + human gates. *Attacker Agent* and *break-the-mechanism* audits keep tests honest ("a test that never failed is a smell").

**Enforcement at scale (Ch 21–24b).** **The pipeline is the real guardrail**: every guardrail is a required merge-blocking check; agents open PRs, never merge; the **enforcer set** is outside agent write scope; provenance (trailers → bot identity → SLSA); *dumb pipe, smart sandbox*. **Two-AI Gripe**: Generator vs. **Inquisitor** separated by objective, context (diff + committed rules only) and runtime (blocking CI); it blocks, never approves; must have a brake. **Prompt lineage**: version load-bearing intent with the diff; pin exact model IDs. **Model routing** by decision density with work orders + escalation. **Git as a save-state engine**: Zero Inter-Prompt Drift, Aggressive Discarding (`git reset --hard`), Squash-on-Completion.

---

## Chapter Index

| ID | Title | Key Frameworks |
|---|---|---|
| [1](chapters/ch01-entropy-of-the-prompt.md) | The Entropy of the Prompt | Vibe Architecture, Tipping Point, Shortest Path Bias |
| [1b](chapters/ch01b-jevons-effect.md) | The Jevons Effect | Jevons Effect, Enforcement Gap |
| [2](chapters/ch02-shift-left-guide-right.md) | Shift Left, Guide Right | Shift Left, Guide Right, Beautifully Deceptive Code |
| [2b](chapters/ch02b-canon-doesnt-compile.md) | The Canon Doesn't Compile | Fitness functions, connascence, entity trap |
| [3](chapters/ch03-context-diets.md) | Context Diets | Context Diet, Tier 1/2/3, prefix determinism |
| [3b](chapters/ch03b-context-graph.md) | From Context Diet to Context Graph | lat.md, Staleness Principle |
| [3c](chapters/ch03c-token-economy-runtime.md) | The Token Economy Runtime | Context Locality, compress vs pre-index |
| [3d](chapters/ch03d-configuration-surface.md) | The Configuration Surface | Four slots, kind × level, hooks enforce |
| [3e](chapters/ch03e-agent-memory.md) | Agent Memory: The Fifth Primitive | Promotion path, lead not citation |
| [3f](chapters/ch03f-instruction-evals.md) | Evals for the Instruction Layer | Binding power, promotion to hooks |
| [4](chapters/ch04-annotation-driven-design.md) | Annotation-Driven Design | VibeTags, @AILocked, @AIContract |
| [4b](chapters/ch04b-regeneration-gap.md) | The Regeneration Gap | Check mode, default-on |
| [5](chapters/ch05-architectural-unit-testing.md) | Architectural Unit Testing | ArchUnit, ratchet, suppression discipline |
| [5b](chapters/ch05b-test-topology.md) | The Test Topology | Feedback budget, two-speed tests |
| [5c](chapters/ch05c-ai-native-design-patterns.md) | AI-Native Design Patterns | Spec/impl split, self-documenting exception |
| [6](chapters/ch06-visualizing-the-vibe.md) | Visualizing the Vibe | Diagrams as build output |
| [6b](chapters/ch06b-log-feedback-loop.md) | The Log Is a Feedback Loop | Log-assertion tests, debug run profile |
| [6c](chapters/ch06c-docs-load-bearing.md) | The Docs Are Load-Bearing Now | DocsAreTrueTest, one source of truth |
| [7](chapters/ch07-spec-driven-development.md) | Spec-Driven Development | .specs/ constitution, EARS, plan-then-stop |
| [8](chapters/ch08-spec-kit.md) | Spec Kit in Practice | constitution→specify→plan→tasks→implement |
| [8b](chapters/ch08b-codekarta-case-study.md) | CodeKarta Case Study | Machine-readable SPEC.md, PLAN.md |
| [8c](chapters/ch08c-legacy-modernization.md) | AI-Assisted Legacy Modernization | Brownfield procedure, strangler fig |
| [9](chapters/ch09-kiro.md) | Kiro | Spec trinity, steering files |
| [10](chapters/ch10-zenflow.md) | Zenflow | Validate before generation, DAG spec |
| [11](chapters/ch11-get-shit-done.md) | Get-Shit-Done | Context allocation, STATE.md, tool rubric |
| [11b](chapters/ch11b-switch-off-the-ai.md) | When to Switch Off the AI | Risk asymmetry, no-AI list |
| [11c](chapters/ch11c-org-scale.md) | Vibe Architecture at Org Scale | Org standards tier, contract registry |
| [11d](chapters/ch11d-org-bottleneck.md) | The Org Bottleneck | PCE, autonomy budget |
| [11e](chapters/ch11e-measuring-vibe-architecture.md) | Measuring Vibe Architecture | Outcome metrics, anti-metrics |
| [12](chapters/ch12-superpowers.md) | Superpowers | Context firewalls, plans without placeholders |
| [13](chapters/ch13-prompt-template.md) | Vibe Coding Prompt Template | Progressive disclosure, saved artifacts |
| [14](chapters/ch14-vibe-coding-playbook.md) | Vibe Coding Playbook | XML prompting, approval gate |
| [15](chapters/ch15-vibe-kanban.md) | Vibe Kanban | Workspaces, review-as-prompt |
| [16](chapters/ch16-skill-forge.md) | Skill Forge | Evidence-cited skills, loop engineering |
| [17](chapters/ch17-asynchronous-trap.md) | The Asynchronous Trap | Forced collision, @AIThreadSafe |
| [17b](chapters/ch17b-performance-contract.md) | Performance as a Contract | Count ops inner loop, @ExpectSelect |
| [18](chapters/ch18-schema-drift-api-contracts.md) | Schema Drift & API Contracts | Expand/migrate/contract, frozen OpenAPI |
| [18b](chapters/ch18b-hallucinated-dependency.md) | The Hallucinated Dependency | Slopsquatting, deny by default |
| [18c](chapters/ch18c-fix-changes-the-data.md) | When the Fix Changes the Data | Data-at-rest test |
| [19](chapters/ch19-prompt-injection.md) | Prompt Injection | Untrusted input, capability vs authorization |
| [19b](chapters/ch19b-vibekit.md) | VibeKit | Contain/redact/record |
| [20](chapters/ch20-attacker-agent.md) | The Attacker Agent | Attack → red test → keep |
| [20b](chapters/ch20b-tests-lie.md) | When the Tests Lie | Green for the wrong reason |
| [20c](chapters/ch20c-simulation-harness.md) | The Simulation Harness | Healthy band, variance literacy |
| [20d](chapters/ch20d-correctness-hunt.md) | Anatomy of a Correctness Hunt | Bug-shape lenses, no red test no bug |
| [21](chapters/ch21-multi-agent-cicd.md) | Multi-Agent Orchestration & CI/CD | Pipeline as guardrail, enforcer set |
| [21b](chapters/ch21b-parallel-agent-workshop.md) | The Parallel-Agent Workshop | Worktree per writer, pipefail |
| [22](chapters/ch22-two-ai-gripe.md) | The Two-AI Gripe | Inquisitor, gripe loop |
| [23](chapters/ch23-prompt-lineage.md) | Prompt Lineage | Versioned intent, model pinning |
| [23b](chapters/ch23b-model-routing.md) | Model Routing | Decision density, work order |
| [24](chapters/ch24-git-save-state.md) | Git as a Save-State Engine | Three save-state rules |
| [24b](chapters/ch24b-anti-patterns.md) | Anti-Patterns | God Prompt, Human CI, Tool Chaser |
| [25](chapters/ch25-conclusion.md) | Conclusion | Five families, adoption roadmap |
| [26](chapters/ch26-epilogue.md) | Epilogue | Cross-repo mesh, self-healing as proposal |
| [App A](chapters/app-a-health-scorecard.md) | Health Scorecard | 33-item 0/1/2 audit |
| [App B](chapters/app-b-platform-coverage-matrix.md) | Platform Coverage Matrix | TS/Python/Go equivalents |

## Topic Index
- **Adoption roadmap / Day One** → 25, App A · **Agent memory** → 3e · **Anti-patterns** → 24b
- **ArchUnit / Spring Modulith** → 5, 5b, 8c · **Attacker Agent / fuzzing** → 20
- **Annotations / VibeTags / @AILocked** → 4, 4b, 21 · **CI/CD enforcement / provenance / SLSA** → 21
- **Concurrency / virtual threads** → 17 · **Context Diet / tiers / CLAUDE.md** → 3, 3d, 13
- **Context graph / lat.md** → 3b, 5c · **Coverage** → 5b, 11d · **Diagrams** → 6
- **Dependencies / supply chain** → 18b · **Docs as input** → 6c · **Evals for rules** → 3f
- **Fitness functions / connascence** → 2b, 5 · **Hooks / skills / subagents** → 3d, 12, 16
- **Inquisitor / adversarial review** → 22, 11c · **Legacy / brownfield** → 8c
- **Logging** → 6b · **Metrics** → 11e, 11d · **Model routing / pinning** → 23b, 23
- **Non-Java ecosystems** → 4, App B · **Org scale / governance** → 11c, 11d
- **Parallel agents / worktrees** → 21b, 15, 24 · **Performance / N+1** → 17b
- **Prompt injection / sandbox** → 19, 19b · **Prompting (box, XML, EARS)** → 2, 14, 7, 9
- **Ralph loop / loop engineering** → 16 · **Risk / when not to use AI** → 11b
- **Schema / API contracts / migrations** → 18, 18c, 26 · **Simulation / emergent behavior** → 20c
- **Spec-driven development** → 7, 8, 8b, 9, 10, 11 · **Test honesty** → 20b, 20d
- **Test topology / speed** → 5b · **Tokens / caching / cost** → 3, 3c · **Git save states** → 24

## Supporting Files
- [glossary.md](glossary.md) — key terms with chapter references
- [patterns.md](patterns.md) — techniques with when/how/trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, intent placement, thresholds, adoption order

## Scope & Limits
Covers the book's content only. Examples lean Java/Spring Boot (ArchUnit, VibeTags, async-test-lib); for TS/Python/Go equivalents see App B. Named third-party tools (Spec Kit, Kiro, Zenflow, GSD, Superpowers, Vibe Kanban, VibeKit, lean-ctx, lat.md) reflect the book's 2026 snapshot — verify current versions before relying on specifics.
