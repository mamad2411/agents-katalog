---
name: grillme
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions in Russian, one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.

When the interview is complete and no blocking questions remain, switch to the `okf` skill workflow and record the user's answers as structured OKF documents. Follow all OKF rules from `AGENTS.md` and the `okf` skill workflow: inspect the existing bundle first, preserve stable concept IDs, create or update only evidence-backed concepts, use valid YAML frontmatter, prefer relative Markdown links, regenerate required indexes/graph outputs when concepts are added, removed, or renamed, and validate the bundle before finishing.

Do not invent missing requirements, schema details, citations, source paths, or domain facts. If the interview reveals unresolved gaps, write them explicitly as gaps or open questions in the OKF output rather than filling them in.
