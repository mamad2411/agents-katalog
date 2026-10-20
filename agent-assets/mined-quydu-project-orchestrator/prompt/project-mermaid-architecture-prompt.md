---
mode: agent
description: Create an executive Mermaid architecture diagram for the current project grounded in repository evidence and business value.
---

# Project Mermaid Architecture Diagram

Create an executive-quality Mermaid architecture document for the current project using repository evidence, not generic template language.

## Objective

Develop a single architecture diagram that tells the story:

Business Need → User Interaction → Intelligence → Orchestration → Enterprise Systems → Governed Business Outcome

The audience should understand the solution purpose, architecture, intelligence, governance, and value within 30 seconds.

## Required repository evidence

Before authoring the diagram, read the current project’s primary evidence files and summarize the actual capabilities the repository supports. Use the project’s real intent and architecture rather than inventing features. At minimum, inspect:

- README.md
- docs/
- config/
- schemas/
- reports/
- pso.mjs
- .github/skills/**
- .github/copilot-instructions.md and AGENTS.md

If there are missing or conflicting signals, prefer the repository’s current operational guidance and machine-readable reports over narrative assumptions.

## Output location

Write the final result to:

- docs/PROJECT-ARCHITECTURE.md

The document must contain:

1. Architecture Summary
2. Mermaid Diagram
3. Executive Story

The Mermaid diagram is the primary deliverable.

## Required output format

Return exactly this structure in the document:

1. Architecture Summary
2. Mermaid Diagram
3. Executive Story

The Mermaid section must be one complete fenced code block, with no prose inside it. It must begin exactly with:

```mermaid
flowchart LR
```

Close the Mermaid code block with a standalone triple-backtick line before writing the Executive Story. Never place headings, bullets, or explanatory text inside the Mermaid fence.

The diagram must be renderable and presentation-ready.

## Architecture summary

Keep the summary to no more than 5 bullets. Cover the major architectural layers, main workflow, where AI reasoning occurs, where agentic orchestration occurs, where deterministic automation occurs, and where governance is enforced.

## Mermaid generation requirements

Generate a complete Mermaid diagram that follows these constraints:

- Use `flowchart LR`
- Use meaningful `subgraph` sections for logical domains
- Keep the architecture left-to-right and easy to scan in a 16:9 slide
- Prefer 12–24 primary nodes total
- Keep node names short and readable
- Label important arrows with concise verbs such as Requests, Reasons, Retrieves, Plans, Validates, Approves, Invokes, Automates, Executes, Monitors, Measures
- Distinguish AI reasoning from enterprise execution
- Show governance and security as visible controls around the flow
- Include explicit business outcomes in the outcome layer
- Use `classDef` styling consistently
- Avoid experimental Mermaid features and unsupported CSS
- Do not include implementation details like every API or microservice

## Business story and governance

The architecture must communicate a business story:

Users → Experience → AI Intelligence → Orchestration → Automation → Enterprise Systems → Business Outcomes

Governance must be visible and must influence the AI and orchestration layers. The diagram should show:

- Identity & Access
- Authentication
- Authorization
- Policy Enforcement
- Responsible AI
- Data Protection
- Compliance
- Audit / Observability
- Human Approval
- Guardrails

AI models must not directly execute privileged enterprise actions without an orchestrator, policy check, or automation layer.

## Presentation styling

Use a professional enterprise palette:

- Users & Personas: light blue
- Experience Layer: blue
- AI Services: violet
- Orchestration: deep blue
- Automation / Integration: cyan
- Data & Knowledge: teal
- Enterprise Systems: slate / gray
- Security & Governance: amber / gold
- Business Outcomes: green

Include a compact legend inside the Mermaid diagram, but do not let it dominate the architecture.

Add an executive title near the top of the diagram.

## Quality gate

Before finalizing, verify:

- The Mermaid block is included and valid
- The Mermaid block has both an opening ` ```mermaid` line and a closing standalone ` ``` ` line
- All headings and prose after the diagram appear outside the Mermaid code fence
- Do not put HTML tags, CSS, explanatory prose, or Markdown headings inside the Mermaid block
- Keep labels and node text compatible with GitHub Mermaid and the VS Code Mermaid preview extension
- The primary workflow is obvious
- AI reasoning is separated from execution
- Automation is visible
- Governance is visible
- Business outcomes are explicit
- The diagram fits a presentation slide
- The document explains that VS Code requires Mermaid preview support when the built-in preview does not render Mermaid
- The result is polished and not cluttered

If it is too dense, simplify it.

## Safety and scope

- Ground the architectures in the current repository’s actual purpose, capabilities, and governance model.
- Do not invent unsupported systems, services, or workflows.
- Keep the diagram at a logical architecture level, not infrastructure detail.
- Do not expose secrets or credentials.

## Final output format

The response must contain exactly:

### Architecture Summary
- maximum 5 bullets

### Mermaid Diagram
- one fenced Mermaid code block beginning with `flowchart LR`

### Executive Story
- maximum 3 short talking points
