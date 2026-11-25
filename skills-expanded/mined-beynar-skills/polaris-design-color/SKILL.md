---
name: polaris-design-color
description: Master Shopify Polaris color system for semantic meaning, brand recognition, and accessible interfaces. Learn color roles, contrast requirements, semantic signaling, and colorblind-safe palettes.
---

# Color

Color communicates meaning through the Shopify admin and builds merchant understanding through consistent, intentional application.

## Color Assigns Meaning

Color is critical for visual communication. When used consistently, color helps merchants understand the admin intuitively.

**Color meaning in Polaris:**
- **Red** signals danger, errors, or critical issues requiring attention
- **Green** signals success, approval, or positive outcomes
- **Yellow/Amber** signals warnings or caution
- **Blue** indicates primary actions or information
- **Gray** indicates secondary or disabled states
- **Purple** indicates data visualization and premium features

**Benefits of semantic color:**
- Clear, immediate understanding
- Reduced cognitive load
- Faster decision-making
- Consistency across interface
- Accessibility when combined with text

**Do:**
- Use color consistently for meaning
- Apply semantic colors to signals
- Combine color with text labels
- Test for colorblind accessibility

**Don't:**
- Use color arbitrarily
- Change meaning of colors
- Rely on color alone
- Mix semantic meanings

## Color Roles

Polaris defines color roles for specific UI purposes.

### Primary Actions

- Initiate main task or workflow
- Most important action
- High contrast and visibility
- Usually darker/bolder colors

### Secondary Actions

- Support primary actions
- Less critical choices
- Reduced visual weight
- Often lighter or neutral colors

### Success States

- Green indicates positive outcomes
- Completed tasks
- Approved items
- Confirmed actions

### Error/Danger States

- Red for problems requiring action
- Failed validations
- Dangerous operations
- Destructive actions

### Warning/Caution States

- Amber/yellow for caution
- Information needing attention
- Potential issues
- Non-critical alerts

### Neutral/Secondary States

- Gray for disabled or secondary elements
- Placeholder states
- Inactive items
- Supporting information

## Color and Hierarchy

Color supports visual hierarchy.

**Hierarchy principles:**
- Vibrant colors attract attention
- Muted colors recede
- Darker colors emphasize
- Lighter colors reduce emphasis
- Color contrast creates hierarchy

**Do:**
- Use color to emphasize importance
- Muted colors for supporting elements
- Strong colors for primary elements
- Contrast for clarity

**Don't:**
- Over-saturate everything
- Use equally vibrant colors everywhere
- Create competition for attention

## Accessibility and Contrast

Color must be accessible to all merchants, including those with color blindness.

### Contrast Requirements

**WCAG standards:**
- **AA standard:** 4.5:1 for normal text, 3:1 for large text
- **AAA standard:** 7:1 for normal text, 4.5:1 for large text
- Critical for text and interactive elements

**Do:**
- Meet minimum contrast ratios
- Test with contrast checkers
- Provide sufficient color contrast
- Prefer AAA when possible

**Don't:**
- Use light text on light backgrounds
- Create low-contrast combinations
- Skip contrast testing

### Colorblind Accessibility

Not all merchants perceive colors the same way.

**Color blindness types:**
- Deuteranopia (green-red color blindness)
- Protanopia (red color blindness)
- Tritanopia (blue-yellow color blindness)
- Monochromacy (complete color blindness)

**Approach:**
- Never rely on color alone
- Use color + text labels
- Use color + pattern or icon
- Test with colorblind simulators
- Use colorblind-safe palettes

**Do:**
- Include text alternatives
- Use patterns or icons with color
- Test with colorblind tools
- Use accessible color combinations

**Don't:**
- Use red-green combinations alone
- Rely solely on color differentiation
- Skip colorblind testing
- Create confusing color meanings

## Color in Data Visualization

Color has specific meaning in charts and graphs.

**Visualization color principles:**
- Single series: One unified color
- Comparison to past: Current distinct from historical
- Multiseries: Specific sequential palette
- Positive/negative: Green vs. red contrast
- Neutral territory: Gray baseline

**Do:**
- Follow visualization color palettes
- Use consistent colors for same data type
- Consider grayscale printing
- Support colorblind perception

**Don't:**
- Create custom colors for charts
- Mix visualization and UI color rules
- Use inaccessible chart colors

## Color Saturation and Intensity

Manage saturation to prevent eye strain and maintain hierarchy.

**Saturation guidelines:**
- Primary UI: Medium to high saturation
- Secondary elements: Reduced saturation
- Illustrations: Lower saturation (doesn't compete with UI)
- Data visualizations: Specific reduced palettes

**Do:**
- Use full saturation for important elements
- Reduce saturation for supporting content
- Consider merchant eye comfort
- Test readability

**Don't:**
- Over-saturate entire interface
- Tire merchant eyes with high saturation
- Create visual chaos with all vibrant colors

## Brand Color System

Shopify's primary color is green, representing growth, approval, and action.

**Primary brand color:**
- Green for "go" actions
- Represents Shopify identity
- Used in primary buttons
- Signals success and approval

**Secondary colors:**
- Support brand color
- Create visual interest
- Maintain hierarchy
- Ensure accessibility

**Do:**
- Use Shopify green for primary actions
- Maintain brand consistency
- Apply colors from design system
- Update as brand evolves

**Don't:**
- Invent colors outside system
- Over-use brand color
- Create inaccessible combinations

## Best Practices

1. **Consistency:** Use colors consistently across experiences
2. **Meaning:** Every color choice should communicate
3. **Hierarchy:** Color supports visual hierarchy
4. **Accessibility:** Always consider contrast and colorblindness
5. **Restraint:** Use color intentionally, not decoratively
6. **Testing:** Verify colors work for all merchants
7. **Combinations:** Test color pairs for accessibility
8. **Context:** Consider where colors appear
9. **Updates:** Keep color system current
10. **Documentation:** Document color meanings and uses

## Implementation

- Reference Polaris design tokens for exact color values
- Use semantic color naming in code
- Test color contrast before deployment
- Provide color alternatives in data visualization
- Document color meanings for team
- Test with colorblind users
- Update colors with design system releases
