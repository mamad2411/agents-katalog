---
name: loop-wiki
description: >-
  Ingest and grow an Obsidian knowledge base as a verifiable loop. Combines Loop
  Engineering (machine-checkable completion criteria, boundary guardrails, a
  verification pass that resists gaming) with the Obsidian "second brain"
  organizing model (typed nodes, wikilinks, MOC, an index and an audit log).
  Use this whenever the user wants to organize, ingest, compile, interlink, or
  query a notes vault — phrases like "整理 inbox", "整理收件箱", "收录这篇文章",
  "把这篇编译进知识库", "organize my inbox", "ingest this article", "build a
  knowledge graph from my notes", "grow my Obsidian vault", "查一下知识库",
  or "second brain". Trigger even when the user only describes the goal (e.g.
  "I dumped 30 articles in my vault, make sense of them") without naming this
  skill. The vault location comes from the WIKI_PATH environment variable.
---

# loop-wiki

Turn an Obsidian vault into a knowledge base that *grows itself*: raw material
goes in, and the Agent compiles it into typed, cross-linked nodes that form a
visible graph — every run leaving an audit trail you can trust.

The hard-won lesson behind this skill: an Agent left to "just organize my notes"
will quietly invent a new naming scheme every day and produce *AI-generated
clutter* instead of knowledge. The fix is Loop Engineering — treat each
organizing pass as a loop with a **machine-verifiable goal**, **guardrails on
what it may not do**, and **a verification pass** that catches the Agent gaming
its own success criteria. That discipline is what makes the vault trustworthy
enough to run unattended later.

## Before anything: locate and validate the vault

The vault path lives in `WIKI_PATH`. Never guess it, never hardcode a path.

```bash
echo "$WIKI_PATH" && ls "$WIKI_PATH"
```

- If `WIKI_PATH` is empty: ask the user for their vault path and suggest they
  `export WIKI_PATH="/path/to/vault"`. Do not proceed without it.
- If the path exists but has no `SCHEMA.md`: this is an uninitialized vault. Run
  the **Initialize a vault** flow below before doing anything else.
- If `SCHEMA.md` exists: read `SCHEMA.md`, `index.md`, and `log.md` first. These
  three files *are the contract*. The rules in `SCHEMA.md` override your own
  instincts about naming and structure — follow them, don't relitigate them.

## The two control files you must respect every run

| File | Role | Your obligation |
|------|------|-----------------|
| `SCHEMA.md` | The rulebook: folder meanings, naming, wikilink policy | Obey it. If a rule is missing, propose adding it rather than improvising silently. |
| `index.md` | The entry map: links to key concepts, MOCs, recent updates | Update it whenever you add an important node. |
| `log.md`   | The audit trail: what changed, from which source, what's unverified | Append a dated entry every run. No log entry = the change didn't happen. |

## Node types — keep them separated

Different content plays different roles in the graph. Mixing them makes
wikilinks meaningless. Honor whatever folders `SCHEMA.md` defines; the default
model is:

- `raw/` — source material (articles, papers, transcripts). **Append-only and
  read-only. Never edit the original text.** This is the evidence layer; if the
  source rots, everything built on it is suspect.
- `concepts/` — durable ideas that recur across sources (e.g. RAG, Loop
  Engineering). Not a summary of one article — a long-lived node.
- `entities/` — concrete things: tools, people, companies, projects. Kept apart
  from concepts so terms and proper nouns don't blur together.
- `comparisons/` — "X vs Y" pages that accrete dimensions as new sources arrive.
- `queries/` — answers worth keeping. Only the ones that resolved a real
  question, not every chat.
- `moc/` — Maps of Content: a *reading route*, not a file listing. "Start here,
  then this, then that."
- `drafts/` — outputs: articles, threads, scripts. The endpoint of a knowledge
  base is output, not hoarding.

## Command: ingest one article ("收录这篇文章")

When the user points at a file in `raw/` (or pastes content for you to save
there first) and wants it compiled in:

1. Read the source. Extract its core themes. **Do not modify the original.**
2. Create or update the right typed nodes (concept / entity / comparison),
   guided by `SCHEMA.md`.
