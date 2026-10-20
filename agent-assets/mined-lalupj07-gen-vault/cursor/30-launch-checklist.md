---
description: Pre-launch requirements for every site
globs: "**/*"
alwaysApply: false
---

# Launch Checklist

Every site MUST meet all of these before launch:

- MUST have a custom domain configured with HTTPS. Never ship on a default `*.vercel.app`, `*.netlify.app`, or builder subdomain. Reference the domain in the canonical URL and sitemap.
- MUST have a favicon set: `favicon.ico`, `apple-touch-icon.png` (180x180), and web manifest icons (192 and 512), all linked in the document head.
- MUST remove any "Made with AI", "Built with [tool]" badge, watermark, or injected tag from the code and the deploy platform settings.
- MUST have a Privacy Policy page at `/privacy`, linked from the footer.
- MUST have a Terms and Conditions page at `/terms`, linked from the footer.
- MUST have a meta title, meta description, and Open Graph image on every page.
- MUST contain no lorem ipsum or placeholder text in production.
