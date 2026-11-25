---
name: release-notes
description: Generate and publish concise, evidence-based notes in the body of the latest existing GitHub Release. Use only when the user explicitly invokes `$release-notes` or explicitly asks to update the latest existing GitHub Release body. Do not invoke for general release planning, changelog, tag, or version tasks.
disable-model-invocation: true
---

# Release Notes

Update only the body of the latest existing GitHub Release. Treat the repository diff as the source of truth. Use pull requests and commits only as supporting evidence.

## Safety rules

- Use `gh` for all GitHub Release, pull request, issue, and API operations. Use `git fetch` only when required tag objects or history are missing.
- Do not create or delete a release.
- Do not change a tag, title, target, draft state, prerelease state, latest-release state, or other release metadata.
- Do not publish a draft.
- Do not use a new release as a fallback when no release exists.
- Do not infer release order from version text, semantic versions, or Git tag order.
- Stop when required evidence is unavailable. Do not publish partial or speculative notes.
- Treat the notes file as a full replacement for the current release body, not as text to append.

## 1. Verify prerequisites

Run all checks from the repository that the user wants to release:

1. Confirm that the current directory is in a Git worktree:

   ```sh
   git rev-parse --is-inside-work-tree
   ```

2. Confirm that `gh` is available:

   ```sh
   command -v gh
   ```

3. Confirm that `gh` can resolve and access the current GitHub repository. Save its URL and get the GitHub host from it:

   ```sh
   REPO_URL="$(gh repo view --json url --jq '.url')"
   GH_HOSTNAME="${REPO_URL#*://}"
   GH_HOSTNAME="${GH_HOSTNAME%%/*}"
   ```

4. Use the repository URL to get its GitHub host. Confirm the active account for that host:

   ```sh
   gh auth status --active --hostname "$GH_HOSTNAME"
   ```

Stop with a clear error if a check fails. Do not initialize a Git repository, change authentication, or select another repository as a fallback.

## 2. Select the release range

Use GitHub's descending release-list order as the release sequence. Include drafts and prereleases because they are existing releases:

```sh
gh release list --limit 2 --order desc \
  --json tagName,name,createdAt,publishedAt,isDraft,isPrerelease,isImmutable,isLatest
```

- Select the first item as the latest release.
- Select the second item as the previous release.
- If the list is empty, stop and state that no existing GitHub Release was found. Never create one.
- If there is one item, treat it as the project's first release.
- Do not re-sort the result. A draft can have no `publishedAt` value.
- Do not replace either tag with a Git tag that has no GitHub Release.

Set `LATEST_TAG` and, when present, `PREVIOUS_TAG` from this result. Quote both values in every command. Then load and record the latest release before any edit:

```sh
gh release view \
  --json tagName,name,body,isDraft,isPrerelease,isImmutable,publishedAt,targetCommitish,url \
  -- "$LATEST_TAG"
```

Confirm that the returned `tagName` is `LATEST_TAG`. Record `tagName`, `name`, `isDraft`, `isPrerelease`, `isImmutable`, and `targetCommitish` from this result. Also record `isLatest`, `createdAt`, and `publishedAt` from the release-list result. Use these values for the final safety check. If `isImmutable` is true, stop and report that GitHub does not permit the body update.

## 3. Resolve the tag history

Set full Git refs so that a tag that starts with `-` cannot become a command option:

```sh
LATEST_REF="refs/tags/$LATEST_TAG"
PREVIOUS_REF="refs/tags/$PREVIOUS_TAG"
```

Set `PREVIOUS_REF` only when `PREVIOUS_TAG` exists. Confirm that each selected release tag resolves to a local commit:

```sh
git rev-parse --verify "$LATEST_REF^{commit}"
git rev-parse --verify "$PREVIOUS_REF^{commit}"
```

Run the second command only when `PREVIOUS_TAG` exists. If a tag is missing, inspect the Git remotes, identify the remote for the same GitHub repository, and use `git fetch` to get the required tags. Do not assume that the remote is named `origin`. Stop if the remote is ambiguous or a release tag still does not resolve. Do not guess a replacement range.

