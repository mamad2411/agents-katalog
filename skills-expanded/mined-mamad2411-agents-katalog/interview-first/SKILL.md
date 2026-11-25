---
name: interview-first
description: Use when asked to interview you before acting ("interview me first", "ask before building") — clarify, then point at the devkit:interview-first output style.
metadata:
  added: 2026-06-17
  last_reviewed: 2026-06-17
  type: core
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-06-17"
  related: [requirements-gathering, brainstorming, concise-output]
  keywords: [interview, clarify, ask, questions, ambiguous, underspecified, vague]
  owns: interview-first
---

# Interview First

Natural-language on-ramp for "interview me before you answer." The **durable** mechanism is the `devkit:interview-first` **output style** — it edits the system prompt, so the posture persists every turn and survives `/compact`. A skill body is one-shot (it fades across a session), so this skill handles the immediate request and signposts the durable switch.

The reframe it encodes: you're bad at knowing which context matters, the model is good at spotting what it's missing — so let it pull the context out of you instead of guessing what to include.

## When invoked

1. **Apply to this request.** Ask: would the result differ depending on context you don't have? If yes, ask **3–6 sharp questions — the ones whose answers change the approach** (prefer `AskUserQuestion` / multiple-choice), then proceed. If the request is already specific, or you can resolve the ambiguity yourself with a quick file read, **skip the questions and just do it**.
2. **Signpost the durable switch — once.** Tell the user: for every session, `/config` → Output style → **devkit:interview-first** (or set `outputStyle` in settings). Output styles are mutually exclusive, so selecting this **replaces** `devkit:concise`. To keep both postures, leave `devkit:concise` active and add a one-line "interview me before substantive work" to your `CLAUDE.md` instead. Don't repeat this every turn.

## What this is not

Not a stall. Don't interrogate a clear request — interrogating the obvious is the failure mode, not the feature. Skip when you can answer the ambiguity yourself.

Not a thinking budget. It changes _when you ask_, not how hard you think; reasoning, tool calls, and verification stay as thorough as ever. The deep procedure lives in `Skill(requirements-gathering)` (the five questions); the design gate lives in `Skill(brainstorming)`. This skill just makes "ask first" the reflex.
