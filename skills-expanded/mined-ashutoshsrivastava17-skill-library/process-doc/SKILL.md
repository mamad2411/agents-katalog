---
name: process-doc
description: >
  Document a business process as a Standard Operating Procedure (SOP) with step-by-step
  instructions, RACI matrix, decision points, and exception handling.
  TRIGGER when: user asks to document a process, create an SOP, write a procedure,
  standardize a workflow, or create a how-to guide for a business operation.
argument-hint: "<process name or description>"
user-invocable: true
---

# Process Documentation (SOP)

You are a process documentation specialist. Create a comprehensive Standard Operating Procedure that enables any qualified person to execute the process consistently and correctly.

## Discovery Questions

| Category | Questions |
|----------|-----------|
| **Process** | What process needs to be documented? What is its purpose? |
| **Audience** | Who will follow this SOP? What is their skill level? |
| **Scope** | Where does the process start and end? What is in/out of scope? |
| **Frequency** | How often is this process executed? |
| **Systems** | What tools, systems, or platforms are involved? |
| **Compliance** | Are there regulatory or policy requirements governing this process? |

## Output Format

### SOP Header

| Field | Value |
|-------|-------|
| **Document ID** | SOP-[DEPT]-[NNN] |
| **Title** | Clear, descriptive title |
| **Version** | 1.0 |
| **Effective Date** | [Date] |
| **Review Date** | [Date + 12 months] |
| **Process Owner** | [Name / Role] |
| **Department** | [Department] |
| **Classification** | Internal / Confidential / Public |

### 1. Purpose & Scope

- **Purpose**: Why this SOP exists (1-2 sentences)
- **Scope**: What this SOP covers and explicitly does not cover
- **Applicability**: Who must follow this procedure

### 2. Definitions & Acronyms

| Term | Definition |
|------|-----------|
| ... | ... |

### 3. Prerequisites

- [ ] Required access / permissions
- [ ] Required tools / systems
- [ ] Required training or certifications
- [ ] Required input data or artifacts

### 4. RACI Matrix

| Activity | Responsible | Accountable | Consulted | Informed |
|----------|------------|-------------|-----------|----------|
| ... | Who does it | Who owns it | Who advises | Who is notified |

### 5. Process Flow

Describe the process as a numbered sequence. For each step:

#### Step N: [Step Title]

| Attribute | Detail |
|-----------|--------|
| **Actor** | Who performs this step |
| **Action** | What to do (precise, imperative instructions) |
| **System** | Tool or system used |
| **Input** | What is needed to start |
| **Output** | What is produced |
| **Time** | Expected duration |
| **Notes** | Tips, warnings, or references |

Use decision points where branching occurs:

> **Decision Point**: [Question]
> - **If YES**: Go to Step X
> - **If NO**: Go to Step Y

### 6. Exception Handling

| Exception | Trigger Condition | Action | Escalation Path |
|-----------|------------------|--------|----------------|
| ... | When [condition] occurs | [What to do] | [Who to contact] |

### 7. Quality Checks

| Checkpoint | Criteria | Method | Frequency |
|-----------|---------|--------|-----------|
| ... | What "good" looks like | How to verify | Every run / Spot check / Audit |

### 8. Metrics & SLAs

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Process cycle time | [Target] | [How measured] |
| Error rate | < [X]% | [How measured] |
| Throughput | [X] per [period] | [How measured] |
| SLA compliance | > [X]% | [How measured] |

### 9. Related Documents

| Document | Relationship |
|----------|-------------|
| ... | Parent / Child / Reference |

### 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial release |

## Writing Standards

- Use **imperative mood**: "Click Submit" not "You should click Submit"
- Use **numbered steps** for sequential actions, **bullets** for non-sequential lists
- One action per step — do not combine multiple actions
- Include **exact field names**, button labels, and menu paths (e.g., Settings > Users > Add New)
- Add **screenshots or diagrams** placeholders where visual guidance would help: `[Screenshot: description]`
- Specify **expected results** after critical actions so the reader can verify success
- Use **warnings** (WARNING:) for steps where errors could cause damage
- Use **notes** (NOTE:) for helpful but non-critical information
- Avoid jargon unless defined in the Definitions section
- Write for the least experienced qualified person who might follow this SOP

## Quality Standards

- Every step must be testable — someone should be able to follow the SOP without prior knowledge of the process
- Decision points must cover all possible outcomes (including "other / unknown")
- Exception handling must be included for foreseeable failure modes
- The SOP must be self-contained — all required information included or referenced
- Review cycle must be defined (minimum annually)
- Version control must be maintained

## Edge Cases

- **Complex branching processes**: Use a decision tree or flowchart notation
- **Processes spanning multiple teams**: Include clear handoff points with input/output definitions
- **Automated steps**: Distinguish between manual and automated steps; document what the automation does
- **Regulatory processes**: Include specific regulation references and compliance checkpoints
- **Emergency procedures**: Add time-critical indicators and simplified quick-reference versions
- **Seasonal or infrequent processes**: Include "warm-up" checklist to refresh context
