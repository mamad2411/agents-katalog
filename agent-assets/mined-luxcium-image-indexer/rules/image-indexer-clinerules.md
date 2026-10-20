# Cline AI Learning Journal

## Purpose

The .clinerules file acts as a learning journal that captures essential information, user preferences, and recurring patterns observed during the project.

## Content to Capture

- Critical implementation pathways.
- User workflow preferences.
- Project-specific patterns.
- Identified challenges and evolving decisions.
- Effectiveness and usage of tools.

## Learning Process

```mermaid
flowchart TD
    Start{Discover New Pattern}
    
    subgraph Learn [Learning Process]
        D1[Identify Pattern]
        D2[Validate with User]
        D3[Document in .clinerules]
    end
    
    subgraph Apply [Application]
        A1[Read .clinerules]
        A2[Apply Learned Patterns]
        A3[Enhance Future Work]
    end
    
    Start --> Learn
    Learn --> Apply
```

## Update Procedures

- **When to Update:**  
  - Discovery of new project patterns.
  - Implementation of significant changes.
  - Explicit user command **update memory bank** (which requires a COMPLETE review of all files).
  - When contextual clarification is needed.
  
```mermaid
flowchart TD
    Start[Update Process]
    
    subgraph Process
        P1[Review ALL Memory Bank Files]
        P2[Document Current State]
        P3[Clarify Next Steps]
        P4[Update .clinerules]
        
        P1 --> P2 --> P3 --> P4
    end
    
    Start --> Process
```

## Compliance with Markdownlint Standards

All generated documentation and internal files must adhere to the following Markdownlint rules:
- **Heading Levels:** Ensure headings increment by one level at a time (MD001).
- **Spacing:** Maintain correct spacing around headings (MD022) and consistent list indentation (MD007). Avoid trailing spaces (MD009) and multiple consecutive blank lines (MD012).
- **Code Blocks:** Fenced code blocks must specify the language (MD040, MD048) and follow a consistent style.
- **Emphasis and Links:** Ensure consistent use of emphasis styles (MD049) and correct link formatting.

## MCP Servers Integration

- Maintain a record of which MCP servers are available for the project, including the decisions to use or not use specific servers (e.g., task management or repository integration servers).
- Document the rationale in the Memory Bank and .clinerules for transparency and future reference.

## Final Directive

Cline AI must self-document every action and decision based on the integrated documentation above. Prior to any task:
- **Read all Memory Bank files and ensure complete context.**
- **Perform thorough workspace diagnostics before and after every tool usage.** This includes validating all issues (denoted by `@problems`) and ensuring no new errors or warnings are introduced.
- **Adhere strictly to all Markdownlint rules in all communications and document outputs.**
- **Continuously update the .clinerules and .clineinstructions files to capture new patterns, user preferences, and any changes in the operational procedures.**

This integrated approach ensures that Cline AI remains self-aware, resilient, and aligned with user directives—guaranteeing perfect continuity despite memory resets and maintaining high project quality.

## Content to Capture
- Critical implementation pathways.
- User workflow preferences.
- Project-specific patterns.
- Identified challenges and evolving decisions.
- Effectiveness and usage of tools.

## Learning Process
```mermaid
flowchart TD
    Start{Discover New Pattern}
    
    subgraph Learn [Learning Process]
        D1[Identify Pattern]
        D2[Validate with User]
        D3[Document in .clinerules]
    end
    
    subgraph Apply [Application]
        A1[Read .clinerules]
        A2[Apply Learned Patterns]
        A3[Enhance Future Work]
    end
    
    Start --> Learn
    Learn --> Apply
```

## Update Procedures
- **When to Update:**  
  - Discovery of new project patterns.
  - Implementation of significant changes.
  - Explicit user command **update memory bank** (which requires a COMPLETE review of all files).
  - When contextual clarification is needed.
  
```mermaid
flowchart TD
    Start[Update Process]
    
    subgraph Process
        P1[Review ALL Memory Bank Files]
        P2[Document Current State]
        P3[Clarify Next Steps]
        P4[Update .clinerules]
        
        P1 --> P2 --> P3 --> P4
    end
    
    Start --> Process
```

## Compliance with Markdownlint Standards
All generated documentation and internal files must adhere to the following Markdownlint rules:
- **Heading Levels:** Ensure headings increment by one level at a time (MD001).
- **Spacing:** Maintain correct spacing around headings (MD022) and consistent list indentation (MD007). Avoid trailing spaces (MD009) and multiple consecutive blank lines (MD012).
- **Code Blocks:** Fenced code blocks must specify the language (MD040, MD048) and follow a consistent style.
- **Emphasis and Links:** Ensure consistent use of emphasis styles (MD049) and correct link formatting.

## MCP Servers Integration
- Maintain a record of which MCP servers are available for the project, including the decisions to use or not use specific servers (e.g., task management or repository integration servers).
- Document the rationale in the Memory Bank and .clinerules for transparency and future reference.

## Final Directive
Cline AI must self-document every action and decision based on the integrated documentation above. Prior to any task:
- **Read all Memory Bank files and ensure complete context.**
- **Perform thorough workspace diagnostics before and after every tool usage.**
- **Adhere strictly to all Markdownlint rules in all communications and document outputs.**
- **Continuously update the .clinerules and .clineinstructions files to capture new patterns, user preferences, and any changes in the operational procedures.**

This integrated approach ensures that Cline AI remains self-aware, resilient, and aligned with user directives—guaranteeing perfect continuity despite memory resets and maintaining high project quality.
