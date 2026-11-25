---
name: pending-approvals-roundup
description: >
  Fetch and summarize all posts pending approval across one or more Planable workspaces.
  Use this skill whenever the user asks about approvals, wants to know what's waiting
  for review, says things like "what needs my approval", "show me pending posts",
  "what's waiting for sign-off", "approval queue", "morning check-in", or
  "what posts are stuck". Also activate when the user asks for a daily or weekly
  content status across clients. Always use this skill for approval-related queries
  that touch Planable.
---

# Pending approvals roundup

Surface all posts waiting for approval across one or more Planable workspaces, so nothing gets missed.

## How this skill works

1. Identify which workspaces to check
2. Fetch posts filtered by approval status
3. Summarize clearly — grouped by workspace/client, with post previews and context

---

## Step 1: Scope the check

Ask (or infer from context):

- **Which workspaces?** — a specific client, a list, or all workspaces
- **Whose approvals?** — posts pending the user's own approval (`PENDING_MY_APPROVAL`) or all pending posts (`NOT_APPROVED`, `PARTIAL_APPROVED`)

**Default behavior if not specified:** fetch `PENDING_MY_APPROVAL` across all workspaces (or the most recently active ones if there are many).

---

## Step 2: Fetch pending posts

For each workspace in scope:

```
list_posts(
  workspaceId,
  approvalStatus: ["PENDING_MY_APPROVAL"]   // or NOT_APPROVED, PARTIAL_APPROVED
)
```

**Approval status reference:**
| Status | Meaning |
|---|---|
| `PENDING_MY_APPROVAL` | Posts where this user is a required approver |
| `NOT_APPROVED` | Posts that are not fully approved yet (partially approved ones included) |
| `PARTIAL_APPROVED` | Posts with some but not all required approvals |
| `REQUESTED_BY_ME` | Posts where this user requested approval from others (can include posts approved since) |

If the user wants a broader view, query `NOT_APPROVED` and `PARTIAL_APPROVED` together.

Results are paginated (25 posts per page by default; pass `limit: 100` to need fewer calls). While `hasMore` is true, call `list_posts` again with `offset: nextOffset` so no pending post is missed. For the broader view, the first page's `totalCount` says how many posts match: if there are more than about 50, show the count and the most urgent posts, and ask before listing them all.

---

## Step 3: Organize and present results

**If results exist**, group by workspace (client). For each post show:
- Platform/page name
- Post preview (first 100–150 chars of `textPreview`)
- Scheduled date (if set) — flag posts that are scheduled soon (within 24–48 hours)
- Current approval status
- Number of approvals received vs. required (if available)

**Sort order within each workspace:** most urgently scheduled first, then by creation date.

**Format:**

```
📋 [Workspace name]
  • [Platform] — "[Post preview...]"
    Scheduled: [date] ⚠️ (if within 48h)
    Status: [approval status]

  • [Platform] — "[Post preview...]"
    No date set
    Status: Partially approved (1/2)
```

**If no pending posts**, say so clearly. Don't pad the response.

---

## Step 4: Optional follow-up actions

After showing results, offer:
- "Want me to show you the full text of any of these?"
- "Should I check a specific workspace in more detail?"

- "Want me to approve any of these, or send one back with a comment?" — approve with `approve_post`. To send a waiting post back, add the reason with `create_comment` (`teamOnly: true` keeps it from the client). Do not use `disapprove_post` here: it only revokes an approval a post already has, and on a post that is still waiting it changes nothing.

Approve only the posts the user names, after they confirm. This needs an approval workflow in the workspace (`approvalWorkflow` from `get_workspace_details` is not "none") and the user's approve permission. Before approving, mention that approving can auto-schedule the post if the workspace is set up that way, and that a post with a `groupId` (created for several pages at once) is approved together with every post in its group.

---

## Edge cases

- **Many workspaces**: If `list_workspaces` returns more than 10, ask the user to confirm scope before fetching each one. Fetching 20+ workspaces sequentially is slow and may not be what they want.
- **No workspace specified**: Default to checking the 5 most recently active workspaces unless the user says "all clients."
- **Posts with problems**: posts that failed to publish (`PUBLISHED_WITH_ERRORS`) and posts with incompatible content (`WITH_ERRORS`, such as an Instagram post without media) are likely blocking issues — call them out separately if the user asks for them or they show up.
