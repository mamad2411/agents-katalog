---
name: manual-bounty-testing
description: "Manual-first bug bounty and pentest methodology built from a top-paid disclosed HackerOne sample. Use when testing real application behavior beyond scanner output: business logic, authorization drift, workflow abuse, state-machine flaws, onboarding abuse, AI/agent access control, race windows, parser/import abuse, and vulnerability chaining."
sources: hackerone_public, field_recon
report_count: 50
---

# Manual Bounty Testing

Use this skill whenever a target is interesting enough that raw recon is no longer the bottleneck.

This skill exists to keep the operator out of the "run scanner, grep output, move on" trap. The highest-value findings are usually hidden in behavior, not banners.

---

## When to use

Load when:
- You already mapped the target and want to test it intelligently
- The feature has roles, approvals, ownership, sharing, imports/exports, AI, billing, onboarding, or asynchronous jobs
- Scanner output is low-signal but the product surface is complex
- The target smells like business logic, IDOR, privilege escalation, ATO, or workflow abuse
- You want to turn one medium-severity primitive into a high- or critical-impact chain

Do not use as a replacement for initial recon. Use it after surface discovery, or whenever a specific workflow deserves deep manual attention.

---

## Core principle

**Scanners find exposed technology. Manual testing finds broken assumptions.**

Your job is to identify where the product assumes:
- the client will respect the intended workflow
- the caller is acting as the right user
- a side effect only happens once
- a field is "internal only"
- an AI feature only sees the right tenant's data
- a background job inherits the same authorization as the UI
- a fix on the happy path covers every alternate path

The target usually breaks at one of those boundaries.

---

## Corpus and why it matters

This skill is grounded in a **50-report sample of the highest-paid disclosed HackerOne reports** available from the public top-paid index on **July 2, 2026**.

The report corpus is internalized in this skill. Do not pause the hunt to open a link list or consult public reports during execution; use the exploitation shapes below as built-in operator memory.

That sample shows a strong pattern:
- Top payouts cluster around **imports, parsers, object movement, password recovery, admin/control-plane exposure, GraphQL object abuse, secondary-object leakage, and rich rendering sinks**
- Many of the most valuable bugs are **not** "scan and grep" issues. They are **workflow and trust-boundary failures**
- Secondary surfaces repeatedly dominate: imports, uploads, exports, previews, quick actions, partner/invite flows, recovery flows, wiki/markdown renderers, CI, VPN, internal dashboards, and GraphQL mutations

The 50-report sample over-indexes on:
- RCE and exposed execution surfaces
- File read / path traversal / export leakage
- Auth and recovery flaws leading to ATO
- Authorization drift, IDOR, and privilege escalation
- Token / secret / credential exposure
- XSS in product-specific rendering and secondary actions
- Import / parser / ingestion abuse
- GraphQL object and mutation abuse

This means your manual testing should bias toward **where objects are transformed, moved, shared, recovered, rendered, imported, or reinterpreted**.

---

## Manual exploitation operating loop

Run this loop on every valuable workflow before calling it done:

1. **Model the workflow as a state machine.** Write the intended path as `create -> verify -> approve -> act -> export/delete/archive`. Then call each later step early, twice, stale, from another actor, and from another tenant.
2. **Capture a clean baseline.** Save one successful browser request, one equivalent API request, and one failure request from a lower-privileged actor. The failure diff is the map of what the backend actually checks.
3. **Break request shape before payloads.** Mutate scalar fields into arrays/objects, duplicate keys, change `Content-Type`, mix form and JSON, add null/empty values, reorder fields, and test mobile/API variants before reaching for classic injection payloads.
4. **Cross the actor boundary.** Replay every read/write/export/move/helper request as owner, member, invited user, removed user, expired user, API token, and unauthenticated user. If a role sounds harmless, test the helper objects it owns.
5. **Cross the object boundary.** Swap primary IDs, child IDs, attachment IDs, GIDs, signed URL IDs, export IDs, webhook IDs, job IDs, template IDs, AI conversation IDs, and imported-copy IDs independently.
6. **Cross the time boundary.** Generate tokens/links/jobs in state A, change the underlying email, role, tenant, object owner, or object status, then redeem/complete in state B. Repeat with two sessions and parallel requests.
7. **Chase every side effect.** Notifications, exports, audit logs, webhooks, AI citations, generated PDFs, background jobs, and support tickets often expose the real impact even when the primary endpoint looks fixed.
8. **Convert signal into control.** Do not stop at "I can read object X." Ask what object X contains: token, email, invite, reset artifact, secret, admin URL, webhook signing key, cloud credential, internal path, or role-changing mutation.
9. **Prove the smallest high-impact chain.** Use synthetic markers and minimal data. Demonstrate account takeover, privilege change, cross-tenant read/write, secret access, or control-plane reach without dumping unnecessary data.

