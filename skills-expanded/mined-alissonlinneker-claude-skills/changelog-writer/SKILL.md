---
name: changelog-writer
description: >
  Generate professional changelogs, release notes, and version history from git commits,
  diffs, PR descriptions, or bullet point lists of changes. Use this skill whenever the user
  says "write the changelog", "create release notes", "generate CHANGELOG.md", "document
  what changed", "what should I put in the release", "bump the version", "write the GitHub
  release", "summarize these commits", "prepare the release", "draft release notes",
  "what changed since last release", "tag and release", "version bump", or pastes a git log,
  list of commits, PR titles, or diff. Also trigger for "keep a changelog format", "semantic
  versioning", "squash and summarize these changes", "release readiness", "changelog for
  this sprint", "what ships today", "monorepo release", "package release", "publish to npm",
  "publish to PyPI", "write CHANGELOG", "update CHANGELOG", or any request to communicate
  what changed between two software versions to developers, end users, or stakeholders.
  Output is always ready to paste — no editing required.
---

# Changelog Writer

The definitive changelog and release notes skill. Transforms raw git history, commit messages,
PR descriptions, and code diffs into polished, production-ready changelogs and release notes.
Produces up to five output formats simultaneously: developer-facing CHANGELOG.md, human-facing
GitHub release notes, internal Slack summary, customer-facing email/newsletter, and package
registry release notes. Every output is ready to paste — zero editing required.

---

## Workflow

Follow these phases in order. Do not skip phases. Do not produce output until Phase 5.

---

### Phase 1 — Acquire Changes

Determine input type and acquire all material needed to generate the changelog.

| Input Type | Action |
|---|---|
| No input provided | Run `git tag --sort=-v:refname` to find the latest tag, then `git log <latest-tag>..HEAD --oneline --no-merges` to get unreleased commits. If no tags exist, use `git log --oneline --no-merges -50` and ask the user for the version range. |
| User says "generate changelog" / "what changed" with no specifics | Auto-detect: find latest two tags with `git tag --sort=-v:refname`, run `git log <prev-tag>..<latest-tag> --oneline --no-merges`. If HEAD is ahead of the latest tag, use `<latest-tag>..HEAD` instead. |
| User specifies version range (e.g., "v1.2.0 to v1.3.0") | Run `git log v1.2.0..v1.3.0 --oneline --no-merges`. |
| Pasted git log | Parse directly. Detect conventional commit format automatically. |
| PR titles / descriptions | Parse each PR as a change entry. Use PR labels for categorization if available. |
| Diff or file list | Analyze the diff to understand what changed. Summarize by functional area. |
| Free-form description | Parse natural language into structured change entries. |
| Existing messy changelog | Parse, validate, clean up, and reformat to Keep a Changelog standard. |
| Single commit message | Expand into a full, context-rich release note. |
| GitHub PR URL or number | Use `gh pr view <number> --json title,body,labels,mergedAt,files` to fetch PR details. Use `gh pr diff <number>` for the code diff. |
| Monorepo with path prefix | Filter commits by path: `git log <range> --oneline --no-merges -- <path>`. See Phase 1b. |

**Git integration commands to run automatically** (when in a git repository):

```bash
# Detect latest tags
git tag --sort=-v:refname | head -5

# Get repo remote URL (for comparison links)
git remote get-url origin 2>/dev/null

# Get current branch
git rev-parse --abbrev-ref HEAD

# Count commits since last tag
git rev-list --count $(git describe --tags --abbrev=0 2>/dev/null)..HEAD 2>/dev/null
```

If any git command fails (not a git repo, no tags), fall back gracefully to whatever
input the user provides and note the limitation.

#### Phase 1b — Monorepo Detection and Handling

When the repository appears to be a monorepo (multiple package.json files, workspace
configuration, `packages/` or `apps/` directory structure, Lerna/Nx/Turborepo config),
or when the user specifies a package/workspace:

1. **Detect workspace structure:**
   ```bash
   # Check for monorepo indicators
   ls packages/ apps/ modules/ libs/ 2>/dev/null
   cat package.json | grep -c "workspaces" 2>/dev/null
   ls lerna.json nx.json turbo.json pnpm-workspace.yaml 2>/dev/null
   ```

2. **Filter commits by path prefix:**
   ```bash
   git log <range> --oneline --no-merges -- packages/<package-name>/
   ```

3. **Handle independent versioning:**
   - Each package may have its own version. Check `packages/<name>/package.json` or equivalent.
   - If the user says "release @scope/package-name", filter to that package only.
   - If the user says "release all packages", generate a changelog per package that has changes.

4. **Cross-package changes:**
   - Commits touching multiple packages get listed in each affected package's changelog.
   - Root-level changes (CI, tooling) go in a "Tooling" or "Infrastructure" section of a root changelog.

