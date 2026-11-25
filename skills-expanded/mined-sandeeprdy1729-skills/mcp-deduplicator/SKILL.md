---
name: mcp-deduplicator
description: >
  MCP tool deduplication and unified abstraction layer for multi-server setups.
  Activate when the user has multiple MCP servers installed and wants to reduce tool
  noise, detect overlapping tools, understand which tool to use for a given task, or
  create routing rules that prevent Claude from wasting tokens choosing between
  near-identical tools.
  Handles: semantic duplicate detection across MCP servers, unified tool abstraction
  mapping, routing rule generation, tool conflict resolution, canonical tool naming,
  and per-server tool audits.
  Use when user says: too many tools, duplicate tools, MCP overlap, tool overload,
  which tool should I use, GitHub vs GitLab tools, Jira vs Linear tools, deduplicate
  my tools, clean up my MCP, tool conflict, tool sprawl, consolidate tools,
  multiple MCP servers, tool redundancy.
  Do NOT activate for: installing MCP servers, configuring individual MCP servers,
  writing code that calls MCP tools, general MCP setup questions without a
  deduplication goal.
  First response: "MCP Deduplicator active. List your connected MCP servers or paste
  their tool manifests. I'll map duplicates and produce a clean routing layer."
license: Apache 2.0
---

# MCP Tool Deduplicator

The MCP ecosystem has 2000+ servers. Users routinely install 3–6 per project, and
conceptually identical operations (create a task, search code, post a comment) exist
across GitHub, GitLab, Jira, Linear, Notion, and others under different names and
schemas. Without deduplication, Claude burns tokens at every turn evaluating 40–90
tools to decide between semantically equivalent ones — and sometimes picks the wrong
one.

This skill maps every available tool across all connected MCP servers, detects semantic
duplicates, and produces a unified abstraction layer with explicit routing rules so
Claude is presented with a clean, deduplicated toolset.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/scan` | Full scan of all connected MCP servers; output duplicate map |
| `/diff <server-a> <server-b>` | Compare two specific servers tool-by-tool |
| `/abstract <operation>` | Show the canonical abstraction for a named operation (e.g. "create issue") |
| `/route <query>` | Given a natural language task, recommend the single best tool to use |
| `/matrix` | Print the full deduplication matrix (all servers × all canonical operations) |
| `/config` | Generate a `.mcp-dedup.yml` routing config ready to paste into your project |
| `/audit <server>` | List all tools from a single server with duplicate annotations |
| `/stats` | Summary: total tools, duplicate count, reduction %, canonical operations |
| `/simulate <query>` | Test the routing config by running a natural-language query through it — shows which tool wins |
| `/test-all` | Run 10 common operations through the routing layer; show tool resolution for each |
| `/verify` | After generating config, automatically run /simulate on 5 common queries to confirm routing works |

---

## HIGH-LEVEL WORKFLOW

```
Input: tool manifests from ≥2 MCP servers (or a list of server names)
    │
    ├─ Phase 1: Inventory
    │     Collect all tool names, descriptions, parameter schemas
    │
    ├─ Phase 2: Semantic Grouping
    │     Cluster tools by canonical operation category
    │
    ├─ Phase 3: Duplicate Detection
    │     Within each cluster, score pairs for semantic similarity
    │     Flag duplicates, near-duplicates, and functional equivalents
    │
    ├─ Phase 4: Canonical Selection
    │     For each duplicate group, select the preferred tool
    │     Apply selection criteria (schema richness, server priority, specificity)
    │
    ├─ Phase 5: Routing Layer
    │     Generate routing rules: canonical name → preferred tool + fallback
    │     Produce .mcp-dedup.yml config
    │
    └─ Phase 6: Validation
          Verify no canonical operation is left without a tool
          Flag any tool with no canonical match (unique capability — keep it)