If one branch fails, pivot across shape, actor, object, time, and side effect before abandoning the workflow.

---

## Exploit motifs distilled from the 50-report corpus

These are not generic categories. They are recurring exploitation shapes from the top-paid sample. Reuse them aggressively.

### 1. Array / structure confusion in auth and recovery

Observed shape:
- A parameter expected to be a scalar is accepted as an array or object
- Backend fans out a side effect to all supplied values
- Recovery or reset artifact reaches attacker-controlled destination

Concrete pattern from the corpus:
- GitLab password reset accepted `user[email]` as an array instead of a single string, causing the reset email to go to both victim and attacker

Manual tests:
- Convert form posts to JSON
- Replace `email=value` with `email=[victim, attacker]`
- Replace scalar fields with arrays, objects, nested objects, duplicated keys
- Test recovery, invite, approval, and notification destinations
- Check whether side effects fire once per field element instead of once per subject

Impact chains:
- reset-link duplication -> ATO
- invite duplication -> collaborator takeover
- notification duplication -> token/session/OTP leakage

### 2. Mid-flight state switch / TOCTOU on verification

Observed shape:
- A link or token is generated for state A
- Before redemption, the attacker changes the underlying object to state B
- The backend redeems against the new state, not the old one

Concrete pattern from the corpus:
- Shopify partner email confirmation bypass: generate verification for attacker email, then change profile email to victim employee email before redeeming

Manual tests:
- Request verification or reset link
- Pause before clicking
- Change email / ownership / collaborator target / workspace / role while token is still valid
- Redeem old link against new state
- Race approval, invite acceptance, password reset, and email change endpoints

Impact chains:
- email verification bypass -> store/collaborator takeover
- stale invite token + changed target object -> unauthorized membership
- stale approval token + changed role target -> privilege escalation

### 3. Import pipeline as a trust-boundary break

Observed shape:
- Import is assumed to be data movement, but it is really code/data interpretation
- Validation focuses on archive shape or source type, not on what the importer will open/fetch/execute later

Concrete patterns from the corpus:
- GitLab bulk imports -> archive parsing to RCE
- GitHub import / RepositoryPipeline -> local repo or dangerous source handling
- project import -> private object exposure

Manual tests:
- Feed archives with symlinks, hardlinks, weird metadata, nested archives, duplicated filenames
- Use imported content that points to local files, internal paths, or unexpected source URIs
- Check whether imported object references preserve access checks
- Look for processors invoked after extraction: metadata stripping, image conversion, markdown rendering, diagram rendering, indexing, diffing

Impact chains:
- import parser abuse -> RCE
- imported path confusion -> local file read
- imported project/object copy -> cross-tenant data theft

### 4. Symlink / archive extraction -> arbitrary file read

Observed shape:
- Importer extracts tar/zip
- Symlinks are preserved
- Downstream uploader or reader follows the symlink as if it were an imported file

Concrete pattern from the corpus:
- GitLab `uploads.tar.gz` import retained symlinks, then later opened them and uploaded target-file contents

Manual tests:
- Add symlink entries to tar/zip
- Point to app secrets, environment files, config files, SSH material, internal metadata
- Add nested paths and name collisions
- Test avatar, attachment, markdown asset, and "uploads" import lanes separately

Impact chains:
- symlink -> file read -> secret extraction -> lateral access
- symlink -> config read -> signing/secret material -> auth bypass

### 5. Local-path / local-repository confusion in remote import

Observed shape:
- Feature claims to import from trusted remote source
- Backend accepts or can be coerced into local path or local repository semantics

Concrete patterns from the corpus:
- GitLab import pipeline accepted local repositories
- Several import findings copied private objects or opened local content during import

Manual tests:
- Substitute local-style paths where URLs are expected
- Try alternate URI forms, file-like references, path traversal-ish source parameters
- Test redirects from allowed remote sources into unexpected backend fetch targets
- Compare validation done in UI versus worker-side source resolution

Impact chains:
- local source resolution -> private repo/object exposure
- local path fetch -> arbitrary read
- local source + parser chain -> RCE

### 6. External integration fetchers -> full-response SSRF

Observed shape:
- Product fetches external content on behalf of user
- Integration URL path can be repointed through redirect or path confusion
- Backend returns or processes internal response body

