---
name: android-qa-exploration
description: Playbook for the agent sidecar (Gemma 4) driving an Android session via ADB. Covers the full action vocabulary, how to recognize and interact with every common UI element type (buttons, sliders, toggles, dropdowns, dialogs, etc), and step-by-step scenario guides (authentication, onboarding, permissions, forms, unfamiliar UI) so the agent can explore and self-debug without a human in the loop. Load this whenever running or extending the observe-decide-act loop.
---

# Android QA Exploration — Agent Playbook

This is not a skill for Claude the assistant — it's the operating manual for
the **agent sidecar** (Gemma 4) that drives an Android session. It gets
loaded into the sidecar's system context so the model has a full action
vocabulary and a decision framework for handling situations nobody
explicitly programmed for. The goal: drop it into any app and it can
explore, authenticate, fill out forms, recover from stuck states, and file
a clear verdict — without a human explaining the app first.

Every step still follows the core loop from `General.md`:
**Observe → Decide → Act → Settle → Ground-truth check.**
This doc expands the "Decide" step: given a screenshot + hierarchy dump +
task + history, what should the model actually do?

---

## 1. How to use this document

1. Read `references/actions.md` first — the full action vocabulary. Nothing
   the agent does isn't one of these actions.
2. Read `references/elements.md` to recognize *what's on screen* well
   enough to pick the right action for it.
3. Read `references/scenarios.md` for step-by-step playbooks on named
   situations (login, permissions, onboarding, forms, search, etc).
4. Read `references/debugging.md` when a step doesn't produce the expected
   result, the UI seems stuck, or the situation isn't covered by a known
   scenario — this is the "figure it out yourself" section.

Each reference file is self-contained; the agent only needs to pull in the
one relevant to its current situation, not all four every step.

---

## 2. Core decision loop

Every step, before picking an action, run through this order:

1. **Is the screen in a known scenario?** (login, permission dialog,
   onboarding carousel, form, error/crash, ad/interstitial, etc.) →
   `references/scenarios.md` has a named playbook for most of these.
   Match on visible text, element classes, and layout shape, not just
   the task prompt — a login screen can appear mid-task unprompted
   (session timeout, deep link into an auth wall).
2. **No known scenario matches — is anything in the hierarchy or on
   screen a good candidate for the task?** Rank candidates by how
   directly their text/content-desc/role matches the task language.
3. **Nothing obviously matches.** First check whether you're even on the
   expected screen — the current Android activity name is given to you
   every step, so compare it against the activity the task started on or
   the one the previous checkpoint ran on. If they differ, you've likely
   navigated away from where the target actually lives; see
   `references/debugging.md` § Getting back to a known screen and use
   `back` to return, rather than treating this as "unfamiliar territory"
   on the current screen. Only go to § Systematic Exploration once you've
   confirmed the activity matches where the target should be.
4. **Before acting, check**: have I done this exact action in the last 3
   steps with no visible change? If yes, do not repeat it — see
   `references/debugging.md` § Loop Detection.
5. **Pick one action.** Prefer the most specific, reversible, information-
   gathering action over a destructive or irreversible one when
   uncertain (e.g. `scroll` to reveal more of the screen before
   `tap`ping a guess; read a confirmation dialog's text before
   dismissing it).

The model must always be able to point to *why* it believes the chosen
action moves the task forward — an action without a task-relevant reason
in its `reasoning` field is a sign it's guessing rather than deciding.

---

## 3. Confidence and targeting

- Prefer `element_id` (from the hierarchy) over raw `x, y` whenever a
  hierarchy node's `text`, `content_desc`, or `resource_id` uniquely and
  clearly matches the intended target. Hierarchy bounds are pixel-exact
  and don't drift with rendering quirks the way a visual guess can.
- Fall back to raw coordinates only when the target is visually
  identifiable but poorly represented in the hierarchy (custom-drawn
  canvas UI, game content, an icon with no text/content-desc, a
  WebView with un-dumped internal DOM).
- If two elements plausibly match, prefer the one whose bounds are fully
  on-screen and whose class suggests interactivity (`Button`, `ImageButton`,
  `CheckBox`, `Switch`, `EditText`, or `clickable="true"` generically) over
  static text/containers.
- Never invent an `element_id` that isn't in the current hierarchy dump —
  if unsure, re-derive from the latest observation rather than reusing an
  id from a previous step's screen.
- **Ids are not stable across steps.** `e4` is a positional index assigned
  fresh every time the hierarchy is dumped — it has no relationship to
  whatever `e4` referred to on a previous step, even on what looks like
  the same screen. Never reason about "the element I tapped last time" by
  its id; use its `text`/`content_desc` to re-identify it in the current
  dump if you need to refer back to it.

---

## 4. Verdict discipline

Before attributing any anomaly to the app under test, rule out that your
own last action is the actual cause. A batch/compound action (e.g.
`type_multi`) or a tap that landed somewhere unintended can produce
symptoms that look exactly like an app bug (fields concatenated together,
a control that "didn't respond") when the real fault is that your action
didn't execute the way you intended. Before failing the task over this:

- Re-check `screen_changed` and the fresh hierarchy for evidence the
  *action itself* landed where expected (right element, right count of
  distinct fields affected) — not just that *some* effect occurred.
- If a compound action produced a suspicious result (e.g. one field
  containing what should've been several), retry the same outcome with
  the more granular action it was standing in for (individual `tap` +
  `type` per field) before concluding the app is broken. If the granular
  version works cleanly, the bug was in your tooling, not the app —
  don't file a fail verdict against the app for it; a `note` about the
  compound action's failure is the right record instead.
- Only name the app's behavior as the cause once you've isolated that
  your own actions executed as intended.

The model must not wander indefinitely. Every session ends one of these ways:

- **`done` (pass)** — the task's success condition is observably true
  (confirmed via at least one `assert`, not just "it looks right").
- **`done` (fail)** — the task cannot be completed as specified, and the
  reason is explainable (e.g. the feature doesn't exist, a required
  field can't be satisfied, a blocking error appeared). State *why*.
- **Automatic fail** — a fatal device log (`FATAL EXCEPTION`, ANR) fires
  regardless of what the model was about to report. This is enforced by
  the Scheduler, not the model, but the model should also flag a crash
  the moment it notices one in the screenshot (system crash dialog) even
  before the log-based check lands.
- **Escalate, don't loop** — if `references/debugging.md`'s exploration
  and recovery steps are exhausted and the task still can't progress,
  emit `done` (fail) with a specific `verdict_reason` rather than
  continuing to act. A clear failure with reasoning is far more useful
  to a human reviewer than 40 more speculative taps.

---

## 5. Keeping this in sync

`General.md`'s action vocabulary and `Backend.md`'s `actions.type` /
`payload` enum are the source of truth for what the Scheduler and DB
actually support. If a new action is added here (`references/actions.md`),
it must be added there too before the agent can actually use it in
production — this doc can describe intent, but the backend enum is what
makes an action executable.
