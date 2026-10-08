---
name: onsite-publish
description: Use to publish an APPROVED, drafted content item via the CMS adapter (WordPress or git-static) - "publish the draft", /organic-os:publish. Refuses unapproved items.
---

# Publish content (gated)

1. Input: a brief item with status "drafted" whose draft file sits next to it
   (same folder, <brief-name>.draft.md produced by ce-produce).
2. Gate: the brief's status must be "drafted" (step 1 already checks) AND
   `core.contracts.require_approval_lineage(brief_path)` must pass; abort on
   ContractError. A rejected item must never reach `create_post`. The profile
   user must also confirm the final draft in-session or via channel.
   Refuse a draft whose frontmatter lacks `capsule: verified` (ce-produce's
   handoff note) - the human can override in-session, and the override is
   recorded in the outcome record.
   Read ce-editor's oversight block from the draft notes: a score at or
   above the profile's `editorial.oversight_threshold` (default 7) adds
   a prominent line to the approval-channel message - "editor recommends
   a human line-edit: <top factor>". Publishing remains gated by the
   same approval either way: the score informs the human, it does not
   add a second gate. Rationale: scaled, unedited AI content correlates
   with deindexation
   (https://www.rankability.com/data/does-google-penalize-ai-content/).
3. Create the post via the CMS adapter (`onsite.cms.adapter_for`;
   wordpress or git-static per `cms.type` - the git-static branch below
   replaces steps 3-4): `create_post` (status draft by default; status
   "publish" only when site-profile sets publishing: direct), then
   `update_seo_meta` with title/description/focus keyword from the draft's
   frontmatter, and schema if the draft includes it. (`update_rankmath`
   remains as the WordPress adapter's alias for `update_seo_meta`.)
4. Verify with `get_rendered_head`; on success `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib"
   python3 -m core status <brief-path> published --actor agent` and
   write the outcome record with measurement dates; on failure leave the post
   in draft and record the post id + failure reason in the outcome record.
   IndexNow: when site-profile.yaml has `indexnow: {enabled: true, key: ...}`
   (additive key) AND the post actually went live (status "publish" - a WP
   draft has no public URL to submit), call `hoo.indexnow.submit(host, key,
   [post_url])` after the successful verify and record the returned status
   in the outcome record; a non-200 is recorded, never retried in-run.
5. If a Canva image brief exists next to the draft (from ce-image), record its
   path in the outcome record for manual upload (media upload is not in v1).
6. Outcome summary - the approver always hears what happened. Compose ONE
   message for the whole run and deliver it through the configured
   approval channel (same channel-neutral delivery as skills/onsite-apply
   step 4; in-session prints it). One line per item: each published post
   with its live URL; each post left in draft, held in a PR, or failed,
   with the reason and what happens next. No per-item message spam. A run
   that published nothing and failed nothing sends nothing.

## Git-static sites (cms.type git-static)

Steps 1-2 are identical: the drafted status check and
`require_approval_lineage` run BEFORE anything is written anywhere, and
the human confirms the final draft the same way. Then the PR replaces the
REST write; the adapter only writes files in the local clone
(`cms.repo_root`), and this skill runs every git/gh command:

3. Create the content file via the adapter: `create_post(slug, title,
   content)` - `draft: true` frontmatter by default, `status="publish"`
   (draft: false) only when site-profile sets publishing: direct. Then
   `update_seo_meta` with description/canonical from the draft's
   frontmatter, and `schema_jsonld` if the draft includes schema - it
   lands in the `jsonld` frontmatter field, which the site's layout must
   render into the head.
4. Deliver as a PR: `git checkout -b organic-os/<brief-id>`, add, commit,
   push, `gh pr create` with the draft's summary and the brief's id and
   approval lineage in the body. The brief STAYS `drafted` while the PR
   is open (drafted -> published is its only legal exit; there is no
   partial state for briefs) - record the PR url in the outcome record.
   Merging is the human's final act: no publish without it.
5. Merge detection, next run (`gh pr view <n> --json state,mergedBy`):
   merged -> `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status
   <brief-path> published --actor <merger>`; finish the outcome record
   with merge time and measurement dates. Closed unmerged -> the brief
   stays drafted; record the closure and leave the retry decision to a
   human. On a pr-merge-channel site the merge doubles as the human
   sign-off; the merge commit and the outcome record carry it.
6. Verify, honestly: `rendered_head_verify` is False - step 4's rendered
   head check does not exist here. If the profile has `cms.deploy_url`,
   fetch the expected live URL after merge detection and record a
   best-effort post-deploy check, labeled exactly that. IndexNow only
   when the post actually went live (draft: false and the site deployed),
   after merge detection, same recording rules as step 4.

Dry-run: with `onsite: {dry_run: true}` in site-profile.yaml, run the same
gated flow with the adapter constructed `dry_run=True` - nothing is
created, the brief stays `drafted`, and the outcome record is marked
dry-run listing every write from the adapter's `dry_run_log` (see
skills/onsite-apply). With git-static, nothing written to the clone means
nothing to commit: no branch, no PR.

Never edit brain frontmatter directly. The contract CLI is the only write
path for status and approvals.
