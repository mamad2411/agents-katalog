---
name: onsite-apply
description: Use to execute APPROVED on-page proposals - "apply the approved fixes", /organic-os:apply, or a routine's apply step. Refuses anything not approved.
---

# Apply approved changes (the gate lives here)

1. Read profile + env file. Poll the channel first if telegram, via
   `core.approval.process_telegram_decisions(root, token, chat_id)` - it
   persists the poll offset and tolerates unknown/stale ids without raising.
2. List approved onpage-fix items. For each:
   a. `require_approved(path)` - this raises on anything not approved. Never
      catch that error to proceed; report it and skip.
   b. `snapshot()` the post (title + meta + content if the proposal touches it)
      -> save to `outcomes/<item-id>-rollback.json` in the brain repo.
   c. Apply via the CMS adapter (`onsite.cms.adapter_for`; wordpress or
      git-static per `cms.type` - the git-static branch below replaces
      steps b-g):
      `update_seo_meta` / `update_post` per the proposal body.
      (`update_rankmath` remains as the WordPress adapter's alias for
      `update_seo_meta`.)
   d. Verify: `get_rendered_head(target_url)` - assert the new
      title/description appear in the rendered head. On mismatch:
      `rollback()` immediately, then
      `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status
      <item-path> failed --actor agent`, append a signal
      "apply-verify failed", and alert. Never leave the item approved.
   e. `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status
      <item-path> applied --actor agent`; write an outcome record
      `outcomes/<item-id>.md`: what changed, when, rollback file, measurement
      due dates (+7d, +28d). Because the verify just succeeded, also write
      the re-verification window into the record, exactly these keys
      (see site-repo-contract.md):

      ```yaml
      reverify:
        due: <UTC now+1h>     # first scheduled re-check
        until: <UTC now+48h>  # window end; drift watch owns the horizon after
      ```

      hoo-daily re-checks the live values between `due` and `until` so an
      external revert (a bulk plugin restore, a theme update) surfaces
      within hours, not at the next audit.
   f. On a successful verify, refresh the drift baseline for this page
      (`onsite.drift.snapshot_pages` on this post id, merged into the
      stored `onsite.drift.baseline_path` entry, then `save_baseline`) so
      the change we just made intentionally is never flagged as drift by
      the next `hoo-daily` run.
   g. IndexNow: when site-profile.yaml has `indexnow: {enabled: true,
      key: ...}` (additive key), call `hoo.indexnow.submit(host, key,
      [target_url])` after the successful verify and record the returned
      status in the outcome record (`indexnow: {status: N, submitted: 1}`).
      A non-200 is recorded, never retried in-run, and never fails the
      apply. Skipped in dry-run - nothing changed, nothing to submit.
3. Commit + push the brain repo if git. Summarize: applied / skipped / failed.
4. Outcome summary - the approver always hears what happened. Compose ONE
   message for the whole run and deliver it through the configured
   approval channel (telegram: one `sendMessage` over the same transport
   `send_item` uses; slack/email: one post/send; in-session: print the
   summary; pr-merge: no live channel mid-cycle - append the summary to
   the run report and outcome records instead). Never send per-item
   messages. Content, one line per item:
   - applied and verified: item id + what changed
   - partially-applied: item id + the exact human step from the status
     note - the approver must know what is waiting on them
   - failed / rolled back: item id + the reason
   Silent success is a bug: whoever said yes hears the result, whether it
   landed, half-landed, or failed. A run that touched nothing sends
   nothing.

## Git-static sites (cms.type git-static)

The adapter is chosen by `cms.type` (`onsite.cms.adapter_for`). When it is
git-static, the write target is a local clone of the site repo
(`cms.repo_root`) and the pull request is the delivery mechanism. The gate
does not move: step 2a's `require_approved` runs unchanged, BEFORE any
file is written to any branch. The adapter never runs git; this skill runs
every git/gh command below.

