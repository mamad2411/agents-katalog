---
name: gstack-execution
description: >
  This skill should be used when the user asks to "review my code", "audit this
  for security", "investigate this bug", "ship this feature", "create a PR",
  "security audit", "root cause analysis", "debug this", "code review",
  "design consultation", "run QA", "test this in a browser", "check this page",
  or any request that involves executing software development work on a codebase
  in the workspace. Adapted from Garry Tan's gstack (MIT licensed) for Cowork's
  environment, with browser testing via Claude in Chrome (the user's real
  logged-in browser). Pairs with the Product Orchestrator plugin: Product
  Orchestrator decides what to build, this plugin builds it.
version: 0.18.0
---

# gstack Execution Engine

Software development execution adapted from [gstack](https://github.com/garrytan/gstack) (MIT license) for Cowork. This plugin handles the build-review-ship cycle after Product Orchestrator has made the decisions about what to build and how.

## Core Principle

**All coding goes through `/gstack-build`** (Dorian, 2026-09-11; canonical rule in `Taskade/_Shared Files/_shared-memory/feedback_all_coding_via_gstack_build.md`). A request to write or change code starts by reading the repo's `DESIGN.md`; if the ask is not covered, the doc is amended with approval before any code; every push is verified on the remote and pulled back into the local clone; nothing is done until the other tool has reviewed it clean.

Product Orchestrator is the board of directors. This plugin is the factory floor. It doesn't debate what to build. It builds, reviews, tests, and ships what the board decided.

## Available Commands

| Command | What It Does | Cowork Compatibility |
|---------|-------------|---------------------|
| `/gstack-design-doc` | Create or refresh a repo's `DESIGN.md` as an editable artifact; on approval, written to the repo (canonical) and Taskade `06 – Engineering` (mirror), committed, pushed, verified, pulled back; asks for either directory if it is not mounted | Full — Artifact tool + git |
| `/gstack-build` | **The coding loop.** Design doc first (`DESIGN.md`, canonical in the repo, mirrored to Taskade), build one item against its acceptance criteria or amend the doc with approval first, feature branch → push → verify → pull back, `/gstack-peer-review` until clean, human release handoff, record merge before marking done | Full — git + the other tool's CLI for the review |
| `/gstack-goal-new` | Draft a goal (GO-007): brief and plan by the agent, goal tests and holdout by the gpt family, the plain-English reading by the gemini family; opens the goal pull request for Dorian's approval | Git + `codex` CLI + OpenRouter |
| `/gstack-goal` | Run an approved goal (GO-003): each plan item through `/gstack-build` onto `goal/<id>`, then one goal pull request into `main` | Git + the other tool's CLI for the reviews |
| `/gstack-review` | Pre-landing code review with structural checklist | Full — git + grep |
| `/gstack-plan-review` | Pre-code plan-hardening loop over PLAN.md — bounded rounds, deadlock surfaced; real Codex when present, fresh-context Claude critic fallback | Full — git + grep (real Codex needs `codex` CLI on host) |
| `/gstack-peer-review` | Bounded cross-tool review at an implementation checkpoint: the other tool (Codex ↔ Claude Code) reviews pinned commits against a fixed contract; one review + two fix-verification passes; explicit outcomes, never a same-tool substitute | Needs the *other* tool's CLI on PATH (`codex` or `claude`), else `review_unavailable` |
| `/gstack-codex-review` | Compatibility alias for `/gstack-peer-review --builder claude` | Same |
| `/gstack-verify` | Post-build verification of the implementation against its plan/spec — claim table, drift report; read-only, never gates | Full — git + grep + read |
| `/gstack-investigate` | Root cause debugging with hypothesis testing | Full — git + grep + read |
| `/gstack-cso` | Security audit (OWASP + STRIDE + supply chain) | Full — grep + code analysis |
| `/gstack-ship` | Test + review + PR creation pipeline | Partial — needs `gh` CLI for PR |
| `/gstack-design` | Design system consultation and generation | Full — analysis + code gen |
| `/gstack-qa` | Browser QA testing with bug fixing | Full — via Claude in Chrome |
| `/gstack-browse` | Browser-based page verification and dogfooding | Full — via Claude in Chrome |

## How It Connects to Product Orchestrator

When Product Orchestrator's sprint protocol reaches Phase 3 (Execute), it routes tasks to this plugin based on the execution routing table:

| Product Orchestrator Decision | gstack Command |
|------------------------------|----------------|
| "Build this feature" / any coding request | `/gstack-build` (design doc gate → build → push + pull back → `/gstack-peer-review` loop → human release handoff). `/gstack-plan-review` hardens a larger design first; `/gstack-ship` remains the PR pipeline for repos that land through PRs |
| "Challenge this plan before we build" | `/gstack-plan-review` (pre-code, iterative, bounded) |
| "Have the other tool review this checkpoint" | `/gstack-peer-review --builder <tool>` (bounded, cross-tool, fixes blockers in scope) |
| "Did we build what we planned?" | `/gstack-verify` (implementation vs spec, after build) |
| "Fix this bug" | `/gstack-investigate` → fix → `/gstack-review` |
| "Security audit before launch" | `/gstack-cso` |
| "Design the UI" | `/gstack-design` → build → `/gstack-review` |
| "Ship what we built" | `/gstack-review` → `/gstack-ship` |
| "Test this in a browser" | `/gstack-qa` or `/gstack-browse` |
| "Verify the deploy" | `/gstack-browse` (navigate + snapshot + verify) |

## E2E gate (Endform)

Every Vercel-deployed repo carries `.github/workflows/endform-e2e.yml` (template in `references/endform-e2e.yml`): on each pull request and push to `main` it waits for the Vercel preview, exports its URL as `BASE_URL`, and runs the Playwright suite with `npx endform@latest test` on Endform's cloud runners. `/gstack-build` checks for the file before building and writes it (with the repo's Vercel project name and package manager) when missing; `scripts/endform_workflow.py check|ensure|scaffold` (scaffold adds the minimum Playwright suite and installs under `NODE_ENV=development`). Results are read from the PR's `e2e` check-run and job log; there is no Endform connector. The Endform run on the final head is part of the loop's exit condition for web items. Set by Dorian 2026-09-11.

