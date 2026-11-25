---
title: Pre-Task Assessment & Readiness
frequency_percent: 95.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/shared/pre-task-assessment-readiness
gigabrain_tags: task-assessment, readiness-check, domain-knowledge, skill-generation, staffing-assessment, knowledge-research
openstinger_context: pre-task-readiness, knowledge-gathering, agent-staffing
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/codebase/agents/openclaw-teams/PromptForge_AI_Team.md
  - docs_construct_ai/skills/shared/workflow-implementation/SKILL.md
  - docs_construct_ai/skills/shared/subagent-driven-development/SKILL.md
related_skills:
  - workflow-implementation
  - subagent-driven-development
  - agent-accuracy-enhancement
  - writing-skills
---

I'm using the pre-task-assessment-readiness skill to assess task readiness before proceeding.

# Pre-Task Assessment & Readiness

## Overview

This skill defines the mandatory pre-task assessment workflow that MUST be executed BEFORE any new discipline workflow, domain task, or significant feature begins. It ensures the system:
1. Analyzes and reviews the task requirements
2. Assesses existing domain knowledge sufficiency
3. Researches knowledge gaps from public sources
4. Updates domain knowledge files with new findings
5. Updates glossary with missing terms and definitions
6. Assesses staffing and hires agents if gaps exist
7. Generates new skills if required

## When to Use This Skill

**Trigger Conditions:**
- New discipline workflow request (e.g., "implement procurement order workflow")
- New domain task assignment (e.g., "create logistics tracking feature")
- Significant scope change in existing workflows
- Request references a discipline with no existing domain knowledge
- Task requires specialized knowledge not currently documented

**Prerequisites:**
- Clear task description or prompt to assess
- Access to existing domain knowledge files
- Access to agent registry for staffing check
- Access to skills directory for skill gap analysis

## Step-by-Step Procedure

### Phase 1: Task Analysis & Review

**Steps:**
1. **Parse Task Requirements**
   - Identify the target discipline (e.g., 01900 Procurement, 01700 Logistics)
   - Extract all functional, technical, compliance, and mobile requirements
   - List all referenced documents, files, and systems

2. **Classify Task Complexity**
   - **Simple:** Single workflow, existing domain knowledge, adequate staffing
   - **Standard:** Multiple workflows, partial gaps, minor staffing needs
   - **Complex:** Multi-system integration, significant gaps, major staffing needs

3. **Map to Existing Capabilities**
   - List all existing skills that relate to this task (check `/skills/` directory)
   - List all existing agents that can work on this task (check agent registry)
   - List all existing domain knowledge files for this discipline

4. **Produce Task Analysis Report**
   ```
   TASK ANALYSIS REPORT — [Task Name]
   Target Discipline: [Code & Name]
   Task Complexity: [Simple / Standard / Complex]
   Existing Skills: [List with locations]
   Existing Agents: [List with capabilities]
   Existing Domain Knowledge: [List with locations]
   Gaps Identified: [List]
   Readiness: [READY / NEEDS PREPARATION / BLOCKED]
   ```

### Phase 2: Domain Knowledge Assessment

**Steps:**
1. **Inventory Existing Domain Knowledge**
   - Locate discipline's domain knowledge file (e.g., `1900_DOMAIN-KNOWLEDGE.MD`)
   - Locate discipline's glossary file (e.g., `1900_GLOSSARY.MD`)
   - List all related documentation (API specs, integration docs, workflow docs)

2. **Assess Knowledge Completeness**
   
   | Assessment Area | Criteria | Pass/Fail |
   |-----------------|----------|-----------|
   | Role & Scope | Clear role definition and boundaries | |
   | Core Knowledge | Order types, processes, data elements | |
   | Behavioral Rules | Agent persona, communication style | |
   | Scenarios | Common scenarios with responses | |
   | Workflow Architecture | Process flows, system integration | |
   | Reference Materials | Standards, terms, lead-times | |
   | Safety Boundaries | What agent must NOT do | |

3. **Assess Glossary Completeness**
   
   | Assessment Area | Criteria | Pass/Fail |
   |-----------------|----------|-----------|
   | Term Coverage | All acronyms defined | |
   | Technical Terms | Domain-specific terms defined | |
   | Quality | Actual definitions (no placeholder text) | |
   | Completeness | 20+ minimum for mature discipline | |

4. **Produce Knowledge Assessment Report**
   
### Phase 3: Knowledge Gap Research (Public Sources)

**Steps:**
1. **Prioritize Knowledge Gaps** by severity (HIGH first)

2. **Research from Public Sources:**
   
   | Gap Type | Research Sources |
   |----------|-----------------|
   | Industry Standards | ISO, ASTM, SANS, EN standards bodies |
   | Regulatory Requirements | Government publications, regulatory agencies |
   | Best Practices | PMI, CIPS, professional associations |
   | Technical Specifications | Vendor docs, open-source project docs |
   | Academic Knowledge | Google Scholar, research papers |
   | Terminology | Wikipedia, industry glossaries, standards bodies |

3. **Source Verification Protocol:**
   - Cross-reference findings against at least 2 independent sources
   - Prioritize authoritative sources (standards bodies, regulatory agencies)
   - Document source URLs and access dates
   - Flag conflicting information between sources

### Phase 4: Domain Knowledge File Update

**Steps:**
1. Map research findings to domain knowledge file sections
2. Update existing sections or add new sections
3. Include source citations for new content
4. Update version number and last_updated date
5. Validate: all sections complete, no placeholder text, cross-references resolve

