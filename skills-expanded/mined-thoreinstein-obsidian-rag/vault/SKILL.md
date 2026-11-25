---
name: vault
description: >-
  Use when the user wants to set or change their Obsidian vault path, or says
  "vault", "set vault", or "change vault".
---

# Set Vault Path

Configure the Obsidian vault path for this session.

## With Argument

If the user provides a path after `/vault`:
- Call `obsidian_set_vault` with the provided path

## Without Argument

If no path is provided:
- Ask the user: "What is the absolute path to your Obsidian vault?"
- Once they respond, call `obsidian_set_vault` with their path

## Confirmation

After setting, confirm: "Vault path set to: [path]"
