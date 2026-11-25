---
name: use-work-order
description: Use the Work Order JoAi app plugin when the task needs Work Order tools or workflows.
---

# Work Order

Connect Work Order to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Work Order tools available in this app.
- Explain what setup or authentication Work Order needs before I run an action.
- Use Work Order to help me with the task I describe next.

## Action Inventory

- `work-order-create` (collect, inline, inline, prompt, inline, prompt, inline, inline, prompt, inline, prompt) — Record field work: collect job details, match products and services, log activity to CRM, create a work item, and generate a PDF report.
- `work-order-create-bill` (collect) — Create a billing order for a work order. Takes the contact and matched product/service IDs from the work order and generates an invoice with payment link.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
