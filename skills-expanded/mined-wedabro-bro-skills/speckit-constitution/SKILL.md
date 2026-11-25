---
name: speckit.constitution
description: Governance Manager - Set up & manage Constitution (Source of Law).
---

## Mission
Establish, audit, and maintain the repository constitution (`constitution.md`) as the supreme operational and architectural law for all agents and contributors.

## Inputs and Outputs
- Read developer inputs, tech stack constraints, environment variables, infrastructure rules, and codebase conventions.
- Produce and maintain `.agents/memory/constitution.md` with explicit, verifiable, non-negotiable architectural, security, code standard, and runtime rules.

## Protocol
1. Collect and codify core technical choices: languages, frameworks, persistence, and environment-driven port allocation.
2. Establish non-negotiable security requirements: non-root containers, forbidden volume shadowing in production, zero hardcoded credentials, and minimal surface exposure.
3. Enforce code quality, testing standards, language policies, and ENV-first configuration rules across all components.
4. Codify monorepo boundaries and build isolation rules when multi-package repositories are detected.
5. Formulate build-time and deployment safety checks including pre-deploy verification commands, healthy container states, and static generation guards.
6. Audit every rule for verifiability: each clause must be objective, enforceable, and measurable via automated checks or manual inspections.

## Completion Gate
`constitution.md` contains unambiguous, testable rules across all required sections with zero placeholder text and no implementation leaks.

## Guard Rails
The constitution defines WHAT is permissible or forbidden, never HOW to implement features. Do not introduce vague principles that cannot be validated.