Check for a shallow repository:

```sh
git rev-parse --is-shallow-repository
```

If the result is `true`, use the identified GitHub remote to fetch complete history and tags:

```sh
git fetch --unshallow --tags "$GITHUB_REMOTE"
```

Then run the shallow-repository check again. Continue only when the result is `false` and both required tag commits resolve. If the full history cannot be fetched, stop. Do not generate notes from an incomplete history.

When `PREVIOUS_TAG` exists, check whether it is an ancestor of `LATEST_TAG`:

```sh
git merge-base --is-ancestor "$PREVIOUS_REF^{commit}" "$LATEST_REF^{commit}"
```

A non-ancestor result is not an automatic failure. State it in the working notes, use the tree diff to identify the shipped-state change, and inspect both sides of the history so that the commit list does not cause a false claim.

## 4. Investigate all shipped changes

When a previous release exists, start with:

```sh
git log --date=short --format='%H%x09%ad%x09%s' "$PREVIOUS_REF..$LATEST_REF"
git diff --stat "$PREVIOUS_REF" "$LATEST_REF"
git diff --name-status "$PREVIOUS_REF" "$LATEST_REF"
git diff "$PREVIOUS_REF" "$LATEST_REF"
```

For non-linear history, also inspect:

```sh
git log --left-right --graph --oneline "$PREVIOUS_REF...$LATEST_REF"
```

For the first release, inspect all history reachable from the latest tag and compare its shipped tree with an empty tree:

```sh
git log --reverse --date=short --format='%H%x09%ad%x09%s' "$LATEST_REF"
EMPTY_TREE="$(git hash-object -t tree /dev/null)"
git diff --stat "$EMPTY_TREE" "$LATEST_REF"
git diff --name-status "$EMPTY_TREE" "$LATEST_REF"
git diff "$EMPTY_TREE" "$LATEST_REF"
```

Account for every changed path. Inspect the relevant diff hunks, not only the statistics or file names. For generated or binary files, inspect the source, manifest, configuration, or other evidence that explains their user impact. Do not include working-tree changes or commits after `LATEST_TAG`.

Use this evidence order:

1. Actual code and configuration diff.
2. Merged pull request title, body, changed files, and linked issue context.
3. Commit messages.

Use PR data when it resolves an unclear purpose, user impact, migration step, or reference. Find associated PRs for a commit when needed:

```sh
gh api -H 'Accept: application/vnd.github+json' \
  "repos/{owner}/{repo}/commits/$COMMIT_SHA/pulls"
gh pr view "$PR_NUMBER" \
  --json number,state,mergedAt,title,body,files,commits,closingIssuesReferences,url
```

Use PR context only when `state` is `MERGED` and `mergedAt` is present. Verify every PR or issue association before adding its number. A commit prefix, PR label, or PR title does not prove user impact.

## 5. Select user-facing changes

For each changed behavior, identify what a user can observe and the evidence that supports it. Include a change only when it materially affects one or more of these areas:

- behavior or user experience
- compatibility or migration
- installation or configuration
- public commands, flags, APIs, or file formats
- security or privacy
- performance or resource use

Normally exclude refactoring, formatting, lint changes, tests, CI changes, build maintenance, merge commits, routine dependency updates, internal cleanup, and documentation-only changes. Include one only when the diff proves material user impact.

Investigate an ambiguous change before classification. If the available evidence cannot support a useful claim, describe only the supported fact or omit the change. Never invent behavior, fixes, performance results, security effects, breaking effects, migration steps, or PR and issue links.

If no change has material user impact, write only a short, factual summary that says the release contains maintenance changes with no material change to user-visible behavior. Do not create empty sections.

## 6. Draft the release body

Create an isolated temporary directory and Markdown file:

```sh
RELEASE_NOTES_DIR="$(mktemp -d)"
RELEASE_NOTES_FILE="$RELEASE_NOTES_DIR/release-notes.md"
```

