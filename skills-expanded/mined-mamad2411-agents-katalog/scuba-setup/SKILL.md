---
name: scuba-setup
description: Connect Scuba MCP and configure a repository's shared engineering-memory collection. Use when setting up Scuba skills, selecting or changing the team's destination collection, or troubleshooting missing Scuba access.
license: MIT
---

# Set up Scuba engineering memory

Configure the user's chosen repository and Scuba collection. Do not assume the
repository containing this installed skill is the repository being configured.
Keep credentials in the MCP client's authentication store, outside repository files.

## Connect

1. Identify the target repository and current agent. Reuse any working Scuba MCP
   connection; discover available tools before changing client configuration. Tool
   namespaces and connection labels differ by host, and legacy Flashback-named
   connections may expose Scuba. Match capabilities rather than a literal prefix.
2. If tools are missing or unauthenticated, follow
   [MCP setup](references/mcp-setup.md) for that client. Prefer repairing or enabling
   an installed Scuba plugin before adding a standalone server. For a new Codex or
   Claude Code installation, prefer the plugin; keep manual setup available for
   standalone skills or an existing team-managed connection. Merge configuration
   without replacing other servers. Explain what teammates install and what each
   person authenticates. Let the user complete OAuth in their browser; do not request
   or store their token in this repository.
3. Use `get_me` to establish the active account when available. Discover `search`,
   `get_collection_by_id`, `get_captures_by_id`, and `read_capture`. For saving memory,
   also check `create_text_capture` and `add_captures_to_collection`. Use the current
   tool schemas for arguments. Report missing write access separately from reads.

## Select the destination

1. Read `<target-repository>/.scuba/config.json` if it exists. Preserve unrelated
   settings; do not replace an existing destination without the user's intent to
   change it. Version 1 requires `engineering_memory.collection_id` to be a UUID.
   An unsupported version, invalid file, or inaccessible destination needs repair,
   not a fallback to a similarly named collection.
2. If no destination is configured, accept a collection URL/ID or search for the
   collection the user names. If multiple results are plausible, have the user
   choose. Resolve and verify the ID with `get_collection_by_id` before persisting it.
3. If the user wants a new collection, agree on its name and use `create_collection`.
   Retain its `action_id` and link. Collection creation is private and does not invite
   anyone. Guide the user through Scuba's sharing controls for the intended team;
   do not claim that naming a collection "Eng Wiki" makes it shared. Do not create
   another collection if creation succeeded but sharing remains incomplete.
4. Check the selected collection through the current connection. A successful read
   proves this account can read it, not that everyone can, or that it can write.
   A collection's private/public type alone does not establish its collaborator list.
   Have a teammate verify access after sharing, and report sharing as unverified
   when the available tools cannot establish it.

## Save repository configuration

Write `.scuba/config.json` at the target repository root using
[the example](assets/scuba-config.example.json), replacing the placeholder with the
verified ID. See [the schema](assets/scuba-config.schema.json). Infer the repository
identity from the user's working repository when writing memory; it is not another
required config value. Do not add environment-variable or global-config overrides.

The file selects a destination; it does not authorize publication. For a public
repository, add this exact file to `.gitignore` and keep the real value untracked.
For a private team repository, the team can commit the configuration. When visibility
is unknown, leave the real config untracked until the user chooses otherwise.
Never place actual team settings in the public skill distribution or modify an
installed skill to hold team-specific values.

Offer the [agent guidance snippet](assets/agent-guidance.md) for the existing
`AGENTS.md` or `CLAUDE.md`. Add it when requested as part of setup, preserve other
guidance, and follow existing symlinks instead of creating conflicting copies.

## Verify and report

- Re-read the saved JSON and retrieve the configured collection by ID.
- Check that a small `search` call works. An empty result is valid; an auth error is
  not an empty result. Search is library-wide and relevance-ranked; the configured
  destination does not restrict search or change account permissions.
- Default verification is read-only. If the user asks for a write smoke test, create
  one clearly labeled temporary note, retain action IDs, and add it to the chosen
  collection only with the required sharing approval. Read it back, then undo the
  membership action and capture creation in reverse order. Respect any destructive
  confirmation and report cleanup that could not complete; do not abandon artifacts
  or retry mutations blindly after ambiguous failures.
- Report the config path, collection link, account if known, and which of read,
  write, sharing, and cleanup were actually verified. No live collection mutation is
  needed merely to validate the skill package.