5. **Output format for monorepo:**
   Present each package with changes as a separate section:
   ```markdown
   # Release Notes — 2026-03-14

   ## @myorg/core (1.5.0 → 1.6.0)
   ### Added
   - ...

   ## @myorg/ui (2.1.0 → 2.1.1)
   ### Fixed
   - ...

   ## @myorg/api (no changes)
   ```

---

### Phase 2 — Detect Project Conventions

Before categorizing, detect the project's conventions to calibrate parsing:

**Conventional commits detection:**
```bash
# Sample recent commits to detect format
git log --oneline -20
```

| Pattern Detected | Behavior |
|---|---|
| Most commits use `type:` or `type(scope):` | Full conventional commit parsing. Use type for category, scope for grouping. |
| Mixed — some conventional, some not | Parse conventional commits by type. Classify others by keyword analysis. |
| No conventional commits | Classify entirely by keyword analysis and diff inspection. |

**Existing CHANGELOG.md detection:**
```bash
# Check for existing changelog
ls CHANGELOG.md CHANGELOG changelog.md HISTORY.md RELEASES.md NEWS.md 2>/dev/null
```

If an existing changelog file is found:
1. Read it to understand the project's changelog style and conventions.
2. Match the existing format exactly (heading levels, bullet style, date format, link format).
3. Validate it against Keep a Changelog format and note inconsistencies (see Phase 2b).
4. Determine the correct insertion point for the new entry.

**Version format detection:**
```bash
# Check existing tags for version format
git tag --sort=-v:refname | head -10
```

Detect and match the project's version format:
- `v1.2.3` vs `1.2.3` (with or without `v` prefix)
- Calendar versioning: `2026.03`, `2026.03.1`
- Build numbers: `build-1042`
- Codenames: detect if tags or releases use codenames alongside semver

#### Phase 2b — Changelog Validation

When an existing CHANGELOG.md is found, validate it before inserting new content:

**Validation checks:**

| Check | Pass | Warn | Fail |
|---|---|---|---|
| Keep a Changelog format compliance | Follows standard headings | Minor deviations | Completely non-standard |
| Version ordering | Newest first, monotonically decreasing | One entry out of order | Multiple entries out of order |
| Date format | ISO 8601 (YYYY-MM-DD) consistently | Mixed formats | No dates at all |
| Comparison links | All versions have diff links at bottom | Some missing | No links |
| Duplicate versions | No duplicates | — | Same version appears twice |
| Unreleased section | Present and correctly placed | Missing but otherwise OK | Unreleased below released entries |
| Empty sections | No empty categories | One or two empty headings | Many empty headings |

Report validation results before proceeding:
```
Changelog validation:
  [PASS] Format follows Keep a Changelog standard
  [WARN] Missing comparison links for v1.1.0 and v1.0.0
  [PASS] Versions correctly ordered (newest first)
  [PASS] Dates in ISO 8601 format
```

If issues are found, offer to fix them: "I found 2 issues in the existing CHANGELOG.md. Want me to fix them while adding the new entry?"

---

### Phase 3 — Parse, Categorize, and Group

Read all changes and categorize them. Apply intelligent grouping.

#### Category Rules

