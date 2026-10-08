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
| `NOT_APPROVED` | Posts with no approvals yet |
| `PARTIAL_APPROVED` | Posts with some but not all required approvals |
| `REQUESTED_BY_ME` | Posts where this user requested approval from others |

If the user wants a broader view, query `NOT_APPROVED` and `PARTIAL_APPROVED` together.

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

Do NOT offer to approve posts — approval actions are not available via the connector.

---

## Edge cases

- **Many workspaces**: If `list_workspaces` returns more than 10, ask the user to confirm scope before fetching each one. Fetching 20+ workspaces sequentially is slow and may not be what they want.
- **No workspace specified**: Default to checking the 5 most recently active workspaces unless the user says "all clients."
- **Scheduled posts with errors**: If `WITH_ERRORS` posts appear in results, call them out separately — these are likely blocking issues.
