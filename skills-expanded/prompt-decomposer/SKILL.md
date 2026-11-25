---
name: prompt-decomposer
description: Analyze large prompts, system instructions, or runbooks to identify sections extractable as standalone skills, then build them. Use when decomposing a big prompt into skills, extracting skills from instructions, or asked to break a prompt apart.
---

# Prompt Decomposer

Accept a large prompt, system instruction set, or runbook. Identify which sections could become standalone skills, present candidates with rationale, and route approved candidates into the Skill Maker for creation.

## When to use

- You have a long system prompt and want to modularize it into skills
- You inherited a monolithic instruction set and want to break it apart
- You want to audit a prompt for skill-worthy patterns
- You pasted a big block of text and want to know what's reusable

## Workflow

### Phase 1: Intake

Accept one of:
- A pasted prompt (inline text in the chat)
- A file path to a `.md`, `.txt`, or any text file containing instructions
- A directory path containing multiple instruction files

If no input provided, ask:

> "Paste your prompt or give me the file path. I'll analyze it for sections that could become standalone skills."

If the input is under 20 lines, push back:

> "This is pretty short -- it might work better as a single skill. Want me to send it to the Skill Maker instead?"

### Phase 2: Chunk

Segment the prompt into logical sections. Look for boundaries at:
- Heading markers (H1/H2/H3, `##`, bold headers)
- Topic shifts (different task domains or tool contexts)
- Behavioral blocks ("when X, do Y" conditional patterns)
- Distinct workflow sequences (numbered steps with a clear start/end)
- Tool-specific sections (sections scoped to one tool, API, or platform)

Ignore:
- Preamble / personality / tone directives (these are rules, not skills)
- Boilerplate (license text, version headers)

Present a numbered summary:

> "I found **N logical sections** in your prompt:"
>
> 1. **[short label]** (lines ~X-Y) -- one-sentence summary
> 2. **[short label]** (lines ~X-Y) -- one-sentence summary
> ...

Ask: "Does this breakdown look right, or should I split/merge any sections?"

Wait for confirmation before evaluating.

### Phase 3: Evaluate

Load the wiki knowledge needed for evaluation. All paths below are relative to the skill-factory root directory.

Read the file `wiki/INDEX.md`, then read:
- `wiki/research/anatomy-of-a-good-skill.md`
- `wiki/concepts/skill-discovery.md`
- `wiki/concepts/token-budget.md`
- `wiki/research/cursorrules-vs-skills.md`
- `wiki/research/anti-patterns.md`

Also read the quality spec: `SKILL_SPEC.md`.

Score each chunk against six criteria:

| Criterion | Question |
|-----------|----------|
| **Distinct trigger** | Could a user naturally ask for this in isolation? |
| **Repeatable task** | Is this a workflow with steps, not just a fact or opinion? |
| **Delta from baseline** | Would an agent get this wrong without explicit instructions? |
| **Self-contained** | Can it run without the rest of the prompt? |
| **Focused scope** | Is it one task, not three bundled together? |
| **Sibling boundary** | Which adjacent skill owns nearby prompts, and what must this candidate not trigger for? |

A chunk that passes 5-6 criteria is a **good candidate**. 3-4 is **marginal**. 0-2 is **not a skill**.

### Phase 4: Present candidates

Show a results table:

> **Skill candidates from your prompt:**
>
> | # | Suggested name | What it does | Verdict | Rationale |
> |---|----------------|-------------|---------|-----------|
> | 1 | `deploy-staging` | Run staging deploys with smoke tests | GOOD CANDIDATE | Distinct trigger, repeatable workflow, agent skips smoke tests without it |
> | 2 | `api-error-handling` | Retry and fallback patterns for our API | MARGINAL | Useful gotchas but no clear trigger -- better as a section in an existing skill |
> | 3 | _(tone/personality)_ | Sets voice and style | NOT A SKILL | Rules, not a skill -- belongs in `.cursorrules` or `AGENTS.md` |

After the table, flag special categories:

**Merge candidates**: "Sections 4 and 7 both cover database operations. These should be one skill, not two."

**Sibling candidates**: "Sections 2 and 5 are independently useful but adjacent. Keep separate skills and add explicit cross-routing negatives; do not assume automatic subskill loading."

**Gotchas, not skills**: "Section 3 has useful facts about your API quirks, but it's not a workflow. Consider adding these as a gotchas section to an existing skill."

**Rules, not skills**: "Section 1 sets coding style and tone. This belongs in `.cursorrules` or `AGENTS.md` as an always-on rule, not an on-demand skill."

Present a recommendation:

> "I recommend building **N skills** from this prompt: [list]. Want to proceed with all of them, pick specific ones, or adjust?"

Wait for the user's selection.

