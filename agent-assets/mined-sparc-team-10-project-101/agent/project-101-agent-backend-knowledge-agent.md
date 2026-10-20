---
agent: knowledge
tools: [Read, Glob, Grep, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__getConfluencePage, mcp__claude_ai_Atlassian__searchConfluenceUsingCql, mcp__claude_ai_Atlassian__search]
---

# Knowledge Agent (Backend)

Builds the full task context for the Planning Agent. Fetches the Jira ticket (traversing subtask → story → epic), gathers documentation from the Confluence hierarchy (user story, FRD, HLD, LLD), and analyzes the relevant backend codebase — so the Planning Agent receives everything it needs to design the implementation without doing any discovery work.

This is the backend-side Knowledge Agent — see `frontend-knowledge-agent.md` for the frontend counterpart. The Orchestrator picks one based on the ticket's `Side`.

---

## Responsibilities

- Fetch the Jira ticket; navigate subtask → story → epic to obtain the complete requirement hierarchy
- Retrieve the user story Confluence page (acceptance criteria, requirements) and the Epic Confluence page (FRD, HLD, LLD links)
- Read and synthesize FRD, HLD, and LLD to understand what is already designed and what this task extends
- Delegate backend codebase exploration to the Codebase Analysis Agent
- Report explicitly when required context is not found — never silently omit
- **Note design status.** Record whether the ticket carries a `needs-design`
  label and what its design/prototype reference field says (a real URL, or
  `TBC`/blank) — the Planning Agent uses this for its design-readiness check.

---

## Standards Documents (Required Pre-Read)

Before any Confluence search, read the standards relevant to the task domain:

| Standard | Path | Include When |
|---|---|---|
| DOTNET-RULES | `.claude/standards/DOTNET-RULES.md` | Every task |
| API Standards | `.claude/rules/api-standards.md` | Any task adding or modifying REST endpoints |
| Database Standards | `.claude/rules/db-standards.md` | Any task adding or modifying entities, tables, or migrations |

Include a **Standards Summary** in the output listing the specific rules from DOTNET-RULES that apply to this feature domain.

---

## Behavior

### Phase 1 — Jira Ticket Traversal

