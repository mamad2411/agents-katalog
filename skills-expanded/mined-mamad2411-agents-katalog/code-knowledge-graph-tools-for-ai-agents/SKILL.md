---
name: code-knowledge-graph-tools-for-ai-agents
description: >
  Compares GitNexus, Graphify, and CodeGraph — tools that precompute a
  structural knowledge graph of a codebase and expose it to AI coding agents
  via MCP, replacing repeated grep/file-read exploration with direct
  impact-radius, call-chain, and dependency queries. Use when a user asks to
  "give my coding agent a code graph," "reduce how many tool calls/tokens my
  agent burns exploring the repo," "set up GitNexus/Graphify/CodeGraph,"
  "find an MCP tool for codebase structure," or is choosing between these
  three tools based on license, language coverage, or query model.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Code Knowledge Graph Tools for AI Agents

## Purpose

An AI coding agent without any precomputed structural index explores a
codebase the same slow way every time: repeated `grep`, file reads, and
directory listings to reconstruct facts (what calls this function, what
would break if I change this type, what's the blast radius of this file)
that are stable properties of the code and don't need to be rediscovered on
every session. Code-knowledge-graph tools solve this by parsing the
codebase once into a structural graph (or graph-like index) — call graphs,
type relationships, module dependencies — and exposing queries over that
graph to the agent via MCP tools, so a question like "what depends on this
function" becomes one precomputed lookup instead of a multi-step
grep-and-read exploration the agent has to redo from scratch each time.
This is a distinct concern from a RAG pipeline's semantic retrieval over
document/code *text*
([rag-pipeline-design](../rag-pipeline-design/SKILL.md)) and from operating
a general-purpose vector database
([vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)):
a code knowledge graph indexes *structure* (calls, references, definitions,
dependencies), not just embedding-similar text chunks, though some of these
tools combine both. This skill compares three current tools in this space —
GitNexus, Graphify, and CodeGraph — on architecture, language coverage,
query model, and licensing, and covers choosing between them and wiring the
one you pick into an agent via MCP
([mcp-server-development](../mcp-server-development/SKILL.md) covers
building an MCP server generally; this skill covers consuming these three
specific pre-built ones).

## When to use

- An AI coding agent repeatedly burns tool calls and tokens re-exploring the
  same codebase structure (grep for callers, read files to trace a type)
  across sessions, and you want to give it a precomputed structural index
  instead.
- Deciding which of GitNexus, Graphify, or CodeGraph fits a given
  repository's language mix, size, and licensing constraints (open-source
  vs. commercial product).
- Setting up impact-radius or blast-zone analysis before a refactor — "what
  breaks if I change this function's signature" — as a query an agent can
  run directly rather than inferring from manual exploration.
- A codebase includes non-code artifacts (design docs, PDFs, recorded
  walkthrough videos) that should also be queryable alongside code
  structure, favoring a tool that ingests more than source files.
- Evaluating whether a commercial product can adopt one of these tools,
  which requires checking each tool's license (GitNexus's noncommercial
  license is a real blocker for commercial use without a paid tier; Graphify
  and CodeGraph are fully permissive).

## Prerequisites & environment

- Node.js and `npx` availability for GitNexus (`npx gitnexus analyze && npx
  gitnexus setup`).
- The `uv` Python package/tool manager for Graphify (`uv tool install
  graphifyy`).
- A Rust-toolchain-built binary or published release for CodeGraph (it is
  itself implemented in Rust for its parsing kernel — no Rust toolchain is
  required on the *consuming* machine unless building from source).
- An MCP-compatible agent host (Claude Code, Cursor, GitHub Copilot, Gemini
  CLI) configured to connect to the tool's MCP server, per each client's own
  MCP configuration mechanism.
- Disk space for the generated index: GitNexus stores its embedded
  graph+vector database (LadybugDB) under a `.gitnexus/` directory in the
  repo; Graphify's and CodeGraph's index storage location should be
  confirmed against each tool's current documentation before assuming a
  fixed path.
