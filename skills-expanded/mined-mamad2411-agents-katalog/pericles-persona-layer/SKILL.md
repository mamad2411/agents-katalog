---
name: pericles-persona-layer
version: 2026.05.0
description: >
  How to build the Persona Layer that frames Skill outputs per user persona — WITHOUT
  forking agents per persona (§6). Use this WHENEVER output should differ for the Global
  Risk Manager vs Supply Chain Manager vs Business Stakeholder, or when you're tempted to
  branch a prompt/agent by role. Encodes the four persona dimensions (output shape, data
  scope, default module, vocabulary), the three real personas, and the rule that one
  substantive answer is rendered per persona.
doctrine_refs: [§6; Security §2]
depends_on: [pericles-doctrine, pericles-functional-agent, pericles-prompts]
last_reconciled: 2026-05-28
---

# Pericles Persona Layer (build skill)

The same underlying truth must serve very different readers. A CFO-facing stakeholder
wants financial impact and a one-paragraph summary; a Supply Chain Manager wants the
affected lanes and the response Plan. The doctrine's answer (§6) is a **thin Persona
Layer that frames outputs**, not per-persona agents. Build one Skill that produces the
substantive answer; let the Persona Layer shape how each persona receives it.

## When to use this skill

Any time output should differ by role; building the rendering layer over Skill outputs;
or whenever you're about to branch an agent/prompt by persona — stop and use this instead.

## The three personas (from the personas rule)

`Global Risk Manager`, `Supply Chain Manager`, `Business Stakeholder`. Each interacts
with Atlas, Insights, Plans, and Co-Pilot differently. The Persona Layer carries this,
not the agents.

## The four persona dimensions

A persona configuration declares:

1. **Output shape** — depth and format (e.g. executive one-paragraph vs operational
   detail with lanes/Plans).
2. **Data scope** — what this persona may see. Financial-impact figures are restricted
   to **Risk Manager and above**; the Persona Layer (with tenant RBAC,
   `pericles-tenant-isolation`) enforces this. A prompt must never embed restricted data
   it wasn't authorized to receive (`pericles-prompts`).
3. **Default module** — where this persona lands (e.g. Risk Manager → Atlas/Assessments;
   Stakeholder → Insights summary).
4. **Vocabulary** — sector/role-appropriate phrasing.

## The rule: render, don't fork (§6)

- One Functional/Industry Skill produces the substantive, persona-neutral result.
- The Persona Layer renders it for each persona (shape + vocabulary) and applies data
  scope.
- There are **no per-persona agents or per-persona prompt branches**. Adding a persona
  is a configuration change, not a new agent.

This keeps consistency (every persona sees the same underlying truth), auditability (one
lineage, not N), and cost (one invocation, not N) intact.

## What this forbids

Per-persona agents or Skills; branching a prompt by role to produce different substance;
embedding financial-impact (or other restricted) data in output for a persona not
authorized to see it; encoding persona logic inside a Functional Agent instead of the
Persona Layer.

## Verification

Output for different personas derives from the same Skill invocation (one lineage);
data-scope restrictions (e.g. financial impact to Risk Manager+) are enforced and tested;
adding a persona requires no new agent; vocabulary/shape differences are configuration.

## Existing standards (read alongside)

Doctrine §6 (Notion); `.cursor/rules/001-application/008-pericles-user-personas-core-standards-auto.mdc`;
`pericles-copilot-ui` and the module UIs (where persona framing surfaces).

## Open questions

- Exact mapping of the three personas to the Admin Portal's RBAC roles
  (OWNER/ADMIN/MEMBER/GUEST) and the data-scope matrix — reconcile with
  `pericles-admin-portal-ui` and `pericles-tenant-isolation`.
- Whether persona config lives in the registry, OrganizationSettings, or a dedicated
  store — decide with the platform team.

## Changelog

- 2026.05.0 — Initial draft from Doctrine §6 and the personas rule; three personas, four
  dimensions, render-don't-fork.
