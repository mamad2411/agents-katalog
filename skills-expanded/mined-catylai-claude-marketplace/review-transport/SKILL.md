---
name: review-transport
description: "Posts a finished code-review-core review (VALIDATED.json) to a GitLab MR as inline notes plus one summary, deduplicated on re-runs. Use when review results need to reach an MR. Not for running a review (use code-review-core:review); not for GitHub (use github-workflow:review-transport)."
when_to_use: "post the review to the merge request, publish review findings to GitLab, re-post the review on the MR, request changes on the MR from the review results"
allowed-tools: Bash(glab auth status), Bash(glab mr view *), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/post-review.sh" --dry-run *), Read
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# review-transport

This skill carries a finished `code-review-core` review to a merge request. The judgement (the
severities, the verdict, and which findings block) was settled by `contract.py finalize`, and this
skill passes it through as it is. `scripts/post-review.sh` does the routing and posting.

## Procedure

1. **Check the review finished.** `.code-review/VALIDATED.json` must exist. If it is missing, run
   `/code-review-core:review` first. Treat a missing file as "the review did not finish" and post
   nothing, because an empty or approving review over an unfinished run looks like a clean result to
   the next reader. A VALIDATED.json whose verdict is `INCOMPLETE` did finish: it names what it could
   not read, and it posts as a comment.
2. **Resolve the MR.** Run `glab auth status`, then `glab mr view --output json --jq '{iid, web_url}'`.
   If there is no MR for this branch, stop and point to `mr-lifecycle` to open one.
3. **Dry run.**
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/post-review.sh" --dry-run --mr <iid>
   ```
   Show the user the verdict, the review event, whether it will approve, the routing counts and the
   plan lines. A dry run makes no API call, so it cannot yet see the diff or what is already posted.
4. **Get an explicit OK.** Post only after the user says yes to that plan. A posted review notifies
   people and cannot be taken back, so their yes is what authorises it.
5. **Post.**
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/post-review.sh" --mr <iid>
   ```
   Add `--project <group>/<project>` outside a checkout, and `--no-approve` when the user wants an
   APPROVE verdict posted without the approval. On a non-zero exit, show the user the printed reason
   and command (see the exit codes below) and re-run once it is dealt with.
6. **Verify.** The success line counts what landed. Confirm the summary is on the MR:
   ```bash
   glab mr view <iid> --comments
   ```

## What the script guarantees

| Situation | Behaviour |
| --- | --- |
| `VALIDATED.json` missing or unparseable | Refuses (exit 4 or 5); nothing is posted |
| `verdict` is `REQUEST_CHANGES` / `APPROVE` / `INCOMPLETE` | Summary states it; reviewer state `requested_changes` / `reviewed` / unchanged; only `APPROVE` approves |
| No `verdict` (a hand-built document) | Event derived with the contract's blocking rule; a derived event never approves |
| Blocking list | Exactly `blocking_reason_ids`; the floor is the document's `blocking_floor` |
| `in_diff: true` with a `path:line` location | Inline note on the diff version of the reviewed commit (`CONTEXT.json`) |
| That line is not in the diff, or GitLab will not anchor it | Moved to the summary; never dropped |
| `in_diff: false`, or a location that does not parse | A section of the summary |
| MR head is not the reviewed commit, `--no-approve`, or the account may not approve | Posted without an approval; the summary says why |
| Finding already on the MR (a fingerprint marker you posted) | Skipped. N markers with one key cover at most N findings, and a marker older than your latest summary counts only while that summary's open set lists its key, so a fixed finding that comes back is posted again |
| A marker in another account's note | Ignored; anyone can quote a marker |
| The set of open findings changed (one was fixed), verdict the same | A summary that records the new open set |
| Every finding present, but the verdict changed | A new summary that carries the new verdict |
| Your approval stands and the verdict is not `APPROVE` | Withdrawn first; if GitLab refuses, exit 14 with the command, nothing posted |
| Existing notes, drafts or approvals cannot be read | Refuses (exit 8), since posting blind could duplicate the review |
| You have pending draft notes of your own | Refuses (exit 10), because publishing would publish them too |

| Exit | Meaning | MR changed? |
| --- | --- | --- |
| 2–9 | Arguments, jq, artifact, read-back, or an `INCOMPLETE` that reached `APPROVE` | no |
| 10 | Your own pending drafts, or GitLab failed while creating drafts (this run's drafts deleted) | no |
| 11 | `bulk_publish` failed; this run's drafts deleted | no |
| 12 | Inline notes published, summary did not; a re-run posts the summary | yes |
| 13 | Review posted, approval failed; the message gives the approve command | yes |
| 14 | Your standing approval could not be withdrawn | no |

How the notes are built (the `position` object, draft notes and `bulk_publish`, the fallbacks for
older GitLab) is in [references/gitlab-api.md](references/gitlab-api.md). The marker grammar is in
the header of `scripts/post-review.sh`.

`CODE_REVIEW_BLOCKING_FLOOR` applies only to a document with no verdict. To review at a different
floor, re-run `finalize --floor <X>`; the script warns about an override that disagrees and does not
apply it.

## Extending the script

Finding text is untrusted: a review of a shell script quotes `$(...)` and backticks. The script
moves every value into the payload with `jq` and passes it to `glab` as a file, and nothing derived
from a finding is ever parsed by the shell. Keep that true in any change, and add a case to
`scripts/post-review.test.sh` that fails without the change.

## Without glab

On the web, or anywhere without a shell, use a GitLab MCP server if one is connected; otherwise
prepare the notes for the user to paste in the GitLab UI. Work from the pasted or attached
`VALIDATED.json`, route findings as in the table above, and get the user's OK first. A standing
approval of yours must be revoked in the UI when the verdict is not `APPROVE`.

Start the summary with `## Code review`, a blank line, then
`<!-- code-review-core:verdict:<VERDICT> -->`. End each finding with its marker, written exactly as
the script writes it, so a later run with glab recognises it. Leave out the open-set line the script
writes under the verdict (`<!-- code-review-core:active:... -->`, digests of the open keys); without
it, the next scripted run treats every marker as still open, which never duplicates a finding:

```
<!-- code-review-core:fp2:<P>:<T> -->
```

- `<T>`: the title, lowercased (ASCII letters), every run of whitespace replaced by one space, and
  leading and trailing spaces trimmed.
- `<P>`: the path from a `path:line` or `path line N` location, unchanged. When the location does
  not parse, the whole location, normalised like the title.
- Percent-encode the UTF-8 bytes of each part, leaving only `A-Z a-z 0-9 - . _ ~` as they are
  (`/` becomes `%2F`, a space `%20`). A `:` can then only be the separator.

Example: `src/auth.py:42` titled "Tenant id is not part of the cache key" gives
`<!-- code-review-core:fp2:src%2Fauth.py:tenant%20id%20is%20not%20part%20of%20the%20cache%20key -->`.
