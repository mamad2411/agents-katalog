---
name: arc-bug-finder
description: >
  Investigates a reported bug (often from a screenshot) through exhaustive repo
  search and online research, isolates the root cause, recommends the best
  possible fix, then files it as a bug in the tracker the codebase already uses
  (GitHub Issues, GitLab, or Linear). Delegates story formatting to
  arc-creating-user-stories and plan formatting to arc-planning-work.
  TRIGGER when: user reports a bug, shares a screenshot of broken behavior,
  asks "why is this happening", or asks to file/triage/research a defect.
  DO NOT TRIGGER when: user asks to implement a fix (use arc-bug-fixer), or to
  plan greenfield features (use arc-defining-work).
---

# Bug Finder

A research-first bug intake skill. It does **not** fix code. It investigates a
reported defect as deeply as the repo and the open web allow, then files a
high-quality, root-cause-backed bug in whatever tracker the project already uses.

The output of this skill is a **filed bug ticket**, not a code change. Handing the
fix off to implementation is a separate step ([arc-bug-fixer](../arc-bug-fixer/SKILL.md)).

## Operating Principles

- **Evidence over assumption.** Never describe a root cause you have not located
  in the actual code. Every claim links to `file:line`.
- **Exhaustive before conclusive.** Search the repo and the web fully before
  proposing a fix. A plausible guess is a bug, not a finding.
- **One bug, one ticket.** If investigation reveals several independent defects,
  file them separately and cross-link.
