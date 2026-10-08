---
name: compounded-author
description: Use this skill when you have just completed a non-trivial task (more than 3 tool calls, novel approach, recovery from a dead end) and are considering whether to save the procedure as a reusable skill via compounded; OR in RULE MODE when the user corrected your approach and the correction encodes a generalizable behavioral rule. Also use when the user explicitly asks you to "save this as a skill", "remember how to do this", or similar.
---

# Authoring a Skill (compounded)

You have just finished a task. You are deciding whether to propose a new skill.

There are two capture modes:

- **Procedure mode** — a successful multi-step task worth saving as a replayable procedure. Sections 1-2 apply.
- **Rule mode** — the user corrected you, and the correction encodes a generalizable behavioral rule. Section 1R applies instead of sections 1-2.

**Default to NOT proposing.** Skills you propose pollute the `.proposed/` queue, cost the user a verifier inference call on the next applicable task, and dilute the trust signal if they fail. Propose only when the capture clears the relevant bar.

**Always get user approval before saving.** Whichever mode you are in, you MUST ask the user to approve the proposal via AskUserQuestion before calling `skill_propose.py`. See section 2.5.

## 0. Did the auto-proposer nudge you?

Nudges arrive two ways:

- **Rule mode** — your turn was interrupted with a `[compounded] Correction detected ...` instruction (the Stop hook blocked the stop and fed it to you). Apply section 1R.
- **Procedure mode** — the user saw a `[compounded] Auto-propose threshold reached ...` message and relayed it (e.g. "save this as a skill"). Apply sections 1-2.

Either marker is a *suggestion*, not an instruction. **Still apply the relevant qualifying bar.** The auto-proposer is conservative but it doesn't know whether the capture is generalizable. Many high-signal turns are one-off chores, and many corrections are one-off taste calls.

If you decide not to propose despite the nudge, that's fine — say nothing to the user and move on. Don't apologize for not proposing.

## 1R. Rule mode

The user corrected your approach (e.g. "no, web-search for the latest model first instead of relying on training data"). The lesson is the delta between three things:

1. **What the user asked** (their original intent)
2. **What you did** (the mistake)
3. **How they corrected you** (the rule)

Propose a rule only when **all three** are true:

1. **Generalizable.** The correction implies behavior for a *class* of future requests, not just this one. "Use port 3001 in this repo" is a note (USER.md), not a rule. "When I ask for the latest version of anything, search the web before choosing" is a rule.
2. **Clear trigger.** You can state, in one sentence, the condition under which the rule should fire. That sentence becomes the skill's `description` — it is how future sessions match it.
3. **Not already covered.** Check existing skills (`/compounded:status`) and the user's CLAUDE.md/USER.md. Don't duplicate.

The procedure bar (section 1) does NOT apply in rule mode — rules are not procedures and don't need >3 tool calls or a numbered replay.

### The shape of a rule SKILL.md

```markdown
---
name: <kebab-case-name>
description: <the trigger condition, one sentence — "When the user asks to use the latest/newest model, library, or API version, web-search current options before choosing.">
kind: rule
---

# <Title Case Name>

## When this fires

<2-3 concrete trigger examples, phrased the way the user actually talks.>

## Rule

<The behavioral rule, imperative, 1-3 sentences. What to do INSTEAD of the default behavior.>

## Why (origin)

<Dated, one paragraph: what the user asked, what went wrong, how they corrected it. E.g.: "2026-06-10: user asked for Gemini's latest embedding model; an older model was chosen from training data; user corrected: web-search first, then present current options.">

## Example

<One before/after: the request, the wrong default, the correct behavior under this rule.>
```

The `kind: rule` frontmatter field matters: the verifier judges rules differently (generalizability instead of procedure replay), and rule proposals are exempt from the 30-day stale sweep (their trigger may legitimately not recur within 30 days).

The `--verification-hint` for a rule restates the trigger: e.g. "next time the user asks for the latest or best-available model or library version, this rule should cause a web search before choosing".

## 1. The qualifying bar

Propose only when **all five** are true:

1. **More than 3 tool calls.** Trivial tasks do not become skills.
2. **A non-obvious step.** If a competent agent would do this without a skill, do not write one. Skills exist for things that are easy to get wrong.
3. **The procedure abstracted to inputs.** If your steps are tied to specific paths, file names, or values from this session, you are writing notes, not a skill. Notes belong in MEMORY.md or USER.md.
4. **You actually finished.** A skill that captures a half-solution is worse than no skill — it teaches the wrong thing.
5. **It is not redundant.** Search existing skills first via `/compounded:status`. If there is overlap, consider extending an existing skill (via the user) rather than authoring a new one.

If any of these fail, stop. Do not propose.

## 2. The shape of a good proposed SKILL.md

Use this exact shape. The verifier subagent reads this file later and replays it; ambiguity causes false rejections.

