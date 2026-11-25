---
name: blogger-vault-elite-designs-templates
description: Premium responsive Blogger template system with modular components, atomic CSS, and SEO optimization
triggers:
  - "install a premium blogger template"
  - "customize blogger theme layout"
  - "apply responsive blogger design"
  - "setup blogger template with dark mode"
  - "optimize blogger template for SEO"
  - "customize blogger widget zones"
  - "configure blogger template variables"
  - "implement modular blogger components"
---

# Blogger Vault Elite Designs Templates

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Blogger Vault Elite Designs (TemplateForge Pro) is a collection of production-grade Blogger templates featuring modular architecture, atomic CSS methodology, and performance optimization. Templates load under 2 seconds, pass Core Web Vitals, and maintain WCAG 2.1 AA compliance. Each template averages under 18KB total footprint with responsive breakpoints, dark mode support, and Schema.org markup.

## Installation

### Basic Template Application

1. **Download Template**
   - Navigate to: https://bungdollzdollz.github.io/Blogger-Vault-Elite-Designs/
   - Select desired template category (Editorial, Portfolio, Minimal, E-commerce, Multimedia)
   - Download the template XML file

2. **Apply to Blogger**
   ```bash
   # In Blogger Dashboard:
   # 1. Navigate to Theme section
   # 2. Click "Backup/Restore" dropdown
   # 3. Choose "Upload" and select downloaded XML
   # 4. Confirm application
   ```

3. **Verify Installation**
   - Check responsive breakpoints: 320px, 768px, 1024px, 1440px
   - Test dark mode toggle (if applicable)
   - Validate widget zones rendering

## Template Categories

### Editorial Templates
For news, magazines, and long-form content:
```xml
<!-- Key features in template structure -->
<b:section id='main-column' class='grid-2-col' showaddelement='yes'>
  <b:widget id='Blog1' type='Blog' locked='false'/>
</b:section>
<b:section id='sidebar' class='sticky-sidebar' showaddelement='yes'>
  <b:widget id='PopularPosts1' type='PopularPosts'/>
</b:section>
```

### Portfolio Templates
For photographers and designers:
```xml
<!-- Masonry gallery structure -->
<div class='masonry-grid' data-columns='3'>
  <b:loop values='data:posts' var='post'>
    <article class='masonry-item'>
      <b:if cond='data:post.featuredImage'>
        <img expr:src='data:post.featuredImage' loading='lazy'/>
      </b:if>
    </article>
  </b:loop>
</div>
```

### Minimal Templates
For personal blogs and journals:
```xml
<!-- Whitespace-driven layout -->
<main class='content-wrapper max-w-prose mx-auto'>
  <article class='post-single serif-body'>
    <h1 class='h1-display'><data:post.title/></h1>
    <div class='post-body'>
      <data:post.body/>
    </div>
  </article>
</main>
```

## Customization

### Variables Configuration

Edit `_variables.xml` to customize without touching core CSS:

```xml
<!-- Color system -->
<Variable name="primary.color" description="Primary brand color" 
          type="color" default="#2563eb" value="#2563eb"/>
<Variable name="text.color" description="Body text color" 
          type="color" default="#1f2937" value="#1f2937"/>
<Variable name="bg.color" description="Background color" 
          type="color" default="#ffffff" value="#ffffff"/>

<!-- Typography -->
<Variable name="font.body" description="Body font stack" 
          type="string" default="system-ui, -apple-system, sans-serif" 
          value="system-ui, -apple-system, sans-serif"/>
<Variable name="font.heading" description="Heading font stack" 
          type="string" default="Georgia, serif" 
          value="Georgia, serif"/>

<!-- Spacing -->
<Variable name="spacing.unit" description="Base spacing unit" 
          type="string" default="1rem" value="1rem"/>
<Variable name="container.width" description="Max content width" 
          type="string" default="1280px" value="1280px"/>
```

### Dark Mode Implementation

```xml
<!-- Add to template head -->
<b:if cond='data:view.isDarkMode'>
  <style>
    :root {
      --bg-color: #1f2937;
      --text-color: #f9fafb;
      --primary-color: #60a5fa;
    }
  </style>
</b:if>

<!-- Toggle button -->
<button id='dark-mode-toggle' aria-label='Toggle dark mode'>
  <b:if cond='data:view.isDarkMode'>☀️<b:else/>🌙</b:if>
</button>

<script>
document.getElementById('dark-mode-toggle').addEventListener('click', () => {
  document.documentElement.classList.toggle('dark-mode');
  localStorage.setItem('darkMode', 
    document.documentElement.classList.contains('dark-mode'));
});
</script>
```

### Widget Zone Customization

