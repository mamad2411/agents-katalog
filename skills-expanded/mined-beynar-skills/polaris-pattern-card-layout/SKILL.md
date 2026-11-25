---
name: polaris-pattern-card-layout
description: Master card anatomy & spacing—consistent header, body, footer structure for scan-friendly merchant interfaces
---

# Card Layout

Standardized card layout gives merchants a content structure to rely on.

## Anatomy

Cards consist of three main parts: **header**, **body**, and **footer**. Each part has a specific role and should contain content that serves that role. A standardized structure ensures common elements can be placed consistently.

## Header

Represents the whole card with a **card title** that identifies it and often a **header action** to modify contents or navigate to details.

### Card titles

- Choose a title that clearly conveys the purpose
- Use the object type as card title when the card is a list of objects
- Choose a title to clarify what the header action does
- Choose a title that represents all sections if a card has multiple sections

### Header actions

Actions in the header should represent the entire card content. Most common: "Edit" (modify contents) or "View" (navigate to source).

**Do:**
- Default to tertiary icon buttons in the header with tooltip
- Place actions that affect specific list items on the item itself

**Don't:**
- Place call-to-actions in the card header (put in footer instead)
- Place actions in the header unless they represent the entire card
- Group actions in the header by default

## Body

Holds the main content, organized into **card sections**.

### Card sections

- Group content that shares purpose in a single card with multiple sections
- Don't divide list items across sections—use appropriate list component
- Omit the section title in single-section cards, but maintain the space-200 gap
- Prevent cards from becoming too tall; provide footer action to expand/collapse
- Place section actions in the section header where merchants can associate them

### Form layouts

Form layouts give structure to form elements ("form layout items"), often containing multiple items.

**Do:**
- Use form layout even with a single item
- Arrange items side-by-side using form layout group

**Don't:**
- Allow form layout items wider than necessary
- Allow large empty space next to choice lists

## Footer

Placed after main content—intuitive place for content and actions extending from the card. Example: call-to-actions guiding merchants to their next task.

### Call-to-actions

Specific prompts guiding merchants toward a goal, placed toward the right to inspire progress.

**Do:**
- Default to basic buttons in footer; only use primary button when most important on page
- Use action list if card has more than two call-to-actions

**Don't:**
- Use call-to-actions to update card content (use header actions and list actions instead)
- Use primary button for actions that aren't critical to page purpose

### List actions

Placed to the left in footer—typically actions to add items or expand/collapse lists.

**Do:**
- Allow merchants to expand and collapse long lists
- Choose button label that doesn't repeat object name

## Spacing for merchants

Spacing achieves **grouping** and **hierarchy**. Clear grouping and hierarchy help merchants scan content faster and find what they need.

### Padding

Default card padding is **space-400**. Deeper nested elements use smaller padding.

**Do:**
- Apply padding to card by default; use bleed with negative margin for optical adjustment
- Use padding inside visually scoped containers (e.g., table header)

**Don't:**
- Use padding to create space between elements (use block stacks instead)
- Use padding for invisible containers (use block stacks instead)

### Stacks and gaps

Stacks group content with equal spacing between elements (the gap). Nested stacks apply different gaps to create grouping and hierarchy. Tighter gaps = more related elements.

#### Common stack gaps

- **space-100** (tightest): Group most related elements within form layout items and simple list items
- **space-200**: Separate content blocks inside card sections; space section header from content
- **space-300**: Separate form layout items with variable weight/shape
- **space-400** (loosest): Separate card sections inside cards

## Alignment

Content should be vertically aligned along left and right edges. Optical alignment is more important than technical alignment.