### Concrete decomposition example

Input sections:

```text
## Release
Build the package, publish it, and verify the registry version.

## Incident response
Collect logs, classify severity, and open the incident timeline.

## Tone
Use short sentences and a friendly voice.
```

Expected classification:

```text
release-package     GOOD CANDIDATE  independent trigger and verifiable workflow
incident-response   GOOD CANDIDATE  separate trigger, tools, and outcome
tone                NOT A SKILL     always-on writing preference; move to AGENTS.md
```

The two candidates are siblings only if a parent operations router genuinely
needs to select between them. Otherwise install them as independent skills.

### Phase 5: Build selected skills

Ask the user's preferred pace:

> **How would you like to build these?**
>
> A) **One at a time** -- Walk through the Skill Maker for each, with full diagnostic questions and design review
>
> B) **Batch draft** -- Generate all skill drafts at once using the authoring workflow, then review together
>
> RECOMMENDATION: A if you have 1-3 candidates. B if you have 4+.

**Route A (one at a time):** For each approved candidate:
1. Read `skill-maker/SKILL.md`
2. Pre-fill Phase 1 (INTAKE) with the extracted chunk text and the suggested name/description
3. Start at Phase 2 (DIAGNOSE) since the idea is already concrete
4. Follow the full Skill Maker flow through validation and test plan

**Route B (batch draft):** For each approved candidate:
1. Read `authoring/SKILL.md`
2. Pass the extracted chunk as a plain-English description
3. Follow the authoring workflow (wiki lookup, gap analysis, draft, validate)
4. Collect all drafts, then present them together for review
5. Add a one-hop sibling routing map when candidates share a broad parent domain
6. Keep structural validation, eval-definition presence, and executed behavioral results as separate statuses

After building, ask: "Ready to move to the next candidate, or want to revise this one?"

### Phase 6: Residual check

After all selected skills are built, evaluate what remains:

> "Here's what happened to your original prompt:"
>
> - **Extracted as skills**: [list with paths]
> - **Flagged as rules**: [list -- suggest adding to `.cursorrules` or `AGENTS.md`]
> - **Dropped**: [list -- general knowledge the agent already knows]
> - **Kept as-is**: [list -- sections that don't fit anywhere else]
> - **Evidence status**: [per skill: structural result, eval definition, executed/not-run behavioral result]

If rule-worthy content was identified, offer to write it:

> "Want me to add the flagged rules to your `.cursorrules` or `AGENTS.md`?"

## Anti-shattering rules

<HARD-GATE>
Do NOT suggest more than 7 skills from a single prompt. If the initial chunking produces more than 7 candidates, merge related sections before presenting. A monolithic prompt should become 2-5 focused skills, not 15 micro-skills.
</HARD-GATE>

Grouping heuristics:
- Chunks that reference the same tool or API belong together
- Chunks that form sequential steps of one workflow belong together
- Chunks that share the same trigger phrase belong together
- When in doubt, merge and let the Skill Maker split later if needed

## Anti-inflation rules

Not every section of a prompt is a skill. Reject chunks that are:
- **General knowledge**: "Use descriptive variable names" -- the agent already knows this
- **Personality directives**: "Use a concise, friendly tone" -- this is a rule, not a skill
- **One-shot facts**: "Our API key is in .env" -- this is a gotcha for an existing skill
- **Vague aspirations**: "Write good code" -- no actionable workflow

When rejecting, explain where the content belongs instead.

## Source and pointer preservation

When extracting from an external runbook, retain its revision, license, and
provenance. Source text does not authorize running its scripts or changing host
configuration. Keep every shared invariant reachable, and attach a distinct
trigger condition to each disclosed reference; splitting by headings alone can
hide required steps. Read `wiki/concepts/skill-supply-chain.md` before adopting
bundled scripts or hooks.

## Dependency awareness

Some prompt sections only make sense together. Before presenting candidates, check:
- Does chunk A reference variables/concepts defined in chunk B?
- Does chunk A assume chunk B has already run?
- Would chunk A break if chunk B were removed?

If dependencies exist, flag them: "Sections 2 and 5 have a dependency -- section 5 assumes the output of section 2. Consider keeping them as one skill or documenting the dependency."

Agent Skills has no native automatic subskill dependency loader. If independent
siblings remain, every router must name the selected skill explicitly, include a
fallback when it is absent, and test adjacent negative routing.

## Gotchas

- Heading boundaries are hints, not proof of independent activation. Sequential
  sections with shared state usually belong in one skill.
- Useful facts and team preferences must be retained in references, rules, or
  memory instead of discarded merely because they are not skills.
- A sibling map is executable routing documentation, not a directory hierarchy;
  test both sibling ownership and the fallback path.
