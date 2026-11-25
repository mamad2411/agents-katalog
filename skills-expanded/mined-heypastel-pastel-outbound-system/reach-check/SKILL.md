---
name: reach-check
description: Gatekeeper — confirms each lead can actually be reached (resolvable LinkedIn profile, connection degree, email route through Lemlist) and completes missing fields from Pastel and public pages only. Use for "find their email", incomplete leads, or just before campaign-launch.
---

# Reach check — Gatekeeper

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

LinkedIn is the main channel, so the question is less "do we have their email?" than "can Pastel reach this profile?".

## Steps

1. **Profile:** `pastel_get_details` for each lead. Without a resolvable LinkedIn profile Pastel can't visit, invite, or message them → route `no-route`.
2. **Degree:** already connected → the sequence can skip the invitation and open with a message. Note it on the lead card.
3. **Missing fields:** fill company domain and current title from the company website or LinkedIn company page, and cite the page.
4. **Email:** Pastel doesn't look up email addresses. If `outbound-brief.md` allows email, route the lead `lemlist` — `campaign-launch` pushes it to Lemlist, which finds the address itself. Otherwise the field stays `[missing: email]`.
5. Someone caught twice (by two agents, say) keeps a single lead card that lists both events.

## Output

```
# Reach check — [date]
Checked: N · LinkedIn: n (connected: n) · Lemlist: n · No route: n

| Person | Company | Profile | Connected | Domain | Email | Route | Source |
```

Routes: `linkedin` · `linkedin-connected` · `lemlist` · `no-route`. Everyone with a route moves on to `priority-rank`.
