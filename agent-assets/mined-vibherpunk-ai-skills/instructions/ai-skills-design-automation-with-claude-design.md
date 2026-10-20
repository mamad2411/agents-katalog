# Copilot Instructions: Design Automation With Claude Design
Description: A comprehensive skill for automating design workflows using Claude Design, including setting up design systems, templates, and skills to generate brand-aligned assets efficiently.

## Overview
Design automation with Claude Design involves setting up a robust design system, creating reusable templates, and leveraging skills to predefine copy and layouts. This approach minimizes iterations and token usage while ensuring brand consistency across various design assets.

## Core Concepts
Before diving into the workflow, it's essential to understand the core concepts:
- **Design Systems**: A collection of reusable components, guided by clear standards, that can be assembled to build any number of applications.
- **Templates**: Predefined layouts and structures that can be reused across different projects.
- **Skills**: Predefined workflows that automate the generation of copy and selection of templates.

For a deeper dive into these concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Set Up a Design System**
   - Navigate to the design system tab in Claude Design.
   - Create a new design system by adding your company name, description, and examples of existing designs.
   - Use the Design System Creator Skill to automate this process.
   ```markdown
   Can you use the design system creator skill?
   ```
   - Follow the prompts to install necessary connectors and provide your website or design files.

2. **Create Templates**
   - Open a new chat in Claude Design and select your design system.
   - Add examples of layouts or structures you want to reuse.
   - Ask Claude to recreate these in HTML.
   ```markdown
   Recreate these layouts in HTML.
   ```
   - Once satisfied, save the template by clicking 'Share' and 'Duplicate as Template'.

3. **Develop Skills**
   - Use the Design Template Skill Creator to transform your templates into skills.
   ```markdown
   Can you use the design template skill creator?
   ```
   - Provide context and references for the skill to generate appropriate copy and templates.

4. **Generate Design Assets**
   - Invoke the skill with your design brief.
   ```markdown
   I'm preparing a new video, and I need your help on creating the visuals. Use the Benny I visual layout skill.
   ```
   - Paste the generated prompt into Claude Design to get a 90% finished design.

5. **Make Final Adjustments**
   - Use the edit button in Claude Design to tweak text, sizes, and elements.
   ```markdown
   Change the size of this text to 24px.
   ```

For detailed instructions and examples, refer to [Practical Guide](references/practical_guide.md).

## Best Practices and Common Pitfalls
- **Best Practices**:
  - Always pre-establish as much of the design as possible before prompting Claude Design.
  - Use skills to handle copywriting and template selection to save tokens and time.
- **Common Pitfalls**:
  - Avoid 'vibe designing' with one-shot prompts; this leads to endless iterations.
  - Ensure your design system is comprehensive to avoid inconsistencies.

For more on best practices and pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing
- **Validation**:
  - Check that the design system includes all necessary components (colors, fonts, buttons, etc.).
  - Verify that templates are correctly saved and can be reused.
- **Testing**:
  - Generate a sample design asset using the skill and template.
  - Ensure the output aligns with your brand guidelines and requires minimal adjustments.

For code snippets and prompt templates, refer to [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples

## Setting Up a Design System
```markdown
Can you use the design system creator skill?
```

## Creating Templates
```markdown
Recreate these layouts in HTML.
```

## Developing Skills
```markdown
Can you use the design template skill creator?
```

## Generating Design Assets
```markdown
I'm preparing a new video, and I need your help on creating the visuals. Use the Benny I visual layout skill.
```

## Making Final Adjustments
```markdown
Change the size of this text to 24px.
```

For more on best practices and pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

### Common Pitfalls

# Common Pitfalls

## Vibe Designing
One of the most common pitfalls is 'vibe designing,' where users throw in a one-shot prompt without pre-establishing the design. This leads to endless iterations and high token usage without achieving a satisfactory result.

## Incomplete Design Systems
Another common issue is setting up an incomplete design system. Without comprehensive brand guidelines, colors, fonts, and components, the generated designs will lack consistency.

## Overlooking Skills
Many users overlook the importance of skills in automating copywriting and template selection. This results in manual iterations, which are time-consuming and expensive.

For more detailed examples and practical applications, refer to the [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts

## Design Systems
A design system is a collection of reusable components, guided by clear standards, that can be assembled to build any number of applications. It includes everything from brand colors and fonts to buttons and cards. The goal is to ensure consistency across all design assets.

## Templates
Templates are predefined layouts and structures that can be reused across different projects. They save time by eliminating the need to redesign layouts for each new project. Templates can be created for various design assets like slide decks, social media images, and landing pages.

## Skills
Skills are predefined workflows that automate the generation of copy and selection of templates. They help in pre-establishing the design elements before prompting Claude Design, thus reducing iterations and token usage.

For more detailed examples and practical applications, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide

## Setting Up a Design System
1. Navigate to the design system tab in Claude Design.
2. Create a new design system by adding your company name, description, and examples of existing designs.
3. Use the Design System Creator Skill to automate this process.
   ```markdown
   Can you use the design system creator skill?
   ```
4. Follow the prompts to install necessary connectors and provide your website or design files.

## Creating Templates
1. Open a new chat in Claude Design and select your design system.
2. Add examples of layouts or structures you want to reuse.
3. Ask Claude to recreate these in HTML.
   ```markdown
   Recreate these layouts in HTML.
   ```
4. Once satisfied, save the template by clicking 'Share' and 'Duplicate as Template'.

## Developing Skills
1. Use the Design Template Skill Creator to transform your templates into skills.
   ```markdown
   Can you use the design template skill creator?
   ```
2. Provide context and references for the skill to generate appropriate copy and templates.

For more on best practices and pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[How to Actually Use Claude Design Like a Pro (Real Use Cases)](https://www.youtube.com/watch?v=cl5Oudk3Hjo)** by Ben AI