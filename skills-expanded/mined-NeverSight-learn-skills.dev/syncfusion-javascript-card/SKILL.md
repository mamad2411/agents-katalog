---
name: syncfusion-javascript-card
description: Create flexible, responsive card layouts with headers, images, action buttons, and custom styling. Use when building UI containers for displaying content, product cards, service offerings, or dashboard components. Customize with CSS styling, add headers, images, and action buttons as needed.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion Card Component

The Card is a lightweight, pure CSS layout component for creating flexible content containers. It provides a structured way to organize and display information with support for headers, images, action buttons, and custom styling.

## When to Use This Skill

Use the Syncfusion Card component when you need to:
- Display content in organized, contained sections
- Build product cards, service offerings, or team member profiles
- Create dashboard or portfolio layouts with multiple card elements
- Combine headers, images, and action buttons in a single container
- Apply consistent styling across multiple content sections
- Integrate other Syncfusion components within card containers

## Key Features

- **Pure CSS Component**: No JavaScript dependencies required for basic functionality
- **Flexible Structure**: Support for headers, content, images, and action buttons
- **Multiple Layouts**: Vertical (default) and horizontal alignment options
- **Customizable**: Extensive CSS customization for styling and responsive design
- **Component Integration**: Embed other Syncfusion controls (ListView, DropDownList, etc.) inside cards
- **Accessibility**: Semantic HTML structure with tabindex support

## Component Overview

### Core Structure
```
e-card (root)
├── e-card-header (optional)
│   ├── e-card-header-image (optional)
│   └── e-card-header-caption
│       ├── e-card-header-title
│       └── e-card-sub-title (optional)
├── e-card-image (optional)
│   └── e-card-title (optional caption)
├── e-card-content
├── e-card-separator (optional dividers)
└── e-card-actions (optional)
    ├── e-card-btn (buttons)
    └── anchor elements
```

### Key CSS Classes

| Class | Purpose | Usage |
|-------|---------|-------|
| `e-card` | Root card element | Required |
| `e-card-header` | Header container | Optional |
| `e-card-header-caption` | Title/subtitle wrapper | Groups header text |
| `e-card-header-title` | Main header title | Primary heading |
| `e-card-sub-title` | Subtitle text | Secondary heading |
| `e-card-header-image` | Header image element | Header decoration |
| `e-card-image` | Full-width card image | Featured image |
| `e-card-title` | Image caption/title | Overlay on image |
| `e-card-content` | Main content area | Body text/elements |
| `e-card-separator` | Visual divider | Section separation |
| `e-card-actions` | Action buttons container | Button group |
| `e-card-btn` | Individual button | Actionable element |
| `e-card-vertical` | Vertical alignment | Button layout option |
| `e-card-horizontal` | Horizontal layout | Side-by-side elements |
| `e-card-stacked` | Stacked within horizontal | Vertical section in horizontal |
| `e-card-corner` | Rounded corners | Image styling |

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup with @syncfusion/ej2-layouts
- Basic card markup structure
- CSS imports and theme configuration
- Dependencies and development environment
- First render with minimal example

### Header and Content
📄 **Read:** [references/header-and-content.md](references/header-and-content.md)
- Header structure with title and subtitle
- Adding header images with positioning
- Subtitle support and styling
- Content sections and text areas
- Header-image alignment (before/after)

### Action Buttons
📄 **Read:** [references/action-buttons.md](references/action-buttons.md)
- Action button structure and markup
- Horizontal alignment (default behavior)
- Vertical alignment with e-card-vertical
- Button styling with e-card-btn class
- Mixed buttons and anchor tags

### Card Layouts and Images
📄 **Read:** [references/card-layout.md](references/card-layout.md)
- Full-width card images (e-card-image)
- Image titles and captions with overlay
- Customizing image title position (4 corners)
- Separators and dividers for section separation
- Horizontal card layout (e-card-horizontal)
- Stacked content within horizontal layout

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- CSS customization patterns and best practices
- Element-specific styling (card, header, content, buttons, images)
- Layout customization (margins, padding, spacing)
- Color, font, and typography changes
- Responsive design considerations
- Theme integration and CSS variables