```

---

## PHASE 1 — INVENTORY

For each connected MCP server, collect:

1. **Server name** (e.g. `github`, `gitlab`, `jira`, `linear`, `notion`, `slack`).
2. **Tool list** — name, description, and parameter schema for every tool.
3. **Server priority** — user-defined preference order. If not provided, ask:
   ```
   Which server is your primary for [code hosting / task management / docs]?
   This determines which tool wins when duplicates are found.
   ```

If the user cannot paste tool manifests directly, use the known tool lists for common
servers from the built-in registry (see Phase 2 — Standard Operation Taxonomy).

**Tool record format:**

```
server   : github
name     : create_issue
desc     : "Creates a new issue in the specified repository"
params   : { owner, repo, title, body, labels[], assignees[] }
category : [unresolved — assigned in Phase 2]
```

---

## PHASE 2 — SEMANTIC GROUPING

Assign each tool to one or more **canonical operation categories**. These are
server-agnostic operation names that represent what the tool does, not which server
it belongs to.

### Standard Operation Taxonomy

| Category | Canonical name | Example tools across servers |
| --- | --- | --- |
| **Issue management** | `issue.create` | `create_issue` (GitHub), `create_ticket` (Jira), `createIssue` (Linear) |
| | `issue.get` | `get_issue`, `fetch_ticket`, `get_issue_detail` |
| | `issue.list` | `list_issues`, `search_issues`, `get_issues` |
| | `issue.update` | `update_issue`, `edit_ticket`, `update_issue` |
| | `issue.comment` | `add_issue_comment`, `add_comment`, `create_comment` |
| | `issue.close` | `close_issue`, `resolve_ticket`, `complete_issue` |
| **Pull request / MR** | `pr.create` | `create_pull_request`, `create_merge_request` |
| | `pr.get` | `get_pull_request`, `get_merge_request` |
| | `pr.list` | `list_pull_requests`, `list_merge_requests` |
| | `pr.review` | `create_review`, `submit_review`, `approve_merge_request` |
| | `pr.merge` | `merge_pull_request`, `merge_merge_request` |
| | `pr.comment` | `add_pull_request_review_comment`, `add_comment_to_mr` |
| **Repository** | `repo.get` | `get_repository`, `get_repo`, `fetch_project` |
| | `repo.list` | `list_repositories`, `get_repos`, `search_projects` |
| | `repo.search` | `search_repositories`, `search_code` |
| | `repo.file` | `get_file_contents`, `get_file`, `fetch_file` |
| | `repo.push` | `push_files`, `create_or_update_file`, `commit_file` |
| **User** | `user.get` | `get_me`, `get_user`, `whoami` |
| | `user.search` | `search_users`, `find_user` |
| **Search (global)** | `search.code` | `search_code`, `search_repositories` |
| | `search.issues` | `search_issues`, `search_tickets` |
| **Notifications** | `notification.list` | `list_notifications`, `get_notifications` |
| | `notification.read` | `mark_notification_read`, `dismiss_notification` |
| **Documents / pages** | `doc.create` | `create_page` (Notion), `create_document` (Google) |
| | `doc.get` | `get_page`, `fetch_document` |
| | `doc.update` | `update_page`, `edit_document` |
| **Messaging** | `message.send` | `send_message` (Slack), `post_message` |
| | `message.list` | `list_messages`, `get_channel_history` |
| **Releases / tags** | `release.get` | `get_latest_release`, `get_release_by_tag` |
| | `release.list` | `list_releases`, `list_tags` |

Tools that do not match any standard category are tagged `UNIQUE` and always kept.

---

## PHASE 3 — DUPLICATE DETECTION

Within each canonical category, score every pair of tools for semantic similarity.

### Similarity Scoring

A tool pair is scored on four axes:

| Axis | Weight | Description |
| --- | --- | --- |
| **Name similarity** | 20% | Edit distance / token overlap between tool names |
| **Description similarity** | 40% | Semantic similarity of the description strings |
| **Parameter schema overlap** | 30% | Fraction of parameters that map to the same concept |
| **Category match** | 10% | Whether both tools were assigned the same canonical category |

**Composite score** = (name × 0.2) + (desc × 0.4) + (schema × 0.3) + (category × 0.1)

### Duplicate Thresholds

| Score | Classification | Action |
| --- | --- | --- |
| ≥90 | **Exact duplicate** | Keep one; suppress the other entirely |
| 70–89 | **Functional equivalent** | Keep one as canonical; expose the other only if server is specified |
| 50–69 | **Near-duplicate** | Keep both but add routing rules to disambiguate |
| <50 | **Distinct** | Keep both; no deduplication needed |

### Duplicate Report Format

```
┌─ DUPLICATE GROUP: issue.create
│  Tools in group: 3
│  ────────────────────────────────────────────────
│  github  / create_issue           score vs primary: baseline
│  jira    / create_ticket          score vs primary: 82  [FUNCTIONAL EQUIVALENT]
│  linear  / createIssue            score vs primary: 91  [EXACT DUPLICATE]
│  ────────────────────────────────────────────────
│  Canonical selection: github/create_issue  (highest schema richness: 6 params)
│  Suppressed: linear/createIssue  (exact duplicate)
│  Demoted:    jira/create_ticket   (functional equivalent; available via /route or
│                                    when jira server explicitly requested)
│  ────────────────────────────────────────────────
│  Routing note: use github/create_issue by default.
│  Use jira/create_ticket when the user mentions "Jira", "project key", or a Jira
│  issue ID (e.g. PRJ-123).
└──────────────────────────────────────────────────────────────────────
```

---

## PHASE 4 — CANONICAL SELECTION

For each duplicate group, select the **canonical tool** using this priority order:

1. **Server priority** — user's declared primary server wins.
2. **Schema richness** — the tool with the most parameters (more expressive) wins.
3. **Description clarity** — prefer a tool whose description is ≥1 full sentence over
   single-word descriptions.
4. **Name clarity** — prefer snake_case names with a clear verb_object structure
   (`create_issue`) over camelCase or abbreviated names (`createIssue`, `ci`).

**Fallback handling:**
If the user does not declare a server priority and two tools score equally, present
both as co-canonicals and ask the user to choose:

```
Tie: github/create_pull_request vs gitlab/create_merge_request
Both score 88. These are functional equivalents for different platforms.
Which platform is your primary? Or keep both with platform-keyword routing?
```

---

## PHASE 5 — ROUTING LAYER

### Routing Rule Format

Each routing rule maps a canonical operation to a preferred tool with optional
override conditions:

```yaml
# .mcp-dedup.yml
routing:
  issue.create:
    default: github/create_issue
    overrides:
      - condition: "user mentions 'Jira' or issue ID matches /[A-Z]+-\\d+/"
        use: jira/create_ticket
      - condition: "user mentions 'Linear' or team is 'eng'"
        use: linear/createIssue

  pr.create:
    default: github/create_pull_request
    overrides:
      - condition: "user mentions 'GitLab' or 'merge request'"
        use: gitlab/create_merge_request

  doc.create:
    default: notion/create_page
    # No GitHub equivalent — Notion is the only doc server

  message.send:
    default: slack/send_message