- For Graphify's documentation/PDF/video ingestion: access to the user's
  own configured AI model (Graphify uses it as part of ingestion) and a
  local `faster-whisper` transcription setup for video content — this is a
  heavier prerequisite than pure source-code parsing and should be scoped
  in before enabling it on a large corpus of recorded content.
- Legal/procurement sign-off before adopting GitNexus for any commercial
  codebase — its license (PolyForm Noncommercial 1.0.0) permits open-source
  and non-commercial use only; commercial use requires a paid enterprise
  tier. This is not a fully permissive open-source license and should be
  flagged to whoever approves tooling for a commercial product, the same
  way you'd flag a GPL/AGPL dependency in
  [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md).

## Step-by-step guidance

1. **Understand what each tool actually indexes and how, before choosing:**
   - **GitNexus**: uses Tree-sitter to extract an AST across 14 languages,
     then stores the resulting structure in **LadybugDB**, an embedded
     graph+vector database, persisted under a `.gitnexus/` directory in the
     repository. It exposes **17 MCP tools** for queries like impact-radius,
     call-chain, and blast-zone analysis — i.e. the query surface is
     deliberately broad and granular (many narrow tools rather than one
     general one).
   - **Graphify**: uses tree-sitter across **36+ languages** — a wider
     language surface than GitNexus — and additionally ingests
     documentation, PDFs, and video (video transcribed locally via
     `faster-whisper`, using the user's own configured AI model as part of
     ingestion). It clusters the resulting structure using **Leiden
     community detection** (a graph-clustering algorithm that groups
     densely-connected nodes into communities), and exposes a CLI-style
     query surface: `graphify query`, `graphify path`, `graphify explain`.
   - **CodeGraph**: implemented with a Rust-powered parsing kernel across
     **20+ languages**, storing the result in a local **SQLite database
     with FTS5** (SQLite's full-text search extension) rather than a
     dedicated graph database. It exposes a single primary MCP tool,
     **`codegraph_explore`**, and includes a **live file-watcher** that
     auto-syncs the index as files change, rather than requiring a manual
     re-index step.

2. **Install and index the codebase** with the chosen tool:
   ```bash
   # GitNexus
   npx gitnexus analyze && npx gitnexus setup

   # Graphify
   uv tool install graphifyy
   graphify query "..."      # query commands available after install/index

   # CodeGraph — consult the current release for the exact install command;
   # its file-watcher then keeps the SQLite/FTS5 index in sync automatically
   ```

3. **Wire the tool's MCP server into your agent host.** All three are
   designed to be consumed by an MCP-compatible agent — the exact client
   config (where you register the server command) is client-specific
   (Claude Code, Cursor, Gemini CLI, GitHub Copilot each have their own MCP
   config location); see
   [mcp-server-development](../mcp-server-development/SKILL.md) for the
   general client/server wiring pattern these tools' own MCP servers
   follow.

4. **Match the query granularity to the tool you chose.** GitNexus's 17
   distinct MCP tools mean an agent (or you, reviewing its tool calls)
   should expect fairly specific, purpose-named queries (e.g. a dedicated
   impact-radius tool vs. a dedicated call-chain tool) rather than one
   general-purpose entry point. CodeGraph inverts this: a single
   `codegraph_explore` tool is the primary surface, so most exploratory
   questions route through it rather than a large discrete toolset — fewer
   tool names for the agent to choose between, at the cost of a less
   explicitly named query surface. Graphify sits outside the MCP-tool-count
   framing entirely for its documented interface, exposing `query`/`path`/
   `explain` as CLI commands.

5. **Decide before adoption whether commercial use is in scope**, since
   this changes which tools are even eligible:
   - GitNexus is licensed under **PolyForm Noncommercial 1.0.0** for
     open-source/non-commercial use, with a **paid enterprise tier**
     required for commercial use. Treat this the same as you would any
     non-permissive dependency license found by an SCA/license scanner —
     flag it explicitly to whoever owns license compliance before adopting
     it inside a commercial product, rather than assuming "open-source
     tooling" implies free commercial use.
   - Graphify is **dual-licensed Apache-2.0 and MIT** — fully permissive,
     no commercial-use restriction.
   - CodeGraph is **MIT**-licensed — fully permissive, no commercial-use
     restriction.

6. **If the corpus includes non-code material** (design docs, PDFs, recorded
   architecture walkthroughs), Graphify is the only one of the three with
   documented ingestion for that content type (via the user's AI model plus
   local `faster-whisper` transcription for video) — GitNexus and CodeGraph
   are scoped to source-code parsing.

7. **If continuous freshness matters more than query breadth**, CodeGraph's
   live file-watcher auto-sync is a meaningful operational difference: the
   index updates as files change without a separate manual re-index step,
   which matters for an agent working against a codebase that's being
   actively edited in the same session (including by the agent itself).

8. **Where a measured before/after comparison exists, use it, and don't
   invent numbers for tools where it doesn't.** CodeGraph publishes a
   measured impact across 7 real-world repositories: **89% fewer tool
   calls, 60% lower cost, and 69% fewer tokens** versus agents operating
   without any such index. No comparable measured figures are given here
   for GitNexus or Graphify — do not assume or restate CodeGraph's numbers
   as if they apply to the other two tools; if a similar before/after
   comparison matters for your decision, run it yourself against your own
   codebase and agent workflow rather than assuming parity.

## Best practices

- Pick based on language coverage first if your codebase is polyglot:
  Graphify's 36+ languages is the widest of the three, CodeGraph's 20+ is
  next, GitNexus's 14 is narrowest — confirm your specific languages are
  covered before committing, since "covers most languages" claims vary in
  how current/complete support actually is per language.
- Treat GitNexus's license as a hard commercial-use gate, not a footnote —
  confirm with whoever owns license/legal compliance before using it on any
  codebase tied to a commercial product, and budget for the paid enterprise
  tier if commercial use is required.
- Prefer CodeGraph's live file-watcher when the agent is actively modifying
  the same codebase it's querying in one session — a stale index (requiring
  manual re-index) can give an agent confidently wrong structural answers
  mid-refactor.
