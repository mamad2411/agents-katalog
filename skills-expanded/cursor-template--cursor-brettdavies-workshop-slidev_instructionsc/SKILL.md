---
description: Creating or editing slides, presentations. ALWAYS when using Slidev
globs: 
alwaysApply: false
---
# Use the following instructions for creating new slides

Always start your reply with "LETS DO THIS!"

<think>I need to create a meta-prompt for creating Slidev presentations. This should include what I've learned about structure, components, common issues</think>

From my experience with this project, I've learned:

1. Slidev uses Markdown for slide creation
2. Slides are separated by "---" with new lines
3. Importing slides can sometimes cause issues
4. Two-column layouts use the "::right::" directive
5. Mermaid diagrams need proper styling for visibility
6. Animation with v-click can be replaced with sections
7. Proper file organization helps with maintainability

I should create a prompt that covers:

- Project structure and organization
- Slide content and design principles
- Component usage and customization
- Common pitfalls to avoid
- Technical considerations for Slidev</think># Prompt for Creating Professional Slidev Presentations

## Project Goal

Create a professional slide deck using Slidev that effectively communicates technical content with beautiful visuals, proper structure, and optimal performance.

## Project Structure and Organization

- Begin with a clear outline of the presentation sections and flow before any coding.
- Organize slides in a single `slides.md` file for simplicity rather than splitting into multiple files.
- If using multiple files, use direct Markdown content in the main file for complex slides.
- Follow a logical progression: introduction → problem → solution → implementation → benefits → recap.
- Include a title slide, a table of contents slide, and a thank you slide.

## Slide Design Principles

- Keep content concise – 5-7 bullet points maximum per slide.
- Maintain consistent styling throughout the presentation.
- Use a dark background with light text for technical presentations.
- Implement a two-column layout for slides that compare concepts or show code examples alongside explanations.
- Ensure proper spacing between elements (use padding classes like `class="mt-4"` or `class="p-4"`).
- Design slide transitions that support your narrative flow.

## Content Formatting

- Use headings consistently: `#` for slide titles, `##` for sections, `###` for subsections.
- Apply YAML frontmatter for slide-specific layouts, backgrounds, or transitions.
- When using code blocks, highlight key lines and add proper syntax highlighting.
- For technical presentations, use diagrams to visualize complex concepts.
- Add presenter notes where needed for additional context during live presentations.

## Component Usage

- Create reusable custom components for repeated elements (info boxes, code examples, etc.).
- Use grid layouts with `<div class="grid grid-cols-2 gap-4">` for multi-column content.
- Style components with scoped CSS using the `<style>` tag at the end of slides.
- Implement consistent color schemes across components (store color variables in CSS).

## Mermaid Diagrams

- Use neutral, accessible colors for diagram elements (prefer `#f5f5f5` background with `#333333` borders).
- Ensure sufficient contrast between elements on dark backgrounds.
- Set stroke width to 2px for better visibility.
- Add specific styles for links with `linkStyle` directives.
- Keep diagrams simple – aim for 5-7 nodes maximum for readability.
- Include a brief text explanation below complex diagrams.

## Technical Considerations

- Avoid `v-click` animations for every element; instead group related points in sections.
- Prefer built-in layouts (e.g., `layout: two-cols`) over custom CSS when possible.
- Test your slides frequently during development to catch rendering issues early.
- Optimize images and assets for web delivery.
- Check presentation on different screen sizes to ensure responsiveness.

## Common Pitfalls to Avoid

- Overcrowding slides with too much text or too many elements.
- Using colors that don't provide enough contrast on projectors.
- Creating complex nested structures that might break during rendering.
- Relying on browser-specific features that might not work everywhere.
- Nesting multiple custom components that can lead to rendering issues.
- Using slide separators (`---`) at the end of imported slide files.

## Technical Implementation

- Configure required components in an `index.js` or equivalent file.
- Use UnoCSS or TailwindCSS for styling to maintain consistency.
- Include proper metadata in the frontmatter for SEO and sharing.
- Implement keyboard shortcuts for presenter navigation.
- Ensure code samples are syntax-highlighted correctly for each language.

## Example Slide Structure

```markdown
---
layout: default
---

# Main Slide Title

<div class="grid grid-cols-2 gap-4 mt-4">
<div>

## Left Column Heading
- Key point 1
- Key point 2
- Key point 3

</div>
<div>

## Right Column Heading
```code example or content```

</div>
</div>

<style>
h1 { color: #E06C75; }
h2 { color: #61AFEF; }
</style>
```
