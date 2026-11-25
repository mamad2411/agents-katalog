---
name: pith-setup
description: >
  Pith onboarding conversation. Runs on first session in a new project.
  Introduces Pith, offers wiki setup, guides through initialization.
  Injected by session-start.js when no prior setup detected.
---

## Onboarding script for Claude

On the user's FIRST MESSAGE this session, respond with this exact introduction — then ask ONE question. Do not dump everything at once.

---

**Introduction (2 sentences, then one question):**

> Pith is active — token compression running automatically. I can also build a project wiki that captures decisions, architecture, and learnings as we work — gets richer every session.
>
> New project or existing codebase?

---

## Greenfield flow (user says "new" or similar)

Ask these three questions, one at a time:

1. "What does this project do? One sentence is fine."
2. "Tech stack? Rough is fine."
3. "Just you, or a team?"

After getting answers, run `python3 ~/.local/share/pith/tools/setup.py --type greenfield` with the answers as context, then say:

> Wiki ready. I'll maintain it as we build — decisions, architecture, key entities. Every session it gets richer.
>
> What are we building first?

---

## Brownfield flow (user says "existing" or similar)

Ask these three questions, one at a time:

1. "What does it do? One sentence."
2. "What's the main pain — losing context between sessions, onboarding new people, documenting decisions?"
3. "Want me to bootstrap the wiki from the existing code? I'll read the codebase and write initial pages. Takes one session."

If they want bootstrap:
> Starting bootstrap. I'll read the main modules and write pages as I go — you'll see the wiki build in real time. Tell me if I'm missing something important.

Then run the bootstrap: explore src/, read main files (compressed by Pith automatically), write entity and concept pages, update index.md and log.md.

If they skip bootstrap:
> No problem. I'll start building the wiki from today's work. Every decision and solution we reach, I'll offer to save it.

Run `python3 ~/.local/share/pith/tools/setup.py --type brownfield` and mark setup complete.

---

## After setup (both flows)

Mark project as setup done: save `setup_done: true` in project state.

End onboarding with:
> Commands:
> - `/pith lean|precise|ultra` — output compression
> - `/pith debug|review|arch|plan|commit` — structured formats
> - `/pith wiki "<question>"` — search the wiki
> - `/pith ingest <file>` — add a source to the wiki
> - `/pith status` — token usage this session
> - `/budget 150` — hard token ceiling
>
> What are we working on?

---

## Rules for the onboarding conversation

- One question at a time. Wait for answer before next question.
- Don't list all features upfront. Introduce them as relevant.
- If user skips ("just start coding"): respect it. Mark setup_done, start working.
- Tone: conversational, not clinical. Brief.
- Don't say "As an AI" or "I'd be happy to". Just respond naturally.
