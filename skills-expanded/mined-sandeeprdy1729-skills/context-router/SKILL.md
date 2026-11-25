---
name: context-router
description: >
  Meta-skill and skill manager. Activate when the user enables this skill as their
  primary entry point. Reads each incoming query, selects only the skills and MCP tools
  relevant to that query, loads them into the active context, executes the work, then
  unloads heavy skills to keep the context window clean.
  Use when user says: route this, manage my skills, smart context, skill router,
  what skill should I use, tool overload, too many skills, enable context router.
  First response: "Context Router active. Tell me what you need — I'll load the right
  skills and tools for the job and keep everything else out of the way."
license: Apache 2.0
---

# Smart Context Router

A meta-skill that manages every other skill and MCP tool in your registry.
Instead of enabling 20 skills and flooding Claude's context with irrelevant instructions,
you enable **only this one**. It reads your query, loads the minimal set of skills and
tools required, does the work, then unloads them — keeping reasoning quality high and
context noise low.

> The official Claude documentation explicitly warns that "too many tools degrade
> reasoning quality" and recommends giving the model "only what it needs."
> This skill automates that advice.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/route <query>` | Analyse query and load the optimal skill + tool set, then execute |
| `/skills` | List all registered skills with their status (loaded / unloaded / conflict) |
| `/tools` | List all registered MCP tools with their status |
| `/load <skill-name>` | Manually force-load a specific skill |
| `/unload <skill-name>` | Manually unload a skill and free its context budget |
| `/conflicts` | Show the current conflict map — which skills cannot be co-loaded |
| `/registry` | Print the full skill registry (names, triggers, weights, conflicts) |
| `/budget` | Show current context budget usage: tokens used / remaining / by skill |
| `/reset` | Unload all skills, reset to router-only state |
| `/audit` | Explain why each currently-loaded skill was selected for the active query |
| `/history` | Show all skills loaded this session, what triggered them, and how many times each was used |
| `/hot` | Show the 3 most-used skills this session — consider pre-loading these permanently |
| `/explain` | Show the confidence score and signal matches that drove the current routing decision |
| `/why <skill-name>` | Explain in detail why a specific skill was or was not loaded for the last query |

---

## HIGH-LEVEL WORKFLOW

```
Incoming query
    │
    ├─ Phase 1: Intent Classification
    │     Parse query → extract domain signals, action verbs, entity types
    │
    ├─ Phase 2: Skill Selection
    │     Match signals against skill registry trigger maps
    │     Resolve conflicts → pick the minimal covering set
    │     Estimate context budget impact
    │
    ├─ Phase 3: Load
    │     Load selected skills + MCP tools into active context
    │     Log what was loaded and why
    │
    ├─ Phase 4: Delegate
    │     Hand off to the loaded skill(s) — act as transparent pass-through
    │     Capture the result
    │
    └─ Phase 5: Cleanup
          Unload skills flagged as single-use
          Log unload event
          Return result to user
```

---

## PHASE 1 — INTENT CLASSIFICATION

Parse the incoming query and extract three signal types:

### Domain Signals

| Signal type | Examples |
| --- | --- |
| **Entity** | file path, PR URL, component name, database name, package name |
| **Action verb** | review, build, fix, query, deploy, animate, design, test, explain |
| **Technology** | React, Python, MongoDB, Terraform, CSS, SQL, Docker |
| **Intent category** | `code-quality`, `ui-design`, `data`, `infrastructure`, `documentation`, `security`, `explanation` |

### Signal Extraction Rules

1. Scan the query for exact trigger keywords from the skill registry (case-insensitive).
2. If no exact match: run semantic intent matching against the `intent_category` field
   of each registered skill.
3. If intent is ambiguous across two skills: present a one-line disambiguation prompt
   before loading. Do not guess silently.
4. If the query contains a file path or diff, infer technology from file extension and
   add it to the signal set.

### Confidence Threshold

| Confidence | Action |
| --- | --- |
| ≥80% | Load and execute automatically |
| 50–79% | Load with a one-line note: `"Loading <skill> — looks like a <intent> request. Correct me if wrong."` |
| <50% | Ask for clarification before loading anything |

---

## PHASE 2 — SKILL SELECTION

### Default Skill Registry

The registry is seeded with the following entries. Extend it by editing `.context-router.yml`.

```yaml
skills:
  - name: pr-review
    triggers: [review, PR, pull request, diff, audit, code quality, SAST, security scan]
    intent_categories: [code-quality, security]
    context_weight: heavy    # ~8 000 tokens when loaded
    unload_after: single-use
    conflicts: []

  - name: design-system
    triggers: [design, UI, UX, component, animation, token, typography, color,
               layout, CSS, Tailwind, motion, frontend, interface]
    intent_categories: [ui-design]
    context_weight: heavy
    unload_after: session
    conflicts: []

  - name: context-router
    triggers: []             # always loaded — never self-unloads
    intent_categories: []
    context_weight: minimal
    unload_after: never
    conflicts: []
