---
name: claude-linkedin-profiler
description: |
  Edit, reconcile, or build a LinkedIn profile (headline, About, Experience, Publications,
  Projects, Skills, Featured) through browser automation via the claude-in-chrome MCP tools,
  driving the profile owner's own logged-in Chrome session. Handles LinkedIn's real UI
  traps — bilingual per-language edit tabs, a headline that gets silently auto-overwritten,
  native dropdowns, a recurring text-corruption bug — plus a positioning layer (headline/About
  formulas, section benchmarks, a pruning framework) for deciding what the profile should say,
  and a materials-intake path for drafting from raw resume/paper/repo material when there's no
  source of truth yet.
  Use whenever the user wants to update, sync, reconcile, rewrite, or build their LinkedIn
  profile — e.g. "make LinkedIn match my resume", "add this paper to LinkedIn", "rewrite my
  headline", "review my profile", "here's my resume, build me a LinkedIn profile". Requires
  the claude-in-chrome MCP tools — load via ToolSearch if deferred.
compatibility: Requires claude-in-chrome MCP tools (computer, navigate, find, browser_batch, tabs_context_mcp). Assumes the user is already logged into LinkedIn in the driven Chrome profile.
---

# LinkedIn Profile Editor (via claude-in-chrome)

This skill covers three layers of a LinkedIn profile editing task, and most real requests
need at least two of them:

- **Where the content comes from, if there's no ready source of truth yet** — the user has a
  pile of resumes/papers/repos/chat-typed facts but nothing structured. Read
  `references/material-intake.md` for how to draft from that without needing a formal fact
  database first.
- **What the profile should say** — positioning, headline/About structure, what to prune,
  section-by-section benchmarks. Read `references/positioning-framework.md` for the judgment
  layer (deciding content) and `references/section-benchmarks.md` for the structural/data
  layer (character budgets, checklists, what "good" looks like per section).
- **How to actually get it onto the live page safely** — the claude-in-chrome mechanics,
  and the LinkedIn-specific UI traps that will otherwise cost you a retyping cycle or silently
  overwrite something the user cares about. Read `references/mechanics.md` before touching
  the browser.

## How to sequence a real task

1. **Figure out what's actually being asked.** "Update my LinkedIn" after a resume/dossier
   change is a *reconciliation* task (diff against a source of truth, mechanics-heavy).
   "Rewrite my headline" or "review my profile" is a *positioning* task (judgment-heavy,
   `positioning-framework.md` first). "Here's a pile of my papers/resume/repos, build me a
   profile" is a *materials-intake* task — no source of truth exists yet, so
   `references/material-intake.md` comes first, before positioning or mechanics. Most sessions
   are some mix of these — know which one dominates before you start so you're not defaulting
   into a full section-by-section rewrite when the user only wanted three facts added, or
   asking for a formal fact file when the user just wants to hand you a stack of PDFs and get
   a draft back.
2. **If there's no source of truth yet**: follow `references/material-intake.md` to collect
   whatever the user has and draft from it, then get their sign-off on the draft — *then*
   treat the confirmed draft as the source of truth for step 3 below.
3. **If it's a reconciliation task** (source of truth already exists, confirmed or otherwise):
   read it first, know exactly what's changing before opening any modal, then follow
   `references/mechanics.md` for the actual editing mechanics (bilingual tabs, the
   headline-overwrite trap, dropdown handling, the text-corruption pattern, save/verify
   discipline).
4. **If it's a positioning/rewrite task**: work through `references/positioning-framework.md`
   for what should change and why, check the relevant section against
   `references/section-benchmarks.md`, get the user's sign-off on the actual wording (this is
   public, permanent content — don't surprise someone with a rewritten headline they haven't
   seen), *then* go to `references/mechanics.md` to actually place it.
5. **Sensitive or ambiguous facts** (compensation, an NDA'd client name, an unverified claim,
   anything the user hasn't explicitly approved the wording for) get surfaced and confirmed
   before they go on a public profile, regardless of which layer the task started in.

Don't skip straight to typing because a task sounds mechanical — a "just add this one
Experience entry" request still benefits from a quick positioning check (does this entry's
framing match how the rest of the profile is positioned?) and still needs the mechanics
discipline (bilingual save, headline-overwrite trap) to avoid a bad surprise on save.