### Phase 5: Glossary Update

**Steps:**
1. Extract all unique terms from updated domain knowledge file
2. Generate definitions with this format:
   ```
   ### Term Name
   **Definition:** [Clear, concise definition]
   **Context:** [How used in this discipline]
   **Related Terms:** [Cross-references]
   **Source:** [Source reference if researched]
   ```
3. Organize by category: Processes, Documentation, Order Types, Financial Terms, Shipping Terms, Quality Terms, Systems & Technology
4. Validate: minimum 20 terms, no placeholder text, cross-references resolve

### Phase 6: Staffing Assessment & Agent Hiring

**Steps:**
1. Map task requirements to agent capabilities
2. Query agent registry for available agents with matching capabilities
3. Identify staffing gaps
   
   ```
   STAFFING ASSESSMENT — [Task]
   Required Capabilities: [List with Assigned Agent / GAP]
   Current Staffing: [Number]
   Staffing Gaps: [Number and description]
   Status: [ADEQUATE / NEEDS ADDITIONAL / CRITICAL]
   ```

4. If gaps exist, create agent definitions with role, responsibilities, specialization, reporting structure, and company assignment
5. Generate SQL migration file for new agents at `/sql/creations/create-[discipline]-[agent]-agent.sql`

### Phase 7: Skill Generation

**Steps:**
1. Review task requirements, domain knowledge, and staffing to identify skill needs
2. Check `/skills/` directory for existing skills that can be adapted
3. Generate new skill files following standard SKILL.md structure:
   - YAML frontmatter (title, frequency, success_rate, tags)
   - Overview section
   - When to Use This Skill (triggers, prerequisites)
   - Step-by-Step Procedure
   - Success Criteria checklist
   - Common Pitfalls
   - Cross-References (related skills, agents)
   - Example Usage
   - Performance Metrics
4. Register skill at appropriate path:
   - Domain-specific: `skills/domainforge_ai/[skill-name]/SKILL.md`
   - Infrastructure: `skills/infraforge_ai/[skill-name]/SKILL.md`
   - Shared: `skills/shared/[skill-name]/SKILL.md`

## Success Criteria

- [ ] Task analysis report produced with complexity classification
- [ ] Domain knowledge file assessed with Pass/Fail for all 7 areas
- [ ] Glossary assessed with Pass/Fail for all 4 areas
- [ ] Knowledge gaps researched from at least 2 public sources per gap
- [ ] Domain knowledge file updated (or confirmed sufficient)
- [ ] Glossary updated with 20+ properly defined terms (or confirmed sufficient)
- [ ] Staffing assessed with agent-to-capability mapping
- [ ] New agents defined with SQL migration (if gaps found)
- [ ] New skills created and registered (if gaps found)
- [ ] Final readiness report produced with sign-off

## Common Pitfalls

1. **Skipping Phase 2 Assessment** — Always assess existing knowledge FIRST before researching. You may already have what you need.
2. **Using Unreliable Sources** — Prioritize standards bodies, regulatory agencies, and peer-reviewed sources over blogs and opinion pieces.
3. **Placeholder Definitions in Glossary** — Every term must have an actual definition. Placeholder text like "Definition of [term]" is unacceptable.
4. **Hiring Without Need Analysis** — Only hire new agents after exhausting existing agent capabilities and cross-team assignments.
5. **Creating Duplicate Skills** — Always check existing skills directory before creating new skills.
6. **Missing Cross-References** — New domain knowledge and glossary entries must cross-reference related files and terms.

## Cross-References

### Related Skills
- `workflow-implementation` — Execute this assessment BEFORE Step 1 of workflow implementation
- `subagent-driven-development` — Execute assessment before subagent dispatch
- `agent-accuracy-enhancement` — Execute staffing check before deployment
- `writing-skills` — Execute skill generation when new skills are needed

### Related Agents
- `PromptForge Sage` — Overall assessment lead, quality gates
- `PromptForge Scholar` — Research and knowledge gathering
- `PromptForge Blueprint` — Skill design and templates
- `PromptForge Cascade` — Workflow analysis
- `PromptForge Specialist` — Domain adaptation

## Example Usage

**Scenario:** "Implement the 01900 Procurement Order Creation workflow"

1. Phase 1: Identify procurement discipline, list existing skills/agents/knowledge
2. Phase 2: Assess 1900_DOMAIN-KNOWLEDGE.MD and 1900_GLOSSARY.MD completeness
3. Phase 3: Research any gaps found (e.g., glossary had placeholder text)
4. Phase 4: Update domain knowledge file with research findings
5. Phase 5: Rebuild glossary with 29+ properly defined terms
6. Phase 6: Assess staffing — identify gaps, define new agents if needed
7. Phase 7: Create missing skills (procurement-order-management, supplier-evaluation, etc.)
8. Produce final readiness report: "READY TO PROCEED"

## Performance Metrics

**Based on 1 assessment (Procurement Order Review, 2026-03-31):**
- **Frequency:** 100% of new discipline workflows should use this skill
- **Target Success Rate:** 90% of assessments result in READY status after remediation
- **Average Duration:** 4-6 hours for Standard complexity tasks
- **Knowledge Gap Fill Rate:** Target 95% of HIGH gaps resolved from public sources
- **Staffing Adequacy Rate:** Target 90% of tasks have adequate staffing after assessment