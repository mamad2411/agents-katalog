---
name: bootstrap-oss
description: Create or repair the governance file set of a repository — CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, SUPPORT, issue and PR templates, CODEOWNERS and funding metadata — tailored to the project's measured size, language and workflow. Use when a repository is going public, when its community files are missing or stale, or when an audit reports a governance gap. Not for triaging issues or cutting a release.
allowed-tools: Read Grep Glob Bash Write Edit
user-invocable: true
argument-hint: "[repo-path] [--band B0|B1|B2|B3] [--dry-run]"
model: sonnet
effort: medium
metadata:
  foundry.vertical: governance
  foundry.io: "repository state -> tailored community health files"
license: Apache-2.0
---

# Bootstrap open source governance files

Generate the community health files a repository actually needs, from what the repository
actually is. Boilerplate is the failure mode: a `CONTRIBUTING.md` that says "run the tests"
without the command, or a `SECURITY.md` with no contact, is worse than an empty repository
because it looks handled.

**Rule:** every generated file contains at least one fact measured from this repository —
a real command, a real path, a real name, a real number. A file with none of those is not
shipped; it is reported as a question for the maintainer.

## Phase 1 — Detect (never assume)

Run the detection sweep and record every answer with its source. Full command list:
`references/detection.md`.

```bash
ls -1 CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md GOVERNANCE.md SUPPORT.md \
      MAINTAINERS.md .github/CODEOWNERS .github/FUNDING.yml 2>/dev/null
ls -1 .github/ISSUE_TEMPLATE/ 2>/dev/null
cat LICENSE 2>/dev/null | head -3
git remote get-url origin
git symbolic-ref --short HEAD
git shortlog -sne --since='12 months ago' --no-merges | wc -l
git shortlog -sn  --since='12 months ago' --no-merges | head -10
git log -1 --format=%cs
```

Language and workflow, from manifests present — not from folder names:

| Marker file | Language | `{{SETUP_CMD}}` | `{{TEST_CMD}}` | `{{LINT_CMD}}` |
|---|---|---|---|---|
| `package.json` | JS/TS | `npm ci` / `pnpm i --frozen-lockfile` / `yarn --immutable` (pick by lockfile) | from `scripts.test` | from `scripts.lint` |
| `pyproject.toml` | Python | `uv sync` / `pip install -e '.[dev]'` | `pytest` or `[tool.*]` config | `ruff check .` if configured |
| `go.mod` | Go | `go mod download` | `go test ./...` | `go vet ./...` |
| `Cargo.toml` | Rust | `cargo fetch` | `cargo test` | `cargo clippy -- -D warnings` |
| `pom.xml` / `build.gradle` | Java | `./mvnw -q -DskipTests package` / `./gradlew assemble` | `./mvnw test` / `./gradlew test` | checkstyle/spotless if declared |
| `Gemfile` | Ruby | `bundle install` | `bundle exec rspec` | `bundle exec rubocop` |

**Read the scripts, do not invent them.** `jq -r '.scripts' package.json`,
`grep -A5 '\[tool.pytest' pyproject.toml`, `grep -E '^[a-z-]+:' Makefile`. If no test command
exists, that is a finding — say so and leave `{{TEST_CMD}}` for the maintainer rather than
writing a command that fails.

CI workflow: `ls .github/workflows/*.y*ml` and extract the job names that gate merges — those
are what `CONTRIBUTING.md` must tell contributors to satisfy.

GitHub-side state, guarded:

```bash
command -v gh >/dev/null && gh auth status >/dev/null 2>&1 && GH=1 || GH=0
[ "$GH" = 1 ] && gh api repos/{owner}/{repo} \
  --jq '{visibility,has_discussions,default_branch,license:.license.spdx_id,stars:.stargazers_count}'
[ "$GH" = 1 ] && gh api repos/{owner}/{repo}/collaborators --paginate \
  --jq '[.[]|select(.permissions.push)|.login]'
```

If `GH=0`: announce it once, derive what you can from git, and mark every GitHub-only value
`unavailable`. Do **not** guess maintainer handles, security contacts, funding accounts or
discussion URLs — those become questions in the report.

## Phase 2 — Size

Assign a band using `references/sizing.md` (same bands as the `governance-architect` agent).
Band drives *how much* document, not *how good*:

| Band | Ship | Do not ship |
|---|---|---|
| B0 solo | CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, issue+PR templates | GOVERNANCE, MAINTAINERS, CODEOWNERS, voting rules |
| B1 small team | + GOVERNANCE (1 page), MAINTAINERS, CODEOWNERS | elections, TSC, charters |
| B2 multi-party | + voting rules, quorum, tie-break, RFC process, emeritus policy | foundation charter |
| B3 institutional | + charter, terms, trademark pointer | — |

Escalate at most one band above measured, and only with a written trigger. If the caller passed
`--band` that exceeds the measured band by more than one, refuse and explain.

## Phase 3 — Ask, once

Some values cannot be measured. Collect them in **one** batch, with a default offered for each,
and never block on them — mark unanswered ones `{{TODO: ...}}` in a report section rather than
inventing a value.

Unmeasurable, must ask: security contact address; CoC contacts (need ≥ 2 routes); published
response-time numbers (default: measured median rounded up); DCO vs CLA; funding accounts;
question channel URL; supported-versions table; who holds release credentials.

## Phase 4 — Render

Templates live in `${CLAUDE_PLUGIN_ROOT}/templates/`. Substitution and conditional-block
conventions are in `${CLAUDE_PLUGIN_ROOT}/templates/README.md`.