Concrete pattern from the corpus:
- Dropbox/HelloSign Google Drive integration yielded full-response SSRF

Manual tests:
- Target integrations: Drive, Slack, GitHub, Sheets, Docs, webhooks, media fetchers, import-from-URL
- Probe redirect behavior
- Test URL components independently: host, path, query, embedded redirectors, file IDs
- Check if backend follows redirects to internal resources and reflects full body

Impact chains:
- SSRF -> metadata / internal admin / service creds
- SSRF + full response -> key extraction -> cloud takeover

### 7. GraphQL object-family abuse

Observed shape:
- GraphQL hides access control flaws behind clean schemas
- Object GIDs or guessed IDs are accepted in queries or mutations without ownership validation
- Helper mutations are less protected than core UI paths

Concrete patterns from the corpus:
- `PolicyPageAssetGroup` disclosure by GraphQL GID
- `SaveCollaboratorsMutation` leaking user emails
- destructive mutation deleting another user's certifications
- mutation aliasing in recovery flow causing resource/logic abuse

Manual tests:
- Enumerate object IDs and GIDs by family
- Replay queries/mutations across tenants and users
- Focus on helper mutations: collaborators, certifications, exports, notifications, invitations
- Try mutation aliasing, batching, stale objects, and mixed-tenant object references
- Compare read authorization to mutate authorization

Impact chains:
- GID disclosure -> private program/object intel -> targeted abuse
- helper mutation leak -> email disclosure -> phishing / account-targeting
- destructive mutation IDOR -> integrity loss / profile sabotage

### 8. Secondary-object exposure beats primary-object controls

Observed shape:
- Primary resource is protected
- Export, attachment, quick action, movement, spotlight item, or copied object is not

Concrete patterns from the corpus:
- internal attachments exported via zip
- private objects leaked through import
- content spotlight deletable remotely
- customer contact quick commands feeding XSS

Manual tests:
- Enumerate attachments, previews, exports, copies, movement endpoints, spotlight/media children
- Move object between projects/tenants/states, then inspect derived URLs
- Trigger "export as zip", copy, clone, move, share, archive, restore
- Test object IDs in secondary endpoints even when primary endpoint is locked down

Impact chains:
- internal attachment export -> confidential data leak
- child-object delete/update -> high-integrity break
- copied object with wrong ACL -> cross-tenant disclosure

### 9. Request smuggling + cache poisoning into stored XSS

Observed shape:
- Frontend and backend disagree on request boundaries
- Poisoned response gets cached for a high-traffic surface
- Cached artifact serves attacker-controlled content on auth-sensitive page

Concrete patterns from the corpus:
- PayPal signin stored XSS via cache poisoning
- follow-up bypass after initial fix

Manual tests:
- Target signin, recovery, login help, preview, and content-negotiated pages
- Check cache keys and cache status
- Explore front-door/backend parser desync
- Vary innocuous-looking headers and path normalization
- After poisoning, validate whether cache serves attacker-controlled redirect or content to clean clients

Impact chains:
- smuggling -> cache poison -> XSS on login -> credential/session theft
- fix bypass -> second-order persistence after remediation

### 10. Product-specific rendering sinks

Observed shape:
- Renderer is not "HTML input" in the classic sense
- Product transforms markdown, diagrams, metadata, customer names, or bot messages into HTML/JS-capable surfaces

Concrete patterns from the corpus:
- Kramdown / wiki options -> RCE
- DesignReferenceFilter markdown XSS
- Kroki diagram XSS
- quick command / contact-name stored XSS

Manual tests:
- Any feature that renders markdown, diagrams, previews, document metadata, filenames, bot greetings, customer names, comments, quick actions
- Test sink-specific payloads, not only generic `<script>`
- Look for server-side renderers and external converters
- Check whether renderer options are attacker-controlled

Impact chains:
- renderer XSS -> admin/session impact
- renderer option injection -> server-side exec

### 11. Observer/support/helper roles often have hidden write paths

Observed shape:
- Role sounds read-only or low-risk
- Nearby helper object grants powerful side effects

Concrete patterns from the corpus:
- Teleport access-list owner can grant higher roles
- Mail.ru observer can create access keys
- TikTok intelbot auth flaw reveals ticket data

Manual tests:
- Compare "read-only" roles against all create/update endpoints for helper objects
- Inspect access-list, API-key, queue, support, bot, ticket, and approval subfeatures
- Test whether ownership of the helper object beats role restrictions on the target privilege

