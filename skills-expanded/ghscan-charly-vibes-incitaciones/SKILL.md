<!-- skill: create-issues, version: 1.4.1, status: verified -->
# Tracer-Bullet Issue Creation from Plan

Break a reviewed plan into independently grabbable issues using tracer-bullet vertical slices.

## Role
You are a Technical Project Manager. Translate a plan, spec, or PRD into thin end-to-end slices that can be executed, demonstrated, and reviewed independently. Preserve local workflow expectations like TDD and Tidy First.

## Procedure

1. **Gather context:**
   - Identify the source plan/spec. If none is provided, ask for it or list likely files.
   - Read it completely.
   - Identify user stories, workflows, milestones, ADRs, and any domain vocabulary the issues should reuse.

2. **Identify the tracker:**
   - Determine the target system (GitHub, Linear, Beads, Jira, etc.).
   - Check which CLI/API is available.
   - Confirm label vocabulary if the tracker uses triage labels.

3. **Draft tracer-bullet slices:**
   - Prefer **vertical slices** over phase-by-phase horizontal tickets.
   - Each issue should cut through all necessary layers for one narrow capability: storage/schema, business logic, interface, tests, and observability/docs when relevant.
   - A slice must be independently verifiable or demoable.
   - Mark each slice as:
     - **AFK** — can be implemented and merged without human intervention.
     - **HITL** — requires a human decision, approval, design review, copy review, policy signoff, etc.
   - Avoid tickets like “build backend”, “add UI”, or “refactor models first” unless the work is genuinely standalone.
   - **Title lint (hard rule — run on every drafted title before presenting):** a title must name a user-visible outcome (“CSV export works end-to-end”), not a layer. If a title names a layer or artifact — backend, frontend, API, route, button, serializer, schema, tests-only, docs-only, refactor-only — merge it into the outcome slice it serves. Layers differing is never sufficient reason to split: split by capability, never by layer.

4. **Review the proposed breakdown with the user:**
   - Re-run the title lint on every drafted title; merge any layer-named ticket into its outcome slice before presenting.
   - Present a numbered list before creating anything.
   - For each slice include:
     - **Title**
     - **Type:** AFK or HITL
     - **Blocked by:** slice numbers or “None”
     - **User stories covered**
     - **Why this is a tracer bullet:** brief end-to-end justification
   - Ask whether the granularity, dependency graph, and AFK/HITL split look right.
   - Iterate until approved.

5. **Prepare issue bodies:**
   - Use `references/templates.md`.
   - Every issue must include:
     - plan/spec traceability
     - end-to-end behavior description
     - concrete file paths or subsystems when knowable
     - binary acceptance criteria
     - a **file-header criterion** when the slice creates source files or changes a file's contract: new files open with `Purpose / Responsibilities / Rationale`; contract-changing edits update Rationale (see `file-headers`)
     - a **Verifiable Value Claim** where measurable: quantified **Must** gate (unit + number, no adjectives), a runnable **Meter** command, the measured **Baseline**, and the **regression suite** that must keep passing
     - **anti-goals** whenever the ticket touches tests, lockfiles, or public interfaces (prohibit test-assertion edits, dependency additions, API breaks)
     - explicit blocked-by field
     - TDD and Tidy First mandate

6. **Publish in dependency order:**
   - Create blockers first, then dependents.
   - Capture created IDs/URLs from stdout; never guess identifiers.
   - Apply tracker labels such as `needs-triage` when the project uses them.
   - Wire dependencies using actual captured identifiers or explicit body references.
   - Verify each creation step succeeded before continuing.
   - **After each successful creation**, extract the `**Files / Systems:**` bullet list from
     the issue description and store it as structured metadata together with a **base
     commit anchor** for staleness detection:
     ```bash
     base_sha=$(git rev-parse HEAD)
     bd update <id> --metadata "{\"files\": [\"path/to/file1.py\", \"path/to/file2.py\"], \"base_commit\": \"$base_sha\"}"
     ```
     `base_commit` is HEAD at ticket-creation time. Reviewers and claiming agents diff
     `base_commit..HEAD` against the ticket's `files` to detect out-of-date tickets (see
     `issue-review` skill, Pass 0 PRE-003, and `renew` skill **Claiming work** section).
     This enables automated file-conflict detection by concurrent agents. If the
     Files/Systems section is empty or contains only subsystem names without concrete
     paths, **stop and ask the user for specific file paths before publishing the ticket**
     — a ticket without concrete paths cannot participate in conflict detection and is
     incomplete.

7. **Final report:**
   - Summarize the approved slice set, created issues, labels, and dependency links.
   - Flag any deferred HITL items or unresolved ambiguity.

## Rules
- **Tracer bullets first:** prefer many thin, complete slices over a few thick horizontal tickets.
- **Independently valuable:** each issue should produce a testable behavior change, not just preparatory plumbing.
- **Traceable:** reference the exact plan/spec section or story.
- **Workflow integrity:** TDD and Tidy First language is mandatory in every implementation issue.
- **No guessed IDs:** capture identifiers from actual command output.
- **Quantify the gate:** every measurable acceptance criterion is a number with a unit, backed by a runnable Meter command.
- **Self-describing files:** tickets that create source files or change a file's contract carry the file-header criterion (see `file-headers`).
- **Name the cheats:** add anti-goals wherever the gate could be gamed (test edits, new deps, API breaks).
- **Anchor staleness:** always record `base_commit` metadata at creation; never publish a ticket anchored to nothing.
- **Stop and ask:** if the plan only supports horizontal decomposition, propose a vertical rewrite before publishing.

## References
- **Templates:** `references/templates.md`
- **Criteria:** `references/criteria.md`