- **The user usually sends a screenshot.** Treat the image as the primary symptom
  and reason from it. See [Screenshot Intake](#step-1-screenshot--symptom-intake).

## Workflow Overview

```
1. Screenshot / symptom intake   → what is broken, observed vs expected
2. Detect tracker                → GitHub | GitLab | Linear (auto, confirm)
3. Exhaustive repo investigation → reproduce, trace, isolate root cause
4. Exhaustive online research    → known issues, upstream bugs, best-fix options
5. Synthesize the bug report     → root cause + ranked solution options
6. File the bug in the tracker   → with screenshot attached, severity, repro
7. Return the link + summary
```

## Step 1: Screenshot & Symptom Intake

The user typically pastes one or more screenshots. For each:

1. **Read the image** with the Read tool — describe exactly what is on screen.
2. **Extract every signal**: visible error text, stack traces, console output,
   URL/route, component or page name, browser chrome, network panel, timestamps,
   element that looks wrong, and what the *correct* state should be.
3. **OCR any error string verbatim** — exact error text is the strongest search key
   for both repo grep and web search. Quote it character-for-character.
4. **Capture environment** if visible: device/viewport, light/dark mode, logged-in
   role, env banner (prod/preview/dev), build/commit hash.

If no screenshot is provided, ask for one or for: the exact steps, the observed
result, and the expected result.

Record a one-line **symptom statement** before investigating:
> "On `<route/component>`, when `<action>`, the app shows `<observed>` instead of `<expected>`."

## Step 2: Detect the Tracker (Auto, Then Confirm)

Determine which system the codebase uses — do not ask blindly. Probe in order:

| Check | Command / signal | Implies |
|-------|------------------|---------|
| Git remote host | `git remote -v` → `github.com` / `gitlab.com` / self-hosted GitLab | GitHub or GitLab |
| GitHub CLI ready | `gh auth status` and `.github/` present | **GitHub Issues** |
| GitLab signals | `.gitlab-ci.yml`, `glab auth status`, `gitlab.*` remote | **GitLab Issues** |
| Linear signals | `LINEAR_API_KEY` set, `.linear`, W-number titles, Linear MCP available | **Linear** |
| Existing ticket numbering | grep recent commits/PRs for `W-######`, `#\d+`, `[A-Z]+-\d+` | matches active tracker |

State the detected tracker and the evidence, then proceed unless the user
redirects. If two are plausible (e.g. GitHub remote *and* `LINEAR_API_KEY`), ask
which is canonical for bugs.

> Detected tracker: **GitHub Issues** (remote `github.com/...`, `gh` authenticated,
> recent commits use `WSM-######`). File the bug here? (yes / Linear / GitLab)

## Step 3: Exhaustive Repo Investigation

Goal: convert the symptom into a located root cause. Be thorough — fan out with
the Explore agent or parallel greps; do not stop at the first plausible file.

1. **Anchor from the screenshot.** Grep the exact error string, visible UI labels,
   route paths, and component names from Step 1.
2. **Trace the call path.** From the rendering component → handler → service →
   data layer. Read the real files; follow imports. Note every `file:line` on the
   path to the defect.
3. **Reproduce locally when feasible.** Run the failing unit/E2E test, or write a
   minimal repro (do not commit it). Confirm the symptom is real and deterministic.
   Capture exact reproduction steps.
4. **Find the root cause, not the surface.** Distinguish where it *manifests* from
   where it *originates*. Check recent changes: `git log -p --follow <file>`,
   `git blame <file> -L <range>` — a regression often points straight at the commit.
5. **Assess blast radius.** Who else calls the broken code? Is it data-dependent,
   role-dependent, viewport-dependent? Note related latent defects.

Output of this step: a root-cause hypothesis with a concrete code citation and a
confidence level. If confidence is low, say so and list what is still unknown.

## Step 4: Exhaustive Online Research

Find the *best possible* fix, not the first one. Use WebSearch / WebFetch and any
available docs skills:

1. **Search the exact error string** in quotes — surfaces known issues fast.
2. **Check upstream trackers** for the library/framework at fault (GitHub issues,
   changelogs, release notes). Is this a known bug? Fixed in a newer version?
   A documented breaking change?
3. **Read authoritative docs** for the API in question — confirm correct usage
   versus what the repo does. Prefer official docs over memory (APIs drift).
4. **Compare candidate fixes.** Collect 2–3 distinct approaches with trade-offs
   (correctness, blast radius, effort, upgrade vs patch vs workaround).
5. **Cite sources.** Every external claim gets a URL. Note version numbers.

If the repo uses a framework with a dedicated skill available (Next.js, Convex,
Clerk, Stripe, Vercel, etc.), consult it before concluding.

## Step 5: Synthesize the Bug Report

Produce the report body below. This is the canonical bug format — reuse it for all
three trackers. Acceptance criteria follow `arc-creating-user-stories/STORY_FORMAT.md`
(verifiable checklist with a `Verify:` method per criterion).

````markdown
## Bug
**ID:** W-XXXXXX
**Severity:** S1 Critical | S2 Major | S3 Minor | S4 Cosmetic
**Status when found:** prod | preview | dev

**Summary:** One sentence — observed vs expected.

## Environment
- Route/Component: `...`
- Role / device / viewport / theme: `...`
- Build / commit: `...`

## Steps to Reproduce
1. ...
2. ...
3. ...

**Observed:** what actually happens (attach screenshot).
**Expected:** what should happen.

## Acceptance Criteria (fix is done when)
- [ ] [Correct outcome stated as an observable fact]
  - Verify: [test command, CLI check, or manual observation]
- [ ] No regression in [adjacent behavior]
  - Verify: [existing test/suite that proves it]

## Root Cause
Grounded in code: `path/to/file.ts:NN`. What is wrong and why it produces the
symptom. Include the originating commit if it is a regression (`<sha>`).

## Recommended Fix
Preferred option first, with rationale.
1. **[Option A — recommended]** — what to change, blast radius, effort. Sources: <url>
2. **[Option B]** — alternative, trade-offs.

## Research Notes
- Known upstream issue: <url> (fixed in vX.Y.Z)
- Relevant docs: <url>

## Blast Radius / Related
- Other call sites: `...`
- Possible latent defects: `...`
````

Set **severity** by impact: S1 data loss/outage/security, S2 broken core flow with
no workaround, S3 degraded with workaround, S4 cosmetic.

## Step 6: File the Bug in the Tracker

Reuse the Step 5 body. Title format: `[W-XXXXXX] BUG: <short symptom>`.

Before creating, **check for duplicates** — search existing open issues for the
error string / route. If one exists, comment with new findings instead of filing a
duplicate.

### Cross-Skill Delegation

| Need | Delegate to |
|------|-------------|
| Story body & acceptance-criteria format | [arc-creating-user-stories](../arc-creating-user-stories/SKILL.md) |
| Fix/implementation plan to attach (incl. GitHub plan-comment workflow) | [arc-planning-work](../arc-planning-work/SKILL.md) |
| Bulk Linear creation mechanics & W-number sequencing | [arc-linear-issue-creator](../arc-linear-issue-creator/SKILL.md) |
| Branch/commit naming for the eventual fix | [arc-conventional-commits](../arc-conventional-commits/SKILL.md) |

### W-number sequencing

Derive the next `W-######` from the active tracker's existing titles (high-water
mark + 1), matching whatever convention the repo already uses (e.g. `WSM-######`).
Never reuse a number.

