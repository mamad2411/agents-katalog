---
name: find-series-opportunities
description: Use when you want to discover content series across your existing work — finds clusters by theme rather than topic, identifies repeated points from different angles, flags incomplete arcs, and suggests series framing that makes relationships explicit.
---

Before doing anything else:
1. Check if `~/.devadvokit.md` exists.
2. If it does, read it silently and use it throughout this skill.
3. If it does not, stop and tell the user: "I need your DevRel context before I can run this skill. Please run /setup-devadvokit first."

---

## What NOT to Do

This skill produces content strategy — not content calendars or editorial schedules. Specifically:

- **No publication dates** — that's an editorial planning skill
- **No content calendar** — this is about theme discovery and arc completion
- **No SEO analysis** — this is about conceptual relationships, not search optimization

The goal is finding the series hiding in your existing work.

---

## How This Skill Works

This skill reads your content library from `~/.devadvokit.md` and finds patterns across it. You don't need to provide input content — the skill analyzes what's already in your library.

---

## Output

Produce all of the following after reading the content library.

### 1. Thematic Clusters

Content grouped by underlying theme (not just surface topic):

For each cluster (2+ pieces identified):

- **Cluster name:** [The underlying theme that connects them]
- **Pieces in this cluster:**
  - "[Title]" ([Year]) - what angle it takes
  - "[Title]" ([Year]) - what angle it takes
- **The connection:** [Why these belong together beyond being the same topic]
- **Series potential:** [Low/Medium/High — whether this could become an intentional series]

Identify 2–4 clusters minimum.

### 2. Repeated Points from Different Angles

Where you've made the same core point without realizing it:

For each repeated point found:

- **The recurring insight:** [The point you keep making]
- **Where it appears:**
  - "[Title]" ([Year]) - how you framed it
  - "[Title]" ([Year]) - how you framed it
- **What's different each time:** [How the framing shifts]
- **Series candidate?** [Yes/No — whether these could be consolidated or sequenced]

### 3. Incomplete Arcs

Where you wrote part 1 and part 3, but part 2 is missing:

For each incomplete arc found:

- **Arc theme:** [The progression that should connect them]
- **What you have:**
  - "[Title]" ([Year]) - the starting point
  - [Missing middle piece(s)]
  - "[Title]" ([Year]) - the endpoint
- **What's missing:** [The conceptual bridge that's absent]
- **Suggested piece to write:** [Title + brief description of the missing link]

### 4. Series Framing Suggestions

For clusters or arcs that could become intentional series:

For each series suggestion:

- **Series title:** [A name that captures the through-line]
- **Pieces in series:**
  1. "[Existing Title]" or "[Missing piece: Working title]"
  2. "[Existing Title]" or "[Missing piece: Working title]"
  3. (etc.)
- **Framing premise:** [What makes this a series rather than unrelated pieces]
- **Why it works as a series:** [What the reader gets from experiencing them together]

Suggest 1–2 series maximum.

---

## No Library Found

If `~/.devadvokit.md` has no content library or an empty content library:

> "Your content library is empty or very small. Add past talks, posts, videos, and other content using `/setup-devadvokit` so I can find series opportunities in your work."

Stop and do not produce output.

---

## Small Library Found

If the content library has fewer than 3 pieces:

> "Your content library has fewer than 3 pieces. Add more content using `/setup-devadvokit` — I need more work to analyze for patterns and series opportunities. Come back when you have 5+ pieces."

Stop but show what you found anyway (it may still be useful).

---

Before presenting any output, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.