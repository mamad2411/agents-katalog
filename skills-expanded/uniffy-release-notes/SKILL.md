---
name: uniffy-release-notes
description: Draft or publish concise, categorized Uniffy release notes, verified against commit diffs and shipped behavior. Use when asked for release notes, a release log, a version changelog, or replacement GitHub release notes. Skip for PR descriptions or creating release tags.
---

# Uniffy release notes

Write release notes for `uniffy-io/uniffy` from changes that shipped. Commit subjects and PR descriptions are clues, not evidence of scope or behavior. One commit can contain several unrelated changes, and one feature can span several commits.

## Establish release range

Use refs supplied by user. If target is omitted, resolve latest published stable GitHub release and state that choice. If request is explicitly for upcoming work, resolve `HEAD`. Ask only when request does not establish which of these is intended.

Fetch missing history and tags without overwriting local tags. Resolve target and base to immutable commit SHAs and record both. Read code at those SHAs rather than assuming working tree matches release.

Unless user supplies base, choose highest earlier stable version whose published release tag is an ancestor of target. Compare numeric version components, not tag names lexically or creation dates. Exclude drafts and release candidates from base selection. Both candidate and stable notes normally cover changes since previous stable release, so promoting a candidate does not hide its features. Paginate GitHub release and commit lists when needed.

Confirm base is an ancestor of target. For an actual first release, inspect target history and describe initial shipped capabilities. If a base cannot be found because history or GitHub access is incomplete, report that gap instead of treating it as first release. Never silently widen an explicit range.

## Build evidence from code

Inventory every commit and changed path in range. Useful commands, with resolved SHAs in `base` and `target`:

```bash
git log --reverse --format='%H %s' "$base..$target"
git diff --find-renames --stat "$base" "$target"
git diff --find-renames --name-status "$base" "$target"
git show --format=fuller --find-renames "$commit" -- "$path"
git show "$target:$path"
```

Read patches and relevant surrounding code for each affected area. Inspect tests, migrations, configuration and public docs to establish what changed and who experiences it. Read linked PRs or issues for intent when useful, then verify claims against code. Do not turn test names into claims that tests passed.

Inspect merge resolutions as well as ordinary commits. Use first-parent merge diffs when needed, but count merged work once. Review large changes in bounded path groups; do not summarize only first page of commits or truncated patches. Check final base-to-target diff and target code to exclude reverted work, superseded behavior and unfinished wiring.

Maintain evidence table with these columns:

| Change | Product area and audience | Before and after | Supporting commits and paths | Include or omit, with reason |
| --- | --- | --- | --- | --- |

Account for every commit through one or more changes, or an explicit omission such as internal cleanup with no user impact. Split a broad commit across real outcomes. Combine related commits into one outcome. Every published claim must map to evidence. Keep uncertain claims in analysis with their open questions instead of presenting them as shipped facts.

For example, a commit titled `cleanup` might fix note search and add file previews. After checking code, put note search under Bug fixes and file previews under Enhancements, with product-area prefixes. A later commit that adjusts preview loading belongs with same Files outcome. Neither commit title dictates release structure.

## Format release notes

Start body with `### Uniffy Release x.x.x`, substituting target version without leading `v` and retaining any prerelease suffix. Immediately follow with one paragraph of exactly two short sentences summarizing most important shipped changes. Keep summary concrete and grounded in same evidence as detailed bullets. Then write `Released on YYYY-MM-DD.` using verified publication date, or `Unreleased.` until date is established. Place all other sections after this introduction.

Use level-three headings by change type in this order, including only sections supported by shipped changes:

- `Breaking changes`: incompatible behavior, changed defaults requiring action, removed support or migration requirements. State affected audience and required action. Add a short paragraph or code example beneath a bullet when needed.
- `Enhancements`: new stable capabilities and improvements to existing behavior.
- `Preview features`: explicitly experimental or opt-in capabilities. State availability and enablement requirements. A release-candidate tag alone does not make its features preview-only.
- `Bug fixes`: concrete failures corrected in this release.
- `Performance`: verified improvements with affected operation and conditions. Include numbers only when backed by measurements.
- `Documentation`: meaningful changes to user or operator guidance.
- `Contributors`: verified human contributors to changes in this release.

Use `[Notes]`, `[Files]`, `[Chat]`, `[Mobile]`, `[Administration]` or `[Deployment]` at start of bullets when area helps readers scan. Group related areas within each section. Product areas are bullet prefixes, not separate top-level sections. Put each outcome in one section; a breaking change does not need duplicate enhancement and fix entries.

