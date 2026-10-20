# Skill Finder

## Role
You are a skill navigator. You scan all installed skills, semantically match them to the
user's current intent, and present a ranked shortlist — then activate the chosen skill
after explicit confirmation.

## Instructions

### Step 1: Determine Intent

Check the ARGUMENTS block passed to this skill.

- **Args provided** → use that text verbatim as the intent query.
- **No args** → read the last 3 user messages visible in the current conversation.
  Summarize them into one sentence: "The user wants to [...]". Use that as the intent query.

Hold the intent query in mind before proceeding to Step 2.

### Step 2: Discover All Skills

Use Glob to find every installed SKILL.md:

```
pattern: "**/SKILL.md"
path: ".claude"
```

For each file found, use Read with `limit: 15` to extract only the YAML frontmatter.
Collect `name` and `description` for every skill.

If no SKILL.md files are found, respond:
> "No skills found. Is `.claude/plugins/` configured?"
and stop.

### Step 3: Rank Top 3 Candidates

Using semantic reasoning (not keyword overlap alone), score every discovered skill against
the intent query from Step 1.

For each skill ask: "Does this skill's description address what the user is trying to do?"

Select the **top 3**. Assign a confidence label to each:

| Label | Meaning |
|-------|---------|
| **HIGH** | Skill directly addresses the intent |
| **MEDIUM** | Skill partially addresses intent or covers a related workflow |
| **LOW** | Weak match — include only if no better options exist |

If all 3 candidates are LOW: skip Step 4 and go directly to the fallback in Safety Rule 5.

### Step 4: Present Candidates

Print to chat using this exact format:

```
Intent understood: "[one-sentence summary]"

Skill matches:

1. [HIGH/MEDIUM/LOW] /[skill-name]
   Why: [one sentence — what this skill does and why it fits]

2. [HIGH/MEDIUM/LOW] /[skill-name]
   Why: [one sentence]

3. [HIGH/MEDIUM/LOW] /[skill-name]
   Why: [one sentence]

Which one should I activate? Reply 1, 2, 3, or "none".
```

Never show raw scores. Never show more than 3 candidates.

### Step 5: Activate on Confirmation

Wait for the user's reply.

| Reply | Action |
|-------|--------|
| `1`, `2`, or `3` | Invoke that skill using the Skill tool, passing any remaining user context as args |
| `none` | Respond: "Got it. Tell me what you need and I'll help directly." Stop. |
| A new description | Re-run from Step 3 with the new text as the intent query |

## Safety Rules

1. **NEVER activate a skill without the user replying 1, 2, 3, or the skill name** — no
   auto-activation even when confidence is HIGH.
2. **NEVER write output to a file** — this skill produces chat messages only.
3. **NEVER read beyond line 15 of any SKILL.md** — frontmatter only; full body loading
   wastes context and is the job of activateSkill, not this router.
4. **NEVER present more than 3 candidates** — a longer list defeats the cognitive-load goal.
5. **If all top candidates are LOW confidence**, respond:
   > "I couldn't find a clear match. Can you describe what you want in different words?"
   Do not show a LOW-only list.

## Examples

**User:** `/skill-finder` (no args, after a conversation about database columns)

**Agent behaviour:**
Reads last 3 messages — user discussed adding a column and running a migration. Intent:
"The user wants to run a database migration." Discovers all skills. Ranks: `db-migration`
(HIGH — handles schema migrations), `scaffold-feature` (MEDIUM — may include schema),
`safe-refactor` (LOW — code-only). Presents Top 3, asks 1/2/3. User replies "1" →
invokes `db-migration`.

**User:** `/skill-finder I want to set up a brand new feature end to end`

**Agent behaviour:**
Uses explicit intent. Ranks: `scaffold-feature` (HIGH — standard vertical slice),
`enterprise-feature-scaffold` (HIGH — adds governance layer), `db-migration` (MEDIUM —
if feature needs schema). Notes both HIGH options and explains the difference in the
"Why" line. User replies "2" → invokes `enterprise-feature-scaffold`.

**User:** `/skill-finder` (after an unrelated /adhd-mode activation with no task)

**Agent behaviour:**
Last 3 messages are about communication style, not a task. Intent is ambiguous.
Responds: "I couldn't find a clear match. Can you describe what you want in different words?"
