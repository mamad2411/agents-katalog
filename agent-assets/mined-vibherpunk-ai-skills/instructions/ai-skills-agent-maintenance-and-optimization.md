# Copilot Instructions: Agent Maintenance And Optimization
Description: A systematic approach to maintaining and optimizing AI agents by focusing on harness (workbench) design, tool pruning, and continuous adaptation to model improvements and workflow changes.

# Agent Maintenance and Optimization Skill

## Overview

This skill teaches you to maintain and optimize AI agents by focusing on their "harness" - the controlled environment that governs their capabilities and constraints. Based on real-world examples like Vercel's agent optimization, you'll learn to:

- Systematically prune unnecessary tools ([Core Concepts](references/core_concepts.md))
- Adapt the harness to model improvements
- Keep the agent aligned with evolving workflows
- Implement rigorous validation processes

## Step-by-Step Workflow

1. **Document Current State**
   - Inventory all tools, permissions, and data sources
   - Record baseline performance metrics
   - Map current workflow touchpoints

2. **Conduct Five Critical Checks** ([Practical Guide](references/practical_guide.md))
   1. Source validity
   2. Permission appropriateness
   3. Job scope alignment
   4. Proof requirements
   5. Business value

3. **Implement Pruning**
   - Use the [decision framework](references/code_examples.md) to evaluate each tool
   - Remove non-essential elements in batches
   - Monitor impact for 1-2 weeks

4. **Update Harness Configuration**
   - Adjust permissions based on model capabilities
   - Refresh stale data sources
   - Modify proof requirements as needed

5. **Establish Maintenance Rhythm**
   - Weekly quick checks
   - Monthly deep reviews
   - Quarterly redesign sessions
   - Immediate updates after model changes

## Best Practices

- **Start Small**: Begin with minimal tools and add cautiously
- **Prove Value**: Every tool should justify its maintenance overhead
- **Document Changes**: Maintain a [change log](references/code_examples.md) for all harness modifications
- **Human Oversight**: Keep review steps even as the model improves

## Common Pitfalls

- **Tool Accumulation**: Adding features without removing obsolete ones
- **Stale Constraints**: Keeping limitations designed for weaker models
- **Silent Drift**: Allowing the agent's role to change without explicit approval
- **Overautomation**: Removing human checks prematurely

## Validation Steps

1. **Regression Testing**
   - Verify core functionality after each change
   - Check error rates on key tasks

2. **Value Assessment**
   - Measure time saved versus maintenance cost
   - Survey end-users on output quality

3. **Stress Testing**
   - Evaluate performance on edge cases
   - Verify fail-safes trigger appropriately

4. **Model Impact Analysis**
   - Assess how model updates affect existing constraints
   - Test whether old protections now limit potential

## Implementation Notes

- Use the [configuration template](references/code_examples.md) to standardize harness setups
- Schedule pruning sessions quarterly at minimum
- Treat the harness as a living system, not a one-time setup
- Balance model capabilities with business risk tolerance

## Reference Guides

### Code Examples

# Code and Prompt Examples

## Harness Configuration Template

```python
class AgentHarness:
    def __init__(self):
        # Data Sources
        self.allowed_sources = [
            'crm/current_customers',
            'knowledge_base/v2',
            'support_tickets/last_90_days'
        ]
        
        # Permissions
        self.permissions = {
            'read': True,
            'write': False,
            'execute': ['search', 'draft_responses'],
            'create_records': False
        }
        
        # Proof Requirements
        self.proof_standards = {
            'claims': 'require_source',
            'recommendations': 'show_alternatives',
            'drafts': 'mark_placeholders'
        }
        
        # Human Review Triggers
        self.review_rules = [
            {'condition': 'dollar_value > 1000', 'action': 'require_approval'},
            {'condition': 'new_company', 'action': 'flag_for_review'}
        ]
```

## Pruning Decision Prompt

```
You are an AI agent optimizer. Evaluate whether to keep or remove the following tool:

Tool: {tool_name}
Current Usage: {usage_frequency}
Error Rate: {error_percentage}
Dependencies: {dependent_processes}

Consider:
1. Is this tool absolutely essential to core functionality?
2. Has usage declined significantly over the past quarter?
3. Does it create more errors/overhead than value?
4. Are there newer tools that make this obsolete?

Format your response as:
Decision: keep/remove
Reason: [1-2 sentences]
Impact: [expected effect on performance]
```

