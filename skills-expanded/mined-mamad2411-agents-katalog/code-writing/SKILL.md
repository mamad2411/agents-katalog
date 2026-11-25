---
name: code-writing
description: Evidence-based rules for writing code as a knowledge graph that orients agentic AI. Use when authoring new code, refactoring for agent-tractability, designing module boundaries, naming identifiers, writing types, documenting modules, choosing architecture patterns (hexagonal, clean, vertical slice, functional-core/imperative-shell), sizing functions/files/classes, defining architectural descriptors (AGENTS.md, ADRs), structuring monorepos (Nx, Turborepo, Bazel, Buck2, Pants, workspace boundaries, affected-graphs, per-package descriptors), or setting up validation gates that enforce these properties. Triggers on tasks framed as "how should this code be written", "agent-readable code", "code as knowledge graph", "naming convention", "folder structure", "AGENTS.md", "CLAUDE.md", "ADR", "function signature", "type contract", "structured output", "repo-level coding agent", "monorepo", "workspace", "module boundary", "architecture pattern", "hexagonal", "clean architecture", "dependency direction", or "affected graph".
license: MIT
metadata:
  author: duke
  version: "0.2.0"
---

# Code Writing

Rules for writing code as a knowledge graph for agentic AI. Each reference separates source-backed empirical evidence from derived authoring guidance, with bad/good code examples.

This skill treats the codebase as the operational ontology an agent consumes when reading and modifying code. The hypothesis: hardened rules covering naming, types, structure, composition, descriptors, and gates produce emergent navigability as the repo grows — reading the code hierarchically co-locates the LLM in the appropriate vector dimensions. The rules are derived from empirical studies of how LLMs and agents consume code, not from human-ergonomics traditions alone.

