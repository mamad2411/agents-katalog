---
name: foss-equivalent-architecture
description: >-
  Research a proprietary AI/software feature, decompose it into component
  capabilities, audit your existing stack for overlap, identify FOSS
  alternatives, and produce a build roadmap with phases.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, architecture, FOSS, competitive-analysis, ai-capabilities]
    triggers:
      - how does X work
      - can we build Y
      - what is the FOSS alternative
      - map out the entire capability
      - recreate X using open source
      - build equivalent of X
      - competitive analysis
      - go over this convo
      - map out all discussed features
      - analyze this conversation
      - report back on this share
      - grok conversation
      - research conversation
      - map this to our app
    related_skills:
      - infrastructure-self-healing-pulse
      - hermes-agent
---

# FOSS Equivalent Architecture

A systematic process for taking a proprietary AI/software capability,
understanding its components, and designing a FOSS equivalent that
can be built in-house.

## When to Use

- A major AI vendor (OpenAI, Anthropic, Google, Meta) ships a new capability
- You want to understand whether to buy, build, or integrate
- The user says "map out how we can create the same functionality using FOSS"
- The user provides an **existing research conversation** (Grok share, ChatGPT link, Claude share) and says "go over this convo and map it to our app"
- The user says "analyze this conversation", "map out all discussed features", "report back on this share link"

## The Process

### Variant A: Fresh Research (default)
Use when the user has not already researched the topic or provided a research source. You do the full investigation.

### Variant B: Analyze Existing Research Conversation
Use when the user provides an **already-completed research conversation** (Grok share URL, ChatGPT share link, Claude artifact) and wants you to extract learnings, map features, and audit against the existing codebase.

1. **Extract the conversation content**:
   - Navigate to the share URL using browser tools (Playwright or Chrome DevTools MCP)
   - Grok share URLs (`https://grok.com/share/...`) render as web pages — use `mcp_playwright_mcp_browser_navigate()` + `mcp_playwright_mcp_browser_snapshot()` to read the full conversation
   - **Pitfall:** Grok share pages are interactive web apps, not static Markdown. The Playwright browser tools handle them well. The built-in `browser_navigate` tool (CDP-based) may fail with "CDP WebSocket connect failed" — use the Playwright MCP browser tools instead.
   - ChatGPT/Claude share links may be simpler HTML or JSON. Try `curl` or `web_extract` first for non-interactive pages.
   - Extract every user question and every assistant response — they contain the research findings you need

2. **Decompose into a feature list**:
   - Read the conversation through the lens of "what capabilities are being discussed?"
   - For each user question, identify the core need
   - For each assistant response, extract: feature name, how it works technically, FOSS alternatives mentioned, implementation difficulty, compliance risks
   - Categorize: what's a feature? what's a data source? what's a compliance concern? what's an architecture pattern?
   - Create a table: Feature | How It Works | FOSS Alternative | Risk Level

3. **Audit existing codebase**:
   - For each feature: does the project already have it? (✅ Built, 🟡 Partial, ❌ Missing)
   - Read key source files to check actual implementation, not just file names
   - Note what's already wired up vs what's skeleton/stub code
   - Identify things the user has already built that the convo says doesn't exist — those are competitive advantages

4. **Add architecture context**:
   - Check existing skills and references for the project to understand the full system
   - Map data sources (The Odds API, Kalshi, Polymarket) against the existing codebase structure
   - Note compliance/latency/regulatory considerations from the convo that might block certain approaches

5. **Structure the output document**:
   ```
   # [Topic] — Features Analysis
   ## Overview
   ## 🟢 Already Built
   ## 🟡 Partially Built / Needs Work
   ## 🔴 FOSS Opportunities (each with: How It Works | Strategy | Priority)
   ## Architecture Map (ASCII diagram)
   ## Priority Implementation Roadmap
   ## Compliance & Risk Notes
   ## Conclusion
   ```

6. **Save for future reference**:
   Store the analysis document under the project's skill (e.g., `ai-sharp` skill's `references/` directory) or in the project's `docs/` folder, then commit it:
   ```bash
   git add docs/[topic]-features-analysis.md && git commit -m "Add [topic] features analysis" && git push
   ```

### Phase 1: Research the Original Feature (Variant A — Fresh Research)

Use this when you don't have an existing research conversation to work from.

1. **Primary source**: Read the official announcement/blog post/vendor docs
   - What does the feature actually do? (not just the marketing claim)
   - What are the user-facing capabilities?
   - What are the system requirements?

2. **Secondary sources**: Search for analysis, deep-dives, critiques
   - Developer blogs, HN threads, Reddit
   - Technical limitations the vendor doesn't emphasize
   - Community reception

3. **Decompose into components**:
   - List every sub-capability the feature provides
   - Identify the data flow (inputs → processing → outputs)
   - Identify the infrastructure needed (storage, compute, networking)
   - For AI features: identify the model, the data, the prompt pipeline,
     the evaluation layer, and the debugging/observability layer

