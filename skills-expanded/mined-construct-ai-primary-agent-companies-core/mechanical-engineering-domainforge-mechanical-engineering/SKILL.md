---
memory_layer: durable_knowledge
para_section: pages/agents
gigabrain_tags: skills, domain-forge, mechanical-engineering-domainforge-mechanical-engineering
documentation
openstinger_context: skill-configuration
last_updated: 2026-04-09
related_docs:
  - ../agents/mechanical-engineering-domainforge-mechanical-engineering/AGENTS.md
  - ../teams/governance/TEAM.md
---

# mechanical engineering DomainForge mechanical engineering Skill

**Skill ID:** `mechanical-engineering-domainforge-mechanical-engineering`  
**Agent:** `mechanical-engineering-domainforge-mechanical-engineering`  
**Company:** DomainForge AI  
**Team:** Governance  
**Status:** Active  
**Type:** Domain Specialist Skill

## Purpose

Enables the agent to understand and document code structures, page implementations, and technical architecture for their assigned discipline within the Paperclip ecosystem.

## Capabilities

### Code Analysis
- Analyze discipline-specific codebase structure
- Document page layouts and component organization
- Map data models and database schemas
- Track API endpoints and integration points

### Technical Documentation
- Maintain discipline-specific technical guides
- Document implementation patterns and best practices
- Create reference materials for developers
- Track version changes and migration paths

### Quality Standards
- Ensure compliance with discipline-specific standards
- Validate code against discipline requirements
- Monitor technical debt and refactoring opportunities
- Support quality assurance processes

### Cross-Discipline Integration
- Coordinate with other engineering and business disciplines
- Ensure systems integrate with broader infrastructure
- Support multi-discipline project workflows
- Facilitate knowledge sharing across teams

## Knowledge Loading Protocol

Before beginning any task, the agent MUST resolve and load relevant knowledge files:

1. **Parse issue frontmatter** for `sector_ref` and `org_ref` fields
2. **Open KNOWLEDGE-REGISTRY.md** at `docs-paperclip/companies/domainforge-ai/knowledge/KNOWLEDGE-REGISTRY.md`
3. **Resolve sector knowledge:**
   - If `sector_ref` is present, filter the sector table for rows matching:
     - `sector_id` = issue's `sector_ref`
     - `discipline` = `mechanical`
   - Resolve each `knowledge_file` path relative to the registry location
   - Read all matched files into working context
4. **Resolve organisation knowledge:**
   - If `org_ref` is present, filter the organisation table for rows matching:
     - `org_slug` = issue's `org_ref`
   - Resolve each `knowledge_file` path relative to the registry location
   - Read all matched files into working context
5. **Proceed with task execution** using the loaded knowledge context

If the registry is missing or stale, fall back to convention-based discovery:
- Sector: `disciplines-sector-specific-details/{sector_ref}/knowledge/mechanical-*-knowledge.md`
- Organisation: `organisation-knowledge/{org_ref}/knowledge/**/*.md`

## Usage

This skill is automatically activated when the agent is assigned tasks related to their discipline domain.

## Success Criteria

- **Documentation Coverage**: 100% of discipline code documented
- **Technical Accuracy**: Zero critical documentation errors
- **Cross-Discipline Integration**: Seamless integration with all business and engineering disciplines
- **Developer Satisfaction**: >90% positive feedback from development teams

---

**Last Updated:** 2026-04-09  
**Maintainer:** DomainForge AI Governance Team  
**Version:** 1.0
