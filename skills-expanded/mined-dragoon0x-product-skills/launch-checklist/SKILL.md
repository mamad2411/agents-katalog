---
name: launch-checklist
description: "Everything that needs to be true before real people see this. Pre-launch audit covering copy, meta tags, error states, mobile, performance, analytics, and the things everyone forgets. Use before any launch or public release."
---

# Launch Checklist

Everything that needs to be true before real people see this.

## How to use

- `/launch-checklist` Run a pre-launch audit against these constraints.

## Checklist

### Copy
- [ ] All placeholder/lorem ipsum text has been replaced
- [ ] Headlines communicate value, not just describe features
- [ ] CTA button text is specific and action-oriented
- [ ] Error messages are human-readable with recovery steps
- [ ] Empty states have helpful copy and clear next actions
- [ ] Legal pages exist: Terms, Privacy Policy, at minimum

### Technical
- [ ] Page loads in under 3 seconds on mobile 4G
- [ ] No console errors in production build
- [ ] Forms validate inline and preserve data on error
- [ ] All links work (no 404s, no placeholder hrefs)
- [ ] Favicon and app icons are set
- [ ] SSL certificate is active and valid

### SEO and Social
- [ ] Page titles are unique and descriptive (50-60 chars)
- [ ] Meta descriptions exist for all public pages (150-160 chars)
- [ ] Open Graph tags are set (title, description, image)
- [ ] Twitter Card tags are set
- [ ] Canonical URLs are configured
- [ ] Sitemap exists and is submitted

### Mobile
- [ ] All pages tested on actual mobile devices (not just responsive preview)
- [ ] Touch targets are at least 44x44px
- [ ] Forms are usable with mobile keyboards (correct input types)
- [ ] No horizontal scrolling on any viewport
- [ ] Text is readable without zooming

### Analytics
- [ ] Analytics tracking is installed and firing
- [ ] Key conversion events are tracked (signup, purchase, activation)
- [ ] Error events are logged
- [ ] UTM parameters are preserved through signup flow

### Post-Launch
- [ ] Monitoring/uptime alerts are configured
- [ ] Error reporting is active (Sentry or equivalent)
- [ ] Support channel exists and is reachable
- [ ] Backup and recovery process is documented and tested
