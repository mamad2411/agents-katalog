---
name: elementor-single-post-templates
description: Skills for designing and deploying Single Post and Custom Post Type templates in Elementor.
---

# Elementor Single Post Templates

## Overview
This skill involves creating dynamic templates for individual blog posts, custom post types, or products using Elementor Pro.

## Core Components
- **Post Title**: Dynamic widget that pulls the current post's title.
- **Featured Image**: Used as a background or standalone image widget.
- **Post Content**: The essential widget that displays the body of the WordPress post.
- **Post Info**: Meta data such as Author, Date, Time, and Comments.

## Best Practices
1. **Dynamic Widgets**: Exclusively use dynamic widgets (Post Title, Post Content, Author Box) instead of static text widgets.
2. **Fallback Images**: Ensure featured image widgets have a sensible fallback if a post lacks a featured image.
3. **Spacing and Typography**: Maintain consistent typography across all post types. Use Elementor's Site Settings for global fonts.
4. **Related Posts**: Include a Posts widget at the bottom of the template configured to show related posts by category or tag to improve SEO and user engagement.

## Display Conditions
- Apply to `Posts -> All` for standard blogs.
- Apply to specific categories if different designs are needed.
- Apply to Custom Post Types (e.g., `Portfolios`, `Services`).