Impact chains:
- observer/helper role -> key creation -> infrastructure access
- support bot leak -> internal ticket intel -> pivot and social/technical escalation
- access-list ownership -> self-upgrade -> full privilege escalation

### 12. Token / secret / artifact exposure pays because it collapses complexity

Observed shape:
- A single leaked credential or token bypasses layers of product logic

Concrete patterns from the corpus:
- GitHub token exposure
- leaked session cookie -> ATO
- Artifactory creds in GitHub
- challenge token leak exposing password or account data

Manual tests:
- Review repos, mobile bundles, build artifacts, CI logs, generated files, support exports, challenge flows
- Search for tokens in secondary objects, not only source code
- Inspect whether challenge or recovery artifacts reflect more state than needed

Impact chains:
- token leak -> immediate account or code access
- support/challenge leak -> email/password/OTP compromise
- artifact creds -> registry/CI/internal-service takeover

### 13. Exposed control planes are still top-payout terrain

Observed shape:
- Internal panel or orchestration surface is reachable
- Weak or absent auth turns it into immediate leverage

Concrete patterns from the corpus:
- exposed Kubernetes API
- open Jenkins
- exposed Zeppelin
- Spring Actuator + broken auth
- VPN and internal docs surfaces

Manual tests:
- Standard admin/control-plane paths are mandatory
- Probe auth boundaries and read-only endpoints first
- Expand from status/env/info into exec, file, pipeline, artifact, and secret surfaces

Impact chains:
- exposed control plane -> credentials -> execution -> full environment compromise

---

## Deep exploitation recipes

Use these as active playbooks. Each recipe starts from a common product feature and forces it through multiple exploitation angles instead of a single checklist.

### A. Recovery, invite, and verification takeover

Goal:
- Turn a recovery/invite/verification primitive into account takeover or unauthorized membership.

Steps:
- Register attacker and victim test accounts where allowed; keep two clean browser sessions plus raw request capture.
- Trigger reset, invite, email-change, MFA-reset, or partner-verification flows for the attacker account.
- Mutate destination fields: scalar to array, nested object, duplicate key, mixed casing, null plus real value, form to JSON, JSON to form.
- Change the protected identity between token generation and redemption: email, phone, workspace, role, invite target, organization, or linked account.
- Replay stale links after account removal, email change, invite revocation, tenant switch, and role downgrade.
- Compare preview, accept, verify, resend, cancel, and finalization endpoints; helper endpoints are often weaker than the obvious redeem endpoint.
- Check side channels: email preview APIs, notification logs, support ticket copies, audit logs, webhook deliveries, and mobile deep-link handlers.

Escalation paths:
- reset artifact reaches attacker -> ATO
- invite token binds to changed target -> unauthorized workspace access
- email verification validates current state instead of token state -> employee/partner impersonation
- MFA reset side path lags behind account state -> durable session takeover

### B. Import, migration, and parser abuse

Goal:
- Treat every importer as a backend file/fetch/execute primitive, not as a harmless upload.

Steps:
- Identify all import lanes: repository, project, archive, CSV, spreadsheet, image, markdown, diagram, ticket, template, migration wizard, "import from URL", and third-party connector.
- Build archives with symlinks, hardlinks, duplicate filenames, absolute-ish paths, nested archives, long names, Unicode-normalized names, hidden files, and metadata payloads.
- Put payloads in filenames, comments, EXIF, markdown links, diagram definitions, CSV formulas, spreadsheet cell metadata, repo hooks, project descriptions, and imported references.
- Replace remote source parameters with local-looking paths, redirectors, unusual URI schemes, encoded separators, and source IDs copied from private objects.
- Separate validation from execution: pass a safe file in the UI, then modify the queued source, redirect destination, archive contents, or referenced object before the worker runs.
- Inspect what the importer creates after success: uploads, generated previews, logs, errors, exported zips, cloned objects, attachments, webhooks, search indexes, and AI knowledge sources.

Escalation paths:
- symlink/import reader -> local file read -> secrets -> admin/control-plane access
- source URL confusion -> SSRF/full response -> cloud metadata or internal API
- parser option injection -> server-side execution or sensitive render
- imported object ACL drift -> cross-tenant private data exposure

### C. GraphQL object-family assault

Goal:
- Find mismatches between schema cleanliness and authorization reality.

