---
name: canvas-enterprise-app
description: Plans and routes enterprise Canvas App creation or editing with MCP coauthoring, SharePoint or Dataverse data, approval gates, and team UI conventions.
allowed-tools: Bash, Read, AskUserQuestion
---

# Canvas Enterprise App

Use this for enterprise Canvas App work. This skill prepares the request and then
routes actual authoring to the existing `canvas-apps` plugin.

## Workflow

1. Run `power-platform-session-start` and select the `maker-canvas` profile.
2. Confirm the app exists in Power Apps Studio, is saved, and has coauthoring
   enabled.
3. If Canvas Authoring MCP is not connected, route to `configure-canvas-mcp`.
4. Capture the app intent:
   - personas and roles
   - primary data sources
   - screens and navigation
   - required actions and approvals
   - audit/history requirements
   - desktop/mobile priority
5. For SharePoint-backed apps, route to `sharepoint-to-canvas-app`.
6. For Dataverse-backed apps, identify tables and relationships before screen
   planning.
7. Route the final build/edit request to `canvas-app`, preserving these
   enterprise defaults:
   - development or sandbox first
   - no production write without explicit confirmation
   - visible receipts after mutations
   - clear empty, error, validation, and success states
   - accessible labels and responsive layout

## Do Not

- Do not bypass Canvas Authoring MCP for compile or sync.
- Do not edit `_EditorState.pa.yaml`.
- Do not claim a connector or data source exists until it is listed by the MCP
  session or confirmed by the user in Studio.