```

Fields:
- `context_weight`: `minimal` (<500 tokens) | `light` (<2 000) | `medium` (<5 000) | `heavy` (>5 000)
- `unload_after`: `single-use` (unload after one response) | `session` (keep until /reset) | `never`
- `conflicts`: list of skill names that cannot be co-loaded (e.g., two competing SQL tools)

### Selection Algorithm

```
1. Collect all skills whose triggers overlap with the query's signal set.
2. If the skill's intent_category matches the classified intent → boost score +20.
3. Sort by score descending. Take the top-scoring skill.
4. If a second skill score is within 10 points of the top → co-load both.
5. Check conflict map: if two selected skills conflict → load only the higher-scored one
   and notify the user.
6. Check total context_weight of the selected set. If it would exceed the budget
   (see Phase 2.1 below) → drop the lowest-scored skill and notify.
7. If no skill scores above 0 → respond without loading any skill;
   add a note: "No registered skill matched this query. Running without specialisation."
```

### Context Budget Management

```
Total context budget    : ~200 000 tokens (Claude 3.x default)
Reserved for output     :  10 000 tokens
Reserved for router     :   1 000 tokens
Reserved for conversation:  20 000 tokens
Available for skills    : ~169 000 tokens
```

If loading the selected set would exceed the available budget:
1. Summarise the lowest-weight loaded skill and replace it with its summary.
2. Log: `"<skill-name> summarised to save ~N tokens."`
3. If still over budget: unload single-use skills from prior turns first.

---

## PHASE 3 — LOAD

When loading a skill:

1. Inject the skill's `SKILL.md` content into the active context.
2. Log a one-line load event in the **Router Log** (appended to the response footer):

```
[ROUTER] Loaded: pr-review  (trigger: "review this PR")  weight: heavy
```

3. For MCP tools: enable only the tool functions listed in the skill's `mcp_tools`
   field. All other MCP tool functions remain hidden from the model.

### MCP Tool Gating

The router acts as a gating layer over MCP tools:

```yaml
# .context-router.yml  — MCP tool assignments
mcp_tools:
  pr-review:
    - mcp_io_github_git_pull_request_read
    - mcp_io_github_git_list_pull_requests
    - mcp_io_github_git_create_pull_request_review

  design-system:
    - open_browser_page
    - screenshot_page

  data-query:
    - mcp_mongodb_mcp_s_find
    - mcp_mongodb_mcp_s_aggregate
    - mcp_mongodb_mcp_s_explain
```

Tools not in any loaded skill's `mcp_tools` list are not surfaced to the model during
that turn. This is the primary mechanism that prevents tool overload.

---

## PHASE 4 — DELEGATE

Once the skill is loaded, the router becomes a transparent pass-through:

- Do not re-process the user's query through router logic.
- Let the loaded skill's instructions take precedence for the task.
- If the loaded skill requests a sub-skill or additional tool mid-task, the router
  intercepts, validates the request against the registry, and loads if valid.
- If two loaded skills give contradictory instructions for the same action,
  apply the higher-scored skill's instruction and log the conflict.

---

## PHASE 5 — CLEANUP

After generating a response:

1. For every `single-use` skill in the loaded set: unload and log:

```
[ROUTER] Unloaded: pr-review  (single-use, turn complete)  freed: ~8 000 tokens
```

2. For `session`-scoped skills: keep loaded until `/reset` or end of session.
3. Append the Router Log to the bottom of the response (collapsed by default if
   the main response is long).

---

## CONFIGURATION FILE

Place `.context-router.yml` in the repo root or Claude project root:

```yaml
# .context-router.yml