```

### Suppressed Tools

Tools classified as exact duplicates and not selected as canonical are listed under
`suppressed`. They remain available if called explicitly but are hidden from Claude's
default tool selection:

```yaml
suppressed:
  - linear/createIssue        # exact duplicate of github/create_issue
  - gitlab/list_issues        # exact duplicate of github/list_issues
```

### Unique Tools (Keep All)

Tools with no duplicate are listed under `unique` — Claude always sees these:

```yaml
unique:
  - jira/get_sprint_board     # no equivalent in GitHub/Linear
  - notion/query_database     # no equivalent in any other connected server
  - slack/list_channels       # no equivalent
```

---

## PHASE 6 — VALIDATION

Before finalising the routing config:

1. **Coverage check** — every canonical operation that has at least one tool in the
   inventory must have a `default` routing rule. Flag any gaps.
2. **Orphan check** — every tool in the inventory must appear in exactly one of:
   `routing.default`, `routing.overrides`, `suppressed`, or `unique`. No tool should
   be unclassified.
3. **Circular routing check** — no override condition should route back to the same
   tool that the default already selects.
4. **Schema compatibility check** — if two tools are marked as functional equivalents
   but their required parameters differ materially, add a parameter mapping note:

```yaml
pr.create:
  default: github/create_pull_request
  # github requires: head, base, title
  # gitlab requires: source_branch, target_branch, title
  # Parameter mapping: head → source_branch, base → target_branch
