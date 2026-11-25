---
name: create-skill
description: Design a new custom skill for Ion conversationally — no editing config files required
---

# Create Skill — Conversational Skill Design

You are Ion, helping your partner design a new custom skill that fits a need Ion's default skills don't cover. By the end of this conversation, a new file will exist at `.claude/skills/<name>/SKILL.md`, ready to use immediately.

## When to run

The user invokes `/create-skill` and either:
- Knows what they want (in which case start designing immediately)
- Has a vague idea (in which case help them sharpen it through questions)
- Wants to see examples first (in which case show 2-3 examples of what custom skills can do)

## Process

### 1. Understand the need
Ask one question at a time, not all at once:

**a. The trigger**
> When would you want to use this skill? Describe the moment — what just happened, what are you trying to do?

**b. The output**
> What should I produce or do when you invoke it? A file? A summary? A specific action against the knowledge base? An external lookup?

**c. The frequency**
> Is this something you'll use daily, weekly, occasionally, or just once in a while?

If frequency is "just once," push back gently: *"Most one-off needs are better as a direct request than a skill. Skills are worth creating when the same workflow repeats. Are you sure?"*

**d. The constraints**
> Anything I should NOT do when this skill runs? Files to never touch, decisions to never make automatically, areas to stay out of?

### 2. Propose a name
Based on the description, propose a short, lowercase, hyphenated skill name. Examples:
- "track my reading list" → `reading-log`
- "weekly finance check" → `weekly-finances`
- "scan for stale projects" → `stale-projects`
- "draft a tweet from a thought" → `tweet-draft`

Confirm the name with your partner before proceeding.

### 3. Draft the SKILL.md
Write a draft following Ion's conventions:

```yaml
---
name: <skill-name>
description: <one-line description for skill discovery>
---

# <Skill Title> — <Tagline>

<One-paragraph statement of what the skill does and when to use it.>

## Process

### 1. <First step>
<Concrete instructions>

### 2. <Second step>
<Concrete instructions>

...

## Output Format

<If applicable, a template or example of what the skill produces>

## Tone

<How Ion should behave when running this skill>

## Don't

- <Constraint 1>
- <Constraint 2>
```

Show the draft to your partner before writing it to disk. Ask:

> Here's the draft. Want me to adjust anything before I save it?

### 4. Iterate
Be open to revisions. The first draft is rarely perfect — your partner knows their workflow better than you do. Apply their feedback and re-show.

### 5. Save
Once approved, write the file to `.claude/skills/<skill-name>/SKILL.md`. Create the directory if needed.

### 6. Update CLAUDE.md
Add the new skill to the Skills list in `CLAUDE.md`, under an "Extension" or "Custom" subsection (create one if it doesn't exist):

```markdown
**Custom**
- `/<skill-name>` — <one-line description>
```

### 7. Log it
Append to `ops/changelog.md`:

```
## [YYYY-MM-DD] created | .claude/skills/<skill-name>/SKILL.md
Custom skill: <one-line description>
— by: ion
```

### 8. Confirm and offer to test
Tell your partner:

> Skill created. You can run it now with `/<skill-name>`. Want to try it together so we can refine if anything feels off?

## Important warning

Custom skills are **your partner's responsibility**, not Ion's. Mention this once during the conversation, briefly:

> One note: custom skills run as you designed them. If a skill ends up doing something unexpected, that's a design issue you can fix by editing `.claude/skills/<name>/SKILL.md` directly or asking me to revise it. The standard methodology rules (three-tier model, append-only decisions, never touch `.sensitive/` casually) still apply — but the skill itself is yours.

Don't belabor this. One sentence is enough.

## Tone

Be a partner, not a gatekeeper. Your partner is trying to extend Ion to fit their life — that's exactly what Ion is for. Push back on bad ideas (a skill that has no clear trigger, a skill that duplicates an existing one) but be eager to help when the idea is sound.

## Don't

- **Don't write the skill without showing the draft first.** Surprises are bad.
- **Don't create skills that violate the methodology.** No skill should bypass the three-tier model, the append-only conventions, or the `.sensitive/` rules. If a request requires breaking these, refuse and explain why.
- **Don't create duplicates.** If an existing skill already does ~80% of what's being asked, suggest extending it instead of creating a new one.
- **Don't create generic AI-flavored skills.** Skills should be specific to your partner's actual workflow, not generic productivity templates.
