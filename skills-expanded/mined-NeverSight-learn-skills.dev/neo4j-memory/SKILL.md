---
name: neo4j-memory
description: Use this skill when the user asks to "record memories", "save this session", "record prior sessions", "remember decisions", "save to neo4j", "update memory graph", or any similar request to persist session history, decisions, actions, or learnings into the Neo4j memory MCP server. Also use when starting a new project and the user wants to set up memory tracking.
version: 1.0.0
---

# Neo4j Memory Skill

Persist Claude session history, decisions, actions, learnings, and artifacts into a Neo4j graph database via the `memory` MCP server. This creates a queryable knowledge graph that future sessions can interrogate.

## Execution Backend

Choose between two backends. Use MCP if available; otherwise fall back to Python.

### Detection

At the start of any session that will use this skill, check whether the MCP tools are available:
- If `mcp__memory__read-cypher` is listed as an available tool, **use MCP** (Tier 1).
- If it is not listed or returns a tool-not-found error, **use Python** (Tier 2).

### Tier 1 — MCP Server (preferred)

All writes use `mcp__memory__write-cypher`. All reads use `mcp__memory__read-cypher`.
Each tool call must contain exactly **one Cypher statement** (the server rejects multi-statement batches).
Use `WITH` to chain clauses within a single query where needed.

### Tier 2 — Python Fallback

See the **Python Fallback** sections below for credential setup and execution templates.
The same single-statement constraint applies — one Cypher statement per Python execution.

## Data Model

```
(:Project    {id, name, folder, description, startDate, activeDashboard?})
(:Session    {id, title, date, startTime?, summary, duration?, resumeId?})  // date: YYYY-MM-DD; startTime: ISO 8601 e.g. "2026-03-19T08:12:28"; duration in minutes; resumeId is the Claude Code session ID for --resume
(:Decision   {id, title, rationale, applies_to})
(:Action     {id, type, description})
(:Artifact   {id, path, type, description})
(:Learning   {id, topic, insight, source})
(:Problem    {id, description, symptom})
(:Solution   {id, description, status, notes?})  // status: proposed | accepted | implemented | rejected
(:Technology   {id, name, category?, description?})
(:WebResource  {id, url, title?, type, description?})  // type: docs | dashboard | api | issue | reference | service | repository

(Project)-[:HAS_SESSION]->(Session)
(Project)-[:FIRST_SESSION]->(Session)      // first session only
(Project)-[:LAST_SESSION]->(Session)       // most recent session; moves with each new session
(Project)-[:USES_TECHNOLOGY]->(Technology) // optional; multiple allowed
(Project)-[:HAS_REMOTE {name}]->(WebResource {type: 'repository'}) // git remote name e.g. 'origin', 'upstream'
(Session)-[:NEXT_SESSION]->(Session)       // chronological chain; last session has no outgoing NEXT_SESSION
(Session)-[:CONTAINS]->(Decision|Action|Learning|Problem)
(Session)-[:ACCESSED {purpose?}]->(WebResource)        // any URL visited; purpose: read-docs | test | screenshot | debug | reference
(Decision)-[:RESULTED_IN]->(Action)
(Learning)-[:INFORMED]->(Decision)
(Learning)-[:SOURCED_FROM]->(WebResource)  // learning was derived from reading this URL
(Action)-[:CREATED|MODIFIED]->(Artifact)
(Action)-[:FIXED]->(Problem)
(Action)-[:ACCESSED]->(WebResource)        // action involved opening/testing this URL (e.g. screenshot, dashboard test)
(Artifact)-[:ACCESSIBLE_AT]->(WebResource) // artifact (dashboard, web app) is live/viewable at this URL
(Problem)-[:HAS_SOLUTION]->(Solution)      // zero or more solutions per problem
(Problem)-[:REFERENCED_AT]->(WebResource)  // external issue, error page, or doc relevant to the problem
(Solution)-[:IMPLEMENTED_BY]->(Action)     // action(s) that implemented the solution; optional
(Decision)-[:ACCEPTS]->(Solution)          // decision to go with this solution
(Decision)-[:REJECTS]->(Solution)          // decision to reject this solution
(Learning)-[:USES_TECHNOLOGY]->(Technology) // optional; tags a learning to a technology
(Artifact)-[:USES_TECHNOLOGY]->(Technology) // optional; tags an artifact to a technology
(Problem)-[:USES_TECHNOLOGY]->(Technology)  // optional; tags a problem to a technology
```

