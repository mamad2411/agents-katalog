---
name: promptize
description: Turn a rough ask into a structured prompt that the user reviews before execution. When the user invokes "/promptize <rough-ask>", Claude parses the ask, clarifies until ≥95% confidence, assembles the prompt using a 9-field canonical structure (Goal, Context, Inputs, Expected output, Scope, Constraints, Success criteria, Open assumptions, Examples), shows it for approval, then executes (in-session by default; optionally in an isolated subagent to avoid context contamination). Approved prompts auto-save to ~/.claude/prompts/ as a versioned history. User-initiated only — never convert a normal request into promptize mode proactively.
user-invocable: true
arguments: [initial_ask]
argument-hint: "<rough initial ask>  e.g. /promptize audit my settings.json for risks"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - WebFetch
  - AskUserQuestion
---

# /promptize — Turn a rough ask into a structured prompt

Guide the user through turning a rough ask into a well-structured prompt, then execute the approved prompt. This skill implements a confidence-gate discipline as a reviewable artefact: it prevents assumption-based execution, produces a prompt worth keeping, and saves approved prompts to a versioned library for reuse. (It pairs naturally with any confidence/verification rules in your `CLAUDE.md`.)

**Target confidence: ≥95%** before assembling and executing — the prompt itself IS the deliverable, and any ambiguity in it propagates downstream into execution.

The skill is invoked explicitly by the user. Never convert a normal ask into promptize mode proactively.

## Design principle — no consequential decision without informed gating

Promptize applies one principle at four touchpoints — gating every consequential decision from intent through completion:

1. **The user's intent** (Steps 1–2, the clarify loop) — never execute on a guessed intent. *(Guards against goal drift before it can start.)*
2. **The user's technical choices** (Step 2a) — when a clarification is a consequential choice the user may not have the full picture on, present grounded trade-offs + a marked, contestable recommendation, not an open-ended question.
3. **The agent's mid-execution forks** (Step 5b) — on an unanticipated *consequential* fork the prompt does not cover, the executor never guesses silently and never blocks an unattended run: in-session it may pause and ask; in auto/subagent mode it takes the safest reversible option (or defers that one branch), records the fork, and surfaces it in the final report. Governed autonomy, not interruption.
4. **The agent's "done" declaration** (Step 5c) — before declaring the task complete, verify the output against the *Success criteria*. This counters *agentic laziness* (stopping early): you set the bar, so check you reached it. *(It only partially counters* self-preferential bias *— an agent grading its own work; the full cure is an independent reviewer, which is orchestration, not Promptize's job.)*

Same move every time: structure and inform a decision *before* it is committed — whether the decider is the user or the executing agent.

---

## When to use / skip

**Use** when:
- The ask is non-trivial and the initial phrasing is ambiguous
- Output quality matters more than getting started fast
- An architectural decision is involved
- The user has a rough idea and wants Claude to produce better-structured execution
- The work would benefit from a reviewable artefact (prompt) before any action

**Skip** when:
- Small / clarifying question
- Follow-up in an active thread
- Brainstorming (not committing to an outcome yet)
- Authorisation-like responses ("commit", "proceed", "ok")
- Tasks where the structure is already fully specified in the first message

If the user asks normally and the ask looks non-trivial enough that `/promptize` would help, Claude may gently suggest it ("this feels like a `/promptize` candidate — want me to structure it?") but does NOT convert automatically.

---

## Step 1 — Parse and identify unknowns

1. Read the user's initial ask (`$initial_ask`).
2. State to the user:

   > Parsing `/promptize` ask: *"<initial ask verbatim>"*
   >
   > Field-by-field readiness (✓ clear, ? needs clarification):
   >
   > | # | Field | Status | Notes |
   > |---|---|---|---|
   > | 1 | Goal | ✓ / ? | <inference or question> |
   > | 2 | Context | ✓ / ? | ... |
   > | 3 | Inputs | ✓ / ? | ... |
   > | 4 | Expected output | ✓ / ? | ... |
   > | 5 | Scope | ✓ / ? | ... |
   > | 6 | Constraints | ✓ / ? | ... |
   > | 7 | Success criteria | ✓ / ? | ... |
   > | 8 | Open assumptions | N/A until the end | ... |
   > | 9 | Examples | optional | ... |
   >
   > Initial confidence: <N>%. Proceeding to Step 2 to clarify the `?` fields.

