---
name: uniffy-permission-matrix-test
description: |
  Execute the full end-to-end permission matrix against the live Uniffy app through the two Playwright MCP browsers: every sharing, access, denial, viewing, revocation, and request-access case on every content domain (notes, files, projects, tasks, calendar, chat, agents, automations, rooms), proven as the affected user. Covers the PostgreSQL-authoritative access behaviors: instant revocation in search and mentions, per-surface search authorization (spotlight, domain searches, filters, pagination), restricted chips, access requests, COMMENTER and role floors, expiry-aware grants, live org-default inheritance, group membership churn, delete and tag and bookmark revocation, attachment byte gating, and live no-reload pruning. Use when asked to run the permission matrix, matrix-test the permission system, do a full e2e sweep of sharing and access control, or validate a permissions PR end to end. Use `uniffy-e2e-flows` for a lighter single-domain permission loop and `uniffy-playwright` for one-off browser inspection. Skip for unit or integration tests, backend-only work, or when the dev stack is not running and the user has not asked to start it.
---

# Uniffy Permission Matrix E2E

This skill drives a complete scenario-by-domain permission matrix against the running dev stack. Every cell is proven by observing the effect **as the affected user** in a second, isolated browser. Admin-side toasts prove nothing.

Read `uniffy-playwright` first for the MCP mechanics (login recipe, selector gotchas, network and console tools). Read `uniffy-e2e-flows` for the general flow discipline. **Ignore the fixture tables in those two skills: dev seeding moved to the demo company roster documented below.**

Background model reference: `.agents/rules/permissions.md` is the source of truth for expected behavior. When a matrix cell surprises you, check the rule file before filing a failure.

## Preflight

1. Stack up: `docker ps | grep uniffy-dev`, UI on `:5173`, backend on `:8000`.
2. Both MCP browsers up: `uniffy-mcp-playwright` (server `playwright`, port 8931) and `uniffy-mcp-playwright-b` (server `playwright-b`, port 8932). If the `playwright-b` tools are missing: `docker compose --profile dev up -d mcp-playwright-b`, then reconnect MCP.
3. Browsers reach the app at `http://host.docker.internal:5173` (never localhost).
4. Do not edit backend or frontend source mid-run. The backend auto-reloads on save and drops every session.
5. This run mutates real dev data. Keep a running ledger of everything you create or change; the Cleanup section reverses it.

## Fixtures (demo company seed)

Source of truth: `src/uniffy/scripts/demo_company/content/people.json` and `manifest.json`. Org is **"Uniffy"** (the card on `/welcome`). Every roster user's password is `admin` (`DEFAULT_PERSON_PASSWORD` in `src/uniffy/scripts/demo_company/loader.py`), except the demo persona `maria@uniffy.io` whose password is `demo`. `admin@uniffy.io` (password `admin`, or `$INITIAL_ADMIN_PASSWORD`) is org OWNER and system admin. Every roster user is an ordinary org MEMBER.

Grantable subjects come in three kinds, all selectable in the share dialog's subject picker (kind-badged): users, **access groups**, and **teams**.

Access groups:

| Group | Members |
|---|---|
| Release Approvers | alice (admin), bob, sofia, teodora, georgi |
| Security Council (private) | viktor (admin), alice, milena, vasil |
| Incident Response | georgi (admin), milena, vasil, hristo, bob, charlie |
| Budget Approvers | elena (admin), maria, martin, diana |

Security Council is a private group: invisible and ungrantable to non-members (the share picker finds nothing and a direct grant 404s). That is correct behavior, so never build a scenario around bob granting it; the multi-group case uses Release Approvers + Incident Response, which bob belongs to.

Teams (subset that matters here):

| Team | Members |
|---|---|
| Backend Team | bob (lead), ivan, nikolay, kristina, radoslav |
| Frontend Team | sofia (lead), dimitar, yana, stefan, gergana |
| Platform Team | alice (lead), charlie, teodora, plamen |

### Cast

