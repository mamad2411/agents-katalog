---
name: web-template-rebrander
description: Automatically rebrand any web template to RJ Business Solutions (or custom brand) while preserving all functionality. Fast changeovers for React, Next.js, HTML, Vue, and vanilla JS templates.
allowed-tools: Read Write Edit MultiEdit Bash Glob Grep
disable-model-invocation: false
---

# Web Template Rebrander Skill

## PURPOSE
Transform ANY web template to **RJ Business Solutions** branding by default. Preserves all functionality while replacing logos, colors, typography, company info, contact details, copyright, meta tags, and SEO data.

## DEFAULT BRAND: RJ Business Solutions
Unless user specifies otherwise, ALL rebranding uses:
- **Company**: RJ Business Solutions
- **Founder**: Rick Jefferson
- **Website**: https://rjbusinesssolutions.org
- **Email**: support@rjbusinesssolutions.org
- **Logo**: https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg

## QUICK START COMMANDS

```bash
# Full rebrand to RJ Business Solutions (default)
/rebrand

# Rebrand with custom brand
/rebrand --brand "Custom Company Name"

# Preview changes before applying
/rebrand --preview

# Rebrand specific files only
/rebrand --files "src/components/Header.tsx,src/components/Footer.tsx"
```

## REBRANDING CHECKLIST (Execute in Order)

### Phase 1: Discovery
1. Identify framework (React/Next.js/Vue/HTML/vanilla)
2. Locate all brand touchpoints:
   - Logo imports/references
   - Company name strings
   - Color definitions (CSS vars, Tailwind config, inline)
   - Font definitions
   - Contact info (email, phone, address)
   - Social links
   - Copyright notices
   - Meta tags (title, description, OG tags)
   - manifest.json / PWA config
   - Schema markup (JSON-LD)

### Phase 2: Asset Replacement
1. Replace logo files or update logo import paths
2. Update favicon
3. Update OG images

### Phase 3: Code Transformation
1. Update CSS variables / Tailwind colors
2. Replace hardcoded company names
3. Update contact information
4. Update social media links
5. Update copyright year and company
6. Update meta tags
7. Update JSON-LD schema
8. Update manifest.json

### Phase 4: Verification
1. Grep for old brand references
2. Verify no broken imports
3. Check all links resolve

## FILE PATTERNS TO SEARCH

```bash
# Find all brand touchpoints
grep -rn "Aivora\|AIVORA\|aivora" --include="*.{tsx,ts,jsx,js,css,scss,html,json,md}"
grep -rn "logo\|Logo\|LOGO" --include="*.{tsx,ts,jsx,js}"
grep -rn "copyright\|Copyright\|©" --include="*.{tsx,ts,jsx,js,html}"
grep -rn "@.*\.com\|@.*\.org" --include="*.{tsx,ts,jsx,js,html,json}"
grep -rn "tel:\|phone\|Phone" --include="*.{tsx,ts,jsx,js,html}"
```

## BRAND KIT REFERENCE
See `${CLAUDE_SKILL_DIR}/brands/rj-business-solutions.md` for complete brand assets.

## TRANSFORMATION TEMPLATES
- CSS Variables: `${CLAUDE_SKILL_DIR}/templates/css-variables.css`
- Meta Tags: `${CLAUDE_SKILL_DIR}/templates/meta-tags.html`
- Footer Component: `${CLAUDE_SKILL_DIR}/templates/footer-template.tsx`
- Header Component: `${CLAUDE_SKILL_DIR}/templates/header-template.tsx`
- JSON-LD Schema: `${CLAUDE_SKILL_DIR}/templates/schema-jsonld.json`
- Manifest: `${CLAUDE_SKILL_DIR}/templates/manifest.json`

## FRAMEWORK-SPECIFIC GUIDES
- React/Next.js: `${CLAUDE_SKILL_DIR}/guides/react-nextjs.md`
- Vue/Nuxt: `${CLAUDE_SKILL_DIR}/guides/vue-nuxt.md`
- HTML/Vanilla: `${CLAUDE_SKILL_DIR}/guides/html-vanilla.md`

## IMPORTANT RULES
1. NEVER break existing functionality
2. ALWAYS preserve component structure
3. ALWAYS backup before major changes
4. VERIFY no old brand references remain
5. UPDATE copyright year to current year
6. MAINTAIN responsive behavior
7. PRESERVE animation/transition code
