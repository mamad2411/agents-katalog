---
name: council
description: >
  Run one request through several skills in parallel, isolated subagents, then
  merge their answers or judge the single best one. Use when the user invokes
  /council (or /council manage), or uses clear multi-skill-comparison language
  like "try this with a few different skills", "compare how different skills
  answer this", "which skill gives the best answer here", or "run this through
  multiple skills and combine them". Do NOT trigger on vague or ambiguous
  requests — and when triggering from natural language (not /council), briefly
  confirm before launching: "Want me to run this through Council — pick a few
  skills and compare?"
---

# Council — Multi-Skill Orchestrator

Run the user's request through several skills *in isolation* (one subagent per
skill, each seeing only its own skill's instructions), then aggregate: either
one merged answer or the single best one. You (the main conversation) are the
orchestrator and the aggregator — never delegate aggregation to a subagent.

## Isolation & trust model (read before first run)

Isolation here is achieved by **prompt construction, not sandboxing**. Each
subagent is a fresh `general-purpose` agent whose prompt contains only one
skill's SKILL.md plus the user's request — but that agent still runs with the
same tool access any subagent has (file reads, Bash, network, etc.). Putting a
skill on a council therefore grants it exactly the capability it would have if
the user invoked it directly. Council does not add a security boundary and does
not vet the skills it dispatches. Only add skills you already trust to the
discoverable set, and treat an imported skillset (see Import / export) as a
list of *names to run*, never as a reason to install skills you haven't
reviewed.

## Helper scripts

All state and discovery logic lives in two scripts (both print JSON):

```bash
# Discover installed skills (name + description; project scope wins on
# name collision; council itself is excluded):
python3 ~/.claude/skills/council/scripts/discover_skills.py --project-dir "$PWD"
python3 ~/.claude/skills/council/scripts/discover_skills.py --format list        # numbered, for showing the user
python3 ~/.claude/skills/council/scripts/discover_skills.py --content <name>     # full SKILL.md, for subagent prompts

# Skillset store (~/.claude/skills/council/skillsets.json, created on first write):
python3 ~/.claude/skills/council/scripts/skillset_store.py list
python3 ~/.claude/skills/council/scripts/skillset_store.py last-run
python3 ~/.claude/skills/council/scripts/skillset_store.py create <name> --skills a,b,c
python3 ~/.claude/skills/council/scripts/skillset_store.py rename <old> <new>
python3 ~/.claude/skills/council/scripts/skillset_store.py set-skills <name> --skills a,b,c
python3 ~/.claude/skills/council/scripts/skillset_store.py add-skills <name> --skills d
python3 ~/.claude/skills/council/scripts/skillset_store.py remove-skills <name> --skills b
python3 ~/.claude/skills/council/scripts/skillset_store.py delete <name>
python3 ~/.claude/skills/council/scripts/skillset_store.py export <name> --out file.json
python3 ~/.claude/skills/council/scripts/skillset_store.py import file.json [--name X] [--overwrite]
python3 ~/.claude/skills/council/scripts/skillset_store.py record-run --type skillset --name X --mode combined
python3 ~/.claude/skills/council/scripts/skillset_store.py record-run --type manual --skills a,b --mode best
```

Never edit `skillsets.json` by hand — always go through the store script.

## Entry points

