---
name: personal-writing
description: Draft and revise Cooper's personal blog posts, essays, and public-facing longform writing in his Obsidian personal vault while faithfully following a designated reference source.
version: 1.0.0
created_by: agent
---

# Personal Writing

Use for drafting or revising Cooper's personal longform writing, especially a blog post requested for `~/personal` / the personal Obsidian vault.

## Source discipline comes first

1. Identify the **authoritative reference source named by Cooper** (a Linear document, an existing post, a note, etc.). Read that exact source before drafting.
2. If Cooper says to use *only* a named source, treat that as a hard scope boundary:
   - Do not borrow tone, framing, claims, or structure from other posts, notes, drafts, or general context.
   - Do not describe other materials as influences.
   - Do not silently substitute a similarly named document; confirm the exact document identity when there are multiple candidates.
3. If he corrects which reference is right, discard the prior source analysis and restart from the corrected source.

## Default voice for Cooper's personal drafts

Unless Cooper asks otherwise:

- Write laid-back, first-person, timeline/story-driven prose.
- Prefer a concrete sequence: what happened → what initially seemed true → the revealing detail → what changed → the transferable point.
- Use short declarative paragraphs and occasional one-line emphasis.
- Use plain language over formal retrospective language. Avoid corporate framing, unnecessary thesis statements, and artificial wrap-ups.
- Let the argument emerge through the story rather than opening with a broad abstraction.

These are defaults, not excuses to override an explicitly designated reference's voice or structure.

## Workflow

1. Resolve the target vault and intended folder. For `~/personal`, it is the personal Obsidian vault; do not assume the team vault from `OBSIDIAN_VAULT_PATH` is the destination.
2. Read the named reference directly, including enough surrounding text to understand its structure and pacing.
3. Extract only source-grounded ingredients:
   - opening move
   - paragraph length and cadence
   - heading pattern
   - sequencing pattern
   - level of technical detail
   - how it qualifies claims / handles non-goals
4. Write the draft as a new Markdown note in the requested vault. Do not publish, deploy, add blog metadata, or alter production content unless asked.
5. Before reporting completion, check:
   - every factual claim is supported by the conversation or the authorized source;
   - no unapproved reference influenced the draft;
   - the file is in the requested vault/folder;
   - the title and structure fit the intended format.

## When revising a miss

If Cooper says a draft is "not quite right":

1. Do not defend the draft or merely tighten sentences.
2. Re-read the requested reference and identify whether the miss was voice, chronology, formality, claim selection, or source contamination.
3. Rewrite from the source's actual pattern, rather than patching individual phrases.
4. Keep the prior draft as a draft unless Cooper asks to replace it; state clearly which file was updated.

## Reference materials

- `references/source-discipline.md` — compact checklist for avoiding reference contamination and document-title collisions.
