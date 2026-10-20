---
name: obsidian-vault-sync
description: Sync agent memory, plans, and tasks directly into an Obsidian vault.
---
# Obsidian Vault Sync Skill

Bridges the AI's internal memory artifacts with a user's Obsidian Vault. 

## When to use this skill
- When the user asks to save plans, tasks, or research to their Obsidian vault.
- When generating complex markdown artifacts that the user wants to visually explore using Obsidian's graph view.

## Usage
1. Identify the location of the user's Obsidian Vault (usually requested via prompt or environment variable).
2. Write structured markdown files directly into the Vault directory.
3. Use `[[Wikilinks]]` to connect related concepts, plans, and tasks so they show up beautifully in the Obsidian graph.
