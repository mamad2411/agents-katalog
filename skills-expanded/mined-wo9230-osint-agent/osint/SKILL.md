---
name: osint
description: Run the osint-agent B2B commercial OSINT workflow for company research, competitor intelligence, supplier checks, Amazon seller investigation, industry scans, buyer personas, psychographic research, and general business intelligence. Use when the user invokes /osint or asks for background checks, commercial investigation, market intelligence, customer/supplier validation, or a complete OSINT report.
---

# OSINT Agent

OSINT_AGENT_HOME="__OSINT_AGENT_HOME__"

## Required Startup

1. Resolve `OSINT_AGENT_HOME`.
   - If it still equals `__OSINT_AGENT_HOME__`, the skill has not been installed from a local clone. Ask the user to run `bash codex-skill/install.sh` from the repository root.
   - Otherwise treat `OSINT_AGENT_HOME` as the repository root.
2. Read `${OSINT_AGENT_HOME}/CLAUDE.md` completely before doing OSINT work.
3. Read `${OSINT_AGENT_HOME}/.claude/commands/osint.md` completely before interpreting `/osint` arguments.
4. Load the matching investigation skill from `${OSINT_AGENT_HOME}/skills/`.
5. Use `${OSINT_AGENT_HOME}/docs/`, `${OSINT_AGENT_HOME}/templates/`, and `${OSINT_AGENT_HOME}/reports/osint/` when the workflow calls for them.

## Command Shape

```text
/osint [target] [type]
```

Types:

```text
company | person | supplier | competitor | amazon-seller | seller-scout | quick-id | b2b-gtm | industry | persona | psychograph | research
```

If the type is missing, infer it using `.claude/commands/osint.md`; default to `company` when uncertain.

## Workflow Contract

Follow the full OSINT Agent process from `.claude/commands/osint.md`:

1. PIR definition.
2. Parallel public-data collection.
3. Source grading with Admiralty Code.
4. ACH analysis.
5. Cross-dimensional weakness analysis.
6. Report generation.
7. Optional sales playbook.
8. Optional strategic analysis.

Preserve citations and mark confidence for important claims. When web or MCP tools are unavailable, state the gap and continue with available public sources rather than fabricating data.

## Safety Rules

- Use public and compliant sources only.
- Refuse prohibited targets and methods described in `CLAUDE.md`.
- Do not collect private addresses, private phone numbers, minors' information, credentialed/private-system data, dark-web data, or sensitive personal attributes.
- Do not help evade sanctions, platform restrictions, authentication, or access controls.
- Do not paste, print, store, or commit API keys, tokens, cookies, or secrets.

## Environment Variables

Only check for variable names. Never display complete existing values.

Core variables:

```text
DEEPSEEK_API_KEY
FIRECRAWL_API_KEY
SEC_EDGAR_USER_AGENT
```

Recommended variables:

```text
HUNTER_API_KEY
APOLLO_API_KEY
SELLERSPRITE_SECRET_KEY
PERPLEXITY_API_KEY
PROXYCURL_API_KEY
```

Advanced optional variables:

```text
OPENCORPORATES_API_KEY
OPENSANCTIONS_API_KEY
TOMBA_API_KEY
TOMBA_SECRET
LENS_API_KEY
HOSTIO_API_KEY
DOMAINSDB_API_KEY
APIFY_TOKEN
OPENROUTER_API_KEY
TWITTER_AUTH_TOKEN
TWITTER_CT0
```

## Output

Use the output rules in `CLAUDE.md`. Keep report filenames in English with hyphens. Include a clear risk rating, source list, confidence markings, and practical next actions.