Steps:
- Enumerate object families by observing UI traffic: users, orgs, teams, projects, assets, attachments, exports, billing objects, AI conversations, saved prompts, certifications, roles, and helper objects.
- Collect IDs from multiple tenants and encode/decode global IDs when possible; map prefixes and object type names.
- Test every object family across read, list, search, preview, export, update, delete, assign, invite, and helper mutations.
- Use aliases and batched operations to mix allowed and forbidden objects; check whether partial failures still leak data.
- Swap nested IDs independently: parent belongs to attacker, child belongs to victim; parent belongs to victim, child belongs to attacker.
- Compare query authorization with mutation authorization. A mutation that only returns `success: true` can still cause high-impact side effects.
- Test stale object references after deletion, archive, transfer, invite revocation, role downgrade, and tenant switch.

Escalation paths:
- object disclosure -> emails/GIDs/internal names -> targeted helper mutation
- helper mutation IDOR -> role/invite/export/delete impact
- batch/alias confusion -> rate-limit or workflow bypass
- AI/knowledge object reference -> cross-tenant document leakage

### D. Secondary-object and derived-artifact leakage

Goal:
- Break the objects around the protected object.

Steps:
- For every protected object, enumerate derived objects: attachments, thumbnails, previews, PDFs, CSV exports, audit entries, notifications, comments, signed URLs, webhooks, background jobs, AI citations, search index entries, copied templates, and migration artifacts.
- Move, clone, archive, restore, share, unshare, export, and re-import the same object. Then retest all derived object URLs and IDs.
- Check whether derived artifacts inherit ACL from the source at creation time or at access time. Stale inherited ACL is a common leak.
- Test child endpoints directly with victim child IDs even when parent reads are blocked.
- Request exports as a lower-privileged user immediately after an owner triggers them; background jobs often trust the creator but expose output to the requester.
- Look for signed URLs without tenant binding, single-use enforcement, expiry enforcement, or object ownership checks at download time.

Escalation paths:
- export/preview leak -> confidential data
- signed URL drift -> durable unauthorized access
- child object delete/update -> integrity impact
- copied template/imported copy -> cross-tenant disclosure

### E. Billing, quota, refund, and credit manipulation

Goal:
- Convert state-machine weakness into financial or entitlement impact.

Steps:
- Map create, preview, apply, finalize, cancel, refund, retry, webhook-confirm, invoice-export, and entitlement-update endpoints.
- Tamper quantities, negative values, archived prices, currency, tax, coupon IDs, trial flags, plan IDs, seat counts, and billing-cycle boundaries.
- Replay finalize after cancellation, apply discount after invoice finalization, and refund while entitlement remains active.
- Race coupon redemption, gift-card use, seat reduction, trial conversion, subscription downgrade, and credit issuance.
- Compare UI, API, mobile, webhook, and admin/support flows. Payment providers often send authoritative events, but the app may accept client-side state transitions too.

Escalation paths:
- payment less than entitlement -> free premium access
- multi-redeem race -> monetary loss
- refund without entitlement revocation -> persistent service theft
- archived/hidden price reuse -> unauthorized discount

### F. Support, observer, and helper-role escalation

Goal:
- Turn low-power roles into high-impact actions through nearby helper objects.

Steps:
- Enumerate every capability available to observer, support, analyst, auditor, billing, integration, bot, API-token, and invited roles.
- Test helper creates and updates: API keys, access lists, queues, approvals, webhooks, integrations, exports, assignment rules, saved searches, alerts, and ticket actions.
- Check whether owning a helper object lets the user act on a protected target object.
- Compare "can configure notification/export/integration" with "can read the underlying data." Configuration often becomes an exfil channel.
- Test support/admin surfaces that render lower-privileged data: names, ticket text, files, markdown, bot commands, customer notes, and quick actions.

Escalation paths:
- observer creates key/export/webhook -> data exfiltration
- helper owner grants role -> privilege escalation
- support rendering sink -> privileged session impact
- bot or ticket leak -> internal intel for next chain

### G. Rendering, cache, and login-surface compromise

Goal:
- Find product-specific rendering sinks and turn them into session or credential impact.

Steps:
- Identify every renderer: markdown, wiki, diagram, PDF, document preview, image metadata, filename display, customer name, contact field, quick command, bot message, notification, email template, and support panel.
- Test the exact renderer grammar rather than generic HTML only; try link syntax, image syntax, table syntax, diagram directives, template variables, metadata, and nested renderers.
- Check whether attacker-controlled content is re-rendered in admin/support/login/recovery contexts.
- For cache-sensitive pages, vary cache keys: host-like headers, scheme headers, port headers, path normalization, query normalization, content negotiation, language, and method override.
- Validate poisoning from a clean client with no attacker cookies. Prove persistence, scope, and victim-visible impact.

