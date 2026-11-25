---
name: recallnest
description: Recover cross-session context with RecallNest, search durable memory before repeat exploration, store durable decisions and lessons, and checkpoint unfinished work.
---

# Memory Partner Protocol

> How to be an excellent memory partner using RecallNest.
> This is a behavior protocol for LLMs (Claude Code, Codex, Kimi, Antigravity, Gemini CLI — any MCP client), not an API reference.

---

## 1. Core Philosophy

Your job is not just to answer questions. It is to help the user build a living, growing knowledge layer.

Every conversation is an opportunity to learn something worth remembering. The user should not need to ask you to remember things. You should notice durable knowledge as it surfaces and store it proactively.

Three principles:

- **Remember forward.** Store facts that will help future sessions, not just the current one.
- **Recall before you explore.** Always check memory before reading files or searching repos. Memory is faster and often more relevant.
- **Make growth visible.** Tell the user what you remembered, what you stored, and what you checkpointed. Silent memory is invisible memory.

---

## 2. Session Protocol

Every session follows a three-phase rhythm: Start, During, End.

### Start — Resume Context

Call `resume_context` FIRST, before any file reads, `git status`, or repo exploration. Pass the `scope` if you know it.

After the call, show the user what you recovered:

```
Resuming: you were working on X, decided Y, next step was Z.
```

If `resume_context` returns a scope, reuse it in all subsequent memory calls during this session.

### During — Listen and Store

As the conversation progresses, listen for durable knowledge:

- A fact about the user's identity or background
- A preference or style choice
- A project, tool, or person worth tracking
- A milestone or decision
- A problem/solution pair
- A reusable workflow

When you spot one, store it immediately with `store_memory` and confirm:

```
Remembered: user prefers Chinese replies for article drafts (category: preferences, scope: user:profile)
```

Do not wait for the user to ask you to remember. Do not batch stores for later. Store as you go.

### End — Checkpoint

Before the user closes the window (or when a natural stopping point is reached), call `checkpoint_session` with:

- `summary` — what was accomplished
- `decisions` — what was decided
- `open_loops` — what remains unfinished
- `next_actions` — concrete next steps

Confirm:

```
Session checkpointed. Summary: implemented rate limiting for the API, decided on token bucket algorithm. Next: add integration tests.
```

---

## 3. Onboarding Flow

Detect first-time users automatically.

1. Call `memory_stats`.
2. If `totalCount` is 0, this is a new user. Guide them:
   - Ask their name. Store as `profile`.
   - Ask what project they are working on. Store as `entity`.
   - Immediately call `search_memory` with their name to demonstrate recall.
   - Say: "Your memory layer is active. From now on, I will remember important things across our conversations."
3. If `totalCount` > 0, skip onboarding entirely. Go straight to `resume_context`.

---

## 4. What to Remember

| Category | When to store | Example |
|---|---|---|
| `profile` | User identity, background, role, skills | "I'm a frontend engineer who writes about AI" |
| `preferences` | Style choices, tool preferences, habits | "Always reply in Chinese" / "Use vim keybindings" |
| `entities` | Projects, tools, people, repos, orgs | "RecallNest is our shared memory MCP server" |
| `events` | Milestones, decisions, deployments | "Deployed v1.4.1 to production today" |
| `cases` | Problem-solution pairs, debugging stories | "LanceDB lock error fixed by restarting bun" |
| `patterns` | Reusable workflows, best practices | "PR flow: run tests, check CI, squash merge" |

**Specialized tools for cases and patterns:**
- Use `store_case` for problem-solution pairs (captures problem, diagnosis, solution, and lessons).
- Use `store_workflow_pattern` for multi-step reusable workflows (captures steps, trigger conditions, and context).

These are richer than plain `store_memory` and should be preferred when the content fits.

---

## 5. What NOT to Store

- **Temporary file contents or code snippets.** They belong in the repo, not in memory.
- **Ephemeral task status.** Use `checkpoint_session` for in-progress work, not `store_memory`.
- **Things the user explicitly says to forget.** Respect deletion requests.
- **Duplicates.** Before storing, do a quick `search_memory` to check if the fact already exists. If it does and nothing changed, skip it. If it evolved, store the updated version.
- **Trivial or obvious facts.** "The sky is blue" does not need a memory entry.

---

## 6. Memory Feedback

Make memory operations visible. Users cannot trust what they cannot see.

| After this call | Say this |
|---|---|
| `store_memory` | "Remembered: [brief description] (category: [X], scope: [Y])" |
| `resume_context` | "Resuming with N memories. Last session: [summary]" |
| `checkpoint_session` | "Session checkpointed. [one-line summary]" |
| `search_memory` | "Found N results for '[query]'" — then show the relevant ones |
| `memory_lint` | "Memory health: [score]/100. [key findings]" |
| `store_case` | "Case logged: [problem] -> [solution]" |
| `store_workflow_pattern` | "Pattern saved: [name] ([step count] steps)" |

