---
name: syncfusion-angular-card
description: Implements Syncfusion Angular Card components with headers, images, action buttons, and configurable layouts. Use this skill when building flexible, reusable card interfaces with custom styling, CSS classes, and component integration patterns for displaying content in structured card formats.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion Angular Cards

The Card is a lightweight, CSS-based layout component that provides a flexible container for displaying structured content. Perfect for creating reusable content blocks with headers, images, text, and interactive elements.

## When to Use This Skill

Use this skill when users need to:
- Create card-based layouts with structured content
- Add headers with titles, subtitles, and images to cards
- Include images and captions within cards
- Add interactive action buttons to cards
- Arrange card elements horizontally
- Customize card appearance with CSS
- Build flexible, responsive content containers
- Integrate other Syncfusion components within cards

## Component Overview

The Syncfusion Angular Card (`e-card`) is a pure CSS component with no JavaScript dependencies. It provides semantic HTML structure and CSS classes that enable you to build professional card layouts with:

- **Flexible Structure:** Pure CSS composition with no complex dependencies
- **Semantic Elements:** Clear class-based architecture for headers, content, and actions
- **Responsive Design:** Works with CSS grid, flexbox, and responsive layouts
- **Component Integration:** Host other Syncfusion components inside cards
- **Extensive Customization:** Full CSS control over appearance and behavior

**Key CSS Classes:**
- `e-card` — Root card container
- `e-card-header` — Header section wrapper
- `e-card-content` — Main content area
- `e-card-image` — Image container
- `e-card-actions` — Action buttons container
- `e-card-horizontal` — Horizontal layout mode
- `e-card-separator` — Visual divider between sections

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and setup
- Angular CLI and environment configuration
- Adding CSS theme imports
- Basic card structure with headers and content
- Your first working card example

### Card Headers
📄 **Read:** [references/card-headers.md](references/card-headers.md)
- Header structure and wrapper elements
- Adding titles and subtitles
- Including images in headers
- Image positioning (before/after caption)
- Rounded corners and image styling
- Complete header examples

### Card Images
📄 **Read:** [references/card-images.md](references/card-images.md)
- Adding images to card content
- Image sizing and dimensions
- Image titles and captions with overlay
- Dividers for visual separation
- Integrating other components inside cards
- Complete image examples

### Action Buttons
📄 **Read:** [references/action-buttons.md](references/action-buttons.md)
- Creating action buttons and links
- Horizontal button alignment (default)
- Vertical button alignment
- Icon buttons and custom styling
- Interactive card controls
- Button examples with layouts

### Horizontal Layout
📄 **Read:** [references/horizontal-layout.md](references/horizontal-layout.md)
- Side-by-side element alignment
- Using the `e-card-horizontal` class
- Stacked sections with `e-card-stacked`
- Mixed horizontal and vertical layouts
- Combining images with vertical content
- Horizontal layout examples

### Styling and Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS structure and class selectors
- Customizing card appearance
- Header, content, and button styling
- Image and divider customization
- Theme integration
- Advanced CSS patterns

---

## Quick Start Example

Here's a minimal working card with header, content, and action buttons:

```html
<!-- In your app.component.html or template -->
<div class="e-card" style="max-width: 400px;">
  <!-- Header Section -->
  <div class="e-card-header">
    <div class="e-card-header-caption">
      <div class="e-card-header-title">Card Title</div>
      <div class="e-card-sub-title">Subtitle or description</div>
    </div>
  </div>

  <!-- Content Section -->
  <div class="e-card-content">
    Your main content goes here. This can be text, images, or any HTML elements.
  </div>

  <!-- Action Buttons Section -->
  <div class="e-card-actions">
    <button class="e-card-btn">Action 1</button>
    <button class="e-card-btn">Action 2</button>
  </div>
</div>
```

**Setup in Component:**

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true
})
export class AppComponent {}
```

**Add CSS Theme to styles.css:**

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-layouts/styles/material3.css';
```

---

## Common Patterns

### Pattern 1: Product Card with Image
Display a product with image, title, description, and action buttons:

```html
<div class="e-card" style="max-width: 300px;">
  <div class="e-card-image" style="background-image: url('product.jpg'); height: 200px;"></div>
  <div class="e-card-header">
    <div class="e-card-header-title">Product Name</div>
  </div>
  <div class="e-card-content">Product description here</div>
  <div class="e-card-actions">
    <button class="e-card-btn">Add to Cart</button>
  </div>
</div>
```