| Role in the run | User | Why |
|---|---|---|
| Owner/actor (browser A) | `bob@uniffy.io` | Ordinary member. Backend Team, Release Approvers, Incident Response. Proves the model without admin conflation. |
| Primary grantee (browser B) | `yana@uniffy.io` | Frontend Team, in no access group. Clean subject for direct grants. |
| Negative control | `stefan@uniffy.io` | Frontend Team, no access group, never granted anything. Must stay denied throughout. |
| Group-grant positive | `sofia@uniffy.io` | Release Approvers member. |
| Team-grant positive | `ivan@uniffy.io` | Backend Team member. |
| Multi-group subject | `georgi@uniffy.io` | Release Approvers + Incident Response; grant both at different roles, highest wins. |
| Single-group control | `teodora@uniffy.io` | Release Approvers only; stays at that group's role in the multi-group case. |
| BLOCKED-in-group subject | `kristina@uniffy.io` | Backend Team member; explicit block must beat her team grant. |
| No-bypass control | `admin@uniffy.io` | Org OWNER + system admin. Must NOT see bob's private content. Also the required actor for agents, automations, and rooms columns. |

Browser A holds the actor for the current column and stays logged in. Browser B is re-logged as whichever subject the current cell checks. Never run a subject check in browser A.

## The matrix

Rows are scenarios, columns are domains. Run column by column: pick a domain, create its item once, then walk the applicable scenarios top to bottom on that item, rotating browser B subjects.

### Domains (columns)

| # | Domain | Create as | Share entry point |
|---|---|---|---|
| D1 | Note | bob, `/notes` -> new note | editor header -> Share |
| D2 | File + folder | bob, `/files` -> upload / new folder | row or details panel -> Share |
| D3 | Project (+ task inheritance) | bob, `/projects` -> New | `/projects/:id/settings?section=members` |
| D4 | Calendar event | bob, `/calendar` -> create (modal-only detail) | event modal -> Share |
| D5 | Chat channel | bob, `/chat` -> create channel | channel settings modal (membership model, not access_mode) |
| D6 | Agent | admin, `/agents` -> create | agents view -> Share |
| D7 | Automation | admin, `/agents/automations` | task detail header -> Share |
| D8 | Room | admin, `/rooms` | room detail panel or table row -> Share |

Column caveats:

- **D3**: tasks have no own policy; after each grant change on the project, open a task inside it as the subject and confirm the task follows (visible, editable, denied) exactly as the project does. Also assert child-creation floors: a VIEWER subject has no working New Task affordance, an EDITOR subject creates tasks.
- **D4**: events are invite-only. The access dialog offers Owner only / Specific people and must NOT offer "Everyone in org"; treat the option appearing as a FAIL. Attendees have a view floor: adding an attendee makes the event visible to them without a separate share, removing the attendee revokes it. Run S6 as this assertion instead of a baseline test.
- **D5**: chat uses channel membership via `ChatAccessChecker`, not `access_mode`. Skip S1-S11 and run S18 instead.
- **D6-D7**: creation and CRUD gate on the agents-builder role (org admins + AGENTS domain admins), so admin is the actor. READ access still flows through content shares, which is exactly what the scenarios test. For D6 also run the live agent-picker case in S14. For D7, S11 has an extra assertion: transferring an automation repoints its execution identity (the task runs as the new owner).
- **D8**: rooms are org infrastructure managed by admins; a shared-in viewer sees and books per role, and Edit/Delete row actions stay hidden without the matching role.

### Scenarios (rows)

Applicability: S1-S11 on D1-D4 and D6-D8 (S6 modified on D4). S3 only where a comment surface exists (notes, files, tasks); N/A elsewhere. S12-S17 and S19 are cross-cutting with named target domains. S18 is D5 only. S20 is optional and destructive.

**S1. Private by default + no admin bypass.** As bob create the item (set "Only owner" if it inherited something wider; org defaults can make a fresh item org-visible, the panel shows the resolved mode). As yana, stefan, and admin in turn: item absent from every list, direct URL shows a denied or not-found state that leaks neither title nor content, and the title returns nothing in global search or `@` mention lookup. Admin being denied is the point, not a bug.

**S2. Explicit VIEWER grant.** Bob adds yana as VIEWER (mode auto-flips to "Invited people"; a member cannot exist under "Only owner"). As yana: item visible and readable, no edit, delete, comment, or member-management affordance anywhere (list row actions, detail header, context menu). As stefan: still fully denied.

