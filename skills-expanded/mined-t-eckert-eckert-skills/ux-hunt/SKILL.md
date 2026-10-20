---
name: ux-hunt
description: Find real usability, information-architecture, and workflow problems in a UI — the design-and-flow counterpart to /bug-hunt. Scales from a fast pass on one screen you just built, up to a driven walkthrough of a whole flow or app. Every finding is grounded in a concrete user, a concrete task, and observed friction, ideally by driving the running UI, so it reports what genuinely trips a user rather than style preferences. Use when the user says "review the UX", "usability review", "is this confusing", "review this flow", "review this screen", "does this make sense", or "/ux-hunt".
---

# Hunt for usability and workflow problems

Find **real** UX problems — poor information architecture, confusing workflows,
missing feedback, misleading affordances, incoherent logic — and report each one
grounded in a concrete user, their task, and the specific point where they get
stuck, misled, or lost. This is the design-and-flow sibling of `/bug-hunt`. Fire
it on a screen you just built, on a flow you are worried about, or across a whole
app. It **finds** problems. It does **not** silently redesign (fixing is a
separate, explicit step; see §6).

The whole value is **signal**. A hunt that surfaces one real "a user trying to do
X cannot find how, or lands on the wrong screen, or gets no confirmation and does
it twice" beats one that lists ten "this could be more polished" opinions. The bar
for reporting is **"I can name a user, their goal, and the concrete point where
the UI fails them"** — not "I would have designed this differently." Everything
below serves that bar.

> **Read the settled decisions first.** This skill hunts *against* the
> information-architecture rules and product decisions the team has already made.
> It does not relitigate them. If your project has settled IA rules, record them
> in `CLAUDE.md`. A finding that argues against a settled rule is out of scope. A
> screen that violates one is a finding.

## Relationship to the other review tools

- **`/bug-hunt`**, if installed, finds code defects: wrong output, crashes, data
  corruption.
- **`/ux-hunt`** (this) finds *experience* defects. The code works as written,
  but the user cannot find it, cannot understand it, cannot finish the task, or
  is misled about what happened.
- The two overlap at **UX logic**: a gate that shows the wrong thing, a state
  that contradicts itself, a button enabled when it cannot work. When a finding
  is really "the code is wrong," hand it to `/bug-hunt`. When it is "the code is
  right but the experience is broken," it is ours.
- **`/code-review`** reviews the current diff for correctness and cleanup.
- They compose. "Is this change correct" goes to `/code-review`. "What could
  break" goes to `/bug-hunt`. "Does this actually work *for a user*" comes here.

## 0. Scope the hunt, then match effort to scope

Decide the surface **first** — it sets everything else. Infer it from what you
have been working on and say what you chose. Ask only if it is genuinely
ambiguous.

| Scope | What it means | Default effort |
|---|---|---|
| **Screen** | One page or component you just built or edited | Drive that screen and its states inline, single pass (§2–§3) |
| **Flow** | An end-to-end task (sign up, check out, triage the inbox) | Drive the whole flow start to finish inline; a few lenses in depth |
| **Surface** | One area of the app (a settings section, a dashboard, onboarding) | Drive the area's main paths; every relevant lens |
| **App** | A whole application | Multi-agent walkthrough workflow (§5) |

Scale the machinery to the ask. "Is this screen confusing" means drive it and
answer. "Walk the whole app for UX problems" means the §5 workflow. **Do not
start a workflow for one screen**, and do not try to eyeball a whole-app
walkthrough from the source.

## 1. Freshness guard — drive the live UI, not a stale checkout

A usability finding is only real if it reproduces in the code that actually
ships. Before asserting that a user hits something:

- **Prefer driving the running UI over reading the source.** "This is confusing"
  is cheap. "I drove the flow as this user, and here is the screenshot where it
  dead-ends" is the whole point. Reach the real rendered screen, its empty,
  loading, and error states, and the actual navigation. Then read the code to
  explain *why*.
- **Confirm you are driving the intended build.** A long-running local dev server
  is often on a stale branch. To exercise a branch's UX, run that branch on its
  own port and drive it there. A confusing screen the main branch already
  redesigned is worth saying so, not filing.
- **Know which app owns the surface.** In a multi-app product, the same route can
  exist in two apps with different gating. Confirm which one you are on.
- **Watch for unreachable pages.** A route that no navigation links to is a
  finding in itself. It is not a page to review as if users see it.

### Driving the UI

Use whichever harness the project already has, in this order of preference:

1. **A Playwright MCP server**, if the project wires one up. Drive it with the
   `browser_*` tools and take screenshots of every state you report.
2. **The `claude-in-chrome` skill**, if the flow needs a real logged-in browser
   session.
3. **A project script** that captures an authenticated `storageState` once, then
   opens pages with it. Authenticated flows are worth the setup, because the
   interesting UX problems are almost all behind a login.
