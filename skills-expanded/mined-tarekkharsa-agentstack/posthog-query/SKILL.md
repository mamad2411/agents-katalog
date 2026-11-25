---
name: posthog_query
description: Turn a product or analytics question into the right PostHog query — trends, funnels, or retention — with the correct events, breakdowns, and date range.
---

# PostHog Query

> Unofficial, agentstack-authored. Not affiliated with or endorsed by PostHog.

Use this skill when someone asks a product question in plain language ("are people
dropping off at checkout?", "is the new onboarding sticking?") and you need to
translate it into a concrete PostHog insight rather than guessing.

## Workflow

1. Restate the question as a measurable outcome. Pin down the **metric** (count,
   unique users, conversion rate, retention), the **population** (all users, a
   cohort, a single platform), and the **time window** before touching any tool.
2. Pick the right insight type for the shape of the question:
   - **Trends** — "how many / how often" over time, with optional breakdowns.
   - **Funnels** — "where do people drop off" across an ordered sequence of steps.
   - **Retention** — "do people come back" after a first action.
   - **Paths** — "what do people actually do" when the journey is unknown.
3. Map the question to **real events and properties**. List the project's events
   first (do not assume `signup` exists) and choose the closest match. Prefer
   unique-user math over raw event counts unless volume is the point.
4. Set an explicit date range and interval. Default to a window that captures at
   least one full cycle of the behavior (e.g. 30 days for weekly habits); never
   leave it implicit.
5. Add breakdowns or a cohort filter only when they answer the question. One clear
   breakdown beats three noisy ones.
6. Sanity-check the result: does the denominator make sense, is the funnel order
   correct, are bot or internal users excluded? State caveats with the answer.

## Conventions

- Confirm the target event names against the project before building — a query on
  the wrong event is worse than no query.
- Funnel steps must be in the order users actually experience them; a misordered
  step silently reports near-zero conversion.
- Report the date range, population, and any filters alongside every number so the
  result is reproducible.
- Prefer saving reusable questions as named insights on a dashboard over one-off
  ad hoc queries.

## Boundaries

- Do not present a query result as fact without stating its window and filters.
- If the right event clearly is not being tracked, say so instead of
  substituting a loosely related event and pretending it answers the question.
