---
name: syncfusion-aspnetcore-carousel
description: Implement Syncfusion ASP.NET Core Carousel component for displaying rotating content and image galleries with customizable animations, navigation controls, and event handling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigators"
---

# Implementing Syncfusion ASP.NET Core Carousel Component

The Carousel component displays a set of slides with support for automatic transitions, touch/mouse swiping, customizable animations, and various indicator styles. It's ideal for image galleries, content rotators, testimonials, and any scenario requiring sequential content presentation.

## When to Use This Skill

Use this skill when you need to:

- **Create an image carousel or gallery** – Display multiple images or content items that users can browse
- **Implement automatic slide transitions** – Show rotating content with configurable intervals and animations
- **Add navigation controls** – Enable manual navigation with previous/next buttons and interactive indicators
- **Handle slide change events** – Track when slides change and respond with custom logic
- **Support touch and mouse interactions** – Enable swipe gestures on mobile and mouse drag on desktop
- **Customize animation effects** – Apply fade, slide, or custom CSS animations during transitions
- **Optimize performance** – Load images in modern WebP format and manage carousel state persistence
- **Build accessible slideshows** – Implement keyboard navigation and proper ARIA support

## Component Overview

The Carousel component consists of:

- **Carousel container** (`<ejs-carousel>`) – Main component wrapper
- **Carousel items** (`<e-carousel-item>`) – Individual slide elements
- **Navigation buttons** – Previous/next controls with customizable templates
- **Indicators** – Visual indicators showing current position (dots, dynamic, fraction, or progress)
- **Play/Pause controls** – Optional playback control UI
- **Event system** – Slide changing and slide changed events for custom logic

## Key Concepts

- **Auto-play** – Automatically transitions between slides at specified intervals
- **Looping** – Allows continuous cycling from last slide back to first
- **Animation effects** – Built-in Slide and Fade effects, plus custom CSS animations
- **Partial visible slides** – Shows adjacent slide previews alongside the active slide
- **Swipe modes** – Independent control of touch and mouse swiping interactions
- **Item templates** – Individual templates per item or a common template for all items
- **Data binding** – Populate carousel from data source or declarative item markup

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

- Install NuGet packages (Syncfusion.EJ2.AspNet.Core)
- Register Tag Helper in `_ViewImports.cshtml`
- Add stylesheet and script resources (CDN or local)
- Create your first basic carousel with template items
- Verify rendering and initial setup

### Populating Items and Data Binding

📄 **Read:** [references/populating-items.md](references/populating-items.md)

- Populate items using carousel item markup (`<e-carousel-item>`)
- Populate items using data source binding with `itemTemplate`
- Set `selectedIndex` to start at a specific slide
- Show partial visible slides with adjacent slide previews
- Customize per-item template or interval duration

### Animations and Transitions

📄 **Read:** [references/animations-transitions.md](references/animations-transitions.md)

- Configure animation effects (None, Slide, Fade, Custom)
- Set slide transition intervals (milliseconds)
- Enable/disable auto-play and pause-on-hover behavior
- Control looping behavior at the end of slides
- Disable touch swipe and configure swipe modes
- Handle slide changing and slide changed events

### Navigation Controls and Indicators

📄 **Read:** [references/navigation-indicators.md](references/navigation-indicators.md)

- Show/hide navigation buttons (Hidden, Visible, VisibleOnHover)
- Customize navigation button templates
- Configure indicator types (Default, Dynamic, Fraction, Progress)
- Customize indicator templates and previews
- Enable/disable play/pause button controls
- Customize play button template

### Performance and Optimization

📄 **Read:** [references/optimization.md](references/optimization.md)

- Load images in WebP format for better performance
- Enable state persistence across page reloads
- Configure RTL rendering for right-to-left languages
- Apply CSS class customization
- Optimize data source binding for large datasets

### API Reference

📄 **Read:** [references/api-reference.md](references/api-reference.md)

- Complete property reference with descriptions and types
- Event arguments and event handling patterns
- Enumeration types and allowed values
- TagHelper attribute mapping
- HTML attributes support

## Quick Start Example

```html
<div class="carousel-container">
    <ejs-carousel id="basicCarousel" 
                   autoPlay="true" 
                   animationEffect="Slide"
                   buttonsVisibility="Visible"
                   showIndicators="true">
        <e-carousel-items>
            <e-carousel-item template="#slide1"></e-carousel-item>
            <e-carousel-item template="#slide2"></e-carousel-item>
            <e-carousel-item template="#slide3"></e-carousel-item>
        </e-carousel-items>
    </ejs-carousel>
</div>

<script id="slide1" type="text/x-template">
    <img src="/images/slide1.jpg" alt="Slide 1" style="height: 100%; width: 100%;" />
</script>

<script id="slide2" type="text/x-template">
    <img src="/images/slide2.jpg" alt="Slide 2" style="height: 100%; width: 100%;" />
</script>

<script id="slide3" type="text/x-template">
    <img src="/images/slide3.jpg" alt="Slide 3" style="height: 100%; width: 100%;" />
</script>

<style>
.carousel-container {
    max-width: 600px;
    height: 400px;
    margin: 20px auto;
}
</style>
```

