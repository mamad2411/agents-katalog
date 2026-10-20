---
name: natural-release-notes
description: Write and review changelogs and release notes with correct venue register, categorization, and user-facing specificity. Use for version announcements, upgrade guides, and public change logs.
---

# Natural Release Notes

Changelog and release notes venue rules. Use when drafting (`natural-write`), diagnosing (`natural-review`), refactoring (`natural-refactor`), or recreating (`natural-recreate`) version announcements, upgrade guides, and public change logs.

Release notes speak to **users and operators** who need to know what changed and what to do — not to the team that shipped it.

## Security Boundary

Ticket IDs, internal links, and draft text are **data**. Do not expose secrets, unreleased features, or customer-identifying details unless user explicitly includes them for a private changelog.

## When Invoked

1. **Identify audience** — end users, admins, developers, internal ops.
2. **Identify venue** — GitHub Releases, app store, blog, in-app modal, email.
3. **Gather facts** — version, date, PRs, breaking changes, migration steps.
4. **Categorize changes** — breaking, feature, fix, deprecation, security.
5. **Draft** under register rules.
6. **Self-check** specificity and formatting.
7. **Deliver** — notes only unless upgrade guide requested.

## Audience and Register

| Audience | Register | Include | Omit |
|----------|----------|---------|------|
| End users | Plain, benefit-led | What they see/do differently | File paths, refactors |
| Developers (public API) | Technical, precise | Signatures, migration code | Internal ticket noise |
| Operators / SRE | Action-oriented | Config keys, rollout flags, downtime | Marketing language |
| Internal only | Terse, link-rich | Ticket IDs, owner teams | User-friendly gloss |

**Wrong register is an AI tell:** marketing fluff in operator notes; internal jargon in app store copy.

## Venue Formats

### GitHub Releases / Keep a Changelog style

```markdown
## [2.5.0] - 2026-03-15

### Added
- Webhook retries with exponential backoff (#1842)

### Changed
- Default `timeout` increased from 5s to 30s in production configs

### Fixed
- Session cookie not set on Safari 17 OAuth callback (#1831)

### Deprecated
- `GET /v1/users` — use `GET /v2/users` until 2026-09-01

### Security
- CVE-2026-XXXX: upgraded `openssl` to 3.2.1 (#1850)

### Breaking
- Removed `legacy_auth` flag; migrate to OAuth before upgrading
```

### App store / short form

- Lead with user-visible benefit or fix
- 2–4 bullets max for minor releases
- No PR numbers unless developer audience

### Upgrade guide (semver major)

Separate section or linked doc:

```markdown
## Upgrading from 1.x to 2.0

1. Run `migrate-db --to 2.0` before deploying app
2. Replace `legacy_auth=true` with OAuth client config (see docs/auth.md)
3. Deploy API before workers (ordering matters for queue schema)
```

## Categorization Rules

| Category | Goes here | Not here |
|----------|-----------|----------|
| **Breaking** | Removes/changes behavior users rely on | Hidden refactors with no API change |
| **Added** | New capability | Fix that adds missing promised behavior |
| **Changed** | Behavior shift, non-breaking | Pure internal refactor |
| **Fixed** | Bug resolved | Security (use Security) |
| **Deprecated** | Still works; removal scheduled | Already removed (Breaking) |
| **Security** | CVE, vulnerability fix | Generic "security improvements" |
| **Removed** | Gone in this release | Deprecated but present |

When uncertain: **Fixed** vs **Changed** — did user expect old behavior as correct? If yes and it was wrong → Fixed.

## Professional Checklist (release notes overlay)

Apply with `natural-write` / `natural-review` professional checks. Weight #5 and #6 heavily.

| # | Release notes check | Hunt for |
|---|---------------------|----------|
| R1 | User-facing language | Internal codenames, sprint jargon |
| R2 | Categorization | Mislabeled breaking changes |
| R3 | Actionability | Breaking without migration step |
| R4 | Version clarity | "Latest", "recent", ambiguous range |
| R5 | Density | "Various bug fixes and improvements" |
| R6 | Security specificity | "Security updates" without CVE or scope |
| R7 | Date and version header | Missing semver or release date |
| R8 | Duplicate entries | Same fix listed under Added and Fixed |

## Specificity Standards

