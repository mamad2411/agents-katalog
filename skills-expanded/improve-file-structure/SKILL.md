---
name: improve-file-structure
description: "Assess project file organization and prepare a behavior-preserving migration plan for /implement when reorganization is justified."
argument-hint: "[path or pain point]"
disable-model-invocation: true
license: MIT
---

# Improve File Structure

Find where file placement makes a project hard to navigate or change. Design the smallest useful reorganization, grounded in the project's language, framework, and existing conventions. End with a plan for `/implement`; this skill changes no project files. Present the plan in the conversation unless the user requests a saved artifact.

**File placement is the scope.** Moves, descriptive path names, and the import or configuration updates they require belong here. Changes to responsibilities, interfaces, or dependency direction belong in `/improve-architecture` in Claude linked installs or Cursor, `/supermatt:improve-architecture` from the Claude plugin, `$improve-architecture` in Codex, or `/skill:improve-architecture` in OMP. Code-level cleanup belongs in `/refactor`, `/supermatt:refactor`, `$refactor`, or `/skill:refactor`, respectively. Identify those needs without adding them to a relocation plan.

## Principles

- **Friction before folders.** A crowded directory is a clue, not a finding. Cite the navigation or maintenance problem and the files that cause it. A small flat project can be healthy; file-count limits and aesthetic symmetry do not justify moves.
- **Locality with ownership.** Group files that implement the same concept and are understood or changed together. Imports and change history support that judgment; neither proves it alone. Prefer feature/domain grouping when it solves the observed problem, and keep an established layout when it works.
- **Paths can be contracts.** Runtime discovery, package visibility, public imports, and published artifacts can depend on a path. Preserve those contracts by default; folder moves do not grant permission to change them.
- **Every directory earns its place.** Give it a clear responsibility and a rule for what belongs there. Keep feature-specific helpers, types, tests, and assets near their owner where tooling permits. Create shared areas only for demonstrated shared use, with a specific purpose rather than a new catch-all.

## Process

### Step 1: Map the area

Use the user's path or pain point as the scope. Otherwise inventory the repository at a high level and inspect likely trouble spots first. Read project instructions, glossary terms, and relevant architecture decisions before choosing a convention.

Identify languages, frameworks, applications versus libraries, workspace/package boundaries, entry points, and the commands used to build, test, and package them. Separate authored source, tests, resources, tooling, generated output, and vendored code. Generated and vendored files are not relocation candidates; inspect their producers when paths matter.

Use CodeGraph first when the repository is indexed, or existing symbol-aware tools when available. Otherwise use file search and read the source. Map each directory's role, related file clusters, dependencies crossing the proposed scope, and path-based discovery. Inspect available git history for files that change together, discounting bulk moves and formatting commits. Mark text-search or dynamic-reference gaps; do not claim an exhaustive dependency graph from filename matches.

Read only the language references used in this area:

| Area | Reference |
|---|---|
| TypeScript/JavaScript apps, libraries, or workspaces | [TypeScript](references/typescript.md) |
| Go packages and commands | [Go](references/go.md) |
| Python packages and applications | [Python](references/python.md) |
| Ruby gems and applications, including Rails | [Ruby](references/ruby.md) |

These references distinguish source-backed constraints from this skill's recommendations. For another language or an uncertain framework/version rule, consult its primary documentation. Try the site's root `llms.txt` or `llms-full.txt` first, then the relevant HTML page. Record the source and its scope; do not present one framework's preferences as language requirements. No general web research pass is needed when the supplied guidance resolves the question.

Done when: the scoped inventory accounts for the directories reviewed, their roles and constraints, and any exclusions or unknowns that limit the assessment.

### Step 2: Assess

Look for mixed concerns in one folder, one feature scattered across unrelated folders, ambiguous catch-all locations, redundant nesting, and inconsistent placement that makes the next file's home unclear. Read the implicated files before reporting a finding.

For each finding, cite concrete paths, explain a real navigation/change task made harder, and explain how a placement change would help. Rank benefit against churn and compatibility risk. A cycle that needs interface redesign is an architecture finding; moving it into prettier folders does not fix it.

| Verdict | Action |
|---|---|
| **Healthy** | Explain why the current layout works and stop. |
| **Localized** | Present the affected clusters and recommend the smallest useful reorganization. |
| **Systemic** | Rank independent candidates and propose an incremental starting area. |

