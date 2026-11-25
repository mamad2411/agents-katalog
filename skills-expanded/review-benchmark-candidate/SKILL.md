---
name: review-benchmark-candidate
description: Review benchmark Dataset candidates or code pull requests. Use when checking a Hugging Face result contribution, investigating acceptance, or reviewing a code change to this repository.
compatibility: Linux, Node.js 24+, GitHub CLI access, and this repository's installed dependencies.
---

# Review a benchmark pull request

## Identify the pull request

- **Ordinary result candidate** — a Hugging Face Dataset pull request with one normalized `candidates/<run-id>/` bundle. It becomes an `unverified` observation.
- **Official result candidate** — a Dataset pull request under `candidates/official/<execution-id>/` with a signed archive, attestation, and transport metadata. It becomes `verified` only after proof validation.
- **Code pull request** — a pull request to this GitHub repository. Merging it changes the benchmark or its automation.

Dataset admission is automatic and never depends on score. A failed task, timeout, or low score is valid evidence. Reject only malformed, unsafe, conflicting, or unverifiable data.

## Dataset candidates

Do not download a Dataset snapshot or candidate revision to the maintainer workstation. Do not run production acceptance locally.

The scheduled **Auto-accept benchmark observations** workflow runs four times an hour. It processes official candidates first and ordinary candidates second. Each candidate is handled serially against the current Dataset head.

If a PR has a closed-to-open transition in its history, scheduled acceptance leaves it out of the queue permanently. This applies to ordinary and official PRs, even if new commits are added later. The PR is now under manual review: the scheduled workflow does not accept its data, post receipts, or close it. Explicit maintainer dispatch remains available; reopening does not authorize replacing accepted evidence.

Normal acceptance is append-only:

1. download `source/index.json`, `dataset-index.json`, and `aggregate-state.json` from current `main`;
2. download only the immutable files belonging to the candidate;
3. validate the normalized bundle, identity, hashes, foreign keys, safe metadata, and task-set compatibility;
4. add one retained source bundle and one new shard per table;
5. append the aggregate state and regenerate only compact views, scores, badges, indexes, and the Dataset card;
6. publish one parent-checked commit;
7. post an acceptance receipt with the run ID and Dataset commit, then close the candidate pull request.

The workflow closes the pull request instead of using Hugging Face's merge action. Merging the raw PR would copy the temporary `candidates/` directory into Dataset `main`, which is not the accepted storage layout.

If acceptance succeeds but the receipt or close request fails, keep the Dataset commit. Report the delivery warning and let the next scheduled pass reconcile the already accepted run and close the PR.

### Manual investigation

Use a server-side dry run only when the user asks to investigate a specific ordinary candidate:

```sh
gh workflow run accept-huggingface-observation.yml \
  -f dataset_repository=alexshpunt/explicit-edit-benchmark \
  -f candidate_ref=PR_NUMBER \
  -f dry_run=true
```

Run it once, record the workflow URL, and wait for it to finish. Do not dispatch several candidates in parallel because Dataset acceptance uses one serialization group.

A dry run must not publish or close the candidate. Its summary reports the run ID and the small number of files that a real append would add or update.

Use production manual dispatch only to recover a candidate that cannot wait for the next scheduled pass and only when the user explicitly asks:

```sh
gh workflow run accept-huggingface-observation.yml \
  -f dataset_repository=alexshpunt/explicit-edit-benchmark \
  -f candidate_ref=PR_NUMBER
```

Never retry a `429` immediately. Leave the candidate open for the next scheduled pass.

A full Dataset download and rebuild is a recovery operation for a missing or invalid aggregate state. It is not candidate validation and must not run during ordinary acceptance.

### Correct accepted usage

An ordinary accepted observation can receive a manual token and cost correction through `correct-huggingface-usage.yml`. This is not normal acceptance and never runs on a schedule. Only the repository owner can run it from `main`.

Pin each request's PR number, contributor, immutable candidate commit, manifest SHA-256, rounds SHA-256, expected total tokens, and CLI-reported cost. Run a dry run first. It compares the candidate against retained evidence and rejects any non-usage change, different identity, or contributor mismatch. Official signed observations are not supported.

Review the dry-run result, then publish the same requests with its `parentCommit` as `expected_dataset_revision`. If Dataset main moved, do a new dry run rather than bypassing the check. The batch replaces existing evidence and derived views in one parent-checked commit, preserving run and submission IDs and observation count. The prior Dataset revision is the recovery reference. Receipts are posted only after publication; PRs remain open under manual control. If receipt delivery fails, retain the Dataset commit and deliver the missing comments separately without repeating the replacement.

## Code pull requests

Read the diff and touched files. Read `docs/benchmark-automation.md` when a change touches schema, aggregation, acceptance, or Dataset views. Run:

```sh
npm run check
```

When the diff adds a harness adapter, also apply `add-benchmark-harness`.

Report what changed, risks, and verification results. Ask the user before merging a code pull request. Merge it through GitHub only after CI passes.

## What to report

For Dataset candidates, report:

- candidate number and contributor;
- claimed model, provider, harness, versions, and reasoning when available;
- whether it was accepted, rejected, or deferred;
- Dataset commit and workflow URL;
- whether the acceptance receipt was posted and the pull request was closed.

For rejected candidates, leave the pull request open and give the contributor the exact validation error. Never edit normalized evidence to make it pass.
