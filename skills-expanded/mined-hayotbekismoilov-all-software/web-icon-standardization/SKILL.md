# Web Icon Standardization Skill

## Purpose
Ensure consistent branding across all web projects by automatically using the Advokatura Platform's standard icon (`myweb.uz/icon.png`) as the website favicon and metadata image whenever creating or updating a website.

## When to Use This Skill
- Creating a new React/Next.js/Vite web project
- Setting up favicon and manifest configurations
- Configuring Open Graph and social media metadata
- Updating existing projects to use brand-standard icons
- Generating HTML head tags with icon references

## Standard Icon URL
```
https://myweb.uz/icon.png
```

## Implementation Checklist

### 1. Favicon Setup (HTML)
Add to `index.html` `<head>`:
```html
<link rel="icon" type="image/png" href="https://myweb.uz/icon.png" />
<link rel="shortcut icon" href="https://myweb.uz/icon.png" />
<link rel="apple-touch-icon" href="https://myweb.uz/icon.png" />
```

### 2. Manifest Configuration (PWA)
In `public/manifest.json`:
```json
{
  "name": "Advokatura Platform",
  "short_name": "Advokatura",
  "icons": [
    {
      "src": "https://myweb.uz/icon.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "https://myweb.uz/icon.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    }
  ],
  "theme_color": "#1a2a5a",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

### 3. Meta Tags (Open Graph / Social)
Add to HTML `<head>`:
```html
<!-- Open Graph -->
<meta property="og:image" content="https://myweb.uz/icon.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter Card -->
<meta name="twitter:image" content="https://myweb.uz/icon.png" />

<!-- Favicon Variants -->
<meta name="msapplication-square150x150logo" content="https://myweb.uz/icon.png" />
<meta name="msapplication-TileImage" content="https://myweb.uz/icon.png" />
<meta name="msapplication-TileColor" content="#1a2a5a" />
```

### 4. SEO Metadata (Next.js/React)
```typescript
// next.config.js or metadata file
export const metadata = {
  title: 'Advokatura Platform',
  description: 'Yuridik xizmatlar',
  icons: {
    icon: 'https://myweb.uz/icon.png',
    apple: 'https://myweb.uz/icon.png',
  },
  openGraph: {
    images: [
      {
        url: 'https://myweb.uz/icon.png',
        width: 1200,
        height: 630,
      },
    ],
  },
};
```

### 5. Tailwind Config (if using brand icon)
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      backgroundImage: {
        'brand-icon': 'url(https://myweb.uz/icon.png)',
      },
    },
  },
};
```

## Files to Update

| File | Change |
|------|--------|
| `index.html` | Add favicon links |
| `public/manifest.json` | Add icon URLs to PWA manifest |
| `src/main.tsx` or `_app.tsx` | Add meta tags dynamically |
| `vite.config.ts` or `next.config.js` | Link favicon in build config |
| `package.json` | Verify favicon plugin if using |

## Quality Checks

✅ **Before Publishing:**
- [ ] Favicon displays in browser tab
- [ ] Icon appears in bookmarks
- [ ] Social media preview shows correct image
- [ ] PWA manifest loads successfully
- [ ] Mobile home screen shows icon (iOS/Android)
- [ ] RSS feeds use correct icon
- [ ] Favicon valid in all browsers (Chrome, Firefox, Safari, Edge)

## Example Usage

**Prompt to Trigger This Skill:**
```
"Create a new React website with Advokatura branding using the standard icon"
"Setup favicon and metadata for the admin panel"
"Configure PWA manifest with our brand icon"
"Update website SEO with brand image for social sharing"
```

## Related Skills
- `frontend-design` - For full website creation
- `fullstack-design-backend-orchestrator` - For complete projects
- `impeccable` - For high-quality UI with consistent branding

## Brand Colors (Context)
```css
--primary-navy: #1a2a5a
--accent-gold: #B8973A
--secondary-blue: #2a4a7a
```

## Notes
- Always use HTTPS URL (`https://myweb.uz/icon.png`)
- Icon should be at least 512x512px for best quality
- Test icon on dark and light backgrounds
- Verify icon displays correctly on mobile devices
- Update all references if URL changes

## Version
Created: April 20, 2026  
Last Updated: April 20, 2026  
Applies To: All Advokatura Platform web projects