**S3. COMMENTER sits between VIEWER and EDITOR.** Bob sets yana to COMMENTER. As yana: reading works, commenting works and the comment persists, editing the content itself is still denied. Drop her to VIEWER: commenting is now denied too. Comments are child content resolving against the parent: as stefan (no access), the comment thread is unreachable and comment text is absent from his search.

**S4. Elevate to EDITOR.** Bob changes yana's role to EDITOR. As yana: editing works and persists (reload, re-open). Sharing management is still denied (no working Share management surface; EDITOR is below MANAGE).

**S5. ADMIN manages, OWNER transfers.** Bob sets yana to ADMIN. As yana: she can open the sharing surface, add stefan as VIEWER, remove him again, and change the access mode. She cannot transfer ownership (OWNER floor). Revert her to VIEWER after.

**S6. OPEN_TO_ORG baseline: elevation AND demotion.** Bob sets "Everyone in org" with baseline VIEWER. As stefan (never granted): item now visible, read-only. Bob keeps yana at EDITOR: as yana, editing works (explicit grant elevates above the baseline). Then invert it: baseline EDITOR with yana explicitly VIEWER. As stefan, editing works (baseline); as yana, read-only. An explicit grant wins over the baseline in BOTH directions, it does not merge to the higher role. On D4 replace this whole scenario with the invite-only assertions from the column caveat.

**S7. BLOCKED beats everything.** Still OPEN_TO_ORG: bob adds stefan as BLOCKED. As stefan: item gone from lists, search, mentions, and the direct URL, despite the org baseline. Then grant Backend Team EDITOR and block kristina: as ivan, edit works; as kristina, fully denied despite her team membership. Remove the blocks after.

**S8. Group, team, multi-group grants + membership churn.** Back to "Invited people", no baseline. Grant the access group Release Approvers VIEWER: as sofia, read-only access; as yana (not in the group, after removing her direct grant), denied. Grant the team Backend Team EDITOR: as ivan, edit works; as stefan, denied. Grant Incident Response EDITOR while Release Approvers is VIEWER: as georgi (in both), edit works (highest role across groups wins); as teodora (Release Approvers only), still read-only. **Churn**: with the Release Approvers grant still in place, remove sofia from the group itself as admin (group membership CRUD is org-admin only; a group admin gets 403 there); as sofia, access is gone with no change to the content's share. Re-add her to the group: access returns. Group membership is part of the access decision, not a snapshot taken at grant time.

**S9. Expiring grants.** Bob adds yana with "Set expiration" (datetime-local input in the add-member popover) about 2 minutes in the future. As yana: access works now; the member row in the sharing panel shows the expiry. Wait past the timestamp (no worker involved; expired rows are ignored at read time), then as yana: list, direct URL, search, and mention lookup all deny. No admin action needed for the revoke. Repeat once with a group subject (expiring Release Approvers grant): sofia's access dies at the timestamp too.

**S10. Narrow back to "Only owner".** With members present, bob selects "Only owner". A confirm dialog warns it removes N members; accept. As yana and sofia: access gone everywhere.

**S11. Transfer ownership.** Bob (or admin for D6-D8) transfers ownership to yana. As yana: OWNER affordances (including transfer). As the previous owner: role is now ADMIN (can manage, cannot transfer). On D7 additionally confirm the automation now executes as yana. Transfer back during cleanup.

**S12. Live org-default inheritance.** Fresh items with no explicit mode follow the org default live, not a create-time snapshot. As bob create a note and leave its mode on "Use organization default" (note the resolved mode the panel shows). As admin, open the org permission defaults and set the Notes default to "Everyone in org" / VIEWER: as stefan, the inherited note becomes visible (appearance in search may lag on the defaults reindex; direct and list access should not). Flip the default to "Only owner": as stefan, the note is denied again immediately, including in search. **Warning**: the default flip affects every inheriting item of that type org-wide; do this on the dev stack only, revert the default to its original value immediately, and note the flip in the run ledger. Target D1; one extra domain if time allows.