### Node ID conventions

| Type | Pattern | Example |
|------|---------|---------|
| Project | `project-<slug>` | `project-kyc` |
| Session | GUID (generated via `randomUUID()`) | `a3f2c1d4-...` |
| Decision | `dec-<slug>` | `dec-filter-widget` |
| Action | `action-<slug>` | `action-create-impl-md` |
| Artifact | `file-<slug>` | `file-implementation-md` |
| Learning | `learn-<slug>` | `learn-map-requires-point` |
| Problem | `prob-<slug>` | `prob-risk-flags-wrong` |
| Solution | `sol-<slug>` | `sol-quantified-path-fix` |
| Technology | `tech-<slug>` | `tech-python`, `tech-neo4j` |
| WebResource | `web-<slug>` | `web-neo4j-cypher-docs`, `web-aura-console`, `web-github-my-repo` |

### Session ownership rules

- Each Session belongs to **exactly one Project** via `HAS_SESSION`. Never create a second `HAS_SESSION` link from a different project to an existing session.
- Sessions **never move between projects** unless the user explicitly requests a correction (e.g. "that session is in the wrong project").
- When recording a new session, always derive the owning project from the current working directory (`cwd`). Do not reuse or re-link sessions across projects.
- If you detect that a session already has a `HAS_SESSION` relationship to a project, do not create another one — abort and alert the user instead.

### One Claude session = one graph Session (with exceptions)

By default, one Claude conversation maps to exactly one `Session` node. Do not create multiple session nodes for the same conversation.

**Exception 1 — User explicitly starts a new session:** Save/update the current session node with everything accumulated so far, note the current time as the new session start, then treat all subsequent work as a new session (new GUID, new node, new `NEXT_SESSION` link).

**Exception 2 — Context shift detected:** If the conversation shifts to what appears to be a distinct new task or project phase, you may *suggest* splitting into a new session: _"This feels like a new session — want me to close the current one and start fresh?"_ Only proceed if the user agrees. If the user declines, continue accumulating into the current session.

**Session start time:** When a new session begins (including after an explicit split), note the wall-clock time so `duration` can be computed correctly when the session is saved.

### Action types

`CREATE_FILE`, `MODIFY_FILE`, `ADD_PAGE`, `ADD_WIDGET`, `MODIFY_WIDGET`, `FIX_BUG`, `ADD_FEATURE`, `REFACTOR`, `SETUP_DATABASE`, `WRITE_QUERY`

---

## Workflow 1 — Set up a new project

1. Check if a Project node already exists:
   ```cypher
   MATCH (p:Project {folder: '<cwd>'}) RETURN p
   ```
2. If not, create it. The project `name` is the last segment of the folder path (e.g. folder `/Users/jstegeman/Projects/aisetup` → name `aisetup`):
   ```cypher
   MERGE (p:Project {id: 'project-<slug>'})
   SET p.name = '<last-folder-segment>',
       p.folder = '<absolute-path>',
       p.description = '<one sentence>',
       p.startDate = '<YYYY-MM-DD>'
   RETURN p
   ```
3. Check for git remotes and create `HAS_REMOTE` links if any exist:
   ```bash
   # jj repo:
   jj --repository '<cwd>' git remote list
   # plain git repo:
   git -C '<cwd>' remote -v
   ```
   For each remote URL, strip the trailing `.git` if present, then:
   ```cypher
   MERGE (w:WebResource {id: 'web-<slug>'})
   SET w.url = '<remote-url>', w.title = '<owner/repo>', w.type = 'repository'
   ```
   ```cypher
   MATCH (p:Project {folder: '<cwd>'}), (w:WebResource {id: 'web-<slug>'})
   MERGE (p)-[:HAS_REMOTE {name: '<remote-name>'}]->(w)
   ```

