---
name: documentation
version: 1.0.0
description: Generate and update documentation, READMEs, and API docs from code
uses:
  - synthesis/content-generation
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:read
    - file:write
  requires_approval: false
---

# Documentation

Generate, update, and maintain documentation from code — READMEs, API docs, guides, changelogs, and inline documentation. Good documentation bridges the gap between code and understanding.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `document` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- Creating or updating README files
- Generating API documentation from code
- Writing setup/installation guides
- Documenting architectural decisions
- Creating changelog entries
- Adding inline documentation to complex code
- Writing user guides or tutorials

## Methodology

### 1. Determine Documentation Type

| Type | Purpose | Audience |
|------|---------|----------|
| **README** | Project overview, quick start | New developers, users |
| **API docs** | Endpoint/function reference | Developers integrating |
| **Setup guide** | Installation, configuration | New team members |
| **Architecture doc** | System design, decisions | Maintainers, architects |
| **Changelog** | Version history, changes | Users, developers |
| **Inline docs** | Code-level explanation | Maintainers |
| **Tutorial** | Step-by-step learning | New users |

### 2. Analyze the Source

Read the code/system being documented:
- What does it do? (purpose)
- How is it structured? (architecture)
- What are the key interfaces? (API)
- What are the prerequisites? (dependencies, setup)
- What are the gotchas? (common mistakes, known issues)

### 3. Write for the Audience

Calibrate content to who will read it:
- **New users**: Start with what it does, then how to get started
- **Developers integrating**: Focus on API contracts, examples, error codes
- **Maintainers**: Focus on architecture, decisions, patterns
- **All audiences**: Be concise, use examples, structure with headers

### 4. Structure the Document

Follow established conventions:

**README structure:**
1. Title and one-line description
2. What it does (2-3 sentences)
3. Quick start (minimal steps to get running)
4. Installation (detailed setup)
5. Usage (key features with examples)
6. API reference (if small enough)
7. Contributing
8. License

**API doc structure (per endpoint/function):**
1. Description
2. Parameters (name, type, required, description)
3. Return value
4. Errors
5. Example

### 5. Include Examples

Every piece of documentation should include:
- **Working examples**: Code that can be copied and run
- **Expected output**: What the example produces
- **Edge cases**: Examples of error handling

### 6. Verify Accuracy

Documentation must match the current code:
- Run examples to confirm they work
- Check parameter names and types against the implementation
- Verify setup steps produce a working environment
- Cross-reference with tests (tests are executable documentation)

## Output Format

```
## Documentation: [Target]

### Type
- Document type: [README/API/guide/changelog/inline]
- Audience: [who will read this]

### Source Analysis
- Files read: [list]
- Key interfaces: [list]
- Prerequisites: [list]

### Document Created/Updated
- Path: [file path]
- Sections: [list of sections]
- Examples: [count]

### Verification
- Examples tested: [yes/no]
- Matches code: [yes/no]
- Reviewed for accuracy: [yes/no]
```

## Quality Criteria

- Documentation is accurate (matches the current code)
- Documentation is complete (covers all public interfaces)
- Documentation is concise (no unnecessary verbosity)
- Examples are working and can be copied directly
- Structure follows conventions for the document type
- Audience is considered (appropriate detail level)
- Prerequisites and setup steps are explicit
- Common mistakes and gotchas are documented

## Common Mistakes

- **Documenting the obvious**: Comments like `# increment counter` on `counter += 1` add noise, not value. Document WHY, not WHAT.
- **Stale documentation**: Updating code without updating docs. Documentation that's wrong is worse than no documentation.
- **No examples**: API reference without examples forces the reader to guess how to use it. Every function/endpoint needs at least one example.
- **Assuming knowledge**: Not listing prerequisites, assuming the reader knows the setup steps or background context. Be explicit.
- **Wall of text**: Long paragraphs without structure, headers, or formatting. Use headers, lists, tables, and code blocks.
- **Documenting implementation details**: Public documentation should describe behavior and interfaces, not internal implementation. Internal docs go in code comments.
- **Not testing examples**: Including code examples that don't actually work. Always run examples before publishing.

## Completion

Documentation is complete when:
- Document type and audience are identified
- Source code is analyzed for accurate information
- Document is written with proper structure and examples
- Examples are verified to work
- Documentation matches the current code
- Document is in the correct location and format
