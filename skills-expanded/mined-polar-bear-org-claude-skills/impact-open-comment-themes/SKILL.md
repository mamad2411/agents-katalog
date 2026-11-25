---
name: impact-open-comment-themes
description: Turns the open comments from a training survey into themes you can check, producing a code list with definitions, themes with comment counts and an anonymous paraphrase each, and what every theme suggests changing in the programme. Use for "run impact-open-comment-themes", "analyse open comments", "open text survey responses", "thematic analysis of survey comments", "summarise training feedback comments", "what did people write in the survey", "code free text answers", part of the Claude Guide for Training Impact Pack by 90n.
---

# Open Comment Themes

## When To Use
You have three hundred open comments and time to read thirty. The closed items gave you counts; the comments are where people said what was missing, what blocked them and what they would cut, and you need them sorted into themes without losing the awkward ones.

## When Not To Use
Not for figures: use the Before-and-After Results Table. Not for interview notes, which are read case by case in the Success Case Method Write-Up. With a handful of comments, read them all yourself; themes built on very few comments mislead more than they help.

## Inputs
- The open answers, with the question each one answers: upload the survey export as a CSV file, or paste the comments. Add how many people were invited and how many responded.
- The agreed measures or critical behaviours, if you want themes read against them.
If you have none of this, I start from the comments you paste and mark the output as a first draft.

## Approach
This follows thematic analysis in six phases, from Braun and Clarke's 2006 paper "Using thematic analysis in psychology" and the authors' University of Auckland page: familiarise yourself with the dataset, code, generate initial themes, develop and review themes, refine, define and name them, write up. Themes do not sit in the data waiting to be found. A reader builds them, and here the first reader is Claude, so you check a sample before you trust a count. The failure it prevents: the three loudest comments become "learners told us", and the one quiet remark about the tool that never worked is averaged away.

## Workflow
1. Ask three questions at once: which survey question or questions do these comments answer, and how many people were invited and responded; how many comments per theme will you check yourself before trusting the counts (you set it); and is there anything the comments must be read against, such as the agreed measures or critical behaviours?
2. Familiarise: read every comment before labelling any. Record how many there are, from which question, and how many respondents left none. If the export carries names or other identifying columns, I ignore them, never reproduce them, and say the file should be stripped before it is shared.
3. Code: give each comment one or more short labels, each with a one-line definition. Code what was said, not what it probably meant. The code list is part of the output, so you can disagree with it.
4. Generate themes from the codes, then review them against the full set. Every comment is placed in a theme or counted as "unplaced"; nothing is dropped quietly. For each theme I list the comments for your sample check, and you move or rename what I got wrong.
5. Define and name each theme in one sentence, with its count. Keep minority views as their own lines, labelled "minority view", however few comments they hold.
6. Write one paraphrase per theme with names, teams, places and tell-tale details removed. A person named in a comment (a trainer, a manager) becomes a role, and a comment about them is read as a point about the programme, never as a finding about that person. No verbatim quote that could identify its author.
7. End each theme with what it suggests changing in the programme, then add the note: these are counts of comments from people who chose to write, not survey results, and not a measure of how common a view is.

## Output Format
```markdown
# Open Comment Themes
Programme: [name] | Question(s): [wording] | Invited: [n] | Responded: [n] | Left a comment: [n] | Left none: [n] | Sample checked per theme: [you set]
## Code list
| Code | Definition (one line) | Comments carrying it |
|---|---|---|
| [code] | [what counts as this code] | [count] |
## Themes
| Theme | Definition (one sentence) | Comments | Paraphrase (anonymous) | What it suggests changing | Sample checked by |
|---|---|---|---|---|---|
| [theme name] | [definition] | [count] | [paraphrase, roles only] | [change to the programme] | [name, or "not yet checked"] |
## Minority views
| View | Comments | Paraphrase (anonymous) | Why it is kept |
|---|---|---|---|
| [view] | [count] | [paraphrase] | [what it could point to] |
## Unplaced comments
[count] comments fit no theme: [short description of what they cover].
## Limits
These are counts of comments from people who chose to write. They are not survey results and do not measure how common a view is. A comment can carry more than one code, so counts do not add up to the number of comments. Themes were built by a reader and checked on a sample of [n] per theme.
## Decision
[Name] decides which suggested changes go into the next run of the programme and which need more evidence first, by [date].
```

## Done When
- Every comment is in a theme or in the unplaced count, and the totals are stated.
- Each theme has a one-sentence definition, a count and a paraphrase.
- You have checked your sample for each theme, or the theme says "not yet checked".
- Minority views appear as their own lines, and the limits note is on the page, not in a footnote.

## Quality Bar
- A theme names a pattern in what was said ("no time to practise after the session"), never a topic heading ("time").
- Comment counts are never turned into a share of learners, and no sentiment score or rating of a trainer, a manager or a learner is drawn from the comments.
- A paraphrase that could still point to its author is rewritten or left out. Privacy points: check with a qualified adviser.
- Praise and complaint get the same care; a theme is not softened because it is uncomfortable for the team that built the programme.
- No comment is invented, merged into a quote or attributed; themes describe the programme, and nothing identifies who wrote what.

## Next
Run impact-training-contribution-analysis (Training Contribution Analysis) to weigh what the numbers and the comments together can support.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
