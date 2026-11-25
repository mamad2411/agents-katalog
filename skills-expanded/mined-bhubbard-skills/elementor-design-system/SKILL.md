---
name: elementor-design-system
description: Managing global colors, fonts, Variables, and Classes using Elementor's Design System to ensure consistent styling across the website.
---

# Elementor Design System

The Elementor Design System empowers you to define and manage your website's global styling in a centralized way. By utilizing Global Variables and Classes, you can ensure a consistent look and feel across all pages, while drastically reducing the time spent adjusting individual elements.

## Core Concepts

### Global Variables
Variables in Elementor represent specific design values—such as primary colors, typography settings, and spacing tokens—that are reused throughout the site. 
- **Consistency**: Changing a variable's value automatically updates every widget where that variable is applied.
- **Workflow**: Access the Design System panel to define variables before building layouts. 

### Global Classes
Classes allow you to group multiple design properties (e.g., background color, padding, border radius, box shadow) and apply them to elements universally.
- **Atomic Editor Integration**: Elementor's Atomic Editor (v4.0+) supports assigning classes to widgets and containers.
- **Reusability**: Build styling combinations once and assign the class to elements across multiple pages.
- **Maintenance**: Adjust the class properties from the Design System panel to update all linked instances instantly.

## Best Practices
1. **Define First**: Establish your Global Colors, Global Fonts, and standard Variables before adding content.
2. **Prioritize Classes Over Inline Styles**: Avoid styling individual widgets. Instead, create a class and apply it. This minimizes CSS bloat and prevents future styling inconsistencies.
3. **Use the Design System Panel**: Manage both Variables and Classes centrally rather than adjusting them at the widget level.
