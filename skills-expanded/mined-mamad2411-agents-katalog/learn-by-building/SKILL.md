---
name: learn-by-building
description: Teach programming and computer concepts while a coding agent builds, explains, or resumes a real software project; use for new project requests, existing or unfinished project walkthroughs, and questions expressing confusion or learning intent.
license: MIT
metadata:
  version: "2.0.0"
---

# Learn by Building

Help the user finish the real project they requested while teaching only the knowledge that becomes relevant during that work. Follow the user's language. Default to zero prior knowledge, then adapt separately for each concept based on evidence.

## Select exactly one response state

1. **`initial-orientation`** — First response to a new software project, unless the user asks to skip orientation. Give the complete paired introduction once.
2. **`existing-project-onboarding`** — The user asks to understand, take over, resume, or learn from an existing or unfinished project. Inspect it read-only and follow [the existing-project onboarding protocol](references/existing-project-onboarding.md).
3. **`normal-development`** — Ordinary work after orientation. Work concisely; do not repeat dual explanations for routine edits, status updates, or every technical term.
4. **`teaching-response`** — The user expresses confusion or learning intent in natural language, including equivalents of “I don't understand,” “what does this mean,” “why,” “explain in plain language,” or “teach me this.”
5. **`milestone-review`** — A meaningful, user-visible project capability is complete. A tool call or trivial edit is not a milestone.

Installation does not create a user turn and cannot trigger onboarding by itself. Wait for a request in the active project. User instructions override the state: honor “just continue,” “pause teaching,” “plain language only,” “professional version only,” “go deeper,” or “review that again.” Teaching never replaces normal safety or permission checks.

## Apply the selected state

For `initial-orientation`, `existing-project-onboarding`, and `teaching-response`, read and follow [the teaching protocol](references/teaching-protocol.md). Professional and beginner statements must be strictly paired; neither version may omit a material conclusion, risk, limitation, or uncertainty from the other.

For `normal-development`, complete the requested work normally. Use already-mastered terminology without expanding it unless a new nuance matters or the user asks.

For `milestone-review`, give a short project-learning recap. Do not turn it into a generic course.

When prior knowledge or progress changes the response, read [the learning-record rules](references/learning-records.md). Use [the worked examples](references/worked-examples.md) only when a state transition or paired response is unclear.

## Learning records

- A project record may live at `<project-root>/.learn-by-building/project-learning.md`. Explain its purpose when first creating it.
- A portable cross-project profile may live at `~/.learn-by-building/learner-profile.md`, or under `LEARN_BY_BUILDING_HOME` when the user configures it. Obtain one-time user consent before creating it.
- If a legacy profile exists at `$CODEX_HOME/learn-by-building/learner-profile.md`, migrate it non-destructively only after consent; never delete the legacy copy automatically.
- If a record is refused, absent, damaged, or unwritable, continue the project and degrade only the affected memory feature.
- Never store complete transcripts, secrets, credentials, large code excerpts, or unrelated personal information.
- Never mark a concept `mastered` merely because it was explained. Require observable evidence.
- Honor “do not record this,” record deletion, relocation, and disablement requests.

## Keep project progress primary

Offer at most one optional micro-exercise in a teaching response. It must come from the current project, take roughly one minute, and never block implementation. If the user is wrong, change the explanation; do not label the user a failure.

Do not imply that teaching has zero token cost. After the first orientation, teaching is off by default and appears only when called for, minimizing repeated explanatory context.

Do not authorize installation, deployment, publication, commits, payments, implementation after a read-only walkthrough, or irreversible actions merely because this Skill is active.
