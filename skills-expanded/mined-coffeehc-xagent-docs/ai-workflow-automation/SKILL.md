---
name: ai-workflow-automation
description: Use when designing, reviewing, or improving an AI-assisted business workflow, automation opportunity, agent workflow, human-in-the-loop process, operational copilot, or task automation plan. Prefer this Skill when the user needs workflow decomposition, automation boundaries, tool needs, review points, risks, ROI logic, or a phased rollout. Do not use for direct code implementation, prompt-only tuning, or unverified claims that a system integration already exists.
meta:
  version: 2
  display_name: AI 工作流自动化
---

# AI Workflow Automation

## Purpose

Turn a business process into a practical AI-assisted workflow with clear inputs, steps, tools, human checks, artifacts, metrics, and rollout limits.

## Use When

Use for:

- AI automation opportunity assessment.
- Agent workflow design for operations, sales, support, finance, HR, or internal teams.
- Human-in-the-loop process mapping.
- Manual workflow reduction and task routing.
- Automation ROI, risk, or rollout planning.
- Copilot or agent service concept design.

## Material Gate

Identify:

- current workflow, owner, trigger, input material, output, frequency, cycle time, and pain points
- decisions that require human review
- systems or files involved
- failure cost, compliance risk, and customer impact
- measurable success metric

If the workflow owner, input material, or success metric is unknown, mark assumptions before proposing automation.
If the workflow opportunity depends on industry attractiveness, customer demand, competitor examples, existing AI automation projects, or monetization potential, use `skills_find` / `skills_load` for market, business-model, or research synthesis Skills when available before treating those claims as source-backed.
If the expected output is a shareable workflow report, opportunity report, evaluation, or roadmap, use `skills_find` / `skills_load` for `html-report-builder` or an equivalent visual report Skill when available.

## Workflow

1. Map the current process from trigger to final outcome.
2. Separate reading, reasoning, drafting, checking, routing, writing, sending, and approval steps.
3. Classify each step as automate, assist, human-only, or not worth automating.
4. Define required Skills, tools, files, integrations, and human confirmations.
5. Identify failure modes, privacy risk, approval risk, and rollback path.
6. Propose a minimum viable workflow before suggesting broad platform buildout.
7. Define metrics: time saved, throughput, quality, error rate, SLA, cost, or revenue impact.
8. For opportunity or industry selection tasks, compose with evidence and business Skills before ranking workflows.
9. Use `html-report-builder` for a visual workflow report when the user needs a shareable artifact, with this Skill providing workflow maps, controls, metrics, and rollout content.

## Checks

- The workflow has a named trigger, owner, inputs, outputs, and stop condition.
- Human review points are explicit.
- Tool or system access is labeled required, available, or unverified.
- The MVP does not require every integration to exist on day one.
- Risks include detection, mitigation, and fallback.
- ROI claims are tied to volume, time, cost, or revenue assumptions.
- Industry, competitor, existing-project, and monetization claims are source-backed or explicitly labeled as assumptions.
- Final report deliverables show workflow diagram, risk/control matrix, assumptions, and unverified integrations.

## Outputs

- automation opportunity brief
- workflow map
- step classification
- MVP automation plan
- risk and control matrix
- rollout roadmap
- measurement plan

## Boundary

This Skill owns workflow framing, automation boundaries, human review design, rollout logic, and measurement structure. It does not own tool schemas, integration implementation, credentials, runtime permissions, external system writes, compliance approval, or final deployment decisions.

It must not run shell, Python, Node, npm, curl, MCP, browser automation, workflow engine, RPA, CRM, ERP, ticketing, email, Slack, Teams, database, package install, deploy, publish, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
