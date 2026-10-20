# Copilot Instructions: Claude Design Automation
Description: A systematic approach to generating brand-aligned design assets (presentations, social media images, websites) in Claude Design with minimal iterations by pre-establishing design systems, templates, and using skills for copy generation.

# Claude Design Automation SOP

## Overview
Claude Design becomes exponentially more effective when you pre-establish:
1. **Design Systems** ([reference](references/design_systems.md))
2. **Templates** ([reference](references/template_creation.md))
3. **Skills** ([reference](references/skill_integration.md))

This creates a 90% complete first draft with minimal iterations.

## Step-by-Step Workflow
1. **Establish Design Foundation**
   - Use the Design System Creator skill
   - Gather existing brand assets
   - Upload to Claude Design System tab

2. **Create Templates**
   - For each use case (slides, social, etc.):
     - Collect 10-15 layout examples
     - Have Claude recreate in HTML
     - Save as template

3. **Build Skills**
   - For each template type:
     - Create a matching skill
     - Train with 5-10 copy examples
     - Connect to template library

4. **Production Flow**
   ```markdown
   1. Invoke appropriate skill
   2. Input: [Content brief/outline]
   3. Skill outputs:
      - Template selection
      - Generated copy
      - Complete Claude Design prompt
   4. Paste prompt into new Claude Design project
   5. Make final tweaks (5-10 min)
   ```

## Code/Prompt Templates
**Design System Setup Prompt**
```
Create comprehensive design system for [Brand Name] including:
1. Color palette (primary/secondary)
2. Typography hierarchy
3. UI components (buttons, cards)
4. Spacing system (8px base)

Reference materials: [attach brand assets]
```

**Template Creation Prompt**
```
Recreate these [number] layout examples in HTML using our design system.
Focus on:
- Responsive structure
- Accessibility
- Brand alignment

Examples: [attach screenshots]
```

## Best Practices
1. **Design Systems**
   - Include dark/light mode variants
   - Document usage rules
   - Store source files externally

2. **Templates**
   - Create variants for A/B testing
   - Organize by use case frequency
   - Include placeholder annotations

3. **Skills**
   - Limit to 3-5 core templates per skill
   - Refresh training data quarterly
   - Validate against design system

## Common Pitfalls
1. **Incomplete Design Systems**
   - Symptom: Inconsistent colors/fonts
   - Fix: Audit with [Design System Checklist](references/design_systems.md)

2. **Overly Broad Templates**
   - Symptom: Constant layout tweaks
   - Fix: Create specialized variants

3. **Skill Drift**
   - Symptom: Off-brand copy
   - Fix: Re-anchor with recent examples

## Validation Steps
1. **Design System**
   - Generate 3 test assets
   - Check for consistency

2. **Templates**
   - Stress test with edge cases
   - Verify mobile responsiveness

3. **Skills**
   - Run 5 sample prompts
   - Check template match rate

## Maintenance Schedule
- Monthly: Review skill outputs
- Quarterly: Update templates
- Biannually: Refresh design system

## Reference Guides

### Design Systems

# Design Systems in Claude Design

A design system is the foundation for consistent brand-aligned outputs in Claude Design. It contains all reusable components, styles, and guidelines that define your brand's visual identity.

## Key Components
1. **Brand Colors**: Primary and secondary color palettes with HEX codes
2. **Typography**: Font families, sizes, and hierarchy (e.g., H1: 32px, Body: 16px)
3. **UI Components**: Buttons, cards, forms with defined states (hover, active)
4. **Assets**: Logos in multiple formats (PNG, SVG), icons, illustrations
5. **Spacing System**: Padding/margin standards (e.g., 8px base unit)

## Implementation Steps
1. Gather existing brand materials (style guides, websites, marketing collateral)
2. Use the Design System Creator skill to automatically extract components
3. Manually verify and supplement any missing elements
4. Upload to Claude via the Design System tab

## Maintenance
- Update seasonally or when rebranding occurs
- Store source files in version control
- Document changes in a changelog.md file

Example structure for a tech company:
```markdown
# Acme Corp Design System
## Colors
- Primary: #3A86FF (Azure)
- Secondary: #8338EC (Purple)
## Typography
- Headings: Inter Bold
- Body: Inter Regular
## Components
- Primary Button: 12px radius, 8px padding
```

### Skill Integration

# Integrating Skills with Claude Design

Skills automate copy generation and template selection, reducing Claude Design iterations.

## Skill Types
1. **Visual Layout Skills**: Match content to templates
2. **Copy Generation Skills**: Maintain brand voice
3. **Asset Production Skills**: Batch create variations

## Implementation Workflow
1. **Setup**:
   - Install Firecrawl/Playwright connectors
   - Load template PDFs/examples
2. **Training**:
   - Provide 5-10 copy examples
   - Define tone guidelines
3. **Execution**:
   - Input: Content brief/outline
   - Output: Structured prompt for Claude Design

## Example Skill Prompt
```
I'm preparing a LinkedIn carousel about our Q3 results. 
Use the Acme Financial Skill with:
- Data: {attach CSV}
- Tone: Professional but approachable
- Template Preference: Stat-heavy layouts
```

## Validation Steps
1. Check copy against brand voice guidelines
2. Verify template appropriateness
3. Test with 3 sample inputs

## Common Issues
- Overly generic copy → Add more examples
- Template mismatch → Adjust skill parameters
- Style drift → Re-anchor to design system

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[How to Actually Use Claude Design Like a Pro (Real Use Cases)](https://www.youtube.com/watch?v=cl5Oudk3Hjo)** by Ben AI

### Template Creation

# Creating Effective Claude Design Templates

Templates pre-establish layouts and structures for repetitive design tasks, eliminating layout iteration time.

## Template Types
1. **Slide Decks**: 20-30 pre-approved slide layouts
2. **Social Media**: Carousel, post, and story formats
3. **Web Pages**: Landing page sections (hero, features, testimonials)
4. **Documents**: One-pagers, reports, proposals

## Creation Process
1. **Research**: Collect 10-15 layout examples from:
   - Dribbble/Behance for inspiration
   - Existing company materials
   - Competitor analysis
2. **Standardize**: Identify 5-7 most used layout patterns
3. **Build in HTML**: Claude recreates layouts using your design system
4. **Test**: Generate 3-5 sample outputs
5. **Save**: Use 'Duplicate as Template' feature

## Best Practices
- Include placeholder text (Lorem ipsum)
- Use clear naming (e.g., 'Feature Comparison - 3 Column')
- Version control templates (v1.0, v1.1)

Example YouTube slide template structure:
```
1. Title Slide (Full bleed image)
2. Section Divider (Gradient bg)
3. Icon + Headline (3 column)
4. Stat Highlight (Large number)
5. Quote Card (Testimonial)
6. Process Flow (5 step)
```

## Maintenance
- Quarterly review for relevance
- Deprecate unused templates
- Create variants for A/B testing