```xml
<!-- Custom CTA widget zone -->
<b:section id='cta-zone' class='widget-zone' maxwidgets='1' showaddelement='yes'>
  <b:widget id='HTML1' type='HTML' locked='false'>
    <b:includable id='main'>
      <div class='cta-card bg-primary text-white p-6 rounded'>
        <data:content/>
      </div>
    </b:includable>
  </b:widget>
</b:section>

<!-- Newsletter widget -->
<b:section id='newsletter' class='widget-zone' maxwidgets='1'>
  <b:widget id='HTML2' type='HTML' locked='false'>
    <b:includable id='main'>
      <form action='YOUR_NEWSLETTER_ENDPOINT' method='post' class='newsletter-form'>
        <input type='email' name='email' placeholder='Enter your email' required='required'/>
        <button type='submit'>Subscribe</button>
      </form>
    </b:includable>
  </b:widget>
</b:section>
```

## SEO Configuration

### Schema.org Markup

```xml
<!-- Article schema (automatically included) -->
<script type='application/ld+json'>
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "<data:post.title/>",
  "image": "<data:post.featuredImage/>",
  "author": {
    "@type": "Person",
    "name": "<data:post.author.name/>"
  },
  "datePublished": "<data:post.date.iso8601/>",
  "dateModified": "<data:post.lastUpdated.iso8601/>",
  "publisher": {
    "@type": "Organization",
    "name": "<data:blog.title/>",
    "logo": {
      "@type": "ImageObject",
      "url": "<data:blog.logoUrl/>"
    }
  }
}
</script>
```

### Meta Tags Configuration

```xml
<!-- Open Graph -->
<meta expr:content='data:post.title' property='og:title'/>
<meta expr:content='data:post.url' property='og:url'/>
<meta expr:content='data:post.featuredImage' property='og:image'/>
<meta expr:content='data:post.snippet' property='og:description'/>
<meta content='article' property='og:type'/>

<!-- Twitter Card -->
<meta content='summary_large_image' name='twitter:card'/>
<meta expr:content='data:post.title' name='twitter:title'/>
<meta expr:content='data:post.snippet' name='twitter:description'/>
<meta expr:content='data:post.featuredImage' name='twitter:image'/>
```

## Performance Optimization

### Lazy Loading Images

```xml
<!-- Automatic lazy loading -->
<b:loop values='data:posts' var='post'>
  <b:if cond='data:post.featuredImage'>
    <img expr:src='data:post.featuredImage' 
         expr:alt='data:post.title'
         loading='lazy'
         decoding='async'
         width='800'
         height='450'/>
  </b:if>
</b:loop>
```

### Critical CSS Inline

```xml
<!-- Add to <head> for above-the-fold content -->
<style>
/* Critical styles - base layout */
body{margin:0;font-family:system-ui,sans-serif;line-height:1.5}
.header{position:sticky;top:0;background:#fff;z-index:100}
.container{max-width:1280px;margin:0 auto;padding:0 1rem}
.grid-2-col{display:grid;grid-template-columns:2fr 1fr;gap:2rem}

/* Mobile-first breakpoint */
@media(max-width:768px){
  .grid-2-col{grid-template-columns:1fr}
}
</style>
```

### Deferred JavaScript

```xml
<!-- Load non-critical JS asynchronously -->
<script async='async' defer='defer' src='YOUR_SCRIPT_URL'/>

<!-- Inline critical interaction -->
<script>
//<![CDATA[
// Menu toggle
document.getElementById('menu-toggle').addEventListener('click', function() {
  document.getElementById('mobile-menu').classList.toggle('open');
});
//]]>
</script>
```

## Common Patterns

### Responsive Navigation

```xml
<nav class='header-nav'>
  <button id='menu-toggle' aria-label='Toggle menu' class='md:hidden'>
    ☰
  </button>
  <ul id='mobile-menu' class='nav-list'>
    <b:loop values='data:blog.pages' var='page'>
      <li><a expr:href='data:page.url'><data:page.title/></a></li>
    </b:loop>
  </ul>
</nav>

<style>
.nav-list { display: none; }
.nav-list.open { display: block; }
@media (min-width: 768px) {
  .nav-list { display: flex; gap: 1rem; }
}
</style>
```

### Post Card Component

```xml
<b:loop values='data:posts' var='post'>
  <article class='post-card'>
    <b:if cond='data:post.featuredImage'>
      <div class='post-thumbnail'>
        <img expr:src='data:post.featuredImage' expr:alt='data:post.title' loading='lazy'/>
      </div>
    </b:if>
    <div class='post-content'>
      <h2 class='post-title'>
        <a expr:href='data:post.url'><data:post.title/></a>
      </h2>
      <p class='post-snippet'><data:post.snippet/></p>
      <div class='post-meta'>
        <time expr:datetime='data:post.date.iso8601'>
          <data:post.date/>
        </time>
        <span class='separator'>•</span>
        <span class='author'><data:post.author.name/></span>
      </div>
    </div>
  </article>
</b:loop>
```

### Breadcrumb Navigation

