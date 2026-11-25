---
title: Electrical Document Generation
description: Generate electrical engineering documents through template-based pipelines: Concept → Design → Construction → Commissioning documents with structured data injection
version: 1.0
frequency_percent: 90.0
success_rate_percent: 97.0
gigabrain_tags: domainforge_ai, electrical-engineering, document-generation, templates, structured-data, compliance
openstinger_context: electrical-docs, document-pipeline
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00860_electrical-engineering/agent-data/domain-knowledge/00860_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/skills/domainforge_ai/electrical-commissioning/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-loto-compliance/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-sld-processing/SKILL.md
related_skills:
  - electrical-commissioning
  - electrical-loto-compliance
  - electrical-sld-processing
---

# Electrical Document Generation

## Overview
An AI-native document generation skill that produces all electrical engineering documents through structured data injection into verified templates. Covers four phases: Concept, Design, Construction/Testing, and Commissioning with quality validation and version control.

## When to Use This Skill
- Generating any electrical engineering deliverable document
- Producing SLDs, cable schedules, test reports, commissioning documentation
- Creating O&M manuals, certificate of compliance packages
- Producing regular reports (daily electrical logs, progress reports)
- Any structured electrical document requiring code-compliant content

## Prerequisites
- Document template (verified and current with applicable codes)
- Structured input data (from power system models, calculations, test results)
- Standards and code references (IEC, NEC, NFPA 70E, local regulations)
- Template configuration (document type, voltage level, project context)

## Step-by-Step Execution

### Step 1: Select Document Template
- Identify document type from phase (Concept, Design, Construction, Commissioning)
- Select appropriate template with correct version number
- Verify template is current with applicable codes
- Load template configuration parameters

### Step 2: Extract Data from Source Systems
- Pull structured data from power system models (bus data, equipment schedules)
- Extract calculation results (load flow, short circuit, protection settings)
- Retrieve test results (insulation resistance, continuity, earth resistance)
- Gather LOTO procedures, commissioning results, as-built changes

### Step 3: Validate Data Completeness
- Verify all required data fields populated
- Check data ranges are within expected limits
- Confirm code references are current
- Flag any missing or inconsistent data

### Step 4: Inject Data into Template
- Map structured data to template placeholders
- Apply conditional logic (include/exclude sections based on data)
- Generate narrative text from structured data
- Insert tables, diagrams, schedules as configured

### Step 5: Quality Validation
- Run completeness check against document specification
- Verify code compliance (all referenced clauses current)
- Check cross-references within document resolve
- Validate numerical data against source systems
- Generate quality report with any issues found

### Step 6: Generate Output
- Produce output in required format (PDF, DOCX, structured JSON, Excel)
- Apply project branding and formatting
- Include revision control information
- Generate metadata (author, date, version, applicable codes)

### Step 7: Archive with Version Control
- Store document in document management system
- Create version record with change history
- Update document status (draft, review, approved, issued)
- Distribute to stakeholders per project workflow

## Success Criteria
- 99%+ data accuracy vs source systems
- All required document sections complete
- Code references current and accurate
- Document format meets project specification
- Version control and audit trail maintained

## Common Pitfalls
- **Outdated Templates**: Templates not updated when codes change → reference outdated requirements
- **Missing Input Data**: Calculation or test results not available → incomplete documents
- **Code Changes**: Standards updated but templates not reviewed → non-compliant documents generated
- **Data Mismatch**: Input data inconsistent with actual conditions → inaccurate documents
- **Format Errors**: Output generation fails due to template-data incompatibility → document delay

## Cross-References
- 00860 Domain Knowledge: Document generation pipeline (Part 8, Part 12)
- Electrical SLD Processing: Provides power system model data
- Electrical Commissioning: Provides test results for commissioning documents
- LOTO Compliance: Provides procedures for safety documentation
- Standards: IEC 60617 (symbols), NEC, NFPA 70E

## Usage Example
```
Scenario: Generate cable schedule for 11kV switchgear installation
Step 1: Select cable_schedule_11kv_v3.docx template
Step 2: Extract data from power system model (cable types, routes, terminations)
Step 3: Validate all cables have source/destination, size, type, length
Step 4: Inject data: cable ID → table row, routing → path description
Step 5: Quality check: all cables present, sizes match calculations, terminations consistent with SLD
Step 6: Generate cable_schedule_11kv_switchgear_revA.xlsx + .pdf
Step 7: Archive with revision A, distribute to cable laying team
```

## Metrics
- Template coverage: 95%+ of document types supported
- Data accuracy: 99%+ vs source systems
- Review cycles: 50%+ reduction vs manual preparation
- Compliance: 100% of documents within regulatory timeframes