Escalation paths:
- stored/admin-rendered XSS -> session or action impact
- cache poison on login/recovery -> credential/session capture path
- renderer option injection -> server-side read/exec depending on backend
- secondary admin sink -> privileged action execution

### H. Integration SSRF and webhook trust abuse

Goal:
- Abuse backend fetchers and callbacks that bridge the product to other systems.

Steps:
- Inventory fetchers: URL preview, import-from-URL, Drive/Slack/GitHub connectors, webhook tests, avatar fetch, PDF capture, screenshot generation, RSS/Atom, OpenAPI import, and AI retrieval sources.
- Test redirect chains, file IDs, path components, fragment handling, encoded hosts, mixed-case schemes, userinfo, IPv6-style host forms, DNS changes, and allowed-domain subpaths.
- Distinguish blind callback from full-response SSRF. Full-response SSRF is much higher value; search for reflected body in previews, errors, logs, exports, and imported content.
- For webhooks, test signature confusion, replay, stale secret rotation, event type swapping, tenant mismatch, and idempotency gaps.
- Check whether fetched data enters a second parser or renderer after retrieval.

Escalation paths:
- full-response SSRF -> internal response/secret disclosure
- blind SSRF -> internal reachability proof plus chained parser/log leak
- webhook replay/type confusion -> unauthorized state change
- integration token leak -> third-party account or repo access

### I. AI, RAG, and agentic multi-tenant abuse

Goal:
- Treat AI features as hidden object graphs with retrieval, tool, and memory boundaries.

Steps:
- Map AI objects: assistant, thread, message, file, vector store, source document, citation, prompt template, tool config, action run, connector, memory, and evaluation logs.
- Swap IDs across tenants for conversations, sources, uploaded files, vector stores, saved prompts, actions, and tool-call results.
- Ask for citations, summaries, exports, or debug views that may reveal retrieved documents without direct file access.
- Test whether imported or shared documents become globally searchable after copy, move, archive, re-index, or assistant duplication.
- Check support/operator views of AI conversations for prompt, token, file, and tool-result exposure.
- Compare UI filters with backend retrieval filters. Retrieval often uses broader access than the front-end object picker.

Escalation paths:
- cross-tenant source/citation leak -> confidential data exposure
- saved prompt/tool config leak -> secrets or internal system behavior
- assistant action misbinding -> unauthorized third-party/API action
- support AI transcript exposure -> token, PII, or internal investigation leak

### J. Race, retry, and eventual-consistency windows

Goal:
- Hit workflows where authorization and state transition are not atomic.

Steps:
- Identify operations with value, permission, or uniqueness: coupon redemption, gift cards, refunds, invite acceptance, role grants, exports, account activation, password reset, file sharing, quota changes, and deletion/restore.
- Send parallel requests from the same session, two sessions, two roles, and API plus browser at the same time.
- Race state transitions: approve/delete, invite/revoke, pay/cancel, refund/consume, downgrade/use, export/remove-access, transfer/act.
- Abuse retries: resend failed webhook, replay idempotency keys, omit idempotency keys, reuse old request bodies after state changes.
- Watch background jobs and delayed effects. If the UI says pending, the backend probably has a window.

Escalation paths:
- duplicate value issuance -> financial impact
- stale authorization in worker -> export/read/write after access removal
- double finalization -> privilege or entitlement drift
- retry replay -> unauthorized state transition

---

## Public-pattern anchors from the top-paid sample

1. **Imports are a gold mine**
   Repeated top-paid GitLab findings in the sample come from project import, bulk import, uploads pipelines, repository import, and parser-adjacent object flows.
   Lesson: whenever a target imports repositories, archives, markdown, diagrams, images, metadata, templates, spreadsheets, tickets, or third-party content, test the full ingestion path manually.

2. **Recovery and invite flows pay more than "normal login"**
   The sample includes high-value ATOs through password reset, leaked challenge tokens, partner email confirmation bypass, and alternate recovery paths.
   Lesson: test recovery, invite, onboarding, email confirmation, challenge, and approval flows before spending hours brute-forcing normal auth.

3. **Secondary objects leak where primary objects don't**
   The sample includes private object exposure via import, internal attachments via export, GraphQL GIDs, collaborator mutations, quick actions, and issue movement.
   Lesson: when the main object is protected, pivot to exports, previews, attachments, linked objects, copied objects, and helper mutations.

4. **Control-plane and internal tooling exposure stays expensive**
   The sample includes exposed Kubernetes APIs, Jenkins, Zeppelin, Artifactory, VPN, Spring Actuator, and internal docs/control surfaces.
   Lesson: manual recon of admin, CI, orchestration, and internal-support surfaces remains worth real money.