## Step 2 — Clarify

For each `?` field, ask 1-3 questions per turn. In English. No cap — keep asking until confidence reaches ≥95% OR the user says "proceed" / "go ahead" / equivalent.

**Ask via `AskUserQuestion` when the host provides it** — present each clarification as a structured choice (labelled options + short descriptions); the user clicks, or picks *Other*. If the host agent has no `AskUserQuestion` primitive, **fall back to plain prose questions** — same questions, no loss (capability-gated, like subagent mode).

State confidence % explicitly before each question batch. After each answer, re-evaluate and state the new confidence. If it is still <95%, ask the next question.

If the user authorises proceeding with open unknowns, document them in the prompt's Open assumptions field (Step 3) — risk transferred in the open rather than buried.

## Step 2a — Informed choice on consequential technical decisions

When a `?` field is a **consequential technical choice the user likely cannot fully assess** (licence, framework, storage engine, protocol, architecture pattern), do not ask open-endedly — the user cannot answer well about trade-offs they don't know. Instead:

1. **Enumerate the real options.**
2. **Present a grounded trade-off analysis.** Ground it: verify or cite when feasible, mark confidence, never present pattern-matched plausibility as fact. By hypothesis the user cannot catch a wrong trade-off, so an unsourced analysis here is *actively harmful*, not merely unhelpful.
3. **Give a clearly-marked recommendation with its reasoning exposed** — transparent and contestable, not an oracle. Lead with the trade-offs so the user can add context the model lacks.

**Deliver this through `AskUserQuestion` when available:** each option becomes a labelled choice, its trade-off the description, and the recommended one is marked `(Recommended)` and placed first — the user picks (or chooses *Other*). Where the host lacks `AskUserQuestion`, fall back to the same options + recommendation in prose. The substance is identical either way.

Trigger only for consequential + low-user-visibility choices. Trivial or pure-preference forks ("which of these two files?") get a plain question — a trade-off dissertation on a trivial choice is ceremony, not rigour.

## Step 3 — Assemble the prompt

Structure (9 fields). Drop fields that are trivially unused for this specific ask. Include Examples only when they meaningfully guide execution.

```markdown
# <goal-one-liner>

## Goal
<one sentence — the outcome, not the method>

## Context
<prior state, constraints, relevant files, why this matters now>

## Inputs
<concrete files to read, info to pull, references, commit hashes>

## Expected output
<format (prose / bullet / table / code / diff), destination (chat / file / commit), length>

## Scope
**IN**: <what to do>
**OUT**: <what NOT to do>

## Constraints
<negative prompting: what NOT to do; rules to respect (git safety, no speculative changes, no destructive ops, English for artefacts, etc.); escalation triggers — consequential forks the executor must not resolve alone (in-session -> ask; auto/subagent -> safest reversible option or defer the branch, then flag in the report; never block, never silently guess)>

## Success criteria
<how the user verifies it worked — acceptance checks, tests that would tell them "this worked">

## Open assumptions
<what is being assumed but not verified, and what the executor should do if an assumption proves false — e.g. "assuming the DB is empty; if not, stop and confirm". The confidence % lives in the saved file's frontmatter, not here.>

## Examples (optional, omit if not useful)
<concrete illustrations: sample inputs, example outputs, edge cases to cover>
```

Field rules:

- Plain English, always. Conversation may be in any language; the persisted prompt is in English (or your artefact-language convention).
- Drop fields that are trivial. Simple "explain X" doesn't need Success criteria or Examples.
- Examples only if they meaningfully guide execution — a 4-word prompt doesn't need examples; a complex refactor does.
- Keep the prompt concise: if it's >500 words, it's probably trying to do too many things; consider splitting into two `/promptize` invocations.

## Step 4 — Approval + execution mode

Show the prompt in a code block (fenced Markdown). Then ask:

> Confidence: <N>%. Ready to execute?
>
> **Execution mode**:
> - **in-session** (default) — execute now in this conversation; you see every tool call and intermediate reasoning.
> - **subagent** — spawn a fresh Claude with this prompt as its task, isolated context, returns one consolidated report to this session. Choose when you want to avoid polluting the current conversation's context (e.g. long research, big audit, exploratory refactor). *Available only where the host agent has a subagent/Task primitive (e.g. Claude Code's `Agent` tool); elsewhere only in-session is offered.*
>
> **The confidence bar is asymmetric by mode:**
> - **in-session** may proceed below 95% if the user authorises it — they are watching and can correct live (document the gap in *Open assumptions*).
> - **subagent requires the full ≥95%** and a self-sufficient brief — there is no live correction once it runs isolated, so sub-threshold work is not allowed here. Below 95%? Clarify more, or run in-session.
>
> Say "execute" or "execute in subagent" to proceed, or adjust the prompt first.

If the user refines the prompt, iterate Step 3 → Step 4 until approval.

## Step 5 — Save + execute

On explicit approval:

### 5a — Save to the prompts library

1. Derive a slug from the Goal sentence — lowercase, kebab-case, first 5-7 meaningful words, strip articles.
   - Example: Goal "Audit my settings.json for risks" → slug `audit-settings-json-for-risks`.
