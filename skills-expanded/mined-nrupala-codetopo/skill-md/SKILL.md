<!--
SPDX-FileCopyrightText: 2026 2351485 ALBERTA INC.

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Skill: codetopo — structural questions about a codebase

Use this skill when you are an AI coding agent working in a repository
and you need **structural facts** — what calls what, what breaks if a
symbol changes, how two modules connect — before you edit, review, or
explain code.

## When to reach for codetopo instead of grep / find / raw reads

- "What calls this function?" / "What would break if I change this?" —
  reach for codetopo **before** editing a shared module. A grep for the
  name finds text matches; codetopo returns the resolved call graph.
- "How are these two modules connected?" — `codetopo_path` answers in
  one call instead of a chain of manual hops.
- "Where are the hotspots / most-depended-on symbols?" — `codetopo_rank`
  and `codetopo_metrics` measure the whole graph at once.
- Reach for grep instead when the question is about text (a string
  literal, a comment, a config value) — codetopo indexes structure, not
  text content.

## The workflow (counts first, files last)

1. **Index once.** `codetopo_index` the repository (Rust,
   TypeScript/JavaScript, Python, Kotlin, C, Java, Go, Shell, C++, Swift, Ruby, R, Julia, C#, PHP, Scala, Haskell, Elixir, and Lua are parsed). Keep the returned
   database path; every later call uses it.
2. **Check the diagnostics before trusting any count.**
   `codetopo_diagnostics` lists what the index could not resolve —
   unresolved calls, dependency cycles, multi-definitions. Counts are
   *resolved* counts: if diagnostics name unresolved calls near your
   target, say so in your answer instead of presenting the count as
   complete.
3. **Discover ids by name.** Exact-id queries need the node's id:
   `codetopo_search_symbols` finds it (the package prefix is the
   indexed directory's name, exactly as indexed).
4. **Ask for counts first.** Tools return aggregate-first answers —
   totals before lists. Read the count, decide if you need the list,
   then expand. Do not open source files to answer a question the graph
   already answered.
5. **Drill in only where the count points.** `codetopo_neighborhood`,
   `codetopo_get_symbol`, then — and only then — read the file.

## The questions agents actually ask

| Question | Tool |
|---|---|
| What breaks if I change X? | `codetopo_blast_radius` |
| What does X depend on / who depends on X? | `codetopo_descendants` / `codetopo_ancestors` |
| How do A and B connect? | `codetopo_path` |
| What are the hotspots? | `codetopo_rank`, `codetopo_metrics`, `codetopo_history` |
| What didn't the index resolve? | `codetopo_diagnostics` |
| Is this index trustworthy / portable? | `codetopo_verify`, `codetopo_snapshot` |

## English-profile graphs (documents, not code)

A snapshot with `profile_id: "english"` is a graph of English
text, in two storeys — treat the storeys differently:

- **Grammar edges** (`subject-of`, `object-of`, `complement-of`,
  `modifier-of`, `clause-of`, `appositive-of`,
  `coordinated-with`, `contains`) are parser measurements
  (spaCy; class `inference`). On dense technical prose ~87% of
  relations are right; the published audit is
  `docs/english-accuracy.md`. Quote them as measurements with
  that accuracy, never as facts about the text's meaning.
- **Claim edges** (`same-entity`, `frames`, `supports`,
  `states-thesis-of`) are a named reader's interpretation
  (class `declared_claim`). Each carries `claimant` and
  `basis` — cite both when you use one. If YOU add a claim edge
  (coreference, claim structure), you are the claimant: put
  your name in `claimant` and your grounds in `basis`. An
  unlabelled interpretation is a defect, not a contribution.
- An english graph is **claims-class**: never present it, or a
  count over it, as truth-class. Ground floors are produced by
  `tools/english-ingest`; it emits grammar only, by design.

## Rules of the house

- codetopo is read-only and domain-blind: it reports measurements with
  the method stated, never quality scores or opinions. Interpretation
  is your job; the graph's job is to make sure you interpret real
  numbers.
- MCP answers are identical to the CLI and HTTP answers by construction
  (same `codetopo-core` queries) — pick whichever surface your host
  gives you.
- Setup and install: `llms-install.md` in this repository (prebuilt
  binaries on the releases page; no toolchain needed for the MCP
  server).

---

*Agentic Packaging Standard conformance (2026-11-16): explicit
uncertainty — met (diagnostics are first-class output; see README
"What the graph does not claim"); composite task tools — open (the 20
tools are atomic; task-level composites are future build work);
agent onboarding — met by this file (+ `GEMINI.md`, `llms-install.md`);
zero-compile install — met for `codetopo-mcp`/`codetopo-acp` prebuilt
release binaries (CLI/server install via crates.io); measured traces —
met in part (`docs/scale-gate.md` measured record; a public
tool-call/token comparison trace is still open); terminal-story docs —
met (README example session shows real fixture output).*
