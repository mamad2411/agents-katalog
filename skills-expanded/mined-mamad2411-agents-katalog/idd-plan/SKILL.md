---
name: idd-plan
description: "Bootstrap a greenfield IDD product PRD, reconstruct one from an already-implemented repository, plan the next issue from an existing sibling {project}-prd repository, or reconcile its progress tracker with verified live GitHub state."
compatibility: "Requires git and GitHub CLI (gh); works with Claude Code, Codex, Pi, and OpenCode."
---

# /idd-plan — start or continue an issue-driven product

Bootstrap a concise product contract — from requirements for a new product, or from the implemented source of an existing one — or bridge an existing private `{project}-prd` repository to its implementation repository, without importing CDD's artifact pipeline. Both bootstrap modes publish only `PRD.md` and `PROGRESS.md` to a private repository by default. Existing-project default mode is read-only and recommends one issue; reconcile mode updates only the tracker.

A greenfield or reconstruct invocation authorizes discovery, drafting, private PRD repository creation, initial commit, and push unless the user explicitly asks for draft-only output. Creating the implementation repository or an issue remains separate. `/idd-plan --reconcile` authorizes a tracker commit/push; successful `/idd-land` supplies the same authority automatically.

## Orient and select the mode

1. Resolve this installed skill directory and run its bundled `scripts/resolve-prd-pair.sh`; the only automatic association is the exact sibling `{implementation-name}-prd` with matching GitHub origins plus `PRD.md` and `PROGRESS.md`. Read both repositories' instructions. GitHub is lifecycle authority and the PRD is requirement authority.
2. Select the mode by what already exists: no product and no PRD source is greenfield; an implemented repository with real delivery history and no sibling PRD is reconstruct, which `--reconstruct` also names explicitly; an exact pair is default, or reconcile with `--reconcile`. Both bootstrap modes resolve a unique project slug, GitHub owner, private visibility, and workspace parent, and never overwrite a path or repository. `--reconcile` always requires an existing exact pair and clean trees.
3. Existing modes fetch the live issue/PR state, comments, checks, closing links, and squash commits needed for each conclusion. Parse requirements, slices, dependencies, release boundaries, tracker links, and explicit deferrals; preserve contradictions.

## Greenfield mode — clarify and author the product contract

1. Clarify intended users, problem, outcomes, workflows, security/data/API behavior, scope, non-goals, release boundary, and observable acceptance. Scale discovery to unresolved domain complexity: a small product gets few questions; a large, ambiguous, or high-risk domain gets more. Ask one decision at a time only when its answer materially changes the product, offer real alternatives with a recommendation, and stop when acceptance is unambiguous. Select technology and implementation details autonomously from best practices unless they change product behavior/risk or the user states a preference.
2. Draft one concise `PRD.md` with stable requirement IDs and small, dependency-ordered, independently reviewable delivery slices — one issue per slice, delivered issue-by-issue, never a monolithic slice for the whole project; every slice states its explicit dependencies and its own acceptance, which must never require a later slice's deliverable, and no slice claims a gate that only applies after all slices land. Draft `PROGRESS.md` as an implementation control panel with the same IDs, explicit status semantics, and only the baseline plus rows that answer what is ready, active, blocked, or missing acceptance; never use it as an append-only or commit log, and invent no GitHub evidence. Do not create a PLAN file or speculative issue backlog; recommend only the first ready slice as an issue contract.
3. Once the complete contract is settled, write only those two files, run this skill's bundled `scripts/init-prd.sh <path> <owner>/<project>-prd`, and read back the private remote and commit. If the user requested draft-only output, present both complete drafts and the recommended first issue without writing or publishing. Stop before implementation-repository or issue creation unless separately authorized.

## Reconstruct mode — derive the contract from implemented source

