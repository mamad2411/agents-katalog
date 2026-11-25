---
description: Documentation Writing Standards
globs: 
alwaysApply: false
---
# Documentation Writing Standards

## File Organization and Structure

### Content Hierarchy
Documentation follows a skill-based progression in [content/docs/](mdc:tools/docs-web/content/docs):
- `getting-started/` - Installation, first program, overview
- `beginner/` - Variables, functions, control flow, data structures  
- `intermediate/` - Advanced functions, error handling, type system, collections, pattern matching
- `advanced/` - Modules, interfaces, concurrency, performance
- `reference/` - Grammar, keywords, built-in types, standard library
- `tutorials/` - Step-by-step application building guides
- `examples/` - Practical code examples and patterns

### File Naming Conventions
- Use lowercase with hyphens: `variables-and-types.md`
- Section indexes: `_index.md`
- Descriptive names that match navigation

## Hugo Front Matter Standards

Every documentation file must include proper front matter:

```yaml
---
title: "Descriptive Title"
linkTitle: "Short Title"  
weight: 10
description: >
  Brief description for SEO and navigation.
---
```

### Front Matter Guidelines
- `title`: Full descriptive title for the page
- `linkTitle`: Shorter title for navigation menus
- `weight`: Controls ordering (lower numbers appear first)
- `description`: One-sentence summary for SEO and previews

## Content Writing Standards

### Progressive Learning Structure
- **Prerequisites section** - What users should know first
- **Learning objectives** - What users will accomplish
- **Step-by-step progression** - Build concepts incrementally
- **Examples first** - Show code before explaining concepts
- **Practical applications** - Real-world usage patterns

### Code Example Requirements
- Use `ms` language identifier for Manuscript code blocks
- All examples must be syntactically correct per [grammar files](mdc:internal/grammar)
- Examples should be runnable and tested
- Include complete, working examples rather than fragments
- Show both basic and advanced usage patterns

```ms
// Example format
fn main() {
  let message = "Hello, Manuscript!"
  print(message)
}
```

### Writing Style
- **Clear and concise** - Avoid unnecessary complexity
- **Active voice** - "Use `let` to declare variables" not "Variables are declared with `let`"
- **Practical focus** - Emphasize real-world applications
- **Consistent terminology** - Use established language terms
- **Beginner-friendly explanations** - Don't assume prior knowledge

## Cross-Referencing Standards

### Internal Links
- Link to related concepts: `[Error Handling](mdc:../../intermediate/error-handling)`
- Use descriptive link text, not "click here"
- Reference prerequisite knowledge
- Link to examples and tutorials

### Section Previews
Include previews of upcoming concepts:
```ms
// Preview of advanced features
async fn fetchData() User! {
  let user = await api.getUser()
  return user
}
```

## Docsy Theme Features

### Alerts and Callouts
Use Docsy shortcodes for important information:

```
{{% alert title="Note" %}}
Important information that users should know.
{{% /alert %}}

{{% alert title="Warning" color="warning" %}}
Critical information about potential issues.
{{% /alert %}}
```

### Code Block Enhancements
- Include language identifier for syntax highlighting
- Add explanatory comments within code
- Show both input and expected output
- Include error handling examples

## Content Validation Standards

### Technical Accuracy
- Examples must align with [Manuscript.g4](mdc:internal/grammar/Manuscript.g4)
- Code samples should match to tests in tests/compilation
- Syntax must be current and correct
- Error messages should be realistic

### Completeness Requirements
- Cover all major use cases for each feature
- Include edge cases and error conditions  
- Provide troubleshooting information
- Show integration with other features

### Quality Checklist
- [ ] Proper Hugo front matter
- [ ] Working code examples
- [ ] Cross-references to related topics
- [ ] Progressive difficulty
- [ ] Clear learning objectives
- [ ] Proper Markdown formatting
- [ ] Docsy features used appropriately

## Example Templates

### Tutorial Structure
```markdown

Brief introduction explaining what users will build.

## What You'll Learn
- Concept 1
- Concept 2  
- Concept 3

## Prerequisites
- [Link to prerequisite topic](mdc:../prerequisite)

## Step 1: Setup
Detailed setup instructions...

## Step 2: Implementation
Code examples with explanations...

## Next Steps
- [Related tutorial](mdc:../next-tutorial)
- [Advanced concepts](mdc:../../advanced/topic)
```

### Reference Structure
```markdown
# Feature Reference

## Syntax
```ms
// Syntax example
```

## Parameters
- `param1`: Description and type
- `param2`: Description and type

## Examples
```ms
// Working example
```

## Related
- [Related feature](mdc:../related)
```

## Content Sources

### Primary Sources
- [Manuscript.g4](mdc:internal/grammar/Manuscript.g4) - Authoritative syntax
- [ManuscriptLexer.g4](mdc:internal/grammar/ManuscriptLexer.g4) - Token definitions
- [basic.md](mdc:tests/compilation/basic.md) - Working examples

### Content Derivation
- Extract examples from existing tests
- Ensure grammar compliance for all syntax
- Reference real compiler behavior
- Use actual error messages where possible

## Documentation Maintenance

### Regular Updates
- Sync with grammar changes
- Update examples when syntax evolves
- Maintain cross-reference accuracy

### Version Management
- Update version numbers in examples
- Maintain backward compatibility notes
- Document breaking changes clearly
- Provide migration guides when needed
