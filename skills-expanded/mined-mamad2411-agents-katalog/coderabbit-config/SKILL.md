---
name: coderabbit-config
description: >
  Use when the user says "configure coderabbit", "add .coderabbit.yaml", "update
  the coderabbit config", "tune coderabbit for this repo", or "make coderabbit
  fit this repository". NOT for running a review — that is code-review.
user-invocable: true
---

# CodeRabbit Repository Configuration

GitHub-workshop only. Origin workshop does not use CodeRabbit. Do not add
`.coderabbit.yaml` or tune CodeRabbit because an Origin change is in flight.

Set up a useful, repository-specific `.coderabbit.yaml` in an existing Git
repository. Treat the repository and its history as the source of truth: do
not paste a generic template and do not hide a path merely because it is
private or inconvenient to review.

## Operating contract

- Work from the repository root. Refuse to guess if the supplied path is not a
  Git worktree.
- Load the applicable `AGENTS.md`, `CLAUDE.md`, `README.md`, contribution
  guide, CI documentation, and repository-local instructions before editing.
- Preserve existing user changes. Inspect `git status --short` first. Do not
  reset, clean, stash, commit, push, or rewrite unrelated files.
- Treat `.coderabbit.yaml` as a tracked repository policy file. Keep existing
  intentional settings unless the inventory gives a concrete reason to change
  them; make the smallest coherent edit.
- Never read the contents of credential files, `.env` files, private keys,
  tokens, browser data, or other secret-bearing material. Record their paths
  and risk classification only.
- Do not commit or push unless the user separately asks for that operation.

## Workflow

### 1. Establish repository identity and current state

Run a compact preflight from the repository root:

```bash
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
git log -12 --oneline --decorate
```

Resolve the canonical remote and the hosting platform. If the worktree is
dirty, preserve all unrelated changes and note whether `.coderabbit.yaml` is
new, modified, staged, or already committed.

### 2. Build a bounded full inventory

Inspect names, metadata, and representative source/config files; do not dump
the whole repository into context. Use `rg --files`, `find` with explicit
exclusions, `git ls-files`, `file`, and targeted `sed`/`head` commands.

Record the following classifications with paths and evidence:

1. **Project shape** — top-level directories, submodules, symlinks, monorepo
   packages, components, and workspace boundaries.
2. **Languages and frameworks** — source extensions, package manifests,
   lockfiles, build systems, runtime versions, generated-code frameworks, and
   declared dependencies.
3. **Execution surfaces** — entry points, scripts, Makefiles, task runners,
   Dockerfiles, deployment manifests, systemd/service files, and release
   tooling.
4. **Quality surfaces** — unit/integration/e2e tests, fixtures, linters,
   formatters, type checkers, schemas, and existing CI checks.
5. **Documentation and policy** — `AGENTS.md`, `CLAUDE.md`, README files,
   contribution guides, code-of-conduct files, editor settings, and any review
   or security policy.
6. **Generated or unsuitable review output** — build directories, rendered
   sites/PDFs, coverage, caches, vendored dependencies, minified assets,
   binaries, lockfiles, media, and large raw data. Confirm that each candidate
   is actually generated or unsuitable before excluding it. Identify the
   generator and keep that source reviewable.
7. **Intentional sensitive or operational content** — private notes,
   inventories, hostnames, public fingerprints, medical/personal records,
   deployment state, or research data. List paths only and determine whether
   the repository policy says these should still receive factual/schema
   review.

Use this inventory to map actual repository paths to review domains. Do not
invent `src/**`, `tests/**`, `scripts/**`, or other patterns that do not exist.

### 3. Learn from history and existing reviews

Inspect history before choosing instructions or exclusions:

```bash
git log --all --oneline --decorate -30
git log --all --stat -20
git log --all -- .coderabbit.yaml
git shortlog -sn --all
```

Look for recurring bug classes, fragile interfaces, repeated rework, generated
file churn, review-policy changes, and paths that maintainers treat as
authoritative. Use `git log --name-only` or `git log --numstat` when a churn
hotspot needs evidence, repeating `git log --all -- path/to/hotspot` for the
actual paths discovered in the inventory. Do not treat one old commit as a
current convention without checking the present tree.

If the remote is GitHub and `gh auth status` succeeds:

```bash
gh repo view --json nameWithOwner,defaultBranchRef,url
gh pr list --state all --limit 20 --json number,title,state,mergedAt,updatedAt,headRefName,baseRefName
```

Inspect a small, representative set of recent merged and open PRs, including
their review bodies and changed-file lists when available. Look specifically
for repeated reviewer comments, accepted versus rejected suggestions,
recurring test gaps, and generated/private paths that caused noise. If GitHub
is unavailable, continue and say that PR history was not inspected; do not
fabricate review learnings. For non-GitHub remotes, use an installed native
CLI only when it is already available and authenticated.

### 4. Decide the review policy

Draft the policy before editing YAML:

- **Review broadly by default.** Source, tests, configuration, scripts,
  documentation, schemas, and intentional operational records remain in scope.