**S13. Delete revokes.** Share an item to yana, then as bob move it to trash: as yana, it leaves lists, direct URL denies, and search drops it instantly. Restore from trash: yana's access returns. Permanently delete: gone for everyone, owner included, and the title never resurfaces in anyone's search or mention lookup. Target D1 and D2.

**S14. Live revocation, no reload.** Two live sessions at once, B parked on the target surface, then A revokes; the item must disappear from B **without any navigation or reload**. Updates are debounced, wait about 1.5 seconds before asserting; confirm B's notification stream is open first (`browser_network_requests` filter `StreamNotifications`). Run at minimum: (a) D1 note shared to yana, B parked on `/notes`, revoke -> sidebar row and any open mention preview of it vanish; (b) D2 file, B parked on `/files`, revoke -> row pruned, and if B has the file viewer open the viewer is evicted; (c) D6 agent, B has the chat agent picker open, unshare or BLOCK -> agent leaves the already-open picker. Also run one positive: share while B is parked -> item appears without reload.

**S15. Search surfaces are PostgreSQL-authoritative.** The asymmetry is the contract: **appearing may lag (Meilisearch indexing), disappearing must be instant.** (a) Share a note to yana; as yana search its title in the global/spotlight search until it appears and confirm the mention `@` lookup finds it. (b) Revoke; as yana immediately re-run the same search and mention lookup: zero hits, zero preview or snippet text, no stale title anywhere. A result that a reload would have removed is still a FAIL. (c) Control sweep: as stefan, search distinctive words from every private item created this run (note title and body words, file name, project and task names, event title, agent name, channel message text): nothing surfaces, in results or in previews. (d) Restricted content is absent from search entirely: unlike mentions there is no "restricted result" row, denied items simply do not appear. (e) Counts and pagination: the count label reflects shown-plus-more (`has_more`), never an inflated index total; paging deeper with "more" keeps returning only accessible hits. (f) Filtered queries stay gated: `type:` prefixed queries and tag-filtered queries return nothing the subject cannot access. (g) Per-domain search consumers, not just spotlight: repeat one allow-then-revoke pair in the files page search, the notes search, and chat message search as the subject; each obeys the same instant-denial rule.

**S16. Access request via restricted chip.** In a note or chat message yana CAN see, bob mentions (`@`) a private item yana cannot see. As yana: the mention renders as a restricted chip (no title leak) offering "Request access". Request with a message. As bob: an ACCESS_REQUESTED notification arrives; open the review dialog and approve as VIEWER. As yana: the chip resolves to the real title without a reload and the item opens. Repeat with stefan and **deny**: stefan gets the denied notification and stays locked out. Pending requests for a chat channel also surface in the channel settings modal.

