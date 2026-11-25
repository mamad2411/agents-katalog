---
name: policy-writer
description: Draft security and compliance policy documents aligned to common frameworks so Claude can turn user requirements into professional, review-ready policy text.
---

# Policy Writer

Use this skill when the user needs a security policy draft, wants to align policy text to a framework, or needs help tailoring standard policy language for an organization.

## Goal

Help Claude produce clear, professional policy content that matches the requested topic, framework expectations, and organizational context.

## Workflow

1. Confirm the policy topic, framework, and organization details the user wants reflected in the document.
2. Identify any required review cycle, ownership details, or implementation constraints.
3. Draft policy language that is structured, specific, and realistic for audit review.
4. Separate mandatory policy statements from optional implementation notes when useful.
5. Return a polished policy draft that the user can review with legal, security, or compliance stakeholders.

## Inputs

Expected inputs from the bundled tool metadata:
- framework: Target framework such as SOC2, ISO27001, NIST, CIS, PCI-DSS, or GDPR.
- topic: Policy topic to generate.
- org_name: Organization name to include in the document.
- review_cycle: Policy review cadence.

## Bundled Files

- main.py contains the document generation logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example topics or prompts.

## Guidance

Write in a professional tone suitable for audit and governance review. Prefer concrete, enforceable statements over vague language, and keep the draft internally consistent.