- Don't adopt Graphify's documentation/PDF/video ingestion by default if all
  you need is code structure — it's a genuinely distinct, heavier
  capability (local transcription, additional AI-model calls at ingestion
  time) that's worth its cost only when the non-code corpus actually matters
  to the agent's task.
- Route an agent's exploratory "what does this touch / what calls this"
  questions through the code-graph tool's MCP interface first, before
  falling back to raw grep/file-read — that's the entire value proposition,
  and an agent still defaulting to manual exploration alongside an
  installed graph tool isn't getting the benefit either tool is meant to
  provide.
- Re-index (or confirm the file-watcher has caught up, for CodeGraph) after
  a large structural refactor before trusting impact-radius/blast-zone
  query results — a graph built against pre-refactor structure will give
  confidently wrong answers about the current codebase, the same staleness
  risk called out for RAG indexes in
  [rag-pipeline-design](../rag-pipeline-design/SKILL.md).

## Common pitfalls

- **Symptom:** A team adopts GitNexus for a commercial product's codebase
  without checking licensing, then discovers during a compliance review
  that commercial use requires a paid tier.
  **Fix:** Check the license (PolyForm Noncommercial 1.0.0) before
  adoption, not after — this is exactly the kind of license-compliance gap
  a dependency/SCA license policy should catch; treat it the same as any
  other non-permissive license finding in
  [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md)
  rather than discovering it downstream.

- **Symptom:** An agent given access to a code-graph tool's MCP server still
  falls back to grep/file-read exploration for structural questions the
  graph could answer directly, so tool-call/token savings don't materialize.
  **Fix:** Check that the tool's description in the MCP tool list makes
  clear *when* to prefer it over manual search (per the tool-schema clarity
  guidance in [mcp-server-development](../mcp-server-development/SKILL.md))
  — an ambiguous or under-described tool name is often the reason a model
  defaults to familiar grep/read behavior instead.

- **Symptom:** Impact-radius or blast-zone query results look stale or
  clearly wrong after a large refactor.
  **Fix:** Confirm the index has actually been rebuilt/re-synced since the
  refactor — GitNexus and Graphify require an explicit re-run of their
  analyze/index step unless documented otherwise for your version;
  CodeGraph's file-watcher should catch this automatically, but confirm it's
  actually running (not just installed) if results still look stale.