**S17. Attachment bytes derive from the parent.** Listing is not proof; the `/api/files/`, `/api/thumbnails/`, `/api/media/` byte routes gate separately. (a) Bob pastes an image into a private note: as yana, note denied, all three byte URLs 403, filename absent from search and mentions. (b) Share the note to yana as VIEWER: embedded image renders (asset requests 200, `naturalWidth > 0`) with no share on the file itself. (c) Revoke the note share: bytes 403 again. (d) File sent into a private chat channel: member fetches bytes, non-member 403s, and the attachment chip resolves for members while showing restricted for others. (e) Attach a file to an OPEN_TO_ORG note: it lands in the shared Organization Attachments folder and becomes org-searchable. (f) An explicit BLOCKED grant on the attachment file itself denies the bytes even for someone who can view the parent. (g) Trash the note and empty trash: attachment rows, file rows, and bytes are gone (owner's byte route 404s).

**S18. Chat's membership model (D5).** (a) Bob creates a private channel with ivan: as ivan, channel opens and messages send; as yana (non-member), channel absent, direct URL denied, message content absent from her search. (b) A PUBLIC channel is reachable by any org member (stefan can open it). (c) Moderation exception, the one kept bypass: as admin, the private channel IS viewable via moderation. Expected, not a leak. (d) Channel roles: a plain member cannot open member management in channel settings; the channel admin can. (e) **Kick**: remove ivan from the private channel while his session is live: the channel leaves his sidebar without a reload, the direct URL denies, and the channel's messages vanish from his search instantly. (f) Chat attachment bytes were covered in S17(d).

**S19. Tags and bookmarks do not leak revoked content.** (a) Bob puts a distinctive tag on a private note: as stefan, the tag filter UI and tag-scoped search reveal neither the tag assignment nor the item (chat moderators seeing CHAT tag assignments is the one documented exception). Share then revoke: the tag surface obeys the same instant-denial rule. (b) As yana bookmark an item shared to her, then have bob revoke: her bookmarks list must not leak the title or preview, and following the bookmark is denied.

**S20. Deactivation kill-switch (OPTIONAL, destructive, run last, only if asked or explicitly in scope).** As admin, deactivate yana's org membership. As yana: every access from this run is gone at once, including content she owns and anything transferred to her in S11. Reactivate immediately (re-adding a deactivated member is the restore path) and confirm access returns. Do not leave her deactivated.

## Evidence rules

- A cell passes only with subject-side proof in browser B. Positive = the subject sees or does the thing. Negative = all three of: absent from lists, direct URL denied without leaking title or content, absent from global search and mention lookup.
- Capture `browser_console_messages` (`level: "error", all: true`) after each scenario; ignore HMR module-script noise, flag the rest.
- Use `browser_network_requests` for RPC status codes (`MembersService`, `SearchService`, asset routes) when the DOM is ambiguous.
- Revocation checks run immediately after the revoke, in the already-open session. Reload only as a last-resort sanity check, and a case that needed the reload to deny is a FAIL.
- "Admin cannot see it" is a PASS everywhere except chat moderation and an audited SupportSession.
- People profiles are member-record data, org-visible by design; do not file profile visibility as a leak. LLM provider keys carry no access mode at all; out of scope.
- Deliberately excluded from this matrix: the SupportSession flow (platform surface with its own audited consent path) and cross-org isolation (the demo seed is single-org). State both as excluded in the report, not as SKIPPED cells.

## Reporting

Maintain the matrix as you go. The final reply to the user is the whole deliverable, no file is written: a short description of the run (actors used, domains covered, anything skipped and why) followed by a single results table, rows S1-S20, columns D1-D8, each cell PASS / FAIL / N/A / SKIPPED. Below the table, one short paragraph per FAIL: exact repro (actor, subject, item, steps), observed vs expected, and the network or console evidence. A run that cannot finish still ships the partial matrix with the untested cells marked SKIPPED and the reason.

## Cleanup (mandatory)

Reverse the ledger: transfer ownerships back, remove every grant and block you added, restore original access modes, delete created items (project deletion requires typing the exact name), empty trash where S17(g) needs it anyway, restore any flipped org default (S12), reactivate anyone deactivated, and leave both browsers logged out or as admin. State in the report that cleanup ran and what, if anything, was left behind.

## Gotchas

- Backend auto-reload drops all sessions on any source save; never edit code mid-run, never `docker restart` the backend.
- `browser_click` with `ref=eXX` throws in this build; click via `browser_evaluate` (find by text or `data-testid`). React-controlled inputs need the native value-setter recipe from `uniffy-playwright`.
- The subject picker search is debounced and hits the backend; type 1-2 chars, wait about a second. Groups and teams share one name namespace, pick by the kind badge.
- The expiry field is a `datetime-local` input; fill it via the value-setter recipe and mind the browser's local timezone when choosing "2 minutes from now".
- A fresh item can inherit an org-wide default; always read the resolved mode in the sharing panel before asserting S1, and pin it to "Only owner" first.
- New content may take a moment to appear in search (indexing lag is allowed); only denial must be instant.
- Byte-route probes (S17) contaminate easily. The browser HTTP cache can serve a stale 200 after a revoke, and the asset-read cookie makes a "logged-out" probe authenticated. Always fetch with `cache: 'no-store'` plus a query-string cache-buster; run denial probes from the denied subject's own session (their cookie must be present and still get 403), and use `credentials: 'omit'` only for the separate unauthenticated-leak variant. A leak verdict from a probe without these controls is invalid; re-run it before reporting.
