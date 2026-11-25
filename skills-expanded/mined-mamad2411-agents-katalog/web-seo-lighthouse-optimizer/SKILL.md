---
name: web-seo-lighthouse-optimizer
description: Guidelines for high-impact SEO, Schema.org JSON-LD structured data (Person, Physician, ScholarlyArticle), Open Graph metadata, and Google Lighthouse 100/100 performance optimization for personal & academic websites.
risk: safe
source: "antigravity-web-skills"
---

# Web SEO & Lighthouse Optimization Skill

## Overview
This skill defines standards for maximizing search visibility, social media preview quality, and Lighthouse performance scores for `bakralhayek.com`.

## SEO & Metadata Requirements

### 1. Title & Meta Tags (`index.html`)
- Page Title: `Bakr Alhayek, MD | Physician, Researcher & Academic Leader`
- Meta Description: Clear, concise summary of clinical expertise, research focus, internal medicine, and digital health initiatives.
- Canonical Tag: `<link rel="canonical" href="https://bakralhayek.com/" />`

### 2. Social Media Sharing (Open Graph & Twitter Cards)
- `og:title`, `og:description`, `og:image`, `og:url`, `og:type` (`website`)
- `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image`

### 3. Schema.org JSON-LD (Physician & Medical Researcher)
Embed structured JSON-LD in `index.html` or dynamic React script tag:
```json
{
  "@context": "https://schema.org",
  "@type": "Physician",
  "name": "Bakr Alhayek, MD",
  "url": "https://bakralhayek.com",
  "medicalSpecialty": ["InternalMedicine", "MedicalOncology"],
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "University of Miami"
  },
  "sameAs": [
    "https://github.com/alhayekbakr1-cell",
    "https://scholar.google.com"
  ]
}
```

### 4. Lighthouse Performance Optimization
- **First Contentful Paint (FCP)** < 1.0s
- **Largest Contentful Paint (LCP)** < 2.0s
- **Cumulative Layout Shift (CLS)** < 0.05
- Use system font fallbacks or preloaded Google Fonts.
- Preconnect to necessary third-party domains (e.g., Google Fonts, Analytics).

### 5. XML Sitemap & Robots.txt
- Maintain `public/sitemap.xml` listing main routes.
- Maintain `public/robots.txt` allowing search engines to index primary pages.
