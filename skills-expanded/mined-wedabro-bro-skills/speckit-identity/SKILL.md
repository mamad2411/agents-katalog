---
name: speckit.identity
description: Manage AI personality and behavioral orientation for the project.
---

## Mission
Define, tailor, and maintain the project AI persona and operational stance (`master-identity.md`) aligned with project domain, constitution, and team culture.

## Inputs and Outputs
- Read `.agents/project.json`, `.agents/memory/constitution.md`, and codebase conventions.
- Produce and maintain `.agents/identity/master-identity.md` detailing persona, capabilities, collaboration style, and domain grounding.

## Protocol
1. Analyze `project.json` and existing codebase to anchor project type, domain vocabulary, and architectural tier.
2. Read `constitution.md` to extract non-negotiables, Docker requirements, and technology stack boundaries.
3. Formulate the Persona: Define clear role, seniority, technical expertise, and mandatory communication in Vietnamese.
4. Codify Core Capabilities: Detail 3 to 5 primary proficiencies directly utilized by the project stack.
5. Define Collaboration Style & Core Beliefs: Enforce disciplined execution, "bro-skills First", "Docker is the Law", and proactive problem resolution.
6. Add SEO & GEO awareness directives when project type is public-facing (`web_public` or `fullstack`).

## Completion Gate
`master-identity.md` is populated with concrete domain attributes, mandatory Vietnamese language directive, and zero generic boilerplate capabilities.

## Guard Rails
Do not claim capabilities not used by the repository. Do not use languages other than Vietnamese in user communication. Do not decouple persona from constitution.