### Component Integration
📄 **Read:** [references/component-integration.md](references/component-integration.md)
- Embedding other Syncfusion components inside cards
- ListView integration for list-based content
- DropDownList and other control integration
- Composite UI layouts and patterns
- To-Do list and advanced examples

---

## Quick Start Example

### Basic Card
```html
<div class="e-card">
    <div class="e-card-content">
        Sample Card Content
    </div>
</div>
```

### Card with Header and Content
```html
<div class="e-card">
    <div class="e-card-header">
        <div class="e-card-header-caption">
            <div class="e-card-header-title">Card Title</div>
        </div>
    </div>
    <div class="e-card-content">
        Card content goes here
    </div>
</div>
```

### Card with Header Image and Actions
```html
<div class="e-card">
    <div class="e-card-header">
        <div class="e-card-header-image"></div>
        <div class="e-card-header-caption">
            <div class="e-card-header-title">Title</div>
            <div class="e-card-sub-title">Subtitle</div>
        </div>
    </div>
    <div class="e-card-content">
        Content here
    </div>
    <div class="e-card-actions">
        <button class="e-card-btn">Button 1</button>
        <button class="e-card-btn">Button 2</button>
    </div>
</div>
```

---

## Common Patterns

### 1. Product Card Pattern
Combine header image, title, description, and action buttons for e-commerce or marketplace interfaces:
```html
<div class="e-card">
    <div class="e-card-image"></div>
    <div class="e-card-header-caption">
        <div class="e-card-header-title">Product Name</div>
        <div class="e-card-sub-title">Price/Category</div>
    </div>
    <div class="e-card-content">Product description</div>
    <div class="e-card-actions">
        <button class="e-card-btn">Add to Cart</button>
        <button class="e-card-btn">Details</button>
    </div>
</div>
```

### 2. Team Member Card Pattern
Display profile information with header image, name, role, and contact buttons:
```html
<div class="e-card">
    <div class="e-card-header">
        <div class="e-card-header-image"></div>
        <div class="e-card-header-caption">
            <div class="e-card-header-title">Name</div>
            <div class="e-card-sub-title">Role/Title</div>
        </div>
    </div>
    <div class="e-card-content">Bio or description</div>
    <div class="e-card-actions">
        <button class="e-card-btn">Email</button>
        <button class="e-card-btn">LinkedIn</button>
    </div>
</div>
```

### 3. Multi-Section Card Pattern
Use separators to divide card into logical sections:
```html
<div class="e-card">
    <div class="e-card-title">Section 1</div>
    <div class="e-card-separator"></div>
    <div class="e-card-content">Content 1</div>
    <div class="e-card-separator"></div>
    <div class="e-card-content">Content 2</div>
</div>
```

### 4. Horizontal Card Pattern
Side-by-side layout with image and stacked content:
```html
<div class="e-card e-card-horizontal">
    <img src="image.png" alt="Sample">
    <div class="e-card-stacked">
        <div class="e-card-header-title">Title</div>
        <div class="e-card-content">Description</div>
        <div class="e-card-actions">
            <button class="e-card-btn">Action</button>
        </div>
    </div>
</div>
```

---

## Common Use Cases

1. **Product Listings**: Build e-commerce product cards with images, names, prices, and purchase buttons
2. **Dashboard Widgets**: Create self-contained card widgets for metrics, charts, and status displays
3. **Team Directories**: Display employee or team member profiles with photos and contact information
4. **Content Cards**: Present articles, blog posts, or news items with featured images and summaries
5. **Service Offerings**: Showcase services with descriptions, icons, and call-to-action buttons
6. **Portfolio Items**: Display project showcases with images, descriptions, and project links
7. **Settings Panels**: Organize configuration or preference options in card-based layouts
8. **Data Cards**: Present structured data with headers, content sections, and action buttons

---

## Installation

The Card component requires the `@syncfusion/ej2-layouts` package. For detailed setup instructions, see **Getting Started** reference.

---

## Next Steps

1. **Start**: Read [Getting Started](references/getting-started.md) for installation and basic setup
2. **Build**: Choose a pattern from Common Patterns section above
3. **Enhance**: Add headers, images, or buttons based on your needs
4. **Style**: Use Customization and Styling guide to match your design
5. **Integrate**: Embed other components if needed using Component Integration guide
