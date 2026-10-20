# Copilot Instructions: Ai Agent Workflow Execution
Description: A comprehensive skill for AI agents to perform complex tasks by perceiving, reasoning, acting, and learning in iterative cycles with optional human oversight.

# AI Agent Workflow Execution Skill

## Overview
This skill enables you to perform complex academic and research tasks through iterative perception-reasoning-action-learning cycles. Unlike single-query responses, you'll decompose tasks, utilize specialized tools, and refine outputs through multiple iterations - functioning more like a research assistant than a simple chatbot. See [Core Concepts](references/core_concepts.md) for foundational principles.

## Step-by-Step Workflow
1. **Task Reception**
   - Parse the user request for key components (topic, scope, deliverables)
   - Example: "Create literature review on perovskite solar cells focusing on stability studies from 2018-2023"

2. **Plan Formulation**
   - Break into subtasks (literature search, analysis, synthesis)
   - Allocate sub-agents if needed
   - Present plan for approval ("I'll search 50 papers, identify top 20, then create tables comparing degradation rates")

3. **Execution with Tools**
   - Use connected APIs (Consensus, Zotero)
   - Apply prompt templates from [Prompt Templates](references/prompt_templates.md)
   - Maintain audit trail of sources

4. **Quality Control**
   - Cross-verify 20% of references
   - Check for hallucination using fact-verification tools
   - Format according to academic standards

5. **Iterative Refinement**
   - Incorporate user feedback
   - Limit to 3-5 refinement cycles
   - Finalize when all quality metrics pass

## Best Practices
1. **Clear Scope Definition**
   - Bad: "Find some papers about batteries"
   - Good: "Find 10 peer-reviewed papers about solid-state battery interfaces published in Nature journals since 2020"

2. **Controlled Automation**
   - Set runtime limits (max 60 minutes for complex tasks)
   - Implement mandatory checkpoints for human review

3. **Academic Rigor**
   - Always trace claims to verifiable sources
   - Use academic formatting (APA/MLA)
   - Disclose search methodology

## Common Pitfalls
1. **Unbounded Research**
   - Without clear limits: "The agent searched 500 papers when 50 would suffice"
   - Solution: Set explicit bounds ("Include maximum 30 references")

2. **Format Inconsistency**
   - Mixing citation styles in one document
   - Solution: Specify style upfront and validate before delivery

3. **Over-automation**
   - Making significant research decisions without human input
   - Solution: Build in approval steps for hypothesis generation or gap analysis

## Validation Protocol
1. **Source Verification**
   - Randomly check 20% of citations exist and support claims
2. **Logical Flow Check**
   - Ensure arguments follow coherent structure
3. **Originality Assessment**
   - Compare against source materials for proper synthesis
4. **User Acceptance Testing**
   - Confirm output meets intended use case

For complete workflow details, consult the [Practical Guide](references/workflow_guide.md). Always use the structured [Prompt Templates](references/prompt_templates.md) for consistent results.

## Reference Guides

### Core Concepts

# Core Concepts of Agentic AI

Agentic AI represents a paradigm shift from simple query-response interactions to complex, multi-step workflows with autonomous execution capabilities. Unlike traditional LLM interactions that provide single-pass responses, agentic systems employ four key phases:

1. **Perception**: The agent gathers information from multiple sources - its internal knowledge base, web searches, uploaded documents (like research papers), and any contextual data provided by the user. For academic tasks, this might involve searching scholarly databases or analyzing provided PDFs.

2. **Reasoning**: The agent develops an execution plan by breaking down the main task into subtasks. This involves determining what information is needed, what analyses to perform, and what format the output should take. The agent may create sub-agents to handle specialized components (e.g., one for literature search, another for data visualization).

3. **Action**: The agent executes its plan by generating content (text, tables, presentations), retrieving data, or performing analyses. Academic examples include creating literature reviews, generating hypotheses, or formatting research presentations.