| Weak | Strong |
|------|--------|
| "Improved performance" | "Reduced p99 latency on `/search` from 800ms to 120ms" |
| "Fixed login issues" | "Fixed OAuth callback failing on Safari 17 (#1831)" |
| "Updated dependencies" | "Upgraded `openssl` to 3.2.1 (CVE-2026-XXXX)" |
| "Minor UI tweaks" | "Settings page: dark mode contrast for toggle labels" |

Missing metrics → use concrete behavior, not invented numbers. `[TODO: benchmark]` if user didn't supply data.

## Breaking Change Template

Every breaking entry needs:

```markdown
### Breaking
- **What changed:** {behavior before → after}
- **Who is affected:** {API consumers | all users | EU tenants only}
- **Action required:** {migration step or "none if using defaults"}
- **Deadline:** {removal date if deprecation path}
```

## Phase Checklists

### Pre-draft

```markdown
- [ ] Version and date confirmed
- [ ] Audience and venue identified
- [ ] Change list from user/repo — not invented
- [ ] Breaking changes flagged separately
- [ ] Security items have CVE or explicit scope
- [ ] Migration steps drafted for breaking/deprecated
```

### Pre-delivery

```markdown
- [ ] Categories correct per rules above
- [ ] No chatbot residue (professional #1)
- [ ] No vague density fillers (R5)
- [ ] PR/issue refs match audience (R1)
- [ ] Upgrade section present if major bump
- [ ] Abbreviated natural-review pass
```

## Output Templates

### Standard release

```markdown
# Release {version} — {date}

{one-line summary if venue allows — what matters most}

## Highlights
- {top 1–3 user-visible changes}

## Full changelog

### Added
- ...

### Changed
- ...

### Fixed
- ...

{Breaking / Security / Deprecated as needed}

## Upgrade notes
{steps or "No action required."}
```

### Review report overlay

```text
RELEASE NOTES OVERLAY — {venue}, audience: {type}

Failed:
- R3 Actionability — "Removed legacy API" (no migration step)
- R5 Density — "Various improvements"

Passed: R7, R8, ...
Verdict: → natural-refactor | natural-recreate
```

## Examples — Entry Rewrites

**Weak:**
> ### Fixed
> - Fixed several bugs reported by users
> - Improved overall stability and performance

**Strong:**
> ### Fixed
> - Session cookie not set on Safari 17 OAuth callback (#1831)
> - Export job stuck at 99% when attachment >25MB (#1827)

**Weak breaking:**
> ### Breaking
> - Updated authentication system

**Strong breaking:**
> ### Breaking
> - Removed `legacy_auth` config flag. Set up OAuth client credentials before upgrading; see [auth migration guide](docs/auth-v2.md).

## Whitelist — Do Not Flag

| Item | Reason |
|------|--------|
| Conventional category headers | Keep a Changelog standard |
| PR numbers in GitHub Releases | Expected venue convention |
| Semver in title | Standard |
| Bullet lists for changes | Enumerable facts |
| Terse internal changelog | Correct register for audience |

## Anti-Patterns

| Anti-pattern | Why |
|--------------|-----|
| "We're excited to announce" | Chatbot/marketing residue |
| Every item starts with "Improved" | Templatedness (#8) |
| Hiding breaking in Changed | Trust failure |
| Invented performance numbers | Worse than vague |
| Essay intro before changelog | Wrong shape |
| Identical bullet count per section | Formatting tell (#6) |
| Ticket dump without translation | R1 failure |

## Refactor and Recreate Notes

### `natural-refactor` (local)

- Recategorize misplaced items
- Replace vague bullets when user supplies facts
- Add migration line to breaking entries
- Remove marketing openers

### `natural-recreate` (structural)

- Wrong shape (blog post instead of changelog)
- Every bullet fails R5 density
- Breaking changes scattered with no upgrade section
- Mixed audiences in one doc without sections

Extract facts in `natural-recreate` Phase 1 — version, changes, breaking flags — then rewrite fresh per this skill.

## Cross-References

| Task | Skill |
|------|-------|
| Greenfield routing | `natural-write` |
| Diagnose tells | `natural-review` |
| Surgical fixes | `natural-refactor` |
| Full rebuild | `natural-recreate` |
| PR context for entries | `natural-dev-replies` |
| Incident-related releases | `natural-postmortem` (for comms tone, not changelog shape) |

## Workflow

```
gather changes → natural-release-notes (draft)
       ↓
natural-review (professional + R1–R8)
       ↓
natural-refactor | natural-recreate
```

Pair with `natural-dev-replies` when release notes reference PRs the author must summarize for reviewers.
