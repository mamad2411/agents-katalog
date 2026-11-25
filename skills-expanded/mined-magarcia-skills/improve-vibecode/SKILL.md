---
name: improve-vibecode
description: Audit and improve the quality of AI-assisted, vibe-coded, branch, or work-in-progress code changes through eight specialist subagents covering duplication, type ownership, unused code, dependency cycles, weak typing, error handling, legacy paths, and code/comment quality. Use when the user requests a comprehensive cleanup, hardening pass, code-quality overhaul, or invokes "Improve VibeCode" for an existing change set.
---

# Improve VibeCode

Improve an existing change set without turning a focused cleanup into a repository-wide rewrite. Use eight specialist subagents for independent research, then coordinate their edits so overlapping concerns do not corrupt the shared worktree.

## Process

### 1. Establish scope and repository rules

Verify state before assessing it:

1. Read the applicable `AGENTS.md` files, architecture notes, ADRs, contribution guidelines, and package/tool configuration.
2. Inspect Git status and preserve unrelated user changes.
3. Pin the target change set. Use the user's fixed point when supplied. Otherwise default to staged and unstaged changes; include branch changes only when the intended base can be established safely. Ask for the base if the worktree is clean or the scope remains ambiguous.
4. Record bounded commands that every subagent can use to inspect the same diff, changed files, and commits.
5. Identify the package manager, language, existing scripts, public/package exports, and whether the project has published compatibility commitments.
6. Run the smallest relevant baseline diagnostics so pre-existing failures can be separated from regressions.

Default edits to files in the target change set. Permit inspection of callers, dependencies, tests, generated entry points, and public consumers outside it. Edit an out-of-scope file only when the change requires it, and record the reason.

Complete this phase only when scope, repository rules, dirty-worktree state, and baseline results are explicit.

### 2. Apply the safety rules

- Prefer simpler code, but deduplicate only when the repeated code represents the same concept and extraction reduces total complexity.
- Share types only when they have the same domain meaning and a clear owning module. Similar shape alone is insufficient and can introduce coupling or cycles.
- Treat analyzer output as evidence, not truth. Corroborate it against framework conventions, dynamic imports, generated code, package exports, resolver configuration, tests, and external consumers.
- Do not add `knip`, `madge`, or another dependency solely for this audit. Use configured or already-available tooling first; use language-native or repository-specific alternatives otherwise.
- Do not ban `unknown`. Keep it at genuinely untrusted or opaque boundaries and narrow or validate it immediately. Remove unjustified `any`, broad object types, unchecked assertions/casts, and equivalent weak types only after proving the replacement.
- Do not remove meaningful error handling. Preserve parsing/validation boundaries, cleanup and `finally`, rollback, retry policy, error translation/context, and user/process/IO boundaries. Remove swallowed errors, false-success fallbacks, redundant log-and-rethrow blocks, and speculative catches.
- Do not break a published or public interface without authorization. Remove compatibility code when no compatibility commitment exists; otherwise surface the tradeoff.
- Do not delete comments that explain intent, invariants, constraints, or non-obvious tradeoffs. Remove narration, stale history, and comments that merely restate code.
- Do not alter behavior just to satisfy a cleanup heuristic. Require semantic evidence and a verification path for every implementation.

### 3. Launch eight specialist audits

Create exactly one capable subagent for each lane below. Request Sonnet or an equivalent reasoning model when model selection is available. Do not claim a specific model was used when it was not selectable. Launch all lanes concurrently up to the runtime's capacity and queue the remainder; do not combine lanes to reduce the total below eight.

The initial pass is read-only. This prevents agents with overlapping concerns from racing on shared files. Give every agent the same scope, repository instructions, baseline, and bounded inspection commands.

