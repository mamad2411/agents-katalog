---
name: jira-automation-rules
description: "Complete protocol for designing, building, debugging, and hardening Jira Cloud
    native automation rules — triggers, conditions, branches, smart values, web requests,
    loop guards, dedupe workarounds, and field/screen prerequisites. Use when: building
    Jira automation from scratch, syncing fields across parent/subtask hierarchies,
    debugging automation audit logs, or replacing Comment actions with REST API web requests."
category: Atlassian Jira
---

# Jira Automation Rules Skill

> **Skill ID:** `jira-automation-rules`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

Complete reference for designing, building, debugging, and hardening **Jira Cloud native
automation rules** — the built-in no-code automation engine under
**Project settings → Automation** (project-scoped) or
**Jira settings → Automation** (global/multi-project scope).

***

## Environment & Dependencies

### 1.1 Access Requirements

| Requirement | Verification |
| :--- | :--- |
| Jira Cloud instance | `https://<org>.atlassian.net` — Cloud only; Server/DC UI differs |
| Project Admin role | **Project settings → Automation** must be visible |
| Rule Actor account | Must have **Edit Issues** and **Transition Issues** permissions |
| Field on screen | Target fields must be added to the issue type's Edit screen before automation can set them |

### 1.2 Field / Screen Prerequisite (Common Blocker)

Before any **Edit work item** action can set a field (e.g., `Due date` on Subtasks),
that field must be present on the issue type's Edit screen:

1. **Project settings → Issue types → `<IssueType>`** → confirm the field appears.
2. If missing: drag it from the right panel → **Save**.
3. Alternatively: **Project settings → Screens → `<IssueType>` Edit Screen** → add the field → **Save**.

Symptom when missing:

```text
Edited issue successfully, however some of the set fields aren't available.
Fields ignored: Due date (duedate)
```

### 1.3 API Token (Required for Send Web Request)

The **Send web request** action makes a real external HTTP call and requires explicit
Basic Auth credentials — the rule actor's session does **not** carry over:

1. Go to `https://id.atlassian.com/manage-profile/security/api-tokens`
2. **Create API token** → name it (e.g., `Jira Automation`) → copy the token.
3. Generate Base64 credentials (run locally, never commit output):

   ```bash
   echo -n "<email>@<domain>.com:<api-token>" | base64
   ```

4. Add to the web request **Headers**:

   | Header | Value |
   | :--- | :--- |
   | `Authorization` | `Basic <base64-string>` |
   | `Content-Type` | `application/json` |

> **Security**: Use a dedicated service account with minimal permissions (comment-only)
> rather than a personal account where possible.

***

## Rule Anatomy

### 2.1 Building Blocks

| Block | Purpose |
| :--- | :--- |
| **Trigger** | What fires the rule (field change, issue created, scheduled, webhook, etc.) |
| **Condition** | Boolean gate — rule only proceeds if condition passes |
| **Branch** | Fan-out — execute nested steps for each related issue (subtasks, linked issues, etc.) |
| **Action** | Performs work — edit fields, comment, transition, send web request, etc. |
| **Log** | Diagnostic — renders smart values to audit log; remove after debugging |

### 2.2 Rule Details Panel (top-right)

| Setting | Recommended Value | Notes |
| :--- | :--- | :--- |
| **Actor** | Your account (or dedicated service account) | Default `Automation for Jira` lacks REST API permissions for web requests |
| **Allow rule trigger** | Off (default) | Prevents actions taken by the rule from re-triggering itself (loop guard) |
| **Scope** | This project | Upgrade to Global only when rule applies to multiple projects |

***

## Smart Values Reference

### 3.1 Key Smart Values

| Smart Value | Resolves To | Notes |
| :--- | :--- | :--- |
| `{{triggerIssue.key}}` | Triggering issue key (e.g., `ALP-1`) | Always the parent in a branch |
| `{{triggerIssue.duedate}}` | Triggering issue due date (`yyyy-MM-dd`) | Verified working; prefer over `fieldChange.to` |
| `{{fieldChange.to}}` | New field value after change | Also resolves correctly for due date |
| `{{fieldChange.to.jiraDate}}` | Empty in some instances | Do **not** use — unreliable |
| `{{now}}` | Current UTC timestamp (e.g., `2026-05-26T19:10:54.6+0000`) | Use for unique comment text |
| `{{now.toEpochSecond}}` | Empty in some instances | Do **not** use — unreliable |
| `{{issue.key}}` | Current issue key **inside a branch** | Resolves to the subtask key, not the parent |
| `{{issue.self}}` | Full REST API URL of current issue (v2) | e.g., `https://<org>.atlassian.net/rest/api/2/issue/15133` |
| `{{issue.self.replaceAll("/rest/.*", "")}}` | Jira base URL | Strips `/rest/…` suffix; use to build web request URLs dynamically |
| `{{baseUrl}}` | Does not resolve in web request URLs | Hard-code or derive from `{{issue.self}}` instead |

### 3.2 Deriving the Base URL (No Hardcoding)

