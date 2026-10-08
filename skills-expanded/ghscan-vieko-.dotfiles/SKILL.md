---
name: lead-agent-weekly
description: Compose a recurring LEAD AGENT project update for Slack in Vieko's voice and format. Use this whenever the user asks to write, draft, compose, or update a Lead Agent project update, weekly or biweekly report, "this week" update, or recurring Lead-Agent progress summary destined for Slack. Gathers merged work from git + the bonfire epic state, then renders it as raw Slack mrkdwn (value-first bullets, not a commit recap).
---

# LEAD AGENT — project update

A recurring project update summarizing everything that shipped on Lead Agent since
the last report (often a two-week window). The audience is GTM stakeholders (MOPS,
sales leadership, the VDR team) plus engineering peers -- they care about *what each
change unlocks*, not the implementation. The output is **raw Slack mrkdwn**, pasted
directly into the channel.

This is a writing-style skill. The single most important reference is the golden
example -- match its voice, rhythm, and structure before anything else.

**Read `references/golden-example.md` first.** It is the spec. Everything below
explains how to reproduce it for a new week.

## The shape of the work

Two phases: **gather** (mechanical), then **compose** (judgment). Don't shortcut the
gather -- the report's credibility comes from it being grounded in real merged PRs and
the real epic state, not vibes.

### 1. Gather

Establish the window first. Use the user's requested cadence; otherwise infer it from
the previous post (the current golden example uses two weeks). Pin the cutoff precisely:
ask when the last report went out or infer it from the previous post's date. Everything
merged *after* that cutoff is in scope; everything before is already reported and must
not be repeated.

Pull the merged work across the Lead Agent surface area:

```bash
git log --format="%h %s (%ad)" --date=short --since="<cutoff>" -- \
  apps/lead-agent apps/lead-web apps/lead-bot \
  agents/lead-cs agents/lead-startup \
  packages/lead packages/lead-agent-framework \
  packages/enrichment packages/bounty-scoring
```

`apps/lead-agent` + `apps/lead-web` + `agents/lead-cs` + `agents/lead-startup` +
the `lead*` packages are the core (the scorer agents live under `agents/`, not
`packages/`). `apps/lead-bot`
feeds the LEAD BOT section when it has activity. Check `apps/api` / `apps/athena` only
if something there is Lead-Agent-adjacent (e.g. a shared DB table the queue reads).

For any commit whose value isn't obvious from the subject line, read the body --
`git show <hash> --stat` and the commit message often carry the *why* and the metrics
(eval deltas, cost numbers, FP rates) that make a bullet land.

Then read `<repo>/.bonfire/index.md`. This is where the epic narrative lives -- which
measurement windows opened/closed, which flags flipped, what's blocked, what's queued
next. The git log tells you *what merged*; bonfire tells you *what it means for the
epic* and feeds the summary and What's next. If the repo has no `.bonfire/`, ask the
user for the epic state instead.

### 2. Compose

Default to the compact project-update structure in the golden example:

1. `*What shipped in the last two weeks*` (name the real window: "three weeks" when it is)
2. `*What's next*`

When the window runs past two weeks or the list is six-plus bullets, open with one
italic `_TL;DR — ..._` line (two sentences max) before the first heading, as in the
2026-08-07 golden example. Skip it for a normal two-week post.

Use themed subsections such as `*VDR DASHBOARD*` or `*OUTREACH DELIVERY*` only when the
user requests a longer narrative report or the volume genuinely needs grouping.

## House style

The voice is the product. These rules reproduce it; the golden example shows it.

**Slack mrkdwn, raw.** Output the literal characters the user will paste:
- `_italic_`, `*bold*` (single asterisks -- NOT `**bold**`), `` `code` ``
- Links as `[label](url)`. (Vieko's Slack composer auto-converts this; don't use `<url|label>` unless asked.)
- Bullets are `* `, matching the posted Slack source exactly.
- Title line: `:update: :lead-agent: *PROJECT UPDATE*`
- Section headings are bold sentence case, with no trailing colon.

**Punctuation:** Vieko deliberately uses literal em dashes (`—`) in polished Slack
prose. Use them sparingly for a meaningful turn in the sentence, as in the golden
example; prefer a colon, semicolon, or comma when one reads more naturally.

**"Stage", never "Chapter."** The epic's internal docs say "Chapter"; the report says
"Stage." Translate on the way out (`Chapter 2.b` → `Stage 2`).

**Value over mechanism -- this is the whole game.** Each bullet leads with what the
change *brings to the table*, then just enough mechanism to be credible. The reader
should learn what's now possible, not what the diff did.
- Yes: *"We catch customers about to churn now:"* then one sentence on the gap that closed.
- No: *"Expanded CHURN_PHRASES regex to match verb-form cancellation."*

**Collapse PRs into outcomes.** Eight hardening PRs become one bullet ("Sends are now
safe and correct:") with the sub-fixes folded into a single sentence. The reader counts
outcomes, not commits. It's fine to mention the PR count as texture ("eight hardening
PRs this week") in a section tagline.

**Bullet structure:** `* Outcome-first sentence`, usually without a bold lead-in or
trailing period. Trailing Linear links are optional when useful:
`([GTMENG-1402](url))`. Multiple IDs are comma-separated inside one parenthesis.
UI labels the reader can see on screen go in inline code (`` `IN SEQUENCE` ``,
`` `Unenroll` ``); a new page or surface gets a link (`[SPAM SURFACE](url)`). When a
teammate owned a real part of a bullet, end it with their `@Name` mention rather than
narrating the split. Cut trailing "so that..." clauses and row-count stats unless the
number is the point. One dry aside per report is the ceiling.

**Long-form exception:** when the user explicitly wants a narrative weekly report,
an italic 2-3 sentence intro and themed section taglines can help. Do not add them to
the default compact project-update format.

**What's next:** include the genuine next priorities pulled from bonfire's "In flight" /
"Next Steps" / blocked items. Three is a useful default, not a hard limit; include a
fourth when it is a real user priority. Lead with the outcome and name gating
dependencies honestly.

## Output

Write the finished report to `<repo>/.bonfire/drafts/lead-agent-this-week.md` so it's a
reviewable artifact in the gitignored drafts area, then offer the clipboard one-liner:

```bash
pbcopy < <repo>/.bonfire/drafts/lead-agent-this-week.md
```

Present the raw mrkdwn in the reply too, so the user can eyeball it before pasting.

## After a real report ships

When the user tells you what they actually posted (it may differ from your draft -- they
edit for voice), **update `references/golden-example.md` with the shipped version.** The
golden example should always be the most recent real post, so the voice anchor never
drifts from what Vieko actually publishes. This skill lives in the dotfiles repo, so
that's a normal `cd ~/.dotfiles && git add` + commit.