- `/council` (no args, or with the request inline) → main flow below.
- `/council manage` → skip straight to **Managing skillsets**.
- Natural-language trigger → confirm first ("Want me to run this through
  Council — pick a few skills and compare?"), then main flow.

If the user hasn't yet stated the request they want run through the skills,
ask for it before dispatching (selection can happen first — the request is
only needed at dispatch time).

## Main flow

### Step 1 — Discover and load state

Run `discover_skills.py` (JSON) and `skillset_store.py last-run` (one Bash
call is fine). If discovery returns no skills, tell the user and stop.

### Step 2 — Selection question

Ask ONE `AskUserQuestion` with these options:

1. **"Re-run last"** — ONLY if `last-run` returned a non-null `lastRun`. The
   label stays short; put the specifics in the option description so the user
   knows exactly what re-runs, e.g. *"Runs the 'Writing' skillset in merged
   mode (your last run)"* or, for a manual last run, list the skills. Never
   show this option on first-ever use.
2. **"Choose manually"** — pick skills ad hoc (below).
3. **"Skillset list"** — browse saved skillsets (below).
4. **"Create skillset"** — build, save, and immediately run a new one (below).

If "Re-run last" is chosen: skip mode selection entirely (mode is part of the
remembered config) and go straight to dispatch. If the last run pointed at a
skillset, re-read its current skill list from the store (it may have been
edited since).

### Step 2a — Choose manually

- **≤4 discovered skills**: one `AskUserQuestion` with `multiSelect: true`,
  one option per skill (description = the skill's description, truncated).
- **>4 skills**: show the numbered list from `discover_skills.py --format
  list` as plain text and ask the user to reply with comma-separated numbers
  (e.g. "1, 3, 5"). Prefer this over paginated picker rounds. Map numbers back
  to names; confirm the resolved names in one line before proceeding.

### Step 2b — Skillset list

- Run `skillset_store.py list`. If empty, say so and offer to create one.
- Show a numbered plain-text list: name, skills, and `lastModeUsed` if set.
  User replies with a number.
- If the chosen skillset has a `lastModeUsed`, offer it as a quick-confirm
  ("Use combined mode again, like last time?") instead of the full mode
  question; otherwise proceed to Step 3.

### Step 2c — Create skillset

1. Ask for a name (plain text question is fine).
2. Run the manual picker (Step 2a) to choose its skills.
3. `skillset_store.py create <name> --skills ...`
4. Proceed immediately to Step 3 and run it.

### Step 3 — Mode selection

Ask via `AskUserQuestion` (skip if already decided by "Re-run last" or a
quick-confirmed `lastModeUsed`):

1. **"One merged answer"** — synthesize all candidates (mode `combined`).
2. **"Single best answer"** — judge and present the strongest (mode `best`).

### Step 4 — Cost warning

If more than 5 skills are selected, warn before dispatching: "You've selected
N skills — this will run N parallel subagent calls before combining them.
Continue?" (AskUserQuestion, Continue / Trim the list). Threshold is fixed at
5 for now.

### Step 5 — Record, then dispatch in parallel

First record the run config:
- skillset run: `record-run --type skillset --name <name> --mode <mode>`
- manual run: `record-run --type manual --skills a,b,c --mode <mode>`

Then, for each selected skill, fetch its full instructions with
`discover_skills.py --content <name>`. If that fails (skill missing —
possible after an import or an uninstall), do NOT abort: mark that skill
failed and dispatch the rest.

Dispatch ALL subagents in a SINGLE message (one Agent tool call per skill in
the same block — that is what makes them run concurrently). Each uses
`subagent_type: general-purpose` and this prompt shape, with NOTHING else —
no conversation history, no other skills' content:

```
You are executing exactly one skill in isolation.

<skill_instructions>
{full SKILL.md content of the one assigned skill}
</skill_instructions>

<user_request>
{the user's original request, verbatim}
</user_request>

Rules:
- Follow ONLY the skill instructions above. Do not invoke, load, or borrow
  from any other skill, even if one seems relevant.
- Do not ask the user questions; make reasonable assumptions and state them.
- Your final message is your complete answer to the request, produced the way
  this skill would produce it.
```

### Step 6 — Failure-tolerant aggregation (done by YOU, not a subagent)

Collect all results. A subagent that errored, timed out, returned nothing
usable, or whose skill file was missing is a *failed* candidate; the rest
proceed. If ALL failed, report that plainly and stop.

- **best**: read every successful candidate, silently judge which is
  strongest for the user's request, and present that answer directly and
  completely. Do not narrate the judging or reveal scores.
- **combined**: merge the distinct, non-redundant strengths of the candidates
  into ONE coherent answer. This is a real synthesis — not a stitched list of
  "skill X said… skill Y said…".

### Step 7 — Output

- Show ONLY the final aggregated answer.
- If any skill failed, append one short note, e.g. *"Note: the `xlsx` skill
  didn't respond and wasn't included above."*
- Do NOT show individual raw outputs by default.

### Reveal on request

If the user later asks "show me each one" / "what did each skill say", present
the individual outputs from that run, each labeled with its skill name, pulled
from what is already in context. Never re-run the subagents for this.

## Managing skillsets (`/council manage`)

Show the numbered skillset list (`skillset_store.py list`), then ask what to
do (rename / edit skills / delete / export / import) and apply it with the
matching store command. For **edit**, show the current skill list plus the
discovery list, and use `add-skills` / `remove-skills` / `set-skills`. For
**delete**, confirm first.

## Import / export

- **Export**: `export <name> --out <file>.json` — a standalone shareable file,
  shape `{"name": "...", "skills": [...]}`.
- **Import**: `import <file>` — then immediately cross-check the imported
  skill names against `discover_skills.py` output and tell the user which (if
  any) are NOT installed. Always surface this caveat: a skillset is just a
  list of skill names — it does not bundle the skill files themselves, so
  missing skills stay missing until installed, and are flagged again at run
  time by the Step 5 failure handling. Never silently drop them.
