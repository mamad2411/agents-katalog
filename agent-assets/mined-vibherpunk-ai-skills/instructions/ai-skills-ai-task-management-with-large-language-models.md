# Copilot Instructions: Ai Task Management With Large Language Models
Description: Skill for effectively delegating complex, high-value tasks to large language models (LLMs) by properly scoping work, preparing data inputs, and reviewing outputs at scale.

# AI Task Management with Large Models

## Overview
This skill enables you to effectively delegate complex, high-value tasks to large language models (LLMs) by:
1. Identifying tasks suited for models like Fable 5 ([Core Concepts](references/core_concepts.md))
2. Preparing comprehensive input packages ([Practical Guide](references/practical_guide.md))
3. Implementing robust validation workflows ([Code Examples](references/code_examples.md))

## Step-by-Step Workflow

1. **Task Identification**
   - List pain points that consume disproportionate time
   - Filter for tasks with:
     - Clear success criteria
     - Available source data
     - Low creative judgment requirements

2. **Economic Assessment**
   - Estimate token costs using model pricing
   - Compare against human labor hours
   - Only proceed if ROI > 3:1

3. **Data Preparation**
   - Gather all source materials
   - Annotate with context notes
   - Structure for model comprehension:
     ```python
     # From [Code Examples](references/code_examples.md)
     input_package = {
         "sources": [
             {"type": "csv", "description": "Q2 customer exports"},
             {"type": "pdf", "description": "Product specs v2.3"}
         ],
         "special_instructions": "Ignore draft watermarks"
     }
     ```

4. **Task Specification**
   - Define success criteria quantitatively
   - Specify review protocols
   - Set runtime constraints

5. **Execution**
   - Submit full package to model
   - Resist hovering during processing
   - Monitor for system alerts only

6. **Validation**
   - Apply predefined checks
   - Sample outputs thoroughly
   - Document all revisions required

## Best Practices
- **Think in Weeks Saved**: Target tasks that would take humans 2+ weeks
- **Pre-Process Data**: Spend 10-20% of expected savings time preparing inputs
- **Version Control**: Maintain copies of all inputs/outputs for audit trails
- **Model Steering**: Provide style guides, previous examples, and rubrics

## Common Pitfalls
1. **Under-Scoping**: 
   - *Bad*: "Improve this email" 
   - *Good*: "Audit all client comms from Q2 for compliance gaps"
2. **Over-Supervision**: 
   - Interrupting model processing wastes resources
3. **Vague Criteria**: 
   - "Make it better" → Unverifiable
   - "Reduce word count by 15% while keeping all key terms" → Measurable

## Validation Framework
1. **Automated Checks**:
   - Scripted validation of structured outputs
   - Statistical sampling of decisions
2. **Human Review**:
   - Spot-check nuanced judgments
   - Validate edge case handling
3. **Process Audit**:
   - Verify all input data was processed
   - Confirm no silent failures occurred

## Implementation Notes
- Start with 1-2 high-impact tasks weekly
- Document lessons after each project
- Gradually increase complexity as trust builds
- Combine with traditional automation for hybrid workflows

## Reference Guides

### Code Examples

# Code Examples for AI Task Management

## Task Specification Template
```python
task_spec = {
    "task_name": "CRM Data Deduplication",
    "input_sources": [
        {"type": "csv_export", "location": "s3://crm-exports/2024-q2.csv"},
        {"type": "api", "endpoint": "https://api.company.com/customers"}
    ],
    "success_criteria": {
        "completeness": "100% records processed",
        "accuracy": "<0.1% false positive merges",
        "output_format": "Standardized JSON customer profiles"
    },
    "constraints": {
        "privacy": "Do not process payment info columns",
        "timeout": "24h max runtime"
    },
    "review_protocol": {
        "sample_size": "5% random sampling",
        "validation_checks": ["email_format", "postal_code_valid"]
    }
}
```