4. Create constraints once per database (skip if already done):
   ```cypher
   CREATE CONSTRAINT project_id IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE
   ```
   Repeat for Session, Decision, Action, Artifact, Learning, Problem, Solution, Technology, WebResource.

---

## Workflow 2 — Record prior sessions from existing files

Use this when the user asks to load history from an existing project into Neo4j.

**Step 1 — Read source files.** Look for: `CONVERSATION.md`, `implementation.md`, `dashboards.md`, any `*.md` files, git log, or any document that records what was done and why.

**Step 2 — Extract entities.** For each session identify:
- **Sessions**: discrete units of work (date, goal, outcome)
- **Decisions**: choices made with a stated or inferable rationale
- **Actions**: concrete things done (files created/modified, widgets added, bugs fixed)
- **Artifacts**: files or other outputs that now exist on disk
- **Learnings**: technical insights, gotchas, surprising discoveries
- **Problems**: bugs or blockers that were encountered

**Step 3 — Write in order.** Always write in this sequence to satisfy foreign key-like constraints:
1. Constraints (once)
2. Project node
3. Session nodes + NEXT_SESSION chain
4. Decision, Action, Artifact, Learning, Problem nodes
5. Relationships (CONTAINS, RESULTED_IN, INFORMED, CREATED, FIXED, etc.)

**Step 4 — Connect to Project.**
```cypher
MATCH (proj:Project {id: 'project-<slug>'}), (s:Session)
MERGE (proj)-[:HAS_SESSION]->(s)
```

Connect `FIRST_SESSION` to the earliest session and `LAST_SESSION` to the most recent:
```cypher
MATCH (proj:Project {id: 'project-<slug>'})-[:HAS_SESSION]->(s:Session)
WITH proj, s ORDER BY s.date ASC
WITH proj, collect(s) AS sessions
MERGE (proj)-[:FIRST_SESSION]->(sessions[0])
MERGE (proj)-[:LAST_SESSION]->(sessions[-1])
```

Build the `NEXT_SESSION` chain in chronological order:
```cypher
MATCH (proj:Project {id: 'project-<slug>'})-[:HAS_SESSION]->(s:Session)
WITH s ORDER BY s.date ASC
WITH collect(s) AS sessions
UNWIND range(0, size(sessions)-2) AS i
WITH sessions[i] AS curr, sessions[i+1] AS next
MERGE (curr)-[:NEXT_SESSION]->(next)
```

---

## Workflow 3 — Record a new session (on request)

At the end of a session, or when the user asks to save, do the following.

**Step 1 — Find the current last session (for chaining).**
```cypher
MATCH (proj:Project {folder: '<cwd>'})-[:LAST_SESSION]->(s:Session)
RETURN s.id AS prevId
```
Note the returned `prevId` — you will need it in Step 4. If no result, this will be the first session for this project.

**Step 2 — Compute session duration and get resumeId.**

