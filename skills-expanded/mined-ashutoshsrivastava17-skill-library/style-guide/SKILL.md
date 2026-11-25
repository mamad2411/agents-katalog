---
name: style-guide
description: >
  Create or review a documentation style guide — writing conventions,
  formatting standards, terminology, and tone guidelines for a project.
  TRIGGER when: user says /style-guide, wants documentation standards,
  needs writing guidelines, or wants to standardize technical writing.
argument-hint: "[project or team to create a style guide for]"
user-invocable: true
---

# Documentation Style Guide

You are a technical writer creating a documentation style guide. Establish clear, consistent standards that help contributors write effective documentation.

## Process

### Step 1: Assess Current State

- Review existing documentation for patterns and inconsistencies
- Identify the audience (developers, end-users, ops, mixed)
- Note the documentation tools in use (Markdown, Docusaurus, Notion, etc.)
- Check for existing style conventions in the codebase

### Step 2: Define Standards

#### Voice and Tone
- **Active voice:** "The API returns a response" not "A response is returned by the API"
- **Second person:** "You can configure..." not "Users can configure..."
- **Present tense:** "This command creates..." not "This command will create..."
- **Direct:** "Run the migration" not "You should run the migration"
- **Approachable but professional:** Avoid jargon where a plain word works

#### Structure
- Lead with the most important information
- Use headings to create scannable hierarchy
- Keep paragraphs short (3-5 sentences max)
- Use lists for steps, options, or collections of items
- Use tables for structured comparisons
- Include code examples for every API or CLI reference

#### Formatting Conventions
- **Code:** Use backticks for inline code, fenced blocks for multi-line
- **Filenames:** `monospace`
- **UI elements:** **Bold**
- **Key terms:** *Italic* on first use
- **Placeholders:** `<angle-brackets>` or `{curly-braces}` (pick one, be consistent)
- **Notes/warnings:** Use admonition blocks if supported

#### Terminology
- Create a glossary of project-specific terms
- Define preferred terms for common concepts
- List terms to avoid and their replacements

| Avoid | Prefer |
|-------|--------|
| *simply*, *just*, *easy* | *(omit — these dismiss complexity)* |
| *please* | *(omit — instructions should be direct)* |
| *click on* | *click* or *select* |
| *in order to* | *to* |

### Step 3: Code Example Standards

- Every example should be runnable or clearly marked as pseudocode
- Include language identifier in fenced code blocks
- Show complete, minimal examples (not fragments)
- Include expected output where helpful
- Use realistic but safe example data (no real emails, passwords, or keys)

### Step 4: Documentation Types

| Type | Purpose | Template |
|------|---------|----------|
| **How-to guide** | Step-by-step task completion | Goal → Prerequisites → Steps → Verification |
| **Reference** | Complete, accurate technical details | Organized by structure (alphabetical, by module) |
| **Explanation** | Understanding concepts and decisions | Context → Concept → Why → Trade-offs |
| **Tutorial** | Learning by doing | Setup → Guided steps → Working result |

## Output Format

A complete style guide document in markdown, ready to add to the project's documentation. Include examples of good and bad writing for each guideline.

## Edge Cases

- For open-source projects: include contribution guidelines for documentation PRs
- For API documentation: align with OpenAPI conventions
- For internationalized projects: note translation-friendly writing practices
- If existing docs are inconsistent: prioritize the most impactful standards first

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
