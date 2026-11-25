---
name: knowledge-curator-domainforge
description: >
  Use when the Knowledge Registry needs to be rebuilt, validated, or updated. This skill handles scanning sector-specific and organisation knowledge directories, maintaining the KNOWLEDGE-REGISTRY.md index, and ensuring all DomainForge discipline agents can resolve knowledge references at runtime.
---

# Knowledge Curator - DomainForge AI Knowledge Registry Maintenance

## Overview
Maintains the DomainForge AI Knowledge Registry (`knowledge/KNOWLEDGE-REGISTRY.md`). Scans `disciplines-sector-specific-details/*/knowledge/` and `organisation-knowledge/*/knowledge/` directories, validates file paths, and rebuilds the registry index on demand.

## When to Use
- When knowledge files have been added or updated in sector-specific or organisation directories
- When a new organisation is added to `organisation-knowledge/`
- When a new sector is added to `disciplines-sector-specific-details/`
- When registry validation is needed (checking for broken links or orphaned entries)
- **Don't use when:** Only discipline-specific workflow changes are needed (use the appropriate discipline agent)

## Core Procedures

### Procedure 1: Rebuild Knowledge Registry

1. **Scan Sector Knowledge Directory**
   - Navigate to `disciplines-sector-specific-details/*/knowledge/`
   - For each `{discipline}-*-knowledge.md` file, extract:
     - `sector_id`: parent directory name (e.g., `00001-solar-installations`)
     - `discipline`: prefix before `-` in filename (e.g., `electrical` from `electrical-solar-knowledge.md`)
     - `knowledge_file`: relative path from registry location
   - Add each entry to the sector table

2. **Scan Organisation Knowledge Directory**
   - Navigate to `organisation-knowledge/*/knowledge/`
   - For each file, extract:
     - `org_slug`: parent directory name (e.g., `GPC`)
     - `knowledge_category`: descriptive category based on filename (e.g., `company-profile`, `core-workflows`)
     - `knowledge_file`: relative path from registry location
   - Add each entry to the organisation table

3. **Validate All Paths**
   - Resolve each `knowledge_file` path relative to `knowledge/KNOWLEDGE-REGISTRY.md`
   - Verify the file exists
   - Flag any broken paths for removal

4. **Update Registry**
   - Update `last_rebuilt` timestamp to current time
   - Commit the updated registry

### Procedure 2: Validate Registry Integrity

1. Read all entries from `KNOWLEDGE-REGISTRY.md`
2. Resolve each file path and verify existence
3. Report:
   - ✅ Valid entries (file exists)
   - ⚠️ Orphaned entries (file missing — suggest removal)
   - ⚠️ Unregistered files (knowledge file exists but no registry entry — suggest addition)

### Procedure 3: Coordinate Agent Creation

When knowledge coverage analysis reveals a discipline gap that requires a new agent:
1. Document the gap (sector, discipline, required knowledge)
2. Coordinate with `paperclipforge-ai-atlasagentcreator` to create the new agent
3. Update the registry after the agent is created

## File Discovery Patterns

### Sector Knowledge Files
```
disciplines-sector-specific-details/{sector_id}/knowledge/{discipline}-{sector}-knowledge.md
```
Example: `disciplines-sector-specific-details/00001-solar-installations/knowledge/electrical-solar-knowledge.md`

### Organisation Knowledge Files
```
organisation-knowledge/{org_slug}/knowledge/{category}/{filename}.md
```
Example: `organisation-knowledge/GPC/knowledge/industry-context/company-profile.md`

## Success Criteria
- Registry entries match actual files 1:1 (no orphans, no gaps)
- All file paths resolve correctly
- `last_rebuilt` timestamp is current
- Discipline agents can resolve knowledge references at runtime

## Error Handling
- **Error:** File path in registry does not resolve
  **Response:** Remove orphaned entry, flag for review
- **Error:** Knowledge file exists but no registry entry
  **Response:** Add entry to registry, flag for review
- **Error:** Duplicate entries found
  **Response:** Deduplicate, keep the valid path

## Cross-Team Integration
- Coordinates with `paperclipforge-ai-atlasagentcreator` for new agent creation
- Reports to `orion-domainforge-ceo`
- Supports all DomainForge AI discipline agents