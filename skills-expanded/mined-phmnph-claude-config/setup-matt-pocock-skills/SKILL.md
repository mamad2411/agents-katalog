---
name: setup-matt-pocock-skills
description: Configure missing tracker and domain-document conventions for the Matt Pocock workflows in a repository.
---

# Fill missing project conventions

Run when workflow conventions are missing or the user requests setup. Existing
AGENTS.md and documentation may already supply everything needed. Ordinary
implementation, research, and local review do not require this setup first.

Inspect relevant existing instructions, the repository remote, documentation
layout, and any docs/agents configuration. For an umbrella directory, distinguish
shared conventions from each independent repository's tracker and code changes.
Do not force one repository's rules onto its neighbors.

Resolve only the missing choices:

- **Tracker:** infer from explicit project instructions, not just the hosting
  provider. Use the user's existing Jira/GitHub/GitLab/local workflow. Ask when
  evidence leaves a materially different choice. A local draft needs no external
  tracker integration. Configure access separately; setup is not permission to
  create issues or change tracker settings.
- **Domain documentation:** link the current glossary, architecture decisions,
  and relevant docs. Retain their existing paths. Create small pointer files
  under docs/agents only when consumers need them; do not duplicate the content.
- **Triage vocabulary:** configure it only if a workflow actually uses it.
  Consumers must work without triage labels when no triage workflow is installed.

For Codex instructions, update the existing AGENTS.md at the appropriate scope,
or create it when setup requires one. Preserve CLAUDE.md and other agent files
unless the user also requests them. If project instructions already define a
shared source, link it rather than making a conflicting copy.

Choose templates only for missing configuration:
[GitHub](issue-tracker-github.md), [GitLab](issue-tracker-gitlab.md),
[local Markdown](issue-tracker-local.md), [domain docs](domain.md), and
[triage labels](triage-labels.md). For other trackers record the actual workflow.
Replace template assumptions with facts from this project.

When the user requested configuration, apply the understood local changes and
verify that referenced paths and commands exist. Ask only about unresolved
material choices. When asked for a proposal, return the concrete draft instead.
Report what changed or that existing conventions were sufficient. Setup is done
when relevant workflows can locate their instructions, not when every template
has been copied.