- **Exclude only demonstrated noise.** Add negative `path_filters` for
  generated output, caches, binaries, vendored code, or large raw artefacts
  when the repository actually contains them. Never exclude a directory only
  because it contains private data, hostnames, or strings that resemble
  secrets if the user wants those files reviewed.
- **Review generators, not emissions.** For every generated exclusion, add a
  path instruction for the script/template/configuration that produces it.
- **Use path instructions for semantics.** Add focused instructions for actual
  controllers, APIs, tests, schemas, infrastructure, data, docs, and policy
  paths. Include the repository's domain-specific failure modes learned from
  history and PRs.
- **Make privacy and secret policy explicit.** If a path contains intentional
  private or operational records that should still be reviewed, tell the model
  to focus on factual consistency, schema integrity, stale state, duplication,
  broken references, and unsafe executable instructions; do not raise privacy,
  PII, credential, token, or secret-like-string findings there unless the user
  requested a privacy/security audit.

### 5. Configure tools without making false promises

Enable tools that match the detected languages and existing repository
configuration, such as Ruff, ESLint, shellcheck, actionlint, markdownlint,
yamllint, or the appropriate language checker. Point them at existing config
files instead of duplicating rules.

Treat secret and security tools separately from AI path instructions:

- `path_instructions` guide the review model; they do not reliably suppress
  findings emitted by a separate scanner.
- Keep secret scanners enabled when the repository needs secret coverage.
- If the repository deliberately stores secret-like operational or personal
  records and its policy requires no secret-scanner comments, disable the
  relevant scanner globally only when there is no supported per-path ignore
  mechanism. State the resulting loss of automated coverage in the report.
- Never disable all security analysis just to make a noisy review disappear.
  Prefer a scanner-supported ignore file or a narrower repository policy when
  available.

### 6. Write or update `.coderabbit.yaml`

Create the file at the repository root with the v2 schema header and a
repository-specific configuration. Prefer this structure, adapted to the
inventory:

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: "en-GB"
early_access: false

reviews:
  profile: "chill"
  high_level_summary: true
  path_filters: []
  path_instructions: []
  tools: {}
```

Do not add empty keys that the repository does not need if the existing config
or schema conventions prefer omission. Preserve an existing language, profile,
auto-review, chat, or tool setting unless the inventory justifies changing it.
Merge path instructions by path rather than duplicating contradictory entries.
Keep comments short and explain only non-obvious exclusions or policy choices.

### 7. Validate the real configuration

Run all available, relevant checks:

```bash
coderabbit config validate
git diff --check
```

The CLI is v0.7.x and its flag set changed from earlier versions — check
`coderabbit --help` / `coderabbit config --help` rather than trusting
memorised flags. If the CodeRabbit CLI is unavailable, use an installed YAML parser or
`yamllint` for syntax validation and report that schema validation could not
be run. Check that every `path_filters` and `path_instructions` glob matches
the intended repository paths, every excluded generator has a reviewable
source, and no secret-bearing file was read or added to the config.

If the YAML change is part of a larger code change, run the repository's
focused validation and a local CodeRabbit review according to the repository's
own instructions. This skill configures the review; it does not silently fix
unrelated findings.

## Required final report

Report, concisely but concretely:

1. Repository identity and worktree state.
2. Inventory summary: project type, languages, execution/quality surfaces,
   generated paths, and intentional sensitive/operational paths.
3. History/PR learnings used, or the exact reason either source was unavailable.
4. `.coderabbit.yaml` changes, including every exclusion and its evidence.
5. Tool choices and any security-scanner coverage trade-off.
6. Validation commands and results.
7. Any unresolved ambiguity. Do not claim the configuration is effective on
   GitHub until the file is committed and the CodeRabbit App has reviewed a
   real PR.

## Gotchas

- A path filter changes the review surface; a path instruction changes the
  review guidance. Do not use one as a substitute for the other.
- CodeRabbit has default ignored paths. Force-include a file only when the
  inventory shows that it is meaningful and the user wants it reviewed.
- A repository can contain intentional secret-like strings without containing
  credentials. Separate privacy/noise policy from actual secret exposure and
  document the decision.
- Historical PRs are evidence, not authority. Reconcile old review habits with
  current code, current instructions, and current dependencies.
- A valid YAML parse does not prove that CodeRabbit understands the intended
  globs or tool names. Prefer `coderabbit config validate`, then inspect the
  resulting diff manually.
- Never overwrite a dirty `.coderabbit.yaml` from a template. Merge it
  surgically and preserve unrelated user edits.

## References

- CodeRabbit path instructions and filters:
  https://docs.coderabbit.ai/configuration/path-instructions
- CodeRabbit YAML configuration:
  https://docs.coderabbit.ai/getting-started/yaml-configuration
- CodeRabbit configuration reference:
  https://docs.coderabbit.ai/reference/configuration
- CodeRabbit tool configuration:
  https://docs.coderabbit.ai/tools
