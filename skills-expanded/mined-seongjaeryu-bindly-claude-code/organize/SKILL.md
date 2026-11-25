---
description: Organize knowledge into Sets
---

Help users organize their Bindly knowledge into curated Sets.

## What are Sets?

Sets are curated collections of knowledge versions, grouped by purpose:
- Project-specific knowledge bases
- Topic collections (e.g., "Authentication Patterns")
- Research compilations
- Learning paths

## Workflow

When the user wants to organize knowledge:

1. **Understand Goal**: What collection are they building?
   - New project starting? Create a fresh Set
   - Existing Set to expand? Find and add to it
   - Reorganizing? Review current structure

2. **Search Existing Sets**: Use `mcp_list_sets`
   - Show current Sets in the Space
   - Check if relevant Set already exists

3. **Create or Update**:
   - **New Set**: Use `request_create_set` with descriptive name
   - **Add to Set**: Use `request_add_version_to_set`
   - Remember: Sets contain specific versions, not bindings directly

4. **Curate**: Help select what to include
   - Search for relevant bindings
   - Review and pick the most useful versions
   - Suggest organization structure

5. **Share (Optional)**: If the user wants to share
   - Use `request_create_set_share` for public link
   - Set TTL (time-to-live) for the share

## Example Prompts

- "Create a Set for my Q1 project research"
- "Add this to my authentication patterns collection"
- "Organize my recent coding notes"
- "Share my API design Set with the team"

## Key Points

- Sets organize versions, not bindings (immutable snapshots)
- Same binding can appear in multiple Sets
- Sets can be shared publicly with time-limited links
- Organization helps future retrieval and cross-agent access