Categories follow [Keep a Changelog](https://keepachangelog.com) standard:

| Category | Triggers | Priority |
|---|---|---|
| **Breaking Changes** | `!` in conventional commit type, `BREAKING CHANGE:` in commit body or footer, "BREAKING", removes or renames a public API, changes return format, removes endpoints, changes required parameters, incompatible schema migration | 1 (always first) |
| **Security** | `security`, `CVE-`, `vulnerability`, `auth bypass`, `XSS`, `injection`, `CSRF`, `SSRF`, `exposure`, `advisory`, `patch security`, commits touching auth/security files | 2 |
| **Added** | `feat:`, `feature`, `add`, `implement`, `introduce`, `support for`, `new`, `enable` | 3 |
| **Changed** | `refactor:`, `change`, `update`, `modify`, `improve`, `enhance`, `rework`, `revamp`, `migrate` | 4 |
| **Deprecated** | `deprecate`, `will be removed`, `legacy`, `sunset`, `end of life`, `EOL` | 5 |
| **Removed** | `remove`, `drop support`, `delete`, `eliminate`, `strip`, `prune` | 6 |
| **Fixed** | `fix:`, `fix`, `resolve`, `patch`, `correct`, `repair`, `handle`, `prevent`, `bug` | 7 |
| **Performance** | `perf:`, `faster`, `optimize`, `reduce latency`, `cache`, `improve performance`, `speed up`, `benchmark` | 8 |
| **Dependencies** | `deps:`, `chore(deps):`, `bump`, `upgrade`, `update [package-name]`, `renovate`, `dependabot` | 9 |
| **Documentation** | `docs:`, `readme`, `update docs`, `add documentation`, `JSDoc`, `docstring`, `API docs` | 10 |
| **Internal** | `chore:`, `ci:`, `build:`, `test:`, `style:`, `refactor:` (when purely internal) — include only when audience is contributors | 11 |

#### Grouping Rules

- **Merge related commits into one bullet.** Ten commits for one feature = 1 bullet, not 10.
  Use the first `feat:` commit as the anchor and absorb subsequent `fix:`, `refactor:`, `test:`
  commits that share the same scope or touch the same files.
- **Group dependency updates.** "Updated React (17 → 18.3), TypeScript (4.9 → 5.4), and 12 other dependencies" not 14 separate bullets.
- **Drop noise.** Skip: `wip`, `tmp`, `minor`, `fix typo`, `fix lint`, `update .gitignore`,
  `merge branch`, `Merge pull request`, commits that only touch test infrastructure or CI
  config — unless the audience is contributors.
- **Preserve PR/issue references.** Attach `(#123)` or `(fixes #456)` to the relevant bullet.
- **Detect scope from conventional commits.** `feat(auth): add OAuth` → the bullet goes under
  "Added" with context that it is in the auth module.

#### Diff-Based Change Detection

When commit messages are poor quality (all say "fix", "update", "wip", or similar):

1. **Analyze the actual diff:**
   ```bash
   git diff <range> --stat
   git diff <range> -- <file> (for key files)
   ```

2. **Infer changes from code:**
   - New files → likely new features. Read the file to understand what it does.
   - Deleted files → likely removed features. Check the file name/path for context.
   - Modified files → examine the diff to understand what changed functionally.

3. **Disclose the limitation:**
   Include a note: "Commit messages were minimal — these notes were inferred from code analysis
   and may be incomplete. Review the diff for full accuracy."

---

### Phase 4 — Version Bump Recommendation

If the user has not specified a version number, calculate and recommend one.

#### Semver Rules

| Changes Detected | Bump | Rationale |
|---|---|---|
| Any breaking change | **MAJOR** | `1.x.x → 2.0.0` |
| New features, no breaking changes | **MINOR** | `1.2.x → 1.3.0` |
| Only bug fixes, patches, deps, docs | **PATCH** | `1.2.3 → 1.2.4` |

#### Pre-1.0 Special Rules

- Breaking changes in `0.x.y` bump MINOR (not MAJOR): `0.3.0 → 0.4.0`
- New features in `0.x.y` bump MINOR: `0.3.0 → 0.4.0`
- Bug fixes in `0.x.y` bump PATCH: `0.3.1 → 0.3.2`
- Note: "Pre-1.0 versioning — breaking changes are expected and do not require a major bump."

#### Calendar Versioning

If the project uses calver (detected from tags like `2025.03`, `2026.01.2`):
- Use `YYYY.MM` or `YYYY.MM.PATCH` based on existing convention.
- Increment PATCH within the same month. New month = reset PATCH.

#### Recommendation Format

Present clearly and ask for confirmation:

```
Version recommendation: MINOR release → v1.3.0
  Rationale: 3 new features, 5 bug fixes, no breaking changes.
  Previous version: v1.2.0 (released 2026-02-01, 41 days ago, 47 commits)

Use v1.3.0? Or specify a different version.
```

#### Release Cadence Awareness

When git history is available, calculate and report:
- Days since last release
- Number of commits since last release
- Average release cadence (from last 5 releases)

If the release is unusually large or overdue, note it:
```
Note: This release includes 127 commits over 89 days. Your average release cadence is
every 14 days with ~20 commits. Consider releasing more frequently to reduce risk per release.
```

---

### Phase 5 — Release Readiness Check

Before generating the final changelog, perform a release readiness assessment.
Run these checks automatically when in a git repository:

```bash
# Check for uncommitted changes
git status --porcelain

# Check for TODO/FIXME/HACK in recently changed files
git diff <range> --name-only | head -20
# Then search those files for TODO/FIXME/HACK

# Check for unreleased migrations
ls **/migrations/ db/migrate/ 2>/dev/null | head -5

# Check if tests pass (only suggest, don't run without permission)
ls package.json Makefile Cargo.toml pyproject.toml go.mod 2>/dev/null
```

**Readiness report (include before the changelog outputs):**

```
Release readiness check:
  [PASS] No uncommitted changes
  [WARN] 3 TODO comments found in changed files (auth.ts:45, cart.js:112, api.py:89)
  [PASS] No unreleased database migrations detected
  [INFO] Test suite detected (Jest) — run `npm test` before releasing
  [WARN] Branch is 2 commits behind origin/main — pull before releasing
```

If any checks fail critically (uncommitted changes that should be included, branch divergence),
warn prominently before proceeding.

---

### Phase 6 — Generate Contributor Acknowledgments

For open-source projects or when the user requests it, generate a contributors section.

```bash
# Get unique authors in the range
git log <range> --format='%aN <%aE>' --no-merges | sort -u

# Get co-authors from commit bodies
git log <range> --format='%b' | grep -i 'co-authored-by' | sort -u

# Get GitHub usernames (if remote is GitHub)
git log <range> --format='%aN' --no-merges | sort -u
```

**Auto-detect if open source:**
- Check for LICENSE file
- Check for CONTRIBUTING.md
- Check if the remote URL is a public GitHub repo

**For open-source projects, always include the contributors section.**
**For private/internal projects, include only if the user requests it.**

Format:
```markdown
### Contributors

Thanks to the following people who contributed to this release:

- @username1 — OAuth implementation (#218, #219)
- @username2 — Bug fixes (#227, #231)
- @username3 — Documentation updates (#220)
- @username4 (first-time contributor!) — Safari date picker fix (#219)
```

Rules:
- Map git author names to GitHub usernames when possible (check `git log --format='%aN'`
  against `gh api` if available).
- Highlight first-time contributors (not found in `git log` before the range start).
- Group contributions by what they did, not just list names.
- Include co-authors from `Co-authored-by:` trailers.

---

### Phase 7 — Produce Outputs

Always produce **Output A** (CHANGELOG.md format). Produce other outputs based on context:

| Output | When to Include |
|---|---|
| **A: CHANGELOG.md** | Always |
| **B: GitHub/GitLab Release Notes** | Always (unless user specifies otherwise) |
| **C: Internal/Slack Summary** | Always (unless user specifies otherwise) |
| **D: Email/Newsletter** | When user requests it, or when the project appears to have end users (web app, mobile app, SaaS) |
| **E: Package Registry** | When user requests it, or when `package.json`, `Cargo.toml`, `pyproject.toml`, `setup.py`, or `*.gemspec` is detected |

Separate each output with a clear header.

---

## Output A: CHANGELOG.md (Keep a Changelog Format)

Follows [keepachangelog.com](https://keepachangelog.com) exactly. Suitable for committing
directly to the repository.

```markdown
## [1.3.0] - 2026-03-14

### Breaking Changes
- **Renamed `/api/v1/users` to `/api/v2/users`** — update all API clients before upgrading. The v1 endpoint returns a deprecation warning in this release and will be removed in v2.0.0 (#234)

### Security
- Patched XSS vulnerability in user-generated content rendering (CVE-2026-XXXX) — upgrade immediately if you render user HTML (#233)

### Added
- OAuth2 login with Google and GitHub — click "Continue with Google" on the login page (#218)
- Dark mode support — respects system preference and includes manual toggle in Settings > Appearance (#225)
- Bulk export to CSV for all report types (#229)

### Fixed
- Cart total calculated incorrectly when multiple percentage-based discounts applied simultaneously (#231)
- Session not invalidated after password change — users remained logged in on other devices (#227)
- Date picker showing incorrect month on Safari 17+ due to locale parsing bug (#219)

### Changed
- Upgraded React from 17.0.2 to 18.3.1 — see [React 18 migration guide](https://react.dev/blog/2022/03/08/react-18-upgrade-guide) (#230)
- Improved error messages for all API validation failures — errors now include field name and expected format (#222)

### Deprecated
- `/api/v1/users` endpoint — will be removed in v2.0.0. Migrate to `/api/v2/users` (#234)

### Contributors

Thanks to @alice, @bob, @carol, and @dave (first-time contributor!) for their contributions to this release.

[1.3.0]: https://github.com/owner/repo/compare/v1.2.0...v1.3.0
```

**Rules:**

- One bullet per user-visible change — not one per commit. Group related commits.
- Each bullet: **what** changed + **why it matters** or **what to do** + issue/PR number in parentheses.
- Breaking changes always first. Bold the breaking part if particularly dangerous.
- Security section comes second — these are urgent.
- No bullet for `chore:`, `ci:`, `test:` unless it affects users of the project
  (e.g., a new required dev dependency, a changed build command).
- Dates in ISO 8601 format (YYYY-MM-DD). Use today's date if no release date specified.
- Comparison link at the bottom pointing to the diff on GitHub/GitLab.
  Auto-detect the remote URL. If not detectable, use a template: `https://github.com/OWNER/REPO/compare/...`
- If the project already has a CHANGELOG.md, match its existing style for consistency.
- Include `[Unreleased]` section header if the existing changelog uses one.

**Insertion into existing CHANGELOG.md:**

If the project has an existing CHANGELOG.md:
1. Show the new entry as an insertion, clearly indicating where it goes.
2. Update the `[Unreleased]` comparison link to point from the new version to HEAD.
3. Update or add the new version's comparison link at the bottom.
4. Offer to write the file directly: "Want me to update CHANGELOG.md directly?"

---

## Output B: GitHub / GitLab Release Notes

Friendlier, narrative tone. Goes on the GitHub Releases page. Mix of brief prose and
bullets. Written for end users and adopters, not contributors.

```markdown
## What's new in v1.3.0

### Sign in with Google and GitHub
You can now log in using your Google or GitHub account. Click "Continue with Google" on
the login page — no new password needed. Your existing account is automatically linked
if the email matches.

### Dark mode
The app now respects your system's dark/light mode preference. You can also toggle it
manually in **Settings > Appearance**. All charts, code blocks, and images are optimized
for both modes.

### Bulk CSV export
Export any report to CSV with a single click. Supports all report types including custom
date ranges. Files are generated server-side — no browser timeout on large datasets.

### Bug fixes
- Fixed cart totals being calculated incorrectly when multiple discounts were applied
- Fixed an issue where sessions weren't invalidated after a password change
- Fixed the date picker showing the wrong month on Safari

### Security
- Patched an XSS vulnerability in user-generated content rendering (CVE-2026-XXXX). We recommend upgrading immediately.

### Breaking change
> **API change:** The endpoint `/api/v1/users` has been renamed to `/api/v2/users`.
> If you use our API directly, update your requests before upgrading.
> The old endpoint still works in this release but will be removed in v2.0.0.

### Contributors
Thanks to @alice, @bob, @carol, and @dave for their contributions!

**Full changelog:** [v1.2.0 → v1.3.0](https://github.com/owner/repo/compare/v1.2.0...v1.3.0)
```

**Rules:**

- Lead with the most exciting user-visible change, not the most technically complex.
- Write for end users, not contributors. Hide implementation details.
- Use emoji sparingly — only for section headers if the project style uses them, never inline.
- Breaking changes get a dedicated blockquote callout — never buried in a list.
- Security advisories are prominent with CVE references and a recommendation to upgrade.
- Keep it scannable — someone should understand the whole release in 30 seconds.
- Include "Full changelog" comparison link at the end.
- If the project has previous GitHub releases, match their tone and style.

---

## Output C: Internal / Slack Summary

One-paragraph or brief bullet list for pasting into Slack, Teams, or internal chat.
No technical jargon. Scannable in 5 seconds.

```
v1.3.0 is live

New: Google/GitHub OAuth login, dark mode, CSV bulk export
Fixed: cart discount calculation, session invalidation after password change, Safari date picker
Security: patched XSS in user content rendering (CVE-2026-XXXX)
Breaking: /api/v1/users -> /api/v2/users (update clients before deploying)

47 commits | 5 contributors | 3 features, 3 fixes, 1 security patch

Release notes: <link>
```

**Rules:**

- Maximum 8 lines. If you cannot fit it in 8 lines, the release is too big — see the
  "Large releases" section.
- Use plain text, no markdown formatting (Slack renders it oddly).
- Lead with what matters most to the team (new features, then fixes, then breaking).
- Include a stats line (commits, contributors, change counts).
- End with a link placeholder.

---

## Output D: Email / Newsletter Format

For product teams that send release emails to customers. Professional, benefit-focused,
non-technical language. Include this output when the user requests it or when the project
appears to be a customer-facing application.

```markdown
Subject: What's new in [Product Name] — March 2026

Hi [Customer],

We've been busy! Here's what's new in [Product Name] this month.

---

**Sign in with Google and GitHub**

No more passwords to remember. You can now sign in with your Google or GitHub account in
one click. Your existing data is automatically linked — nothing to migrate.

[Sign in now →](https://app.example.com/login)

---

**Dark mode is here**

We heard you. The app now supports dark mode, either automatically following your system
preference or manually via Settings > Appearance.

---

**Export reports to CSV**

You can now export any report to CSV with a single click — including custom date ranges
and large datasets. Perfect for bringing data into Excel or your BI tools.

---

**Bug fixes and improvements**

- Cart discounts now calculate correctly when multiple promotions are active
- Improved session security after password changes
- Fixed a display issue with the date picker on Safari

---

Questions or feedback? Just reply to this email.

— The [Product Name] Team
```

**Rules:**

- Subject line: product name + month/date, not version number. Customers do not care about v1.3.0.
- Lead with benefits, not features. "No more passwords to remember" not "Added OAuth2 support."
- Include call-to-action links where relevant.
- Group bug fixes into a brief list — do not explain technical details.
- Never mention breaking API changes unless the customer uses the API directly.
  If they do, include a separate section with migration instructions.
- Tone: professional, warm, concise. Not corporate. Not casual.
- No emojis in the email body.

---

## Output E: Package Registry Format

For publishing to npm, PyPI, crates.io, RubyGems, or other package registries.
Include this output when a package manifest is detected or the user requests it.

### npm (package.json)

```json
{
  "version": "1.3.0"
}
```

And the npm release notes (goes in `npm publish` or GitHub release that npm links to):

```markdown
## 1.3.0 (2026-03-14)

### Breaking Changes
* `/api/v1/users` renamed to `/api/v2/users` (#234)

### Features
* OAuth2 login with Google and GitHub (#218)
* Dark mode support (#225)
* Bulk CSV export for all report types (#229)

### Bug Fixes
* Cart total incorrect with multiple discounts (#231)
* Session not invalidated after password change (#227)
* Date picker wrong month on Safari (#219)
```

### PyPI (pyproject.toml / setup.py)

```toml
[project]
version = "1.3.0"
```

### Cargo (Cargo.toml)

```toml
[package]
version = "1.3.0"
```

### RubyGems (*.gemspec)

```ruby
spec.version = "1.3.0"
```

**Rules:**

- Show the version bump for the detected package manager.
- Format release notes in the style conventional for that ecosystem.
- npm uses `*` bullets and `### Features` / `### Bug Fixes` (conventional-changelog style).
- PyPI uses restructuredText or Markdown depending on project config.
- Cargo uses markdown in the GitHub release (crates.io links to it).
- Include only the version string change — do not rewrite the whole manifest.
- Offer to update the version in the manifest file directly.

---

## Writing Quality Rules

Apply these transformations to every raw commit message. Every bullet must meet this standard.

### Transformation Examples

| Raw Commit | Good Changelog Bullet |
|---|---|
| `fix: cart bug` | Fixed cart total calculated incorrectly when multiple percentage-based discounts applied simultaneously |
| `feat: dark mode` | Added dark mode — respects system preference with manual override in Settings > Appearance |
| `chore: upgrade deps` | Updated React (17.0.2 → 18.3.1), TypeScript (4.9 → 5.4), and 8 other dependencies |
| `fix: #234` | (Look up the issue/PR. If inaccessible, write "Fixed issue #234" as fallback.) |
| `wip` / `tmp` / `minor fix` | Skip, or group multiple into "Various minor improvements and stability fixes" |
| `feat!: new API` | **Breaking:** Renamed `/api/v1` to `/api/v2` — update all API clients before upgrading |
| `perf: optimize query` | Improved dashboard load time by 60% by optimizing the main analytics query |
| `security: patch CVE-2026-1234` | **Security:** Patched authentication bypass vulnerability (CVE-2026-1234) — upgrade immediately |
| `refactor: extract service` | (Skip in user-facing notes. Include in contributor changelog if requested.) |
| `ci: fix deploy` | (Skip entirely unless it affects the release process.) |

### Bullet Writing Rules

1. **User/developer perspective**, not implementer perspective.
   - Bad: "Refactored cart module to use reducer pattern"
   - Good: "Fixed cart total calculated incorrectly when multiple discounts applied"

2. **Start with past-tense verb:** Added, Fixed, Removed, Improved, Updated, Changed, Deprecated, Secured.

3. **Include what changed AND what it means for users:**
   - Bad: "Added OAuth2 support"
   - Good: "Added OAuth2 login with Google and GitHub — click 'Continue with Google' on the login page"

4. **Merge commits that form one feature.** 10 commits building the same feature = 1 bullet.

5. **Quantify when possible.** "Improved load time by 40%" not "Improved performance."

6. **Drop purely internal commits** from user-facing outputs. Keep them in contributor changelogs.

7. **Breaking changes must include migration instructions:**
   - Bad: "Changed API endpoint"
   - Good: "Renamed `/api/v1/users` to `/api/v2/users` — update all API clients. The old endpoint returns a deprecation warning and will be removed in v2.0.0"

8. **Security fixes must include severity signal:**
   - Bad: "Fixed security issue"
   - Good: "Patched XSS vulnerability in user-generated content rendering (CVE-2026-XXXX) — upgrade immediately if you render user HTML"

---

## Special Scenarios

### Hotfix Releases

Lead with the bug that was fixed, its severity, and who is affected:

```markdown
## [1.2.1] - 2026-03-14

### Security
- **Critical:** Patched authentication bypass that allowed unauthenticated access to user
  data when using OAuth login. All users of v1.2.0 with OAuth enabled should upgrade
  immediately. (#241)
```

For the Slack summary:
```
URGENT: v1.2.1 hotfix released

Patched critical auth bypass in OAuth login (v1.2.0 affected).
All instances with OAuth enabled must upgrade immediately.

Changelog: <link>
```

### Large Releases (50+ Changes)

Do not produce a 60-item list. Group under functional themes:

```markdown
## [2.0.0] - 2026-03-14

This is a major release with significant changes across the platform.

### Authentication & Security
- Added OAuth2 login with Google and GitHub (#218)
- Added two-factor authentication via TOTP (#240)
- Patched 3 security vulnerabilities (see Security section)

### Dashboard & Reporting
- Redesigned analytics dashboard with real-time updates (#215)
- Added bulk CSV export for all report types (#229)
- Improved chart rendering performance by 3x (#232)

### API (Breaking Changes)
- **Renamed all v1 endpoints to v2** — see [migration guide](link) (#234)
- **Changed authentication from API keys to OAuth tokens** (#238)
- Added rate limiting: 1000 req/min for authenticated, 100 for anonymous (#236)

### Bug Fixes
- Fixed 12 bugs across cart, checkout, and payment modules (see full list below)

<details>
<summary>All bug fixes (12)</summary>

- Fixed cart total with multiple discounts (#231)
- Fixed session invalidation (#227)
- ...
</details>
```

### First Release / Initial Commit

```markdown
## [1.0.0] - 2026-03-14

Initial release.

### Features
- User authentication with email/password and OAuth (Google, GitHub)
- Dashboard with real-time analytics
- Report generation with CSV/PDF export
- REST API with comprehensive documentation
- Role-based access control (admin, editor, viewer)
```

### Pre-release Versions

For alpha, beta, RC releases:

```markdown
## [2.0.0-beta.1] - 2026-03-14

> This is a pre-release. APIs may change before the stable 2.0.0 release.
> Do not use in production.

### Added
- [Beta] New dashboard layout (#250)
- [Beta] GraphQL API alongside REST (#252)
```

### Backport / Maintenance Releases

When a fix is backported to an older major version:

```markdown
## [1.2.5] - 2026-03-14

Maintenance release for the v1.x series. Backported security fix from v2.1.0.

### Security
- Patched XSS vulnerability in content rendering (CVE-2026-XXXX) — same fix as v2.1.0 (#260)
```

---

## i18n — Multilingual Changelogs

When the user requests changelogs in multiple languages, or when the project has an
international audience:

1. **Generate the canonical changelog in English first** (this is the source of truth).
2. **Translate to requested languages,** maintaining technical accuracy:
   - Keep technical terms (API names, function names, package names) untranslated.
   - Keep version numbers, dates, and PR/issue references identical.
   - Adapt tone to the target language's conventions (e.g., formal "vous" in French,
     polite form in Japanese).
3. **File naming convention:**
   - `CHANGELOG.md` — English (default)
   - `CHANGELOG.pt-BR.md` — Portuguese (Brazil)
   - `CHANGELOG.es.md` — Spanish
   - `CHANGELOG.ja.md` — Japanese
   - `CHANGELOG.zh-CN.md` — Chinese (Simplified)

4. **For GitHub releases:** Offer to include a translated summary in the release body
   below the English version, separated by a language header.

Supported languages: translate to any language the user requests. Common requests include
Portuguese (pt-BR), Spanish (es), French (fr), German (de), Japanese (ja), Chinese (zh-CN),
and Korean (ko).

---

## Automated File Update

After generating all outputs, always offer to directly update project files:

```
---
Ready to update your project? I can:
  [1] Write/update CHANGELOG.md with the new entry
  [2] Create the GitHub release (gh release create v1.3.0 --notes "...")
  [3] Bump the version in package.json / pyproject.toml / Cargo.toml
  [4] Generate all files for a monorepo release
  [5] Create a release commit ("chore: release v1.3.0") and tag
  [6] All of the above

Which would you like?
```

**When the user accepts:**

1. **CHANGELOG.md update:** Use the Edit tool to insert the new entry at the correct position.
   If the file does not exist, create it with proper Keep a Changelog header:
   ```markdown
   # Changelog

   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
   and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

   ## [Unreleased]

   ## [1.3.0] - 2026-03-14
   ...
   ```

2. **GitHub release:** Use `gh release create` with the Output B content.

3. **Version bump:** Update the version string in the detected manifest file(s).

4. **Release commit and tag:**
   ```bash
   git add CHANGELOG.md package.json  # or equivalent
   git commit -m "chore: release v1.3.0"
   git tag -a v1.3.0 -m "v1.3.0"
   ```
   Always ask before pushing.

---

## Edge Cases

### No Tags in Repository

```bash
git tag --sort=-v:refname | head -1
# (empty)
```

Fall back to:
1. Ask the user: "No git tags found. What was the previous version, or is this the first release?"
2. If first release, generate a v1.0.0 (or v0.1.0) initial changelog.
3. If the user provides a previous version, use the full commit history or a commit range they specify.

### Detached HEAD / CI Environment

If `git` commands fail because of a shallow clone or detached HEAD:
```bash
# Try to fetch tags
git fetch --tags 2>/dev/null

# Try unshallow if needed
git fetch --unshallow 2>/dev/null
```

If still unable to get history, work with whatever input the user provides.

### Empty Diff / No Changes

If no changes are found between the specified versions:
"No changes detected between v1.2.0 and HEAD. Are you on the right branch? Or specify the range manually."

### Squash-Merged PRs

When the project uses squash merging, each commit represents one PR. Use `gh pr list --state merged`
or parse the squash commit messages (which typically include the PR title and number) for richer context.

### Revert Commits

When a `revert:` or "Revert " commit is found:
- If the original commit is also in the range, **cancel both out** — neither appears in the changelog.
- If only the revert is in the range, list it as a change: "Reverted [description] due to [reason if stated]."

### Commit Message in Non-English Languages

Detect the language of commit messages. If they are not in English:
- Parse them in their original language for categorization.
- Write the changelog in the language the user requests (default: English).
- If translating, note: "Changelog translated from [language] commit messages."

---

## Version String Handling

Detect and handle all common version formats:

| Format | Example | Handling |
|---|---|---|
| Semver | `1.2.3`, `v1.2.3` | Standard semver bump rules. Match `v` prefix convention. |
| Semver with pre-release | `1.2.3-beta.1`, `2.0.0-rc.1` | Increment pre-release suffix. |
| Calendar versioning | `2026.03`, `2026.03.1` | Use current date. Increment patch within month. |
| Build number | `build 1042`, `b1042` | Increment build number. |
| Codename + semver | `v3.0.0 "Orion"` | Keep codename in release notes, suggest also bumping semver. |
| Date-based | `20260314` | Use current date. |

If the user has not decided on the version number yet:
"I'd suggest **v1.3.0** for this release (3 new features, no breaking changes). Want to use a different version?"

---

## Format Reference

### Date Format
Always ISO 8601: `YYYY-MM-DD`. Today is `2026-03-14`.

### Link Format

Auto-detect from `git remote get-url origin`:

| Host | Comparison Link Format |
|---|---|
| GitHub | `https://github.com/OWNER/REPO/compare/v1.2.0...v1.3.0` |
| GitLab | `https://gitlab.com/OWNER/REPO/-/compare/v1.2.0...v1.3.0` |
| Bitbucket | `https://bitbucket.org/OWNER/REPO/branches/compare/v1.3.0..v1.2.0` |
| Azure DevOps | `https://dev.azure.com/ORG/PROJECT/_git/REPO/branchCompare?baseVersion=GTv1.2.0&targetVersion=GTv1.3.0` |
| Unknown | `https://HOSTNAME/OWNER/REPO/compare/v1.2.0...v1.3.0` (template) |

### Issue/PR Link Format

When including issue/PR references:
- GitHub: `(#123)` — GitHub auto-links these in release notes.
- GitLab: `(!123)` for MRs, `(#123)` for issues.
- Jira: `(PROJ-123)` — include the full key.

---

## Configuration Respect

If the project has any of these configuration files, respect their settings:

| File | What to Respect |
|---|---|
| `.versionrc`, `.versionrc.json` | `standard-version` / `commit-and-tag-version` config — section ordering, header, types |
| `cliff.toml` | `git-cliff` config — commit parser, groups, template |
| `.releaserc`, `release.config.js` | `semantic-release` config — branch, plugins, changelog options |
| `.changeset/config.json` | Changesets config — linked packages, changelog format |
| `lerna.json` | Lerna versioning mode (fixed vs independent) |
| `CHANGELOG` section in `package.json` | Custom changelog config |

When these exist, read them and align output with the project's configured release tooling.
Note: "Detected `semantic-release` configuration — formatting changelog to match its conventions."

---

## Final Checklist

Before presenting the output, verify:

- [ ] Every breaking change is explicitly called out and appears first
- [ ] Every security fix includes severity indication and CVE if available
- [ ] Every bullet starts with a past-tense verb
- [ ] No raw commit hashes appear in the user-facing text (only PR/issue numbers)
- [ ] Comparison links are correctly formatted for the detected hosting platform
- [ ] Date is in ISO 8601 format
- [ ] Version number follows the project's existing convention (with or without `v` prefix)
- [ ] Related commits are merged into single bullets (no duplicates)
- [ ] Internal/noise commits are excluded from user-facing outputs
- [ ] Monorepo: each package's changes are correctly attributed
- [ ] Outputs are ready to paste with zero editing required
