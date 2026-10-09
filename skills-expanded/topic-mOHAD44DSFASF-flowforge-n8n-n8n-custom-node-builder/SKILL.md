---
name: n8n-custom-node-builder
description: Scaffolding and packaging custom community node files for n8n.
---

# n8n Custom Node Builder Skill

This skill outlines guidelines for packaging custom n8n integration nodes.

## When to Use
Use when users want to generate TypeScript integrations, credentials types, or package assets matching n8n nodes templates.

## Workflow Steps
1.  Define authentication mechanics (API Key vs OAuth2) and operations.
2.  Run `flowforge node-new <name> --auth <auth> --resource <resource> --operation <list>`.
3.  Fill in the code templates. Ensure class properties are lint-compliant.

## Constraints
*   Ensure all community naming structures begin with `n8n-nodes-`.
*   Maintain clean typings and imports from `n8n-workflow`.