# Override default registry or add custom skills
skills:
  - name: my-custom-skill
    triggers: [deploy, release, ship]
    intent_categories: [infrastructure]
    context_weight: medium
    unload_after: single-use
    conflicts: [pr-review]
    skill_file: ./skills/deploy/SKILL.md   # path to the SKILL.md to load
    mcp_tools:
      - mcp_io_github_git_create_pull_request

# Global budget overrides
budget:
  reserved_for_output: 15000
  reserved_for_conversation: 30000

# Confidence threshold override
routing:
  auto_load_threshold: 80       # % confidence required for silent auto-load
  disambiguation_threshold: 50  # below this → ask before loading

# Conflict map (overrides per-skill conflict lists)
conflicts:
  - [skill-a, skill-b]   # these two can never be co-loaded
```

---

## ROUTER LOG FORMAT

The router appends a collapsible log block to every response:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONTEXT ROUTER LOG
  Query intent  : code-quality  (confidence: 94%)
  ─────────────────────────────────────────────────────
  Loaded        : pr-review          weight: heavy  (+8 200 tokens)
  MCP tools     : github-pr-read, github-pr-list   (2 / 47 total tools exposed)
  Skipped       : design-system      reason: no UI signals
  Skipped       : context-router     reason: always-loaded, not counted
  ─────────────────────────────────────────────────────
  Budget used   : 29 400 / 169 000 tokens  (17%)
  ─────────────────────────────────────────────────────
  Unloaded      : pr-review          freed: ~8 200 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## CONFLICT MAP

Conflicts prevent co-loading skills that would contradict each other or waste context.

**Built-in conflict rules:**

| Conflict | Reason |
| --- | --- |
| Two competing database skills (e.g., `mongo-query` + `sql-query`) | Contradictory query syntax guidance confuses output |
| Two competing style systems (e.g., `tailwind-design` + `css-modules-design`) | Contradictory class naming conventions |
| A general skill + its specialised variant (e.g., `code-review` + `pr-review`) | Specialised skill is strictly better; general skill adds noise |

**Conflict resolution:** always load the higher-scored (more specific) skill. Log:

```
[ROUTER] Conflict: pr-review vs code-review — loaded pr-review (score: 92 vs 61)
```

---

## BEHAVIOUR RULES

- **Never load more than is needed.** One well-matched skill is better than three
  partially-relevant ones.
- **Always log routing decisions.** The user should never wonder why a particular
  skill was or was not loaded.
- **Disambiguation over guessing.** When confidence is below 50%, ask one clarifying
  question rather than guessing and potentially loading the wrong skill.
- **Transparent pass-through.** Once a skill is loaded, do not re-interpret its
  instructions through the router lens. The skill owns the task.
- **Conflict resolution is silent when unambiguous.** Only notify the user when a
  conflict required dropping a skill they explicitly requested.
- **Never self-unload.** The router itself is always in context.
- **Respect explicit overrides.** If the user runs `/load <skill>` manually, do not
  unload it based on routing logic alone — only `/reset` or `/unload` can remove it.
- **MCP tool gating is strict.** A tool not assigned to any loaded skill is never
  surfaced, regardless of how relevant it seems.

---

## EXTENDING THE REGISTRY

To add a new skill to the router:

1. Create the skill's `SKILL.md` file at `./skills/<name>/SKILL.md`.
2. Add an entry to `.context-router.yml`:

```yaml
skills:
  - name: my-new-skill
    triggers: [keyword1, keyword2, "multi word trigger"]
    intent_categories: [code-quality]   # pick from the standard category list
    context_weight: medium
    unload_after: single-use
    conflicts: []
    skill_file: ./skills/my-new-skill/SKILL.md
    mcp_tools: []   # add any MCP tool names this skill needs