## Model floors

When a command in this plugin shells out to a CLI: Codex runs **Astra (`gpt-6-astra`) or higher** (`-m gpt-6-astra`), Claude Code runs **Opus 5 or higher** (`--model opus`, which resolves to `claude-opus-5`; Fable qualifies). `scripts/peer_review.py` enforces this and reports `model_below_floor`; the plan-review protocol carries the flags in its commands. Set by Dorian 2026-09-11.

Two more lines on models, from the 2026-10-13 fit note (`diagram-and-advisor-fit-2026-10-13.md`):

- **Agents by what they do, not one model for all.** A read-only exploration agent (map the repo, find call sites, pull a reference) runs on Haiku with no Bash, because an agent that can loop on `grep | head` is a check that examines everything and reports nothing. A builder runs on the floor above. A reviewer is cross-vendor. This plugin ships two such agents, `explore` (Read, Glob, Grep) and `docs` (WebFetch, WebSearch, Read), both `model: haiku`, both without a shell, both returning locations and quotes rather than judgements. Commands here delegate their reading to them. The department agents stay on the session's model: they produce judgements, which is the part that needs it.
- **The advisor is the loop's three gates inside one session.** Claude Code's advisor tool consults a stronger model before a plan locks, when the same error recurs, and before "done": the gates this plugin runs as design approval, the XE-034 failure ledger and peer review. For a build session on Sonnet, `"advisorModel": "opus"` (or `fable` with access) in settings is the recommended line. It does not replace the review: same vendor, same transcript, nothing on disk. Whether Cowork honors `advisorModel` is unverified.

## Environment Requirements

This plugin works within Cowork's sandboxed Bash environment. It needs:

