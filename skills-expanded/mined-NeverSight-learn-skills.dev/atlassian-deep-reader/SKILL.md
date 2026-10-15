---
name: atlassian-deep-reader
description: >
  Deep-reads Jira tickets and Confluence pages for developer implementation
  context. Fetches the full ticket, analyzes images via LLM vision, searches
  for related docs beyond explicit links, checks PRs/branches/commits,
  detects duplicate/regression bugs, follows Confluence links recursively
  (up to 2 levels), flags conflicting information across sources, and
  produces an actionable implementation plan. Use when the user pastes a
  Jira key (e.g. PROJ-123) or URL, says "read this ticket", "what do I
  need to do", "deep read", "summarize this issue", "check the docs",
  "what's the context", or any request to understand Jira/Confluence
  content before implementing. NOT for creating or updating tickets.
license: MIT
compatibility: "Requires MCP-Atlassian server. Core toolsets plus jira_attachments, confluence_attachments. Optional: jira_development, jira_metrics, confluence_analytics."
metadata:
  author: crazyads69
  version: "1.1.1"
---

# Atlassian Deep Reader

Read Jira tickets and Confluence pages as a **developer preparing to
implement** — not just a summary, but an actionable implementation plan.

## Gotchas

- **Image tools return inline ImageContent for LLM vision.** Both
  `jira_get_issue_images` and `confluence_get_page_images` let you see
  images directly. No download/rendering needed. Just call and describe.

- **Confluence param names are inconsistent — three different names.**
  `confluence_get_page` uses `page_id`. `confluence_get_page_images` and
  `confluence_get_attachments` use `content_id`. `confluence_get_page_children`
  uses `parent_id`. All three are the same numeric value.

- **Markdown mode hides content.** Confluence in markdown loses Jira macros,
  status labels, expand blocks, draw.io diagrams. If content seems short,
  re-read with `convert_to_markdown: false` (HTML mode).

- **Dev info needs `jira_development` toolset.** If
  `jira_get_issue_development_info` fails, tell user to enable it.

- **Subtask descriptions contain the real spec.** The parent story often
  has only the business requirement. Backend/Web/FE subtasks contain the
  API contracts, error codes, and technical decisions. Always deep-read
  implementation subtasks, not just list their status.

- **Subtasks use JQL, not a field.** Find via `parent = PROJ-123`.

- **Epic link field varies.** Check `parent` first; if absent, use
  `jira_search_fields: {"keyword": "epic"}`.

- **Comments contain the real context.** Use `comment_limit: 50`.

- **Confluence links can be circular.** Track visited page IDs in a set.

- **`confluence_search` returns snippets, not content.** Search results
  have 1-2 line previews. You MUST call `confluence_get_page` to read the
  actual page. Never list search snippets as your Confluence analysis.

- **Large Confluence pages eat context.** If a page is very long, summarize
  it rather than dumping everything. Prioritize info relevant to the ticket.

- **Don't fire 50 API calls at once.** Process links sequentially or in
  small batches to respect rate limits.

---

## Workflow 1: Deep-Read a Jira Issue

### Phase 1 — Gather core content

- [ ] **1. Get issue with all fields and comments**
  ```
  jira_get_issue:
    issue_key: "PROJ-123"
    fields: "*all"
    expand: "renderedFields"
    comment_limit: 50
  ```
  Immediately note the **issue type** (Bug/Story/Task/Epic) — this
  determines what to extract in Phase 4.

- [ ] **2. Get images (LLM vision)**
  ```
  jira_get_issue_images:
    issue_key: "PROJ-123"
  ```
  For bugs: error screenshots, console logs, broken UI states.
  For features: mockups, wireframes, Figma exports, flow diagrams.
  Quote error text verbatim. Describe layouts precisely.

