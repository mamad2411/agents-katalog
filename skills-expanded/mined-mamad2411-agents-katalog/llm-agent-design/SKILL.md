---
name: llm-agent-design
description: Use this skill when the user asks to design, review, implement, or improve LLM agents, tool-using agents, RAG agents, hospital workflow automation agents, document processing agents, EMR agents, administrative automation agents, or multi-step AI workflows. Trigger for requests mentioning LLM Agent, 에이전트, RAG, tool, workflow, 자동화, 병원 업무, 문서처리, 정보추출, human-in-the-loop, validation, logging, security.
---

# LLM Agent Design Skill

## Purpose

Design practical and secure LLM agent workflows.

The goal is to make the agent usable in real research, hospital, administrative, document-processing, or business workflows.

## Default Response Structure

Use this structure unless the user requests another format:

## 결론
State the recommended agent structure first.

## 사용 목적
Define the user goal and workflow problem.

## 입력 데이터
Specify input data, file types, database fields, documents, or user messages.

## Agent Role
Define what the agent is responsible for.

## Tool Scope
List available tools and what each tool can and cannot do.

## Retrieval / Knowledge Source
Define whether the agent uses:
- static prompt context
- database
- vector store
- file search
- API
- rule-based lookup
- human-provided documents

## Workflow
Describe the step-by-step agent flow.

## Output Schema
Define the expected output format.

## Validation Step
Define how the output is checked.

## Human Review Step
Define where human approval is required.

## Logging Policy
Define what can be logged and what must not be logged.

## Failure Handling
Define fallback behavior when the agent is uncertain or tool calls fail.

## Security Policy
Define privacy, permission, and data handling rules.

## 다음 액션
Suggest implementation steps.

## Core Agent Design Checklist

Always define:

- user goal
- agent role
- input schema
- output schema
- tool list
- tool permission boundary
- retrieval source
- memory policy
- validation logic
- human review point
- escalation rule
- audit log
- failure mode
- evaluation metric

## Healthcare / Hospital Agent Rules

For hospital, EMR, patient document, or clinical workflow agents:

- Never expose raw PHI/PII unnecessarily.
- Mask names, patient numbers, phone numbers, addresses, resident registration numbers, and other identifiers.
- Do not store raw patient data in logs.
- Add human-in-the-loop review before final administrative or clinical action.
- Separate “recommendation” from “final decision.”
- Define access control assumptions.
- Define audit log requirements.
- Define what the agent must refuse or escalate.
- Avoid letting the agent make final clinical, legal, financial, or administrative decisions without approval.

## LLM Agent Architecture Options

When useful, compare multiple architectures:

| 구조 | 장점 | 단점 | 추천 상황 |
|---|---|---|---|
| Single Agent | Simple and fast | Limited control | Simple document or Q&A task |
| Router Agent | Routes tasks clearly | More design needed | Multiple task types |
| Tool-Using Agent | Can act on systems | Permission risk | Workflow automation |
| RAG Agent | Uses documents | Retrieval quality matters | Policy, manual, report search |
| Multi-Agent | Specialized roles | More complex | Research pipeline or review workflow |

## Evaluation Metrics

For agent tasks, consider:

- task success rate
- exact match
- factual consistency
- hallucination rate
- human review agreement
- retrieval precision
- retrieval recall
- latency
- cost
- security failure rate
- escalation accuracy

## Output Style

Prefer concrete workflow diagrams in text form:

User Input
→ Pre-check
→ Retrieval
→ Reasoning
→ Tool Call
→ Validation
→ Human Review
→ Final Output
→ Logging

## Final Output Standard

The final answer should include a design that can be directly converted into:

- system prompt
- agent spec
- implementation plan
- README
- workflow diagram
- security checklist
