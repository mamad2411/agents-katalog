---
name: artifact-report
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never plain markdown). Use this skill whenever the user asks for a status update, weekly report, monthly report, status report, engineering update, project update, incident report, post-mortem, retro, retrospective, PR description, or PR writeup that should be delivered as a polished HTML document. Trigger when the user wants to "summarize what shipped this week", "write up the incident", "draft a post-mortem", or any similar recurring written deliverable that benefits from a small chart, a timeline, a colored highlight, or a structured table over a flat markdown summary. Pair with artifact-css for the underlying design system. Do NOT use for casual chat summaries that the user just wants to read in the conversation - only when an HTML artifact is the deliverable.
---

# artifact-report

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file. Not markdown. Not `.md`. Not plain text.**
>
> Use templates from `templates/`. Inline `artifact.css` inside `<style>` (Mode B — single-file portable) or `<link>` to it. Use the class vocabulary from `artifact-css/SKILL.md` (`.panel`, `.kv-strip`, `.timeline`, `.callout`, `.badge`, `.note`, etc.) — never markdown syntax like `# headings`, `| pipe tables |`, or `* bullets`.
>
> This holds even for "internal" or "working" reports. The shape is HTML, always. The file extension is `.html`, always.

---

Polished HTML reports: status updates, post-mortems, incident timelines, PR writeups. These all share the same shape - a header that says what this document is and when it covers, a one-block summary that someone scrolling through Slack can absorb in five seconds, then progressively more detail underneath.

Read `artifact-css/SKILL.md` first for the full OUTPUT CONTRACT, the design system, and the page skeleton.

## Three subtypes

The skill ships templates for three reliable archetypes. Pick the closest fit and edit.

| Subtype | Template | Use when |
|---|---|---|
| Status report | `templates/status-report.html` | Recurring "what shipped, what slipped, what's next" updates. Weekly, biweekly, monthly. |
| Incident report | `templates/incident-report.html` | After an outage or production incident. Minute-by-minute timeline, mitigations, follow-ups. |
| PR writeup | `templates/pr-writeup.html` | The author's PR description - motivation, before/after, file-by-file tour, what reviewers should focus on. |

If the user's request doesn't match one of these cleanly, start from the status report template and adapt.

## Anatomy of a status report

Every status report is built from five blocks. Use this order.

1. **Header.** Title (period the report covers), the team or system, and a `.prompt-box` if the report is being generated from a specific user instruction.
2. **Summary band.** Four `.stat` cards. The numbers should be the four that the reader most cares about - usually a velocity metric, a quality metric, and two others tied to the team's current goals. Use `.stat-delta up/down` to show movement.
3. **Highlights.** A `.highlights` list of three to five bullets. Each bullet leads with what shipped (in `<strong>`) and follows with one sentence on why it matters. Resist filling this with everything that happened - the value is in the curation.
4. **Body sections.** Two or three sections, each with a `.sec-head` and a different rendering: a `.table` for "shipped this week", a small inline SVG chart inside a `.panel` for velocity, a `.callout` for the one thing the team is asking for help with.
5. **What's next.** Either a short `.timeline` for fixed-date commitments, or a second highlights list for softer "we're going to look at" items.

Keep the whole page to one printable screen if possible. A weekly status that runs longer than two scrolls is not being skimmed.

## Anatomy of an incident report

Incident reports prioritize the timeline. Everything else is context.

1. **Header.** Incident ID (`<div class="eyebrow">INC-2025-0412</div>`), one-line title (the symptom, not the cause), and a `.kv-strip` with duration, detected-at, resolved-at, owner, and severity.
2. **TL;DR.** A `.callout` with two or three sentences: what users saw, what caused it, what fixed it. The reader who closes the tab after the TL;DR should still know the most important things.
3. **Timeline.** A vertical timeline of timestamped events. Use the milestone pattern with the `when` slot holding the time. Distinguish event types with `.dot` color: clay for "alert / impact", olive for "mitigation / recovery", slate for "neutral / context".
4. **Root cause.** Prose explanation. One or two paragraphs. Resist bulleting this - the causal chain is the point and bullets hide it.
5. **What we changed and what we'll change.** Two tables or one combined table. The first column is the change, the second is the owner, the third is the status (`.badge-success` "shipped", `.badge-warn` "in progress", `.badge` "planned"). Be honest about what isn't done yet.
6. **Detection and response notes.** Brief reflection on what went well and what didn't in the response itself. Often two short notes (`.note-success` + `.note-warn`).

## Anatomy of a PR writeup

The author's-side document, not the reviewer's-side. Goal: the reviewer should be able to do a good review from this page alone.

1. **Header.** Repo path in mono, PR title, status badge, author avatar.
2. **Motivation.** A short paragraph. What changed in the world such that this PR is now worth doing. No CSS class needed - just a paragraph after the header.
3. **Before / after.** A `.grid-2` of two `.panel`s, "Before" on the left and "After" on the right. Either prose, screenshots (inline SVG mockups), or short code snippets in `.code-block`s.
4. **File-by-file tour.** A series of `.panel`s, one per file or coherent file group. Each panel: file path (mono, in `.file-label`), one paragraph of "what this file does now and why it changed", optional code snippet, optional list of risks or callouts.
5. **What reviewers should focus on.** A `.highlights` list of three to five things. This is the single highest-leverage section in the document.
6. **Testing.** A small table: what was tested, how, result. Brief.
7. **Rollout.** A `.kv-strip` with feature flag name, ramp plan, rollback procedure, monitoring dashboard link.

## Voice and density rules

These artifacts have a specific tone. Worth respecting.

- **Lead with the verb.** "Shipped threaded comments" beats "Threaded comments were shipped".
- **One stat per claim.** "Latency p99 down 38% on the hottest tenant" - not "significantly improved latency".
- **Name things by their real names.** Service names, file paths, ticket numbers in mono. The reader is technical and wants the precise reference.
- **No padding sentences.** Cut anything that doesn't move the reader closer to a decision or an understanding.
- **Honest about what isn't done.** A status report that hides slippage is worse than no status report. Use `.dot-warn` and `.dot-bad` freely.

## Common mistakes

- **Stat cards filled with whatever was easy to count.** If the team's actual goal this quarter is reducing on-call pager volume, the first stat card should be pager pages, not lines of code.
- **TL;DR that is longer than the summary band.** The TL;DR is two or three sentences. If it needs more, the cause analysis below isn't doing its job.
- **A timeline where every dot is the same color.** Visual differentiation between "alert", "human action", "recovery" is the whole point of using a timeline component instead of a numbered list.
- **PR writeups that summarize the diff instead of arguing for it.** A reviewer who can read the diff doesn't need an English copy of it. They need to know what to look at first and why.

## After the artifact

Always offer to also produce a short plain-text summary the user can paste into Slack or email. The HTML is the canonical artifact; the plain-text is the distribution channel.
