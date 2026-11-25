---
name: uniffy-e2e-flows
description: |
  Run disciplined end-to-end flows against the live Uniffy app through the project's Playwright MCP infrastructure. Covers authentication, content creation across domains, and the full permission and sharing model, including verification as a second user. Use when asked to test auth, login, permissions, sharing, access control, creation or CRUD, smoke-test the app, exercise each domain, or run a create-and-share flow. Use `uniffy-playwright` instead for a one-off browser inspection or single-bug reproduction. Skip for unit or integration tests, backend-only work, or when the dev stack is not running and the user has not asked to start it.
---

# Uniffy End-to-End Flow Testing

This skill turns the Playwright MCP browser into a disciplined E2E tester for the three flows that touch every domain: **auth**, **creation**, and **permissions**. It is the methodology layer; `uniffy-playwright` is the prerequisite that documents the MCP connection, the core tools (`browser_navigate` / `browser_snapshot` / `browser_evaluate` / `browser_click` / `browser_console_messages` / `browser_network_requests`), and the low-level selector gotchas. Read that first for anything about *how* to talk to the browser; this file covers *what* to test and *how to prove it*.

## Preflight (do this before any flow)

1. Confirm the dev stack is up: `docker ps | grep uniffy-dev` and `curl -s -o /dev/null -w "%{http_code}" http://localhost:5173` (expect 200). Backend on `:8000`. **Two MCP browser containers**: `uniffy-mcp-playwright` (`playwright` server on `:8931`) and `uniffy-mcp-playwright-b` (`playwright-b` server on `:8932`). The second is a fully isolated browser for multi-user flows - see "Two-browser setup" below. If the `playwright-b` tools are missing, start it (`docker compose --profile dev up -d mcp-playwright-b`) and reconnect MCP (`/mcp`) or restart the agent session.
2. The browser reaches the UI at `http://host.docker.internal:5173` (NOT localhost - that's the container's localhost). Backend at `http://host.docker.internal:8000`.
3. **Do NOT edit backend or frontend source while a flow is running.** The dev backend auto-reloads on any file save and will drop your auth session mid-test (you bounce to `/auth`). The Vite dev server HMRs frontend edits the same way. If you must change code, expect to re-login afterward.
4. **Never `docker restart uniffy-dev-backend` to pick up a code change** - it auto-reloads, and a manual restart drops every session (and can 500 in-flight requests during the reload window). Only restart for a genuinely stuck container.

## Fixtures (dev seed - `src/uniffy/db/seed_dev.py`)

All users share the password `admin` (or `$INITIAL_ADMIN_PASSWORD` if set). Org is **"Uniffy"** (the workspace card on `/welcome`).

| Email | Org role | Groups | Use as |
|---|---|---|---|
| `admin@uniffy.io` | OWNER + system admin | - | The actor/owner who creates + shares |
| `alice@uniffy.io` | MEMBER | Engineering | Engineering-grant subject |
| `bob@uniffy.io` | MEMBER | Engineering (group admin) | Engineering-grant subject |
| `charlie@uniffy.io` | MEMBER | Engineering + Product | Multi-group resolution |
| `diana@uniffy.io` | MEMBER | Product (group admin) | Negative control vs Engineering grants |
| `eve@uniffy.io` | MEMBER | Product | Direct-grant subject / negative control |

Negative-control rule: every seed member belongs to a group, so there is no "in no group" user. For a **direct user grant** to `eve`, any other ungranted user (e.g. `diana`) is a clean control. For an **Engineering group grant**, `diana`/`eve` are controls (Product-only). For a **Product group grant**, `alice`/`bob` are controls.

Two groups exist: **Engineering** (alice, bob, charlie) and **Product** (charlie, diana, eve).

## Login + switch-user recipe

Auth inputs are React-controlled - set them via the native value setter, not `browser_type`:

```js
// browser_evaluate, on /auth
const setVal = (el, v) => {
  const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  set.call(el, v);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
};
setVal(document.querySelector('input[type="email"], input[autocomplete="email"]'), 'admin@uniffy.io');
setVal(document.querySelector('input[type="password"]'), 'admin');
```

Then `browser_click [data-testid="auth-submit-login"]`, then select the workspace (click via `browser_evaluate` - see below; `browser_click` with `ref=eXX` throws "Unknown engine ref"):

```js
[...document.querySelectorAll('button')].find(b => /Uniffy/.test(b.textContent) && /owner/i.test(b.textContent))?.click();
```

### Two-browser setup (preferred for any multi-user flow)

Use the two MCP containers as two independent users. Each is a separate Chromium with its own cookie jar + `localStorage`, so the sessions never collide - no sign-out churn, and you can `browser_navigate`/reload either browser freely.

