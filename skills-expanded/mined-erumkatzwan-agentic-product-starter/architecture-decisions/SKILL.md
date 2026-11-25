---
name: architecture-decisions
description: Use before building anything that changes how parts of the system fit together, and whenever a decision is hard to reverse. Reads the architecture overview and ADRs first, checks a plan or pull request against them, writes MADR 4 ADRs, keeps the C4 diagrams and overview in sync, and optionally draws interactive diagrams with Archify.
---

# Architecture decisions

This repo documents architecture three ways. Keep them consistent with each other and with the code:

| What | Where | Format |
|---|---|---|
| The big picture | `docs/architecture/README.md` | arc42 sections with C4 diagrams in Mermaid |
| Why it is that way | `docs/adr/NNNN-*.md`, indexed in `docs/adr/README.md` | MADR 4 (`docs/adr/template.md`) |
| Domain language | `GLOSSARY.md` | `domain-modeling` skill |

## 1. Before you plan or build: read

1. `docs/architecture/README.md`: at least the sections for the parts you will touch.
2. `docs/adr/README.md`, then every **accepted** ADR in that area.
3. `GLOSSARY.md` if it exists.

Then state, in the plan, spec or ticket: "Fits ADR-NNNN" for each relevant decision, or "Conflicts with ADR-NNNN because…". Never silently work around an accepted ADR.

## 2. Decide whether a new ADR is needed

Write one only when all three are true (rule from `domain-modeling`):

1. **Hard to reverse**
2. **Surprising without context**
3. **The result of a real trade-off**

Always write one for: a database, message bus, auth or identity provider, hosting or deployment target, a new app or service, a new integration pattern between apps and backend, a new cross-cutting library (DI, networking, state), or a deliberate deviation from an existing ADR.

Do not write one for: bug fixes, routine upgrades, a new screen that follows the platform checklist, configuration changes.

## 3. Write the ADR

1. Copy `docs/adr/template.md` to `docs/adr/NNNN-short-title.md` (next free number, lowercase, hyphens).
2. Front matter: `status: proposed`, today's date, `decision-makers`.
3. **Context and Problem Statement:** 2-4 sentences; link the spec issue.
4. **Decision Drivers:** prefer the quality goals in section 1 of the overview (consistency, changeability, testability, security).
5. **Considered Options:** at least two real options. "Do nothing" counts if it was a real option.
6. **Decision Outcome:** "Chosen option: …, because …". List good and bad consequences honestly.
7. **Confirmation:** name the CI check, test or lint rule that enforces it. If none exists yet, add a ticket for one.
8. Keep it short: one screen is typical. Use plain English.

When the pull request merges: set `status: accepted`, add the row to `docs/adr/README.md`.

To change a decision: write a new ADR, and set the old one's status to `superseded by ADR-NNNN`. Never rewrite the decision of an accepted ADR; fixing typos and links is fine.

## 4. Keep the overview and diagrams in sync

In the same pull request as the architecture change:

* Update the affected arc42 section of `docs/architecture/README.md`: building blocks, runtime, environments, cross-cutting concepts, risks.
* Update the C4 diagram that changed: context (level 1) for a new user type or outside system, containers (level 2) for a new app, service or data store, the layer diagram for a new layer.
* Link the new ADR from section 4 (Solution strategy) if it is a strategy-level decision.
* Mermaid only, using the classes already defined in the diagrams (palette from `design/tokens.json`). Check it renders (`npx -y @mermaid-js/mermaid-cli -i file.mmd -o out.svg` or the GitHub preview).

## 5. Review checklist (used by `code-review`)

- [ ] The change respects every accepted ADR in its area, or includes a new ADR that supersedes it.
- [ ] A decision that meets the three criteria has an ADR with status, date, options and Confirmation.
- [ ] `docs/architecture/README.md` and its diagrams still match the code.
- [ ] `docs/adr/README.md` lists the new ADR.
- [ ] Names match `GLOSSARY.md` and the platform skills (the same names on iOS, Android and web).

## 6. Interactive diagrams (optional): Archify

For a shareable, interactive view (zoom, click-through, sequence animation, export to PNG or SVG), use [Archify](https://github.com/tt-a1i/archify) by tt-a1i (Apache 2.0). It is not stored in this repo (about 18 MB); install it when needed, project only:

```bash
npx -y skills@latest add https://archify.si --skill archify --agent claude-code --copy --yes
```

Use `--agent codex`, `cursor` or `opencode` for other agents. Then ask, for example: "Use Archify to draw the containers in docs/architecture/README.md from this repository." It writes standalone HTML into `.archify/`, which is git-ignored. Mermaid in `docs/architecture/` stays the source of truth; Archify output is for presenting and exploring, so do not commit it unless asked.

## How it connects to the other skills

| Stage | Skill | What this skill adds |
|---|---|---|
| Shape, Refine | `grill-with-docs`, `domain-modeling` | When a hard-to-reverse decision lands, write it here in MADR format |
| Specify | `to-spec` | The spec lists the ADRs it relies on and any new ADR it needs |
| Plan | `to-tickets` | A ticket for each new ADR, ordered before the code tickets that depend on it |
| Build | `implement`, `tdd`, platform skills | Read section 1 before coding |
| Review | `code-review`, `pr` | Section 5 checklist |
| Improve | `improve-codebase-architecture` | Proposals that contradict an ADR become a new ADR, not a silent refactor |
