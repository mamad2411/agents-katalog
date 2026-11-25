---
name: topic-research-brief
description: Multi-round web research on a topic, synthesised into a cited brief and saved as a structured vault note.
---

Run several rounds of web research on a topic, cross-check the sources, and write a cited research brief into the vault as a structured wiki note that the RAG pipeline can index.

> Placeholders: `{{RESEARCH_TOPIC}}` = the subject to research, `{{VAULT_PATH}}` = vault path (the `VAULT_PATH` env var), `{{EIDETIC_OS}}` = repo path. Any API keys (web-search provider, embeddings/LLM endpoint) come from env vars such as `SEARCH_API_KEY` / `LLM_BASE_URL` — never inline a credential.

**Objective:** Produce a balanced, well-sourced brief on `{{RESEARCH_TOPIC}}` in 2–3 research rounds, save it as a dated note under the vault wiki, and re-index so the new note is searchable.

**Step 1 — Gather sources (multi-round web research):**

1. Round 1 — broad scan. Run an MCP web-search for `{{RESEARCH_TOPIC}}` to map the landscape: key facts, main viewpoints, recurring sources, open questions.
2. From round 1, derive 3–5 sharper follow-up queries (definitions, latest developments, counter-arguments, primary data, credible critics).
3. Round 2 — depth. Run a web-search per follow-up query and fetch the most promising results with the MCP web-fetch tool to read past the snippet.
4. Round 3 — verification (only where it matters). For any load-bearing or contested claim, find a second independent source. Prefer primary sources, official docs, and reputable outlets over aggregators.
5. For every source you keep, record: title, publisher, publication date, URL, and the specific claim it supports. Note the date each fact was checked.
6. Discard low-quality, undated, or unverifiable sources. Flag anything you could not corroborate rather than presenting it as settled.

**Step 2 — Build the brief (synthesise, cite, save):**

1. Synthesise across sources — do not paste raw search results. Resolve agreement, surface genuine disagreement, and keep your own commentary clearly separated from sourced facts.
2. Write the note to `{{VAULT_PATH}}/wiki/research/{{RESEARCH_TOPIC}}-[YYYY-MM-DD].md` (slugify the topic for the filename) using the MCP file-write tool, with this structure:
   - YAML frontmatter: `title`, `date`, `tags: [research, brief]`, `topic: {{RESEARCH_TOPIC}}`, `status: draft`
   - **Summary** — 3–5 sentence TL;DR a reader can absorb in 30 seconds
   - **Key findings** — bullets, each ending with an inline citation `[n]`
   - **Context / background** — what a newcomer needs to follow the findings
   - **Open questions & uncertainties** — what is contested, thin, or unverified
   - **Sources** — numbered list `[n] Title — Publisher (date) — URL`, matching the inline `[n]` markers
   - **Related notes** — wikilinks to existing vault notes on adjacent topics, if any
3. Keep claims traceable: every factual statement in the findings maps to a numbered source. If a claim has no source, label it as your inference.

**Step 3 — Index and confirm:**

1. Re-index the vault so the new note is searchable:
   - Incremental: `EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic embed` (routes through the CLI so the run is audited; reads `VAULT_PATH` from the env)
2. Confirm the note exists at the expected path and that the embed run reported it as added/modified.
3. Output a short run summary: note path, source count, number of rounds, and any claims left flagged as unverified.

**Constraints:**
- Unattended run — make reasonable judgement calls; do not stop to ask for input.
- Only write the single new note under `wiki/research/` — never modify existing notes.
- Cite everything; mark uncertainty honestly rather than overstating confidence.
- Never inline credentials — read them from env vars.