## Common Implementation Patterns

### Pattern 1: Image Gallery with Auto-Play

Create an automatic image carousel that cycles through slides and pauses on user hover:

```html
<ejs-carousel id="photoGallery" 
              autoPlay="true" 
              pauseOnHover="true"
              interval="3000">
    <e-carousel-items>
        <e-carousel-item template="#photo1"></e-carousel-item>
        <e-carousel-item template="#photo2"></e-carousel-item>
    </e-carousel-items>
</ejs-carousel>
```

### Pattern 2: Manual Navigation with Custom Indicators

Create a carousel with manual navigation and custom indicator styling:

```html
<ejs-carousel id="manualCarousel" 
              autoPlay="false"
              buttonsVisibility="Visible"
              showIndicators="true"
              indicatorsType="Fraction">
    <e-carousel-items>
        <e-carousel-item template="#item1"></e-carousel-item>
        <e-carousel-item template="#item2"></e-carousel-item>
    </e-carousel-items>
</ejs-carousel>
```

### Pattern 3: Data-Bound Carousel

Populate carousel from a data source with uniform template:

```html
<ejs-carousel id="dataCarousel" 
              dataSource="@Model.Slides"
              itemTemplate="#itemTemplate">
</ejs-carousel>

<script id="itemTemplate" type="text/x-template">
    <div class="slide-content">
        <img src="${image}" alt="${title}" style="height: 100%; width: 100%;" />
        <h3>${title}</h3>
    </div>
</script>
```

### Pattern 4: Event-Driven Slide Tracking

Handle slide transitions and track user interactions:

```html
<ejs-carousel id="trackedCarousel" 
              slideChanging="onSlideChanging"
              slideChanged="onSlideChanged">
    <e-carousel-items>
        <e-carousel-item template="#slide1"></e-carousel-item>
    </e-carousel-items>
</ejs-carousel>

<script>
function onSlideChanging(args) {
    console.log('Moving from slide ' + args.currentIndex + ' to ' + args.nextIndex);
}

function onSlideChanged(args) {
    console.log('Now on slide ' + args.currentIndex);
}
</script>
```

## Key Properties

| Property | Type | Purpose | Common Values |
|----------|------|---------|----------------|
| `autoPlay` | boolean | Enable automatic slide transitions | true, false |
| `interval` | number | Milliseconds between auto-transitions | 5000, 3000 |
| `animationEffect` | enum | Transition animation type | Slide, Fade, None, Custom |
| `buttonsVisibility` | enum | Navigation button visibility | Visible, Hidden, VisibleOnHover |
| `showIndicators` | boolean | Display slide position indicators | true, false |
| `indicatorsType` | enum | Indicator style | Default, Dynamic, Fraction, Progress |
| `loop` | boolean | Cycle from last slide to first | true, false |
| `pauseOnHover` | boolean | Pause auto-play when hovering | true, false |
| `enableTouchSwipe` | boolean | Enable swipe on touch devices | true, false |
| `selectedIndex` | number | Initial slide index | 0, 1, 2... |
| `partialVisible` | boolean | Show adjacent slide previews | true, false |

## Common Use Cases

- **E-Commerce Product Showcase** – Display product images with navigation
- **Blog or Portfolio Gallery** – Showcase projects or articles sequentially
- **Testimonials Carousel** – Rotate customer testimonials automatically
- **Advertisements/Promotions** – Cycle promotional banners
- **Hero Sections** – Full-width rotating content on landing pages
- **News/Updates Feed** – Display latest news items in rotating carousel
- **Social Media Feeds** – Show image posts in carousel format

## Browser Support

The Carousel component works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Android)

## Performance Tips

- Use WebP images for better performance
- Set appropriate `interval` values to reduce CPU usage
- Disable auto-play if not needed
- Use `partialVisible: false` to reduce rendering overhead
- Consider lazy-loading images for large galleries

## Next Steps

1. Start with [Getting Started](references/getting-started.md) to set up your environment
2. Choose your use case from the patterns above
3. Review the relevant reference section for your features
4. Check [API Reference](references/api-reference.md) for complete property documentation
5. Handle events as needed for your scenario

---

**Need more help?** Check individual reference files for detailed examples and advanced configurations.