Keep unresolved inspection gaps visible alongside the verdict. For a recently reorganized area, require new evidence before proposing another layout. If the same problem remains, explain why the previous move failed. Honor a specific user request on healthy code, but distinguish that preference from a defect. Assess the existing layout separately from a requested move: a move that violates a path contract does not make the current layout defective. Report the conflict and keep that candidate pending.

Done when: every candidate has evidence, a placement-level remedy, and a benefit that justifies the migration.

### Step 3: Choose and design

Present candidates with stable IDs, affected paths, the intended benefit, migration cost, and contract risks. Recommend one and ask the user which to pursue using the host's question tool when available. If their request already selects the area and approach, continue without repeating that choice. Ask only decisions the repository cannot answer.

For the selected candidate, show a before/after tree and each proposed directory's responsibility. Explain where the next similar file belongs, including when it should remain local or become shared. Use project vocabulary and naming conventions. A feature folder is not automatically a new package, public API, barrel, or architectural layer.

Resolve outstanding choices that affect public paths, framework discovery, package boundaries, or migration scope with the user before finalizing. Preserve contracts by default, using existing entry points or a concrete compatibility forwarding plan where needed. A straightforward forwarding entry point that satisfies an already chosen preservation requirement needs no repeated approval. If preserving contracts requires a broader design change, stop that candidate at the architecture handoff.

Done when: the target layout, placement rules, and compatibility choices are settled.

### Step 4: Write the migration plan

Include these sections so another agent can execute without choosing a different layout:

1. **Problem and target:** scope, evidence, before/after tree, directory responsibilities, and future placement rules.
2. **Move map:** every source path and destination, including tests and resources. A directory-level row is sufficient only when all descendants keep their relative paths; enumerate exceptions. Note conflicts and case-only renames.
3. **Reference and contract updates:** identify importers/re-exports and affected manifests, aliases, discovery globs, resource paths, generated-file producers, packaging, CI, scripts, and documentation. Name preserved external paths and any approved compatibility mechanism. Flag dynamic references that need runtime checks.
4. **Migration sequence:** bounded steps, keeping each move with its caller/configuration updates. Separate independent clusters; preserve unrelated work. Specify any temporary forwarding files and their lifetime. Do not mix behavioral refactors or test deletions into file moves.
5. **Verification:** commands discovered from the project, baseline status, and the failure each relevant check can catch. Cover affected tests, type/build checks, runtime discovery and packaged entry points where applicable; retain test assertions and ensure the same tests are discovered. Add a focused behavior check only for a real uncovered path contract. Record pre-existing failures and unavailable checks instead of promising a green migration without evidence.

Run cheap, non-mutating checks when they settle an uncertainty; leave write-producing generation, migration, or auto-fix commands to implementation. Every moved path must be accounted for in the move map and the verification strategy. A directory-only smoke check is not proof that runtime behavior survived.

Done when: every move has a destination, required reference updates, compatibility treatment, and a check that can detect its likely failure.

### Step 5: Hand off

Hand off only when Step 4's completion criterion is met. Missing facts that determine a move, reference update, or verification method keep the plan provisional: inspect them or ask for unavailable information first. Known checks that cannot run in this environment remain explicit verification gaps, not invented results.

For a multi-session migration, pass the complete approved move map to `to-spec` as path requirements, not disposable implementation notes. Its published spec must retain the exact source/destination rows and preserved path contracts in a **Migration map** section. Each affected ticket must link that authoritative section and identify its assigned rows and contract updates; a fresh implementation session reads it before moving files. Do not hand off an outline that requires the next agent to reconstruct the approved layout.

For work that fits this session, tell the user to run `/implement` in Claude linked installs or Cursor, `/supermatt:implement` from the Claude plugin, `$implement` in Codex, or `/skill:implement` in OMP with this plan. For multiple sessions, point to `/to-spec`, `/to-tickets`, then `/implement`; `/supermatt:to-spec`, `/supermatt:to-tickets`, then `/supermatt:implement`; `$to-spec`, `$to-tickets`, then `$implement`; or `/skill:to-spec`, `/skill:to-tickets`, then `/skill:implement`, according to the host. These are user-invoked skills: recommend the next command, do not invoke it or start moving files.