4. **Reading the source**, as the last resort. Say clearly in the report that you
   did not drive it.

> **Record your project's recipe.** The exact commands — which port, how auth is
> captured, where the browser binaries live, which fixture to seed — belong in
> your `CLAUDE.md` or a project skill, not here. Write them down the first time
> you work them out. The second hunt is then ten minutes instead of an hour.

**Rule out the harness artifacts that masquerade as UX bugs** before you file
anything. A blank page is often a render crash, not a design choice. A "failed to
load" screen may be the app's real, rendered error state rather than a browser
error, so you detect it by its text or a screenshot rather than by a status code.
Both are real user-facing states worth reviewing. Just attribute them correctly.

Say what you drove, and which build or branch you drove it against, in the
report.

## 2. Hunt by usability lenses, not by "looking at the screen"

Do not eyeball for polish. Pass each surface through concrete lenses, tracing a
real user with a real goal through each one.

- **Information architecture** — Where does this surface live, and does that match
  the user's mental model? Is it reachable from the main navigation, or is it an
  orphan island? Is the same task exposed in two competing places? Does the
  hierarchy match how the user thinks about the product? Does the surface survive
  a deep link, a refresh, and the back button?
- **Task flow, and whether they can finish** — Trace the core job end to end. Can
  the user actually complete it? Where are the dead ends, the steps that need
  knowledge the UI never gave them, and the forced detours? How many steps are
  there, and how many are necessary? After the user acts, does the UI leave them
  oriented with a sensible redirect and a confirmation, or stranded?
- **Feedback and system status** — Every action and every load has states:
  loading, empty, success, error. Are they all handled? Does an error render as a
  *helpful* state that says what to do next, or as a blank screen? Does the UI
  confirm what happened, so the user does not retry and submit twice? Does the
  empty state teach the next step, or just sit there empty?
- **Affordance and clarity** — Does each control say what it does? Is the primary
  action on the screen obvious, or buried in an overflow menu or a hover state?
  Are labels, buttons, and icons unambiguous? Is a destructive action visually
  distinct from a safe one?
- **Error prevention and recovery** — Look for destructive or irreversible
  actions with no confirmation and no undo. Check validation timing: does the
  form wait until submit to reveal a problem the user could have fixed while
  typing? Do error messages say *how* to fix the problem? Does the form lose the
  user's input on error? Are required fields and format rules stated up front?
- **Content design and cognitive load** — Look for internal jargon leaking to
  users: database column names, internal role names, raw slugs and ids, where a
  human word belongs. Look for too much on one screen with no hierarchy, and for
  concepts used before they are explained.
- **Consistency** — The same concept named differently on two screens. The same
  action styled or placed differently in two places. Patterns that fight the rest
  of the app.
- **UX logic — the seam with `/bug-hunt`** — Does the UI's conditional logic make
  *sense to a user*? Look for gates that show or hide the wrong thing, states
  that contradict each other, a control enabled when it cannot work, a status
  that never updates, and a gate that appears to do something but gates nothing
  the user can see. If it is a genuine code defect, route it to `/bug-hunt`. If
  the code is right but the resulting experience misleads, it is a finding here.
- **Accessibility, lightly** — Check keyboard reachability of the primary flow,
  visible focus, and obvious contrast or label gaps. Note these. A full
  accessibility audit is its own effort, so go deep only if the user asks.

For a **Screen**-scoped hunt, run the lenses that screen plausibly trips. For
**Flow**, **Surface**, or **App**, run every relevant lens across the whole path.

## 3. Ground every finding before you report it

This is the step that keeps the tool trustworthy. It is the analog of
`/bug-hunt`'s adversarial repro. For each candidate problem, **make it concrete or
drop it**.

- Name the **user, their goal, and the exact point of friction**. "A collaborator
  opening the inbox for a workspace they were just added to sees 'Failed to load'
  with no next action" beats "the inbox error state is bad."
- **Show it.** Drive the UI to that point and capture the rendered state: a
  screenshot, a snapshot, or the actual copy on screen. If you could not drive
  it, quote the component or route that produces it. A finding you cannot reach
  is a hypothesis, not a finding.
- **Refute the easy objections.** Is there already a tooltip, an empty state, or
  help text that resolves it? Is the screen reachable at all, or is it dead code?
  Has the main branch already redesigned it? Is it actually one of the harness
  artifacts from §1 rather than a design choice?
- **Separate a defect from a preference.** "The user cannot tell which of two
  identically labeled buttons submits" is a defect. "I would use a card layout
  here" is a preference. Drop it, or clearly mark it as optional polish at the
  bottom, not as a finding. Default to **not a finding** when it is taste.

Only candidates that survive this get reported.