```text
{{issue.self.replaceAll("/rest/.*", "")}}/rest/api/3/issue/{{issue.key}}/comment
```

`{{issue.self}}` is always available inside a branch and carries the
`https://<org>.atlassian.net` prefix. Stripping `/rest/.*` leaves the base URL
without hardcoding the domain.

***

## Worked Example — Sync Parent Due Date to Subtasks

This rule propagates a parent issue's due date (add / change / remove) to all
non-`Done` subtasks, with a REST API audit comment on each subtask.

### 4.1 Complete Rule

**Location:** Project settings → Automation → Create rule

***

#### Rule Name

`Sync Due Date from Parent to Subtasks`

#### Description

`When a parent issue's due date is added, changed, or removed,
propagate the same value to all open subtasks and leave an audit comment.
Fails hard if either edit or comment fails.`

***

#### Step 1 — Trigger: Field value changed

| Setting | Value |
| :--- | :--- |
| Fields to monitor | `Due date` |
| Change type | `Any changes to the field value` |
| For | `Edit issue` and `Create issue` |

> Including **Create issue** handles the case where a parent is created with a due
> date already set. If subtasks do not exist yet, the branch iterates zero times —
> harmless.

***

#### Step 2 — Condition: Issue fields condition

| Setting | Value |
| :--- | :--- |
| Field | `Issue Type` |
| Condition | `does not equal` |
| Value | `Subtask` |

> **Loop guard** — prevents the rule from firing when a subtask's own due date
> changes. Combined with **Allow rule trigger = Off** for belt-and-suspenders protection.

***

#### Step 3 — Branch: Related issues

| Setting | Value |
| :--- | :--- |
| Type | `For each: Subtasks` |

All steps below sit **inside** this branch.

***

#### Step 4 — Condition (inside branch): Issue fields condition

| Setting | Value |
| :--- | :--- |
| Field | `Status` |
| Condition | `does not equal` |
| Value | `Done` |

> Skips completed subtasks. Adjust to your project's statuses (e.g., `Closed`,
> `Resolved`) if your workflow has more terminal states.

***

#### Step 5 — Action (inside branch): Edit work item

| Setting | Value |
| :--- | :--- |
| Choose fields to set | `Due date` |
| Due date smart value | `{{triggerIssue.duedate}}` |
| More options — Send email notification | Off |

> If the parent's due date is cleared, `{{triggerIssue.duedate}}` resolves to
> empty and the subtask's due date is also cleared.
>
> **Prerequisite**: `Due date` must be on the Subtask Edit screen — see §1.2.

***

#### Step 6 — Condition (inside branch): JQL condition

| Setting | Value |
| :--- | :--- |
| JQL | `issue = {{issue.key}} AND due = {{triggerIssue.duedate}}` |

> Verifies the edit actually took effect. If **Edit work item** silently failed
> (field not on screen, workflow restriction), this condition fails and blocks the
> comment — preventing a false audit trail.
>
> **Note**: **Work item fields condition** does NOT accept smart values for Date
> fields (date picker only). Use **JQL condition** instead.

***

#### Step 7 — Action (inside branch): Send web request

| Setting | Value |
| :--- | :--- |
| URL | `{{issue.self.replaceAll("/rest/.*", "")}}/rest/api/3/issue/{{issue.key}}/comment` |
| Method | `POST` |
| Web request body | `Custom data` |
| Content type | `application/json` |
| Header: `Authorization` | `Basic <base64-credentials>` (see §1.3) |
| Header: `Content-Type` | `application/json` |
| Delay until response | On |
| Continue on non-200 | Off |

**Body:**

```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "[{{now}}] Due date synced from parent {{triggerIssue.key}} \u2192 {{triggerIssue.duedate}}"
          }
        ]
      }
    ]
  }
}
```

> **Why web request instead of Comment action?** Jira Automation's built-in<br>
> **Comment on issue** action has a permanent per-rule dedupe memory — it refuses
> to post a second comment on any issue the rule has previously commented on,
> regardless of content, even after deleting the comments or toggling the rule
> off/on. The **Send web request** action bypasses this entirely.
>
> **Delay on**: prevents race conditions when iterating multiple subtasks.
>
> **Continue off**: makes comment failure a hard stop — the run is marked **Failed**
> in the audit log rather than silently skipping.

***

#### Rule Details Panel

| Setting | Value |
| :--- | :--- |
| Actor | Your Jira account (or service account with Edit Issues and comment permissions) |
| Allow rule trigger | Off |
| Scope | This project |

***

#### Final Visual Structure

```text
WHEN  Field value changed → Due date  (Create + Edit)
IF    Issue Type ≠ Subtask                                   ← loop guard
  FOR EACH subtask
    IF    Status ≠ Done                                      ← skip terminal subtasks
    THEN  Edit work item → Due date = {{triggerIssue.duedate}} (notifications off)
          JQL condition  → issue = {{issue.key}} AND due = {{triggerIssue.duedate}}
          Send web request → POST /rest/api/3/issue/{{issue.key}}/comment
                             (Basic Auth, delay on, continue off)
```

