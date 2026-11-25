---
name: using-devkit
description: How to use the devkit plugin on bb — discover skills with devkit_find_skills, load them with devkit_load_skill, and the old Claude-Code name → new invocation mapping. Read this first.
---

# Using devkit on bb

devkit's skill library is **located on demand, not autoloaded**. Only a few skills (this one,
`honest-completion`) are always visible. The rest of the library (~165 skills) is reachable
through two tools, so their descriptions never flood your context.

## The two-step discovery model

1. **Find** — call `devkit_find_skills({ topic })` with what you're working on (a language,
   framework, tool, or task). It returns ranked `slug: description` lines.
2. **Load** — call `devkit_load_skill({ slug })` to read the chosen skill's body. For a skill
   that points to a deeper reference doc, call `devkit_load_skill({ slug, reference })` with the
   reference's bare name.

Do this **before answering a domain/language/tooling question from memory** — if a devkit skill
covers it, load the skill and follow it.

## Old Claude-Code names → bb invocation

On Claude Code, devkit exposed skills and commands as `Skill(devkit:<slug>)` and
`/devkit:...` slash commands. On bb those become:

| Claude Code | bb |
|---|---|
| `Skill(devkit:go-essentials)` | `devkit_load_skill({ slug: "go-essentials" })` |
| `Skill(devkit:skill-discovery)` | `devkit_find_skills({ topic: "…" })` |
| `/devkit:review:review-code` | `bb devkit review code` (or `devkit_load_skill({ slug: "review-code" })`) |
| `/devkit:review:review-impl` | `bb devkit review impl <base>..<head>` |
| `/devkit:review:review-plan` | `bb devkit review plan <path>` |
| `/devkit:experts:go-expert` | `devkit_load_skill({ slug: "go-expert" })` |
| `/devkit:execute:commit` (and other `execute:`/`plan:`/`workflow:` commands) | `bb devkit run commit` — list them all with `bb devkit commands` |

> `bb devkit review …` **prints the review workflow instructions for a coding agent to run** —
> it does not produce a report by itself. Run it inside an agent, or load
> `devkit_load_skill({ slug: "review-code" })` and follow it.

## Other surfaces

- **Docs lookup:** `devkit_docs({ query })` or `devkit_docs({ libraryId: "/vercel/next.js" })` —
  current library/framework documentation via Context7.
- **CLI:** `bb devkit skills list | find <topic> | show <slug>` to browse the library from a
  shell; `bb devkit commands` and `bb devkit run <name>` for the ported devkit command workflows
  (commit, ship, tdd, pr, audit, brainstorm, onboard, …); and `bb devkit review
  <code|impl <base>..<head>|plan <path>>` to run the calibrated multi-perspective review
  (also driven by the `auto-review` plugin's `reviewMode: "devkit"`).
  `run` and `review` **inject a turn** into the current thread when run inside one (the agent
  runs the workflow as the next turn); outside a thread they print the workflow instructions
  for an agent — they are not standalone report generators.
- devkit's Claude-Code **agents** (experts, reviewers, workflow) are reframed as skills here —
  experts are `devkit_load_skill` slugs; reviewer calibrations load as references
  (`devkit_load_skill({ reference: "reviewer-senior-dev" })`).

## Notes

- If `devkit_find_skills` returns nothing, broaden the term; it also lists the domain categories
  it covers.