5. **Rendering paths still hide critical bugs**
   The sample includes repeated XSS through signin flows, markdown, diagrams, quick commands, and cache poisoning.
   Lesson: test every rendering sink that product teams think of as "formatting", not "execution".

6. **Role drift beats obvious admin endpoints**
   The sample includes role escalation, observer-to-key-creator abuse, improper auth to support bots, and destructive IDORs.
   Lesson: compare the effective power of each role against the intended power, especially on helper or support objects.

7. **Secrets beat scanners**
   The sample includes token exposures, leaked session cookies, exposed credentials, and GitHub-exposed internal secrets.
   Lesson: manual review of repositories, support flows, artifact systems, and generated files is still one of the highest ROI actions in bug bounty.

8. **GraphQL deserves object-centric testing**
   The sample includes object disclosure, mutation abuse, destructive IDOR, and mutation-aliasing abuse.
   Lesson: test GraphQL by object family and mutation side effect, not by introspection alone.

---

## Feature-driven manual checklists

### Recovery / reset / verification

Always try:
- scalar -> array/object replacement
- duplicate keys for destination fields
- stale token redemption after identity change
- multi-channel delivery
- alternate path redemption
- victim + attacker destinations in same request
- content-type switch (form to JSON)

### Import / migration / bulk operation

Always try:
- symlinks, hardlinks, nested archives, duplicate names
- local path confusion
- remote redirectors
- parser-targeted payloads in metadata and filenames
- imported references to private objects
- move/copy/export/import symmetry checks

### GraphQL

Always try:
- guessed IDs and GIDs
- read/mutate mismatch on same object family
- helper mutations
- mutation aliasing
- mixed-object batches across tenants
- destructive action with another user's object ID

### Rich rendering

Always try:
- markdown-specific payloads
- diagram/preview payloads
- filenames/metadata/comments as sink sources
- secondary renderers used in admin/support interfaces
- renderer options and config injection

### Control plane / support plane

Always try:
- low-priv user access to admin-ish objects
- helper role ownership -> privilege side effects
- bot/support/ticket objects with hidden data exposure
- read-only role performing create/update on keys, queues, approvals, or assignments

---

## Manual-first workflow

### 1. Pick one workflow, not one endpoint

Bad:
- "Test `/api/orders/123` for IDOR"

Better:
- "Test the whole order lifecycle: create, assign, view, refund, export, share, webhook, archive"

Endpoints lie. Workflows reveal assumptions.

Choose one workflow such as:
- signup / invitation / approval
- workspace creation / tenant switching
- payment / refund / coupon / billing credits
- report creation / export / share / comment / delete
- AI assistant creation / prompt source / knowledge base / history / attachments
- role assignment / ownership transfer / alerting / configuration
- password reset / email change / recovery / MFA reset

### 2. Build the actor matrix

For each workflow, enumerate:
- unauthenticated user
- freshly registered user
- invited user
- standard user
- elevated user
- owner/admin
- service account/API token
- background job/webhook consumer

Then ask:
- Which objects can each actor read?
- Which objects can each actor modify?
- Which objects can each actor create on behalf of someone else?
- Which transitions require approval in the UI but maybe not in the API?

### 3. Build the state matrix

For the same workflow, test objects in different states:
- draft
- pending
- approved
- rejected
- archived
- deleted
- expired
- imported
- shared externally

Most mature targets protect the happy state. Many fail on transitional states.

### 4. Attack assumptions, not inputs

For every state-changing flow, try:
- skipping a step
- replaying the last step
- calling the final endpoint first
- changing actor mid-flow
- changing tenant/workspace mid-flow
- changing object IDs after approval but before commit
- performing the action twice quickly
- performing the action from two sessions at once
- using stale links, stale tokens, stale invitations, stale previews
- invoking the same action through mobile/web/API variants

### 5. Chase secondary objects

When a main object looks protected, pivot to nearby objects:
- exports
- previews
- audit logs
- comments
- attachments
- signed URLs
- templates
- background jobs
- notification preferences
- webhook deliveries
- AI conversation history
- embeddings / sources / indexes / uploaded documents
- imported copies
- migration artifacts
- recovery state
- collaborator / membership mutations
- support / admin helper objects

Critical bugs often live in the nearby object, not the primary one.

---

## High-yield manual test themes

### Business logic