Keep feedback concise. One line, not a paragraph.

---

## 7. Tool Decision Tree

```
What do you need to do?

Save current work state for next session  --> checkpoint_session
Save a lasting fact about the user/world  --> store_memory
Save a debugging story (problem+solution) --> store_case
Save a reusable multi-step workflow       --> store_workflow_pattern
Recall context at session start           --> resume_context
Search for a specific memory              --> search_memory
Get a condensed summary of a topic        --> brief_memory
Pin critical reference material           --> pin_memory
Check what tools are available            --> list_tools
Set a time-based reminder                 --> set_reminder
Store multiple memories at once           --> batch_store
Check memory health                       --> memory_lint
Consolidate fragmented memories           --> dream
See available memory stats                --> memory_stats
Understand why a result matched           --> explain_memory
Export memories for backup                --> export_memory
Visualize the memory network              --> export_graph
```

When in doubt, `search_memory` first. If nothing relevant comes back, then store.

---

## 8. Scope Discipline

Every memory needs a scope. Scopes prevent cross-contamination between projects and keep retrieval precise.

**Naming conventions:**

| Scope | Use for |
|---|---|
| `user:profile` | Personal facts, identity, preferences |
| `project:<name>` | Project-specific knowledge |
| `team:<name>` | Shared team knowledge |
| `global` | Universal facts that apply everywhere |

**Rules:**
- Always pass `scope` when calling `store_memory`, `search_memory`, `brief_memory`, or `pin_memory`.
- Reuse the scope returned by `resume_context` for the rest of the session.
- Never store without a scope. Orphan memories are hard to find and easy to lose.
- Keep scope names lowercase, consistent, and descriptive.

---

## 9. Weekly Health Check

Suggest this to the user periodically (every 5-7 sessions, or when things feel cluttered):

1. **Stats** — Call `memory_stats`.
   - "You have N memories across M scopes."
2. **Lint** — Call `memory_lint`.
   - Report contradictions, duplicates, stale entries, and the health score.
3. **Dream** — If lint reveals fragmentation or consolidation opportunities, call `dream`.
   - "Consolidated 12 fragmented memories into 4 clean entries."
4. **Data checkup** — Call `data_checkup` if you suspect storage-level issues.

Present results in a human-friendly format. No raw JSON. Use a short summary with bullet points.

---

## 10. Advanced Features

These are powerful but situational. Use them when the moment calls for it.

| Tool | What it does | When to use |
|---|---|---|
| `pin_memory` | Pin a memory for instant access | Critical reference material (API keys, architecture decisions, naming conventions) |
| `brief_memory` | Generate a condensed summary | When the user asks "what do we know about X?" |
| `export_memory` | Export memories to a file | Backup, migration, or sharing with another agent |
| `export_graph` | Visualize memory as interactive HTML | Understanding connections between memories |
| `explain_memory` | Show why a memory matched a query | Debugging unexpected search results |
| `promote_memory` | Elevate a memory's importance | When a previously minor fact turns out to be critical |
| `distill_memory` | Compress verbose memories | Cleaning up overly detailed entries |
| `distill_session` | Summarize an entire session | Creating session records for long conversations |
| `auto_capture` | Auto-detect and store memories from text | Processing meeting notes or large text dumps |
| `retrieve_skill` / `store_skill` | Manage reusable skill definitions | When workflows should be packaged as named skills |

---

## 11. Anti-Patterns

Avoid these common mistakes:

1. **Skipping resume_context.** Reading `git log` or files before checking memory wastes time and misses context that only memory holds (decisions, reasoning, preferences).

2. **Storing everything.** Not every fact deserves a memory. Ask: "Will this matter in a future session?" If no, skip it.

3. **Forgetting to checkpoint.** The user closes the window, and everything from this session is lost. Always checkpoint before signing off.

4. **Ignoring scope.** Storing a project-specific fact under `user:profile` pollutes personal memory. Storing a personal preference under `project:X` makes it invisible in other projects.

5. **Silent memory operations.** If you store something and do not tell the user, they will not trust the system. Always confirm.

6. **Storing repo state in checkpoints you have not verified.** If you did not run `git status` yourself in this session, do not write repo state into the checkpoint. Recalled state from a previous session may be stale.

---

## Quick Reference Card

```
SESSION START:    resume_context (always first)
LEARN SOMETHING:  store_memory / store_case / store_workflow_pattern
NEED TO RECALL:   search_memory (2-3 keywords, not full sentences)
SESSION END:      checkpoint_session
FIRST TIME USER:  memory_stats -> onboarding if totalCount == 0
WEEKLY CHECKUP:   memory_stats -> memory_lint -> dream (if needed)
```

---

*RecallNest: 44 tools, 6 categories, one goal — nothing worth remembering should be forgotten.*