***

#### Behavior Matrix

| Scenario | Outcome |
| :--- | :--- |
| Edit and comment both succeed | Run = Success, comment posted on subtask |
| Edit fails silently (field not on screen) | JQL condition fails → comment blocked → run = Some errors |
| Edit succeeds, comment fails (auth/network) | Web request fails → run = Some errors |
| Subtask status = Done | Skipped entirely — no edit, no comment |
| Parent due date cleared | Subtask due date also cleared (`{{triggerIssue.duedate}}` = empty) |

***

## Debugging Protocol

### 5.1 Add Log Actions for Smart Value Inspection

Insert a **Log action** before any suspect step:

```text
URL WILL BE: {{issue.self.replaceAll("/rest/.*", "")}}/rest/api/3/issue/{{issue.key}}/comment
DUE DATE: [{{triggerIssue.duedate}}]
NOW: [{{now}}]
ISSUE KEY: [{{issue.key}}]
```

Check **Project settings → Automation → Audit log → expand run → Log action output**.
Remove all Log actions after debugging.

### 5.2 Audit Log Status Meanings

| Status | Meaning |
| :--- | :--- |
| **Success** | All steps executed without error |
| **Some errors** | One or more steps failed; rule continued |
| **Failed** | A step with continue-on-error = Off failed; rule stopped |
| **Conditions not met** | A condition blocked execution (not an error) |

### 5.3 Common Failures and Fixes

| Symptom | Root Cause | Fix |
| :--- | :--- | :--- |
| `Fields ignored: Due date` | Field not on Subtask Edit screen | Add field — see §1.2 |
| `No new comment added since this issue has been commented on before` | Built-in Comment action dedupe | Replace with Send web request — see §4.1 Step 7 |
| `404 Issue does not exist or you do not have permission` | Web request missing Authorization header | Add `Basic <base64>` header — see §1.3 |
| `500 ProtocolException: Target host is not specified` | `{{baseUrl}}` does not resolve in web request URL | Derive base URL from `{{issue.self.replaceAll("/rest/.*", "")}}` — see §3.2 |
| `400 No content to map to Object due to end of input` | Web request body empty or not set to Custom data | Set body type to Custom data, paste JSON body directly |
| `{{now.toEpochSecond}}` renders empty | Transformation not supported in this Jira instance | Use `{{now}}` directly |
| `{{fieldChange.to.jiraDate}}` renders empty | Transformation not supported in this Jira instance | Use `{{triggerIssue.duedate}}` or `{{fieldChange.to}}` directly |
| Comment posts but smart values render as literal `{{...}}` text | Input field in rich-text mode, not smart-value mode | Click the `{{}}` icon or Insert smart value button in the UI |

***

## Design Decisions and Rationale

### 6.1 Why `{{triggerIssue.duedate}}` Over `{{fieldChange.to}}`

Both resolve correctly for the `Field value changed → Due date` trigger.
`{{triggerIssue.duedate}}` is more self-documenting (explicitly reads from the parent)
and works correctly in the JQL verification condition.

### 6.2 Why JQL Condition to Verify Edit

Jira's **Edit work item** action has no fail-on-error toggle — failures are silent.
A JQL condition immediately after the edit (`issue = {{issue.key}} AND due = {{triggerIssue.duedate}}`)
acts as an assertion: if the edit did not take effect, the condition fails and blocks
downstream actions, preventing false audit comments.

### 6.3 Why Send Web Request Instead of Comment Action

Jira Automation's built-in **Comment on issue** action maintains a permanent per-rule
dedupe registry. It refuses re-posting even if the prior comment was deleted or the rule
was toggled off/on. The **Send web request** action with an ADF body bypasses this
entirely. `{{now}}` is included in the comment body as a human-readable timestamp.

### 6.4 Edit Notification Off

The subtask assignee already receives notifications from watching the parent. A second
email per subtask per due-date change creates noise. Disable via
**Edit work item → More options → Send email notification = Off**.

### 6.5 Trigger For: Create issue

Including **Create issue** in the trigger handles due dates set at creation time.
If the parent has no subtasks yet, the branch iterates zero times — safe, no error.
If subtasks are auto-created by a companion rule, they should inherit the due date
directly in their creation action using `{{triggerIssue.duedate}}`.

***

## SSOT Compliance

| Standard | Skill |
| :--- | :--- |
| Jira acli CLI operations | [`../jira-acli-operations/SKILL.md`](../jira-acli-operations/SKILL.md) |
| Markdown linting | [`../markdown-generation/SKILL.md`](../markdown-generation/SKILL.md) |
| Skill metadata structure | [`../skill-factory/SKILL.md`](../skill-factory/SKILL.md) |

***

## Related Conversations and Traceability

| Session | Date | Context |
| :--- | :--- | :--- |
| Jira automation from scratch — due date sync | 2026-05-27 | Built complete parent-to-subtask due date sync rule; debugged field-not-on-screen, Comment dedupe, web request auth, base URL derivation, JQL verification pattern |