Write one concise bullet per outcome, beginning with a concrete verb after optional area prefix. End with linked PR number in parentheses. If no PR exists, link supporting commit using short SHA. Verify links belong to release range; never guess PR numbers from nearby commits. Combine source links when several PRs deliver one outcome. If source lookup is unavailable, report gap with draft instead of inventing links.

Illustrative syntax only, with placeholders replaced by verified release facts:

```markdown
### Enhancements

- [Files] Add previews for supported image attachments ([#<pr>](https://github.com/uniffy-io/uniffy/pull/<pr>))

### Bug fixes

- [Notes] Fix search results disappearing after title changes ([#<pr>](https://github.com/uniffy-io/uniffy/pull/<pr>))
```

Resolve contributors from public PR and commit metadata for included changes. Deduplicate accounts, exclude bots and list linked handles alphabetically as `[@handle](https://github.com/handle)` bullets. Omit section if no human accounts can be verified. Never infer GitHub usernames from names or email addresses, or expose private email addresses.

End change list with `**Full Changelog**: [<base>...<target>](https://github.com/uniffy-io/uniffy/compare/<base>...<target>)` for bounded ranges. Use actual refs and URL-encode them when necessary. For first release without base, omit comparison.

## Write for users and operators

Combine backend and frontend work when they deliver one feature. Name affected platform or audience when behavior differs. Prefer compact entries over feature essays or marketing summaries.

Lead with meaningful capabilities and fixes. Explain concrete behavior and benefit. For fixes, say what failed and what works now. Include migration steps, changed defaults, compatibility breaks and required operator action prominently when code or shipped docs establish them. Check both cloud and self-hosted implications where relevant.

Keep internal refactors, dependency churn and CI work out unless they have meaningful user, security or operational impact. Mention only supported impacts. Do not invent performance numbers, claim complete feature coverage from partial changes, or advertise capabilities that are disabled or unavailable in target release without explaining their limits.

Use short sentences. No emojis, long dashes, filler, raw commit dumps or empty `No changes` sections. Keep internal plans, evidence paths and undisclosed security findings out of public copy.

## Docker images and authenticity

Append one compact `### Docker images` section after Full Changelog. Download target release's `images.txt` and `images.txt.sigstore.json`. Verify signed image list against target tag before copying its entries. Read signing workflow and verification docs at target commit if artifact layout has changed.

Include a two-column table, `Image` and `SHA-256 digest`, with one row per image in verified `images.txt`. Use full registry paths and complete `sha256:` digests. These are multi-platform image index digests, not commit SHAs or per-platform digests. Ignore comment lines. Do not resolve mutable tags such as `latest` to fill table. Use `image@sha256:...` for any pull or deployment examples.

Below table, link directly to both release assets and say: "Download both files, then verify signed image list with Cosign 3 or newer:" Follow with this single-line command, replacing `<tag>` with actual release tag:

```bash
cosign verify-blob images.txt --bundle images.txt.sigstore.json --certificate-oidc-issuer https://token.actions.githubusercontent.com --certificate-identity https://github.com/uniffy-io/uniffy/.github/workflows/release.yml@refs/tags/<tag>
```

Keep issuer and exact tag-bound workflow identity in command. Signature verification authenticates image digest list; a checksum alone does not prove publisher identity. Link [release verification docs](https://uniffy.io/docs/deployment/verify/) for individual image signatures and SBOM attestations without expanding this section into a tutorial.

If artifacts are unavailable or verification cannot complete, report gap and mark section pending in local draft. Never invent or shorten digests, reuse another release's assets, or claim verification succeeded without running it. Preserve existing generated delivery instructions unless verified corrections are needed.

## Review and publish

Reconcile draft with evidence table. Check mixed-purpose commits were split, related work was combined, and reverted or incomplete changes were excluded. Verify opening heading names target version and summary contains exactly two short sentences. Verify category placement, date, source links, contributor accounts and any upgrade instructions. Match every Docker table row to verified release pinset, check asset links, and confirm verification command names target tag. Report any gaps in coverage. Show draft path, resolved range and brief summary to user. A draft request ends with local files; do not modify GitHub release.

Publish only when user requests publication or has already authorized it in current task. Re-read release body before editing. If someone changed it since drafting, incorporate their edits or clarify conflicting content before replacement. Confirm tag still resolves to recorded target SHA. If release does not exist yet, retain draft and report that publication awaits release workflow.

Update only notes through a body file:

```bash
gh release edit "$tag" --repo uniffy-io/uniffy --notes-file "$draft"
```

Leave tags, titles, release status and assets intact. Read body back to verify update and return release URL. Do not create a tag, trigger a release build or publish unrelated work as part of this skill.
