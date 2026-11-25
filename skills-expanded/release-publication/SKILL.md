---
name: release-publication
description: Use when preparing, qualifying, publishing or closing an AIP release (a 0.x.0 capability release or a 0.x.y patch/demo release) - version bump and release docs, exact-candidate readiness, the owner's publication decision, tagging and GitHub Release publication, GHCR digest capture, post-release verification and the closure PR. Not for spec or feature work.
---

# Release publication

This skill is **procedural, not normative**. The release's own specification (for a capability
release, its `iN-release-*.md` increment spec, e.g. v0.5.0's
[I6](../../../docs/specifications/0.5.0/i6-release-candidate-publication-and-post-release-verification.md))
and the owner's decisions govern. Where they disagree with this skill, they win: stop and flag the
conflict. [`AGENTS.md`](../../../AGENTS.md) rules still apply, including never merging a PR.

It encodes what v0.5.0 (full I6 path) and v0.5.1 (lightweight path) actually did. The records are
[`v0.5.0-post-release-verification.md`](../../../docs/release-validation/v0.5.0-post-release-verification.md)
and [`v0.5.1-release-record.md`](../../../docs/release-validation/v0.5.1-release-record.md).

## Hard rules

- **Publication needs the owner's explicit "go" for this exact candidate,** given in the moment.
  Never infer it from an earlier approval, a merged PR or a green readiness check. Confirm right
  before tagging.
- **One exact candidate.** `CANDIDATE_SHA` is the merge commit of the release-prep PR. Every check
  names that SHA. An earlier checkout, a PR head, a rebuilt image or an older tag is not a
  substitute. Any later commit to candidate content means a new candidate and new readiness.
- **SHAs come from git, never from memory.** Capture them in the same command that uses them
  (`gh pr view <n> --json mergeCommit -q .mergeCommit.oid`, `git rev-list -n1 <tag>`).
- **Never move, delete or re-create a published tag or release.** If publication happens but no
  verifiable digest results, the outcome is `POST_RELEASE_FAILED`, and a re-publication needs a new
  owner authorization.
- **Verify by digest, not by tag.** After publication, every image check uses
  `ghcr.io/michaelegner/architecture-intelligence-platform@<FINAL_IMAGE_DIGEST>`.
- **Release docs are candidate content.** CHANGELOG, release notes and README claims ship inside
  the tag. Check every "all tools" or "every answer" claim against each request/response model
  individually. A wording fix after the candidate is frozen means a new candidate.

## Choose the path