0. pr-merge channel only, before the gate: proposals on such sites arrive
   as PRs against the brain repo, and the human merge IS the approval.
   Detect newly merged proposal PRs (`gh pr view <n> --json
   state,mergedBy`) and record each decision the merge represents:
   `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core approve
   <item-path> --actor <merger> --channel pr-merge`. The merge commit is
   GitHub's durable record; the CLI entry is the one the gates check. A
   closed-unmerged proposal PR is a rejection - record it with `core
   reject` the same way. (This mirrors step 1's telegram poll.)
   On every other channel the item was approved before this skill ran,
   and the site PR below is created only AFTER that approval.
1. Gate: `require_approved(path)` - unchanged, never caught to proceed.
2. Freshen the clone (`git pull` on the default branch in `cms.repo_root`).
3. `snapshot()` each target file (the snapshot stores the file's full
   text) -> `outcomes/<item-id>-rollback.json` in the brain repo.
4. Apply via the adapter: `update_seo_meta` / `update_post` per the
   proposal body - frontmatter and body edits in the working tree only.
5. Deliver as a PR - run:
   `git checkout -b organic-os/<item-id>`, `git add` the changed files,
   `git commit`, `git push -u origin organic-os/<item-id>`, then
   `gh pr create --title "<item title>" --body "<the proposal text>"`.
6. Honest status: the adapter's `capabilities()` declares `needs_human:
   ["merge-pr", "deploy"]`, so the item does NOT become applied here. Set
   `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status
   <item-path> partially-applied --actor agent --note "PR <url> open - a
   human must merge; the site then deploys itself"`. The queue shows it
   as a PARTIAL row until the merge. No publish happens without a human.
7. Merge detection, next run: `gh pr view <n> --json state,mergedBy`.
   Merged -> `core status <item-path> applied --actor <merger>`; write
   the outcome record (what changed, PR url, who merged and when,
   measurement due dates +7d, +28d). On a pr-merge-channel site this
   merge doubles as the human sign-off; the merge commit and the outcome
   record carry it. Closed unmerged -> a human said no: `core status
   <item-path> failed --actor agent --note "PR closed unmerged"` and
   delete the branch; nothing reached the default branch, so the
   rollback file needs no replay.
8. Verify, honestly: `rendered_head_verify` is False for this adapter -
   there is no rendered head to assert at apply time, and step 2d's
   verify does not run. If the profile has `cms.deploy_url`, fetch the
   live page after merge detection and record the result in the outcome
   as a best-effort post-deploy check, labeled exactly that - it never
   counts as the WordPress-grade verify. IndexNow (step 2g) also moves
   to after merge detection: only a merged and deployed change has a
   live URL to submit. Skip the drift-baseline refresh (step 2f); the
   drift watch is WordPress-only. No `reverify` keys on this path either:
   they attach only to a rendered-head-verified apply (step 2e), and the
   best-effort post-deploy check is not that verify.

Dry-run with git-static: the same rules as below - the gate still runs
first, the adapter logs every intended write in `dry_run_log`, and with
nothing written to the clone there is nothing to commit: no branch, no
PR. The outcome record, marked dry-run, lists the log.

## Dry-run mode

When site-profile.yaml has `onsite: {dry_run: true}` (additive key, schema
stays 1), construct the CMS adapter with `dry_run=True`
(`adapter_for(profile, ..., dry_run=True)`) and run
the full flow above unchanged - `require_approved` is still enforced
BEFORE the dry-run write, so a dry run rehearses the real path, gate
included, not a shortcut around it. Nothing reaches the site: every
mutating call lands in the adapter's `dry_run_log` instead of the session,
and reads (snapshot, get_rendered_head) behave normally. Skip step 2d's
verify assertion (a
write that never happened cannot appear in the rendered head) and do NOT
set the item to `applied` - it stays `approved` so a real apply can follow.
Write the outcome record marked `dry-run: true`, listing every entry from
the adapter's `dry_run_log` - each write that would have happened, with method,
post id, and fields. Skip the drift-baseline refresh (2f) and the
`reverify` keys; the page did not change, so there is nothing to
re-check.

## Redirect fixes (action type: redirect)

Some approved onpage-fix proposals prescribe a redirect - a moved target
behind broken internal links (skills/onsite-audit's link-health
dimension), or a cannibalization consolidation (skills/hoo-weekly). A
plain link REWRITE is not this action type: it edits the source page's
content and rides the normal `update_post` path above, gate, snapshot,
verify and all.

Redirects are a CMS capability, not a universal write. Consult the
adapter's `capabilities()['redirects']` mode FIRST and never fake a
write path the adapter does not declare:

- `needs-plugin` (the WordPress adapter): core WordPress has no redirect
  REST surface. Probe the known plugin surfaces at run time with the
  connected role - Rank Math's redirections module, the Redirection
  plugin's REST route. A surface is writable: create the 301, record its
  id in the outcome record (rollback for a redirect is deleting it),
  then verify by fetching the old URL and asserting a 301 status
  pointing at the new target. A failed verify deletes the redirect and
  marks the item failed, per the hard rules. No writable surface (module
  absent, or it needs an admin role the connected user lacks): set the
  item partially-applied with the exact manual step, e.g. "add a 301
  from /old-path to /new-path in the SEO plugin's redirections screen
  (Rank Math -> Redirections)". Never faked as done.
- `config-file` (the git-static adapter): write the platform's redirect
  file - the profile's additive `cms.redirect_file` key names it
  (`_redirects`, `netlify.toml`, or `vercel.json`; see
  site-repo-contract.md). The write is ADDITIVE: append or merge the one
  new rule, never a rewrite of existing rules. Everything else follows
  the git-static flow above unchanged: gate first, `snapshot()` of the
  redirect file, branch, PR, partially-applied until the human merge,
  best-effort post-deploy check of the old URL when `cms.deploy_url` is
  set. No `redirect_file` key in the profile: partially-applied naming
  the step ("set cms.redirect_file in site-profile.yaml, or add the
  redirect to the platform config by hand").
- `native`: reserved for an adapter whose backend writes redirects
  first-class through the adapter itself; no shipped adapter declares it
  today.

## Image and alt-text fixes (action type: image-fix)

Approved image-fix proposals carry per-image items (see the image-fix
section in skills/onsite-propose): missing alt text with the proposed
alt, and missing in-content images referencing a ce-image brief. The
gate is unchanged - `require_approved` runs before any write, per item.
Consult the adapter's `capabilities()['media_alt']` mode FIRST, the same
honesty rule as redirects:

- `True` (the WordPress adapter): before writing, record each target
  image's current alt (`get_media(post_id)`) in the item's rollback
  file - rollback for an alt fix is rewriting the old value (empty
  included). Then `update_media_alt(media_id, alt_text)` per item.
  An image `get_media` reports with `media_id: None` has no attachment
  to write to - its alt is hard-coded in the post content, so fix it
  via `update_post` on the content (snapshot and verify as usual); if
  the markup is theme- or builder-owned and `update_post` cannot reach
  it, the item ends partially-applied naming the step ("set the alt on
  <src> in the theme/page builder").
- `"in-content"` (the git-static adapter): `update_media_alt` rewrites
  the alt inside the content file - media_id `<post-ref>::<src>` for a
  body image, `<post-ref>::frontmatter` for the featured image's `alt:`
  field. The change rides the normal git-static flow above unchanged:
  gate first, `snapshot()` of the file, branch, PR, partially-applied
  until the human merge.
- Missing in-content image items PLACE, never generate: apply inserts a
  reference to an image file that already exists (the ce-image output
  named in the proposal, or a human-produced asset at that path), with
  the proposal's alt text. Nothing in the apply path generates an
  image. No file at the named path -> partially-applied with the step
  named ("produce the image per <slug>-image-brief.md, then re-run
  apply").

Verify step reads the result back: after the writes, `get_media` on the
target must show the new alt (and the placed image, for insertion
items); on WordPress also confirm via the rendered content where
available. A mismatch rolls back from the recorded prior values and
marks the item failed, per the hard rules. Anything the adapter cannot
do ends partially-applied with the named human step - never faked as
done.

## Partial application

When some changes in a proposal succeed and others hit a permission or
capability wall (a step needs a WordPress role the connected user does not
have), do NOT pick between "applied" and "failed" - both would lie. Set the
honest state via the contract CLI, with a note naming exactly what a human
must finish:

```
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status <item-path> \
  partially-applied --actor agent --note "<exactly what a human must finish>"
```

The outcome record lists done vs pending: every change that landed (with
its verify result) and every step still waiting on a human, each named
precisely. Once the human finishes the pending steps, the item moves
partially-applied -> applied via the CLI; if the partial work is rolled
back instead, partially-applied -> failed.

HARD RULES: no snapshot -> no write. Verify after every write. A failed verify
means rollback, never retry-and-hope. Never edit brain frontmatter directly.
The contract CLI is the only write path for status and approvals.
