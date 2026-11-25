---
name: evaluation-domains
description: "Domain profile contract for evaluating any source, repo, or point of interest — credibility axes, verification procedure, verdict vocabulary, and memory home, per domain. Triggers: \"evaluate a source\", \"vet a source/domain\", \"credibility\", \"domain profile\"."
allowed-tools: Read, Glob, Grep
---


# Evaluation Domains

Router + reference set for a portable evaluate-decide-remember loop. It provides a shared,
data-shaped contract instead of requiring each caller to hardcode its own axes.

## Domain Profile Contract

Every `references/profiles/<domain>.md` answers six fixed sections: **primary-source
definition** (what outranks what), **credibility axes + weights** (from the shared vocabulary
below), **staleness horizon** (defaults to the >30-day re-verify rule), **verification
procedure** (one of the three below), **verdict vocabulary**, and **memory home**
(progressive-disclosure: index line + linked record). A profile missing any section fails the
self-check. Adding a domain requires only a new conforming profile file — no spec or command
change.

## Routing

| Domain | Profile | Procedure | Caller |
|---|---|---|---|
| Claude Code official channels (changelog, GitHub releases, npm) | `references/profiles/claude-code-official.md` | signal-bundle liveness | release-currency review |
| External GitHub repos / docs sites | `references/profiles/external-repos.md` | duplicate-gate + evidence-audit | `/recon` |
| AI/tech news, blogs, UGC | `references/profiles/ai-tech-news.md` | SIFT / lateral reading | `add-source-trust-vetting` (planned) |

Shared axes vocabulary, the three procedures, and the recording rule live in
`references/axes-and-procedures.md` — read that before authoring a new profile. Do not restate
axes content here or in a consuming command body; cite the profile instead.

## Adding a fourth domain

Author `references/profiles/<new-domain>.md` answering all six contract sections. No edit to
this file, the spec, or any consuming command is required.
