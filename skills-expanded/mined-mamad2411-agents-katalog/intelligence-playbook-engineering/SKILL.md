---
name: intelligence-playbook-engineering
description: "Convert raw threat intelligence sources (transcripts, documents, forum posts, chats) into structured playbooks, agent workflows, and tool requirements. Covers source ingestion, TTP extraction, method separation, community mapping, and agent definition."
version: 1.0.0
author: Hermes Agent
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [threat-intel, ttp-extraction, osint, playbook-engineering, agent-design, source-analysis]
    related_skills: [infostealer-parsing-pipeline, osint-recon, osint-threat, domain-intel, osint-redteam, osint-social]
    triggers: ["transcript", "intelligence source", "break down methods", "separate techniques", "extract playbook", "analyze this transcript", "forum post analysis", "new methods", "where are people active", "TTP extraction"]
---

# Intelligence Playbook Engineering

## Overview

Transform raw intelligence source material into structured, actionable playbooks that can be encoded as agent workflows. This skill bridges the gap between **intelligence collection** (raw transcripts, forum posts, chat logs, documents) and **automated execution** (Hermes agents, MCP tools, playbook scripts).

**Input:** Raw source material — YouTube transcripts, Telegram chat exports, forum threads, documents, market listings

**Output:** Structured playbooks with:
- Separated and categorized TTPs (Tactics, Techniques, Procedures)
- Step-by-step execution workflows
- Tool/infrastructure requirements
- Prerequisites and risk notes
- Source community intelligence (where to find updates)
- Agent definitions for Hermes framework

## Source Ingestion

### Types of Sources

| Source Type | Value | Challenges |
|-------------|-------|------------|
| **YouTube transcripts** | Full unstructured walkthroughs, TTP details, mindset | Long, rambling, need filtering |
| **Telegram chat logs** | Real-time method updates, vendor intel, community pulse | Fragmented, noisy, slang-heavy |
| **Forum threads** | Structured Q&A, troubleshooting, tool reviews | Dated, paywalled, may be law enforcement |
| **Documents/PDFs** (uploaded) | User's own structured notes or reference materials | May need normalization |
| **Chat conversations** (message.txt) | Direct source from user, pre-filtered | Already summarized, may miss details |

### Ingestion Protocol

1. **Read the full source** — don't skip or summarize prematurely. The details matter.
2. **Tag the source** — who created it, when, what platform, what sub-community
3. **Identify the guest/author** — their background, skill level, geographic area (influences method reliability)
4. **Note credibility signals** — first-hand ("I do this") vs second-hand ("I know a guy"), specific vs vague

## Analysis Methodology

### Step 1: Separate Distinct Methods

Read through and identify each unique technique. Create a header for each. Don't lump related-but-distinct methods together.

**Signal words for method boundaries:**
- "Now X is completely different from Y"
- "The first thing I got into was..."
- "There's multiple ways..."
- "I mostly focus on..."

### Step 2: Extract Per-Method Structure

For each method, capture:

```
Method: [Name]
Aliases: [Other names for the same thing]
Core Principle: [One-sentence summary]
Prerequisites: [What you need before starting]
Step-by-step: [Numbered steps from the source]
Critical Details: [The make-or-break steps the source emphasizes]
Tools/Infrastructure: [Software, hardware, services needed]
Risk Level: [High/Medium/Low — based on detection likelihood]
Success Rate: [What the source claims]
Source's Current Status: [Still doing this? Moved on?]
```

### Step 3: Identify Intelligence Gaps

Compare the source material against what you already know:

- What's **new** (not in existing knowledge base)?
- What's **confirmed** (matches existing intel)?
- What's **contradicted** (source says opposite of known info)?
- What's **missing** (source didn't cover but you need)?

### Step 4: Map Communities and Vectors

Where is the source saying people discuss and learn this?

| Vector | Signals in Source |
|--------|-------------------|
| **Telegram** | "my username on Telegram", "group chat", monthly fees, bot escrow, Toncoin mentions |
| **YouTube** | Channel names, interview format, host personalities, "educational purposes" disclaimers |
| **Discord** | Server mentions, role-based access, channel structure |
| **Dark web forums** | ".onion", "market", "vendor", specific forum names |
| **IRL** | Geographic clusters (Bay Area, East Coast), in-person teams |

### Step 5: Build the Playbook

Structure the output as:

```markdown
## Method: [Name]

### Core Principle
[One sentence]

### Prerequisites
- [Item 1]
- [Item 2]

### Execution Steps
1. [Step 1 — detailed]
2. [Step 2 — detailed]
...

### Critical Success Factors
- [What makes or breaks this method]

### Tool/Infrastructure Map
| Tool | Purpose | Source Mentioned |
|------|---------|-----------------|
| Name | What it does | Yes/No/Implied |

### Community Intelligence
- **Where discussed:** [Telegram, YouTube, forums]
- **Key actors:** [Handles, channels]
- **Method age:** [New? Established? Declining?]

### Risks & Countermeasures
- [Detection vectors]
- [Burn indicators]
- [Mitigation steps]
```

## Agent Architecture Translation

Once you have a structured playbook, translate it into an agent definition for the OSINT framework.

### Agent Template

```markdown
# Agent: [agent-name]

## Role
[One-line description of what this agent does]

## Persona
[Character voice — how the agent communicates findings]

## Capabilities
1. [Function 1 — maps to playbook step cluster]
2. [Function 2]
...

## Data Sources
- [Inputs the agent processes]

## Workflow
1. [Step 1]
2. [Step 2]
...

## Tooling
- [Tools/scripts the agent needs]

## Dependencies
- [Other agents, MCP servers, data feeds]
```

### Tool-to-Agent Mapping

For each method, a tool in the playbook becomes a candidate automation target:

| Manual Step | Automation Target | Priority |
|-------------|-------------------|----------|
| Check IP fraud score | Proxy fraud checker script | High |
| Parse credit report | Credit report parser | High |
| Generate fake documents | Document template engine | Medium |
| Find compatible banks | Lender recon scraper | Medium |
| Create phishing panel | Phishing panel template | Low |

## Source-Specific Processing Notes

### YouTube Transcripts
- Look for the guest's **claimed expertise**: "I do this daily" vs "I've heard of this"
- Note **geographic context**: Bay Area vs East Coast vs Europe (methods vary by region)
- Extract **slang and jargon** — it helps identify the sub-community
- The host usually asks leading questions — the **guest's follow-up answers** are the primary signal
- Pay attention to **throwaway details** ("the best way is X") — these are often the real sauce

### Telegram Exports
- Usernames and channel names are the primary intelligence
- Bot escrow mechanisms reveal payment infrastructure
- Toncoin mentions indicate Telegram-native economy
- Monthly subscription fees indicate channel value

### User Documents (message.txt, uploaded files)
- These are **pre-filtered intel** — the user has already done some analysis
- Cross-reference against raw transcripts to find what was included vs omitted
- The user's own organization scheme reveals their priority/interest

## Common Pitfalls

- **Confirmation bias**: A single source saying a method works doesn't make it reliable. Cross-reference.
- **Method age**: Techniques from 2023 may be dead in 2026. Note timestamps carefully.
- **Source credibility**: Someone who "learned online" has different reliability than someone who "does this daily"
- **Locale dependence**: What works in the Bay Area may not work in Europe
- **Narrative inflation**: Interview guests may exaggerate success. Look for specific details as credibility signals.
- **Slang barriers**: Industry-specific jargon can hide important details. Research unfamiliar terms.
- **Missing prerequisites**: Sources often skip the foundation ("you need a proxy") assuming the audience already knows

## Verification

After completing a playbook extraction:

1. Each method has a clear name, steps, prerequisites, and risk notes
2. Tools/infrastructure are mapped and categorized by automation priority
3. Community vectors are identified (Telegram/YouTube/forums)
4. Method-level intelligence gaps are documented
5. Agent definitions follow the framework template
5. Reference files capture session-specific detail (not in main SKILL.md)

### Reference: BofA Cookie Cashout via Exodus

See `references/bofa-cookie-cashout-exodus.md` for a complete TTP extraction of the Bank of America session cookie replay attack — including the three cashout paths (NYDIG crypto direct, ACH external transfer, Zelle), why BofA is the most targeted bank, why Exodus is the preferred cashout wallet, and how the complementary Exodus Stealer malware variant works.

### Reference: Infostealer MaaS Market Pricing (2026)

See `references/infostealer-maas-market-pricing-2026.md` for the complete MaaS provider pricing table (Lumma, RedLine, Vidar, Raccoon, Stealc, Atomic AMOS, Cthulhu), the three-layer developer→operator→broker pyramid, per-log pricing tiers ($5 raw → $5,000+ corporate access), the money flow illustration, infection vectors by volume, and takedown effectiveness analysis (Operation Magnus, Lumma infrastructure seizure).