- [ ] **3. Get non-image attachments**
  ```
  jira_download_attachments:
    issue_key: "PROJ-123"
  ```
  ⚠️ This downloads ALL attachments including images. Skip files already
  analyzed in step 2 (extensions: .png, .jpg, .jpeg, .gif, .svg, .webp).
  Focus on: API specs, log files, HAR files, Postman collections,
  design docs, CSV test data.

  **Fallback:** If step 2 returned no images but this step returns image
  files (.png, .jpg, etc.), analyze those via their base64 content — some
  Jira instances store images only as regular attachments.

### Phase 2 — Enrich context

**Every step below MUST produce output** — either the data, or an explicit
note like "⚠️ Dev info unavailable — `jira_development` toolset not enabled."
Never silently omit a section. The user needs to know what was checked and
what wasn't.

- [ ] **4. Development info** (PRs, branches, commits)
  ```
  jira_get_issue_development_info:
    issue_key: "PROJ-123"
  ```
  Extract: repo name, branch name, changed file paths, PR status,
  review comments. Tells you if work started and where in the codebase.

  **If tool fails:** Include in output: "🔀 **Development Status:** ⚠️
  Unavailable — enable `jira_development` toolset in MCP-Atlassian config
  (`TOOLSETS=default,jira_development,...`)."
  **If tool returns empty:** Include: "🔀 **Development Status:** No PRs,
  branches, or commits linked to this issue."

- [ ] **5. Subtasks**
  ```
  jira_search:
    jql: "parent = PROJ-123"
    fields: "summary,status,assignee,issuetype"
  ```

  **Deep-read implementation subtasks:** For each subtask that is a
  Backend, Web, or Frontend type (not QA), do a deeper read:
  ```
  jira_get_issue:
    issue_key: "PROJ-SUB"
    fields: "summary,status,description,assignee,comment,attachment"
    expand: "renderedFields"
    comment_limit: 20
  ```
  The parent story often has only the business requirement. The subtask
  descriptions contain the actual **API contracts, error codes, technical
  details, and implementation decisions** that a developer needs. This is
  where the real spec lives.

- [ ] **6. Epic context** — if issue has a parent epic, shallow-read it.

- [ ] **7. Status history**
  ```
  jira_get_issue_dates:
    issue_key: "PROJ-123"
    include_status_changes: true
    include_status_summary: true
  ```
  Shows when issue moved between statuses and how long it stayed in each.
  Reveals bottlenecks like "stuck in Code Review for 2 weeks."

  **If tool fails:** Include in output: "⏱️ **Status History:** ⚠️
  Unavailable — enable `jira_metrics` toolset."
  **If tool returns data:** Include the full status transition table.

### Phase 3 — Contextual discovery (search beyond explicit links)

The ticket may not link to all relevant docs. Search for related content
the author forgot to link or didn't know about.

- [ ] **8. Search Confluence for related docs** using keywords from the
  ticket summary, description, and component names:
  ```
  confluence_search:
    query: "keywords from ticket title and description"
    limit: 10
  ```
  Extract 2-4 keywords from the ticket (system name, feature name,
  technical terms). Don't use full sentences — just key terms.

  Example: ticket "Support getting tone voice list from API" →
  search `"tone voice API"`, then `"agent voice configuration"`.

  **⚠️ Search results are just pointers, not content.** The snippets
  from `confluence_search` are too brief to extract implementation detail.
  For any relevant result (top 3-5), you MUST fetch the full page:
  ```
  confluence_get_page:
    page_id: "<id from search result>"
    include_metadata: true
    convert_to_markdown: true
  ```
  Then extract developer-relevant info (API specs, architecture, config).
  List these under 🔍 **Discovered Documentation** (separate from
  📚 Linked Documentation which comes from explicit ticket links).

  **Output rule:** Every Confluence page mentioned in your output MUST
  have one of these tags:
  - `(Updated 2026-03-18 — ✓ current)` — you read it and checked freshness
  - `(Updated 2024-06-01 — ⚠️ 20 months old)` — you read it, it's stale
  - `(search result only — not read)` — you listed it from search but
    didn't fetch the full page. Use this for low-relevance results.

