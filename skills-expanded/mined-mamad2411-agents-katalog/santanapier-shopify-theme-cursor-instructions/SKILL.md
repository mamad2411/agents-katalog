# SantanaPier Shopify Theme - AI Assistant Instructions

## Project Overview

This is a custom Shopify theme for SantanaPier ecommerce store, built with modern web technologies and focused on toys with plans to expand into other niches.

## Tech Stack

- **Platform**: Shopify (Liquid templating)
- **Frontend**: TypeScript + Vite build system
- **Styling**: Tailwind CSS + PostCSS
- **JavaScript**: Vanilla ES6+ (no frameworks)
- **Deployment**: GitHub Actions + Shopify CLI

## Project Structure

```
santanapier-shopify-theme/
├── assets/                 # Compiled CSS and JS (auto-generated)
├── config/                 # Theme settings and schema
├── layout/                 # Base theme layout
├── locales/               # Translation files
├── sections/              # Reusable sections
├── snippets/              # Reusable code blocks
├── templates/             # Page templates
├── src/                   # TypeScript source files
│   └── assets/           # TypeScript modules
├── .cursor/              # AI assistant instructions
├── .github/              # GitHub Actions workflows
└── santanapier-shopify-theme.plan.md  # Complete development plan
```

## Key Features to Implement

- Multi-level collection architecture (Toys, Horror, Hotwheels, Holidays)
- Advanced filtering and sorting
- Predictive search with real-time suggestions
- Cart drawer for quick checkout
- Mobile-first responsive design
- WCAG 2.1 accessibility compliance
- SEO optimization with structured data
- Payment method support (Credit Card, PayPal, Venmo, Apple Pay, Google Pay)

## Development Guidelines

### Code Style

- Use TypeScript for all JavaScript functionality
- Follow Shopify Liquid best practices
- Use Tailwind CSS utility classes for styling
- Write semantic HTML with proper ARIA labels
- Include comprehensive comments for complex logic

### File Naming

- Use kebab-case for Liquid files
- Use camelCase for TypeScript files
- Use descriptive names that indicate purpose

### Accessibility Requirements

- All interactive elements must be keyboard accessible
- Proper ARIA labels and roles
- Color contrast meets WCAG 2.1 AA standards
- Screen reader friendly navigation
- Skip links for main content

### Performance Requirements

- Lazy load images and non-critical resources
- Minimize JavaScript bundle size
- Use responsive images with srcset
- Optimize for Core Web Vitals
- Target 90+ Lighthouse scores

## Collection Architecture

The theme supports a specific collection hierarchy:

1. **Top-level Collections** (e.g., Toys, Horror, Hotwheels)

   - Landing page template: `collection.{name}-landing.json`
   - All products template: `collection.{name}-all.json`
   - Subcollection template: `collection.{name}-subcollection.json`

2. **Special Collections**
   - All products: `collection.all.json` (with advanced filtering)
   - Holidays: Thanksgiving, Christmas, Mother's Day, Father's Day, 4th of July

## Current Status

- ✅ Theme foundation and structure
- ✅ TypeScript + Vite + Tailwind setup
- ✅ Core layout with SEO and accessibility
- ✅ Header and footer sections
- ✅ Essential snippets (product-card, icons, breadcrumbs, pagination)
- ✅ Homepage template with hero slider
- ✅ TypeScript modules for core functionality
- ✅ GitHub Actions deployment workflow
- ✅ Documentation (README, requirements)

## Next Priority Items

1. Collection templates (toys-landing, toys-all, subcollections)
2. Product detail page with gallery and variants
3. Cart page functionality
4. Additional sections (newsletter, announcement bar)
5. Final testing and polish

## Important Notes

- All sales are final (configurable in theme settings)
- Focus on conversion optimization
- Mobile-first approach is critical
- Maintain consistency with brand guidelines
- Test across all major browsers and devices

## Reference Files

- `docs/santanapier-shopify-theme.plan.md` - Complete development plan
- `docs/REQUIREMENTS.md` - Detailed requirements document
- `context/project-overview.md` - Quick project reference
- `context/tech-specs.md` - Technical specifications
- `README.md` - Setup and usage instructions

## When Making Changes

1. Always test on mobile devices
2. Ensure accessibility compliance
3. Update TypeScript types if needed
4. Run `npm run build` before deployment
5. Update documentation if adding new features
6. Follow the established file structure

## Common Commands

```bash
npm run build          # Build TypeScript and Tailwind
npm run dev            # Development mode
npm run shopify:deploy # Deploy to Shopify
npm run shopify:dev    # Development server
```