## 4. Report — ranked, concrete, actionable

Lead with the findings that block or mislead. For each survivor, give:

- **Severity** — *blocker* (the user cannot complete the task), *major* (they
  complete it, but with real friction, an error, or a risk of doing it twice),
  *moderate* (confusing but recoverable), or *minor* (polish) — and a one-line
  statement of what fails for the user.
- **User and task** — who is trying to do what, from the concrete scenario in §3.
- **Where** — the screen or route, and `file:line` for the code behind it, so it
  is clickable. Attach the screenshot or the rendered copy if you drove it.
- **Why it fails** — the architecture, flow, or feedback reason, tied to a lens
  from §2.
- **Fix direction** — the smallest change that removes the friction, in one or
  two lines of intent: a redirect, a confirmation, an empty state, a relabel,
  moving the surface to where the user looks for it. Do not apply it yet (§6).
- **Confidence**, and what you drove it against (§1).

If a lens came back **clean**, say so briefly. "Drove the sign-up flow end to end
as a first-time user: every step has a clear next action, submit is confirmed,
input is preserved on a validation error — clean" is real signal. If nothing
survived, report that plainly. A coherent surface is a good result, not a failed
hunt.

## 5. Deep walkthrough — the multi-agent workflow (Surface and App scope only)

For a broad walkthrough, use the **Workflow** tool so walkers fan out across
routes and flows, and each candidate is grounded by an independent skeptic. Do
this **only when the user has opted into a broad walkthrough**, because workflows
spawn many agents. For Screen and Flow scope, stay inline.

The shape is **walk → dedup → ground and verify → synthesize**, pipelined.

- **Walkers** — one agent per flow and lens, for example
  `signup-flow:task-completion`, `settings:information-architecture`,
  `inbox:feedback-states`, `onboarding:content-clarity`. Each drives its slice of
  the running UI. Give it the §1 harness recipe and the authenticated session.
  Each returns structured candidates:
  `{summary, user, task, screen, file, severity, evidence}`.
- **Dedup** — plain code over the pooled candidates, matching on screen or root
  cause. Do this *before* verifying. A barrier is justified, because dedup needs
  every candidate at once.
- **Ground and verify** — for each unique candidate, spawn two or more
  independent skeptics, each prompted to **refute** it, and each defaulting to
  `refuted: true` when the candidate is taste, is already handled, is
  unreachable, or is a §1 harness artifact. Keep only the survivors. Where a
  candidate can fail in several ways, give the verifiers distinct lenses:
  reachability, clarity, defect-versus-preference.
- **Freshness in every agent's prompt** — tell each walker to drive the intended
  branch and build, and to flag stale-checkout and render-crash artifacts (§1).
- **Synthesize** — rank the survivors by severity, dedup once more, and produce
  the §4 report.

Skeleton. Adapt the flows and lenses to the ask, and see the Workflow tool
documentation for the find-then-verify pipeline pattern.

```
export const meta = {
  name: 'ux-hunt-walkthrough',
  description: 'Drive the app flows across usability lenses, ground each candidate against the running UI',
  phases: [{ title: 'Walk' }, { title: 'Verify' }],
}
const WALKS = [ /* {key, prompt} per flow × §2 lens; each prompt embeds the §1 harness recipe */ ]
const found = (await parallel(WALKS.map(w => () =>
  agent(w.prompt, {phase: 'Walk', schema: CANDIDATES})))).filter(Boolean).flatMap(r => r.candidates)
const unique = dedupeByScreen(found)               // plain code — barrier justified
const verified = await parallel(unique.map(c => () =>
  parallel(['reachability','clarity','defect-vs-preference'].map(lens => () =>
    agent(`Try to refute this UX finding via the ${lens} lens; default refuted:true if it is taste, already handled, or unreachable: ${JSON.stringify(c)}`,
          {phase: 'Verify', schema: VERDICT})))
    .then(vs => ({...c, real: vs.filter(Boolean).filter(v => !v.refuted).length >= 2}))))
return verified.filter(v => v.real)
```

## 6. Fixing and filing — opt-in, never automatic

The hunt **stops at the report** by default. Then, on the user's word:

- **Fix** — if asked, address a finding. Isolate the work first in a worktree if
  you are in a real git repository. Follow the target app's conventions, and
  **drive the flow again to confirm the friction is gone**. Do not hand back an
  unverified redesign. Honor the project's branching rules, and never merge or
  deploy from a hunt.
- **File** — if asked, file the survivors as issues in the project's tracker.
  Each issue must be **self-contained**: inline the user, the task, and the
  evidence, rather than linking to a document the reader may not be able to open.
  Never echo secrets.

Offer these. Do not assume. The common flow is: hunt, report, the user says "fix
the inbox error state and the orphaned settings page", you fix and re-drive those.
