---
description: 
globs: .cursor/rules/*.mdc
alwaysApply: false
---
Description: Declares how .mdc files are structured and prioritized across the project.

# .mdc File Structure Guide
- File naming: NNN-name.mdc (NNN = 001–299)
  - 001–099: Core/project-wide rules
  - 100–199: Workflow and integration rules
  - 200–299: Pattern and style rules
  - 300–399: Technology-specific rules (frameworks, libraries, tools)
- Higher NNN takes precedence when Globs overlap
- Each rule should target a single logical purpose (SRP)
- Use Cursor GUI to assign Rule Type: Always, Auto, Manual, AgentRequested
- Keep body concise: ideally under 25 lines
