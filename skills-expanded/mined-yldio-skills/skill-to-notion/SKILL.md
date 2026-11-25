---
name: skill-to-notion
description: Turns a workshop board (a task broken into six blocks, pasted as rough text from Miro) into a finished SKILL.md and a matching Notion skill page in the YLD format. Use when a team has broken a recurring task down and wants it written up as a skill.
---

# Create New Skills Notion Page

## Goal

Turn a workshop board (a task broken into six blocks) into a finished YLD skill: a
SKILL.md file, and a Notion skill page that documents it, formatted and ready to
paste under one of the team's skill types.

## The input

The person pastes the contents of the Break Down frame from the Miro board, plus
anything from the Build frame if a test has been run. It arrives as rough text: one
line per sticky, sometimes with author names, duplicates, or half-sentences. Expect
these headings, in any order:

- Task (the name of the recurring task)
- Owner
- Team (Design, Marketing, Client Partner, or General)
- 1. Input: what goes in before any work starts
- 2. Output: what "done" looks like; may have a "today" version (text) and an "end
  state" version (slide template, Notion page, connector)
- 3. Steps: what we do, in order
- 4. Decisions: judgement calls, each ideally with a default
- 5. Review point: what a person must confirm before it's done
- 6. What could go wrong: bad inputs, edge cases, things it must never do
- Optional: Later (templates, connectors, datasets to wire up), Test input, Test
  output, What we noticed

Read all of it first. Merge duplicate stickies. Ignore author names. Keep the
team's own words wherever they are clear; they know the task and you don't.

## Naming

Skill names are a short kebab-case description of what the skill does, with no
team prefix, for example `eow-summary` or `campaign-plan`. The name is the slash
command, the SKILL.md `name`, and the folder name in the `yldio/skills`
repository. Ask the person to check that no other YLD skill already uses it.

The team decides which skill suite the skill goes in:

| Team | Suite | Folder |
|---|---|---|
| Design | Design (Skill Suite) | `plugins/yld-design/skills/` |
| Marketing | Marketing (Skill Suite) | `plugins/yld-marketing/skills/` |
| Client Partner | Client Partners (Skill Suite) | `plugins/yld-cp/skills/` |
| Engineering | Engineering (Skill Suite) | `plugins/yld-engineering/skills/` |
| Any team | General (Skill Suite) | `plugins/yld-general/skills/` |

If the board gives no team, suggest one and ask the person to confirm.

## The skill file

Produce a SKILL.md in this exact shape. Plain language, British English, short
sentences, no code, under 450 words.

````markdown
---
name: <kebab-case-name>
description: <one sentence: what it does and when to use it, written so Claude knows when to apply it>
---

# <Title Case label>

## When to use
<from Task and Input: the trigger, in one or two lines>

## You need
<from Input: a bullet per item the user must paste, attach or point to>

## Steps
<from Steps: numbered, one action each, in order. Add a first step "State what the input covers and what it doesn't" if the task involves data. Add a last step "List anything you were unsure about" always.>

## Decisions and defaults
<from Decisions: one bullet each, "<decision>. Default: <default>." Where the board gives no default, write "Default: ask before proceeding.">

## Output
<from Output: the shape of today's text output. Format, length, sections, order.>

## Never do this
<from What could go wrong: one bullet each, phrased as a rule. Always include: do not invent numbers, names, quotes or trends; if the input doesn't support it, say so and leave a placeholder. For anything with personal data: never output anything that identifies an individual; aggregates and role-level findings only.>

## Before it goes out
<from Review point: a checklist a person runs. End with: "This output is a draft. A person signs it.">

## Later
<from Output end state and Later: the template, connector or dataset this skill will use once wired up. One line each. Omit the section if there is nothing.>
````

## The Notion page

Produce the page in this exact order:

1. Title, in the format `/<slash-command> | <Title Case label>`, for example
   `/linkedin-monthly-report | Monthly LinkedIn Performance Report`. The
   slash command is the SKILL.md `name`.
2. Properties: Ownership, Last Updated
3. What it is, 2 to 3 plain sentences
4. When to reach for it, 1 to 2 lines
5. What AI helps with, in bullets, each with a bold lead-in
6. Tools, which tools and any setup
7. The skill, one copyable block containing the SKILL.md above, unchanged
8. Review before it ships, the human check for this skill's output
9. Sample output, a real example or a placeholder

## How to build it

1. Read the whole board. Identify the Task, the Owner, the Team and the six
   blocks. Note which blocks are thin or empty.
2. Name and title: propose the kebab-case name and a Title Case label
   describing what it does.
3. Write the SKILL.md from the blocks using the mapping above. Do not add steps,
   decisions or rules the team did not say, except the standing ones listed in the
   template (state coverage, list uncertainties, never invent, personal data,
   draft not deliverable).
4. Write the page sections from the same blocks: What it is from Task and Output;
   When to reach for it from When to use; What AI helps with from the Steps the AI
   takes, three bullets at most; Tools from Input and Later (Claude, plus the
   files, exports or connectors named). Keep them short and concrete.
5. Put the SKILL.md into "The skill" as one block, unchanged.
6. Properties: set Ownership from the board's Owner slot. If empty, write
   [owner]. Set Last Updated to today's date.
7. Review before it ships: rewrite the Review point as a concrete check specific
   to this skill's output, and state that the output is a draft, never a
   deliverable on its own.
8. Sample output: if the board has a Test output, summarise it in one or two lines
   and note the test input used. Otherwise leave a one-line placeholder telling
   the owner to paste a real run.
9. Gaps: if a block is empty, a decision has no default, the trigger is unclear,
   or the output has no format, do not invent it. List each under "Gaps to fill",
   naming the block it belongs to, so the team can fix the board.

## Output

Return four copy-ready blocks, then guidance:

1. The page title on its own, in the format `/<command> | <Label>`.
2. The two properties: Ownership and Last Updated.
3. The SKILL.md on its own, in a ```` ```markdown ```` fence, so it can be saved
   as a file.
4. The page body in markdown, in the section order above. The skill (section 7)
   must stay inside its own ```` ```markdown ```` code fence so it copies as one
   unit. If you wrap the body in a fence to make it copyable, the outer fence must
   be longer than the skill's: four backticks outside, three inside. Never flatten
   the skill into the surrounding text or drop its fence.

Then a short "Before you paste" checklist: confirm the name and label, set
ownership and date, confirm the team, add a sample output after the first real
run, resolve anything under "Gaps to fill", and propose the SKILL.md to the
`yldio/skills` repository so it becomes available as a slash command.

## Rules

- Plain language. No hype, no filler. British English.
- Never invent detail to fill a gap. Flag it instead.
- The team's words win. Tidy grammar, keep meaning.
- The skill is always one copyable block with its own ```` ```markdown ```` fence,
  and the SKILL.md and the page's skill block are identical.
- Templates, connectors and datasets go under Later. Do not write steps that
  assume they are wired up.
- No ampersands, no em dashes, no all caps. Title Case for the label, sentence
  case everywhere else.

## Before it goes out

- The generated "What it is" and "When to reach for it" match what the skill
  actually does; the model is inferring intent and can get it slightly wrong.
- The skill block came across intact.
- Nothing was invented to fill a gap; "Gaps to fill" should catch it.

This output is a draft. A person signs it.