- **Symptom:** Graphify's documentation/PDF/video ingestion is enabled
  against a large archive of recorded meetings, and ingestion takes far
  longer and costs far more (in AI-model calls) than expected.
  **Fix:** This ingestion path uses local `faster-whisper` transcription
  plus the user's own configured AI model, so cost and time scale with the
  volume of non-code content processed — scope it to the specific documents
  or recordings that actually matter to the agent's task rather than
  ingesting an entire archive by default.

- **Symptom:** A team assumes CodeGraph's published 89% fewer tool calls /
  60% lower cost / 69% fewer tokens figures also describe GitNexus or
  Graphify's expected impact, and sets a similar expectation for those
  tools.
  **Fix:** Those figures are specific to CodeGraph's own measurement across
  7 real-world repositories versus agents with no index at all — there is
  no equivalent published figure here for GitNexus or Graphify; if a
  before/after comparison matters for the decision, measure it directly
  against your own codebase and agent workflow rather than assuming another
  tool's published number transfers.

## Worked example

**Scenario:** A team is choosing a code-knowledge-graph tool for an AI
coding agent that works across a polyglot monorepo (Go, TypeScript, Python,
plus some Rust services), with two decision factors: (1) the company's main
product is commercial, so licensing matters, and (2) the agent frequently
needs impact-radius answers ("what breaks if I change this function") while
actively refactoring in the same session.

Evaluation:

```
GitNexus  — 14 languages (covers Go/TS/Python/Rust if all 14 include them;
            verify each specific language is on the list), 17 MCP tools
            including dedicated impact-radius/call-chain/blast-zone
            queries, backed by LadybugDB in .gitnexus/.
            License: PolyForm Noncommercial 1.0.0 — BLOCKS use on this
            commercial product without purchasing the paid enterprise
            tier. Flagged to legal/procurement before proceeding further.

Graphify  — 36+ languages, widest coverage, plus doc/PDF/video ingestion
            this team doesn't currently need. Leiden clustering,
            query/path/explain CLI. License: Apache-2.0 / MIT — no
            commercial-use restriction.

CodeGraph — 20+ languages, single codegraph_explore MCP tool, SQLite+FTS5
            index, live file-watcher auto-sync — directly addresses the
            "actively refactoring in the same session" requirement since
            the index doesn't go stale mid-session. License: MIT — no
            commercial-use restriction. Published measured impact (89%
            fewer tool calls, 60% lower cost, 69% fewer tokens across 7
            repos) is the only one of the three tools with a stated
            before/after figure, though the team notes this was CodeGraph's
            own measurement, not an independent benchmark, and plans to
            spot-check it against their own agent workflow before relying
            on it as a hard expectation.
```

Decision: GitNexus is eliminated on licensing alone for this commercial
codebase. Between Graphify and CodeGraph, the team picks **CodeGraph** for
this use case specifically because of the live file-watcher (matching the
active-refactor requirement) and the permissive MIT license, while noting
Graphify's wider language coverage and non-code ingestion would make it the
better fit if the agent's task set expanded to include querying design docs
alongside code.

## Cross-references

- [mcp-server-development](../mcp-server-development/SKILL.md) — the general pattern for building and hardening an MCP server; these three tools each ship their own MCP server, so this skill is about consuming, not building, that surface.
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) — semantic retrieval over document/code text, a distinct concern from these tools' structural graph indexing; the two are complementary when a corpus needs both kinds of lookup.
- [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md) — operating the vector-store layer underneath a RAG pipeline, relevant if you pair one of these code-graph tools with a separate semantic-search index rather than relying on Graphify's built-in vector component alone.
- [agent-architecture-design](../agent-architecture-design/SKILL.md) — the general principle of giving an agent narrow, well-described tools; applies directly to how these tools' MCP surfaces (17 tools for GitNexus vs. one for CodeGraph) get selected correctly by a model.
- [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md) — the general discipline of checking dependency licenses before adoption, directly relevant to GitNexus's noncommercial license restriction.
