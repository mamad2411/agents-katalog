---
name: progressive-disclosure-agent-skills-evidence
description: Applies the first controlled evidence on progressive disclosure for long-document agents (arXiv:2607.17598, UC Davis/Zhejiang/HKU; LOONGDOC environment over ∞ Bench, three harnesses × three model families) — the harness-dependent rule: on a single book, a flat SKILL.md pack matches or exceeds raw navigation only when the agent cannot already locate passages itself, adds nothing for strong-navigator agents (Codex-style greps), never rewards a second routing level (and can collapse accuracy), and becomes decisive at library scale (20 books: raw open-QA 0.26 → flat 0.46). Core conclusion: progressive disclosure buys CONTEXT, not intelligence — package a document as ONE skill with a flat in-skill index; never as per-chunk child skills with always-loaded descriptions. Use when [deciding whether to wrap documentation or corpora as Agent Skills, designing SKILL.md structures for long documents, budgeting context for book-scale or multi-book agent tasks, or briefing on when skills beat retrieval]. NOT for [human progressive-disclosure UI patterns (use curiosity-gap-progressive-disclosure) or RAG pipeline design].
---

# Progressive Disclosure for Agents: What the First Controlled Study Shows

## Overview

Agent Skills (the standard that packages expertise as a folder rooted at a SKILL.md, loaded on demand) spread on engineering intuition before anyone measured them. The first controlled test compares three agentic reading approaches over the same book, holding chunk set and task instruction fixed so only the routing varies:

1. **raw** — hand the agent the raw document; it navigates (grep/read) however it likes.
2. **flat** — one SKILL.md; always-in-context description gates discovery, the body carries a chunk index, `references/` files load on demand.
3. **hierarchical** — every chunk is its own skill with an always-loaded description, plus a meta-router.

Findings across three harnesses (Codex, Pi, Claude-Code) and three model families:

- **On a single book, the gain is harness-dependent.** Flat matches or exceeds raw on weak-navigator harnesses (Pi, Claude-Code) but adds nothing under Codex, whose bare agent already greps for question entities and reads matched passages — it reconstructs locate-then-read retrieval on the fly.
- **Depth never pays.** The hierarchical pack ties or trails flat everywhere, and can collapse outright (En.MC 0.9126 → 0.6398; Zh.QA 0.7479 → 0.3890 on Pi): always-loaded child descriptions saturate the router's context before it commits to a chunk.
- **At library scale, the verdict flips in flat's favor.** Raw navigation collapses as K grows (En.QA 0.657 → 0.257 from K=5→K=20 on Codex; Zh.QA to near zero), while flat degrades more slowly and leads on all three subsets by K=20 (En.QA 0.462 vs 0.257). A pre-cut index lets the agent commit to the target book before burning context traversing the library.
- **Cost sharpens the verdict.** At K=20 raw reads ~68.3M tokens/question (~$52) for the worst accuracy; flat reaches nearly double the accuracy at roughly half the tokens and cost (32.5M, ~$25, uncached upper bound). The corpus frontier recedes down-and-to-right with scale: a larger library is strictly less efficient to read.
- **The retrieval baseline loses.** Hybrid-RAG trails raw and flat on qwen3.6-27b across all subsets (widest on open QA) — routing to a chunk through an in-skill index outscores the classical rerank-and-feed pipeline in most cells.

## When to Use

- Deciding whether to package documentation, manuals, or corpora as Agent Skills
- Choosing between one index and a hierarchy of child skills
- Estimating when a skill pack beats a raw file drop or a RAG pipeline
- Designing context strategy for agents over long or multi-document corpora

## Core Workflow

