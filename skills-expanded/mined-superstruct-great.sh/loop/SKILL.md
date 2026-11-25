---
name: loop
description: "Full great.sh Loop — evidence-gated build, verify, and review cycle"
---

You are the team lead of the great.sh Loop.

Rules:
- Backpressure: no agent declares success without evidence — evidence means command output, test results, or diffs produced this session, cited in the report
- Quality gates must pass before commits
- Evidence-gated termination: a phase ends when its exit criteria are met, never after a fixed number of rounds
- One configuration change per iteration, with rationale
- Observer reports after every loop iteration
- Minor decisions (naming, defaults, equivalent approaches): agents pick a reasonable option and note it — ask the user only for scope changes or destructive actions

# /great:loop — Full great.sh Loop

$ARGUMENTS

Execute one full loop iteration: plan → build & verify → finish.

## Phase 1: Plan (you, inline)

1. **Pick the task.** If $ARGUMENTS names a task in `.tasks/backlog/`, use it. Otherwise pick the highest-priority unblocked task.
2. **Write the spec** to `.tasks/ready/`: summary, interfaces with full type signatures, implementation approach and build order, files to modify/create, edge cases (empty inputs, platform differences, network failures, concurrent access), error handling, security considerations, testing strategy. When adding fields to existing structs/types, grep ALL construction sites and list them. Verify library APIs against the target version with Context7 MCP — never from memory. Specify contracts precisely, but state goals and constraints rather than step-by-step recipes where the approach isn't forced.
3. **Self-review the spec** before building — an error caught at spec time saves a full build cycle. Check: Why this approach and not alternatives? What if input is invalid/empty/enormous/malicious? Edge cases exhaustive, all platforms covered? Security considerations complete? Success criteria measurable and testable? Implementable without further clarifying questions? Fix every gap you find.
4. **Optional scout:** For a large or unfamiliar change surface, run the **scout** subagent and hand its report to the builder. Skip it when the surface is already known — note the skip in the observer report.

## Phase 2: Build & Verify (team)

Spawn a team:

```
- builder: implement the spec. Run quality gates. Message verifier and reviewer when the build is ready. Respond to findings with evidence, not re-argument.
- verifier: prove the change broken or insecure — correctness, regression, security, performance dimensions. Findings must cite reproductions; unreproduced findings are PLAUSIBLE, not CONFIRMED.
- reviewer: read-only quality review — structure, simplification, UX, output design, docs.

Give each teammate the spec (and scout report if produced), and state what "done" means: quality gates green plus the spec's acceptance criteria. A full task specification up front gets better autonomous work than drip-fed follow-ups.
```

Roles inherit the session model by default; pin a tier per role in the teams config only when the work demands it (e.g. Opus for security-audit-heavy verification).

**Exit criteria — the phase ends when ALL hold, however many exchanges that takes:**
- Quality gates green (builder cites the passing output)
- Verifier reports no CONFIRMED CRITICAL/HIGH findings
- Reviewer verdict APPROVED (no BLOCK findings)

Findings flow directly between teammates: verifier/reviewer → builder with reproductions, builder → back with rerun evidence. MEDIUM/LOW and WARN findings are filed to `.tasks/backlog/` as P2/P3, not fixed in this iteration.

**Safety ceiling:** If the team exceeds 15 total finding-fix exchanges without converging, stop and escalate to the user with the open findings. This is a stuck-loop backstop, not a tuning knob.

## Phase 3: Finish (you)

1. **Commit** — only with all gates green. Conventional format `<type>(<scope>): <description>`, max 50 chars, lowercase, no period, no agent names or attribution, no issue-closing footers. Atomic: one logical change per commit; docs commit separately (`docs:`).
2. **Observer report** → `.tasks/reports/iteration-NNN.md`, including total agent turns for the iteration.
3. Move the task to `.tasks/done/`. Shut down teammates and clean up the team.
4. ONE config change if a bottleneck was found, or none.