| | Capability path (`0.x.0`) | Lightweight path (patch or demo release, owner's choice) |
|---|---|---|
| Governing text | The release's I6-style increment spec | The release spec's publication clause plus this skill |
| Candidate attempts | `rc.N` labels; a failed gate is recorded in `vX-rc.N-no-go.md` | One candidate; a failure is fixed in a new prep PR |
| Records | Readiness record, publication-decision record, post-release verification, completion record (one PR each) | Readiness posted as a comment on the prep PR; one release record in the closure PR |

Ask the owner which path applies if the release spec doesn't say.

## 1. Entry audit

- Fetch and merge `origin/main`. Confirm from `ROADMAP.md` and the release spec that all increments
  are complete, with no open release blockers.
- Confirm the tag and the GitHub Release don't exist yet: `git ls-remote --tags origin vX.Y.Z` and
  `gh release view vX.Y.Z` (the latter must fail).

## 2. Release-prep PR (candidate content)

Follow the most recent prep PR as the template (#264 for v0.5.0, #274 for v0.5.1). It contains:

- **Version bump:** `pyproject.toml`, the root project version in `uv.lock` (the lock diff should be
  that one line), `_RELEASE_VERSION` in `tests/unit/test_release_version_consistency.py`, and
  `producer.version` in every `evaluation/architecture_answers/scenarios/*/expected_answer.json`
  (one line each). Frozen tests that pin a released version (such as the I5 freeze test's
  `RELEASED_PRODUCER_VERSION`) change only where the release spec allows it.
- **Pins:** if a file listed in `examples/release-golden-path/SHA256SUMS` changes, re-pin exactly
  those entries.
- **Release notes:** `docs/release-validation/vX.Y.Z-release-notes.md`, plus a row in
  `docs/release-validation/README.md`.
- **CHANGELOG:** move `[Unreleased]` to `[X.Y.Z] - <date>`, and leave an empty `[Unreleased]` above
  it.
- **Not in this PR:** README "Latest release", ROADMAP "shipped" and the spec's status. They change
  in the closure PR, after publication.

Run the full local gate from `AGENTS.md` (format, lint, pyright, both suites) and the evaluation
twice, and report totals exactly as run. Stop any running demo stack before `demo_e2e`, because a
running stack makes those tests skip or fail on ports.

## 3. Readiness on the exact candidate

After the owner merges the prep PR, read `CANDIDATE_SHA` from git and check it alone:

- **CI:** every check-run succeeded on that SHA, read from
  `gh api repos/<owner>/<repo>/commits/<sha>/check-runs`, not from `gh pr checks`.
- **Clean build:** in a clean detached worktree at the SHA, build the image with `--no-cache` and
  `--build-arg AIP_BUILD_REVISION=<sha>`, and record the image id and base-image digests.
- **Golden path:** run
  `RELEASE_CANDIDATE_SHA=<sha> examples/release-golden-path/run.sh <image> <out>`. All phases must
  pass, with the new `package_version` and `build_revision = <sha>` on every answer.
- **Evaluation:** run twice from clean state; the outputs must be byte-identical.
- **Security:** compare Trivy findings with the previous release. A new HIGH or CRITICAL finding
  needs an owner disposition before publication.
- **Demos** named in the release spec come up and tear down cleanly.

Record the results: as a readiness record (capability path) or as a comment on the prep PR
(lightweight path). Then ask the owner for the publication decision, naming the candidate SHA.

## 4. Publish (only after the owner's explicit go)

Re-check first: the candidate is unchanged, readiness still applies, and no tag or release exists.
Then:

```bash
SHA=$(gh pr view <prep-pr> --json mergeCommit -q .mergeCommit.oid)
git tag -a vX.Y.Z "$SHA" -m "AIP vX.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z --verify-tag --title "AIP vX.Y.Z" --notes-file <rendered notes>
test "$(git rev-list -n1 vX.Y.Z)" = "$SHA"
```

The rendered notes are the release-notes file without its title and candidate-status line, with
every relative link rewritten to `blob/vX.Y.Z/...`. Check that each target exists at the tag. The
v0.5.0 precedent is an annotated tag at the exact SHA. v0.5.1 let `gh release create --target`
create a lightweight tag instead; either way, verify the tag's commit.

Publishing triggers exactly one `docker.yml` run (`release: published`; there is no
`workflow_dispatch`). Record its run id and every attempt, with each attempt's conclusion and
pushed digest. Take `FINAL_IMAGE_DIGEST` from the job summary.

## 5. Post-release verification (by digest)

- **Workflow:** every step succeeded (build and push, digest record, Trivy SARIF, full report,
  SBOM, retained security artifacts).
- **Anonymous pull:** `docker pull <image>@<digest>` works with an empty Docker config. The image's
  `AIP_BUILD_REVISION` equals the candidate, and the `vX.Y.Z` and `latest` tags resolve to the
  digest.
- **Golden path** passes against the published digest.
- **Code scanning** on `refs/tags/vX.Y.Z` is compared with the previous tag, and any new finding is
  dispositioned.
- **Release body:** every link returns 200.

## 6. Closure PR

It contains:
- the release record (lightweight path), or the post-release verification plus the completion
  record (capability path);
- README "Latest release";
- ROADMAP marked shipped;
- the release spec's status;
- the release-validation index row.

**Two-step link closure.** Release-body links pinned to the tag cannot reach the closure commit.
Either accept and document this in the record (v0.5.1), or, after the closure PR merges, fetch the
closed-state files, verify every new URL, and run `gh release edit` on the body only, never the
tag. Treat this as a planned step, not something a reviewer has to catch.

## Terminal outcomes

```text
RELEASE_READY_NOT_PUBLISHED  qualified; owner did not authorize publication; no release claim
SHIPPED_VERIFIED             published; exact tag, digest and golden path verified
NO_GO / POST_RELEASE_FAILED  blocking failure before or after publication, with its disposition
```