2. Filename: `~/.claude/prompts/YYYY-MM-DD-<slug>.md` (today's date, UTC or local — match the session).
3. If a file with that exact name already exists, append `-2`, `-3`, etc.
4. File content:

```markdown
---
date: <YYYY-MM-DD>
execution_mode: in-session | subagent
confidence_at_approval: <N>
approval_timestamp: <YYYY-MM-DD HH:MM>
iteration_count: <N>
status: approved
goal_slug: <slug>
---

# <goal-one-liner>

## Goal
...

## Context
...

(...the 9 fields as approved...)
```

5. Use `Write` to save.
6. Confirm to the user: "Saved to `~/.claude/prompts/<filename>.md`."

### 5b — Execute per the chosen mode

**Default execution behaviour (touchpoint 3 — agent forks).** On an unanticipated, *consequential* fork the prompt does not cover (irreversible or materially outcome-changing — never trivial doubts), behaviour is mode-aware and the executor **never silently guesses**:

- **In-session:** pause and ask — you are present, it is cheap.
- **Auto / subagent (unattended):** **never block the run.** Take the safest reversible option; if the action is irreversible with no safe default, defer just that branch (skip it, finish the rest). Record every such fork — what it hit, what it did, and why — and surface them in the final report.

This keeps fire-and-forget intact (the run completes) while leaving an audit trail of judgement calls instead of silent guesses — governed autonomy. A populated *Constraints* escalation trigger makes the criteria task-specific.

- **In-session**: treat the approved prompt as the new task instruction. Start executing, tool-calling, delivering. The conversation continues naturally — this skill's job ends here; standard conversation resumes.
- **Subagent** — *capability-gated:* this needs a subagent/Task primitive in the host agent (e.g. Claude Code's `Agent` tool). **If the host has none, do not fail — run the task in-session and tell the user subagent mode isn't available here.** When available, invoke the Agent tool with:
  - `subagent_type`: pick the best match for the task (`general-purpose` by default, `Explore` if the task is codebase research-heavy, `Plan` if the task is design-only)
  - `description`: short label like "execute promptized task: <goal>"
  - `prompt`: the FULL prompt text (everything inside the saved file, minus the YAML frontmatter)
  - **Scope its permissions to the task** where the harness allows (read-only for research/audit; no destructive ops unless the task explicitly needs them) — so touchpoint 3's "never act irreversibly on a guess" is *enforced*, not just instructed.
  - Wait for the subagent's return, deliver its report to the user in the main session.

**Before declaring the task done (touchpoint 4):** verify the output against the *Success criteria* field; if it falls short, fix the gap or report it — never declare complete on work you haven't checked against the bar you set. (This counters *agentic laziness*; it does not fully cure an agent's bias toward its own output — that needs an independent reviewer, which is out of scope.)

### 5c — Optional post-execution metadata update

After execution completes (whichever mode), optionally update the saved prompt file's status to `executed` (or `executed-with-issues` if something went wrong). Use `Edit` to change the `status:` line in the frontmatter.

This is best-effort — if the update fails (e.g. the session ends before execution completes), the file keeps `status: approved`, which is still useful.

The skill ends after delivery. Subsequent conversation with the user proceeds normally — no ceremony.

---

## Canonical field reference

**Goal** — one sentence. What outcome the user wants. Avoid method in the Goal; leave method to Claude.

**Context** — state, constraints, prior decisions, files the work depends on. Why this matters now. If this section is empty, ask whether the request is truly context-free or if you're missing something.

**Inputs** — concrete: file paths, commit hashes, URLs, prior docs. What Claude must read before starting. Reduces guessing.

**Expected output** — format (prose / bullets / table / code / diff / commit), destination (chat response / a specific file / a commit / an email), length target ("<500 words", "under 5 bullets", "one diff").

**Scope** — two lists. IN = what's in bounds. OUT = explicit non-goals. This is the single biggest defence against scope creep. If the user can't enumerate OUT, clarification is needed.

**Constraints** — negative prompting. What NOT to do. Reference existing rules (git safety, no speculative changes, no destructive ops, English for artefacts). Link to the relevant rule when applicable. Include **escalation triggers** here — the consequential forks the executor must not resolve on its own (touchpoint 3). Behaviour is mode-aware: in-session it asks; in auto/subagent mode it takes the safest reversible option or defers that branch and flags it in the final report — never blocking an unattended run, never guessing silently.

**Success criteria** — how the user verifies. Acceptance checks. A test that would tell the user "this worked". Often this is "I review the output and it matches my intent" — that's fine, but more specific is better.

**Open assumptions** (a.k.a. known unknowns) — the assumptions the prompt carries unverified, plus what the executor should do if one proves false (e.g. "assuming the DB is empty; if not, stop and confirm"). This is where the risk of proceeding below 95% is transferred in the open. The confidence % itself lives in the saved file's frontmatter (`confidence_at_approval`) — a number isn't actionable for the executor; the assumptions are.

**Examples** (optional) — concrete illustrations. Sample inputs, example outputs, edge cases. Include only if meaningfully guides execution. The user and Claude can both propose examples; either can refine before execute.

---

## Saving and retrieval

- Prompts live at `~/.claude/prompts/`. Versioned (e.g. committed to your dotfiles/config repo) — a history of every approved structured prompt.
- Filename pattern: `YYYY-MM-DD-<slug>.md`.
- Metadata frontmatter at top of each saved file.

To reuse a past prompt later:
1. Read `~/.claude/prompts/<filename>.md`.
2. Copy the body into a new `/promptize` invocation, adjust Context/Inputs for the new case.
3. If a pattern emerges (same prompt used 3+ times), consider promoting it to a dedicated skill instead of a prompt.

Future refinement (not in MVP): a `/prompts list` helper to search the library by slug or date.

---

## Portability notes

- **User-level**, works in every project. No project-specific assumptions.
- Claude may still invoke other skills/subagents as part of executing the promptized task — `/promptize` is the wrapper, not a replacement for specialised tools.
- English for saved prompts (or your artefact-language convention). Conversation remains in the user's preferred language.
