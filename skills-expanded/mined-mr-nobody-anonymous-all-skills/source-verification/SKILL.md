---
name: source-verification
description: Evaluate a source's credibility, bias, recency, and relevance before relying on it.
category: research
aliases:
- evaluate-source
- source-credibility
- source-quality
triggers:
- is this source reliable
- evaluate this source
- check this citation
- source quality
keywords:
- source
- credibility
- bias
- reliable
- citation
- evaluate
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- bias
- credibility
- reliable
- research
- source
- verification
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

# Source Verification

## Purpose

Evaluate a source before relying on it. Check who published it, when, why, what evidence it
cites, and how it fits into the broader conversation.

## When to Use

- User asks about a specific source / URL / paper
- User wants to know if something is reliable
- Triaging sources during research

## When NOT to Use

- The user wants to check a factual claim (route to `fact-checking`)

## Capabilities

- Identify publisher, author, funding
- Check publication date and recency
- Note bias / perspective
- Compare to other sources on the same topic

## Inputs

- The source (URL, title, author, or document)
- The claim being supported

## Workflow

1. **Identify the source.** Who published it? Who is the author? What is their expertise?
2. **Date and venue.** When published? Where (peer-reviewed, blog, news, etc.)?
3. **Funding / conflicts.** Any disclosed conflicts?
4. **Evidence cited.** Does it cite primary sources? Reproducible data?
5. **Cross-check.** What do other sources say?

## Output

A short profile of the source: reliability tier, perspective, recency, and any caveats.

## Source

Custom skill, written for this library.

## Notes

Pairs with `fact-checking` and `web-research`.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "is this source reliable"; "evaluate this source"; "check this citation".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