Tailoring that must actually happen — this is the difference between this skill and copying a
starter repo:

1. **Commands are the project's real commands**, taken from Phase 1, and each one is executed
   once in a scratch checkout where safe (`{{LINT_CMD}}`, `{{TEST_CMD}}`) so the document does
   not ship a command that fails. If execution is not safe or too slow, say the command is
   unverified.
2. **Response times come from measurement**, rounded up, never from a template default.
3. **`CODEOWNERS` paths come from the actual tree**, and every owner is a real handle with push
   access. Verify: `gh api repos/{owner}/{repo}/codeowners/errors --jq '.errors'` must return
   `[]`. An unresolvable owner silently blocks every PR.
4. **Issue templates reference real version commands** (`{{VERSION_CMD}}`), the project's real
   runtime names, and the real support channel.
5. **Band-conditional blocks are resolved and deleted**, not left as comments.
6. **Existing files are merged, not overwritten.** For each existing file: diff the current
   content against the rendered one, keep project-specific prose, propose additions as a patch,
   and list removals for confirmation. Overwriting a hand-written `CONTRIBUTING.md` destroys
   institutional knowledge — never do it without an explicit confirmation in the transcript.
7. **`FUNDING.yml` is only written when a funding account exists.** Otherwise skip the file and
   say why.
8. **`CODE_OF_CONDUCT.md`** is rendered from the original Foundry policy template. If the
   maintainer prefers the Contributor Covenant, do not paste it: point them at the upstream
   source, let them add it themselves, and delete the Foundry template.

Also seed the label taxonomy when `gh` is present and the maintainer confirms:

```bash
jq -r '.[] | [.name,.color,.description] | @tsv' \
  "${CLAUDE_PLUGIN_ROOT}/templates/labels.json" |
while IFS=$'\t' read -r n c d; do
  gh label create "$n" --color "$c" --description "$d" --force
done
```

Never mass-relabel existing issues here — that belongs to `triage-inbox`, with confirmation.

## Phase 5 — Verify

Machine checks, all must pass before reporting success:

```bash
# 1. No unresolved markers anywhere in the rendered set
grep -rn '{{\|<!-- BAND\|<!-- OPT\|<!-- CHOOSE' \
  CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md SUPPORT.md GOVERNANCE.md \
  .github/ 2>/dev/null && echo 'FAIL: unresolved markers'

# 2. Issue forms are valid YAML
for f in .github/ISSUE_TEMPLATE/*.yml; do
  python3 -c "import sys,yaml;yaml.safe_load(open(sys.argv[1]))" "$f" || echo "FAIL: $f"
done

# 3. Internal links resolve
grep -oE '\]\(([^)h][^)]*)\)' *.md .github/*.md | sed 's/.*(\(.*\))/\1/' |
  while read -r p; do [ -e "${p%%#*}" ] || echo "FAIL: dead link $p"; done

# 4. CODEOWNERS resolves (requires gh)
gh api repos/{owner}/{repo}/codeowners/errors --jq '.errors | length'   # must be 0
```

Then the human checks, which are the ones that matter:

- Follow your own `CONTRIBUTING.md` from a **clean clone** in a scratch directory. If the test
  suite does not pass, the document is wrong, not the reader.
- Confirm the security contact receives mail. An unmonitored address is the most common
  silent failure in `SECURITY.md`.
- Confirm both CoC contacts have agreed to be listed. Listing someone without asking is itself
  a conduct problem.

If `superpowers` is installed, run `superpowers:verification-before-completion` over this list.
If not, walk it manually and state in the report that verification was unassisted.

## Exit criteria

- [ ] Band assigned from measured numbers; the numbers and their commands are in the report.
- [ ] Every file for the band exists; no file above the band was created.
- [ ] Zero unresolved `{{TOKEN}}` / conditional markers (check 1 passes).
- [ ] `{{SETUP_CMD}}`, `{{TEST_CMD}}`, `{{LINT_CMD}}` were executed, or explicitly flagged
      unverified with the reason.
- [ ] `CODEOWNERS` errors == 0, or `gh` unavailable and this stated.
- [ ] Issue forms parse as YAML; internal links resolve.
- [ ] `SECURITY.md` has a contact and a supported-versions table with at least one row.
- [ ] `CODE_OF_CONDUCT.md` has ≥ 2 contact routes and an acknowledgement window in hours.
- [ ] Response-time numbers are ≥ the measured medians, or marked `{{TODO}}`.
- [ ] Every pre-existing file was merged, not overwritten, unless overwrite was confirmed.
- [ ] Open questions listed with the exact value needed and who can supply it.

## What this skill deliberately does not cover

- **Designing governance.** It renders a decision; `governance-architect` makes it.
- **The licence itself.** It reads `LICENSE`; it never chooses, changes or adds one — that is a
  legal decision for the copyright holder.
- **Contributor Covenant or any other third-party policy text.** Referenced as an option, never
  vendored.
- **CLA infrastructure** (bot installation, agreement drafting, signature storage).
- **Branch protection, required checks, repository settings.** It reports what would be needed;
  it does not change repository configuration.
- **Existing issues and PRs** — `triage-inbox`.
- **Translation** of the generated files.
- **README, docs site, architecture documentation.**

## References

- `references/detection.md` — the full detection command set and what each answer feeds.
- `references/sizing.md` — band definitions, entry conditions and what each band ships.
- `${CLAUDE_PLUGIN_ROOT}/templates/README.md` — substitution and conditional conventions.
