---
name: "syncfusion-aspnetcore-cards"
description: "Complete guide to implementing Syncfusion ASP.NET Core Card component with layout structures, headers, images, actions, and advanced customization. Use this skill when building card-based layouts, displaying content with headers and images, creating action buttons, or organizing responsive card designs."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion ASP.NET Core Card Component

The Card component is a flexible layout container for displaying content with headers, images, actions, and more. It's perfect for creating product showcases, content summaries, user profiles, and dashboard widgets with a clean, modern appearance.

## When to Use This Skill

Use the Card component when you need to:
- **Display organized content** — Group related information (titles, images, text, actions) in a visually cohesive container
- **Create dashboard widgets** — Build reusable card layouts for dashboard panels and content cards
- **Showcase products or items** — Present product images, descriptions, and action buttons in a structured format
- **Build responsive layouts** — Enable horizontal/vertical stacking with responsive design
- **Add interactive elements** — Include buttons, links, images, and other components within the card
- **Implement modern UI patterns** — Follow Material Design and modern card-based interfaces

## Component Overview

The Syncfusion ASP.NET Core Card (`e-card` class) provides:
- **Flexible structure** — Headers, content, images, action buttons in any combination
- **Layout options** — Vertical (default), horizontal, or stacked layouts
- **Rich content support** — Text, images, headers with titles/subtitles, dividers
- **Action buttons** — Horizontal or vertical button alignment for user interactions
- **Responsive design** — Adapts to different screen sizes and containers
- **Easy customization** — CSS classes for styling and positioning

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- ASP.NET Core project setup and prerequisites
- Adding Syncfusion stylesheets and scripts
- Creating your first basic card
- Running the application and viewing results

### Header and Content
📄 **Read:** [references/header-and-content.md](references/header-and-content.md)
- Header structure with titles and subtitles
- Adding header images with alignment options
- Content areas for text and HTML elements
- Complete examples with proper element structure

### Images and Dividers
📄 **Read:** [references/images-and-dividers.md](references/images-and-dividers.md)
- Including full-width images in cards
- Adding image titles and captions with overlays
- Using dividers to separate content sections
- Multiple images and advanced image layouts

### Action Buttons
📄 **Read:** [references/action-buttons.md](references/action-buttons.md)
- Creating action button containers
- Horizontal vs vertical button alignment
- Button styling with e-card-btn class
- Using buttons and anchor tags as actions

### Horizontal and Stacked Layouts
📄 **Read:** [references/horizontal-layout.md](references/horizontal-layout.md)
- Creating horizontal card layouts with e-card-horizontal
- Mixing horizontal and vertical with e-card-stacked
- Content positioning in multi-column designs
- Responsive considerations for horizontal layouts

### Advanced Customization
📄 **Read:** [references/advanced-customization.md](references/advanced-customization.md)
- Customizing image title positioning with CSS
- Integrating other Syncfusion components inside cards
- Styling and theming options
- Real-world integration examples (ListViews, forms, etc.)

## Quick Start Example

Basic card with header and content:

```html
<div class="e-card">
    <div class="e-card-header">
        <p><strong>Card Title</strong></p>
        <p>Subtitle or description</p>
    </div>
    <div class="e-card-content">
        Your content goes here
    </div>
</div>
```

## Common Patterns

### Pattern 1: Card with Image and Header
```
Header (title/subtitle) + Image + Content + Actions
```
Use for product cards, profile cards, blog post previews.

### Pattern 2: Horizontal Image + Content
```
Image (left) | Header + Content + Actions (right)
```
Use for horizontal layouts, list items, media cards.

### Pattern 3: Image with Title Overlay
```
Image + Title (overlay at bottom) + Actions
```
Use for gallery cards, featured content, visual showcases.

### Pattern 4: Content-Only Card
```
Header + Content + Divider + Actions
```
Use for simple information cards, summary cards, action items.

## Key CSS Classes

| Class | Purpose |
|-------|---------|
| `e-card` | Root card container |
| `e-card-header` | Header wrapper element |

| `e-card-content` | Content area |
| `e-card-image` | Full-width card image |
| `e-card-title` | Image overlay title |
| `e-card-actions` | Action button container |
| `e-card-btn` | Action button styling |
| `e-card-separator` | Divider between sections |
| `e-card-horizontal` | Horizontal layout |
| `e-card-stacked` | Vertical section in horizontal layout |
| `e-card-vertical` | Vertical action button alignment |
| `e-card-corner` | Rounded corners on images |

## Before You Begin

Ensure your ASP.NET Core project has:
- Syncfusion NuGet packages installed
- TagHelpers registered in `_ViewImports.cshtml`
- Syncfusion CSS stylesheets referenced in `_Layout.cshtml`
- Required JavaScript files included

For a complete setup walkthrough, see [Getting Started](references/getting-started.md).