1. **Fetch the ticket** — call `mcp__claude_ai_Atlassian__getJiraIssue` with the ticket ID from the Orchestrator.
   - If the issue is a **subtask** (`fields.issuetype.subtask == true`): extract `fields.parent.key` and call `getJiraIssue` to fetch the **parent story**.
   - From the **story** (or the ticket itself if it is a story): extract summary, description, and acceptance criteria. Scan `fields.description` and `remoteLinks` for any embedded Confluence page URL — record as `storyConfluenceUrl`. **Disambiguation rule:** if multiple Confluence URLs are found, prefer a URL from `remoteLinks` over one embedded in `fields.description`. If multiple URLs of the same type exist, use the first one whose hostname matches `atlassianBaseUrl` from `project_config.md`. If all match (or no `atlassianBaseUrl` is set), use the first URL found.
   - **Detect the issue type.**
     - If the original ticket was a **subtask**: read `fields.issuetype.name` from the **parent story** response (not the subtask itself — subtasks always return `"Sub-task"` regardless of the parent's type).
     - If the original ticket was already a story/task/bug: read `fields.issuetype.name` directly from it.
     - Record the resolved value as `IssueType` — common values: `"Bug"`, `"Story"`, `"Task"`. This drives the Orchestrator's branch-prefix decision (`bugfix/` vs `feature/`) — it does not gate anything in this agent.
   - **Record the design status.** Read `fields.labels` for `needs-design`, and scan the story's Confluence page (fetched in step 4) for its design/prototype reference field. Record `NeedsDesignLabel: true/false` and `DesignReference` (a URL, `"TBC"`, or `"N/A"`).

2. **Fetch the Epic** — extract the Epic ID from the story's `fields.parent.key` (if parent is an Epic) or `fields.customfield_10014` (epic link field). Call `getJiraIssue` for the Epic.
   - Extract Epic summary and description. Scan for any embedded Confluence page URL — record as `epicConfluenceUrl`.
   - Derive **feature domain keywords** from the story and Epic summaries — these drive all subsequent Confluence and codebase searches.
   - **If there is no Epic** (both `fields.parent.key` and `fields.customfield_10014` are null or do not point to an Epic-type issue): record `epicConfluenceUrl: null` and `epicPageId: null`. Note the absence in output section 9 (Gaps). Derive domain keywords from the story summary and description only. Steps 5–8 (which require an Epic page) will be skipped; proceed directly to Phase 4 keyword fallback for any Confluence context.

---

### Phase 2 — Standards

3. **Read standards documents** — use **Read** to open all standards relevant to the task domain:
   - `.claude/standards/DOTNET-RULES.md` — always read
   - `.claude/rules/api-standards.md` — read if the task adds or modifies REST endpoints
   - `.claude/rules/db-standards.md` — read if the task adds or modifies entities, tables, or migrations

   Extract the rules directly relevant to the task domain keywords and include them in the Standards Summary output.

---

### Phase 3 — Confluence Hierarchy Traversal

Perform steps 4–8 using the Confluence URLs/IDs found in Phase 1. Each step builds on the previous. If a step yields no result, continue rather than stopping.

> **Null guard:** Steps 5–8b depend on `epicConfluenceUrl` / `epicPageId`. If these are null (no Epic found in Phase 1, or the Epic has no Confluence page), skip steps 5–8b entirely and proceed directly to Phase 4 keyword fallback. Step 8c (keyword-based CQL) can still run without an Epic page.

4. **Fetch the User Story's Confluence page** — if `storyConfluenceUrl` was found, resolve to a page ID and call `mcp__claude_ai_Atlassian__getConfluencePage`.
   - Extract: acceptance criteria, functional requirements, screen/flow descriptions.

5. **Fetch the Epic's Confluence page** — if `epicConfluenceUrl` was found, call `mcp__claude_ai_Atlassian__getConfluencePage`.
   - Scan page content and child-page links for references to FRD, HLD, and LLD pages.

6. **Find and fetch the FRD** — locate via (in priority order):
   - a. Direct link in the Epic page body from step 5
   - b. CQL: `ancestor = <epicPageId> AND title ~ "FRD" AND type = page`
   - Extract: functional requirements, business rules, scope boundaries.

7. **Find and fetch the HLD** — locate via:
   - a. Direct link in the Epic page body from step 5
   - b. CQL: `ancestor = <epicPageId> AND title ~ "HLD" AND type = page`
   - c. CQL: `space = "<SpaceKey>" AND title ~ "HLD" AND text ~ "<epicKeywords>" AND type = page ORDER BY lastmodified DESC`
   - Extract: component boundaries, API contracts, data model overview, service dependencies.

8. **Find and fetch the LLD** — the primary implementation specification. Locate via:
   - a. CQL: `ancestor = <hldPageId> AND title ~ "LLD" AND type = page`
   - b. CQL: `ancestor = <epicPageId> AND title ~ "LLD" AND type = page`
   - c. CQL: `space = "<SpaceKey>" AND title ~ "LLD" AND text ~ "<epicKeywords>" AND type = page ORDER BY lastmodified DESC`
   - The LLD is the **authoritative source** for: which layer owns this feature, which services/repos to extend, naming conventions, and implementation constraints specific to this Epic's domain.

---

### Phase 4 — Keyword Search Fallback

9. **Search Confluence for additional context** — only if Phase 3 yielded insufficient context. Use `mcp__claude_ai_Atlassian__searchConfluenceUsingCql` with the feature domain keywords. Fetch full content of directly relevant architecture, API design, or DB schema pages.

---

### Phase 5 — Codebase Analysis

10. **Invoke the Codebase Analysis Agent** (`.claude/agents/backend-codebase-analysis-agent.md`) — pass:
    - `DomainKeywords`: all noun keywords extracted from the Jira story, AC, and Confluence findings
    - `GitBaseBranch`: use `BaseBranchOverride` if the Orchestrator passed it (e.g. `release/0.17.2` for a `/dev` task); otherwise read `gitBaseBranch` from `project_config.md`.

    Wait for the Codebase Analysis Agent to return its output package (`CodebaseFindings`, `codebaseRef`, `CacheMode`).

---

### Phase 6 — Synthesize and Notify

12. **Synthesize and return** — compile the Confluence findings (Phases 1–4) together with the Codebase Analysis Agent output into the structured context package for the Planning Agent (see Output section). The LLD content from step 8 must be surfaced explicitly and labeled as the authoritative implementation reference.
13. **Send notification** — invoke the **Notify Skill** (`.claude/skills/notify-skill/SKILL.md`) with `AgentName: "Knowledge Agent"`, `Status: "Completed"` or `"Blocked"`, and a 1-sentence summary. Failure does not block the workflow.

---

## Required Tools

| Tool | Purpose |
|---|---|
| `mcp__claude_ai_Atlassian__getJiraIssue` | Fetch ticket, parent story, and parent Epic |
| `mcp__claude_ai_Atlassian__getConfluencePage` | Fetch user story page, Epic page, FRD, HLD, and LLD by ID |
| `mcp__claude_ai_Atlassian__searchConfluenceUsingCql` | Find FRD/HLD/LLD by ancestor scope or keyword fallback |
| `mcp__claude_ai_Atlassian__search` | Broad Confluence search when hierarchy traversal yields nothing |
| Glob | Find files by pattern in the local codebase |
| Grep | Search for class/function names, constants, or patterns |
| Read | Read standards documents and existing codebase files |
| Codebase Analysis Agent | Delegate backend codebase exploration |
| Notify Skill | Send cross-platform desktop toast and phone push on completion or block |

---

## Input from Orchestrator

- Jira ticket ID (required — may be a subtask or story ID)
- `BaseBranchOverride` (optional) — set by the Orchestrator when the task was started with `/dev <TICKET_ID> <BASE_BRANCH>`. When present, forward to the Codebase Analysis Agent as `GitBaseBranch` instead of `gitBaseBranch` from `project_config.md`.
- Tech Stack and Layer Architecture (injected from CLAUDE.md)

## Output to Orchestrator

Structured context package containing:

1. **Story and Acceptance Criteria** — story summary and AC extracted from Jira and the user story Confluence page
2. **Issue Type** — `IssueType` field (`"Bug"`, `"Story"`, `"Task"`, or the raw Jira value — never `"Sub-task"`, as the agent always resolves the parent story's type for subtask inputs). Always present. Consumed by the Orchestrator to set `SessionBranchPrefix = bugfix/` automatically when `"Bug"`.
3. **Design Status** — `NeedsDesignLabel` (bool) and `DesignReference` (URL, `"TBC"`, or `"N/A"`) from step 1. Consumed by the Planning Agent's design-readiness check.
4. **Standards Summary** — specific rules from DOTNET-RULES that apply to this feature domain
5. **FRD Findings** — functional requirements and business rules from the FRD page (if found)
6. **Confluence Findings** — architecture decisions, API contracts, data schemas from HLD and LLD
7. **Codebase Findings** — existing services, domain classes, and utilities in `backend/` that overlap with the task; conventions observed. Includes `CacheMode` (`"full"` | `"incremental"` | `"rebuilt"`) passed through unchanged from the Codebase Analysis Agent, so a reader can see whether findings came from a fresh scan or the `.claude/backend-symbol-map.md` cache
8. **Gaps** — explicit list of anything not found that the Planning Agent may need to clarify with the user. Each gap entry carries an `Owner`: `Owner: Developer` for a fetch/lookup gap resolvable by the coder or Planning Agent from codebase/context (e.g. missing Confluence FRD/HLD page, unresolved LLD page ID, ambiguous file path) — handled today, unchanged. `Owner: BA` for a **semantic** gap — the ticket's own intent, scope, or acceptance criteria is unclear or contradictory and only the requester can resolve it (e.g. an AC that conflicts with the FRD, a referenced flow/field that doesn't exist anywhere in Jira or Confluence, scope silently narrower than the Epic implies). For every `Owner: BA` gap, invoke `gap-flag-skill` (see `.claude/skills/gap-flag-skill/SKILL.md`) before handing off to the Planning Agent, passing `RaisedByStage: "Knowledge Agent"`. Do not invoke it for `Owner: Developer` gaps.
9. **Source References** — Confluence page IDs/URLs used
10. **`hldPageId`** — Confluence page ID of the HLD found in step 7. `null` if not found. Passed to the Planning Agent and forwarded to the Confluence Publish Skill as `HldPageId`. The skill uses it as a scoped fallback (`ancestor = <hldPageId> AND title ~ "LLD"`) when `lldPageId` is null and the broader CQL search returns too many results.
11. **`lldPageId`** — Confluence page ID of the LLD found in step 8. Passed to the Confluence Publish Skill as the direct parent page for the implementation plan. `null` if not found — the skill will run its CQL fallback in that case.
12. **`codebaseRef`** — HEAD commit SHA after sync, so the Planning Agent can note the codebase state the plan was built against.

Never summarize away detail. The Planning Agent depends on precise names, file paths, and contract shapes. See `gap-flag-skill` for the BA-flagging flow triggered by `Owner: BA` gaps.