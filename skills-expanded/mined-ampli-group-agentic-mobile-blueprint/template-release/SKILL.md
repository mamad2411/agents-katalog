---
name: template-release
description: Cut a new template version — bump TEMPLATE_VERSION, write upgrade notes, tag and publish a GitHub release. Use when releasing a new version of the agentic-mobile-blueprint template.
---

# Release Process

This template uses **semver** (`MAJOR.MINOR.PATCH`) for tracking purposes only.
CI/CD pipelines are not gated on version tags — they trigger on merges to `main`.

| Bump | When |
|------|------|
| **PATCH** (0.1.x) | Bug fixes, security patches, dependency updates — no API or skill changes |
| **MINOR** (0.x.0) | New features, new skills, new integrations — backwards-compatible |
| **MAJOR** (x.0.0) | Breaking changes to file structure, API contracts, or required env vars |

---

## Step 1 — Decide the next version

1. Read `TEMPLATE_VERSION` to get the current version.
2. Review changes since the last tag:
   ```bash
   git log $(git describe --tags --abbrev=0)..HEAD --oneline
   git diff $(git describe --tags --abbrev=0)..HEAD --stat
   ```
3. Apply the semver rules above to pick `MAJOR.MINOR.PATCH`.

## Step 2 — Write upgrade notes

Create `.agents/skills/template-upgrade/vMAJOR.MINOR.PATCH.md` using the template below.
Every section is required. Use "None" for empty sections — never omit them.

### What belongs in upgrade notes

Only document changes that consuming projects can and should pull in:

| Include | Exclude |
|---------|---------|
| `supabase/functions/_shared/` utilities | `mobile/app/` screens and components |
| `.agents/skills/` (new or updated skills) | `maestro/` YAML test flows |
| `supabase/migrations/` shared schema | Example / demo screens |
| Build config (`eas.json`, `app.json` keys) | Any file a project is expected to replace |
| New required env vars | Internal refactors with no consumer impact |
| Dependency version bumps | |
| `AGENTS.md` changes agents should adopt | |

**Rule of thumb:** if a project that forked this template has almost certainly replaced the file already, do not mention it.

```markdown
# vMAJOR.MINOR.PATCH — <one-line summary>

Released: YYYY-MM-DD

## Breaking Changes

<!-- What existing projects MUST change before upgrading. -->
<!-- Format: "**`path/to/file`** — what changed and why" -->

None

## New Features

<!-- New shared skills, utilities, or integrations. -->
<!-- Do NOT include app-scaffold additions (screens, demo flows, etc.). -->

None

## Improvements

<!-- Reliability, performance, or DX improvements to shared infrastructure. -->

None

## Bug Fixes

<!-- Defects corrected in shared code. -->

None

## Dependency Updates

<!-- Package version bumps worth noting. -->

None

## Upgrade Instructions

Step-by-step for a project that already uses a previous version of this template.

1. Copy changed shared files / snippets as described in each section above.
2. Update any env vars listed under Breaking Changes.
3. Run `mise run configure` if new env vars were added.
```

## Step 3 — Bump TEMPLATE_VERSION

Update the `TEMPLATE_VERSION` file (single line, no `v` prefix):

```bash
echo "MAJOR.MINOR.PATCH" > TEMPLATE_VERSION
```

## Step 4 — Commit and tag

Stage everything, commit, then create an annotated tag:

```bash
git add TEMPLATE_VERSION .agents/skills/template-upgrade/vMAJOR.MINOR.PATCH.md
git add -A   # any other changed files in the release
git commit -m "release: vMAJOR.MINOR.PATCH"
git tag -a vMAJOR.MINOR.PATCH -m "vMAJOR.MINOR.PATCH — <one-line summary>"
git push origin main --follow-tags
```

## Step 5 — Publish GitHub release

```bash
gh release create vMAJOR.MINOR.PATCH \
  --title "vMAJOR.MINOR.PATCH — <one-line summary>" \
  --notes-file .agents/skills/template-upgrade/vMAJOR.MINOR.PATCH.md
```

---

## Rules

- **Never skip the upgrade notes.** Projects forking this template rely on them to know what to pull in.
- **Upgrade notes cover shared infrastructure only.** App scaffold files (`mobile/app/`, example screens, demo Maestro flows) are replaced by consuming projects — never mention them in upgrade notes.
- **Never force-push a tag.** Create a new patch release instead.
- **One release per PR.** Do not bundle multiple feature sets into a single release if they serve different purposes — prefer smaller, focused releases.
- The `TEMPLATE_VERSION` file is the single source of truth. Do not derive the version from `package.json` or any other file.
