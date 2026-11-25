---
name: sg-manage-roles
description: Guided flow for creating, changing and deleting StackGuardian custom roles with the create_role / update_role / delete_role tools — turning "let team X read/run workflows in group Y" into the right permission names and scopes. Use when the user wants a new role, wants to widen or narrow what a role can do, asks why a role grants nothing, or wants to retire a role.
---

# Manage Roles — Guided Flow

A StackGuardian **role** is a named bundle of **permissions**. Each permission
is one platform capability (`GetWorkflow`, `CreateWorkflowRun`, ...) plus a
**scope**: for every placeholder the permission carries, a list of full-match
regex **patterns** over resource IDS. Five **predefined roles** (ADMIN, DEV,
SEC, OPS, READ_ONLY) are code and cannot be changed; everything else is a
**custom role**. Roles are allow-only and additive — a user with several
roles gets the union. Only ADMIN can manage roles. Follow the steps IN ORDER.
Never surface parameter names like `resourceName` or `<wfGrp>` to the user;
say "the role's name", "workflow group".

**What these tools can't do — say so up front, before building anything:**
they can't list users, look up a person, assign a role to anyone, or show a
role's current permissions. "Give Alice read access to group X" ends with
the user assigning the role in the dashboard's Access Management, and any
change to an existing role needs its current patterns from the user.

## The rules that make a role silently wrong

1. **Patterns match IDS, not display names.** The scope is matched against
   the URL segment, and an id can differ from the name: a group created in
   the dashboard as `gitops` may have the id `gitops-y8pf2mb1`. A pattern
   `gitops` would then save fine and grant nothing. Look every named group,
   workflow, connector, policy or secret up with
   `search_orchestrator_resources` and use the last segment of its
   `ResourceId`. A NESTED group is its full id-path: the ids after each
   `/wfgrps/` in its `ParentId`, then its own id, joined by `/`
   (`company-x1/team-y2`). The bare leaf grants nothing on it, and would
   match an unrelated top-level group of that id. Roles created by
   `create_role` have id = name.
2. **Patterns are full-match, anchors implicit.** `team-a` grants exactly
   `team-a`; write `team-a-.*` for a prefix. Never `^` or `$` — the platform
   strips them from anywhere, so `[^/]+` would invert. No inline flags
   (`(?i)`), named groups, backreferences, nested repetition
   (`(?:x+)+`) or big counted repeats (`a{5000}`): the tool refuses them.
3. **GET on a group path grants every ancestor, no descendants.**
   `company/team` also grants `company`, never `company/team/project`. The
   platform splits a group pattern at each `/`, so a `/` may only separate
   whole segments: not inside `[...]` or `(...)`, and not with a top-level
   `|` (use one row per path).
4. **Root-level Create* patterns match a NAME; CreateNestedWorkflowGroup
   matches a PATH** (`parent/child-.*`).
5. **User management matches a principal** via `<loginType>` (local|sso)
   and `<principalId>` (an email pattern like `.*@example\.com`, or an SSO
   group name). `<entityType>` must be `.*`: the platform ignores it, so
   `group` would not keep email users out. It also needs `GetRole` scoped
   to the roles the holder may assign — that scope IS the list of roles
   they can hand out, so `.*` lets them invite admins.

Scope lists are index-parallel rows: `{"<wfGrp>": ["prod", "dev"], "<wf>":
[".*", "x-.*"]}` is two grants, (prod, all) and (dev, x-*). Use `a|b` inside
one pattern for alternatives; all lists must be the same length. Any ONE row
that is all `.*` makes the whole permission org-wide.

## Step A — Translate the ask into permissions

1. Check whether a role already does the job:
   `search_orchestrator_resources(resourceTypes=['ROLE'])` (names and
   descriptions only). Reusing one beats creating a near-duplicate.
2. Ask what the holder should be able to DO and WHERE, then resolve every
   WHERE to an id (rule 1):

