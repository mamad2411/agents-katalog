---
name: crm-workflows
description: Build and operate CRM-native automations in Twenty — workflows, versions, steps, edges, triggers, logic functions, runs, and validation. Use for "when X happens do Y" automation inside the CRM (auto-assign, notify, update fields, send email on stage change).
---

# CRM Workflows

Read the `crm` skill first. Workflows are Twenty's built-in automation:
a trigger plus a graph of steps, versioned, with only one active version at a
time.

## Model

- **Workflow** — the container. `List Workflows`, `Delete Workflow`.
- **Version** — an editable draft or an activated snapshot.
  `Get Workflow Current Version` shows the live definition.
- **Steps** — nodes: record create/update/delete, send email, HTTP request,
  code (logic function), branches/filters. **Edges** connect steps.
- **Trigger** — record event (created/updated/deleted, with filters), manual,
  cron/schedule, or webhook.
- **Runs** — executions with per-step status. `List Workflow Runs`,
  `Get Workflow Run`.

## Building a workflow

Prefer the one-shot builder when creating from scratch:

1. `Create Complete Workflow` — name, trigger, steps, and edges in a single
   call. Read its input schema carefully and pass exact object/field names
   from `Get Object Metadata`.
2. Otherwise compose manually: `Create Draft From Workflow Version` (or start
   from the current version), then `Create Workflow Version Step`,
   `Create Workflow Version Edge`, `Update Workflow Version Trigger`,
   `Update Workflow Version Step`, `Update Workflow Version Positions`
   (canvas layout), `Delete Workflow Version Step/Edge` to prune.
3. For code steps: `List Logic Function Tools`, `Get Logic Function Source`,
   `Update Logic Function Source` edit the serverless function behind the
   step; `Compute Step Output Schema` derives a step's output shape so
   downstream steps can reference its variables.
4. **Validate before activating**: `Validate Workflow` catches broken
   references and incomplete steps.
5. `Activate Workflow Version` to go live; `Deactivate Workflow Version` to
   stop it. Activation supersedes the previously active version.

## Operating and debugging

- Verify a new automation by causing (or asking the user to cause) a matching
  event, then checking `List Workflow Runs` for the workflow and inspecting
  the failing step via `Get Workflow Run`.
- Common failures: renamed fields (schema drift), select values that no
  longer exist, HTTP steps hitting auth errors. Fix in a new draft, validate,
  re-activate.

## Safety

- Workflows act on their own from the moment they are activated. Recap what
  the automation will do and get user confirmation **before activating**,
  especially for anything that sends email or deletes/overwrites records.
- Deactivate rather than delete when the user wants an automation "off";
  deleting the workflow loses its history.
