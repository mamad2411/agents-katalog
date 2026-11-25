# OSIA Framework

“Open Source Intelligence Agency” orchestration framework: event-driven multi-agent routing with a Chief of Staff that assigns tasks to specialist “Desks,” each with its own prompt + model config + vector collection (Qdrant). The architecture diagram emphasizes a research loop (multiple sources/tools), RAG context building (desk collection + cross-desk fan-out + “boost” collections like CVE/MITRE/WikiLeaks, etc.), and a final synthesis desk (“Watch Floor”) that dispatches briefings via Signal and writes analysis back into collections. Notable design choice: it uses “uncensored” models for routing / certain desks to avoid misrouting/sanitization on sensitive topics, with explicit fallback models and scheduled digest/SITREP jobs.

## Triggers
- "osia framework"
- "open source intelligence agency"
- "chief of staff desk"
- "event driven multi agent"
- "qdrant vector collection"
- "sitrep dispatch"

## Description
OSIA Framework is an orchestration system for OSINT operations that uses a Chief of Staff to route tasks to specialist Desks. Each Desk has its own configuration, prompts, models, and vector collections (using Qdrant). The framework includes a research loop, RAG context building with boosted collections, and a Watch Floor desk for synthesis and dissemination. It employs uncensored models for certain tasks to avoid sanitization on sensitive topics, with fallback models and scheduled intelligence reports.

## Features
- Chief of Staff orchestration
- Event-driven multi-agent routing
- Specialist Desks with individual configurations
- Prompt and model configuration per Desk
- Vector collections using Qdrant
- Research loop architecture
- RAG context building
- Desk collection and cross-desk fan-out
- Boost collections (CVE/MITRE/WikiLeaks/etc.)
- Watch Floor synthesis desk
- Briefing dissemination via Signal
- Analysis write-back to collections
- Uncensored models for routing/sensitive desks
- Explicit fallback models
- Scheduled digest/SITREP jobs
- Structured, inspectable outputs

## Usage
Use when you need to orchestrate a team of AI agents for complex OSINT investigations that require multiple specialized approaches and structured intelligence production.

## Example
```
/osia-framework initiate investigation on cyber threat group
/osia-framework assign desk: GEOINT for location analysis
/osia-framework configure desk: CYBER with threat intelligence feeds
/osia-framework run research loop with CVE boost collection
/osia-framework generate SITREP via Watch Floor
/osia-framework dispatch briefing to Signal channel
```