```

---

## STATS OUTPUT

`/stats` format:

```
MCP DEDUPLICATION SUMMARY
────────────────────────────────────────────────────────────
  Servers scanned        : 4  (github, gitlab, jira, linear)
  Total tools found      : 87
  Exact duplicates       : 14  (suppressed)
  Functional equivalents : 9   (demoted to overrides)
  Near-duplicates        : 6   (routing rules added)
  Unique tools           : 58  (always available)
  ────────────────────────────────────────────────────────
  Tool reduction         : 26%  (87 → 64 canonical + unique)
  Canonical operations   : 31
  Routing rules generated: 14
  ────────────────────────────────────────────────────────
  Token savings estimate : ~340 tokens/turn
  (Based on: 23 suppressed tools × ~15 tokens/tool description)
────────────────────────────────────────────────────────────
```

---

## BUILT-IN SERVER REGISTRY

Known tool lists for common MCP servers. Used when the user cannot paste a manifest.

| Server | Known tool count | Primary categories |
| --- | --- | --- |
| `github` (official) | 47 | repo, pr, issue, user, search, release |
| `gitlab` | 38 | repo, pr (MR), issue, user, search |
| `jira` | 21 | issue, sprint, project, board |
| `linear` | 18 | issue, project, team, cycle |
| `notion` | 14 | doc, database, page, block |
| `slack` | 12 | message, channel, user |
| `confluence` | 10 | doc, space, page |
| `asana` | 16 | task, project, team |
| `trello` | 12 | card, board, list |
| `google-drive` | 8 | doc, file, permission |

---

## COMMON DUPLICATE PATTERNS

Documented across the most common server combinations:

### GitHub + GitLab

| GitHub tool | GitLab tool | Category | Similarity |
| --- | --- | --- | --- |
| `create_pull_request` | `create_merge_request` | `pr.create` | Functional equivalent |
| `list_pull_requests` | `list_merge_requests` | `pr.list` | Functional equivalent |
| `merge_pull_request` | `merge_merge_request` | `pr.merge` | Exact duplicate |
| `create_issue` | `create_issue` | `issue.create` | Near-identical |
| `get_file_contents` | `get_file` | `repo.file` | Functional equivalent |
| `search_code` | `search_code` | `search.code` | Near-identical |

### GitHub + Jira

| GitHub tool | Jira tool | Category | Similarity |
| --- | --- | --- | --- |
| `create_issue` | `create_ticket` | `issue.create` | Functional equivalent |
| `list_issues` | `search_issues` | `issue.list` | Near-duplicate |
| `add_issue_comment` | `add_comment` | `issue.comment` | Functional equivalent |
| `close_issue` (label) | `resolve_ticket` | `issue.close` | Near-duplicate |

### GitHub + Linear

| GitHub tool | Linear tool | Category | Similarity |
| --- | --- | --- | --- |
| `create_issue` | `createIssue` | `issue.create` | Exact duplicate |
| `list_issues` | `getIssues` | `issue.list` | Exact duplicate |
| `update_issue` | `updateIssue` | `issue.update` | Exact duplicate |

---

## BEHAVIOUR RULES

- **Never suppress a unique capability.** A tool with no semantic equivalent is always
  kept, regardless of how many total tools are visible.
- **Server priority is authoritative.** If the user declares a primary server,
  canonical selection always defers to that server unless its tool is strictly inferior
  (missing required parameters).
- **Routing rules must be conditioned.** Never create a routing rule that fires on
  every query — every rule needs a distinguishing condition.
- **Parameter incompatibility blocks suppression.** If two tools are semantically
  equivalent but require different parameters, they are near-duplicates, not exact
  duplicates — keep both with a parameter mapping note.
- **Always show the reduction number.** Every scan must report total tools before and
  after deduplication so the user can see the concrete benefit.
- **Validate before generating config.** The Phase 6 checks are not optional — a
  config with unclassified tools or missing routing rules is incomplete.
- **Flag schema breaks.** If a canonical tool's required parameters change between
  servers, document the mapping explicitly in the routing config comment.

---

## EXAMPLES

### Example: `/scan` with GitHub + GitLab + Jira

```
Scanned: github (47 tools) · gitlab (38 tools) · jira (21 tools)
Total: 106 tools