| Lane | Audit brief |
| --- | --- |
| 1. Deduplicate and consolidate | Find repeated logic and fragmented implementations. Recommend consolidation only when it improves locality, naming, or complexity; reject speculative abstractions. |
| 2. Type definitions | Locate relevant type definitions, determine their domain ownership, and identify genuinely shared definitions or duplicated sources of truth. Avoid generic dumping-ground type modules. |
| 3. Unused code | Use configured tools such as Knip when applicable, plus targeted searches and export/call-site checks. Prove code is unused across runtime, tests, tooling, dynamic imports, generated files, and package consumers before deletion. |
| 4. Circular dependencies | Use configured tools such as Madge or language-native dependency analysis. Distinguish runtime from type-only cycles, identify the ownership error causing each cycle, and avoid barrel-file reshuffling that merely hides it. |
| 5. Weak types | Find unjustified weak types, assertions, casts, and unvalidated data. Derive replacements from local declarations, schemas, call sites, tests, generated types, or official package documentation. Preserve and narrow `unknown` at trust boundaries. |
| 6. Error handling and defensive code | Find swallowed errors, misleading fallbacks, redundant catches, and speculative guards. Preserve handling with concrete recovery, translation, cleanup, retry, validation, or boundary semantics. |
| 7. Deprecated and legacy code | Find deprecated APIs, compatibility branches, stale feature paths, and fallbacks. Verify release/public API obligations and all consumers before recommending removal; do not leave breadcrumbs or unused re-exports. |
| 8. Code and comment quality | Find unfinished stubs, placeholders, fabricated implementations, speculative helpers, needless wrappers, vague naming, redundant prose, stale TODOs, and history comments. Preserve useful documentation and intentional extension points. |

Complete this phase only after all eight agents return an assessment, including lanes with no justified changes.

### 4. Enforce the evidence contract

Require each finding to include:

- stable finding ID and lane;
- file and line or symbol;
- concrete evidence and tools/configuration consulted;
- impact on readability, correctness, performance, security, accessibility, or maintenance;
- proposed change and why it is simpler;
- confidence level and semantic proof;
- affected callers, public API risk, and compatibility implications;
- dependencies or conflicts with findings from other lanes;
- focused verification command;
- intended files to edit.

Require each agent to provide a concise critical assessment of its lane, not merely a list of tool hits. Define high confidence as demonstrated semantics plus a credible verification path, not intuition.

### 5. Synthesize before writing

As coordinator:

1. Deduplicate findings that describe the same root cause.
2. Resolve contradictions between lanes using repository rules, domain ownership, public API constraints, and observed behavior.
3. Reject cosmetic churn, speculative generality, low-confidence deletions, and recommendations outside the agreed scope.
4. Build an implementation ledger containing accepted finding IDs, dependencies, execution order, exact file ownership, and validation commands.
5. Assign shared hotspots to one owner. Never allow concurrent edits to the same file or tightly coupled module.

Present tradeoffs to the user before implementation only when multiple valid approaches would materially change architecture, behavior, compatibility, or scope. Otherwise proceed with accepted high-confidence work.

Complete this phase only when every finding is marked `accepted`, `deferred`, or `rejected`, and accepted edits have conflict-free ownership.

### 6. Implement in conflict-safe waves

Send each originating specialist a follow-up task to implement its accepted high-confidence findings. A lane with no accepted findings remains a valid no-change assessment. Run agents in parallel only when their owned files and dependencies do not overlap.

Use this default dependency order, adjusting when evidence requires it:

1. remove proven-unused, deprecated, legacy, and stub surfaces;
2. fix dependency cycles and type ownership;
3. strengthen types and error semantics;
4. consolidate duplication and clean comments/naming.

Before every edit, have the owner re-read the current file because earlier waves share the worktree. Require focused tests or diagnostics after each wave. If a change fails, stop that line of work, identify why, and do not stack another speculative fix on top.

The coordinator owns integration edits that cross lane boundaries. Preserve unrelated changes and do not format untouched files.

Complete this phase only when all accepted findings are implemented or explicitly deferred with evidence.

### 7. Verify and re-audit

Run validation proportional to the changed code and repository conventions:

1. focused unit and integration tests for modified behavior;
2. type checking and editor/LSP diagnostics when available;
3. relevant linting and formatting checks;
4. unused-code and dependency-cycle analysis again;
5. the smallest relevant build or end-to-end check;
6. a bounded final diff review for accidental behavior changes, unrelated edits, stale comments, and newly unused exports.

Compare results with the baseline and label pre-existing failures separately. Do not treat one specialist's green command as validation of the integrated change set.

Complete this phase only when touched tests pass, relevant diagnostics are clean, and any remaining failure or risk is precisely reported.

### 8. Report the result

Return:

- the scoped critical assessment, summarized by all eight lanes;
- implemented changes grouped by root cause, with file references;
- validation commands and results;
- deferred or rejected recommendations with reasons;
- pre-existing failures, remaining risks, and explicit follow-ups.

Do not claim the codebase is clean beyond the pinned scope.