```

3. Run `/registry` to confirm the skill appears and `/route <test query>` to verify
   it triggers correctly.

**Standard intent categories:**

| Category | Description |
| --- | --- |
| `code-quality` | Review, audit, refactor, test |
| `ui-design` | Frontend, component, animation, styling |
| `data` | Database queries, schema, migrations |
| `infrastructure` | CI/CD, deployment, IaC, Docker |
| `documentation` | Writing, editing, README, changelogs |
| `security` | Vulnerability scanning, threat modelling |
| `explanation` | Teaching, debugging help, concept explanation |
| `planning` | Architecture decisions, task breakdown, roadmapping |

---

## EXAMPLES

### Example: automatic routing

> User: "Review this PR — diff attached."

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONTEXT ROUTER LOG
  Query intent  : code-quality  (confidence: 97%)
  Loaded        : pr-review          weight: heavy  (+8 200 tokens)
  MCP tools     : github-pr-read  (1 / 47 total tools exposed)
  Skipped       : design-system  (no UI signals)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[pr-review skill output follows…]
```

### Example: low-confidence disambiguation

> User: "Help me with the modal."

```
Ambiguous query — could be:
  A) UI/component work  → would load: design-system
  B) Code review of a modal component  → would load: pr-review

Which do you mean?  (A / B / describe further)
```

### Example: budget pressure

> User: "Review this PR and also redesign the button component."

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONTEXT ROUTER LOG
  Query intent  : code-quality + ui-design  (multi-intent)
  Loaded        : pr-review          weight: heavy  (+8 200 tokens)
  Loaded        : design-system      weight: heavy  (+9 100 tokens)
  Budget        : 46 500 / 169 000 tokens  (28%) — within limits
  MCP tools     : github-pr-read, screenshot_page  (2 / 47 exposed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Example: /skills output

```
REGISTERED SKILLS
  ● pr-review         [unloaded]  triggers: review, PR, diff, audit…
  ● design-system     [loaded]    triggers: design, UI, component…
  ● context-router    [loaded]    (always-on)

Run /load <name> to force-load a skill.
Run /unload <name> to free its context budget.
```

### Example: MCP tool overload prevention

Without context-router: 47 MCP tool definitions in context → model picks wrong tool,
reasoning degrades, latency increases.

With context-router loading `pr-review`: 1 tool exposed → model always picks correctly.

---

## ROUTING LOG FORMAT

After every routed response, append a one-line routing summary so the user always knows what's active:

```
[Router] Loaded: pr-review (97% confidence · "review" signal) | Budget: 8 200/169 000 tokens | /explain for details
```

This line keeps iteration fast — the user sees the current state without running `/audit`.

---

## ITERATION AND HISTORY

**Session history tracking:** Every load/unload event is logged internally with the triggering query and confidence score.

`/history` output format:

```
SESSION ROUTING HISTORY
  Turn 1  → pr-review loaded  (query: "review this PR")         used: 3 turns
  Turn 4  → pr-review unloaded  (single-use cleanup)
  Turn 5  → design-system loaded  (query: "redesign the button") used: 2 turns
  Turn 7  → design-system still active

  HOT SKILLS (most used):
  1. pr-review        3 turns loaded
  2. design-system    2 turns loaded

  → Consider adding these to always-on in .context-router.yml
```

**`/hot` output** surfaces co-occurrence patterns: which two skills are loaded together most often. If pr-review and security are always co-loaded, suggest merging their triggers into a single routing rule.

**Routing improvement loop:**
1. Run `/history` after a session.
2. If any skill was loaded with confidence <80% and the load was correct → add the triggering query's phrasing to the skill's trigger list.
3. If a skill was loaded and turned out to be wrong → add the triggering query as a negative trigger.
4. Run `/registry` to confirm the update took effect.
5. Test with `/route <original query>` to verify the confidence score improved.
