---
name: maintain-changelog
description: >-
  Curate a hand-maintained CHANGELOG.md from Git history by reading the actual commits and diffs, whatever the commit message style. Use whenever the user wants to update, write, reconcile, or catch up a changelog — "update the changelog", "add this to Unreleased", "what changed since 1.4.0?", "prepare the 1.5.0 changelog section", "record that 2.0.0 shipped", or "start a changelog for this repo". Also use to propose the next Semantic Versioning bump from those changes. Not for GitHub release notes or announcements, and not for changelogs a release tool generates (changesets, release-please, semantic-release, git-cliff): there it explains and offers the tool's own input instead.
compatibility: Requires read access to local Git history, Node.js for the bundled script, and file editing tools. No GitHub integration or Conventional Commits required.
---

# Maintain Changelog

A changelog is a public promise to the people who use the software: users, integrators, and operators decide whether and how to upgrade from it. Two things follow from that. First, it should hold curated changes in reader terms, not a dump of commit subjects. Second, an unverified claim is worse than a gap. An invented migration step, audience, link, security claim, version, or release date can mislead readers in ways a missing entry cannot. When the evidence runs out, ask.

This workflow edits only the changelog. Committing, tagging, publishing, versioning manifests or lockfiles, and installing automation belong to the user's release process. Write separate release notes only if asked.

## 1. Establish scope

- **Check whether a release tool owns the changelog.** Look for `.changeset/`, `release-please-config.json` or `.release-please-manifest.json`, semantic-release config (`.releaserc*`, `release.config.*`, a `release` key in `package.json`), `cliff.toml`, or a "generated" note in the changelog header. If you find one, do not edit the changelog: the tool regenerates or prepends to it and hand edits will conflict or vanish. Explain what owns it and offer to write that tool's input instead, such as a `.changeset/*.md` file.
- Read repository guidance, the existing changelog, version sources, and compatibility and migration docs. Keep the changelog's language and existing human edits. Default to root `CHANGELOG.md` when none exists. If several changelogs are plausible (a monorepo, per-package files), ask which to maintain.
- Review the current checkout's committed history through HEAD. Do not fetch, switch branches, or inspect other branches unless asked. Leave staged and uncommitted work out and mention that you excluded it.
- **Decide the release mode from the user's words.** Commit dates, version bumps, and deployment plans do not tell you what shipped, so never infer the mode from them:
  - **Unreleased** (default): reconcile the `Unreleased` section only.
  - **Preparing release X**: the user explicitly asks to cut, prepare, or write the section for a version that has not shipped yet, typically in a release PR. Create that versioned section.
  - **Released**: the user says the changes shipped. Record them in a versioned section.

  Apply the mode to the changes under review. Ask only if the user's words leave a material subset unclear, and keep unrelated pending entries in `Unreleased`.

## 2. Find the candidate commits

The boundary is the release date of the newest **released** section, inclusive from midnight. Use the timezone documented by the project, otherwise local time. `Unreleased` has no date and does not move the boundary. The window is inclusive because a release-day commit may or may not have made it into the release. Re-reading it costs little, because reconciliation (§3) keeps it from being recorded twice.

List the candidates with the bundled script, using the path relative to this skill:

```bash
node scripts/list-candidates.mjs --since 2026-11-01 --offset +00:00   # omit --offset for local time
node scripts/list-candidates.mjs --after <commit>                    # user-supplied boundary, excluded
```

The script enumerates all history from HEAD and filters by committer date. It does not use `git log --since` pruning, which can skip commits behind an out-of-order timestamp. Committer dates are used because author dates can predate integration. It reports the branch, HEAD, the commit count, merge commits, and whether the clone is shallow.

- With no changelog, released section, or usable date, ask for a starting date or commit and for the initial or current version. Do not silently treat all history as the first release or reconstruct historical releases.
- If the clone is shallow, history is missing, or release dates conflict, say what cannot be established and ask. Never claim complete coverage without the evidence.

## 3. Inspect and reconcile every candidate

Read each commit's full message and diff, then the code, tests, docs, and related commits needed to understand its effect. Commit messages may be in any format and are often vague, so judge each change by its resulting behavior, never by its wording, prefix, or label.

