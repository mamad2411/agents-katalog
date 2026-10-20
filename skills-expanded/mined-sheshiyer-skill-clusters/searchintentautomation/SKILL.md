---
name: searchintentautomation
description: Use when turning a niche, offer, product, or topic into a keyword map, audience question map, and an agent-executable workflow using Ubersuggest, AnswerThePublic, Playwright MCP browser capture, and Python orchestration. Also use when extracting repeatable market-research workflows from reels, demos, or creator tool stacks and rewriting them into non-interactive CLI-agent pipelines.
cluster: growth-seo
version: 1.0.0
---

## Customization

**Before executing, check for user customizations at:**
`~/.Codex/skills/PAI/USER/SKILLCUSTOMIZATIONS/SearchIntentAutomation/`

If this directory exists, load and apply any `PREFERENCES.md`, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# SearchIntentAutomation

Turn a seed topic into an actionable research and automation workflow.

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| Extract a reusable workflow from a reel or creator demo | `Workflows/ExtractFromSource.md` |
| Build a keyword, question, and automation stack for a topic or offer | `Workflows/BuildOpportunityMap.md` |
| Run the workflow end-to-end with CLI coding agents | `Workflows/RunWithCliAgents.md` |

## Quick Reference

- Step 1: Use `Ubersuggest` to map demand, keyword variants, SEO opportunities, and competitor gaps.
- Step 2: Use `AnswerThePublic` to map real audience questions, comparisons, and prepositions around the same seed term.
- Step 3: Use `Playwright MCP` to capture browser-only research data and a Python CLI pipeline to normalize, merge, and route outputs.
- Step 3a: Hand off browser results with the capture manifest contract in `Tools/CaptureStatusContract.md`.
- Step 4: Optional AI layer: generate content briefs or landing-page drafts from the validated keywords/questions.
- If the pipeline gets stuck, stop and present a taxonomy-based checkpoint with:
  - Recommended option 1
  - Recommended option 2
  - Custom user direction

## Loaded Context

- Reel evidence and extraction trace: `ReelEvidence.md`
- Core workflow details: `Workflows/BuildOpportunityMap.md`
- Non-interactive agent execution: `Workflows/RunWithCliAgents.md`
- Failure and checkpoint taxonomy: `FailureTaxonomy.md`
- Playwright-to-Python handoff contract: `Tools/CaptureStatusContract.md`
