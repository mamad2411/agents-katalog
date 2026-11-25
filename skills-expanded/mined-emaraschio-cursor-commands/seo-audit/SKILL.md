---
name: seo-audit
description: SEO audit of pages or app
user-invocable: false
---
## Overview

Conduct a comprehensive SEO audit to identify optimization opportunities, technical issues, and content gaps that impact search engine visibility and rankings. This audit evaluates technical infrastructure, on-page elements, content quality, off-page signals, and user experience factors to create an actionable roadmap for improving organic search performance.

The audit covers foundational technical requirements, content optimization, user experience signals, and modern SEO best practices including Core Web Vitals, structured data, and mobile-first considerations.

## Steps

1. **Technical SEO Foundation**
    - Verify HTTPS/SSL certificate is valid and properly configured
    - Validate robots.txt file structure and directives
    - Audit sitemap.xml for completeness and submission status
    - Check canonical URL implementation and duplicate content issues
    - Review site architecture, URL structure, and internal linking
    - Assess crawlability and indexability (check for blocked resources)
    - Verify site speed and Core Web Vitals metrics
    - Check for broken links and redirect chains
    - Validate structured data (JSON-LD, microdata, Schema.org)
    - Review international SEO elements (hreflang tags, if applicable)

2. **On-Page SEO Elements**
    - Audit title tags (uniqueness, length, keyword placement, brand consistency)
    - Review meta descriptions (compelling copy, length, call-to-action)
    - Evaluate header tag hierarchy (H1-H6 structure and keyword usage)
    - Check image optimization (alt tags, file names, compression, format)
    - Assess URL structure (readability, keyword inclusion, depth)
    - Review internal linking strategy and anchor text distribution
    - Verify breadcrumb navigation and schema markup
    - Check for duplicate or thin content issues

3. **Content Quality & Optimization**
    - Evaluate content quality, depth, and relevance to target audience
    - Assess keyword targeting and natural keyword integration
    - Review content length and comprehensiveness
    - Check content freshness and update frequency
    - Analyze content structure, readability, and user engagement signals
    - Identify content gaps and opportunities for expansion
    - Review content formatting (bullet points, headings, multimedia)
    - Assess E-A-T (Expertise, Authoritativeness, Trustworthiness) signals

4. **Keyword Research & Strategy**
    - Identify primary and secondary target keywords
    - Analyze search volume, competition, and intent for each keyword
    - Map keywords to specific pages and content
    - Research long-tail keyword opportunities
    - Identify keyword cannibalization issues
    - Review competitor keyword strategies
    - Assess semantic keyword coverage

5. **Mobile & User Experience**
    - Verify mobile-responsive design and viewport configuration
    - Test mobile usability and touch interactions
    - Review mobile page speed and Core Web Vitals on mobile devices
    - Check mobile-specific UX elements (navigation, forms, CTAs)
    - Assess accessibility (WCAG compliance, screen reader compatibility)
    - Review user engagement metrics (bounce rate, time on page, pages per session)

6. **Off-Page SEO & Authority**
    - Analyze backlink profile (quality, quantity, diversity, anchor text)
    - Review referring domains and link velocity
    - Assess domain authority and trust metrics
    - Check for toxic or spammy backlinks
    - Review social media presence and engagement
    - Evaluate brand mentions and unlinked citations
    - Assess content distribution and syndication strategies

7. **Local SEO** (if applicable)
    - Verify local business information (NAP consistency)
    - Review Google Business Profile optimization
    - Check local citations and directory listings
    - Assess local review management and response rate
    - Validate local schema markup (LocalBusiness, etc.)
    - Review location-specific content and landing pages

8. **Structured Data & Rich Snippets**
    - Audit JSON-LD schema implementation
    - Verify structured data with Google Rich Results Test
    - Review Open Graph meta tags for social sharing
    - Check Twitter Card implementation
    - Assess recipe, review, FAQ, and other relevant schema types
    - Verify entity markup and knowledge graph signals

9. **Analytics & Tracking**
    - Verify Google Analytics 4 implementation and event tracking
    - Check Google Search Console setup and data integrity
    - Review conversion tracking and goal configuration
    - Assess Google Tag Manager implementation
    - Verify search performance data (impressions, clicks, CTR, rankings)
    - Review user behavior and engagement analytics

