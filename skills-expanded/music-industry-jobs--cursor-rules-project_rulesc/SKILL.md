---
description: 
globs: 
alwaysApply: true
---

# Your rule content

- You can @ files here
- You can use markdown but dont have to
{
  "projectRules": [
    {
      "pattern": ".*",
      "rules": [
        "Follow the structure and instructions outlined in [PRD.md](mdc:PRD.md), [AppFlow.md](mdc:AppFlow.md), and [ImplementationPlan.md](mdc:ImplementationPlan.md).",
        "Use the design system defined in [FrontendGuidelines.md](mdc:FrontendGuidelines.md) when building UI components.",
        "Reference [TechStack.md](mdc:TechStack.md) to ensure consistent library and tool usage.",
        "Always check [BackendStructure.md](mdc:BackendStructure.md) before modifying or creating new database logic."
      ]
    }
  ]
}
