---
name: vidiq-competitor-watchlist
description: Find and manage the competitor channels tracked in vidIQ for an authorized YouTube channel, adding or removing channels only after explicit approval. Use when asked 'who are my competitors', 'youtube competitor analysis', 'find channels like mine', 'channels similar to [channel]', or 'clean up my competitor list'.
---

# vidIQ Competitor Watchlist

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Audit or update a watchlist for the intended authorized channel. Research only what the request
needs; a recommendation never authorizes a mutation. Only this skill changes the saved watchlist.

## Establish the list and candidate fit

1. Resolve the intended owner with `vidiq_user_channels`, then
   capture `vidiq_list_competitors` for its `youtubeChannelId` as the original canonical-ID set.
   Enrich titles with `vidiq_get_channels_by_ids` only when useful.
2. Exclude self, known siblings, and unrelated channels from analysis, but present removals as
   recommendations. Unknown ownership/fit is not an automatic removal reason; preserve
   intentional references.
3. For discovery, `vidiq_similar_channels` takes canonical `channelId` with optional `size` and
   `sort`, or manual `niche` with its declared filters. Do not mix modes or pass `subNiches`.
   Reuse known IDs; resolve manual context through `vidiq_channel_search` only when needed,
   matching the returned canonical ID. Country/format can influence ranking rather than strict
   eligibility, so check actual fit.
4. Use generic niche `vidiq_channel_search` for broader discovery and `breakoutChannel: true`
   for emerging challengers (`vidiq_breakout_channels` is a deprecated alias of that search). Set `subscriberCountMin` only for a requested or justified cohort
   boundary. Disclose it; tiny or nonpositive baselines make growth ratios unreliable.
5. Read [Discovery evidence](references/discovery-evidence.md) for candidate discovery or
   audience/mechanism pattern claims; individual candidate fit can
   remain tentative. Use semantic mechanism matching where declared.
6. Verify upload recency only when it affects a recommendation: use `vidiq_channel_search`
   with `channelTitle` and `channelTitleMatch: "exact"` when declared, verify the ID, and read
   `lastVideoPublished`. Channel `publishedAt` is creation time. Alternatively, a scoped
   `vidiq_channel_videos` read needs `popular: false` and `videoFormat: long`, `short`, or
   `live`; that format sample cannot prove channel-wide inactivity. Missing dates mean unknown.
   `vidiq_channel_stats` with the `channelId` and a `from`/`to` window verifies a growth claim
   before a candidate is added.

Classify useful candidates as direct competitors, format references, or emerging challengers.
Raw fame or size is insufficient; do not invent audience-overlap or private competitor analytics.

## Propose and execute an exact change

1. Present owner ID, original snapshot, canonical-ID `add`/`remove` sets, rationale, and expected
   final set: `(snapshot - remove) ∪ add`. Deduplicate, prevent overlap, and omit already-present
   additions or absent removals. Map additions to `follow` and removals to `unfollow`.
   An empty diff needs no mutation. Do not invent a watchlist/plan cap.
2. Obtain approval of the exact owner and add/remove diff.
3. Immediately before mutation, re-read the list within that approval. Compare canonical-ID sets
   with the original snapshot. If changed, abort, show the concurrent difference, and obtain
   approval for a revised diff. If the read fails, pause.
4. With unchanged preflight and approval, call `vidiq_update_competitors` once with
   `youtubeChannelId`, `follow`, and `unfollow`. Preserve the response and read back with
   `vidiq_list_competitors`.
5. Compare actual added/removed and final sets with the approved expectation. Report discrepancies,
   partial updates, or limit failures; never silently repair, roll back, or resubmit. Readback
   detects but cannot prevent a race after preflight because no atomic compare-and-swap is
   declared. If verification fails, label readback unverified and distinguish
   any response-confirmed state.

## Deliver

For an audit, return the diagnosis and proposed changes. After an approved update, report the
confirmed final list or exact verification gap, approval state, and unresolved discrepancies.
Keep the owner explicit for multi-channel accounts.