Arrange the body in this exact order, and omit all empty sections:

1. `### Highlights`
2. `### Added`
3. `### Changed`
4. `### Fixed`
5. `### Breaking Changes`
6. `### Deprecated`
7. `### Removed`
8. `### Security`

Start with a concise one-sentence or two-sentence summary. Do not add a version heading and do not repeat the release title. Use this shape only for sections that contain entries:

```markdown
A concise summary of the release and its most important user impact.

### Highlights

- Major user-facing improvement.

### Added

- Added support for ... (#123)

### Changed

- Improved ...

### Fixed

- Fixed an issue where ...

### Breaking Changes

- Replaced `--old-flag` with `--new-flag` for users of the command-line interface.
  - **Migration:** Replace `--old-flag` with `--new-flag` in scripts and configuration.
```

Apply these writing rules:

- Write for users, not for maintainers of the internals.
- Give one meaningful change in each bullet.
- Prefer concrete behavior over implementation detail.
- Start bullets with consistent verbs such as `Added`, `Improved`, `Changed`, `Fixed`, `Deprecated`, or `Removed`.
- Put commands, flags, configuration keys, API names, file paths, environment variables, and other technical identifiers in backticks.
- Add a verified PR or issue reference at the end of a bullet when it is useful.
- Use `Highlights` only for approximately one to three important items. Omit it for a small release.
- Do not repeat a change in two sections unless a short `Highlights` entry gives useful emphasis.
- Do not add a commit dump, contributor section, dependency-update list, or `Full Changelog` link.
- Keep the notes concise. Prefer useful information to complete internal history.

For each breaking change, explain what changed and who is affected. Add a nested `**Migration:**` instruction when the evidence supports one. Mention an important breaking change in the opening summary. Do not use the breaking label without evidence.

Use `### Security` only for material public security impact. State the improvement at a safe public level. Do not include sensitive vulnerability details or exploitation instructions.

## 7. Review before publishing

Read the complete temporary Markdown file. Correct all problems before the edit. Confirm that:

- the summary is one or two sentences
- no version heading or release title is present
- sections use the canonical order and no section is empty
- entries are not duplicated
- internal-only work is absent
- each claim has evidence
- each category matches the observable impact
- breaking changes have affected-user and migration details when available
- wording is consistent and concise
- the body has no contributor list, dependency dump, or `Full Changelog` link

Immediately before the edit, run the release-list query from step 2 again. Confirm that its first tag is still `LATEST_TAG` and that the recorded list metadata for this release did not change. Then run `gh release view -- "$LATEST_TAG"` again and confirm that the recorded release metadata still identifies the intended release. Stop if CI or another actor created a newer release or changed the selected release.

## 8. Update only the body

Run exactly this release edit command. Do not add any other `gh release edit` option:

```sh
gh release edit --notes-file "$RELEASE_NOTES_FILE" -- "$LATEST_TAG"
```

If the command fails, report the error. Do not create a replacement release and do not change release settings to make the edit pass.

Read the release again after success. Confirm that its body matches `RELEASE_NOTES_FILE` and that `tagName`, `name`, `isDraft`, `isPrerelease`, and `isImmutable` match the values recorded before the edit:

```sh
gh release view \
  --json tagName,name,body,isDraft,isPrerelease,isImmutable,publishedAt,targetCommitish,url \
  -- "$LATEST_TAG"
gh release list --limit 2 --order desc \
  --json tagName,name,createdAt,publishedAt,isDraft,isPrerelease,isImmutable,isLatest
```

Also confirm that `targetCommitish`, `createdAt`, `publishedAt`, and `isLatest` did not change. Confirm that `LATEST_TAG` is still the first item. If a new release appeared during the edit, report the race and do not claim that the edited release is still the latest.

Report the updated tag and URL, the sections that were published, and any omitted ambiguous change. Do not claim success if the readback does not match.

Remove the temporary file and directory after success or failure. Delete the file first, then remove the empty directory. Do not use a recursive removal command.
