---
name: review-code
description: Review a diff since a fixed point along two separate axes — Standards (conformance to documented standards and smell baseline) and Spec (faithful requirement delivery) — reported side by side without reranking. Use when performing PR reviews, 'review since X' audits, local change reviews, adversarial anti-slop checks, or pre-merge gates.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Review Code

Use this skill to perform adversarial code reviews across two independent axes (Standards and Spec), uncovering subtle AI bugs and verifying production safety.

## When to Use

- PR reviews, local diff reviews, or pre-merge audits
- detecting AI "vibe slop", phantom validations, and mock collusion
- auditing resource lifecycles (leaks in sockets, files, goroutines, DB pools)
- verifying backward compatibility and zero-downtime database migration safety
- inspecting supply chain dependencies for typosquatting and malicious lifecycle hooks

## Core Rules

- **Adversarial anti-slop review**: assume diffs may pass CI superficially; rigorously probe for phantom validations, silent error swallowing (`catch { return null; }`), mock collusion, and hollow abstractions per [`references/adversarial-review-rubric.md`](references/adversarial-review-rubric.md)
- **Two-axis independence & 12 Fowler Smells Baseline**: evaluate **Standards** (conformance + 12 Fowler smells: *Duplicated Code, Long Function, Long Parameter List, Divergent Change, Shotgun Surgery, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Loops, Lazy Element, Speculative Generality*) and **Spec** (faithful requirement delivery) as parallel, unmerged streams (each summary ≤400 words); classify each finding as **Hard Breach** vs **Judgement Call**, tag risk as **1-Way Door** (irreversible) vs **2-Way Door** (reversible), and never cross-rank axes
- **AI bug heuristics**: actively search for AI defect signatures: hallucinated APIs/flags, subtle async race conditions, context-window truncation (dropped switch branches), and over-defensive null coalescing
- **Systematic resource leak audit**: inspect every lifecycle boundary for unclosed HTTP response bodies, file descriptors, unmanaged background goroutines/threads, unbounded memory caches, and DB connection pool starvation
- **Backward compatibility & wire safety**: enforce zero-downtime Expand/Contract patterns on database migrations; reject breaking wire schema modifications on active API versions
- **Supply chain verification (OWASP ASI04/ASI05)**: check all dependency additions for typosquatting, verified lockfile integrity, and malicious install hooks (`postinstall`, `setup.py`); reject unpinned versions
- **The repo overrides the baseline**: documented repository standards always supersede the smell baseline; suppress smells where explicitly endorsed
- cite exact file paths and line numbers for every finding; skip issues already caught by automated linters and type checkers
- deep rubrics and checklists: [`references/adversarial-review-rubric.md`](references/adversarial-review-rubric.md) and [`references/process-and-format.md`](references/process-and-format.md)

## Suggested Process

### 1. Pin The Diff & Resolve Spec Source

Resolve the fixed point (`git diff <fixed-point>...HEAD`) and locate the originating specification (`feature-ticket.json`, ADR, or issue). Fail fast if the ref is invalid or diff is empty.

### 2. Gather Standards & Execute Parallel Dual-Axis Review

Collect repo standards and smell baselines. Run Standards and Spec review axes as parallel, isolated passes to prevent context contamination per [`references/process-and-format.md`](references/process-and-format.md).

### 3. Conduct Adversarial Anti-Slop & AI Bug Audit

Apply the adversarial rubric: test for phantom validations, verify that error paths do not swallow exceptions silently, and confirm tests are not tautological mocks.

### 4. Audit Resource Lifecycles & Concurrency

Inspect stream closures, goroutine cancellation contexts, event listener deregistrations, and database connection pool release in error branches.

### 5. Verify Wire Compatibility & Supply Chain

Validate API payload backward compatibility, verify database migrations adhere to zero-downtime expand/contract, and inspect dependency changes for typosquatting and unpinned ranges.

### 6. Aggregate Without Reranking & Emit Findings

