# Copilot Instructions: Ai Native Workflow Automation
Description: A comprehensive skill for building AI-native organizations using skill files, resolver tables, and company brains to achieve 400x productivity gains.

# AI-Native Workflow Automation Skill

## Overview
This skill enables you to build organizations that achieve 400x productivity gains by treating AI as a workforce rather than just a tool. The core concepts are explained in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Identify automatable processes**
   - Start with repetitive, well-defined tasks
   - Document current human workflows

2. **Create skill files**
   - Each file represents one atomic capability
   - Follow templates from [Code Examples](references/code_examples.md)

3. **Build resolver tables**
   - Create routing logic for different task types
   - Test with trigger evaluations

4. **Implement company brain**
   - Start capturing organizational knowledge
   - Set up retrieval with provenance tracking

5. **Establish maintenance routines**
   - Regularly prune and update knowledge
   - Skillify all successful tasks

6. **Scale across organization**
   - Train all team members to create skill files
   - Monitor for pitfalls listed in [Common Pitfalls](references/common_pitfalls.md)

## Implementation Guidance
For detailed implementation advice, see the [Practical Guide](references/practical_guide.md). Key principles include:
- Always separate latent and deterministic space
- Never do one-off work - always skillify
- Design for AI's million-token context window

## Validation Steps
1. Test resolver tables with sample tasks
2. Verify skill files produce consistent outputs
3. Check company brain retrieval accuracy
4. Monitor for contradiction alerts
5. Measure productivity gains over time

## Maintenance
- Weekly: Review and prune knowledge base
- Monthly: Audit skill file effectiveness
- Quarterly: Reassess computation placement

Remember: Model quality is rented, but your company brain is owned. The organization that captures what it learns gets smarter every day.

## Reference Guides

### Code Examples

# Code Examples and Prompt Templates

## Basic Skill File Template
```markdown
# Skill: Process Customer Refund

## Purpose
Handle customer refund requests according to company policy

## Inputs
- Customer email or ticket
- Order details
- Reason for refund

## Steps
1. Verify order meets refund policy criteria
2. Calculate refund amount
3. Approve with manager if over $100
4. Process payment system update
5. Send customer confirmation

## Outputs
- Updated order status
- Refund transaction record
- Customer notification
```

## Resolver Table Example
```typescript
const resolverTable = {
  "customer_refund": "skills/process_refund.md",
  "invoice_processing": "skills/process_invoice.md",
  "technical_support": "skills/handle_support_ticket.md",
  "default": "skills/escalate_to_human.md"
};

function routeTask(taskType) {
  return resolverTable[taskType] || resolverTable.default;
}
```

## Context Engineering Prompt
```
You are an AI assistant with access to our company brain. Before responding to this customer request, please:

1. Retrieve all prior interactions with this customer
2. Find 3 similar cases and their resolutions
3. Review current policies related to this request
4. Synthesize this information before formulating your response

The request is: [PASTE REQUEST HERE]
```

## Skillification Prompt
```
I just completed this task successfully:
[TASK DESCRIPTION]

Please convert this into a reusable skill file with:
1. Clear purpose statement
2. Defined inputs
3. Step-by-step instructions
4. Expected outputs
5. Any relevant policy references

Format as markdown ready to add to our skills directory.
```

### Common Pitfalls

# Common Pitfalls and How to Avoid Them

## 1. Treating AI as Autocomplete
**Mistake**: Using AI just for code completion or simple suggestions
**Solution**: Structure your organization around skill files and treat AI as a workforce
**Example**: The fastest-growing YC companies had 95% AI-generated codebases by treating AI as workforce, not autocomplete

## 2. Uncurated Company Brains
**Mistake**: Letting your knowledge base become a garbage dump with great search
**Solution**: Implement strict hygiene practices with provenance tracking and contradiction checks
**Example**: Without curation, retrieval will surface stale facts with high confidence

## 3. Computation in the Wrong Space
**Mistake**: Putting deterministic tasks in latent space or vice versa
**Solution**: Clearly separate tasks requiring human judgment (latent) from repeatable processes (deterministic)
**Example**: Seat assignments must be stored in deterministic space while matching logic uses latent space

## 4. One-Off Work
**Mistake**: Solving problems individually without creating reusable skills
**Solution**: Always "skillify" successful tasks into reusable components
**Example**: Garry Tan's rule: "If you have to ask for something twice, you failed"

## 5. Overlooking Non-Technical Users
**Mistake**: Thinking only engineers can build these systems
**Solution**: Create interfaces that allow all team members to contribute skill files
**Example**: YC's finance team member who collapsed 100 Excel workbooks into a single app

## 6. Underestimating Scale Differences
**Mistake**: Designing for human working memory limits (7 items) rather than AI scale (million tokens)
**Solution**: Build processes that leverage AI's massive context window
**Example**: An agent can keep "three Harry Potter books" worth of information active simultaneously

### Core Concepts

# Core Concepts of AI-Native Workflow Automation

## Skill Files as Employees
A skill file is a markdown document that defines a single capability or job clearly enough for an AI agent to execute it. Think of each skill file as an employee with one specific role. For example, a skill file might define how to process an invoice or how to respond to a customer support ticket.

## Resolver Tables as Org Charts
A resolver table acts as an organizational chart for your AI workforce. When a task comes in, the resolver table determines which skill file (employee) should handle it. This is similar to how a traditional org chart routes work to different departments or individuals.

## Company Brains as Memory Layers
A company brain serves as the memory and knowledge base for your organization. It combines retrieval mechanisms with curation to ensure agents have the right context (the right three books open) for any given task. This is more than just RAG (Retrieval-Augmented Generation) - it includes provenance tracking, contradiction checks, and active pruning of stale information.

## Latent vs Deterministic Space
Understanding where computation happens is critical:
- **Latent space**: The LLM handles tasks requiring human-like judgment, taste, or understanding of vague requests
- **Deterministic space**: Traditional code handles precise, repeatable operations like data processing or calculations

## Working Memory Scale
While humans can hold about 7 items in working memory, AI agents can manage about a million tokens (roughly three Harry Potter books worth of information). This massive scale difference enables entirely new organizational structures.

### Practical Guide

# Practical Guide to Implementing AI-Native Workflows

## Getting Started
1. **Identify repetitive tasks**: Start with processes that are well-defined and frequently repeated
2. **Create initial skill files**: Document each task as a standalone markdown file with clear inputs, outputs, and steps
3. **Set up resolver tables**: Build routing logic to direct tasks to the appropriate skill files

## Scaling Your Implementation
1. **Build your company brain**: Start capturing organizational knowledge in a structured, retrievable format
2. **Implement context engineering**: Develop systems to ensure the right context is available for each task
3. **Establish hygiene practices**: Create processes for regularly updating and pruning your knowledge base

## Maintenance and Improvement
1. **Skillify everything**: Never do one-off work - always convert successful tasks into reusable skill files
2. **Monitor performance**: Set up trigger evaluations to test if resolver tables are routing correctly
3. **Handle contradictions**: Implement systems to detect and resolve conflicting information in your knowledge base

## Real-World Examples
- **Seating 800 people**: Combining deterministic space (seat assignments in a multi-dimensional array) with latent space (matching people who should meet)
- **Finance automation**: Collapsing 100 Excel workbooks into a single app built by a non-technical finance person managing agents
- **Medical research**: A father building a company brain with 80,000 markdown files to research his son's rare epilepsy condition

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[The New Physics of Business — Garry Tan, Y Combinator](https://www.youtube.com/watch?v=eBUyTS7SzV4)** by AI Engineer