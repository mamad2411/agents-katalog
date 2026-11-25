---
name: syncfusion-javascript-avatar
description: Implement Syncfusion TypeScript Avatar components for user representations. Use when user needs to display user profiles, avatars with different shapes (circular or rectangular), custom sizing, media formats (images, SVG, icons, letters), color customization, or integrate avatars with other controls like Badge or ListView.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Avatar Control

The Syncfusion Avatar control is a lightweight component used to display user profiles and representations in various formats including images, SVG, font icons, letters, and words. Avatars are essential for user-facing applications, contact lists, notification badges, and profile sections.

## When to Use Avatar

Use the Avatar control when you need to:
- Display user profile pictures or initials
- Create circular or rectangular user representations
- Show notification counts with badges
- Build contact lists or user directories
- Implement user avatars in messaging or social applications
- Display profile indicators with custom sizes and colors
- Integrate user representations with other UI components

## Control Overview

The Avatar control provides:
- **Multiple shapes**: Default (rounded rectangle) and circle
- **5 predefined sizes**: XLarge, Large, Default, Small, XSmall
- **Multiple media formats**: Images, SVG, font icons, letters, and words
- **Color customization**: Default gray or custom CSS classes
- **Component integration**: Works with Badge and ListView controls
- **Responsive design**: Scales based on font-size
- **ES5 and modern module support**: Compatible with various project setups

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and dependencies setup
- Webpack and CSS configuration
- Basic avatar implementation with HTML span
- Running the application
- ES5 global script alternatives
- CDN setup options

### Avatar Types and Sizes
📄 **Read:** [references/avatar-types-and-sizes.md](references/avatar-types-and-sizes.md)
- Avatar shape types (Default and Circle)
- Five size classes explained
- Size reference table
- Complete code examples for each type and size
- Visual demonstrations

### Customization and Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Color customization with CSS classes
- Custom sizing using font-size scaling
- Multiple media format support (images, SVG, icons, letters, words)
- CSS class customization examples
- Responsive design considerations
- Custom color palette examples

### Avatar with Badge Integration
📄 **Read:** [references/avatar-with-badge.md](references/avatar-with-badge.md)
- Combining Avatar with Badge control
- Notification badge positioning and styling
- Badge overlap technique
- Examples with all size combinations
- Notification badge with different counts

### Avatar in ListView
📄 **Read:** [references/avatar-in-listview.md](references/avatar-in-listview.md)
- Integrating Avatar with ListView control
- Creating contact list applications
- TypeScript implementation with data binding
- Template binding with conditional rendering
- Avatar positioning and styling in list items
- Complete working example with multiple contacts

## Quick Start Example

Basic avatar with default styling:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Avatar Quick Start</title>
    <link href="url" rel="stylesheet" />
    <link href="url" rel="stylesheet" />
</head>
<body>
    <!-- Default square avatar with initials -->
    <span class="e-avatar">AB</span>
    
    <!-- Circle avatar -->
    <span class="e-avatar e-avatar-circle">JD</span>
    
    <!-- Avatar with image -->
    <span class="e-avatar e-avatar-circle" style="background-image: url('profile.jpg')"></span>
</body>
</html>
```

## Common Patterns

### Pattern 1: Different Sizes
Apply size classes with the base `.e-avatar` class:

```html
<span class="e-avatar e-avatar-xlarge">AB</span>
<span class="e-avatar e-avatar-large">AB</span>
<span class="e-avatar">AB</span>
<span class="e-avatar e-avatar-small">AB</span>
<span class="e-avatar e-avatar-xsmall">AB</span>
```

### Pattern 2: Color Variations
Create custom color classes for avatars:

```html
<span class="e-avatar e-avatar-circle primary">JD</span>
<span class="e-avatar e-avatar-circle success">MK</span>
<span class="e-avatar e-avatar-circle warning">LP</span>
```

```css
.e-avatar.primary {
    background-color: #0071c1;
    color: white;
}

.e-avatar.success {
    background-color: #00b251;
    color: white;
}

.e-avatar.warning {
    background-color: #ffc900;
    color: #333;
}
```

### Pattern 3: Mixed Media Types
Display different avatar formats in a row:

```html
<div class="avatar-group">
    <!-- Image avatar -->
    <span class="e-avatar e-avatar-large" style="background-image: url('user1.jpg')"></span>
    
    <!-- SVG avatar -->
    <span class="e-avatar e-avatar-large">
        <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="15" fill="currentColor"/>
        </svg>
    </span>
    
    <!-- Letter avatar -->
    <span class="e-avatar e-avatar-large">AB</span>
    
    <!-- Icon avatar -->
    <span class="e-avatar e-avatar-large">
        <i class="icon-user"></i>
    </span>
</div>
```

### Pattern 4: Avatar with Status Badge
Combine avatar with notification indicator:

```html
<div style="position: relative; display: inline-block;">
    <span class="e-avatar e-avatar-large e-avatar-circle">JD</span>
    <span class="e-badge e-badge-success e-badge-overlap e-badge-circle">●</span>
</div>
```

## Key Properties and Classes

### Size Classes
- `.e-avatar-xlarge` - Extra large avatar
- `.e-avatar-large` - Large avatar
- `.e-avatar` - Default size
- `.e-avatar-small` - Small avatar
- `.e-avatar-xsmall` - Extra small avatar

### Shape Classes
- `.e-avatar` - Default (rounded rectangle)
- `.e-avatar-circle` - Circular shape

### Media Support
- **Images**: Use `background-image` property with `background-size: cover`
- **SVG**: Embed SVG markup or reference SVG files
- **Icons**: Use icon fonts or icon libraries
- **Text**: Display initials or short text directly

## Common Use Cases

**User Profile Display**
Display user avatar and information in a profile card with the appropriate size and shape.

**Contact List**
Use small or xsmall avatars in ListView for displaying contact lists with initials or profile pictures.

**Notification Badge**
Combine avatar with Badge control to show notification counts or status indicators.

**Team Member Grid**
Display team members in a grid layout with different avatar types and custom colors.

**Chat Application**
Use avatars in message threads to identify senders using small circle avatars with custom colors.

**User Selection UI**
Present users in dropdown or selection lists with consistent avatar styling and sizing.

## Next Steps

- Read [Getting Started](references/getting-started.md) for installation and basic setup
- Explore [Types and Sizes](references/avatar-types-and-sizes.md) for different shape and size options
- Learn [Customization](references/customization.md) for colors and media formats
- Check [Badge Integration](references/avatar-with-badge.md) for notification scenarios
- Review [ListView Integration](references/avatar-in-listview.md) for contact list patterns