```xml
<nav aria-label='Breadcrumb' class='breadcrumb'>
  <ol itemscope='itemscope' itemtype='https://schema.org/BreadcrumbList'>
    <li itemprop='itemListElement' itemscope='itemscope' 
        itemtype='https://schema.org/ListItem'>
      <a expr:href='data:blog.homepageUrl' itemprop='item'>
        <span itemprop='name'>Home</span>
      </a>
      <meta content='1' itemprop='position'/>
    </li>
    <b:if cond='data:view.isPost'>
      <li itemprop='itemListElement' itemscope='itemscope' 
          itemtype='https://schema.org/ListItem'>
        <span itemprop='name'><data:post.title/></span>
        <meta content='2' itemprop='position'/>
      </li>
    </b:if>
  </ol>
</nav>
```

## Troubleshooting

### Template Upload Fails

**Issue**: "Template contains invalid elements"
```xml
<!-- Ensure all Blogger tags are properly closed -->
<b:if cond='condition'>
  <!-- content -->
</b:if>

<!-- Use CDATA for JavaScript -->
<script>
//<![CDATA[
// Your JS code
//]]>
</script>
```

### Widget Not Displaying

**Issue**: Custom widget doesn't appear
```xml
<!-- Verify section has correct attributes -->
<b:section id='unique-id' class='widget-section' 
           showaddelement='yes' maxwidgets='3'>
  <!-- widgets here -->
</b:section>

<!-- Check widget has required includable -->
<b:widget id='Widget1' type='HTML'>
  <b:includable id='main'>
    <data:content/>
  </b:includable>
</b:widget>
```

### Responsive Breakpoints Not Working

**Issue**: Layout doesn't adapt on mobile
```xml
<!-- Add viewport meta tag to head -->
<meta content='width=device-width, initial-scale=1.0' name='viewport'/>

<!-- Use mobile-first CSS -->
<style>
/* Mobile default */
.grid { display: block; }

/* Tablet and up */
@media (min-width: 768px) {
  .grid { display: grid; grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
```

### Dark Mode Not Persisting

**Issue**: Dark mode resets on page reload
```xml
<script>
//<![CDATA[
// Check localStorage on load
if (localStorage.getItem('darkMode') === 'true') {
  document.documentElement.classList.add('dark-mode');
}

// Save preference on toggle
document.getElementById('dark-mode-toggle').addEventListener('click', () => {
  const isDark = document.documentElement.classList.toggle('dark-mode');
  localStorage.setItem('darkMode', isDark);
});
//]]>
</script>
```

### SEO Meta Tags Missing

**Issue**: Social sharing doesn't show preview
```xml
<!-- Ensure all required meta tags are in head -->
<b:if cond='data:view.isPost'>
  <meta expr:content='data:post.title' property='og:title'/>
  <meta expr:content='data:post.url' property='og:url'/>
  <meta expr:content='data:post.firstImageUrl' property='og:image'/>
  <meta expr:content='data:post.snippet' property='og:description'/>
  <meta content='article' property='og:type'/>
</b:if>
```

## Advanced Customization

### Custom Font Integration

```xml
<!-- Add to head for Google Fonts -->
<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;display=swap' 
      rel='stylesheet'/>

<!-- Update variables -->
<Variable name="font.body" value="'Inter', system-ui, sans-serif"/>

<!-- Or use self-hosted fonts -->
<style>
@font-face {
  font-family: 'CustomFont';
  src: url('YOUR_CDN_URL/font.woff2') format('woff2');
  font-display: swap;
}
body { font-family: 'CustomFont', sans-serif; }
</style>
```

### Cookie Consent UI

```xml
<div id='cookie-consent' class='cookie-banner' style='display:none'>
  <p>We use cookies to improve your experience.</p>
  <button id='accept-cookies'>Accept</button>
</div>

<script>
//<![CDATA[
if (!localStorage.getItem('cookieConsent')) {
  document.getElementById('cookie-consent').style.display = 'block';
}

document.getElementById('accept-cookies').addEventListener('click', () => {
  localStorage.setItem('cookieConsent', 'true');
  document.getElementById('cookie-consent').style.display = 'none';
});
//]]>
</script>
```

### Print Stylesheet

```xml
<style media='print'>
@page { margin: 2cm; }
.header, .sidebar, .comments, .footer { display: none; }
.post-body { max-width: 100%; }
a[href]:after { content: ' (' attr(href) ')'; }
</style>
```

## Best Practices

1. **Always backup** existing theme before applying new template
2. **Test on multiple devices** after installation (mobile, tablet, desktop)
3. **Validate HTML** using W3C validator before deployment
4. **Check performance** with Google PageSpeed Insights (target 90+ score)
5. **Update variables.xml** instead of modifying core CSS for easier updates
6. **Use semantic HTML** for better accessibility and SEO
7. **Optimize images** before upload (use WebP format when possible)
8. **Keep JavaScript minimal** and defer non-critical scripts

## Resources

- Preview templates: https://bungdollzdollz.github.io/Blogger-Vault-Elite-Designs/
- Repository: https://github.com/bungdollzdollz/Blogger-Vault-Elite-Designs
- Documentation: `/docs` folder in repository
- Community support: GitHub Issues