| User says | Permissions (scope the placeholders they named, `.*` for the rest) |
| --- | --- |
| see workflows in group G | `GetWorkflowGroup` {G}, `GetWorkflow` {G, .*}, `GetWorkflowRun` {G, .*, .*} |
| run workflows in G | + `CreateWorkflowRun` {G, .*}, `GetWorkflowRunLogs` |
| create workflows in G | + `CreateWorkflow` {G, .*} (pattern = the new workflow's name) |
| manage a group's stacks | `GetStack`, `CreateStack`, `UpdateStack`, `CreateStackRun`, `GetStackRun` |
| use connector C | `GetIntegration` {C} ("connector" is `Integration` on the wire) |
| read secrets/policies | `GetSecret` {name}, `GetPolicy` {name} |
| invite / remove users | `InviteUser`/`UpdateUser`/`DeleteUser` + `GetRole` {assignable roles} — privileged |
| manage roles / API keys / billing | `CreateRole`… / `*APIAccess` (regenerating a key is `UpdateAPIAccess`) / `ManageBilling` — privileged |

An unknown permission name returns the full catalog grouped by area
(`availablePermissions`) with `didYouMean`; a missing placeholder returns
`requiredPlaceholders`. There is no "everything" shorthand — an admin-like
role lists every permission explicitly.

## Step B — Create

1. Ask for a name: letters, digits, `_`, `-` (it becomes the permanent id;
   no rename). Not a predefined name.
2. If any permission is privileged (roles, users, API access, billing, or
   `GetRole` next to user management), tell the user plainly that holders
   could change who can do what, and only on an explicit yes call with
   `confirmPrivileged=true`. If a write permission (anything but Get*/List*)
   is scoped to ALL resources, the tool asks for `confirmOrgWide=true`:
   first try to narrow the scope to what the user actually said; confirm
   only when "everything" is what they mean.
3. Call `create_role(resourceName, permissions=[{permission, scope}, ...],
   description?, tags?)`.
4. Walk the user through the returned `permissions` table row by row, in
   words ("workflow group prod, any workflow") — it is the only way they
   catch a wrong pairing — and relay `warnings`.
5. Assignment has no tool here: the user assigns the role to people or SSO
   groups in the dashboard's Access Management. Changes apply on the
   holder's next request.

## Step C — Change

1. Find the id: `search_orchestrator_resources(resourceTypes=['ROLE'])` or
   the `availableRoles` list a tool error returns. Ids are case-sensitive.
2. `setPermissions` REPLACES a stored entry of the same permission name in
   full, and no tool shows the stored patterns. Before replacing one, ask
   the user for its current patterns (the role's page in the dashboard's
   Access Management) and resend them along with the change — otherwise
   widening `prod` to `prod|dev` silently drops whatever else was there.
   Adding a permission the role doesn't hold, `removePermissions`, and
   `description`/`tags` need no read. Never use `delete_role` to read a role.
3. `update_role(roleId, setPermissions=[...], removePermissions=[names],
   description?, tags?)`. Untouched permissions are kept. Writing a
   privileged permission (new or rewritten) needs `confirmPrivileged`; an
   org-wide write scope needs `confirmOrgWide`. The response's
   `permissions` is the full table after the write — show it.
4. A V3.BETA role is rewritten as equivalent V4 rows on its first permission
   edit (`migratedFromV3`); say so. A role stored with NO version grants
   nothing today: ANY update turns all of its permissions on, so the tool
   gates them all — tell the user that before confirming. An update that
   would leave zero permissions is refused — use Step D.
5. A stored permission with an EMPTY scope is an unrestricted grant; the tool
   warns — offer to scope it.

## Step D — Delete

1. Call `delete_role(roleId)` WITHOUT `confirmDelete`. The error carries
   `holders` (users and SSO groups bound to it, with their other roles),
   `permissionsSnapshot` and the `cascade` note.
2. Tell the user: deletion strips the role from every holder atomically, a
   holder with no other role loses all access, API-key bindings are not
   cleaned, and there is no undo (keep the snapshot to recreate).
3. Only after an explicit yes, call `delete_role(roleId, confirmDelete=true)`.
   Predefined names are refused outright.

## Why does my role grant nothing?

Ask the user to open the role in the dashboard and read you its permissions.
Then check: a pattern is a display name where the id differs (rule 1); an
exact name where a prefix was meant (rule 2); a GET on a child path was
expected to cover descendants (rule 3); user management without `GetRole`
(rule 5); the role was stored without a version (the gateway ignores it
until an update rewrites it); the holder's token predates an SSO group
change (needs a fresh login).