The `SessionStart` hook writes one file per session to `~/.claude/session_starts/`, named by the Claude Code process PID, containing JSON with `session_id`, `start_time`, and `cwd`. Read it using `$PPID` (which matches the hook's parent PID):

```bash
session_file=~/.claude/session_starts/$PPID.json
if [ -f "$session_file" ]; then
  data=$(cat "$session_file")
  ts=$(echo "$data" | jq -r '.start_time')
  echo "resume_id=$(echo "$data" | jq -r '.session_id')"
  echo "start_time=$(date -r "$ts" +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -d "@$ts" +%Y-%m-%dT%H:%M:%S)"
  echo "duration=$(( ($(date +%s) - ts) / 60 ))"
else
  # Fallback for legacy .txt files (older sessions, no resumeId or startTime available)
  cwd=$(pwd) && for f in ~/.claude/session_starts/*.txt; do read ts dir < "$f"; [ "$dir" = "$cwd" ] && echo "duration=$(( ($(date +%s) - ts) / 60 ))" && break; done
fi
```

Capture `resume_id` and `duration` from the output. If neither file is found, omit both.

**Step 3 — Create the session node with a GUID.**
```cypher
CREATE (s:Session {id: randomUUID()})
SET s.title = '<concise title>',
    s.date = '<YYYY-MM-DD>',
    s.startTime = '<ISO 8601 start_time from step 2, or omit if not available>',
    s.summary = '<2-4 sentence summary of what was done and why>',
    s.duration = <minutes from step 2, or omit if unknown>,
    s.resumeId = '<resume_id from step 2, or omit if not available>'
RETURN s.id
```
**Capture the returned `id`** — you will need it for all subsequent steps. Refer to it as `<new-session-id>` below.

**Step 4 — Link to project and update session pointers.**

Create `HAS_SESSION`:
```cypher
MATCH (proj:Project {folder: '<cwd>'}), (s:Session {id: '<new-session-id>'})
MERGE (proj)-[:HAS_SESSION]->(s)
```

If this is the first session for the project, set `FIRST_SESSION`:
```cypher
MATCH (proj:Project {folder: '<cwd>'}), (s:Session {id: '<new-session-id>'})
WHERE NOT (proj)-[:FIRST_SESSION]->()
MERGE (proj)-[:FIRST_SESSION]->(s)
```

If a previous session was found in Step 1, chain it with `NEXT_SESSION` and rotate `LAST_SESSION` to the new session:
```cypher
MATCH (proj:Project {folder: '<cwd>'})-[last:LAST_SESSION]->(prev:Session {id: '<prevId>'}),
      (curr:Session {id: '<new-session-id>'})
DELETE last
MERGE (prev)-[:NEXT_SESSION]->(curr)
MERGE (proj)-[:LAST_SESSION]->(curr)
```

If this is the first session (no previous), set `LAST_SESSION` directly:
```cypher
MATCH (proj:Project {folder: '<cwd>'}), (s:Session {id: '<new-session-id>'})
WHERE NOT (proj)-[:LAST_SESSION]->()
MERGE (proj)-[:LAST_SESSION]->(s)
```

**Step 5 — Create and link this session's entities** (decisions, actions, learnings, problems, artifacts, solutions) following the patterns in Workflow 2 Step 3 and Workflow 6 below. Use `<new-session-id>` wherever session id is required.

When recording problems, also capture any solutions that were proposed, accepted, rejected, or implemented during the session — see Workflow 6.

---

## Workflow 4 — Record a specific memory (on request)

When the user says "remember this decision", "note this learning", etc., create the appropriate node and attach it to the current session.

Example — recording a learning:
```cypher
MERGE (l:Learning {id: 'learn-<slug>'})
SET l.topic = '<topic>',
    l.insight = '<what was learned>',
    l.source = '<how it was discovered>'
```
```cypher
MATCH (s:Session {id: '<session-guid>'}), (l:Learning {id: 'learn-<slug>'})
MERGE (s)-[:CONTAINS]->(l)
```

---

## Workflow 5 — Record solutions

Use this workflow whenever a Problem has a proposed, accepted, rejected, or implemented solution.

**Status values:**
- `proposed` — suggested but not yet accepted, rejected, or implemented
- `accepted` — the human agreed to the solution but it has not been implemented yet
- `implemented` — work was done to implement it (always link to the implementing Action via `IMPLEMENTED_BY`)
- `rejected` — explicitly not going ahead with this solution

**Step 1 — Create the Solution node.**
```cypher
MERGE (sol:Solution {id: 'sol-<slug>'})
SET sol.description = '<what the solution does>',
    sol.status = '<proposed|accepted|implemented|rejected>',
    sol.notes = '<optional — why this approach, caveats, etc.>'
RETURN sol.id
```

**Step 2 — Link the Solution to its Problem.**
```cypher
MATCH (prob:Problem {id: 'prob-<slug>'}), (sol:Solution {id: 'sol-<slug>'})
MERGE (prob)-[:HAS_SOLUTION]->(sol)
```

**Step 3 — If implemented, link to the Action that implemented it.**
```cypher
MATCH (sol:Solution {id: 'sol-<slug>'}), (a:Action {id: 'action-<slug>'})
MERGE (sol)-[:IMPLEMENTED_BY]->(a)
```

**Step 4 — If a Decision was made about the solution, link it.**

When a decision was made to go with the solution:
```cypher
MATCH (dec:Decision {id: 'dec-<slug>'}), (sol:Solution {id: 'sol-<slug>'})
MERGE (dec)-[:ACCEPTS]->(sol)
```

When a decision was made to reject the solution:
```cypher
MATCH (dec:Decision {id: 'dec-<slug>'}), (sol:Solution {id: 'sol-<slug>'})
MERGE (dec)-[:REJECTS]->(sol)
```

**Step 5 — Update status if it changes.**

If a `proposed` solution later becomes `accepted` or `implemented` in a subsequent session:
```cypher
MATCH (sol:Solution {id: 'sol-<slug>'})
SET sol.status = 'implemented'
```

**Rules:**
- A Problem can have multiple Solutions (e.g. one rejected and one accepted).
- A single Action can implement multiple Solutions (use `MERGE` to avoid duplicates).
- Always update `status` when the outcome changes — do not leave stale `proposed` nodes after implementation.
- Solutions are not `CONTAINS`-linked to Sessions. They belong to Problems, not sessions. Session context is recoverable via `Session -[:CONTAINS]-> Problem -[:HAS_SOLUTION]-> Solution`.

---

## Workflow 6 — Manage project technologies

Technologies are **shared global nodes** — a single `(:Technology {name: 'Python'})` node is reused across all projects. Never create duplicates.

**Step 1 — Check what Technology nodes already exist.**
```cypher
MATCH (t:Technology) RETURN t.id, t.name, t.category ORDER BY t.name
```

**Step 2 — Identify technologies to associate with the project.**
Based on what you know about the project (from files, conversation, etc.), propose a list of technologies to the user. **Always confirm with the user before proceeding** — do not create new Technology nodes or link existing ones without explicit approval.

Present a summary like:
> "I'd like to record the following technologies for this project:
> - **Python** (already exists in the graph) — link to this project?
> - **FastAPI** (new node needed) — create and link?
>
> Please confirm which to add."

**Step 3 — Create any new Technology nodes (only after user confirms).**
```cypher
MERGE (t:Technology {id: 'tech-<slug>'})
SET t.name = '<name>',
    t.category = '<category>',
    t.description = '<optional one-line description>'
RETURN t
```

Suggested `category` values: `language`, `framework`, `database`, `tool`, `platform`, `library`, `infrastructure`.

**Step 4 — Link technologies to the project (only after user confirms each).**
```cypher
MATCH (p:Project {folder: '<cwd>'}), (t:Technology {id: 'tech-<slug>'})
MERGE (p)-[:USES_TECHNOLOGY]->(t)
```

**Step 6 — Optionally tag individual Learnings, Artifacts, and Problems to technologies.**

When recording these entities, consider whether they are specifically about one or more technologies. If so, link them after creating the node:

```cypher
MATCH (l:Learning {id: 'learn-<slug>'}), (t:Technology {id: 'tech-<slug>'})
MERGE (l)-[:USES_TECHNOLOGY]->(t)
```
```cypher
MATCH (art:Artifact {id: 'file-<slug>'}), (t:Technology {id: 'tech-<slug>'})
MERGE (art)-[:USES_TECHNOLOGY]->(t)
```
```cypher
MATCH (prob:Problem {id: 'prob-<slug>'}), (t:Technology {id: 'tech-<slug>'})
MERGE (prob)-[:USES_TECHNOLOGY]->(t)
```

Use your judgement — only tag when the association is meaningful. The test is: **is this learning/artifact/problem fundamentally *about* the technology?** Not merely "was the technology involved when this happened?"

Examples of correct tagging:
- A learning about a Cypher ORDER BY aggregation bug → tag Cypher ✓
- A learning about a NeoDash widget JSON format → tag NeoDash ✓
- A learning about wrong relationship names in the project's data model (discovered via a Cypher query) → do NOT tag Cypher ✗
- A learning about missing nodes in the graph schema → do NOT tag Neo4j ✗
- A learning about Claude Code not exposing a session env var (noticed while working on a Neo4j project) → do NOT tag Neo4j ✗
- A learning about cmux browser pane management (noticed during a Neo4j Aura session) → do NOT tag Neo4j Aura ✗

Do not tag every node to every technology the project uses.

**Rules:**
- Always query existing Technology nodes first — never assume a node doesn't exist.
- Use the canonical, well-known name for the technology (e.g. `Python`, `Neo4j`, `React`, `PostgreSQL`).
- Technology nodes are **optional** — a project does not need any.
- A project can have **multiple** Technology relationships.
- **Never create a new Technology node without user confirmation.**
- **Never link an existing Technology to a project without user confirmation.**

---

## Workflow 7 — Record web resources

Use this workflow when a URL was accessed during a session — for reading docs, testing a live URL, taking screenshots, referencing an issue, etc.

`WebResource` is a **shared global node** — like `Technology`, the same URL reuses a single node across all projects and sessions. Always check for an existing node before creating one.

**Step 1 — Check if the WebResource already exists.**
```cypher
MATCH (w:WebResource {url: '<url>'}) RETURN w
```

**Step 2 — Create if new.**
```cypher
MERGE (w:WebResource {id: 'web-<slug>'})
SET w.url = '<url>',
    w.title = '<page title or short label>',
    w.type = '<docs|dashboard|api|issue|reference|service>',
    w.description = '<optional one-line description>'
RETURN w
```

**Step 3 — Link to the session (general access).**
```cypher
MATCH (s:Session {id: '<session-id>'}), (w:WebResource {id: 'web-<slug>'})
MERGE (s)-[:ACCESSED {purpose: '<read-docs|test|screenshot|debug|reference>'}]->(w)
```

**Step 4 — Add more specific links as appropriate.**

If a Learning was derived from reading the URL:
```cypher
MATCH (l:Learning {id: 'learn-<slug>'}), (w:WebResource {id: 'web-<slug>'})
MERGE (l)-[:SOURCED_FROM]->(w)
```

If an Action involved opening/testing the URL (e.g. took a screenshot, tested a dashboard):
```cypher
MATCH (a:Action {id: 'action-<slug>'}), (w:WebResource {id: 'web-<slug>'})
MERGE (a)-[:ACCESSED]->(w)
```

If an Artifact (dashboard, web app) is live/viewable at the URL:
```cypher
MATCH (art:Artifact {id: 'file-<slug>'}), (w:WebResource {id: 'web-<slug>'})
MERGE (art)-[:ACCESSIBLE_AT]->(w)
```

If the URL is relevant to a Problem (GitHub issue, error page, relevant docs):
```cypher
MATCH (prob:Problem {id: 'prob-<slug>'}), (w:WebResource {id: 'web-<slug>'})
MERGE (prob)-[:REFERENCED_AT]->(w)
```

**Rules:**
- Always query for an existing `WebResource` by URL before creating a new node.
- Record `SOURCED_FROM`, `ACCESSIBLE_AT`, and `REFERENCED_AT` links in addition to (or instead of) the session-level `ACCESSED` link whenever the more specific relationship applies.
- `ACCESSED` on a Session is for general access; prefer the specific relationships where they fit.
- Use `purpose` on `ACCESSED` to capture why the URL was opened.

---

## Querying memory in future sessions

To get oriented at the start of a session:

```cypher
// What project is this?
MATCH (p:Project {folder: '<cwd>'}) RETURN p

// What sessions exist?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->(s:Session)
RETURN s.id, s.title, s.date, s.summary ORDER BY s.date

// What did we learn?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->(s)-[:CONTAINS]->(l:Learning)
RETURN l.topic, l.insight ORDER BY l.topic

// What files exist?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->()-[:CONTAINS]->(a:Action)-[:CREATED]->(art:Artifact)
RETURN art.path, art.description

// What decisions were made and why?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->()-[:CONTAINS]->(d:Decision)
RETURN d.title, d.rationale ORDER BY d.title

// What technologies does this project use?
MATCH (p:Project {folder: '<cwd>'})-[:USES_TECHNOLOGY]->(t:Technology)
RETURN t.name, t.category, t.description ORDER BY t.name

// Which projects use a given technology?
MATCH (p:Project)-[:USES_TECHNOLOGY]->(t:Technology {name: '<name>'})
RETURN p.name, p.folder

// What learnings are tagged to a given technology (across all projects)?
MATCH (l:Learning)-[:USES_TECHNOLOGY]->(t:Technology {name: '<name>'})
MATCH (s:Session)-[:CONTAINS]->(l)
MATCH (p:Project)-[:HAS_SESSION]->(s)
RETURN l.topic, l.insight, p.name AS project ORDER BY p.name, l.topic

// What artifacts are tagged to a given technology (across all projects)?
MATCH (art:Artifact)-[:USES_TECHNOLOGY]->(t:Technology {name: '<name>'})
MATCH (a:Action)-[:CREATED|MODIFIED]->(art)
MATCH (s:Session)-[:CONTAINS]->(a)
MATCH (p:Project)-[:HAS_SESSION]->(s)
RETURN art.path, art.description, p.name AS project ORDER BY p.name, art.path

// What problems are tagged to a given technology (across all projects)?
MATCH (prob:Problem)-[:USES_TECHNOLOGY]->(t:Technology {name: '<name>'})
MATCH (s:Session)-[:CONTAINS]->(prob)
MATCH (p:Project)-[:HAS_SESSION]->(s)
RETURN prob.description, prob.symptom, p.name AS project ORDER BY p.name

// What open problems exist (no implemented solution) across all projects?
MATCH (p:Project)-[:HAS_SESSION]->(s:Session)-[:CONTAINS]->(prob:Problem)
WHERE NOT (prob)-[:HAS_SOLUTION]->(:Solution {status: 'implemented'})
OPTIONAL MATCH (prob)-[:HAS_SOLUTION]->(sol:Solution)
RETURN p.name AS project, prob.description AS problem, collect(sol.status + ': ' + sol.description) AS solutions
ORDER BY p.name

// What solutions exist for a given problem?
MATCH (prob:Problem {id: 'prob-<slug>'})-[:HAS_SOLUTION]->(sol:Solution)
OPTIONAL MATCH (sol)-[:IMPLEMENTED_BY]->(a:Action)
OPTIONAL MATCH (dec:Decision)-[:ACCEPTS|REJECTS]->(sol)
RETURN sol.id, sol.status, sol.description, a.description AS implemented_by, type(dec) + ': ' + dec.title AS decision

// What proposed solutions are waiting to be implemented?
MATCH (p:Project)-[:HAS_SESSION]->(s:Session)-[:CONTAINS]->(prob:Problem)-[:HAS_SOLUTION]->(sol:Solution {status: 'proposed'})
RETURN p.name AS project, prob.description AS problem, sol.description AS proposed_solution ORDER BY p.name

// Which decisions led to rejected solutions (and why were they rejected)?
MATCH (dec:Decision)-[:REJECTS]->(sol:Solution)<-[:HAS_SOLUTION]-(prob:Problem)
RETURN prob.description AS problem, sol.description AS rejected_solution, dec.title AS decision, dec.rationale AS rationale

// What git remotes does this project have?
MATCH (p:Project {folder: '<cwd>'})-[r:HAS_REMOTE]->(w:WebResource)
RETURN r.name AS remote, w.url

// Which projects have GitHub remotes?
MATCH (p:Project)-[r:HAS_REMOTE]->(w:WebResource {type: 'repository'})
RETURN p.name, p.folder, r.name AS remote, w.url ORDER BY p.name

// What URLs were accessed during this project (and why)?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->(s:Session)-[a:ACCESSED]->(w:WebResource)
RETURN w.url, w.title, w.type, a.purpose, s.date ORDER BY s.date, w.type

// What learnings came from reading a specific URL?
MATCH (l:Learning)-[:SOURCED_FROM]->(w:WebResource {url: '<url>'})
RETURN l.topic, l.insight

// What learnings across all projects were sourced from docs?
MATCH (l:Learning)-[:SOURCED_FROM]->(w:WebResource {type: 'docs'})
MATCH (s:Session)-[:CONTAINS]->(l)
MATCH (p:Project)-[:HAS_SESSION]->(s)
RETURN l.topic, l.insight, w.url, p.name AS project ORDER BY p.name, l.topic

// Where are this project's artifacts accessible (deployed URLs)?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->()-[:CONTAINS]->(a:Action)-[:CREATED|MODIFIED]->(art:Artifact)-[:ACCESSIBLE_AT]->(w:WebResource)
RETURN art.path, art.description, w.url

// What external resources are referenced by open problems?
MATCH (p:Project {folder: '<cwd>'})-[:HAS_SESSION]->(s:Session)-[:CONTAINS]->(prob:Problem)-[:REFERENCED_AT]->(w:WebResource)
WHERE NOT (prob)-[:HAS_SOLUTION]->(:Solution {status: 'implemented'})
RETURN prob.description, w.url, w.type ORDER BY prob.description
```

---

## Python Fallback — Credential Setup

When the Python backend is first needed, check for a credentials file at `~/.claude/neo4j-credentials.json`.

**If the file does not exist**, ask the user for the following and then write the file:
- **URI** — e.g. `bolt://localhost:7687` or `neo4j+s://xxxxx.databases.neo4j.io`
- **Username** — typically `neo4j`
- **Password**
- **Database name** — default is `neo4j`

Write the file with the Write tool:
```json
{
  "uri": "bolt://localhost:7687",
  "username": "neo4j",
  "password": "your-password",
  "database": "neo4j"
}
```

Remind the user: `~/.claude/neo4j-credentials.json` contains plaintext credentials. Do not commit or share this file.

---

## Python Fallback — Virtual Environment

The `neo4j` driver requires a virtual environment at `~/.claude/claude-memory`.

**First-time setup** (if the venv does not exist):

If `uv` is available (preferred):
```bash
uv venv ~/.claude/claude-memory
uv pip install neo4j --python ~/.claude/claude-memory/bin/python
```

Otherwise, use standard Python tooling:
```bash
python3 -m venv ~/.claude/claude-memory
~/.claude/claude-memory/bin/pip install neo4j
```

---

## Python Fallback — Execution

Use this template for every Cypher statement when MCP is unavailable. Always invoke the venv's Python binary directly (`~/.claude/claude-memory/bin/python`) — do not activate the venv.

```python
import json
from pathlib import Path
from neo4j import GraphDatabase

creds_path = Path.home() / ".claude" / "neo4j-credentials.json"
creds = json.loads(creds_path.read_text())
driver = GraphDatabase.driver(creds["uri"], auth=(creds["username"], creds["password"]))
with driver.session(database=creds["database"]) as session:
    result = session.run("""
<CYPHER STATEMENT HERE>
""")
    print([dict(r) for r in result])
driver.close()
```

Invoke as:
```bash
~/.claude/claude-memory/bin/python << 'EOF'
<paste the filled-in template>
EOF
```

Rules:
- Unlike MCP, **Python can run multiple Cypher statements in one script** — batch an entire workflow into a single Bash tool call to minimise round trips.
- Use a heredoc (`<< 'EOF'`) rather than `-c` to safely handle multi-line Cypher and quotes.
- Parse and display the printed results at the end of the script.

---

## Tips

- Use `MERGE` (not `CREATE`) for all nodes and relationships — safe to re-run.
- Keep `summary` and `insight` fields concise but self-contained — they will be read without surrounding context in future sessions.
- Prefer recording the *why* over the *what* for decisions and learnings; the *what* is usually recoverable from files.
- Always include `source` on Learning nodes — knowing *how* something was discovered helps judge its reliability.
- If the `memory` MCP server is not available, automatically fall back to the Python backend. Only surface this to the user if credential setup is needed.