10. **Performance & Core Web Vitals**
    - Measure Largest Contentful Paint (LCP)
    - Assess First Input Delay (FID) / Interaction to Next Paint (INP)
    - Evaluate Cumulative Layout Shift (CLS)
    - Review Time to First Byte (TTFB)
    - Check resource loading optimization (preload, prefetch, preconnect)
    - Assess image and asset optimization strategies
    - Review JavaScript and CSS delivery optimization

11. **Social Media & Brand Signals**
    - Review social media profile optimization
    - Assess social sharing optimization (Open Graph, Twitter Cards)
    - Check social media link implementation (rel="me" for verification)
    - Evaluate social engagement and brand mention tracking
    - Review social content strategy alignment with SEO goals

## Checklist

### Technical Foundation

- [ ] HTTPS/SSL certificate valid and properly configured
- [ ] robots.txt file optimized and tested
- [ ] XML sitemap created, validated, and submitted
- [ ] Canonical URLs properly implemented (no duplicate content)
- [ ] Site architecture and URL structure optimized
- [ ] Internal linking strategy implemented
- [ ] No broken links or excessive redirect chains
- [ ] Crawlability verified (no critical resources blocked)
- [ ] Structured data validated (JSON-LD/Schema.org)
- [ ] International SEO elements configured (hreflang, if needed)

### On-Page Elements

- [ ] Unique, optimized title tags on all pages
- [ ] Compelling meta descriptions (50-160 characters)
- [ ] Proper header tag hierarchy (H1-H6)
- [ ] Image alt tags and optimization complete
- [ ] Clean, keyword-rich URL structure
- [ ] Breadcrumb navigation implemented
- [ ] Internal linking optimized with descriptive anchor text

### Content & Keywords

- [ ] Keyword research completed and mapped to pages
- [ ] Content quality and depth optimized
- [ ] Target keywords naturally integrated
- [ ] Content gaps identified and addressed
- [ ] Content freshness maintained
- [ ] E-A-T signals strengthened
- [ ] Content formatting optimized for readability

### Mobile & UX

- [ ] Mobile-responsive design verified
- [ ] Mobile usability tested and optimized
- [ ] Core Web Vitals meet Google thresholds
- [ ] Accessibility standards met (WCAG compliance)
- [ ] User engagement metrics analyzed

### Performance

- [ ] LCP optimized (< 2.5s)
- [ ] FID/INP optimized (< 100ms)
- [ ] CLS minimized (< 0.1)
- [ ] TTFB optimized
- [ ] Resource hints implemented (preload, prefetch, preconnect)
- [ ] Images and assets optimized
- [ ] JavaScript and CSS delivery optimized

### Off-Page & Authority

- [ ] Backlink profile analyzed and cleaned
- [ ] Toxic backlinks disavowed (if needed)
- [ ] Social media presence optimized
- [ ] Brand mentions tracked
- [ ] Content distribution strategy implemented

### Local SEO (if applicable)

- [ ] NAP consistency verified across platforms
- [ ] Google Business Profile optimized
- [ ] Local citations built and verified
- [ ] Local reviews managed
- [ ] Local schema markup implemented

### Structured Data & Rich Results

- [ ] JSON-LD schemas implemented and validated
- [ ] Open Graph tags optimized
- [ ] Twitter Cards configured
- [ ] Rich snippets tested in Google Rich Results Test
- [ ] Entity markup verified

### Analytics & Tracking

- [ ] Google Analytics 4 configured with proper events
- [ ] Google Search Console verified and monitored
- [ ] Conversion tracking implemented
- [ ] Google Tag Manager properly configured
- [ ] Search performance data analyzed

### Social & Brand

- [ ] Social media profiles optimized
- [ ] Social sharing meta tags implemented
- [ ] Social verification links added (rel="me")
- [ ] Brand signal tracking configured

## Guardrails

- Recommend only white-hat tactics; do not recommend black-hat tactics.
- Ground every finding in a measurable check or observed metric; measure first.