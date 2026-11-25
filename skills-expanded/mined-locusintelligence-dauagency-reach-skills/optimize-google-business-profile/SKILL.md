---
name: optimize-google-business-profile
description: Optimize a Google Business Profile (GMB, Google My Business listing) with the Reach MCP server. Finds what the profile is missing (description, hours, services, links, attributes, categories), previews each fix with before and after, and writes one approved change at a time, then reads it back from Google. Use when someone asks to optimize, complete, audit or fix their Google Business Profile, improve their GBP for local SEO, or update hours, description or services.
license: MIT
---

# Optimize a Google Business Profile

Find the gaps in a Google Business Profile and fix them one previewed, approved change at a time.

## Setup

This skill needs the Reach MCP server connected in your AI client:

- Server URL: `https://reach.locus-intelligence.com/api/mcp` (remote, Streamable HTTP, OAuth sign-in, no API key)
- Setup for Claude, ChatGPT, Claude Code, Codex, Cursor, VS Code and others: [README](https://github.com/LocusIntelligence-DauAgency/google-business-profile-mcp#install)

Editing needs the Google Business Profile connected in Reach.

## Steps

1. **Pick the location.** Call `get_account`. If there is more than one location, ask which one. If its `connectionStatus` is not `active`, tell the owner to reconnect Google in Reach and stop.
2. **Find the gaps.** Call `get_recommendations` for the location, then `get_listing` with `sections: ["profile"]` to see what is there now. If `readiness` is `never_run`, the profile has not been scored yet: say that, not "nothing missing". Never add gaps that are not in the response.
3. **Summarise** the gaps in a few lines, most useful first, grouped by `actionability`:
   - `agent_can_fix`: offer to do it with the tool named in `fix`.
   - `needs_owner_input`: ask the owner for the substance (a phone number, the real opening hours, what services they offer). Never invent it.
   - `needs_setup`: explain once what it needs, without pushing.
4. **One change at a time.** For each fix the owner wants:
   1. Call `update_listing` with `preview: true` (the default) and only that change in `changes`.
   2. Show each changed field's before and after, exactly as the preview returns it.
   3. Ask for an explicit yes to that change. One yes covers one change, never "all of the above".
   4. Call `update_listing` again with the same `changes`, `preview: false` and the `basedOn` the preview returned. Pass an `idempotencyKey`.
   5. Report `published.applied`, `skipped` and `failed` exactly as returned.
   6. Read back with `get_listing` (`sections: ["profile"]`). If the old value still shows, say Google may still be applying it.
   7. When the fix is done and read back, call `update_recommendation_status` with the item's `taskId` and `status: "completed"`.
5. **Next item**, or stop when the owner says so. Use `status: "dismissed"` only when the owner asks to drop an item.

## Things to know

- Settable fields: name, additional categories, description, opening date, phones, website, action links, social and messaging links, regular and special hours, services and attributes. Service area is added or removed by place name.
- The primary category and the address cannot be changed here. Photos are a separate, previewed tool (`manage_media`).
- If the write is refused because the listing changed since the preview, preview again and ask again.
- If the preview shows `stagedDashboardEdits` (unpublished edits saved in Reach), show them separately. Set `includeStagedEdits` only after the owner approves those too.
- Use `publishMode: "all"` only when the owner asks to publish everything.
- A description should describe the business in the owner's words: no keyword stuffing, no links, nothing the owner has not confirmed.

## Safety

- Never write to Google without the owner's explicit yes to the exact before and after. Preview first, always.
- Stop if the location's `connectionStatus` is not `active`.
- Read `limitations` before saying there is no data.
- On `rate_limited`, give `retryAfterSeconds` and do not retry right away. On `listing_only`, relay the message and `connectUrl`, and stop. On `limit_reached` or `monthly_quota_exhausted`, say what was blocked, give the `manageUrl`, and stop.