3. **Cross-link with `[[wikilinks]]`.** This is the single rule that makes the
   graph exist. Each new node must link to at least one existing node, and
   incoming concepts should be linked from related nodes. A node with zero links
   is an orphan and a failure.
4. Bind key conclusions to their source: cite `raw/articles/<file>.md`.
5. Mark anything that's your inference or unconfirmed as **`待验证`
   (to-verify)** — never launder a guess as fact.
6. Update `index.md` (add notable new nodes) and, if it fits, the relevant
   `moc/` map.
7. Append a `log.md` entry: date, source, files created/updated, anything
   flagged to-verify.
8. **Run the verification pass** (below) and report exactly which files you
   created and updated.

## Command: organize the inbox ("整理 inbox")

When the user has dumped material into `raw/` (or an `Inbox/`) and says
"organize" / "整理":

1. List the unprocessed files.
2. For each, run the ingest flow above — classify into a typed node, wikilink,
   cite source, flag to-verify items.
3. Update `index.md` and `log.md` once for the batch.
4. Run the verification pass and summarize: how many processed, into which
   types, and any items needing the user's judgment.

If you are unsure where something belongs, **stop and ask** rather than forcing
a guess. A wrong classification pollutes the graph quietly.

## Command: query / assist writing

- **Query:** consult `index.md` to locate relevant nodes, read them, answer with
  sources cited (which node each claim came from).
- **Writing:** gather material via `index.md` and the relevant nodes, draft, and
  save the output under `drafts/`.

## The verification pass (the Loop Engineering core)

Every ingest/organize run ends here. This is what separates a trustworthy vault
from "a pile of new AI clutter." Run the bundled checker:

```bash
python3 ~/.claude/skills/loop-wiki/scripts/verify_wiki.py "$WIKI_PATH"
```

It checks the **machine-verifiable completion criteria**:

- no orphan nodes (every concept/entity/comparison has ≥1 wikilink),
- no broken wikilinks (every `[[target]]` resolves to a file),
- no duplicate stems (no two files share a basename, which would make
  `[[name]]` resolve ambiguously),
- every synthesized node (`concepts/`, `comparisons/`) cites a `raw/` source,
  so conclusions stay traceable to evidence,
- `index.md` and `log.md` were updated this run,
- to-verify items are explicitly marked, not silently dropped.

**Guard against Goodhart's law.** The goal is a *trustworthy, connected graph* —
not a green checkmark. Never satisfy the checker by deleting content, deleting a
failing source, removing a to-verify flag, or fabricating a link to a node that
isn't really related. If the checker can't pass honestly, report what's wrong
and let the user decide. Gaming the verifier is the one failure mode this whole
skill exists to prevent.

If the checker fails, fix the *real* gap (add the missing link, update the log)
and run it again. That retry-until-honestly-green behavior is the loop.

## Initialize a vault

If `WIKI_PATH` points at a vault with no `SCHEMA.md`, scaffold it:

1. Read `references/vault-structure.md` for the folder layout and the rationale.
2. Create the folders and the three control files, using
   `references/schema-template.md` as the starting `SCHEMA.md`.
3. Tell the user to open the folder in Obsidian via **Open folder as vault**
   (the whole vault, not a subfolder) so the graph view and backlinks work.
4. Do **not** auto-ingest on first run. Confirm the structure with the user,
   then ingest 3–5 items as a trial before scaling up to papers and transcripts.

## Operating principles (carry these into every run)

- **Schema before content.** A stable rulebook is what lets the Agent maintain
  the vault without drifting. Give rules, then material.
- **Wikilinks are non-negotiable.** No double-links, no graph — pages stay
  islands. This is the lesson the Obsidian "second brain" writers repeat most.
- **Everything traceable.** `log.md` is what makes an AI knowledge base auditable
  instead of a black box. Future-you needs to know where each node came from.
- **Human judges, Agent compiles, Obsidian stores.** You wire and link; the
  person decides what's true and what to keep; Obsidian renders the graph.
- **Define "done" so a machine can check it.** A vague goal ("optimize my
  notes") produces vague work. The verification pass is your definition of done.