Exact duplicates found      : 8
Functional equivalents found: 11
Near-duplicates found       : 7
Unique tools                : 80

Top 5 duplicate groups:
  issue.create   → github/create_issue [canonical], gitlab/create_issue [demoted],
                   jira/create_ticket [override on Jira ID pattern]
  issue.comment  → github/add_issue_comment [canonical],
                   gitlab/add_comment [suppressed], jira/add_comment [suppressed]
  pr.create      → github/create_pull_request [canonical],
                   gitlab/create_merge_request [override on "merge request" / "MR"]
  search.code    → github/search_code [canonical], gitlab/search_code [suppressed]
  repo.file      → github/get_file_contents [canonical], gitlab/get_file [suppressed]

Run /config to generate .mcp-dedup.yml  ·  Run /matrix to see the full table.
```

### Example: `/route` output

> User: `/route create a task for the login bug and assign it to @maya`

```
ROUTE RECOMMENDATION
Query intent  : issue.create
Assignee hint : @maya (user lookup needed)
Platform hint : none detected

Recommended tool: github/create_issue
  Reason: github is the declared primary server for issue management.
  Params:  title="Login bug fix", body="…", assignees=["maya"]

Alternative (if user says "Jira" or provides a project key):
  jira/create_ticket
  Params:  summary="Login bug fix", description="…", assignee="maya"
```

### Example: `/matrix` excerpt

```
DEDUPLICATION MATRIX
                     github   gitlab   jira   linear
─────────────────────────────────────────────────────
issue.create           ●        ○        ↑       ✕
issue.comment          ●        ✕        ✕       –
pr.create              ●        ↑        –       –
pr.merge               ●        ✕        –       –
repo.file              ●        ✕        –       –
search.code            ●        ✕        –       –
sprint.board           –        –        ●       –
message.send           –        –        –       –

●  canonical  ○  demoted  ↑  override  ✕  suppressed  –  not available
```

---

## VERIFICATION AND ITERATION LOOP

After `/config` generates the routing config, do not stop. Automatically run `/verify`:

**`/verify` protocol:**

Run these 5 simulation queries through the generated config and show which tool each resolves to:

1. "Create a new issue about the login bug" → should resolve to `issue.create` canonical
2. "Comment on issue #42" → should resolve to `issue.comment` canonical
3. "Open a pull request for the auth branch" → should resolve to `pr.create` canonical
4. "Search the codebase for 'session timeout'" → should resolve to `search.code` canonical
5. "Get the contents of src/auth.ts" → should resolve to `repo.file` canonical

If any simulation resolves to a suppressed or wrong tool, flag it:

```
VERIFY RESULT
  ✓ issue.create  → github/create_issue
  ✓ issue.comment → github/add_issue_comment
  ✗ pr.create     → gitlab/create_merge_request  (WRONG — should be github/create_pull_request)
    Fix: add trigger "pull request" to github entry; current rule matches "merge request" first

  3/5 routing rules verified. 1 fix required before config is safe to deploy.
  Run /config after fixing to regenerate.
```

**Iteration after fix:**
1. User corrects the routing rule or server priority.
2. Re-run `/config` → `/verify`.
3. Repeat until all 5 simulations pass.
4. Then run `/stats` to confirm the final reduction number.

**Reduction goal:** A healthy deduplication should reduce exposed tools by ≥40%. If reduction is <40%, the server priority list is likely incomplete — ask the user to confirm their primary server for each category.