- [ ] **9. For bugs: search for similar/previously-fixed issues**
  ```
  jira_search:
    jql: "project = PROJ AND type = Bug AND text ~ \"error keywords\" ORDER BY updated DESC"
    fields: "summary,status,resolution,assignee,updated"
    limit: 10
  ```
  Look for:
  - **Duplicate:** same error + same component + recent (<30 days) →
    flag: "⚠️ Possible duplicate of PROJ-XXX"
  - **Regression:** same error that was previously resolved →
    flag: "⚠️ Possible regression of PROJ-XXX (fixed [date] by @person)"
  - **Related:** similar symptoms, different root cause →
    note under Related Issues

  Skip this step for features/tasks.

### Phase 4 — Follow documentation links

- [ ] **10. Extract ALL links** from `renderedFields` (primary source).

  Links live in `renderedFields.description` and
  `renderedFields.comment.comments[].body` as HTML `<a href="...">` tags.
  Do NOT parse the raw `description` field (it's ADF JSON on Cloud, which
  is much harder to extract links from). Always use `renderedFields`.

  **Link patterns to find:**
  - Confluence: `*.atlassian.net/wiki/spaces/*/pages/*` → extract page ID
  - Confluence short: `/wiki/x/*` → search by title
  - Confluence display: `/display/SPACE/Title` → title+space lookup
  - Jira: `*.atlassian.net/browse/PROJ-*` → note as related issue
  - External: any other URLs → list under External Links

  For each Confluence link: run **Workflow 2** (depth=0).
  Also read any relevant pages discovered in step 8.
  See [references/link-extraction.md](references/link-extraction.md).

- [ ] **11. Check issue links** from `issuelinks` field. Build a
  **dependency chain**: what blocks this → this issue → what it unblocks.
  For blockers, do a shallow read.

### Phase 5 — Extract developer context (TYPE-SPECIFIC)

Based on issue type, extract structured implementation context.
Load [references/developer-context.md](references/developer-context.md)
for detailed extraction patterns. Summary:

**Bugs:** repro steps, error details (verbatim), expected vs actual,
affected code (from stack traces + PR file paths), environment, root
cause hypothesis, fix approach. **Also check step 9 results for
duplicates/regressions.**

**Features/Stories:** acceptance criteria (checkboxes, Given/When/Then),
API contracts, design refs (Figma links, mockup images analyzed via
vision), technical scope (repos/services/files), non-functional reqs.
**Also note any related docs found via search in step 8 that aren't
linked from the ticket.**

**Tasks:** specific deliverable, technical scope, completion criteria.

**All types:** dependency chain, open questions (ambiguities that would
block implementation), implementation steps.

### Phase 6 — Validate & synthesize

- [ ] **12. Validation** — go through this checklist. For ANY item
  answered "no", you MUST include an explicit note in the output:

  - [ ] Did I call `jira_get_issue_images`?
  - [ ] Did I call `jira_download_attachments`? (logs, specs, etc.)
  - [ ] Did I call `jira_get_issue_development_info`? (include 🔀 section)
  - [ ] Did I call `jira_get_issue_dates`? (include ⏱️ section)
  - [ ] Did I deep-read implementation subtasks (Backend/Web/FE)?
  - [ ] Did I search Confluence for related docs beyond explicit links?
  - [ ] For bugs: did I search for similar/previously-fixed issues?
  - [ ] Did I **fetch full page content** (`confluence_get_page`) for each
    Confluence link — not just use search snippets? Search snippets are
    too brief. You MUST read the actual page.
  - [ ] Did I include a freshness note for each Confluence page read?
  - [ ] Did I separate 📚 Linked Documentation from 🔍 Discovered Docs?
  - [ ] Did I include ⚠️ Conflicting Information section?
    (either list conflicts, or say "No conflicting info found")

  **Conflict detection:** Review ALL gathered info. If sources contradict
  each other, flag explicitly:

  > ⚠️ **Conflicting info:** [Source A] says X, but [Source B] says Y.
  > Verify which is current before implementing.

  Common conflicts:
  - Confluence doc vs ticket comment (comment may be newer)
  - Two Confluence pages disagree (one may be stale)
  - Description vs attached image
  - API spec in doc vs actual implementation (from subtask description)

  **Rule: every section heading from the output template must appear.**
  A section can say "N/A" or "No conflicts found" but cannot be omitted.