### Pattern 2: User Profile Card
Display user information with avatar and social actions:

```html
<div class="e-card" style="max-width: 350px;">
  <div class="e-card-header">
    <div class="e-card-header-image" style="width: 60px; height: 60px; background-image: url('avatar.jpg');"></div>
    <div class="e-card-header-caption">
      <div class="e-card-header-title">John Doe</div>
      <div class="e-card-sub-title">Senior Developer</div>
    </div>
  </div>
  <div class="e-card-content">Bio or description text</div>
  <div class="e-card-actions">
    <button class="e-card-btn">Follow</button>
    <button class="e-card-btn">Message</button>
  </div>
</div>
```

### Pattern 3: Horizontal Card Layout
Combine image with vertical content for compact horizontal layout:

```html
<div class="e-card e-card-horizontal" style="max-width: 500px;">
  <img src="image.jpg" alt="Image" style="height: 200px; width: 200px;">
  <div class="e-card-stacked">
    <div class="e-card-header">
      <div class="e-card-header-title">Title</div>
    </div>
    <div class="e-card-content">Content description</div>
  </div>
</div>
```

---

## Key Props and Classes Reference

| Class | Purpose | Usage |
|-------|---------|-------|
| `e-card` | Root container | Required for all cards |
| `e-card-header` | Header wrapper | Groups title, subtitle, images |
| `e-card-header-caption` | Header content container | Wraps titles and subtitles |
| `e-card-header-title` | Main header title | Card headline |
| `e-card-sub-title` | Subtitle text | Secondary header information |
| `e-card-header-image` | Header image | Avatar or header graphic |
| `e-card-content` | Content area | Main card body content |
| `e-card-image` | Content image | Full-width or sized images |
| `e-card-title` | Image overlay title | Caption over images |
| `e-card-separator` | Visual divider | Separation between sections |
| `e-card-actions` | Buttons container | Groups interactive elements |
| `e-card-btn` | Action button style | Interactive button element |
| `e-card-vertical` | Vertical alignment | Stack action buttons vertically |
| `e-card-horizontal` | Horizontal layout | Side-by-side element arrangement |
| `e-card-stacked` | Vertical section | Vertical area within horizontal layout |
| `e-card-corner` | Rounded corners | Add border-radius to images |

---

## Component Architecture

The Card component uses a layered CSS structure:

```
Card Container (e-card)
├── Header Section (e-card-header) [optional]
│   ├── Header Image (e-card-header-image) [optional]
│   └── Header Caption (e-card-header-caption)
│       ├── Header Title (e-card-header-title)
│       └── Subtitle (e-card-sub-title) [optional]
├── Image Container (e-card-image) [optional]
│   └── Image Title (e-card-title) [optional]
├── Content Section (e-card-content)
├── Separator (e-card-separator) [optional]
└── Actions Container (e-card-actions) [optional]
    ├── Button (e-card-btn)
    └── Link Elements
```

**Layout Modes:**
- **Vertical (default):** All elements stack vertically
- **Horizontal:** Use `e-card-horizontal` class to arrange elements side-by-side
- **Stacked within Horizontal:** Use `e-card-stacked` to force vertical flow in horizontal layouts

---

## Common Use Cases

1. **Product Catalogs:** Display products with images, descriptions, and purchase buttons
2. **User Profiles:** Show user information with avatars and action buttons
3. **Blog Posts:** Create article previews with images, excerpts, and read buttons
4. **Dashboard Widgets:** Build dashboard cards with data and interactive elements
5. **To-Do Lists:** Combine cards with ListView components for task management
6. **Image Galleries:** Display images with captions and metadata
7. **Team Members:** Show staff profiles with contact and role information
8. **Feature Highlights:** Showcase features with icons and descriptions

---

## Next Steps

Choose your learning path based on your needs:

- **New to Cards?** Start with [Getting Started](references/getting-started.md) to set up your first card
- **Building Complex Headers?** Read [Card Headers](references/card-headers.md) for advanced header patterns
- **Styling Your Cards?** Check [Styling and Customization](references/styling-customization.md) for CSS techniques
- **Creating Layouts?** Explore [Horizontal Layout](references/horizontal-layout.md) for side-by-side arrangements
- **Need Full Examples?** Each reference file includes complete, copy-paste-ready code

---

**Questions?** Each reference file has detailed examples and edge cases. Refer to the specific topic that matches your current need.