- **Browser A = `playwright` server** (`:8931`): the persistent **actor/owner** (e.g. `admin` or `alice`). Stays logged in for the whole flow.
- **Browser B = `playwright-b` server** (`:8932`): the **subject/observer**. Log in whichever grantee or control user you're currently checking.

Log each in once with the recipe above (each browser navigates to `http://host.docker.internal:5173` independently). To check a *different* subject, just re-login browser B - browser A is untouched. **This is REQUIRED, not optional, for live cross-session updates** (e.g. A shares/creates -> B's sidebar/board must update without a reload): both sessions have to be live at the same time, which a single browser cannot do.

### Single-browser fallback (only without the 2nd container)

A single browser shares one cookie jar, so two users can't truly coexist - this is fragile, use it only when browser B is unavailable. **Switch users by signing out then logging in as the next user:**

```js
// browser_evaluate - clear and bounce to /auth, then run the login recipe with new creds
[...document.querySelectorAll('button')].find(b => /sign out|log ?out/i.test(b.textContent))?.click();
```

If no logout button is reachable, `localStorage.removeItem('persist:root')` then navigate to a protected route; the auth guard redirects to `/auth`. After re-login, re-select the org. (The two-tab variant from `uniffy-playwright` works too, but the access token is in-memory per tab while `persist:root` is shared, so a full reload silently swaps a tab's identity - the two-container path avoids all of that.)

## Reusable helper snippets

```js
// click a control by visible text (browser_click ref= selectors are unreliable)
const clickByText = (re) => { const b=[...document.querySelectorAll('button')].find(x=>re.test(x.textContent)); if(b) b.click(); return !!b; };

// which access mode is selected in the shared sharing panel
const selectedAccessMode = () => [...document.querySelectorAll('button')]
  .filter(b=>/Only owner|Invited people|Everyone in org/.test(b.textContent))
  .find(b=>b.className.includes('border-primary'))?.textContent.trim().split('\n')[0];

// surface any toast (errors, confirmations)
const readToasts = () => [...document.querySelectorAll('[data-sonner-toast]')].map(t=>t.textContent.trim());
```

For RPC verification use `browser_network_requests` with a filter, e.g. `MembersService|ListMembers`, `ProjectsService`, `AuthService`. Check the status code; pull the body with the network-request-by-number tool when you need the policy payload.

## Playbook A - Auth

| # | Case | Expected |
|---|---|---|
| 1 | Login, valid creds | `/auth` -> `/` in the last used org, or `/auth` -> `/welcome` -> pick org -> `/` when none is picked yet |
| 2 | Login, wrong password | stays on `/auth`, error toast, no token |
| 3 | Protected route while logged out | navigate to `/notes` after logout -> redirect to `/auth` |
| 4 | Logout | tokens cleared, redirect to `/auth`, browser-back does not restore the app |
| 5 | Org selection | the workspace card sets org context; landing shows that org |
| 6 | Register (if open) | switch to register tab, submit -> `/welcome` (with a create card when the deployment allows it) |
| 7 | Token refresh | over a long session, `AuthService/RefreshToken` fires and succeeds silently (network tab); access token is memory-only (never in localStorage) |
| 8 | MFA (if enabled) | TOTP challenge after password; recovery path. Planned feature - test only if the flow is present |

Capture console errors (`browser_console_messages level:error all:true`) after each case; ignore HMR `Failed to load module script ... text/html` noise (dev-server reload artifacts), flag anything else.

## Playbook B - Creation (per domain)

Create via the real UI, then **reload** and confirm it persisted. Delete in cleanup.

| Domain | Create entry point | Verify |
|---|---|---|
| Notes | `/notes` -> new note in tree | title saves, node in tree, opens at `/notes/:id` |
| Files | `/files` -> upload | row appears, thumbnail/size correct |
| Projects | `/projects` -> "New" -> name + "Create Project" | appears in sidebar, settings reachable |
| Tasks | open a project -> "New Task" | row in Table/Board, subtasks nest |
| Calendar | `/calendar` -> create event | block on the grid at the right date |
| Chat | `/chat` -> create channel / send a message | message renders, persists on reload |
| Agents | `/agents` -> create agent | appears in list, config opens |
| Prompts | `/agents` prompts view -> create | appears in prompt list |

For each: create -> assert in list -> reload -> still present -> note the id/URN for cleanup.

## Playbook C - Permissions (the core)

### Model cheat-sheet
- **Access modes**: `OWNER_ONLY` ("Only owner" = personal) - only the owner; `EXPLICIT_MEMBERS` ("Invited people") - owner + listed members/groups; `OPEN_TO_ORG` ("Everyone in org" + a baseline role) - all org members inherit the baseline, explicit members elevate or block.
- **UNSPECIFIED** ("Use organization default") inherits the org default for that content type (the panel shows the *resolved* mode via `effective_access_mode`). The org PROJECT default is OPEN_TO_ORG/EDITOR; many other types default OPEN_TO_ORG too - so an *inherited* item is usually org-wide, not personal.
- **Role order**: VIEWER < COMMENTER < EDITOR < ADMIN < OWNER. **BLOCKED beats everything** (even ownership, even OPEN_TO_ORG).
- **No org/admin content bypass.** `admin@uniffy.io` being org owner + system admin does NOT let it see another user's personal content. If admin can't see a member's private note, that's correct - not a bug. (Only exceptions: an audited SupportSession, and chat moderation.)
- **Adding a member to a personal item auto-widens it to "Invited people"** (you can't have members under OWNER_ONLY). **Narrowing back to "Only owner" with members present** prompts a confirm and removes them.

### Share entry points (all render the shared `AccessPolicyPanel`)
| Domain | Open sharing |
|---|---|
| Projects | `/projects/:id/settings?section=members` |
| Notes | note editor header -> Share |
| Files / Folders | file details panel / list row -> Share |
| Agents / Prompts / Provider keys | the agents views -> Share |
Tasks inherit the parent project's policy (no own sharing UI).

### The canonical per-domain permission test
Run this loop for each domain you're asked to cover. Each grant is only proven by **logging in as the target user**.

1. As **admin**, create content X (projects start as explicit "Only owner").
2. **Negative baseline**: sign in as **diana** -> X is not visible / not accessible. (Proves no-bypass + private-by-default.)
3. As **admin**, open X's sharing -> add **eve** as VIEWER. Confirm the mode auto-flips to "Invited people" and the hint showed.
4. Sign in as **eve** -> X is visible, **read-only** (no edit/delete affordance).
5. As **admin**, change eve to EDITOR -> as **eve**, editing now works.
6. As **admin**, set "Everyone in org" baseline VIEWER -> as **diana** (never a member) -> X now visible (inherited baseline).
7. As **admin**, add diana as BLOCKED -> as **diana**, X disappears despite OPEN_TO_ORG.
8. As **admin**, **group grant**: set "Invited people" and add the **Engineering** group as EDITOR -> alice/bob/charlie can edit; eve (Product-only) cannot.
9. As **admin**, narrow to "Only owner" -> confirm dialog ("removes N members") -> as eve, X is gone.
10. **Cleanup**: delete X, remove members, restore original mode.

### Matrix to drive coverage
Rows = the steps above (personal-private, explicit VIEWER, explicit EDITOR, OPEN_TO_ORG baseline, BLOCKED, group grant, narrow). Columns = domains in scope (Notes, Files, Projects, Calendar, Agents...). Tick each cell with the as-the-other-user confirmation, not just the admin-side action.

## Playbook D - Attachment access derives from the parent

When a file is attached to content (note image/video, chat upload, event/task file), the byte copy
lives in the **attacher's** private "Attachments" folder as `OWNER_ONLY` (an OPEN_TO_ORG parent
instead routes it to the shared "Organization Attachments" folder). Read access to those bytes is
**derived from the parent content**, not from the file's own owner/sharing: anyone who can VIEW the
parent can fetch the attachment (clamped to read-only), and access revokes when the share is removed.

**Why this needs its own playbook (the trap):** the attachment *list* (`ListAttachments` /
`BatchListAttachments`) already defers to parent access, so a shared user *sees the attachment listed*.
The actual bytes are a **separate gate** - the asset routes `/api/files/{org}/{file}`,
`/api/thumbnails/{org}/{file}`, `/api/media/{org}/{file}` run their own per-file check. The classic bug
is "attachment shows in the list / file shows in the owner's folder, but the `<img>` in the note 403s
for the shared user." **Listing is not proof. The image actually rendering (asset request 200) is.**

### Proof method (per viewer)
1. Sign in as the viewer, open the parent content (note editor / chat channel / event).
2. `browser_network_requests` filtered to `api/files|api/thumbnails|api/media` -> every attachment
   asset request is **200**, never **403**.
3. DOM cross-check via `browser_evaluate` - no broken attachment images:
   ```js
   const brokenAttachmentImages = () =>
     [...document.querySelectorAll('img[src*="/api/files/"], img[src*="/api/thumbnails/"]')]
       .filter(img => img.complete && img.naturalWidth === 0).length; // expect 0 for a permitted viewer
   ```

### Cases (attacher x viewer - both directions matter)
| # | Setup | Viewer | Expected asset fetch |
|---|---|---|---|
| 1 | admin owns note, shares eve as VIEWER, **admin** attaches an image | eve | 200, image renders |
| 2 | admin shares eve as **EDITOR**, **eve** attaches an image | admin (owner) | 200 - owner sees a member's attachment |
| 3 | note shared to Engineering group, **alice** attaches | bob (same group) | 200 |
| 4 | same note | diana (Product-only control) | parent not accessible; direct asset URL -> 403 |
| 5 | note set "Everyone in org" baseline VIEWER, anyone attaches | diana (never a member) | 200 (org folder / parent-derived) |
| 6 | admin adds diana BLOCKED on the note | diana | 403 (BLOCKED parent denies the bytes too) |
| 7 | admin removes eve / narrows to "Only owner" | eve | now 403 - access revoked with the share |
| 8 | chat: upload in a **private** channel | channel member | 200; non-member -> 403 (parent check via ChatAccessChecker) |

Case 2 is the one grant-mirroring designs miss - close that loop explicitly. Case 4/6/7 are the
no-leak controls: confirm the **byte** route denies, not just the list.

## Playbook E - Live cross-session updates (no reload)

The recipient's sidebar/page updates **without a refresh** when their accessible-content set changes - shared with them, content created in the org-wide space, or a task created in a project they can access. It rides the notification stream (`StreamNotifications`), so it is a true two-browser flow: actor in A, observer in B, **B must stay parked on the relevant page** and update on its own.

Per-domain where B has to be looking (page-scoped domains only refetch while mounted):
- **Notes** - refreshes globally once B's notes tree has loaded (B can be anywhere, but visiting `/notes` first is the reliable setup).
- **Files / Calendar / Projects** - B must be **on that page** (`/files`, `/calendar`, the project board).

| # | Actor A does | Observer B (parked on...) | Expected, no reload |
|---|---|---|---|
| 1 | Share a note with B | `/notes` | note appears in B's "Shared With Me" |
| 2 | Create a note in the **Organization** space | `/notes` | appears in B's "Organization" section |
| 3 | Create an **org-wide** file/folder, event, or project | `/files` / `/calendar` / `/projects` | appears in B's list/grid |
| 4 | Create a **task** in a project B can access | the project's board | task appears on B's board |
| 5 | **Remove** B's access (or BLOCK) | the item's list/page | item disappears from B's view |

Proof method: snapshot B's relevant section **before**, do A's action, then read B's DOM (`browser_evaluate`) - the item must appear/disappear **without B navigating or reloading**. Confirm B's stream is live first (`browser_network_requests` filter `StreamNotifications` -> a `200` open request). A passing case shows the change arriving on its own; if you had to reload B, it failed. Updates are debounced (~500ms) - wait ~1.5s before asserting. Chat is **not** covered by this stream (separate `ChatAccessChecker` + its own realtime).

## Multi-user verification (do not skip)
A grant is NOT tested until you have confirmed the expected access **as the grantee** AND denial **as a control user**. The admin-side "member added" toast only proves the write, not the effect.

Run it across the two browsers: keep the **actor/owner in browser A** (`playwright` server) and the **subject in browser B** (`playwright-b` server). Loop: in A grant/change -> read the effect in B (re-login B to swap which subject) -> never touch A's session. For **live cross-session** assertions (the change must land in B *without* a reload), this two-browser setup is mandatory - keep B parked on the relevant page and watch its DOM update after A's action; only reload B as a last-resort sanity check, since a passing test must show the update arriving on its own.

## Cleanup discipline (MANDATORY)
You are mutating real dev data. Track everything you create/change and reverse it at the end of the session:
- Delete created content (Danger Zone for projects - it requires typing the exact name to confirm).
- Remove members you added; restore the original access mode (revert "Invited people"/"Everyone in org" back to "Only owner" if that was the start state).
- Sign back in as `admin` and leave the workspace as you found it.

## Flow-specific gotchas
- **Backend auto-reload drops your session on any source save** - do not edit code mid-flow; re-login if you did.
- **Don't manually restart the backend** for code changes (auto-reload covers it; restart kills sessions and can 500 in-flight calls).
- **`browser_click` with `ref=eXX` throws "Unknown engine ref"** - click via `browser_evaluate` (find by text/selector) instead.
- **SubjectPicker search is debounced + hits the backend** - type >= 1-2 chars, wait ~1s before reading result rows. Selecting a single subject usually fires the add immediately (no separate confirm click).
- **Destructive confirms** (delete project) require typing the exact item name into the dialog input before the confirm button enables.
- **HMR console noise** (`Failed to load module script ... text/html`, a one-off token-refresh error right after a reload) is dev-server churn, not a product bug - distinguish it from real errors.
- **Don't read "admin can't see it" as a failure** - the permission model gives org/domain admins no content bypass by design.
- **An attachment showing in the list does NOT prove the bytes are accessible** - `ListAttachments` defers to parent access, but the `/api/files|thumbnails|media` asset routes gate the file separately. Always confirm the image actually renders (request 200, `naturalWidth > 0`), not just that it is listed.