Test whether the product enforces:
- ordering of steps
- one-time use
- quantity/limit ceilings
- ownership at every phase
- separation between "can view" and "can act"
- consistency across UI and API
- consistency across create/import/clone/export/delete
- consistency across human workflow and background jobs

Good prompts:
- "What if the discount, refund, and credit systems disagree?"
- "What if approval is checked in the UI but not in the finalize endpoint?"
- "What if the product assumes the object owner never changes mid-flow?"
- "What if the imported copy has weaker checks than the original object?"
- "What if recovery validates the wrong state snapshot?"

### Authorization drift

Test every place where privilege is implied rather than explicit:
- team/workspace switchers
- alerting and admin subpanels
- AI assistants
- tenant-scoped search
- imports/exports
- hidden "internal" flags
- report- or case-management objects
- secondary APIs used by background workers
- collaborator-management APIs
- support bots and operator tooling
- imported or migrated objects
- GraphQL mutations with global IDs

### Signup, invite, recovery, and anti-automation

Manually inspect:
- optional anti-bot fields
- headers that exist only in browser traffic
- challenge fields present in one endpoint but absent in another
- invite acceptance versus invite preview
- account activation versus login
- reset-token state after email changes
- MFA reset paths that lag behind account state
- alternate recovery channels and fallback challenges
- partner / employee / delegated-admin onboarding flows

### AI/agent surfaces

Test whether the product leaks or over-trusts:
- chat history
- uploaded files
- retrieved documents
- system prompts
- knowledge-base IDs
- agent/topic IDs
- saved prompt templates
- cross-tenant embeddings or citations
- support bot or triage bot conversation objects
- agent configuration copied from another workspace

Treat AI features like ordinary multi-tenant apps with extra hidden objects.

### Import, parser, and ingestion surfaces

Manually test:
- project import
- repo import
- archive import
- metadata stripping / rewriting
- image/document processing
- markdown / wiki / diagram renderers
- template import
- CSV / spreadsheet import
- migration or bulk-import assistants
- external-link fetchers during import

Questions:
- Can the import read local files?
- Can it reach internal URLs?
- Can parser-side effects execute code?
- Does the imported object expose private linked data?
- Does validation happen before or after extraction/rewriting?

### Async and race-sensitive behavior

Manually test:
- duplicate submits
- concurrent membership changes
- parallel invite acceptance
- approval and deletion in close sequence
- checkout/refund/credit issuance overlap
- repeated export/download requests
- object transitions from two sessions or two roles

If the feature has queues, retries, or eventual consistency, race it.

### Exposed internal and operator surfaces

Manually inspect:
- Jenkins / CI
- Artifactory / package registries
- Kubernetes dashboards / APIs
- Spring Actuator / health / env / heapdump
- support panels
- admin sidecars
- VPN, SSO, or device-management portals
- internal docs and attachments reachable from external paths

---

## The manual hypothesis list

Use these prompts constantly:

- "What does the developer assume only the frontend will do?"
- "What object exists here that the product forgot to secure?"
- "What happens if this action is taken by the wrong actor at the right time?"
- "Which nearby feature would turn this medium into a critical?"
- "Where does the app copy state from one object to another?"
- "Which path was likely patched, and which sibling path was forgotten?"
- "What if the enforcement exists on create but not on update, export, clone, import, or retry?"
- "What if the AI feature inherited search access but not authorization filters?"
- "What if import, export, clone, or move changes the security model?"
- "What if this helper mutation was never threat-modeled like the main workflow?"
- "What if a support or operator surface trusts data from a lower-privileged context?"

---

## Evidence discipline

Manual testing should still produce structured proof:
- actor A
- actor B
- object ID
- object state
- exact step order
- exact request that changed outcome
- exact impact unlocked

Document the workflow, not just the request. For business logic findings, the sequence is part of the vulnerability.

---

## What success looks like

A good manual finding usually reads like one of these:
- "A standard user can finalize an owner-only action by replaying the approval endpoint with a swapped object state."
- "An AI assistant object is tenant-scoped in the UI but globally addressable in the backend."
- "A signup anti-automation control is enforced only on one branch of the onboarding flow."
- "An export/log/attachment object inherits visibility from the wrong parent object."
- "A race or retry path grants value twice because the state transition is not atomic."
- "An import or migration pipeline reads, fetches, or executes content the product assumes is inert."
- "A recovery or partner-confirmation path authenticates the attacker through a weaker side channel."
- "A GraphQL mutation or helper object changes authorization behavior compared to the main REST/UI flow."

If your notes are still just "possible IDOR on endpoint X", you have not pushed the manual analysis far enough.
