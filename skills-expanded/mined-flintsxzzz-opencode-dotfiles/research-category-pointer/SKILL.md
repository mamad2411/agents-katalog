---
name: research-category-pointer
description: "Pointer to a library of 14 specialized Research skills. Use when working on research-related tasks."
risk: none
---

# Research Capability Library 🎯

This is a **pointer skill**. The 14 specialized Research skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **deepapi** — Use DeepAPI for supported scraping, research, and email workflows with explicit credentials and approval.
- **dsh-deepread** — Use for evidence-first reading of articles, books, PDFs, web pages, or document sets, with knowledge maps and Feynman checks.
- **entropy-box** — Entropy Box knowledge-compiler for embodied-AI: turns bounded requirements into grounded workflows via Solution Consult, Search, Lookup, and Evidence. Do not use it to control physical robots.
- **fact-check-x-complete** — Compare claims from one or more AI answers, verify their citations against public primary sources, and produce an evidence-linked fact-check report without installing a bundled browser runtime.
- **gemini-deep-research** — Run autonomous multi-step research with Google's Gemini Deep Research Agent: kick off a query, poll progress, and collect a cited report for market analysis or literature reviews.
- **ii-commons** — Deterministic search across arXiv, PubMed/PMC, and US policy corpora with daily freshness cutoffs.
- **multi-source-search** — Cross-validate web research and produce an offline-checkable evidence ledger with explicit source diversity, confidence, conflicts, and gaps.
- **news-sentiment-engine** — Multi-source RSS news aggregation with Claude-powered sentiment analysis and structured briefing output
- **papers-skill** — Skill for academic research workflows: search Semantic Scholar (200M+ papers), inspect citations, download arXiv PDFs, and extract PDF text. Bundles a self-contained Python CLI.
- **people-data** — Research LinkedIn professional profiles and public business-contact data, including email/phone lookup, people search, and YouTube channel business-email discovery.
- **pi-web-search** — Give Pi Agents a safe web-search and fetch workflow using the installed pi-web-access package.
- **research-prompt** — Turn vague research needs into one precise deep-research prompt with context and output criteria.
- **survey-generator** — Generate source-backed AI/ML survey paper artifacts with curated bibliographies and Fireworks/Kimi HTML rendering.
- **youtube-transcript** — Fetch YouTube transcripts through DeepAPI or local fallback tooling and save clean text output.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/research/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/research`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
