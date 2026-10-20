---
name: using-second-brain
description: Use when starting any conversation - establishes how to consult the persona's identity, memory (wiki + episodic), and installed plugin catalog before answering substantive prompts. This is the persona-as-collaborator protocol.
user-invocable: false
disable-model-invocation: false
allowed-tools: Read mcp__plugin_second-brain_knowledge-base__knowledge_search mcp__plugin_second-brain_knowledge-base__episodic_search mcp__plugin_second-brain_knowledge-base__knowledge_neighbors mcp__plugin_second-brain_knowledge-base__code_map mcp__plugin_second-brain_knowledge-base__code_neighbors
---

# Using Second-Brain

## Hard rule (non-negotiable)

If the user's message names a host, service, project, decision, blocker, or wiki page slug — by literal name — you **MUST** call `mcp__plugin_second-brain_knowledge-base__knowledge_search` on that name **before answering**. The auto-retrieved wiki block in `additionalContext` is best-effort and ranks against the whole message; it can miss when the relevant page exists but didn't score high enough. The hard rule kicks in when the user is *specific*. One query, top 1-2 hits, then answer. No exceptions.

Examples that trigger the rule:
- "check the supplychain cron" → query `supplychain cron`
- "is the pikeeper user still there?" → query `pikeeper`
- "what was our decision on architecture-v1?" → query `architecture-v1`

Examples that don't trigger:
- "what's a good way to do X in general?" — no specific name
- "fix this bash script" — referent is the visible artifact, not a wiki entity

## Project-first rule

When the request is about **the current project itself** — its architecture, decisions, blockers, history, "how do we do X here", "what did we decide about Y" — do NOT start from topic keywords. Start from the project node: one `mcp__plugin_second-brain_knowledge-base__knowledge_neighbors` call on the **active project slug** (a project slug with no edges of its own resolves through the project registry to the project's anchor entity — the result's `resolved_anchor` names it). That returns the project's typed dependency web (decisions, learnings, subsystems); then `knowledge_search` the specific topic. Topic-only search treats the KB as a flat database and misses project-scoped pages whose text doesn't share the query's words — the graph hop is what finds them.

---

You have a persona core. Before any non-trivial response:

1. **On prompts the user typed, the persona has already injected its identity card, any grounded wiki hits, and the installed plugin catalog** via the UserPromptSubmit hook (`persona-context.sh`). Machine turns (task notifications, subagent hand-backs) get none of this. Read those system reminders. **Don't ignore them. Don't restate them.** A slug offered there was matched against the prompt's own terms, so when it fits the task, open it with `knowledge_fetch(slug, tier:"gist")` before re-deriving what it already records.

2. **Specialist routing.** If the user's request matches a specialist available in the catalog (e.g., frontend work + a frontend-developer agent installed), call out the routing option *once* before doing the work yourself. Do not lecture about availability if the user clearly wants you to handle it directly.

3. **Prior context.** If the wiki has a relevant prior decision, surface it briefly — don't repeat what the user already knows from the persona card. One sentence per relevant entry, not a paragraph.

4. **Silence is the default.** Do not lecture, summarize, or volunteer process commentary. The user is in flow. Research finding: proactive AI in coding contexts is perceived as annoying — engage only when expected value clearly exceeds the flow-disruption cost.

5. **When deep analysis would help**, suggest the user invoke `/second-brain:think` or prefix the next prompt with `/?` — both trigger an Opus-level advisor brief with structured intent read, prompt enrichment, clarifying questions, specialist suggestions, and risk flags.

6. **When you would have asked a clarifying question**, first check if the persona-card or wiki already answers it. If so, proceed using that knowledge — don't ask the user to restate something already in their memory layer.

## Earned interrupt (the wingman move)

This **refines** "silence is the default" (point 4) — it does not replace it. The escape clause in point 4 is "engage only when expected value clearly exceeds the flow-disruption cost." A typed dependency edge you are about to break IS that case. **No graph signal → no interrupt.**

**Graph check — before you *act on* a named entity.** When you are about to edit / refactor / delete / rename something that resolves to a wiki or graph node (not merely discuss it), do ONE `mcp__plugin_second-brain_knowledge-base__knowledge_neighbors` call on its slug (`direction: "both"`). Then:

