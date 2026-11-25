---
name: create-prd
description:
  Turn the current conversation context into a PRD and publish it to the project
  issue tracker. Use when user wants to create a PRD from the current context.
---

This skill takes the current conversation context and codebase understanding and
produces a PRD. Do NOT interview the user — just synthesize what you already
know.

## Process

1. Explore the repo to understand the current state of the codebase, if you
   haven't already. Use the project's domain glossary vocabulary throughout the
   PRD, and respect any ADRs in the area you're touching.

2. Sketch out the major components you will need to build or modify to complete
   the implementation. Actively look for opportunities to extract deep components
   that can be tested in isolation.

A deep module (as opposed to a shallow components) is one which encapsulates a
lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. 

3. Write the PRD using the template below, then publish it to
   `docs/product/001-<descriptive-title>.md`. Use numbering and kebab casing for
   the filename of the new PRD you're creating. 

We use PRDs to describe functional requirements, a solution strategy, and
associated features and user stories as you would in an agile project. 

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format
of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I
   can make better informed decisions about my spending </user-story-example>

This list of user stories should be extremely extensive and cover all aspects of
the feature.

## Risks

A list of the risks that are worth considering. These can be technical,
organizational, or integration related.

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes that are important for this PRD.

</prd-template>