1. **Ship the flat pack as the default.** One SKILL.md; description always in context; body indexes chunks; `references/` files read on demand. One routing level is enough.
2. **Do not build per-chunk child skills.** The second level never helps on a single book and sometimes breaks accuracy; at library scale it reproduces the context pressure disclosure exists to relieve (always-loaded per-chunk summaries inflate the always-on budget).
3. **Match the mechanism to the corpus size.** Single document + capable agent → disclosure is redundant (controllable retrieval path at best). Corpus too large to navigate by reading → flat disclosure becomes an accuracy tool, sharpest on open QA.
4. **Expect task/language dependence.** Gains are sharpest on English open QA; multiple-choice books carry a pre-training confound (memorized canonical novels blunt the signal); Chinese QA showed neutral-to-negative effects where the base model, not the pack, sets the ceiling.
5. **Validate with a pilot before committing.** The complementary preregistered wiki study (arXiv:2607.04576, 709-page LLM-maintained wiki; 960-run ablation, byte-identical page bodies across arms) found a capable self-routing agent never loads the index at all — the retrofit's nominal saving (avoiding a 150KB index load) materialized only under catalog-preload; the real saving (~30% under enforced, ~34% free, ~58% forced; every CI excluding zero) came from more targeted access (pages cited 6.10→4.22; fewer tool turns) at non-inferior quality. Measure the actual access behavior, not the nominal mechanism.

## Key Evidence

- He, Zhao, Wang & Chen, "Is Progressive Disclosure All You Need for Long-Context Agents?" (arXiv:2607.17598): single-book and K∈{5,10,20} corpus-scaling results with a cost-accuracy Pareto frontier; trajectory inspection explains the harness dependence.
- Cochran, "Progressive Disclosure for LLM-Maintained Wiki Knowledge Bases: a Preregistered Ablation" (arXiv:2607.04576, July 6, 2026): quality non-inferior (A3−A0 = +0.01 composite, δ=0.5 margin), cost −30% (enforced), −34% (free), −58% (forced), mechanism = more targeted access, not index-load avoidance; honest deviations disclosed (reliability gate κ=0.23 vs planned 0.60; favorable-direction cost refutation of the preregistered null).
- Design-rule synthesis: curated/structure-derived skills help; model-authored skill text adds little; the always-loaded description is the load-bearing metadata (Zhang et al., 138K SKILL.md audit).

## Pairs with

- `mcp-code-execution-agent-efficiency` (progressive disclosure via filesystem exploration for MCP tools)
- `agent-experience-ax-devex-evolution` (codebase-as-source-of-truth; progressive disclosure for machines)
- `hyperlayered-hypertext-agentic-reading` (what the route and layers should contain, this skill's structural sibling)
- `recursive-language-models` (the alternative long-context strategy)
- `knowledge-activation-atomic-knowledge-units` (the institutional-knowledge framing)

## A-Tech Alignment

- **Open source:** the Agent Skills pattern and the LOONGDOC evaluation environment are open; every A-Tech product can adopt the flat-pack default without proprietary infrastructure.
- **Privacy:** file-system-based disclosure keeps corpus access local and auditable; no external retrieval index required.
- **Financial freedom:** the flat pack is both the more accurate AND the cheaper choice at scale — halving token cost while doubling accuracy is a direct margin lever.
- **Practical:** the packaging recipe (chunk by document structure; per-chunk descriptions + key-element lists into the in-skill index; temperature-0 deterministic metadata) is a one-day build per corpus.

## Sources

- He, Y., Zhao, Y., Wang, J. & Chen, H. "Is Progressive Disclosure All You Need for Long-Context Agents?" arXiv:2607.17598 (LOONGDOC environment; ∞ Bench; Codex/Pi/Claude-Code × gpt-5.4-mini, qwen3.6-27b, claude-haiku-4.5; hybrid-RAG baseline).
- Cochran, T.O. "Progressive Disclosure for LLM-Maintained Wiki Knowledge Bases: a Preregistered Ablation." arXiv:2607.04576 (OSF preregistration feka7; content-parity gate; cross-family judge).
- Caveats: En.MC pre-training confound (canonical novels); corpus-scale axis bracketed coarsely (K ≤ 20); gains task- and language-specific; single chunking recipe; several comparisons within one standard error.