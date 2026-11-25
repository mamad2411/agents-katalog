---
name: knowledge
description: Our project memory in the repo's Obsidian vault (docs/knowledge/). CAPTURE — when asked to remember, note, or not relitigate a decision, rationale or learning, write it as an atomic wikilinked note. RECALL — answer what we know, have already decided, or noted (including prior art we recorded) from our own notes. New external investigation is research; onboarding a whole codebase is repo-onboarding.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Knowledge (recall + capture)

Maintain and read the project's durable knowledge — the Obsidian vault at `docs/knowledge/`
(atomic notes + `[[wikilinks]]` + maps-of-content). The deterministic vault operations are the
plugin's `bin/af.py`; this skill adds the judgement: what's worth recalling,
what's worth capturing, and how to keep notes atomic and linked. (Mechanism: ADR 0018.)

## Vault operations (deterministic core)

Run these exactly as written; each prints one JSON object. They need nothing installed.

```
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" vault-validate --repo .
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" vault-scaffold --repo .
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" vault-recall --repo . --query '<keywords, letters and digits only>'
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" vault-add-note --repo . --json - <<'NOTE'
{"name": "<kebab-case-name>", "title": "<human title>", "body": "<markdown>",
 "tags": ["tag-a", "tag-b"], "moc": "<themed-moc, or leave this key out for the root MOC>"}
NOTE
```

`vault-add-note` writes the note with its canonical frontmatter and links it from a MOC; the same
`name` replaces that note, and the result's `replaced` says so. `vault-validate` checks the graph
before finishing. It exits 1 with the `problems`, and `exists` is false if there is no vault yet.

**Folders.** Notes in every folder below `docs/knowledge/` are read, as Obsidian reads them, and
`[[name]]` resolves by file name wherever the note sits (folders starting with `.` or `_`, links,
and folder `README.md` files are skipped). A new note is written at the vault root; an existing
one is replaced in its folder (`path` says where). The root map is `MOC.md`, else `INDEX.md`,
`Home.md` or `README.md`. Two notes of one name in two folders is a `vault-validate` problem: rename
one.

**A refusal is the answer, not an obstacle.** If `vault-add-note` exits non-zero the note was NOT
saved: report its error to the user as it stands. Do not write the note by hand, or anywhere else,
to get round it. The vault's rules on where a note may go are in that command, so a note written
any other way skips them. Change a note by running `vault-add-note` again, not with `Edit`.

## When to use

- **Recall** — "what do we know about X", "have we decided / discussed X", "our notes or prior
  art on X", before designing or building. This reads **our** vault — not the outside world
  (that's `research`).
- **Capture** — "remember this", "capture this decision / rationale / learning", "note that …".
  Save durable knowledge that does **not** belong in code or git history (the *why* behind a
  choice, a gotcha, how we think about something).

## Recall

1. Detect the vault — `vault-validate`; if `exists` is false, **scaffold it**
   (`vault-scaffold`) and say so — don't stop to offer, a headless run has no one to answer.
   Recall on a fresh vault is then simply "nothing yet".
2. `vault-recall` → ranked candidate notes, with each one's `path`; read the top few in full.
3. Answer **grounded in those notes**, citing `[[note]]` links. If the vault has nothing on it,
   say so plainly — never invent knowledge.

## Capture

1. Distill to **one atomic idea per note** (split if it's several). Choose a kebab-case `name`,
   a `title`, and `tags`. **Nothing to capture** ("remember this" with no decision or rationale
   attached, nothing in the conversation to distill): say so, and capture what the prompt *does*
   carry — the decision context, the open question, who raised it and when — as a note tagged
   `needs-rationale`, so the next session can fill it in; ask for the rationale only when
   interactive.
2. `vault-add-note` — writes the note and links it from the
   root MOC. Use `[[wikilinks]]` in the body to connect related notes; add or extend a themed
   MOC (`"moc"`) for a cluster.
3. When a note records a decision that changes a **code, config or infrastructure artifact, name
   that artifact in the note** (the file, the manifest, the flag). A reader can then verify the
   decision actually shipped with one grep — a note is an intent, and intents go unimplemented.
4. `vault-validate` and fix any broken link or orphan before finishing.

## Definition of done

- Recall answers are grounded in real notes and cite `[[links]]`, or state the vault is silent.
- A recalled note asserting a code/config fact was checked against that artifact before being acted
  on, and any disagreement was surfaced rather than resolved silently.
- Captured notes are atomic, tagged, wikilinked, and reachable from a MOC; `vault-validate` is
  clean — no broken links, no orphans.
