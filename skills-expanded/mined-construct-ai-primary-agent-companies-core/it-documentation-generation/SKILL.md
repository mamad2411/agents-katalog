---
title: IT Documentation Generation
description: Skill for auto-generation of system documentation, architecture diagrams, API guides, and operational runbooks from code and system state in the ConstructAI platform
frequency: As code changes occur or scheduled updates
success_rate: 90%
tags:
  - it-operations
  - documentation-generation
  - api-documentation
  - architecture-diagrams
  - runbooks
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/skills/domainforge_ai/civil-documentation/SKILL.md
---

# IT Documentation Generation

## Overview

This skill covers automated generation of IT system documentation from code, configuration, and system state. It encompasses architecture diagram generation, API documentation, database schema documentation, operational runbooks, and component reference guides. Primary agent: 02050-005 Doc Generator. Supporting skills: `domainforge_ai/civil-documentation`.

## Triggers

- New component deployed to production
- API endpoint added or modified
- Database schema change deployed
- System architecture updated
- Scheduled documentation update cycle
- New configuration change requires documentation

## Prerequisites

- Access to codebase and deployment state
- Component topology documentation
- API route definitions and schemas
- Database schema definitions
- Existing documentation templates

## Steps

### Step 1: Source Data Collection
- Scan codebase for component definitions
- Extract API route definitions and request/response schemas
- Extract database schema (tables, columns, relationships, indexes)
- Collect deployment topology (services, environments, connections)
- Gather configuration parameters and defaults

### Step 2: Template Selection
- Select appropriate template for document type (architecture, API, schema, runbook, component reference)
- Verify template currency against documentation standards
- Load template with document metadata and context

### Step 3: Structured Data Injection
- Map collected data to template placeholders
- Generate architecture diagrams from component topology
- Generate API endpoint listings with request/response examples
- Generate schema documentation with data types and constraints
- Inject provenance tags on all inserted data

### Step 4: Conditional Logic Processing
- Apply conditional sections based on data availability
- Omit sections where data is not available
- Include warnings for data that could not be retrieved
- Apply formatting based on document type and audience

### Step 5: Quality Validation
- Verify completeness (no empty sections, all required data present)
- Verify links and cross-references resolve
- Check terminology against IT glossary
- Validate generated diagrams render correctly
- Review for consistency with existing documentation standards

### Step 6: Version Control
- Assign documentation version number
- Record change summary with code change reference
- Create/update table of contents
- Generate diff from previous version

### Step 7: Output & Distribution
- Generate output in required formats (MD, PDF, HTML)
- File to correct documentation location
- Update documentation index
- Notify stakeholders of documentation updates

## Success Criteria

- All required sections populated with accurate data
- Cross-references and links resolve correctly
- Documentation matches current system state
- All formats generated successfully
- Version history updated
- Stakeholders notified of changes

## Common Pitfalls

1. **Stale data**: Ensure source data is from current deployment, not staging
2. **Missing components**: New components may not be in topology scans
3. **Diagram rendering**: Auto-generated diagrams may need manual cleanup
4. **Template staleness**: Verify templates match current documentation standards
5. **Empty sections**: Handle gracefully with "not available" markers

## Cross-References

- `it-system-architecture-design/SKILL.md` — Architecture design input for diagrams
- `it-code-generation-scaffolding/SKILL.md` — Generated code documentation
- `domainforge_ai/civil-documentation/SKILL.md` — Document generation patterns
- `shared/systematic-debugging/SKILL.md` — Investigating documentation inconsistencies

## Usage

Apply this skill when generating or updating system documentation after code changes, creating API documentation for new endpoints, or performing scheduled documentation updates.

## Metrics

- **Documentation Coverage**: 90%+ of code and system components documented
- **Accuracy**: 95%+ of generated documentation matches system state
- **Timeliness**: Documentation updated within 24 hours of code change
- **Completeness**: 95%+ of template sections populated with relevant data
- **Format Success**: 100% of output formats generated without errors