- [ ] **13. Synthesize** — load
  [references/output-templates.md](references/output-templates.md).
  Output MUST lead with **🛠️ Implementation Plan** — the actionable part —
  then back it up with evidence sections.

---

## Workflow 2: Deep-Read a Confluence Page

Track `depth` (start 0) and a visited set of page IDs.

### Phase 1 — Read

- [ ] **1. Get page** — `confluence_get_page` with `include_metadata: true`
- [ ] **2. Validate** — if short, re-read with `convert_to_markdown: false`
- [ ] **3. Images** — `confluence_get_page_images` (⚠️ uses `content_id`)
- [ ] **4. Attachments** — `confluence_get_attachments` (⚠️ `content_id`)

### Phase 2 — Freshness assessment (ALWAYS do this, not just depth 0)

- [ ] **5. Staleness check** — from the metadata returned in step 1, extract
  `lastModified` date and `version` number. **Always include a freshness
  line in your output for every Confluence page you read:**

  - If <1 month old: "(Updated [date] — current)"
  - If 1-6 months old: "(Updated [date] — check if still accurate)"
  - If >6 months old: "⚠️ Last updated [date] — content may be outdated"

  Then check comments for corrections newer than the page:
  ```
  confluence_get_comments:
    page_id: "<id>"
  ```
  If a comment says "this is outdated" or contradicts page content, flag
  it prominently — the comment may be more accurate than the page.

  If `confluence_analytics` toolset is available, also check:
  ```
  confluence_get_page_views:
    page_id: "<id>"
  ```
  Low views + old = likely stale. High views + old = actively used but
  possibly outdated. Include view count if available.

### Phase 3 — Follow links

- [ ] **6. Internal links** — depth limits:

  | Depth | Action |
  |---|---|
  | 0 | Read fully, follow all links → depth 1 |
  | 1 | Read fully, follow ≤5 links → depth 2 |
  | 2 | Summarize only. Stop. |

  Max 10 pages total. Skip visited. If limit hit, tell user which pages
  remain and offer to continue.

- [ ] **7. Child pages** — `confluence_get_page_children` (⚠️ uses `parent_id`).
  List; auto-read first 5 if thorough read.
- [ ] **8. Labels + comments**

### Phase 4 — Extract developer-relevant info

When reading pages linked from a Jira issue, specifically extract:
- API specs (endpoints, auth, request/response formats)
- Architecture (services, connections, data flows)
- DB schemas (tables, migrations, constraints)
- Config (env vars, feature flags, URLs)
- Code examples (patterns to follow)
- Business rules (validation, edge cases)

### Phase 5 — Synthesize

Load [references/output-templates.md](references/output-templates.md).

---

## Graceful Degradation

| Situation | Action |
|---|---|
| MCP-Atlassian not connected | Tell user: run `scripts/validate-setup.sh` |
| Tool not available | Name the exact toolset to enable |
| Vision not available | List image URLs so user can view manually |
| Confluence page 404/restricted | Note "couldn't access" and continue |
| Very large page (>10K words) | Summarize; prioritize ticket-relevant info |
| Rate limited | Pause, summarize progress, offer to continue |

## Error Handling

Never skip silently. Always report: not found, permission denied, tool
unavailable (name the toolset), empty content, no images, rate limits.

## Reference Files

- **[references/tool-parameters.md](references/tool-parameters.md)** —
  Exact MCP-Atlassian API params.
- **[references/output-templates.md](references/output-templates.md)** —
  Implementation Plan templates (Bug/Feature/Task).
- **[references/developer-context.md](references/developer-context.md)** —
  Type-specific extraction patterns for Phase 4.
- **[references/link-extraction.md](references/link-extraction.md)** —
  URL regex patterns, Confluence macro parsing, draw.io refs.