```markdown
---
name: <kebab-case-name>
description: <one sentence describing when this skill should activate, written so a verifier can decide if a future task matches>
---

# <Title Case Name>

## When to use

<2-3 bullet points describing the trigger conditions. Concrete, not abstract.>

## Inputs

<List of inputs the skill expects, in plain English. e.g.: "the path to a Node.js project", "a function name to refactor".>

## Procedure

<Numbered steps. Each step is a single concrete action. Use file paths in angle brackets like `<project-root>/package.json`. Avoid pronouns like "it" or "this" — be explicit about what you mean.>

1. ...
2. ...
3. ...

## Pitfalls

<Failure modes you encountered or anticipate. Each pitfall pairs a symptom with a fix.>

## Verification

<How a future invocation can confirm it worked. Concrete check: tests pass, file exists, value matches, etc.>
```

## 2.5. User approval — REQUIRED before saving

Before calling `skill_propose.py`, present the proposal to the user with the AskUserQuestion tool. Show:

- The skill **name** and its **trigger** (the `description` line)
- In rule mode: the **rule** itself, verbatim
- In procedure mode: a one-line summary of what the procedure does

Offer options like "Save it" / "Don't save". If the user picks "Don't save" (or edits the rule via Other), respect that — discard or revise accordingly and do not propose. **Never call `skill_propose.py` without an explicit approval in this turn.** If AskUserQuestion is unavailable in your environment, state the proposal in plain text and wait for the user's reply before proposing.

## 3. Calling skill_propose

Once the user has approved, invoke the compounded proposal mechanism via the `Bash` tool with `--approved`. **The user's approval is the only gate** — approved skills save directly to `.verified/` and are active immediately; there is no verifier round-trip. Resolve the installed plugin path first (the version segment changes across updates):

```bash
PROPOSE=$(ls ~/.claude/plugins/cache/*/compounded/*/scripts/skill_propose.py 2>/dev/null | sort -V | tail -1)
python3 "$PROPOSE" \
  --name "<kebab-case-name>" \
  --approved \
  --verification-hint "<one-sentence description of when a future task should apply this skill>"
```

(Omit `--approved` only when staging something the user has NOT approved — it then goes to `.proposed/` and waits for verification. With the approval gate in section 2.5, that path is rare.)

When you run that command, write the SKILL.md content to stdin via a heredoc so it is captured exactly. Example invocation:

```bash
python3 "$PROPOSE" \
  --name "express-to-fastify" \
  --verification-hint "next time the user asks to migrate an Express server to Fastify, this procedure should reproduce successfully" <<'EOF'
---
name: express-to-fastify
description: Migrate an Express.js HTTP server to Fastify, preserving routes and middleware semantics.
---

# Express to Fastify Migration

## When to use

- The user asks to migrate or convert an Express app to Fastify
- The project has an Express dependency in package.json
- Routes are defined via `app.get`, `app.post`, etc.

[... rest of SKILL.md ...]
EOF
```

The script will:

1. Validate the frontmatter and structure
2. Run a security scan against the content (rejects prompt injection patterns)
3. Write to `~/.claude/compounded/skills/.proposed/<name>/SKILL.md`
4. Record a verification hint to the trust database
5. Return a one-line confirmation, or an error explaining why the proposal was rejected

## 4. The verification hint

The hint is critical. It is the criterion that the verifier subagent uses to decide whether a future task qualifies for replay.

**Good hints:**

- "next time the user asks to migrate an Express server to Fastify, this procedure should reproduce successfully"
- "next time the user asks to add a new resolver to this Apollo GraphQL schema, this procedure should produce the resolver, type definition, and test in one pass"
- "next time the user asks to convert a class component to a functional component with hooks, this procedure should preserve all state and side effects"

**Bad hints:**

- "use this for refactoring" (too vague — what kind of refactoring?)
- "any time the user asks for help" (matches every task; will trigger spurious verifications)
- "see procedure" (gives the verifier nothing to check against)

## 5. After saving

After `skill_propose.py` returns success:

1. Tell the user briefly: "Saved `<name>` — it's active now (rules are injected at session start) and earns trust with each clean use; a correction demotes it."
2. Do NOT save another related skill in the same session unless the lessons are genuinely orthogonal. Multiple saves in one session usually indicate it should have been one skill.

## 6. Pitfalls

- **Proposing notes as skills.** "Remember that user prefers tabs" is a note (USER.md). "How to convert tabs to spaces in this codebase" is a procedure skill. "When the user asks for the latest version of anything, web-search before choosing" is a rule skill. The line: procedures are *replayable steps*, rules are *triggered behaviors*, notes are *facts with no trigger*.
- **Hint too narrow.** "Next time the user runs `npm test` on this exact repo" — the verifier will never trigger because the next session is on a different repo.
- **Hint too broad.** "Next time the user does anything with TypeScript" — the verifier will trigger on every TS task and waste tokens on irrelevant verifications.
- **Forgetting to abstract.** If your SKILL.md says "edit `~/projects/myapp/src/server.ts` line 47", it cannot be replayed elsewhere. Use placeholders like `<server-file>` and explain how to find them.
- **Authoring during the same task you would test against.** The first verification must be a *fresh* applicable task, not a retrospective check on the task that produced the skill. The hook respects this.

## 7. What success looks like

A skill you propose today shows up in `.proposed/`. Days or weeks later, a similar task arrives, the verifier runs, the skill graduates to `.verified`, and now Claude can invoke it by name. After 3 successful uses, it auto-loads on relevant tasks. After 10, it runs without asking. **You are training your replacement, one verified skill at a time.**
