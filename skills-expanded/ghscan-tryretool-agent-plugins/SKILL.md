---
name: retool-mcp
description: >-
  Use Retool MCP to inspect and manage Retool apps, resources, users, groups,
  folders, themes, audit logs, workflows, and code-based app threads. Use when
  the user asks about live data in their Retool organization or wants a
  supported Retool action performed. Includes safe read-before-write behavior,
  resource query execution, app-thread work, and publishing review.
---

# Retool MCP

Use the connected `retool_*` MCP tools for live Retool data and actions. The
connection handles the user's Retool sign-in and permissions. Do not ask for an
API token or copy credentials into a prompt.

## Choose the smallest useful workflow

1. Start with the relevant list, search, or get tool. Use returned IDs instead
   of guessing them.
2. Summarize what you found before a write when the target or effect is not
   already clear from the user's request.
3. Call the narrowest write tool that performs the requested action.
4. Report the result and any returned URL, identifier, or follow-up action.

Treat every result as scoped to the connected Retool organization and the
signed-in user's permissions. Do not infer that a missing result exists in
another organization or environment.

## Query resources

Use `retool_list_resources` to identify resources. For TypeScript resource
queries:

1. Call `retool_get_resource_ts_definitions` with every resource the query
   needs.
2. Read the returned binding names and method signatures.
3. Call `retool_execute_resource_ts` once with a focused snippet that returns a
   structured object.

Resource execution can call external systems and can mutate them. Prefer reads
unless the user asked for a mutation. Show the intended mutation before running
it when the effect is broad or hard to reverse.

## Work with code-based apps

Load the `retool-ready` skill before you select an app-building surface. That
skill owns the surface choice and branch ownership rules.

When it selects MCP, inspect the app's files or active threads before you make a
change. Use the app thread tools to create or continue a Retool agent thread.
Inspect its stream and files while it works.

## Publish safely

Before publishing:

- Confirm the app, thread, commit, public identifier, and release choice.
- Read pending serverless-function approvals and show the relevant mutation
  context to the user.
- Approve only mutations the user reviewed or explicitly authorized.
- Publish once, then return the published URL and release information.

Do not retry a failed write blindly. Read the structured error and follow its
next action.