## Prompt Structure for Large Tasks
```markdown
# PROJECT: Annual Report Fact-Checking

## CONTEXT
- Company: Acme Corp (industrial manufacturing)
- Audience: Investors and regulators
- Style Guide: [LINK_TO_STYLEGUIDE]

## SOURCE MATERIALS
1. Draft report PDF: [LINK]
2. Supporting data: [LINK_TO_SPREADSHEET]
3. Previous year's report: [LINK]

## DELIVERABLES
- Annotated PDF with all factual claims verified
- Appendix of uncorroborated statements
- Consistency matrix against last year's report

## PROCESS INSTRUCTIONS
1. First pass: Flag statistically improbable claims
2. Second pass: Cross-reference with source data
3. Third pass: Check all numerical references

## QUALITY CONTROLS
- Zero tolerance for false verifications
- 100% coverage of numerical data
- Style consistency with previous reports
```

## Output Validation Script
```python
def validate_output(task_output, success_criteria):
    """Sample validation function for programmatic checks"""
    errors = []
    
    # Check completeness
    if len(task_output["processed_items"]) != task_output["total_items"]:
        errors.append(f"Completeness fail: {len(task_output['processed_items'])}/{task_output['total_items']} processed")
        
    # Check accuracy sample
    sample = random.sample(task_output["decisions"], 
                          max(100, int(0.05*len(task_output["decisions"]))))
    false_positives = [d for d in sample if d["action"] == "merge" and not validate_merge(d)]
    
    if len(false_positives)/len(sample) > 0.001:
        errors.append(f"Accuracy fail: {len(false_positives)} false merges in sample")
        
    return {"valid": len(errors) == 0, "errors": errors}
```

### Core Concepts

# Core Concepts of AI Task Management

## The Big Model Shift
Modern LLMs like Fable 5 represent a paradigm shift where the limiting factor is no longer model capability but human imagination in task formulation. These models can handle entire projects (e.g., refactoring codebases, processing 40,000 customer records) rather than just discrete prompts.

## Task Imagination
Unlike traditional delegation of defined tasks, this requires identifying:
- Undocumented pain points ("rain clouds over your work")
- Projects considered too large/complex for automation
- Tasks where quality matters more than speed

## Economic Considerations
At ~$50/million output tokens, these models demand:
- High-value tasks justifying the cost
- Proper data preparation (2-4 hours acceptable for work that would take 2 weeks)
- Clear success metrics before execution

## Quality Assurance
Models now implement advanced features like:
- Garbage data quarantine instead of silent fixes
- Automatic review queues for uncertain outputs
- Reproducible workflows for validation

## Human Role Evolution
Shifts from:
- Constant supervision → Final quality review
- Prompt engineering → Project scoping
- Task execution → Model management

### Practical Guide

# Practical Guide to AI Task Management

## Identifying Fable-Scale Tasks
Look for:
1. Tasks that make you sigh/face-palm when considering them
2. Work everyone knows needs doing but nobody owns
3. Projects requiring weeks of manual effort (e.g., 500-page document review)
4. Data-intensive operations (CRM cleanups, inventory reconciliations)

## Data Preparation Framework
1. **Source Identification**: Map all required data sources (APIs, spreadsheets, documents)
2. **Sanitization**: Remove sensitive data the model shouldn't process
3. **Structuring**: Organize data for model comprehension (e.g., CSV for tabular data)
4. **Metadata**: Include explanatory notes about data conventions

## Success Criteria Definition
For each task, document:
- **Quality Standards**: What "done right" looks like (e.g., "0 typos in final document")
- **Review Process**: How you'll validate outputs (sampling strategy, automated checks)
- **Revision Protocol**: Process for correcting identified issues

## Common Task Archetypes
1. **Mega-Document Processing**: Legal/compliance reviews, consistency checks
2. **Data Reconciliation**: CRM deduplication, financial record alignment
3. **Code Refactoring**: Large-scale architecture changes with style enforcement
4. **Research Synthesis**: Combining multiple sources into executive briefs

## Cost Management
- Estimate token usage using model pricing calculators
- Compare against human labor costs for same task
- Budget for 2-3 revision cycles in cost projections

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[The Doing Got Cheap. Now What? | Claude Fable 5 Changes Work](https://www.youtube.com/watch?v=2w_vwQVvFmc)** by AI News & Strategy Daily | Nate B Jones