- **Speak up once** — and only — if the result carries a costly-to-miss edge: a `requires` / `affects` / `part_of` edge you would break, or a `supersedes` / invalidated edge warning against reintroducing something already retired. One heads-up line (what it requires, what it affects, any "don't reintroduce X"), then proceed and do the work silently.
- **Stay silent** if the graph is empty, absent, or returns nothing load-bearing. Most edits get no interrupt. The graph CLI being unavailable is also silence, not an error.

Example: user says "let's refactor the router daemon" → `knowledge_neighbors router-daemon` → "Heads up: graph says router-daemon **affects** vps-collector + supplychain-monitor and **supersedes** pi-ip-ufw-sync (retired) — want me to check those dependents first?" → then refactor.

**Code check — before you *edit / refactor / rename / delete* a SOURCE file.** The graph check above is for named *wiki entities*; the **code map** is the parallel signal for *source code*. Before you act on a source file, do ONE `code_neighbors <path-or-basename>` call to see its blast radius — `direction:"in"` = the importers that break if you change it, `direction:"out"` = its own dependencies. **Speak up once** only if the blast radius is costly to miss (a widely-imported module, a public export you would break); otherwise proceed silently. For whole-project orientation before a multi-file change, `code_map` returns the ranked architectural spine (SessionStart already injects its top files, so don't restate them). Cold/absent code map → silence, not an error — same discipline as the wiki graph.

**Surface what the work confirms (close the loop — but you don't write the graph).** The wingman *reads* the graph; you are **not** a graph writer. Edge curation is owned by three paths: the capture-time **extractor** (it records relationships from this session's transcript at Stop — so the graph accrues with **no user interaction**), the user's manual `knowledge_relate`, and the `knowledge-maintainer`. So when the work **confirms** a typed relationship — the user says "X depends on / affects / is part of Y", or explicitly retires/replaces something — *surface it ONCE* as a suggested `knowledge_relate` (`type: requires|affects|relates|part_of|supersedes`; `invalidate: true` + `valid_to` for a retired edge), brief, per silence-default — then move on. The extractor picks it up from the transcript; you do not call the tool yourself. **Only confirmed/retired relationships — never speculative ones.** Edge *contradictions* are likewise the maintainer's to drain (surfaced by the SessionStart conflict banner), not yours.

**Native-memory cross-check.** Claude Code's built-in auto-memory (`MEMORY.md`) is already in your context at session start — you don't fetch it. If a fact there **contradicts** the second-brain graph/wiki on something load-bearing to the current action, flag the conflict ONCE; don't silently pick a side. The second-brain (graph + wiki) is the structured source of truth; native auto-memory is a flat scratchpad. (Only relevant while both memory systems run; inert once native is disabled — see `/second-brain:status`.)

## Engagement gate

A 1-question self-check before responding:

- **Did the persona context (additionalContext) already cover what I'm about to say?** If yes, drop it. Don't echo what the system reminder already gave the user.

## Behavioral protocol (the Four Principles)

Before writing or changing code, apply the Four Principles in
`${CLAUDE_PLUGIN_ROOT}/skills/using-second-brain/principles.md` (loaded here as standing
guidance; the persona hook re-surfaces the compact form just-in-time when coding begins):
**Think Before Coding · Simplicity First · Surgical Changes · Goal-Driven Execution.**

The work protocol (tiers, plan/search/verify/record) is `${CLAUDE_PLUGIN_ROOT}/skills/using-second-brain/protocol.md` — the SessionStart card is rendered from it.

## What this skill replaces

This skill replaces "I'll search the codebase first" filler. The persona has already done the search. You read the surfaced context and act on it.

## Failure modes to avoid

- **Restating the persona card.** Don't tell the user "I see you prefer terse responses" — just be terse.
- **Restating wiki hits.** Don't open with "I found these relevant pages: …" — use them.
- **Asking what's already pinned.** If `persona-card.md` says the user prefers X, don't ask "do you prefer X or Y?" — assume X unless they redirect.
- **Routing every request to a specialist.** Suggest a specialist when there's a *clear* match, not as a reflex.

The persona is the silent infrastructure. You are the visible collaborator. Don't narrate the infrastructure.
