---
name: create-frontend-spec
description: Create comprehensive UI/UX specification documents using interactive YAML-driven workflow. Use when starting new features, planning UI overhauls, or documenting design requirements for frontend development.
---

# Create Frontend Specification

## Purpose

Generate a complete UI/UX specification document through an interactive, section-by-section workflow. This skill uses the front-end specification template to guide you through documenting all aspects of your user interface design.

## When to Use This Skill

Use this skill when you need to:

- **Start a new feature** with UI/UX components
- **Plan a UI overhaul** or redesign
- **Document design requirements** before development
- **Create design handoff documentation** for developers
- **Establish design patterns** for a new project
- **Align stakeholders** on UI/UX direction

**Prerequisites:** Have user research, PRD, or project brief ready (helpful but not required).

## What You'll Create

A comprehensive UI/UX specification document that includes:

### Core Sections
- **Introduction** - Purpose, scope, and overall UX goals
- **Target user personas** and usability goals
- **Design principles** (3-5 guiding principles)
- **Information architecture** - Site maps and navigation structure
- **User flows** - Detailed flow diagrams for critical tasks
- **Wireframes & mockups** - Key screen layouts and references

### Design System
- **Component library** - Core reusable components with variants and states
- **Branding & style guide** - Colors, typography, iconography
- **Spacing & layout** - Grid systems and spacing scales

### Requirements
- **Accessibility** - WCAG compliance targets and testing strategy
- **Responsiveness** - Breakpoints and adaptation patterns
- **Animation** - Motion principles and key micro-interactions
- **Performance** - Design considerations for load times and interactions

### Handoff
- **Next steps** - Actions needed after specification
- **Design handoff checklist** - Validation before development

## How It Works

This skill uses the **`create-doc`** skill with the front-end specification template:

### 1. Template Loading
- Loads `resources/front-end-spec-tmpl.yaml`
- Parses section structure and elicitation requirements
- Sets up interactive workflow

### 2. Interactive Mode (Default)
- **Section-by-section creation** with user collaboration
- **Mandatory elicitation** for critical sections (marked with `elicit: true`)
- **1-9 format interaction:**
  - Option 1: Proceed to next section
  - Options 2-9: Choose elicitation method for deeper exploration
- **Detailed rationale** explaining design decisions and trade-offs

### 3. YOLO Mode (Optional)
- Process all sections at once without elicitation stops
- User can toggle with `#yolo` command
- Faster but less collaborative
- Recommended for experienced users

### 4. Elicitation Methods
When you reach a section marked for elicitation, you'll get options to:
- Expand or contract content for different audiences
- Explain reasoning step-by-step
- Critique and refine from UX perspective
- Identify risks and unforeseen issues
- Explore alternatives through Tree of Thoughts
- Get multi-persona perspectives (PM, Dev, Designer, QA)
- And many more specialized techniques

### 5. Incremental Saving
- Sections saved to file as you complete them
- Document builds progressively
- Can pause and resume work

## Prerequisites & Inputs

### Essential
- **Project name** - What you're building
- **User understanding** - Who will use this interface
- **Key goals** - What users need to accomplish

### Highly Recommended
- **PRD or project brief** - Business context and requirements
- **User research** - Personas, interviews, surveys
- **Existing designs** - Figma/Sketch files or screenshots

### Optional but Helpful
- **Technical constraints** - Platform limitations or requirements
- **Brand guidelines** - Existing company style guide
- **Competitive analysis** - Reference designs

## Output

**File:** `docs/front-end-spec.md` (or custom path)

**Format:** Markdown with:
- Structured sections following template
- Mermaid diagrams for flows and architecture
- Tables for color palettes, typography, breakpoints
- Checklists for handoff validation
- Change log for version tracking

## Example Workflow

1. **Activation:**
   ```
   User: "Create a frontend spec for our mobile account dashboard"
   → create-frontend-spec activates
   → Loads front-end-spec-tmpl.yaml
   ```

