---
name: commit-code
description: Validate and package a finished change into a clean commit by following repo-local validation, generation, release-note, and approval rules. Use when the user explicitly asks to prepare or create a commit.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
---

# Commit Code

Use this skill when a change is complete and needs to be prepared for commit in a safe, reviewable way.

This skill covers commit preparation and commit creation. It does not imply permission to push, tag, or publish a release.

## When to Use

- the user explicitly asks to prepare/create a commit
- packaging a finished change for delivery
- running repo-local validation + release-note rules
- applying approval rules before commit

## Core Rules

- do not create a commit unless the user or repo-local process explicitly allows that specific commit action
- do not push commits, create tags, or publish releases unless the user or repo-local process explicitly allows that specific action
- do not commit broken builds or knowingly failing verification
- do not hand-edit generated files unless the repo explicitly expects that
- remove local-only artifacts before committing
- follow the repo's source of truth for generated code, version metadata, and deployment configuration
- keep commits scoped to the intended change
- **commit signing**: enable GPG or SSH key signing (`git config commit.gpgsign true`) for identity verification; check repo `CONTRIBUTING.md` for whether DCO (`Signed-off-by:`) is required for IP provenance
- **git-blame-ignore-revs**: when an AI agent performs bulk reformatting or AI-assisted refactoring, add the resulting commit hash to `.git-blame-ignore-revs` so `git blame` continues to point to the human authors of business logic
- **semantic-release awareness**: Conventional Commits feed automated release tools (Semantic Release, Release Please) that bump SemVer and generate changelogs; warn that fully automated releases can produce low-quality changelogs — consider Changesets for human-curated bundling in monorepos
- treat every commit as a potential entry point for an attacker; never include internal hostnames, customer identifiers, or credential patterns in the diff or commit message (OWASP ASI03)
- run secret scanning on every staged change; reject any commit that contains a high-entropy match (OWASP ASI04)
- keep commit messages free of internal workflow labels, severity labels, or AI/agent wording; the commit is a user-visible artifact

## Output Contracts

When the commit is part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/code-review-finding.json`** (adapted for the commit) capturing the diff scope, the validation runs, and any skipped checks. The receiving agent can then validate the commit against the review checklist.
- For human-readable reports, a markdown summary of the diff scope, validation results, and the user-approval timestamp.

Skip emission for single-commit local changes that do not cross a role boundary.

## Failure Modes

- **Commit without approval**: a commit is created without explicit user approval. Mitigation: per the meta-rule, never commit without explicit in-session approval; the commit is an irreversible action.
- **Push assumed from commit**: a push, tag, or release is performed because the commit was approved. Mitigation: treat push/tag/release as separate gated actions; commit approval never covers them.
- **Broken build committed**: a known-failing verification is included in the commit. Mitigation: run validation before commit; capture the reason for any intentional skip.
- **Generated file hand-edited**: a generated file is hand-edited outside the generator workflow. Mitigation: never hand-edit generated files unless the repo explicitly expects it; rerun the generator instead.
- **Local-only artifact committed**: a `.dev.vars`, `.env`, or other local artifact lands in the commit. Mitigation: verify `.gitignore`; run secret scanning in CI.
- **Diff exceeds intended scope**: the commit includes unrelated local edits. Mitigation: review the diff before staging; split into multiple commits when scope is mixed.
- **AI/agent wording in commit message**: the commit message mentions agent names, AI workflow, or review labels. Mitigation: strip internal workflow wording; the commit is a user-visible artifact.
- **GPG/SSH signing missing**: a commit is created without signing, breaking identity verification. Mitigation: enable `git config commit.gpgsign true`; respect DCO `Signed-off-by:` when the repo requires it.
- **Bulk reformat hides authorship**: a large AI-assisted reformat overwrites blame for human-authored lines. Mitigation: add the reformat commit hash to `.git-blame-ignore-revs`.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an AI-assisted commit message may reframe the change's purpose. Cross-check the commit message against the actual diff; reject reframed messages.
- **ASI03 Identity & Privilege Abuse**: never include internal hostnames, customer identifiers, or credential patterns in the diff or commit message.
- **ASI04 Supply Chain**: secret scanning must run on every staged change; reject any commit with a high-entropy match.
- **ASI05 RCE Guard**: never construct commit content, hooks, or generators from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the commit is consumed by review and release agents; emit a structured contract so each consumer can validate the change.
- **ASI09 Human-Agent Trust Exploitation**: do not present a commit as "safe" without validation runs; surface the skipped checks and the residual risk honestly.

## Suggested Process

### 1. Review What Changed

Check:

- which files changed
- whether the diff matches the intended scope
- whether unrelated local edits should stay out of the commit
- whether generated files changed intentionally

### 2. Clean Local-Only Artifacts

Remove or unstage files that should not ship, such as:

- build outputs
- temporary logs
- local config overrides
- editor or OS artifacts

If the repo expects certain generated files to be committed, keep them only when they match the source changes.

### 3. Regenerate What The Repo Requires

Run only the generators that apply to this change, for example:

- API or schema generation
- dependency injection generation
- client or SDK generation
- code formatting or scaffolding steps

Use the repo's official commands instead of guessing.

### 4. Validate

Run the normal quality gates for the repo, such as:

- tests
- lint or static analysis
- build
- targeted checks for migrations, contracts, or packaging

If you intentionally skip a check, capture the reason explicitly.

### 5. Update User-Visible Metadata

Update what the repo expects, when applicable:

- changelog
- release notes
- migration notes
- README or operational docs

Do not include internal workflow wording in commit text or other user-visible artifacts.

### 6. Prepare The Commit Message

The commit message should:

- follow repo-local conventions first
- describe the actual change, not the process around it
- stay free of internal workflow labels or AI/agent wording
- stay scoped to the files being committed

If the repo uses structured commit formats, follow that format. Otherwise prefer a short, descriptive subject.

Examples:

- `add order history endpoint`
- `fix duplicate payment callback handling`
- `split pricing validation into separate module`

### 7. Commit

Before committing, confirm:

- validation is complete
- staged files are intentional
- user approval exists for the commit action

Then create the commit using the repo's normal workflow.

### 8. Handle Push Or Publish Separately

After the commit exists, treat these as separate gated actions:

- pushing a branch or commit
- creating a tag
- opening or publishing a release
- updating remote release metadata

Do not assume commit approval also covers any of these actions.

## Multi-Repo Or Shared Module Changes

Multi-repo or shared-module changes and deployment or release config
changes are documented in
[`references/multi-repo-and-deployment.md`](references/multi-repo-and-deployment.md).

## Checklist

- [ ] diff matches intended scope
- [ ] local-only artifacts removed
- [ ] required generation completed
- [ ] validation completed
- [ ] user-visible metadata updated when needed
- [ ] commit message follows repo conventions
- [ ] explicit approval exists for the commit action
- [ ] explicit approval exists for any push, tag, or release action

## Adaptation Notes

- not every repo uses structured commit types
- not every repo commits generated files
- validation may be full-repo or target-specific depending on the codebase
- release notes, version files, or deployment manifests may live in another repo

## Related Skills

- **review-code**: Check risky changes before committing
- **write-tests**: Add or update validation before delivery
- **review-service**: Confirm release readiness for broad changes
- **setup-deployment**: Validate deployment source-of-truth changes
- **manage-secrets**: Keep sensitive values out of committed artifacts