Each reference below is a separate file in `references/`; the agent loads only the references it needs for the current task. The fully expanded long-form guide lives in `AGENTS.md` for tools that follow the [AGENTS.md convention](https://agents.md) rather than the [Agent Skills spec](https://agentskills.io/specification).

## References

### 1. Identifiers — Names as Vector-Space Anchors — **CRITICAL**

Identifier obfuscation is the single most damaging transformation for LLM code comprehension — accuracy on intent-level tasks collapses while behavior-tracing persists, evidence that names carry the semantic signal models actually use. Misleading or inconsistent names actively poison agent reasoning because LLMs trust naming over deeper analysis. Names are the codebase's primary ontology layer; every other rule in this skill compounds with naming discipline.

- [`identifiers-descriptive-names`](./references/identifiers-descriptive-names.md) — Use Descriptive Identifiers That State Intent, Not Abbreviations or Single Letters
- [`identifiers-canonical-consistency`](./references/identifiers-canonical-consistency.md) — Use One Canonical Name Per Concept Across the Entire Repository

### 2. Types & API Surfaces — Contracts the Compiler and Decoder Both Enforce — **CRITICAL**

Types, schemas, and public-surface APIs are enforceable at both compile-time and LLM decode-time, making them the only contracts that hold under agent authorship. Type-constrained generation cuts compile errors by more than half and lifts functional correctness; typed-hole context produces the largest single accuracy gain for LLM completion. The public API of every module is simultaneously a runtime contract and the agent's retrieval index — DocPrompting shows a 52% relative Pass@1 lift when docs/types are retrievable at generation time. Narrow, well-documented surfaces win because they are cheaper to attend to and harder to misuse.

- [`types-strong-signatures`](./references/types-strong-signatures.md) — Annotate Every Public Signature With Specific, Non-any Types
- [`types-schema-validated-outputs`](./references/types-schema-validated-outputs.md) — Define and Schema-Validate Every Structured Output Cross-Boundary
- [`types-narrow-api-surfaces`](./references/types-narrow-api-surfaces.md) — Design Narrow, Deep Public API Surfaces; Curate Re-Exports Deliberately

### 3. Architecture & Repository Graph — Files, Folders, Imports, and Dependency Direction — **CRITICAL**

Repository-level coding gains from 2023–2026 come almost entirely from exposing code as a graph of definitions, callers, dependencies, and data flow — graph retrieval outperforms embedding retrieval by 23 percentage points on hidden-dependency tasks, plug-in repo graphs lift SWE-bench by tens of points, and cross-file is consistently the failure surface. Architectural discipline acts as a force multiplier on capability: SOTA proprietary models produce 0% hexagonal-direction violations under enforcement while open-weight models produce 80% with the same prompt. Folder layout, import topology, dependency direction, layered/hexagonal separation, and the pure-vs-effectful boundary are not aesthetic choices; they determine whether the dependency graph is legible at all, and they amplify whatever the model can do.

- [`architecture-fitness-functions`](./references/architecture-fitness-functions.md) — Encode Architecture as Executable Fitness Functions, Not Prose
- [`graph-acyclic-explicit-surfaces`](./references/graph-acyclic-explicit-surfaces.md) — Forbid Import Cycles and Publish Module Surfaces via Explicit Index Files
- [`architecture-dependency-direction`](./references/architecture-dependency-direction.md) — Make Dependency Direction Explicit; Domain Points Inward, Adapters Point Out
- [`graph-folder-as-module`](./references/graph-folder-as-module.md) — Make Folder Structure Mirror the Module Dependency Graph
- [`architecture-functional-core-imperative-shell`](./references/architecture-functional-core-imperative-shell.md) — Separate the Functional Core From the Imperative Shell; Push Effects to the Edge

### 4. Module Sizing — Functions, Files, and Classes Sized for Effective Context — **HIGH**

Effective LLM context is far smaller than advertised: Claude 3.5 Sonnet drops from 29% to 3% on LongSWE-Bench as context grows from 32K to 256K tokens; Chroma's "Context Rot" study reports significant degradation at 50K tokens inside 200K-token windows. The corollary is sizing discipline: short files with cohesive purpose, functions decomposed to roughly six lines when behavior-preserving, classes with few methods, docstrings compressed to information content, and stripped formatting on critical paths save 24.5% of input tokens with negligible accuracy loss. LLM-specific cognitive complexity (LM-CC) predicts agent struggle better than McCabe — sizing rules should target the LLM, not the human reviewer.

- [`sizing-function-and-file-bounds`](./references/sizing-function-and-file-bounds.md) — Keep Functions Small and Files Cohesive; Bound by LLM Cognitive Complexity, Not McCabe
- [`sizing-token-budget-and-context-rot`](./references/sizing-token-budget-and-context-rot.md) — Treat the LLM's Effective Context as a Hard Budget; Optimize Token Density

### 5. Composition — Front-Load Semantics in Every File — **HIGH**

LLM comprehension is empirically stronger at the start of files than the end, and explanatory comments measurably lift downstream task performance because they live in-distribution with pretraining corpora. File-level intent at the top, public types and exports before implementation, and WHY-not-WHAT comments are the highest-signal investments per token. They also pre-load the relevant region of vector space before the model reads the implementation.

- [`composition-front-load-intent`](./references/composition-front-load-intent.md) — Front-Load Every File With a Module-Intent Header and Public Surface
- [`composition-why-not-what-comments`](./references/composition-why-not-what-comments.md) — Write Comments That Explain WHY, Not WHAT — Especially at Non-Obvious Constraints

### 6. Descriptors — The Architectural Map an Agent Reads First — **HIGH**

Formal architecture descriptors reduce agent navigation steps by 33–44 percent and behavioral variance by 52 percent in field studies, regardless of file format. AGENTS.md and CLAUDE.md function as the orientation header for the entire repository, but single-file manifests stop scaling at roughly 10k lines — past that point, descriptors must tier (root contract, per-module specs, decision records). Without an explicit map, prompt wording silently fixes architecture ("vibe architecting") and the resulting decisions are unreviewable.

- [`descriptors-agents-md-tiered`](./references/descriptors-agents-md-tiered.md) — Maintain a Tiered AGENTS.md Map — Root Contract, Per-Module Specs, Sub-Agent Definitions
- [`descriptors-adrs-for-non-obvious-decisions`](./references/descriptors-adrs-for-non-obvious-decisions.md) — Record Every Non-Obvious Design Decision as an ADR

### 7. Monorepo Architecture — Workspaces, Boundaries, and Affected Graphs — **HIGH**

Monorepos compound every other rule in this skill: a well-structured workspace gives agents one coherent vector-space to navigate, while a poorly-structured one fragments context across implicit boundaries the agent cannot see. Industry evidence at scale is unambiguous — Stripe's autonomous agents ship roughly 1,300 PRs per week into a hundreds-of-millions-of-lines monorepo only because rules are scoped per-subdirectory, not global; Cursor's auto-index hard-caps at 50,000 files; AGENTS.md spec mandates nearest-wins precedence. Tag-based package boundaries (Nx, Packwerk, Spring Modulith), affected-graph build systems (Bazel, Buck2, Turborepo, Nx), and tiered per-package descriptors are the three mechanical levers that keep the monorepo legible as it grows.

- [`monorepo-tagged-package-boundaries`](./references/monorepo-tagged-package-boundaries.md) — Enforce Tag-Based Package Boundaries So Workspaces Form a Layered Dependency Graph
- [`monorepo-affected-graph-as-agent-context`](./references/monorepo-affected-graph-as-agent-context.md) — Expose the Affected/Build Graph as the Agent's Primary Navigation Primitive
- [`monorepo-per-package-tiered-descriptors`](./references/monorepo-per-package-tiered-descriptors.md) — Place AGENTS.md at Every Package Root; Nearest-File-Wins as Default

### 8. Gates — Mechanical Enforcement of the Ontology — **CRITICAL**

Every property the prior sections prescribe must be mechanically enforced at write-time and merge-time, or it drifts. Type-checking and linting catch surface defects; structured-output validation catches LLM-produced contract violations; strong test oracles catch behavioral shortcuts (a third of "successful" agent patches on weak oracles reflect inadequate tests, not correct fixes); agent-comprehension re-derivation tests catch semantic drift between the code's intent and its current shape. Gates are the only mechanism that keeps the ontology hardened under agent authorship.

- [`gates-type-check-and-lint`](./references/gates-type-check-and-lint.md) — Gate Every Commit With Strict Type-Checking and Naming/Style Lint
- [`gates-strong-oracles-and-agent-comprehension`](./references/gates-strong-oracles-and-agent-comprehension.md) — Test With Strong Oracles and Add Agent-Comprehension Re-Derivation Checks

## Full Compiled Document

For the complete guide with every reference expanded inline (bad/good examples, citations, prerequisites), see [`AGENTS.md`](./AGENTS.md). It is the [AGENTS.md-convention](https://agents.md) fallback for tools that do not load individual references on demand.
