---
name: composio-tools
description: This skill should be used when a task needs an app or service that has no native Cowork MCP connector — for example Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, or Calendly — and the Composio connector is installed. It explains Composio's session-based Tool Router model, the meta-tool discover/authenticate/execute loop, and when to reach for Composio versus a native MCP. Trigger when the user asks to act on a third-party app that Cowork has no dedicated connector for, or mentions Composio directly.
---

# Composio tools

Composio's Tool Router gives Claude access to 1000+ app toolkits through a single MCP connector. This skill covers how to use it well — and, just as important, when not to.

## When to use Composio

Native MCP connectors come first. If Cowork already has a dedicated connector for the app — GitHub, Gmail, Google Calendar, Slack, Google Drive, Supabase — use that. Native connectors are faster, give finer control over what enters context, and are independently maintained.

Reach for Composio when the task needs an app with no native connector: Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, Calendly, and roughly a thousand others. Composio is the breadth layer, not a replacement for the native connectors.

This is the lesson of the Rube retirement (see the plugin README): a single gateway in front of everything was removed on purpose. Composio re-enters as an additive reach layer, never a gateway the other plugins route through.

## Prerequisite

The Composio MCP connector must be installed in Cowork. If it is not, run `/composio-setup` first — that command walks through retiring the old Rube connector and adding Composio.

## How Composio works

Composio is session-based. A session is scoped to one user and exposes a remote MCP endpoint. Once the connector is installed, Claude sees Composio's meta-tools rather than thousands of individual tool schemas:

1. Discover — `COMPOSIO_SEARCH_TOOLS` finds the right tool from a plain-language description of the task. You do not need to know tool names up front.
2. Authenticate — if the toolkit is not yet connected for this user, `COMPOSIO_MANAGE_CONNECTIONS` produces a Connect Link. The user authorizes the app once, and the connection persists for future sessions.
3. Execute — call the discovered tool. Meta-tool calls share session context, so discovery in one step and execution in the next stay connected.

For large responses or bulk operations, Composio's workbench is a persistent Python sandbox scoped to the session — use it instead of stuffing long tool outputs into context.

## Working pattern

1. Confirm there is no native MCP for the app. If there is, stop and use the native one.
2. Confirm the Composio connector is installed (`/composio-setup` if not).
3. Use `COMPOSIO_SEARCH_TOOLS` to find the tool from a plain-language description.
4. If the app is not connected, surface the Connect Link from `COMPOSIO_MANAGE_CONNECTIONS` and let the user authorize it.
5. Execute. Tell the user what the action will do before running it — Composio tools take real actions on real accounts.

## Notes

- Composio actions run on the user's real connected accounts. Confirm intent before executing any write.
- Any side-effectful action taken through a Composio toolkit is governed by the same risk tiers and Release-Owner gate as native skills; do not let an external toolkit bypass the gate. Downstream third-party toolkits reached via Composio inherit this fleet's gate rules.
- Each teammate connects their own app accounts through Composio, so actions are attributed per person.
- The standalone `composio-agent` project (a runnable Claude Agent SDK program) is a separate artifact, not part of this plugin. This skill is about using Composio from within Cowork.