2. **Introduction Section:**
   ```
   Claude: "Let's start with the introduction. What's the primary purpose
   of this dashboard?"
   [User provides context]
   Claude: [Drafts introduction with rationale]
   "Select 1 to proceed or 2-9 to explore this section deeper"
   ```

3. **UX Goals & Principles (elicit: true):**
   ```
   Claude: [Drafts user personas, usability goals, design principles]
   Claude: [Provides detailed rationale for choices]
   "Select an option:
   1. Proceed to next section
   2. Expand or Contract for Audience
   3. Explain Reasoning (CoT)
   4. Critique and Refine
   5. Analyze Logical Flow
   6. Identify Potential Risks
   7. Challenge from Critical Perspective
   8. Agile Team Perspective Shift
   9. Stakeholder Round Table

   Select 1-9 or just type your question/feedback:"
   ```

4. **User Selection:**
   - Option 1: Moves to next section
   - Options 2-9: Executes elicitation method, refines content
   - Custom feedback: Discusses and incorporates changes

5. **Continues through all sections:**
   - Information Architecture
   - User Flows (repeatable for multiple flows)
   - Wireframes & Mockups
   - Component Library
   - Branding & Style Guide
   - Accessibility
   - Responsiveness
   - Animation
   - Performance
   - Next Steps

6. **Completion:**
   ```
   Claude: "Frontend specification complete! Saved to docs/front-end-spec.md

   Next steps:
   1. Review with stakeholders
   2. Create/update visual designs in Figma
   3. Run UI/UX validation checklist
   4. Hand off to developers"
   ```

## Best Practices

### Before Starting
- Gather user research and PRD documents
- Review similar products for inspiration
- Clarify technical constraints with development team
- Identify accessibility requirements early

### During Creation
- Be thorough in elicitation sections - they're critical
- Think mobile-first for responsive design
- Consider edge cases and error states
- Document the "why" behind decisions
- Ask questions when uncertain

### After Completion
- Review with stakeholders for alignment
- Validate accessibility requirements
- Run design checklist (use `execute-checklist` skill)
- Update design files to match specification
- Share with development team

## Integration with Other Skills

This skill integrates with:

- **`create-doc`** (called internally) - Executes the YAML-driven document creation
- **`execute-checklist`** (often follows) - Validates the completed specification
- **`generate-ui-prompt`** (often follows) - Creates AI prompts from the spec
- **`ux-expert`** (parent skill) - Orchestrates overall UX workflow

## Key Features

### Mandatory Elicitation
Sections marked `elicit: true` require user interaction:
- Ensures alignment on critical decisions
- Provides 8 elicitation methods for deeper exploration
- Prevents AI from making assumptions on important topics

### Repeatable Sections
Some sections (like User Flows) can be repeated:
- Add multiple user flows
- Document multiple key screens
- Define multiple core components

### Rationale Transparency
Every section includes explanation of:
- **Trade-offs:** What was chosen and why
- **Assumptions:** Key assumptions made
- **Decisions:** Interesting choices needing validation
- **Validation needs:** Areas requiring user confirmation

### Progressive Disclosure
- Load only what's needed when needed
- Template referenced but not loaded until activation
- Elicitation methods loaded on demand
- Efficient token usage

## Success Criteria

A successful frontend specification includes:

✅ Clear user personas and usability goals
✅ Comprehensive information architecture
✅ Detailed user flows with edge cases
✅ Complete component library documentation
✅ Accessibility and responsiveness strategies
✅ Design system with colors, typography, spacing
✅ Performance considerations
✅ Next steps and handoff checklist

## Notes

- This is an **interactive workflow**, not a document generator
- Plan 1-2 hours for thorough specification creation
- Elicitation is required for critical sections - don't skip it
- You can pause and resume work anytime
- Document is saved incrementally as you progress
- YOLO mode available but interactive mode recommended for quality

---

Ready to create a comprehensive frontend specification? Let's document your UI/UX vision!