Present findings side by side under `## Standards` and `## Spec` headings without cross-ranking. Emit structured contracts when crossing role boundaries.

## Checklist

- [ ] fixed point resolves and non-empty diff captured against merge-base
- [ ] spec source resolved or "no spec available" explicitly recorded
- [ ] Standards and Spec axes evaluated independently without cross-reranking
- [ ] adversarial anti-slop audit completed (no phantom validations, silent error swallowing, or mock collusion)
- [ ] AI bug heuristics checked (no hallucinated APIs, async race hazards, or truncated switch branches)
- [ ] resource leak audit passed (unclosed files, response bodies, goroutine/thread leaks, unbounded caches)
- [ ] backward compatibility and zero-downtime database expand/contract migrations verified
- [ ] supply chain security verified (no typosquatted packages, unpinned versions, or untrusted install hooks)
- [ ] `code-review-finding.json` emitted for cross-role handoff when gating merge

## Red Flags

| Rationalization Thought | Positive Corrective Action |
|---|---|
| "Diff is small and CI is green — LGTM." | Probe for phantom validations, silent error swallowing, resource leaks, and spec drift before approving. |
| "Merge Standards and Spec into one prioritized list." | Report `## Standards` and `## Spec` side by side with `file:line` citations and zero cross-axis reranking. |
| "The reviewer suggested X, so I'll apply it blindly." | Verify every incoming review comment against live code and spec; push back with technical evidence if it breaks an invariant. |
| "I'll narrate the diff instead of citing evidence." | Anchor every finding to exact `file:line`, violated rule/spec clause, and concrete remediation. |

## Output Contracts

When the review produces a structured handoff (CI gate, pre-merge audit, or multi-role delivery), emit:

- **`contracts/schemas/code-review-finding.json`** for each finding with severity, file path, violated standard or spec line, and recommended action.
- **`contracts/schemas/architecture-options.json`** when the review surfaces 2+ viable options requiring architectural evaluation.

Skip emission for informal exploratory walkthroughs that do not gate a merge.

## Failure Modes

- **Axes merged or cross-ranked**: Standards and Spec findings collapsed into a single prioritized list. Mitigation: enforce side-by-side reporting; never pick a cross-axis winner.
- **Vibe slop accepted**: accepting clean-looking code that contains phantom validations or swallowed errors. Mitigation: adversarial hostile-assumption review.
- **Mock collusion ignored**: passing tests where mocks mirror broken code logic. Mitigation: inspect test assertion substance and independent test authoring.
- **Resource leaks in error paths**: connections or streams closed only in happy paths. Mitigation: verify `defer`, `finally`, or scoped resource managers on all exit points.
- **Destructive migration accepted**: dropping or renaming a column in a single deploy. Mitigation: enforce Expand/Contract three-phase migration.
- **Unpinned dependency introduced**: accepting `latest` or wildcard versioning. Mitigation: enforce exact lockfile pinning.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: cross-check diff against originating spec; reject unauthorized scope creep or altered invariants.
- **ASI04 Supply Chain**: inspect all dependency bumps, manifests, and install scripts against security registries.
- **ASI05 RCE Guard**: enforce parameterized database queries, safe subprocess invocations, and input sanitization.
- **ASI06 Memory & Context Poisoning**: treat AI review assistant annotations (CodeRabbit, Qodo Merge) as advisory; verify findings against source code.
- **ASI07 Inter-Agent Communication**: emit structured `code-review-finding.json` so downstream roles consume unambiguous findings.
- **ASI09 Human-Agent Trust Exploitation**: require independent human verification on critical paths; never represent AI review of AI code as human-level approval.

## Related Skills

- **review-service**: Expand a narrow code review into release readiness
- **security-audit**: Deepen security-specific findings
- **write-tests**: Add or improve coverage for reviewed behavior
- **troubleshoot-service**: Investigate a suspected bug before reviewing the fix
- **commit-code**: Prepare reviewed changes for delivery