### Phase 2: Audit Your Existing Stack

1. **Check state.db schema** — what data is already captured?
   - `sessions` table: session metadata, costs, timing, parent hierarchy
   - `messages` table: every turn, tool calls, reasoning chains, token usage
   - FTS5 search: full-text across all content

2. **Check existing skills** — what patterns already exist?
   - Cron jobs, MCP servers, reference docs
   - Existing tools like `session_search`, `delegate_task`

3. **Identify gaps** — what's missing between what you have and the target feature?

### Phase 3: Identify FOSS Alternatives

Research and rank by maturity:

| Tier | Description | Examples |
|------|-------------|---------|
| **Tier 1 (Mature)** | Production-ready, self-hostable, active community | Langfuse, Arize Phoenix |
| **Tier 2 (Specialized)** | Focused on one aspect, good at it | OpenLLMetry, Braintrust |
| **Tier 3 (Building Blocks)** | Infrastructure components | OpenTelemetry, MLflow |

For each alternative, evaluate:
- **License** — MIT/Apache vs AGPL vs proprietary
- **Self-hosting** — Docker/K8s/standalone
- **Core capabilities** — does it have the feature you need?
- **Missing pieces** — what would you still need to build?

### Phase 4: Produce Architecture Document

Structure the output as a markdown file with:

1. **What the proprietary feature does** — concise, technical
2. **What you already have** — state.db, existing tools, MCP servers
3. **FOSS alternatives landscape** — ranked table
4. **Architecture diagram** — component map (text-based or SVG)
5. **Implementation roadmap** — phases with weeks and deliverables
6. **Key decisions** — trade-offs, build vs integrate decisions

### Phase 5: Save for Future Reference

Write the architecture document to the project's `docs/` folder (so it lives in git):

```markdown
git add docs/<topic>-features-analysis.md
git commit -m "Add <topic> features analysis"
git push
```

Also save under an existing skill's references for agent discovery:

```python
# Save under an existing skill that matches the domain
skill_manage(action='write_file',
    name='<relevant-umbrella-skill>',
    file_path='references/<topic>-architecture.md',
    file_content=architecture_doc)
```

If the document describes a system that crosses multiple domains, store it
in the `hermes-agent` skill's references or create a dedicated skill group.

### Phase 6: Implement Phase 1 Immediately

The analysis document identified highest-priority FOSS features. **Build the top item now** — don't stop at documentation. This session produced a 180-check QA-certified SharpSports replacement with vault, scrapers, normalizer, and sync engine.

Implementation pattern:
1. Identify the highest-priority feature from the roadmap
2. Build all supporting modules in parallel (vault + scrapers + normalizer + sync engine)
3. Wire into existing API layer
4. Create ad-hoc verification script with `tempfile`
5. Fix bugs found during QA (expect to fix 1-3 per 100 checks)
6. Commit and push with comprehensive message
7. Re-verify the fixed bugs with a targeted script

## Output Template

```markdown
# <Feature> — FOSS Architecture

## What <Vendor>'s Feature Does
- Core capability
- User-facing UX
- System components

## What We Already Have
- State.db tables/schemas
- Existing tools/MCP servers
- Existing skills

## FOSS Alternatives Landscape
| Tool | Maturity | Record | Replay | Diff | Self-Host |
|------|----------|--------|--------|------|-----------|

## Architecture Diagram
<text-based component diagram>

## Implementation Roadmap
### Phase 1 (Week X-Y): <Name>
- [ ] Task A
- [ ] Task B

### Phase 2 (Week Y-Z): <Name>
- [ ] Task C
- [ ] Task D
```

## Pitfalls

- **Don't over-research** — 3 FOSS tools max, go deep on the top 1-2
- **Don't just describe, produce artifacts** — write the architecture as a file
- **Don't assume 'easiest to integrate' = 'right priority'** — The user may want the HARDER option that covers their actual use case. When you find an easy API integration (Kalshi/Polymarket with official docs) and a hard scraper-based approach (DraftKings/FanDuel with Playwright/automation), LIST BOTH and let the user pick. Don't default to the easiest one to code. The user explicitly corrected this priority: "no, we build the full SharpSports replacement first, prediction markets later." Lead with options, not with what's easiest to implement.
- **Audit first, design second** — don't propose building what already exists
- **Build vs integrate decision** — for each component, decide: build in-house, integrate FOSS, or use a managed service. Default to integrate unless there's a clear reason to build.
- **Rank by maturity** — Langfuse is 10k+ stars for a reason; don't lead with a 200-star side project
- **Verify the license** — some "open source" tools have restrictive licenses (Elastic, BSL, Confluent Community)
- **Check self-hosting docs** — Langfuse is easy to self-host (Docker + Postgres); Arize Phoenix is even simpler (pip install + one command)
