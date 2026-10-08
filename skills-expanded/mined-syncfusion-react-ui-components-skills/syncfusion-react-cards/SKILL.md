---
name: syncfusion-react-cards
description: Build flexible card layouts for displaying content in React. The Card component is a lightweight container that supports headers, images, action buttons, horizontal layouts, and integration with other Syncfusion components. Use this skill whenever the user needs to create cards, build card-based UIs, display content cards, add action buttons to cards, customize card layouts, or embed components within cards.
metadata:
  author: "Syncfusion"
  category: "Layout Components"
  version: "34.1.29"
---

# Implementing React Card Component

The Syncfusion React Card component is a lightweight, flexible container for displaying organized content with support for headers, images, dividers, action buttons, and integrated components.

## When to Use This Skill

Use this skill when you need to:
- Create simple or complex card-based layouts
- Build a card with header, image, and action sections
- Display content in a card with separators or dividers
- Add action buttons (horizontal or vertical) to cards
- Create horizontal card layouts with stacked content
- Embed other Syncfusion components (ListView, Charts, etc.) inside cards
- Customize card appearance with images, titles, and positioning
- Build responsive card-based user interfaces

## Navigation Guide

Follow this guide based on what you're implementing:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and setup
- Basic card structure and CSS imports
- Simple card examples
- Required dependencies

### Card Structure & Headers
📄 **Read:** [references/card-structure-headers.md](references/card-structure-headers.md)
- Card root element and classes
- Header structure with title and subtitle
- Header images and positioning
- Content sections and organization

### Images, Titles & Dividers
📄 **Read:** [references/images-titles-dividers.md](references/images-titles-dividers.md)
- Adding images to cards
- Image titles and overlay effects
- Dividers for section separation
- Title positioning and customization

### Action Buttons
📄 **Read:** [references/action-buttons.md](references/action-buttons.md)
- Adding buttons and links to cards
- Horizontal button layout (default)
- Vertical button alignment
- Icon buttons and styling

### Layouts & Advanced
📄 **Read:** [references/layouts-customization.md](references/layouts-customization.md)
- Horizontal card layout
- Stacked sections within cards
- Image title position classes
- CSS positioning and styling

### Embedding Components
📄 **Read:** [references/embedding-components.md](references/embedding-components.md)
- Integrating ListView with cards
- Embedding charts and data components
- Dynamic content patterns
- Practical use cases

## Quick Start Example

**Basic Card with Header and Content:**

```jsx
import React from 'react';
import '@syncfusion/ej2-layouts/styles/tailwind3.css';

export default function BasicCard() {
  return (
    <div className="e-card">
      <div className="e-card-header">
        <div className="e-card-header-caption">
          <div className="e-card-header-title">Card Title</div>
          <div className="e-card-sub-title">Subtitle</div>
        </div>
      </div>
      <div className="e-card-content">
        This is the main content of the card. Add any HTML content here.
      </div>
    </div>
  );
}
```

**Card with Action Buttons:**

```jsx
import React from 'react';

export default function CardWithButtons() {
  return (
    <div className="e-card">
      <div className="e-card-header-title">Product Card</div>
      <div className="e-card-content">
        High-quality product description goes here.
      </div>
      <div className="e-card-actions">
        <button className="e-card-btn">View</button>
        <button className="e-card-btn">Buy Now</button>
        <button className="e-card-btn">Share</button>
      </div>
    </div>
  );
}
```

**Horizontal Layout Card:**

```jsx
import React from 'react';

export default function HorizontalCard() {
  return (
    <div className="e-card e-card-horizontal" style={{ width: '400px' }}>
      <img src="./image.png" alt="Card" style={{ height: '180px' }} />
      <div className="e-card-stacked">
        <div className="e-card-header">
          <div className="e-card-header-caption">
            <div className="e-card-header-title">Title</div>
          </div>
        </div>
        <div className="e-card-content">
          Content displayed vertically within horizontal layout
        </div>
      </div>
    </div>
  );
}
```

## Common Patterns

### Pattern 1: User Profile Card
Combine header images, titles, and action buttons to create profile cards for user listings or team pages.

```jsx
<div className="e-card">
  <div className="e-card-header">
    <div className="e-card-header-image" style={{ backgroundImage: 'url(./profile.jpg)', width: '60px', height: '60px', borderRadius: '50%' }} />
    <div className="e-card-header-caption">
      <div className="e-card-header-title">John Doe</div>
      <div className="e-card-sub-title">Product Manager</div>
    </div>
  </div>
  <div className="e-card-content">
    Experienced in building user-centric products.
  </div>
  <div className="e-card-actions">
    <button className="e-card-btn">Message</button>
    <button className="e-card-btn">Follow</button>
  </div>
</div>
```

### Pattern 2: Product Card with Image
Use card images and titles for product listings with pricing and action buttons.

```jsx
<div className="e-card">
  <div className="e-card-image" style={{ backgroundImage: 'url(./product.jpg)', height: '200px' }}>
    <div className="e-card-title">Product Name</div>
  </div>
  <div className="e-card-content">
    <p>$99.99</p>
    <p>High-quality product with excellent features</p>
  </div>
  <div className="e-card-actions">
    <button className="e-card-btn">Add to Cart</button>
    <button className="e-card-btn">Buy Now</button>
  </div>
</div>
```

### Pattern 3: Blog Post Card
Combine headers, dividers, and content sections to create blog post cards.

```jsx
<div className="e-card">
  <div className="e-card-header-title">Blog Post Title</div>
  <div className="e-card-sub-title">Published on March 26, 2026</div>
  <div className="e-card-separator" />
  <div className="e-card-content">
    Blog post excerpt and content goes here...
  </div>
  <div className="e-card-actions">
    <button className="e-card-btn">Read More</button>
    <button className="e-card-btn">Share</button>
  </div>
</div>
```

## Key CSS Classes

| Class | Purpose |
|-------|---------|
| `e-card` | Root container for the card |
| `e-card-header` | Header section container |
| `e-card-header-caption` | Wrapper for title and subtitle |
| `e-card-header-title` | Main title text |
| `e-card-sub-title` | Subtitle text |
| `e-card-header-image` | Header image element |
| `e-card-image` | Full-width card image |
| `e-card-title` | Title overlay on image |
| `e-card-content` | Main content section |
| `e-card-actions` | Button container |
| `e-card-btn` | Individual button styling |
| `e-card-vertical` | Vertical button alignment |
| `e-card-separator` | Divider element |
| `e-card-horizontal` | Horizontal card layout |
| `e-card-stacked` | Vertical stack within horizontal |
| `e-card-corner` | Rounded corners on images |

## Essential Setup

1. **Install package:**
   ```bash
   npm install @syncfusion/ej2-layouts
   ```

2. **Import CSS:**
   ```css
   @import '@syncfusion/ej2-layouts/styles/tailwind3.css';
   ```

3. **Create card element:**
   - Add `e-card` class to root div
   - Add header, content, images, or buttons as needed
   - Apply additional classes for layout and styling

## Common Use Cases

- **Dashboard cards**: Display key metrics or data summaries
- **Product listings**: Showcase products with images and prices
- **Team members**: Display user profiles and contact info
- **Blog posts**: Show article previews with meta information
- **Feature highlights**: Present features with descriptions
- **Data reports**: Organize tabular or list data in cards
- **Notification cards**: Display alerts or messages
- **Settings cards**: Group related settings together

---

**Next Steps:** Choose a reference based on your specific need, then implement your card layout following the examples and patterns provided.
