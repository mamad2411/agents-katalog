---
name: consolidate-changelogs
description: Consolidate open changelog PRs into a single PR, filtering out non-user-facing changes
disable-model-invocation: true
argument-hint: [optional: PR numbers to include, or "all" for all open changelog PRs]
---

# Consolidate Changelog PRs

Combine open changelog entry PRs into a single reviewable PR. Filter out entries that aren't meaningful to users.

## Step 1: Gather open changelog PRs

```bash
gh pr list --state open --json number,title,headRefName,body --limit 50
```

Filter to PRs whose branch matches `changelog/v*`. These are auto-generated changelog PRs.

## Step 2: Fetch changelog content from each PR branch

For each changelog PR, extract the actual markdown file from the remote branch:

```bash
git show "origin/<branch>:<changelog-file-path>"
```

The changelog files live at `src/content/changelog/` and are named `YYYY-MM-DD-vX-Y-Z.md`.

## Step 3: Filter out non-user-facing entries

**Remove entries that are purely backend/infrastructure with no user-visible impact:**

- Test coverage changes (regression tests, unit tests, CI fixes)
- Internal refactors that don't change behavior
- Asset/dependency swaps that don't affect what users see (e.g. switching to local fonts for CSP compliance)
- Internal component renames or code reorganization
- Build system or tooling changes

**Remove entries that describe implementation plumbing rather than user outcomes:**

- Adding internal components (e.g. "Added BuildingOverlay component") when later entries describe what users actually see
- API or data model changes with no UI impact
- Internal architecture changes

**Keep entries that describe things users can see, do, or experience:**

- New features and capabilities
- UI changes (new screens, layouts, navigation)
- Removed features or UI elements
- New interactions or workflows
- AI/agent behavior changes visible to users
- Performance improvements users would notice

**Present the list of entries you plan to remove and why, so the user can coach you before you proceed.**

## Step 4: Write changelog files

For each kept entry, create a markdown file in `src/content/changelog/` following this format:

```markdown
---
version: 'X.Y.Z'
date: 'YYYY-MM-DD'
prNumber: NNN
prUrl: 'https://github.com/sociotechnica-org/lifebuild/pull/NNN'
---

# vX.Y.Z

- User-facing description of the change
```

Do NOT include "View PR" links in the markdown content — PR links are rendered separately by the updates page using the frontmatter `prNumber` and `prUrl` fields.

File naming: `YYYY-MM-DD-vX-Y-Z.md` (use the date from the original entry, dashes instead of dots in version).

### Writing style for changelog entries

Write entries from the user's perspective. Describe what changed for them, not what code changed.

- Good: "The Life Map is now a full-bleed hex map that fills the entire screen"
- Bad: "Refactored HexMap component to use full-viewport CSS"
- Good: "Jarvis now guides a real conversation at the campfire during onboarding"
- Bad: "Integrated LLM streaming into CampfireScene component"

Entries can include:

- Bullet points for multiple related changes
- Narrative descriptions for major features
- Screenshots or GIFs (as markdown images) when they help illustrate the change
- Bold text for emphasis

Keep entries concise but descriptive. One to three bullet points per version is typical.

## Step 5: Update version.json

Update `src/data/version.json` with the highest version number from the kept entries and today's date:

```json
{
  "version": "X.Y.Z",
  "lastUpdated": "YYYY-MM-DD"
}
```

## Step 6: Lint, commit, and create PR

1. Run `npm run lint-all`
2. Stage all new/modified files
3. Commit with message: `Changelogs: vX.Y.Z through vX.Y.Z`
4. Push and create a PR with:
   - Title: `Changelogs: vX.Y.Z through vX.Y.Z`
   - Body listing all included entries
   - **Important:** Include `Closes #N` for every original changelog PR in the body. This ensures merging the combined PR auto-closes and links all the individual PRs it supersedes. Use the format `Closes #75, #76, #77, ...` in the body.
5. Report what was included and what was filtered out

## Changelog file format reference

- Frontmatter fields: `version`, `date`, `prNumber`, `prUrl`
- The `# vX.Y.Z` heading is hidden on the updates page (CSS `display: none`)
- Do NOT include `[View PR]` links in markdown — PR links are rendered from frontmatter
- Entries are grouped by date on the updates page, with the highest version as the group header
- Inline links in changelog content (e.g. linking to a URL like playground.lifebuild.me) are supported and styled
