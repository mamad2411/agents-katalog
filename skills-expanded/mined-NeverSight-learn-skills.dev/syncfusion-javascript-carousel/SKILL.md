---
name: syncfusion-javascript-carousel
description: Build carousel components for displaying image galleries, news headlines, and rotating content. Use this skill when implementing image sliders, automatic content rotation, or carousel-based galleries. Covers navigation controls, slide transitions, animation effects, and indicators.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Syncfusion Carousel

The Carousel component allows users to display images with content, links, and other media in a slide show format. It's perfect for creating image galleries, displaying rotating content, featured items, and interactive media presentations.

## Key Features

- **Multiple item rendering** - Display items from arrays or data sources
- **Animation effects** - Smooth transitions with Slide, Fade, or custom animations
- **Navigation controls** - Previous/Next buttons with configurable visibility modes
- **Indicators** - Show slide position with numeric, dot, dynamic, or progress indicators
- **Auto-play** - Automatic slide progression with configurable intervals
- **Keyboard support** - Full keyboard navigation support
- **Accessibility** - WAI-ARIA compliant for assistive technologies
- **Touch/Mouse swiping** - Gesture-based navigation on touch devices
- **Template support** - Custom HTML templates for items and buttons
- **Responsive** - Adapts to different screen sizes and partial visibility modes

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and dependencies
- Package setup with npm
- CSS imports and theme configuration
- Basic carousel initialization
- First working example with HTML and TypeScript

### Populating Carousel Items
📄 **Read:** [references/populating-items.md](references/populating-items.md)
- Creating and populating items array
- Template syntax for individual items
- Data source binding approaches
- Dynamic item rendering
- Item-specific configuration
- WebP image format optimization for better performance

### Animations and Transitions
📄 **Read:** [references/animations-and-transitions.md](references/animations-and-transitions.md)
- Animation effect types (Slide, Fade, None, Custom)
- Configuring animation timing
- Disabling animations when needed
- Animation examples and patterns
- Performance considerations

### Navigators and Indicators
📄 **Read:** [references/navigators-and-indicators.md](references/navigators-and-indicators.md)
- Navigation button visibility modes (Hidden, Visible, VisibleOnHover)
- Indicator types (Default, Dynamic, Fraction, Progress)
- Auto-play and interval configuration
- Play/Pause button control
- Manual slide navigation
- Loop and direction configuration

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS class structure and customization
- Styling indicators and their appearance
- Customizing navigation buttons
- Theme Studio integration
- Creating custom themes
- Responsive design patterns

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property reference with types and defaults
- 12 methods for carousel control and navigation
- Event handling (slideChanged, slideChanging)
- Type definitions and enumerations
- Item model and data structures

## Quick Start Example

```typescript
import { Carousel } from "@syncfusion/ej2-navigations";

// Create carousel with basic items
const carouselObj = new Carousel({
  items: [
    { template: '<img src="image1.jpg" alt="Image 1" style="height:100%;width:100%;" />' },
    { template: '<img src="image2.jpg" alt="Image 2" style="height:100%;width:100%;" />' },
    { template: '<img src="image3.jpg" alt="Image 3" style="height:100%;width:100%;" />' }
  ],
  animationEffect: "Slide",
  autoPlay: true,
  interval: 3000,
  buttonsVisibility: "Visible"
});

// Append to DOM
carouselObj.appendTo("#carousel");
```

## Common Patterns

### Image Gallery with Auto-play
```typescript
const carousel = new Carousel({
  items: galleryImages,
  autoPlay: true,
  interval: 4000,
  pauseOnHover: true,
  animationEffect: "Fade"
});
carousel.appendTo("#gallery");
```

### Manual Navigation Only
```typescript
const carousel = new Carousel({
  items: slides,
  autoPlay: false,
  buttonsVisibility: "Visible",
  indicatorsType: "Numeric"
});
carousel.appendTo("#slides");
```

### With Event Handling
```typescript
const carousel = new Carousel({
  items: items,
  autoPlay: true
});

carousel.addEventListener('slideChanged', (args) => {
  console.log(`Slide changed to: ${args.currentIndex}`);
});

carousel.addEventListener('slideChanging', (args) => {
  if (args.nextIndex === 5) {
    args.cancel = true; // Prevent navigation to slide 5
  }
});

carousel.appendTo("#carousel");
```

### Responsive Partial Visible
```typescript
const carousel = new Carousel({
  items: items,
  partialVisible: true,
  width: "100%",
  height: "auto",
  animationEffect: "Slide"
});
carousel.appendTo("#container");
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `items` | CarouselItemModel[] | Array of carousel items to display |
| `autoPlay` | boolean | Enable automatic slide progression |
| `interval` | number | Milliseconds between auto-play transitions |
| `animationEffect` | CarouselAnimationEffect | Slide transition animation type |
| `buttonsVisibility` | CarouselButtonVisibility | Show/hide navigation buttons |
| `indicatorsType` | CarouselIndicatorsType | Style of position indicators |
| `showIndicators` | boolean | Display indicator dots/numbers |
| `showPlayButton` | boolean | Display play/pause button |
| `pauseOnHover` | boolean | Pause auto-play when hovering |
| `enableTouchSwipe` | boolean | Allow touch swipe gestures |
| `allowKeyboardInteraction` | boolean | Enable keyboard navigation |
| `loop` | boolean | Restart from beginning after last slide |
| `partialVisible` | boolean | Show previous/next slides partially |
| `height` | string \| number | Carousel height in pixels or percentage |
| `width` | string \| number | Carousel width in pixels or percentage |

## Common Use Cases

**Image Gallery**
- Photo albums with thumbnails
- Product showcase with multiple images
- Featured items carousel

**News/Content Rotation**
- Rotating headline display
- Featured article carousel
- Testimonial rotation

**Media Presentations**
- Slideshow viewer
- Portfolio presentation
- Video thumbnail carousel

**E-commerce**
- Product image gallery
- Featured products section
- Category showcase

**Landing Pages**
- Hero image rotation
- Featured section carousel
- Promotional banners

---

## Next Steps

1. **Start with Getting Started** - Set up your first carousel
2. **Choose your approach** - Items array or data source binding
3. **Configure animations** - Select transition effects
4. **Add navigation** - Set up buttons and indicators
5. **Customize styling** - Apply your theme and CSS
6. **Handle events** - Respond to slide changes
7. **Reference API** - Use methods for programmatic control

For detailed implementation patterns and advanced features, refer to the appropriate reference guide above.
