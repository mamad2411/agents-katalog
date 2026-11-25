---
name: academic-research
description: Find and use scholarly articles, preprints, and academic sources for research.
category: research
aliases:
- scholarly-research
- literature-review
- papers
triggers:
- find papers on
- academic sources
- scholarly research
- literature review
- find me research on
keywords:
- academic
- scholarly
- paper
- preprint
- journal
- literature
- study
- research
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- academic
- paper
- preprint
- research
- scholarly
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Academic Research

## Purpose

Locate and use scholarly sources for a research question. Distinguish peer-reviewed work
from preprints, popularizations, and predatory journals.

## When to Use

- User wants scholarly evidence
- User is writing a literature review
- The question benefits from primary research

## When NOT to Use

- The user wants a quick answer (route to `web-research`)

## Capabilities

- Query academic databases (arXiv, PubMed, Google Scholar, etc.)
- Identify peer-reviewed vs. preprint vs. predatory
- Extract methods, findings, and limitations
- Compose literature-review prose

## Safety

- Don't conflate preprints with peer-reviewed work
- Flag predatory / low-quality journals
- Note study limitations

## Source

Custom skill, written for this library.

## Notes

Specialized version of `web-research` focused on academic sources. Pairs with `source-verification`.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "find papers on"; "academic sources"; "scholarly research".
