---
name: content-calendar-audit
description: >
  Audit a Planable workspace's content calendar for a given period — surface what's
  scheduled, what's missing, what has no date, and what might have publishing issues.
  Use this skill whenever the user asks about upcoming content, wants to review the
  calendar, says things like "what's scheduled this week", "check the calendar for
  [client]", "what's going out next week", "any gaps in the schedule", "content audit",
  "what do we have planned", or wants a weekly/monthly content overview for a workspace.
  Always activate for calendar review and scheduling gap analysis in Planable.
---

# Content calendar audit

Review a Planable workspace's content schedule for a given period — what's ready, what's missing, what needs attention.

## How this skill works

1. Identify the workspace and time window
2. Fetch scheduled and unscheduled posts
3. Surface gaps, issues, and a clean calendar view
4. Flag anything that needs action before posts go live

---

## Step 1: Gather inputs

- **Workspace / client name** — which workspace to audit
- **Time window** — default to the next 7 days if not specified; accept "this week", "next week", "this month", or a custom range
- **Platforms** — all pages by default, or specific platforms if requested

---

## Step 2: Fetch posts

```
list_workspaces → find workspaceId
list_pages(workspaceId) → get pageIds for context

// Scheduled posts in window
list_posts(
  workspaceId,
  postStatus: ["SCHEDULED"],
  scheduledAfter: [start of window],
  scheduledBefore: [end of window]
)

// Posts with no date set (drafts that may be intended for this period)
list_posts(
  workspaceId,
  postStatus: ["NO_DATE_SET"]
)

// Posts with publishing errors
list_posts(
  workspaceId,
  postStatus: ["WITH_ERRORS"]
)
```

Also check for posts needing approval that are scheduled soon:
```
list_posts(
  workspaceId,
  approvalStatus: ["NOT_APPROVED", "PARTIAL_APPROVED"],
  scheduledAfter: [start of window],
  scheduledBefore: [end of window]
)
```

---

## Step 3: Build the audit view

### Calendar overview

Show scheduled posts grouped by day. For each day:
- List platform + post preview (first 80 chars)
- Flag approval status inline (✅ approved / ⏳ pending / ❌ not approved)
- Flag any errors (🔴)

**Example format:**
```
Monday, May 19
  • LinkedIn — "Three things we learned running 50 client campaigns..."  ✅
  • Instagram — "Behind the scenes of our Q2 content sprint..."  ⏳ pending approval

Tuesday, May 20
  ⚠️ Nothing scheduled

Wednesday, May 21
  • Facebook — "Meet the team: this month we're spotlighting..."  ✅
  🔴 Instagram — Publishing error — needs attention
```

### Gap analysis

After the calendar view, add a short summary:

- **Total posts scheduled:** [n] across [n] platforms
- **Days with no content:** list them
- **Posts with no date set:** [n] drafts not yet placed on the calendar
- **Posts with errors:** [n] — list them with platform and preview
- **Posts scheduled but not yet approved:** [n] — flag urgency if within 24–48h

### Recommendations

2–4 short, specific callouts. Examples:
- "Wednesday has nothing scheduled across any platform — consider moving [post X] there."
- "2 Instagram posts are going out tomorrow without approval."
- "3 LinkedIn drafts have no date — worth placing them before the end of the week."

Keep recommendations specific to what's in the data. Don't generate generic best-practice advice.

---

## Step 4: Optional follow-up

After the audit, offer:
- "Want me to draft posts to fill the gaps?"
- "Should I check another client or a different date range?"

---

## Edge cases

- **Many workspaces**: If the user asks to audit "all clients", loop through workspaces and produce one summary section per workspace. Warn if there are more than 5 — it may take a moment.
- **Empty calendar**: If nothing is scheduled, say so directly. Offer to draft posts if appropriate.
- **Recurring / synced posts**: Grouped posts show as one unit — note this if multiple platforms are covered by a single grouped post.
- **Time zones**: Scheduled times are returned in UTC. If the user's timezone is known, convert. Otherwise, note that times shown are UTC.