## Source Validation Check

```python
def validate_sources(sources):
    """Check if configured sources are still valid"""
    invalid = []
    for source in sources:
        if not source.exists():
            invalid.append(f"Missing: {source}")
        elif source.last_updated < (datetime.now() - timedelta(days=90)):
            invalid.append(f"Stale: {source} (last updated {source.last_updated})")
        elif source.deprecation_notice:
            invalid.append(f"Deprecated: {source}")
    
    if invalid:
        raise ConfigurationError(
            f"{len(invalid)} invalid sources detected:\n" +
            "\n".join(invalid)
        )
```

## Change Log Template

```markdown
## Harness Update {date}

### Changes Made
- Removed: {tools_removed}
- Added: {tools_added}
- Modified: {config_changes}

### Reason
{justification}

### Expected Impact
{performance_prediction}

### Verification Plan
1. {test_case_1}
2. {test_case_2}
3. {test_case_3}
```

### Core Concepts

# Core Concepts of Agent Maintenance

## The Harness (Workbench) Concept

The harness is the controlled environment surrounding your AI agent that defines:
- What data sources it can access
- What tools it can use
- What actions it's permitted to take
- What proof requirements exist for its outputs
- What human review steps are required

Unlike traditional software, agents require maintenance in two directions:
1. **Model Evolution**: As the underlying AI model improves, the harness must adapt to leverage new capabilities while maintaining appropriate constraints.
2. **Workflow Drift**: As business processes change, the agent's sources, tools, and permissions must stay synchronized with current reality.

## The Pruning Principle

Counterintuitively, agents often improve when tools are removed rather than added. Vercel's case study showed an 80% reduction in tools led to better performance by:
- Reducing cognitive load on the agent
- Minimizing potential failure points
- Focusing the agent on core competencies

## Maintenance Cycles

Effective agent maintenance requires regular checks of:
1. **Input Sources**: Are the documents, databases, and context still accurate and relevant?
2. **Permission Scope**: Does the agent's access level match its current reliability?
3. **Output Validation**: Are proof requirements rigorous enough for the agent's growing capabilities?
4. **Value Assessment**: Is the agent's output actually being used and improving workflows?

## The Sailboat Analogy

Agents are more like sailboats than traditional software - they exist in dynamic environments where:
- Salt (data drift) corrodes components
- Lines (prompts) loosen over time
- Weather (business conditions) changes constantly

This requires ongoing maintenance rather than one-time deployment.

### Practical Guide

# Practical Guide to Agent Maintenance

## Step 1: Establish Baseline Metrics

Before making changes, document:
- Current toolset and permissions
- Key performance indicators (response time, accuracy, etc.)
- Human review workload
- Error rates by task type

## Step 2: Implement the Five Checks

1. **Source Audit**:
   - List all data sources the agent uses
   - Verify each is still authoritative
   - Identify new sources that should be added
   - Flag deprecated sources for removal

2. **Permission Review**:
   - Catalog all access rights (read, write, execute)
   - Assess if each is still appropriate for current model capabilities
   - Implement least-privilege principles

3. **Job Description Validation**:
   - Compare current agent outputs to original design
   - Identify capability creep or underutilization
   - Explicitly document allowed and prohibited actions

4. **Proof Requirements**:
   - Ensure every factual claim requires sourcing
   - Implement traceability for all recommendations
   - Standardize evidence presentation formats

5. **Value Assessment**:
   - Track actual usage of agent outputs
   - Measure time saved versus time spent reviewing
   - Identify redundant or low-value outputs

## Maintenance Schedule

- **Weekly**: Quick source validity checks
- **Monthly**: Full permission and job scope review
- **Quarterly**: Comprehensive harness redesign session
- **After Model Updates**: Immediate impact assessment

## Pruning Methodology

1. List all tools/integrations
2. For each, ask:
   - Is this absolutely essential to core functionality?
   - Has usage declined over time?
   - Does it create more errors than value?
3. Remove anything not passing all three questions
4. Monitor performance for 1-2 weeks
5. Reintroduce tools only if clear regression appears

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Don't build more AI agents until you watch this](https://www.youtube.com/watch?v=BOXK2XFLA-E)** by AI News & Strategy Daily | Nate B Jones