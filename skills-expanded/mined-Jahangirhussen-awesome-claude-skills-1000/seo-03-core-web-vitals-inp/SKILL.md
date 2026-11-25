---
name: seo-03-core-web-vitals-inp
description: INP (SEO). Use when the request involves: inp, interaction to next paint, responsiveness. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# INP

ID: 03.08.2 | Level: grandchild | Parent: [Core Web Vitals and speed](../SKILL.md)

## Purpose
INP within the seo-master tree: Slowest interactions with cause and fix.

## When to use
Triggers: inp, interaction to next paint, responsiveness

## When NOT to use
- The topic is covered by a sibling skill: `../cls`, `../lcp`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Record interactions in DevTools; find long tasks (>50ms)
2. Break up/defer JS, remove unused bundles, use web workers for heavy work
3. Optimize event handlers; avoid forced reflow; debounce input
4. Check third-party tag impact

## Decision rules and checks
- Profile long tasks
- Split/defer JS, reduce main-thread work
- Debounce handlers, avoid layout thrash

## Edge cases and failure handling
- Hydration blocks input -> partial/lazy hydration
- Heavy filter UIs -> virtualize lists

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Slowest interactions with cause and fix. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hydration blocks input
- Action: partial/lazy hydration
- Output: Slowest interactions with cause and fix.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
