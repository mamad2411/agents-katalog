---
name: mind-reader
description: Retrieve the right context from the owner's central mind (this brain repo) before doing any task in their name or voice. Use this whenever a task needs the owner's context, voice, takes, project facts, or content history — replying to a post as them, writing their newsletter/blog/social/video content, remixing an external title/hook/trend with their substance, answering questions about their projects, or any request like "reply as me", "use my brain", "what's my take on", "based on my mind". Every consumer project should invoke this skill instead of improvising retrieval.
---

# Mind Reader — the consumer protocol

You retrieve context from the owner's central mind. Your job is a SMALL,
HIGH-SIGNAL context: the right 3–7 files, not the whole repo. Read
`CLAUDE.md` at the repo root first — it is the contract.

## Protocol

1. **Locate the repo.** Path is given by the consumer project (env var
   `MIND_PATH` or its config). If missing, ask.

2. **Resolve the lens.** In priority order:
   - a lens named by the task ("use the building-in-public lens") → read
     `lenses/<name>.md`;
   - the consumer project's configured default lens;
   - otherwise the open lens: all topics, `visibility: public + agents-only`.
   A lens defines: primary topics, allowed note types, visibility ceiling.
   Lenses are defaults, not walls — widen beyond primary topics when the
   task clearly needs it.

3. **Load the identity core** (`identity/core.md`, `identity/voice.md`;
   `identity/beliefs.md` when writing opinionated content). Always.

4. **Read `INDEX.md`** and select targets:
   - task mentions a project → its `projects/` card;
   - task needs the owner's angle → matching `knowledge/takes/` (+
     `stories/` for narrative, `lessons/` for teaching content);
   - remix/repurposing task ("use this proven title/hook with my content")
     → `content-catalog/` for what already exists on the topic, then takes;
   - factual claims about their work → `knowledge/facts/`.
   Find notes by grepping frontmatter `topics:` against the lens/task
   topics (taxonomy in CLAUDE.md §7). Typical budget: 2–5 files beyond
   identity. If more seem relevant, take the most recent `current` ones.

5. **Apply the safety rules** (CLAUDE.md §6):
   - skip `status: superseded` notes — they are history, not positions;
   - respect `visibility`; never quote `private`;
   - if a project card's `last-verified` is >45 days old, do not present
     its numbers/status as current — hedge ("as of <date>") or omit;
   - open `raw/` ONLY for deep tasks (long-form, deep Q&A), via the links
     in notes/cards — never by browsing.

6. **Use it faithfully.** For voice tasks, anchor on the VERBATIM quotes in
   takes/stories — adapt the owner's actual phrasing rather than
   summarizing it into generic prose. Cite provenance (`source_url`) when
   the output format allows. If the mind has NOTHING relevant, say so and
   proceed on general knowledge WITHOUT pretending it came from the mind —
   and suggest feeding the gap later.

## Never

- Never dump whole folders or `raw/` into context.
- Never present a superseded take, a stale number, or invented context as
  the owner's current position.
- Never let a lens's primary scope hide an obviously-needed cross-topic
  note — lenses focus retrieval, they don't censor it.
