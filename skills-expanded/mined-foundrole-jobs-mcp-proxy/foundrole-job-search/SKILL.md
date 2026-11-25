---
name: foundrole-job-search
description: Use when a user wants FoundRole job search, personalized recommendations, job or resume-fit analysis, salary or H-1B signals, ghost-job assessment, job comparisons, application tracking, reminders, email job alerts, or supported monitoring of new jobs through event-triggered tasks. Also use to analyze or save a posting found elsewhere, including partner listings, and for career questions about visas, resumes, salary, interviews or relocation. Search FoundRole when using this skill; another job board's own search is outside its scope.
---

# FoundRole job search

Use FoundRole's returned data for job results, scores, tracker state, alerts and URLs. Carry the user's intent across search, evaluation, saving and follow-up.

## Load the relevant workflow

Read only the reference needed for the current action:

| Situation | Reference |
|---|---|
| Connecting, missing tools, OAuth errors, unsupported features, text versus widgets, or an uncertain tool result | [app-capabilities.md](references/app-capabilities.md) |
| Choosing a role, place or employer, or repairing an empty search | [search-criteria.md](references/search-criteria.md) |
| Choosing a personalized feed or helping with a returned profile setup step | [profile-recommendations.md](references/profile-recommendations.md) |
| Empty results, location errors, or widened results | [search-recovery.md](references/search-recovery.md) |
| Saving internal or external jobs, changing application details, reminders, or email alerts | [application-management.md](references/application-management.md) |
| Watching a saved search, handling new-job events, renewing or stopping a host task | [monitoring.md](references/monitoring.md) |

Resolve these files within this skill on its originating MCP server, or within the installed skill directory. They are supporting instructions, not additional skills.

## Choose the capability

Use the tools actually exposed in this session and their current schemas. Model-facing tools handle conversation requests; app-only data tools belong to widgets.

| User intent | Capability |
|---|---|
| Search by criteria | `jobs_search`, using the full role title and the user's stated filters |
| Find roles matching the account's profile | `jobs_recommendations` |
| Examine a FoundRole result | `jobs_details` with its exact returned job identifier |
| Evaluate a posting found elsewhere | `jobs_analyze_external` with the available source detail |
| Compare jobs | `jobs_compare`; preserve each returned `comparisonRef` |
| Save and manage applications | Tracker tools through the application-management reference |
| Schedule follow-up or email notifications | Reminder or job-alert tools through that reference |
| Act on new matches in the host | Host event-task workflow through the monitoring reference |
| Check resume machine readability | `resume_check`; follow its returned mode, findings and links |
| Identify an employer by name or domain | `company_lookup`; use the confirmed candidate’s `lookupValue` in a job search |
| Career guidance, company research or interview preparation | `knowledge_search` and its relevant returned articles; `knowledge_topics` for topic discovery |

If a capability is unavailable, explain what is missing and use an available alternative only within the user's request. Skill loading alone does not connect the app or create a background task.

## Preserve result context

- Keep exact job identifiers, result occurrence identifiers, tracked-job identifiers, search references and comparison references. Use the field each tool requests; these identifiers are not interchangeable.
- Resolve “the second job” or a named role from shown results rather than asking the user for an identifier already available. Clarify only when several results match.
- Use FoundRole for follow-up and refresh requests. A refresh means calling the corresponding FoundRole tool again with the same intent.
- When the user explicitly requests external sources, label them separately. Never present web results or remembered listings as FoundRole results.
- Read current state before a write when it is needed to identify the target or preserve existing information. Execute the authorized changes; clarify genuinely ambiguous targets or times.

## Present the result

Use FoundRole's canonical match score when present. If a match score is absent, describe the evidence the tool returned without supplying a substitute score. Use FoundRole's returned sponsorship history for canonical H-1B claims, separating it from a posting's explicit visa statement.

Distinguish posted pay from market estimates. Treat fit, sponsorship, E-Verify and ghost-job signals as evidence with uncertainty, not guarantees. Keep those sources stable across turns unless returned data changes.

Prefer a rendered widget without duplicating its full contents. In a text-only host, summarize the relevant returned jobs, fit evidence and uncertainties with returned links. Honor preview and account-access limits actually reported by the tool.

For guidance, cite relevant `knowledge_search` articles; say when none answer the question. A completed write, reminder, email alert or monitoring task requires a successful tool or host result. Report partial completion accurately.