1. Read the whole implemented surface before drafting: every tracked entry point, its tests, its build/verification gate, its documentation, and any retained charter, plus the live issue, pull-request, and commit history. Name the exact source commit the reconstruction describes. Clarify with the user only what the source cannot answer — the release boundary, publication posture, or a disputed non-goal — never what the code already states.
2. Write requirements descriptively: each states behavior the source implements at that commit, and rationale is quoted only from repository evidence such as code comments, documentation, charters, issues, and pull requests. Attribute no intent the repository does not state, and stay silent where the implementation is silent.
3. Collapse all implemented scope into one verified implementation baseline in the PRD and `PROGRESS.md`, bound to the named source commit and real repository-gate result. Git and GitHub retain historical chronology: never turn each past commit, issue, or PR into a delivery slice or tracker row. Add slices only for explicitly accepted remaining feature, changed-behavior, or repair outcomes, carrying only real current lifecycle evidence and never invent issue numbers. Mark nothing `validated` without live acceptance evidence, state outstanding verification gaps explicitly, publish through this skill's bundled `scripts/init-prd.sh`, then continue in default mode.

## Default mode — recommend one next issue

1. Reconcile mentally, without editing, what is landed, partially landed, active, blocked, and unstarted. Do not equate merged code with release validation, and do not advance post-release work ahead of unmet initial-release dependencies.
2. Build a dependency-ordered view of the remaining slices, then select only the first independently reviewable outcome. Prefer completing a partially landed slice over starting a later one unless a recorded dependency blocks it.
3. Draft a compact, public-safe issue contract: source requirement and slice IDs, outcome, publishable evidence, acceptance criteria, non-goals, likely boundary, and verification. Reference rather than quote private rationale or source material; do not invent implementation details or create a speculative backlog.

## Reconcile mode — persist verified progress

1. Pull each clean default branch with `--ff-only`. Re-read every tracker-linked issue, PR, and commit needed for the changed rows. When called by `/idd-land`, also bind the supplied issue, PR, and squash commit to the matching requirement slice; stop rather than guess when that mapping is ambiguous.
2. Edit only `PROGRESS.md`, the implementation control panel: it must answer what is ready, active, blocked, and still missing acceptance. Record current issue/PR/squash evidence in its owning row, apply the existing status semantics, and replace superseded state instead of appending. At a completed release boundary, collapse terminal rows into one baseline containing requirement coverage, source commit, and verification or acceptance result; Git and GitHub retain lifecycle history. Keep only that baseline and rows that still guide implementation. Never copy private PRD content into the public repository or claim acceptance not proven by live evidence.
3. Run repository instructions, validate referenced requirement IDs and Markdown links, then run `git diff --check`. Audit the complete diff for lifecycle-only changes. If byte-identical, report already reconciled; otherwise commit `progress: reconcile <owner/repo>#<issue>` (or an equally specific repair subject), push the PRD default branch normally, and read back the remote commit.

## GATE — planning and reconciliation integrity

Both bootstrap modes require PRD/tracker ID agreement and private visibility readback unless draft-only. Greenfield additionally requires material product decisions settled and no technical-question drift; reconstruct additionally requires a named source commit, every implemented requirement traceable to source, one baseline bound to the real verification result, no historical delivery rows, and no `validated` status without live acceptance evidence. Existing modes require an exact pair and complete live-state reads. Every mode permits one next issue at most, dependency-respecting order, and no invented lifecycle evidence. Reconcile leaves both repositories clean and synchronized with only `PROGRESS.md` changed and only evidence needed for current implementation decisions; failure after merge is reported as `landed, PRD reconciliation incomplete` and never rolls back the merge.

## Completion

Greenfield returns the approved PRD/tracker repository and one next issue contract. Reconstruct returns the published PRD/tracker repository, the source commit, the requirement and slice inventory, and either one next issue contract or the outstanding acceptance and verification gaps when the implemented scope is already complete. Existing default returns discrepancies, ordered remaining slices, and one issue contract. Reconcile returns changed rows, evidence URLs and squash, commit/push state, and incomplete postconditions. Every mode gives exactly one next action (`/idd-issue …`, implementation-repository authorization, a named verification gap, or the named blocker).
