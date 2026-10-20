---
name: web-task-scoping
description: Governance procedure for scoping any browser-automation or web-agent task before granting it autonomy — whether driven by the pre-installed Playwright CLI, an MCP browser tool, or an external framework (Playwright MCP, Stagehand, Skyvern, Magentic-UI, Steel Browser). Use this whenever a task involves an agent clicking, filling forms, navigating, or taking actions on a live website, especially one with side effects (submitting, purchasing, posting, deleting) rather than pure read/screenshot. Also trigger when the user asks "should I let the agent do X on the web," wants a checklist before turning on browser automation, or is choosing between browser-agent frameworks.
---

# Scope Before Speed

Source: "AI Power User Stack" carousel (@zhiprompts), governance slide "SCOPE BEFORE SPEED — GIVE THE AGENT A SMALL WEB JOB." The core discipline: **give a web agent a small, inspectable job — not a browser with unlimited authority.**

## The rule

Before letting any agent touch a live website with actions that have side effects, define four things *first*, in this order:

1. **Target** — one permitted site (or a fixed allowlist), named explicitly. Not "the web" — a URL or domain.
2. **Limit** — one measurable outcome the run is trying to produce, and what's out of bounds (no purchases over $X, no sending messages, no deleting records, read-only unless stated otherwise).
3. **Run** — one test/sandbox account wherever the site supports one, never a production or personally-identifying account for a first run.
4. **Review** — one approval checkpoint before the agent gets to act again with more autonomy (a human looks at what it did, or is about to do, before the next step).

If any of the four is missing, the task isn't scoped yet — narrow it before starting, don't improvise mid-run.

## Applying this in Claude Code specifically

- **Read-only tasks** (checking a page, extracting data, taking a screenshot) don't need the full four-step ritual — Target and Limit ("just reading, nothing submitted") are usually enough.
- **Side-effecting tasks** (filling forms, submitting, purchasing, posting, deleting, changing account settings) need all four, and the Review checkpoint should happen *before* the side-effecting action fires, not after — inspect the planned action, then approve.
- The pre-installed Playwright CLI in this environment (`playwright screenshot <url> <file>`, used elsewhere in this repo for verifying rendered HTML) is inherently a Target=one-file, Limit=screenshot-only, low-autonomy case — it doesn't usually need the full ritual. The ritual matters once a task moves from "look at this page" to "act on this page."
- For a multi-step or exploratory browser job, restate the scope explicitly at the start of the task (in a comment, a command's confirmation, or a message to the user) rather than assuming it's implied.

## Choosing a framework, if one is needed

This skill governs *how* to scope the task, not *which* tool executes it. `claude-code-tooling` documents the five browser-agent frameworks from the same source carousel (Playwright MCP, Stagehand, Skyvern, Magentic-UI, Steel Browser) — pick based on whether the job needs structured tools, natural-language flexibility, visual understanding, a visible human-in-the-loop interface, or durable remote infrastructure. Scope the job with this skill's four-step rule regardless of which one is chosen.

## Output conventions when using this skill

- State the four elements explicitly before starting a side-effecting browser task — don't bury them in narration.
- If the user's request doesn't specify a Limit or Review checkpoint, ask for one rather than assuming full autonomy is fine.
- Treat "the agent did something unexpected" during a scoped run as a signal to stop and return to the Review checkpoint, not to push through and hope the next step self-corrects.

## Related skills in this repo

- **claude-code-tooling**: Documents the five external browser-agent frameworks (Playwright MCP, Stagehand, Skyvern, Magentic-UI, Steel Browser) this governance procedure applies to.
- **attachment-intake**: Same underlying discipline (inspect before acting, don't force autonomy onto ambiguous input) applied to files instead of web actions.
- **night-shift-workflow**: The same "match oversight to the stakes" autonomy boundary, applied to scheduled/unattended background workflows instead of interactive browser tasks — apply both together when a scheduled workflow's job involves web automation.
- **subagent-depth-control**: The same "don't grant more scope than the task needs" discipline, applied to Claude Code's subagent nesting-depth setting instead of browser tasks — deeper nesting multiplies context windows and token cost the same way ungoverned browser autonomy multiplies risk.
- **image-to-code** / **design-templates**: Both already use a scoped, single-purpose Playwright CLI pattern (screenshot one file, compare, done) — this skill formalizes why that pattern is safe by default.

## Notes

Source: "AI Power User Stack — 5 AI browser agents that can do the clicking for you" carousel (@zhiprompts). The five tool profiles feed `claude-code-tooling`; this governance slide is the genuinely new procedural content, captured here as its own skill.