### Labels

Apply a consistent bug taxonomy across all three trackers:
`type:bug`, `severity:S1|S2|S3|S4`, `priority:P0|P1|P2`, and `area:<subsystem>`.

### GitHub Issues

```bash
# ensure labels exist (idempotent)
gh label create "type:bug" --color B60205 2>/dev/null || true
gh label create "severity:S2" --color D93F0B 2>/dev/null || true

# write body to a temp file, then create
gh issue create \
  --title "[W-XXXXXX] BUG: <short symptom>" \
  --body-file /tmp/bug-W-XXXXXX.md \
  --label "type:bug,severity:S2,priority:P1"
```

### GitLab Issues (`glab`)

```bash
# labels are created on first use; comma-separated
glab issue create \
  --title "[W-XXXXXX] BUG: <short symptom>" \
  --description "$(cat /tmp/bug-W-XXXXXX.md)" \
  --label "type::bug,severity::S2,priority::P1"
```

If `glab` is unavailable, use the REST API:
`POST /projects/:id/issues` with `PRIVATE-TOKEN: $GITLAB_TOKEN`.

### Linear (GraphQL)

Follow [arc-linear-issue-creator](../arc-linear-issue-creator/SKILL.md) for context
resolution (team/project/labels/W-number) and the `issueCreate` mutation. Set the
issue to the bug-equivalent label/state for the team.

## Screenshot Handling per Tracker

The user almost always supplies a screenshot — attach it; do not just describe it.

- **GitHub:** the `gh` CLI cannot upload inline images. Options, in order of
  preference:
  1. Commit the image under `docs/bugs/W-XXXXXX-<slug>.png` on a branch and
     reference it in the body with a relative or raw URL.
  2. Upload via `gh api` to the repo and embed the returned `user-attachments` URL.
  3. If neither is appropriate, file the issue, then tell the user the one drag-and-drop
     step to attach it in the web UI, and include a placeholder line in the body.
- **GitLab:** upload first, then embed the returned markdown:
  `POST /projects/:id/uploads` (multipart) → returns `{ "markdown": "![file](/uploads/..)" }`
  — paste that markdown into the description. Or drag-drop in the UI as a fallback.
- **Linear:** request an upload URL via the `fileUpload` mutation, PUT the bytes to
  the signed URL, then reference the asset URL in the issue description markdown.

Always save the user's pasted screenshot to a local temp path first so it can be
read, hashed for the filename, and uploaded.

## Step 7: Return Result

Report back concisely:
- The filed bug's **URL/ID** and W-number.
- Tracker and labels applied.
- One-line **root cause** and the **recommended fix** option.
- Whether a screenshot was attached or needs a manual drag-drop.
- Any *additional* bugs discovered and filed during investigation.

## Rules

- This skill **investigates and files** only — it does not modify product code.
- No root cause without a `file:line` citation; no external claim without a URL.
- One defect per ticket; cross-link related ones.
- Always check for an existing duplicate before filing.
- Match the repo's existing ticket numbering and label conventions.
- Never commit or expose API tokens (`LINEAR_API_KEY`, `GITLAB_TOKEN`); read from
  env or prompt at runtime, and delete any temp files holding secrets.