Keep a temporary ledger as you go: commit, observed effect, and disposition (new entry, already covered, combined, reverted, or omitted with reason). It lets you prove nothing was skipped. Keep it out of the changelog and out of any tracking file. Work through large histories in explicit batches rather than sampling.

- **Merges:** review a merge's first-parent diff (`git diff <merge>^1 <merge>`) to see everything it brought in. Branch commits dated before the boundary only appear there. Run `git show --remerge-diff <merge>` to catch changes made during conflict resolution. Count each change once.
- **Include** features, fixes, deprecations, removals, security changes, and anything else that affects users, integrators, or operators.
- **Omit** refactors, tests, tooling, and dependency churn unless they materially affect those readers. Inspect them before deciding.
- **Combine** related commits into one entry. **Split** a commit that holds distinct reader-facing changes.
- **Reconcile** against both released sections and existing `Unreleased` entries on every run. Keep useful existing prose, improve it only as evidence warrants, and never duplicate a covered change. That way, running the workflow twice on unchanged history changes nothing.
- **Reverts:** drop pending entries for changes fully reverted before release and describe the final effect of a partial revert. Released entries stay, even if a later release reverts their behavior.

## 4. Write the entries

Follow [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/):

- `## [Unreleased]` first, even when empty, then releases newest first as `## [1.4.0] - 2026-11-02` (ISO dates). The header states that the project follows Keep a Changelog and Semantic Versioning.
- Categories appear in the order `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, each at most once per release, and only when non-empty. A replaced interface goes under `Changed`. A removal with no replacement goes under `Removed`.
- Write short plain-language bullets: what changed, who is affected when it matters, and any action required. Leave out hashes, file lists, and jargon that do not help the reader.
- Prefix incompatible changes with **Breaking:**, then state the upgrade action and link a migration guide only if one exists. If the upgrade steps are unknown, ask before presenting the entry as finished.
- Treat published sections as history. Ask before reorganizing or correcting them beyond incidental formatting.
- Keep working comparison links. Add new ones only for verified repository URLs and refs. Plain version headings are fine otherwise.

For worked examples, read [references/changelog-examples.md](references/changelog-examples.md) before writing or rewording entries: a complete changelog, curating commits into entries, rewriting weak bullets, breaking changes, deprecations, security fixes, and preparing a release.

## 5. Choose the version and apply the release mode

Use [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) against the project's declared public contract, such as documented APIs, integrations, configuration, import/export formats, and supported workflows. Ordinary visual changes alone do not make a major bump. If no adequate contract exists and that prevents a reliable decision, ask.

For stable versions (`1.0.0`+), take the highest bump the changes require:

| Change | Next version |
| --- | --- |
| Incompatible change to the public contract | Major, reset minor and patch |
| Compatible new functionality or a public API deprecation | Minor, reset patch |
| Only compatible bug fixes | Patch |

For `0.x`, the first `1.0.0`, prereleases, or anything else outside these rules, follow the project's policy or ask. Validate user-supplied versions as SemVer, check that they come after the previous release, and flag any conflict with the required bump rather than silently accepting or replacing the version.

- **Unreleased:** propose the next version with its rationale, labeled as a proposal. Do not add a version or date to the changelog.
- **Preparing release X:** move the changes into `## [X] - <date>` below an empty `Unreleased`. Use the planned date the user gives. If they give none, use today's date and note in the report that it must be updated if the release slips.
- **Released:** use the version and actual release date the user gives. If either is missing, propose the version and ask for the date. Today's date is not a substitute for a past release date.
- In both release modes, move only the in-scope changes, including relevant existing `Unreleased` entries. If the version is already recorded, reconcile it instead of adding a second section.
- If there are no notable changes, say so instead of manufacturing entries or a version.

## 6. Verify and report

Review the diff and confirm that:

1. Every candidate in the ledger has a disposition, and the counts match the script output.
2. Entries describe verified final behavior with no noise or duplicates, so a second run would change nothing.
3. The release mode, dates, and version follow the user's input and the compatibility policy.
4. Section order, category order, unique headings, breaking-change actions, and links are correct, and no history or user edits were lost.
5. Only the changelog changed. A prose update needs no application test run. Verify it against the source evidence and the Markdown diff.

Report the file edited, the branch, HEAD, boundary, and commit count, notable inclusions and exclusions, the release mode, the proposed or recorded version with rationale, and open questions. Separate inspected evidence from assumptions and incomplete coverage.