4. **Learning**: The agent evaluates its outputs for quality and relevance, potentially refining them through multiple iterations. It may request human feedback ("How deep should I go with this analysis?") or automatically improve based on predefined criteria.

Key differentiators from standard LLM use:
- **Iterative refinement**: May take minutes to hours versus seconds
- **Multi-modal outputs**: Can produce documents, slides, data visualizations
- **Tool integration**: Leverages specialized APIs and connectors
- **Human-in-the-loop**: Can pause for approval at decision points

### Prompt Templates

# AI Agent Prompt Templates

## Literature Review Template
```
Create an academic literature review on [TOPIC]. Focus on:
- [NUMBER] seminal papers from [TIME PERIOD]
- [NUMBER] recent studies from last [YEARS] years
Required elements:
1. Comparative tables of [SPECIFIC METRICS]
2. Timeline of key developments
3. Identification of 3-5 major research gaps

Search parameters:
- Use [TOOL NAME] for primary searches
- Include studies with [INCLUSION CRITERIA]
- Exclude [EXCLUSION CRITERIA]

Process:
1. Present search plan for approval
2. Deliver outline before full draft
3. Limit to [NUMBER] refinement cycles
```

## Research Hypothesis Generation
```
Generate testable hypotheses based on:
- This paper: [ATTACH PDF/DOI]
- My existing data: [DESCRIBE DATASET]

Constraints:
- Must be testable with [AVAILABLE RESOURCES]
- Should address gaps in [SPECIFIC FIELD]
- Prioritize hypotheses with [DESIRED CHARACTERISTICS]

Process:
1. First identify 3 key papers to ground hypotheses
2. Propose 5 candidate hypotheses
3. Refine to top 3 based on novelty/feasibility
```

## Presentation Generation
```
Convert this [SOURCE MATERIAL] into a [NUMBER]-minute presentation for [AUDIENCE TYPE].

Requirements:
- [NUMBER] slides maximum
- Include [SPECIFIC ELEMENTS]
- Use [STYLE GUIDELINES]

Process:
1. Show slide outline for approval
2. Apply branding from [STYLE GUIDE]
3. Add speaker notes for key slides
```

Always include these control parameters:
- "Wait for approval after [SPECIFIC STAGE]"
- "Limit runtime to [MAX MINUTES]"
- "Verify all citations with [TOOL NAME]"

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[What Is Agentic AI? AI Agents and the Revolution That Changes Everything](https://www.youtube.com/watch?v=fOfy-OsKWf4)** by Andy Stapleton

### Workflow Guide

# Practical Workflow Guide for AI Agents

## Task Initiation
Begin by clearly defining the task scope and requirements. Academic tasks typically fall into these categories:
- Literature reviews ("Create a review of OPV devices focusing on indoor use")
- Research gap analysis ("Identify gaps in my PhD project on nanomaterials")
- Presentation generation ("Make a 10-minute conference presentation from this paper")

## Execution Parameters
Set these critical parameters upfront:
1. **Depth**: Specify search breadth ("Include 10 seminal papers and 20 recent studies")
2. **Format**: Define output structure ("Include tables comparing device efficiencies")
3. **Tools**: Designate specialized resources ("Use Consensus for scholarly searches")
4. **Checkpoints**: Determine where human input is required

## Quality Control Measures
Implement these validation steps:
1. **Source Verification**: Cross-check 20% of references for accuracy
2. **Hallucination Check**: Flag unsupported claims for review
3. **Format Compliance**: Ensure output matches requested structure
4. **Iteration Limits**: Set maximum refinement cycles (typically 3-5)

## Specialized Academic Tools
Integrate these common academic resources:
- **Consensus**: For verified paper searches
- **Zotero**: Reference management
- **Overleaf**: LaTeX document generation
- **Figshare**: Data visualization

Example workflow timeline for literature review:
1. Minutes 0-5: Task decomposition and plan formulation
2. Minutes 5-20: Initial data gathering
3. Minutes 20-30: First draft generation
4. Minutes 30-45: Refinement based on quality checks
5. Minutes 45-60: Final formatting and delivery