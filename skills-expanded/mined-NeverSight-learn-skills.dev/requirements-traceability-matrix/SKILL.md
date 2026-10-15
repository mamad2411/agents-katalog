---
name: requirements-traceability-matrix
description: Build a requirements-to-implementation trace matrix that proves coverage and exposes gaps. Use when the user asks to trace requirements, map specs to code, prove coverage, identify missing validation, or build a matrix for review, planning, or compliance work.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
  purpose: Trace requirements to artifacts, tests, and validation evidence
---

# Requirements Traceability Matrix

Use this skill when the user needs a durable mapping from requirement to implementation evidence.

This skill exists to prevent dropped requirements, vague coverage claims, and spec drift during planning, implementation, and review.

## When to use

Use this skill for prompts like:

- "Build a traceability matrix"
- "Show me which requirements are covered"
- "Map the spec to code and tests"
- "Prove the implementation covers the requirements"
- "Find gaps between the requirements and the artifacts"

Use it whenever coverage must be auditable rather than implied.

## Required workflow

1. Extract each requirement as a discrete traceable statement.
2. Assign stable identifiers so distinct requirements do not get merged accidentally.
3. Map each requirement to implementation artifacts, tests, docs, and validation evidence.
4. Mark each requirement as covered, partial, missing, superseded, or out of scope.
5. Surface gaps, contradictions, and unverified assumptions explicitly.
6. Preserve superseded requirements instead of erasing them.
7. Update the matrix when requirements change so history stays visible.

## Non-negotiable rules

- Do not invent coverage.
- Do not merge multiple requirements into one row when the distinction matters.
- Do not drop superseded requirements from the trace.
- Do not mark a requirement covered unless the evidence is concrete.
- Do not rely on a vague summary when the user asked for a matrix.
- Do not hide missing validation behind implementation-only evidence.

## Matrix expectations

Each row should, at minimum, capture:

- requirement ID
- source location or provenance
- coverage status
- implementation evidence
- validation evidence
- remaining gap or note

If a requirement is only partially satisfied, say what is missing and whether it is blocking.

## Definition of done

This skill is complete only when all of the following are true:

- every requirement in scope appears in the matrix
- every status is backed by evidence or a clear gap note
- contradictions and partial coverage are called out
- the result is usable by a reviewer without reconstruction

## Final output contract

Report all of the following:

- the requirement list you traced
- the matrix itself or a compact equivalent
- uncovered or partially covered items
- superseded requirements that were preserved
- any assumptions that were intentionally resolved

If the user asked for a proof of coverage, make the gaps impossible to miss.