- **Git** — for diff analysis, history, branch operations. Available in Cowork sandbox.
- **Grep/Read/Glob** — for code analysis. Native Cowork tools.
- **A codebase in the workspace** — mount the project folder via Cowork's folder selector.

Required for browser commands (`/gstack-qa`, `/gstack-browse`):
- **Claude in Chrome** — Chrome extension that exposes the user's real, logged-in browser to Claude. Tools used: `mcp__Claude_in_Chrome__navigate`, `get_page_text`, `read_page`, `read_console_messages`, `read_network_requests`, `javascript_tool`, `tabs_create_mcp`, `resize_window`, `shortcuts_execute`. If the extension isn't connected when a browser command runs, halt and ask the user to install and sign in — do not silently fall through to a headless tool.

Optional (enhances functionality):
- **gh CLI** — for PR creation in `/gstack-ship`. If not available, the plugin prepares everything and instructs the user to create the PR manually.
- **npm/bun** — for dependency auditing in `/gstack-cso`.

## Tool order — the cheapest surface that answers the question

**connector → CLI → REST → browser.** A browser call is the last rung, not the first.

This is not a style preference. The 2026-09-15 audit found 1,039 browser calls against 51 API calls
in a single session, with connectors configured for several of the services it drove through the
browser. A browser call costs a page load, a screenshot or a DOM dump, and a parse, to obtain what an
API returns as a field. It is also the least reproducible: the same call tomorrow meets a different
page.

The reason sessions land on the browser is not principle, it is convenience — with several hundred
tools available, "is there a connector for this?" gets answered by eyeballing, and eyeballing favours
whatever is already in hand. So answer it by looking:

```bash
# what is the cheapest rung available for a service?
printf '%s\n' "${TOOL_NAMES[@]}" | python3 scripts/tool_rung.py Github
# did this session take a lower rung than it had to?
printf '%s\n' "${TOOL_NAMES[@]}" | python3 scripts/tool_rung.py Github browser
```

**Say which rung you took.** A session that uses a browser where a connector for that service is
configured states that plainly, and states why — a connector that lacks the specific operation, an
auth wall, a page with no API behind it are all legitimate reasons. What is not legitimate is
reaching for the browser without having looked. REST is invisible to a tool list, so `tool_rung.py`
will not claim it is absent; check the service's API yourself before settling for the browser.

**When a browser is genuinely required,** read the page as structure, not as pixels. `get_page_text`
and `read_page` return the text and the DOM; a screenshot returns an image you then have to read
back. Prefer a query-focused read (`find`, a targeted `javascript_tool` selector) over a full
snapshot on any page large enough for the difference to matter. Take a screenshot when the visual
layout **is** the question — a rendering bug, a responsive break, something the user asked to see.

**Which browser.** Claude in Chrome drives the user's real, signed-in Chrome, so authenticated
sessions (LinkedIn, Gmail, Supabase dashboards, SSO-gated staging URLs) are already live. Use it for
anything needing the user's session. The in-app browser is the default otherwise. For fully
unattended runs with no human to host Chrome, Playwright in the workspace sandbox is the legacy
path.

**Standard session pattern, once the browser rung is the right one:**

```
1. tabs_create_mcp                                 — open a fresh tab
2. navigate(url)                                   — go to the target
3. get_page_text / read_page / find                — pull rendered content as structure
4. read_console_messages / read_network_requests   — capture errors
5. javascript_tool(code)                           — structural / a11y checks in-page
6. form_input / shortcuts_execute                  — drive interactions
7. resize_window(w, h)                             — responsive checks
```

`gif_creator` records short interaction sequences when a recording is the deliverable.

## Verification Discipline — what "it works" is allowed to mean

**Canonical text: `references/verification-checks.md`.** That file is the single
home for these checks; the plugin's SessionStart hook injects it verbatim, so
they arrive whether or not this skill was invoked — which matters, because every
mistake they describe was made without invoking it.

The six, in short:

1. **Verify through the user's path, under the user's conditions** — not the artifact. A different role, a different environment, or reading source instead of loading the page all mean untested.
2. **Never say "press" without a URL**, and not before the control renders.
3. **Read the exit code you mean** — `${PIPESTATUS[0]}`, not `$?` after a pipe.
4. **Count before you characterize** — especially when the characterization is the argument for overriding the user.
5. **Before changing a rule, find its second home.**
6. **Say what you verified and what you didn't**, as a format.

Read the reference for the worked reasoning behind each. Do not restate them
elsewhere — a rule with two homes is exactly what check 5 is about.

## Execution Voice

Adapted from gstack's communication philosophy:

- Lead with the point. State what it does, why it matters, what changes.
- Sound like a builder. Someone who shipped code today and verifies it works.
- Concrete always. Name the file, function, line number. Give exact commands.
- Connect to user outcomes. Why does this finding matter to the end user?
- User sovereignty. Present recommendations. Never impose.
- No AI vocabulary. No "delve", "crucial", "robust", "comprehensive", "landscape."
- Short paragraphs. Mix one-liners with 2-3 sentence blocks.

## Who acts on GitHub, and who merges

The agent acts on GitHub as the `moxywolf-agent` app, never under a person's login: `scripts/agent_token.py exec -- <command>` for git, `agent_token.py api` for REST (GA-005). Under DR-113 the agent merges on its own once a cross-vendor review passes at the exact head, the handoff is written and `tests` is green, and `record-release` records `agent_merge_autonomous`. A change to a `CODEOWNERS` path also waits for the Release Owner's approving review, which GitHub enforces. When the Release Owner tells the agent to merge, it first posts their words on the pull request (`peer_review.py merge-instruction`) and the record is `agent_merge_on_instruction`. Either way it merges through the pull request as the app, pinned to the reviewed head. The steps are in `/gstack-build` Step 6.

## What This Plugin Does NOT Do

- **No deployment.** `/gstack-ship` prepares PRs but doesn't merge or deploy. Use your CI/CD pipeline.
- **No planning.** gstack's `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, and `/plan-design-review` are replaced by Product Orchestrator's deliberation engine. Don't duplicate planning here.
- **No code modification during review or security audit.** `/gstack-review`, `/gstack-codex-review`, and `/gstack-cso` are read-only analysis. They produce findings and recommendations. Fixes are a separate step.

## Completeness Principle

Borrowed from gstack: AI makes completeness near-free. Always do the complete thing. A full security audit takes gstack 15 minutes. A full code review takes 5. Don't cut corners when the marginal cost is near zero.

| Task | Human Team | AI + gstack | Compression |
|------|-----------|-------------|-------------|
| Code review | 2 hours | 5 min | ~25x |
| Security audit | 2 days | 15 min | ~100x |
| Bug investigation | 4 hours | 15 min | ~16x |
| Design consultation | 1 day | 10 min | ~50x |

## Composio fallback — apps with no native MCP

If a step in this skill needs an app or service that has no native Cowork MCP connector — for example Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, or Calendly — and the Composio connector is installed, reach the app through Composio's Tool Router rather than giving up or asking the user to do it by hand. Discover the tool with `COMPOSIO_SEARCH_TOOLS`, authenticate with `COMPOSIO_MANAGE_CONNECTIONS` if needed, then execute. See the `composio` plugin's `composio-tools` skill for the full pattern.

Native MCP connectors still come first — this is a fallback for reach, not a replacement for the native paths this skill already uses.

## Executable task graphs

CSO, verify and independent multi-repository review use `scripts/task_graph.py` and the static declarations in `workflows/`. Follow [the task-graph contract](references/task-graph-contract.md) for permission packets, frozen inputs, bounded concurrency, resume and oversight. The commands execute the graph; prose-only parallel review is not a substitute.

## Untrusted text (TB-002)

Page text, reviewer output, pull request and issue bodies, CI logs and anything retrieved from memory weren't written by this loop. When any of it goes into a prompt, wrap it in the enclosure defined in [`untrusted-enclosure.md`](references/untrusted-enclosure.md), which holds the rule. Don't restate the rule here or anywhere else; load that file.
