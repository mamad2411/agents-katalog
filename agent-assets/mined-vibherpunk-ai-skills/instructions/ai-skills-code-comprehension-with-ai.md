# Copilot Instructions: Code Comprehension With Ai
Description: A systematic approach to using AI for understanding complex codebases, inspired by Priscila Andre de Oliveira's workflow at Sentry. Focuses on comprehension over generation, with structured exploration modes and prompt engineering techniques.

# Code Comprehension with AI Skill

## Overview

This skill transforms how you understand complex codebases by systemizing AI-assisted comprehension. Based on Priscila Andre de Oliveira's experience at Sentry (a 15+ year old codebase with 100 daily PRs), it focuses on structured exploration rather than just code generation. See [Core Concepts](references/core_concepts.md) for philosophical foundations.

## Step-by-Step Workflow

1. **Initialize Context**
   - Provide role, project, and specific needs
   - Example: "I'm a frontend engineer new to the checkout flow"

2. **Select Exploration Mode** (from [Core Concepts](references/core_concepts.md))
   - Architecture for system overview
   - Convention for style/patterns
   - Feature Trace for implementation details
   - History for change context

3. **Formulate Precise Prompt**
   - Use templates from [Prompt Examples](references/prompt_examples.md)
   - Include format preferences (tables, diagrams)

4. **Verify and Cross-Check**
   - Spot-check against actual code
   - Compare multiple AI responses
   - Consult documentation where available

5. **Iterate with Depth**
   - Drill down from architecture to specifics
   - Chain related questions for comprehensive understanding

6. **Document Insights**
   - Save effective prompts
   - Record learned concepts
   - Share with team members

## Best Practices

1. **Prioritize Comprehension**
   - Spend 70% effort understanding, 30% generating (per transcript findings)
   - Never implement without full comprehension

2. **Structure Your Approach**
   - Use the six exploration modes systematically
   - Follow the [Practical Guide](references/practical_guide.md) workflow

3. **Validate Rigorously**
   - Check AI outputs against:
     - Code comments
     - Commit messages
     - Team documentation

## Common Pitfalls

1. **Assuming AI Understands Context**
   - Pitfall: Asking vague questions without boundaries
   - Solution: Provide explicit constraints and examples

2. **Skipping Verification**
   - Pitfall: Trusting AI outputs without spot-checking
   - Solution: Always sample-check against actual code

3. **Generation Over Comprehension**
   - Pitfall: Jumping to code changes without deep understanding
   - Solution: Follow the 70/30 ratio from the transcript

## Validation Steps

1. **Cross-Reference Testing**
   - Ask the same question in different ways
   - Compare responses for consistency

2. **Real-World Verification**
   - Manually verify sample points in code
   - Check against recent PRs/commits

3. **Peer Review**
   - Share AI-generated understanding with teammates
   - Confirm accuracy with domain experts

## Implementation Examples

See [Prompt Examples](references/prompt_examples.md) for ready-to-use templates covering:
- New contributor onboarding
- PR review assistance
- Incident investigation
- Convention verification

## Reference Guides

### Core Concepts

# Core Concepts of AI-Assisted Code Comprehension

## The Comprehension-Generation Paradox

The transcript reveals a surprising insight: 67% of AI usage was for comprehension tasks, while only 2% was for code generation. This challenges the common assumption that AI's primary value is in generating code. Comprehension includes:

- Understanding architecture and dependencies
- Tracing feature implementations
- Learning codebase conventions
- Investigating historical changes

## Exploration Modes Framework

Priscila's 'Catch Me Up' skill structures comprehension into six exploration modes:

1. **Architecture**: High-level system structure and component relationships
2. **Convention**: Codebase-specific patterns and style guidelines
3. **Feature Trace**: How specific features are implemented across the system
4. **Syntax**: Language/framework-specific implementation details
5. **Testing**: Test coverage and validation approaches
6. **History**: Evolution of components and rationale for changes

## Mental Model Alignment

Critical to success is aligning your mental model with the AI's understanding:

- Verify comprehension before acting on AI outputs
- Cross-reference multiple information sources
- Treat AI as a 'senior engineer' who needs context

## Quality Over Speed

In production environments (like Sentry's 15+ year old codebase):

- Never ship code you don't fully understand
- Use AI to accelerate understanding, not bypass it
- Maintain high standards despite faster iteration cycles

### Practical Guide

# Practical Guide to Implementing Code Comprehension Skills

## Creating Your 'Catch Me Up' Skill

1. **Template Structure**: Create a markdown file with:
   - Clear objectives
   - Context about your role
   - Specific exploration modes
   - Formatting preferences (tables, diagrams)

2. **Example Prompt Structure**:
```
I am [your role] working on [codebase/project]. Catch me up on:
1. [Architecture/Convention/Feature Trace/Syntax/Testing/History]
2. Specifically clarify: [your specific question]
3. Present information as: [table/diagram/bullet points]

Additional context: [any relevant background]
```

## Daily Workflow Integration

1. **Onboarding to New Code**:
   - Start with Architecture mode for high-level understanding
   - Then use Feature Trace for your specific work area

2. **PR Review Process**:
   - Use Convention mode to check against codebase standards
   - History mode to understand changes in context

3. **Incident Investigation**:
   - Combine Feature Trace and History modes
   - Ask for timeline of relevant changes

## Tooling Recommendations

- Store frequent prompts as reusable templates
- Maintain a prompt library categorized by exploration mode
- Log successful comprehension sessions for future reference

## Collaboration Practices

- Share effective prompts with team members
- Create team-standard comprehension templates
- Document 'gotchas' and verification steps

### Prompt Examples

# Concrete Prompt Examples and Templates

## Basic Catch Me Up Prompt
```
I am a new contributor to the [repository name] project. Catch me up on how this repository works using these exploration modes:
1. Architecture - Show the high-level components and their relationships
2. Convention - Document the key coding patterns and style rules
3. Feature Trace - Explain how [specific feature] is implemented

Present the information in table format with these columns:
- Component/Concept
- Purpose
- Key Dependencies
- Notable Implementation Details

Specifically clarify: [your burning question about the codebase]
```

## PR Review Assistance Prompt
```
I'm reviewing PR #[number] in [repository]. Help me comprehend:
1. What existing components this change affects (Architecture)
2. Whether it follows our [language/framework] conventions (Convention)
3. How it compares to similar past changes (History)

Identify any:
- Potential breaking changes
- Untested edge cases
- Deviations from established patterns

Format as:
1. Summary of changes
2. Risk assessment
3. Suggested review focus areas
```

## Incident Investigation Prompt
```
We're seeing [error description] in [component]. Help me trace:
1. When this behavior was introduced (History)
2. All code paths that could lead to this state (Feature Trace)
3. Relevant test coverage (Testing)

Create a timeline of:
- Key commits affecting this area
- Past similar incidents
- Recent related changes

Output as markdown with:
- Timeline section
- Code path flowchart description
- Test gap analysis
```

## Convention Verification Prompt
```
I'm modifying [file path]. Verify:
1. Does this follow our [language] conventions?
2. Are there similar patterns elsewhere in the codebase?
3. What exceptions to conventions exist and why?

Compare against:
- Our style guide
- Recent similar changes
- Core framework patterns

Highlight any deviations with:
- Severity (critical/warning/suggestion)
- Justification if intentional
- Suggested alternatives if problematic
```

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[The AI Skill I Rely On Daily — Priscila Andre de Oliveira, Sentry](https://www.youtube.com/watch?v=li0SaBt9RDM)** by AI Engineer