# Cursor AI Instructions for Alma de Tüz Website

## 🚀 GETTING STARTED

When working on this project, ALWAYS:

1. **Read the rules first**: Check `.cursor/rules.md` for development standards
2. **Understand the context**: Review `.cursor/context.md` for project background
3. **Follow mobile-first**: Start with mobile design, scale up
4. **Use existing patterns**: Check similar components before creating new ones
5. **Test thoroughly**: Verify responsive design and functionality
6. **Update documentation**: Update docs files when a significant change is made

## 📋 TASK WORKFLOW

### Before Starting Any Task:

1. **Identify the component type**:
   - Layout component → Use `_layouts/`
   - Reusable UI → Use `_includes/`
   - Styling → Use `_sass/`
   - Content → Use appropriate content directory

2. **Check existing patterns**:
   - Look for similar components in `_includes/`
   - Review existing CSS in `_sass/`
   - Check current content structure

3. **Plan the approach**:
   - Mobile-first responsive design
   - Component reusability
   - SEO optimization needs
   - Performance impact

### During Development:

1. **Follow the established patterns**:
   - Use existing SASS variables
   - Follow component parameter structure
   - Implement proper error handling
   - Include accessibility features

2. **Test continuously**:
   - Check mobile responsive behavior
   - Verify form functionality
   - Test analytics tracking
   - Validate HTML/CSS

3. **Document your work**:
   - Add component usage examples
   - Update relevant documentation
   - Comment complex logic

### After Completing Tasks:

1. **Quality check**:
   - Run through testing checklist
   - Verify SEO metadata
   - Check accessibility compliance
   - Test across different screen sizes

2. **Performance review**:
   - Check page load speed
   - Verify image optimization
   - Test JavaScript functionality
   - Monitor analytics tracking

## 🛠️ COMMON TASK TYPES

### Creating New Components

```liquid
<!-- Template structure to follow -->
<!--
  Component: component-name.html
  Purpose: What this component does

  Required Parameters:
  - param_name (type): Description

  Usage Example:
  {% include component-name.html param_name="value" %}
-->

{% unless include.param_name %}
  {% error "component-name.html: param_name is required" %}
{% endunless %}

<div class="component-name {{ include.css_class }}">
  <!-- Component implementation -->
</div>
```

### Adding New Pages

```yaml
---
title: Unique Page Title (50-60 chars)
layout: page
seo_description: Compelling description (150-160 chars)
seo_image: /assets/images/page_seo.jpg
seo_image_width: 1280
seo_image_height: 720
---

Page content here using existing components:
{% include block_container_start.html %}
<!-- Content -->
{% include block_container_end.html %}
```

### Styling Components

```scss
// Follow SASS organization order
.component-name {
  // Mobile styles first
  display: block;
  padding: 1rem;

  // Use existing variables
  color: $color-eerie-black;
  background: $color-isabelline;

  // Responsive enhancements
  @media screen and (min-width: $bp-tablet) {
    padding: 2rem;
  }

  // BEM naming for variants
  &--variant {
    background: $color-tea-rose;
  }

  &__element {
    margin-bottom: 1rem;
  }
}
```

### Adding JavaScript

```javascript
(function() {
  'use strict';

  // Module pattern with error handling
  function initializeFeature() {
    try {
      // Feature implementation
      const elements = document.querySelectorAll('.feature-element');

      // Event delegation
      document.addEventListener('click', function(event) {
        if (event.target.matches('.feature-trigger')) {
          handleFeatureClick(event);
        }
      });

    } catch (error) {
      console.error('Feature initialization error:', error);
      // Graceful fallback
    }
  }

  // Auto-initialize
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeFeature);
  } else {
    initializeFeature();
  }
})();
```

## 📊 ANALYTICS INTEGRATION

When adding tracking to components:

```javascript
// Always check environment
if (environment === 'production') {
  // Amplitude tracking
  amp_event('ComponentInteraction', {
    component_name: 'component-name',
    action: 'click',
    ...web_event_prop
  });

  // Facebook Pixel
  fb_event('CustomEvent');

  // Google Ads
  gads_event('conversion', 'component_interaction');
}
```

## 🎵 MUSIC PLATFORM INTEGRATION

For music-related content:

```yaml
# Link page front matter
seo_type: music.song
seo_audio: /assets/audio/song_preview.mp3
seo_music_duration: 217
seo_music_album: https://artist.bandcamp.com/album/album-title
seo_mobile_bandcamp_url: https://artist.bandcamp.com/album/album-title
```

## 📱 RESPONSIVE DESIGN CHECKLIST

- [ ] Mobile styles as base (no media queries)
- [ ] Touch targets minimum 44px
- [ ] Readable text at all sizes
- [ ] Images scale appropriately
- [ ] Navigation works on mobile
- [ ] Forms are mobile-friendly
- [ ] Performance acceptable on mobile

## 🔍 SEO CHECKLIST

- [ ] Unique page title (50-60 characters)
- [ ] Meta description (150-160 characters)
- [ ] SEO image (1280x720px)
- [ ] One H1 per page
- [ ] Logical heading hierarchy
- [ ] Alt text for all images
- [ ] Clean URL structure
- [ ] Internal linking strategy

## 🧪 TESTING CHECKLIST

- [ ] Component renders correctly
- [ ] Responsive behavior works
- [ ] Forms submit successfully
- [ ] JavaScript functions without errors
- [ ] Analytics tracking fires
- [ ] Page loads under 3 seconds
- [ ] No console errors
- [ ] Accessibility features work

## 🚨 TROUBLESHOOTING

### Common Issues and Solutions:

**Jekyll Build Errors**:
```bash
bundle exec jekyll clean
bundle exec jekyll build --verbose
```

**SASS Compilation Issues**:
- Check variable definitions in `_sass/`
- Verify import paths in `styles.scss`
- Look for syntax errors in SASS files

**Component Not Rendering**:
- Check parameter validation
- Verify include path is correct
- Look for Liquid syntax errors

**JavaScript Errors**:
- Check browser console for errors
- Verify event delegation setup
- Test progressive enhancement

**Analytics Not Tracking**:
- Verify environment detection
- Check analytics script loading
- Test event firing manually

## 📚 REFERENCE DOCUMENTATION

- **Project Rules**: `.cursor/rules.md`
- **Project Context**: `.cursor/context.md`
- **Architecture Docs**: `docs/` directory
- **Component Examples**: `_includes/` directory
- **Layout Patterns**: `_layouts/` directory

## 🎯 SUCCESS CRITERIA

Your work is successful when:

1. **Functionality**: Feature works as intended
2. **Responsive**: Works across all device sizes
3. **Performance**: No negative impact on page speed
4. **SEO**: Proper metadata and structure
5. **Accessibility**: Usable by all users
6. **Consistency**: Follows established patterns
7. **Documentation**: Code is well-documented
8. **Testing**: Thoroughly tested and validated

---

**Remember**: Quality is more important than speed. Take time to follow the established patterns and test thoroughly. The goal is to maintain the high standards of this professional artist website while adding valuable new functionality.
