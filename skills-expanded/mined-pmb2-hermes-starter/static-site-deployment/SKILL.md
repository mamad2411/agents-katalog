---
name: static-site-deployment
description: "Deploy a static site (HTML/CSS/JS) to GitHub Pages with custom domain — single-file collapse, asset optimization, SEO setup, DNS configuration, and verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [static-site, github-pages, deployment, dns, seo, web]
    triggers: [deploy-static-site, github-pages-setup, custom-domain-dns, namecheap-dns-github-pages, single-file-html-refactor, webp-image-optimization, static-site-launch, site-to-github-pages, collapse-to-single-file]
    related_skills: [vps-application-deployment]
---

# Static Site Deployment (GitHub Pages + Custom Domain)

Standardized procedure for taking a static site (or existing multi-file site) and deploying it to GitHub Pages with a custom domain, optimized assets, and SEO metadata.

## 🔑 Core Principles

### When to use (vs VPS deployment)

| Factor | Single Static Site (this skill) | Mass Deployment (200+ sites) | VPS (vps-application-deployment) |
|--------|-------------------------------|------------------------------|----------------------------------|
| Backend | None / client-side JS only | None — pure static HTML | Server-side runtime (Node, Python, etc.) |
| Hosting | GitHub Pages (free) | Cloudflare Pages / Cheap VPS + nginx | Docker + Caddy on cloud VPS |
| URL pattern | `yourdomain.com` | `yourdomain.com/{niche}/{slug}/` | Separate subdomains or ports |
| Deployment | `git push` | Bulk upload / wrangler / nginx conf | SSH + docker compose |
| Cost | $0 | $0 (Cloudflare) / ~$6/mo (VPS) | ~$6/mo (Oracle free tier) |
| SSL | Auto (GitHub) | Auto (Cloudflare) | Auto (Caddy/LetsEncrypt) |

### Mass Deployment (200+ Sites Under One Domain)

When deploying multiple business websites under a single domain (e.g., for the operator's local website business):

**For the operator's Website Landlord (your-domain.example DNS must not be touched):**
Cloudflare Pages is NOT available. Use GitHub Pages against the `project-sites` repo:
1. Push built dist/ to `preview-sites/<slug>/` in `pmb2/project-sites`
2. Make repo public (required for GitHub Free Pages)
3. Enable Pages → Deploy from main → / (root)
4. Each site at: `https://your-username.github.io/project-sites/preview-sites/<slug>/`

| Option | Cost | Setup Time | URL Pattern | Tradeoffs |\n|--------|------|------------|-------------|-----------|\n| **GitHub Pages** | FREE | 30 min | `user.github.io/repo/sites/site-name` | 1GB limit; 10 builds/hr; must be public |\n| **Cloudflare Pages** | FREE | 15 min | `domain.com/plumber/bass-plumbing` | 500 builds/mo; **requires DNS change** |\n| **Cheap VPS + nginx** | ~$6/mo | 20 min | `domain.com/bass-plumbing` | Full control, no limits; needs server mgmt |\n| **Netlify** | FREE | 15 min | `domain.com/bass-plumbing` | 100GB bandwidth; easy deploy |

**Recommended: Cloudflare Pages** — API token and Zone ID typically pre-configured. A single Pages project serves all sites under one domain:

```
yourdomain.com/plumber/bass-plumbing/        → all 200+ sites
yourdomain.com/electrician/capital-electric/ → instantly accessible
```

Deploy from the website-landlord repo:
```bash
# Collect all generated site dist/ folders
# Upload each to Cloudflare Pages at the correct subdirectory path
# Each site accessible via short link for text messaging

# Via wrangler CLI (one project approach):
wrangler pages project create business-sites
wrangler pages deploy astro-sites/generated/<slug>/dist \
  --project-name business-sites \
  --branch main \
  --directory <slug>
```

### Deployment Flow (summary)

```
Audit → Optimize → Simplify → SEO → Deploy → DNS → Verify
```

---

## 📋 Full Workflow

### Phase 1: Site Audit

1. **Check existing structure:** How many files? Build step? Dependencies?
2. **Assess if single-file collapse is appropriate:**
   - Site is 1-3 pages → collapse to single `index.html` (Option 1)
   - Site will grow to 5+ pages or add a CMS → use Astro or 11ty (Option 3)
   - Site needs utility-first styling → use Tailwind (Option 2)
   - See `HECS-ENHANCEMENT-REPORT.md` for the full comparison matrix
3. **Check for external dependencies:** Google Fonts, analytics, CDN libs

**Key question:** Does the user want simplicity NOW (collapse) or a foundation for growth (framework)? Ask or infer from context. Users who say "simplify/modernize" and "less code" lean toward collapse.

### Phase 2: Image Optimization

Convert all raster images to WebP for 40-80% file size savings:

```bash
# Banner/hero images: quality 80, lossy
ffmpeg -i input.png -q:v 80 -compression_level 6 output.webp -y

# Logo/icons: quality 85 (preserve crisp edges)
ffmpeg -i input.png -q:v 85 -compression_level 6 output.webp -y
```

**HTML integration — use `<picture>` for WebP + PNG fallback:**
```html
<picture>
  <source srcset="assets/banner.webp" type="image/webp" />
  <img src="assets/banner.png" alt="" class="hero-bg" aria-hidden="true" />
</picture>
```

**⚠️ Pitfall: ffmpeg outputs animated WebP for single frames** — Add `-frames:v 1` if you need a truly static WebP. The output file will still display correctly either way.

### Phase 3: Single-File Collapse

When collapsing an existing multi-file HTML/CSS/JS site into one file:

| Before | After |
|--------|-------|
| 3+ files (html + css + js) | 1 file (`index.html`) |
| External CSS `<link>` | Inline `<style>` in `<head>` |
| External JS `<script src>` | Inline `<script>` before `</body>` |
| ~970+ total code lines | ~400-500 lines (minified CSS + compact JS) |

**CSS compression techniques:**
- Use CSS custom properties (`:root{...}`) for repeated values
- Combine short selectors on one line: `.a,.b{...}.c,.d{...}`
- Use shorthand properties: `margin:0 auto`, `padding:.85rem 2.2rem`
- Remove redundant prefixes (autoprefixer not needed for modern browsers targeting GH Pages)
- Single-line rule bodies: `.class{prop:val;prop:val}`

**JS compression techniques:**
- Short variable names for DOM refs: `const h=document.getElementById('hamburger')`
- Chain ternary expressions: `header.style.background=scroll>100?'rgba(...)':'rgba(...)'`
- Remove unused variables (e.g., `lastScroll` tracking var that's never read)
- Use `&&` chaining instead of `if` blocks for simple guard clauses

**⚠️ Pitfall — Event listener references in single-file JS:** When minifying JS variable names, ensure both the variable declaration and the event listener reference use the same name. Test by clicking all interactive elements after refactoring.

**⚠️ Pitfall — CSS `background-*` properties do NOT work on `<img>` elements:** A very common mistake is applying `background-size: cover` or `background-position: center` to an `<img>` tag. These are CSS *background* properties that only affect elements with a CSS `background-image`. For `<img>` tags, use `object-fit` instead:

```css
/* ❌ WRONG — does nothing on <img> */
.hero-bg {
  background-size: cover;
  background-position: center;
}

/* ✅ CORRECT — scales the <img> content properly */
.hero-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
```

This is especially tricky with `<picture>` elements, where the `<img>` inside is what renders — the `<picture>` wrapper is just a source selector and has no dimensions of its own. Always pair `object-fit` with explicit `width` + `height` on the `<img>`.

**⚠️ Pitfall — Decorative hero images should be `aria-hidden="true"`:** When an image is purely decorative (hero backgrounds, abstract visuals), add `aria-hidden="true"` to the `<img>` and empty `alt=""` so screen readers skip it. The `<picture>` wrapper does not need ARIA attributes — apply them to the `<img>`.

### Phase 4: SEO & Social Metadata

Add these to `<head>`:

**Open Graph tags (social share cards):**
```html
<meta property="og:title" content="Your Site Name" />
<meta property="og:description" content="Your tagline." />
<meta property="og:url" content="https://yourdomain.com" />
<meta property="og:type" content="website" />
<meta property="og:image" content="https://yourdomain.com/assets/banner.webp" />
<meta property="og:image:width" content="1180" />
<meta property="og:image:height" content="587" />
```

**JSON-LD structured data (Google rich results):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://yourdomain.com/assets/logo.webp",
  "url": "https://yourdomain.com",
  "description": "...",
  "address": { "@type": "PostalAddress", ... },
  "telephone": "...",
  "email": "...",
  "priceRange": "$$$"
}
</script>
```

⚠️ **Important:** Use the domain URL in OG/JSON-LD URLs, not the GitHub Pages URL. Hardcode the final domain so social previews work immediately after DNS resolves.

### Phase 5: Repo Visibility Check (before enabling Pages)

**GitHub Free plan only supports Pages on PUBLIC repos.** Check before attempting to enable:

```bash
gh repo view <owner>/<repo> --json visibility,name
# Expected: {"visibility":"PUBLIC",...}
```

If the repo is private, you have two options:
1. **Make it public** (recommended if it's a public-facing site): `gh repo edit <owner>/<repo> --visibility public`
2. **Use an alternative host** (Cloudflare Pages, Netlify — both have free tiers that work with private repos)

The API will return `422: Your current plan does not support GitHub Pages for this repository.` if the repo is private.

### Phase 6: GitHub Pages Enablement

**Option A — via repo Settings UI:**
1. Go to repo → Settings → Pages
2. Source: **Deploy from a branch** → Branch: `main` → folder: `/` (root)
3. Click Save

**Option B — via API (useful when UI is inaccessible):**
```bash
export MSYS_NO_PATHCONV=1
gh api -X POST repos/<owner>/<repo>/pages \
  -f source[branch]=main -f source[path]=/
```

After enabling, poll for build completion:
```bash
# Wait for build (usually 15-60 seconds)
# Status transitions: "building" → "built"
gh api repos/<owner>/<repo>/pages --jq '.status'
```

**⚠️ CNAME TIMING PITFALL — CRITICAL**

Do NOT add the `CNAME` file to the repo until DNS has propagated to the GitHub IPs. Here's what happens:

| Scenario | CNAME present? | DNS set up? | Result |
|---|---|---|---|
| ✅ Correct | No (or not yet) | No | Site works at `https://<user>.github.io/<repo>/` |
| ❌ Wrong | Yes | No | **Site 404s everywhere** — GH Pages only serves at custom domain, which doesn't resolve |
| ✅ Correct | Yes | Yes | Site works at `https://yourdomain.com/` |

**The workflow is:**
1. Build and deploy your site to GH Pages (no CNAME file)
2. Verify site works at `https://<user>.github.io/<repo>/`
3. User sets up DNS at their registrar
4. Verify DNS resolves (e.g., `nslookup yourdomain.com` returns GitHub IPs)
5. **Then** add the CNAME file and push
6. Verify site at `https://yourdomain.com/`

If you accidentally add CNAME before DNS (site goes 404), the fix is: **remove the CNAME file**, push, wait for rebuild, and verify the default URL works again. Then re-add CNAME after DNS verification.

### Phase 7: DNS Configuration

See `references/namecheap-github-pages.md` for Namecheap-specific steps.

**Generic DNS requirements for GitHub Pages:**

| Type | Host | Value |
|------|------|-------|
| A | `@` (apex) | `185.199.108.153` |
| A | `@` (apex) | `185.199.109.153` |
| A | `@` (apex) | `185.199.110.153` |
| A | `@` (apex) | `185.199.111.153` |
| CNAME | `www` | `<user>.github.io` |

**⚠️ Pitfall — All 4 A records are required:** GitHub uses all 4 IPs for CDN redundancy. Missing one makes the site intermittently unreachable.

**⚠️ Pitfall — Delete old parking/placeholder records:** The registrar's default A record (e.g., Namecheap's `162.255.119.240` parking page) must be deleted, or it will override the new records.

**Post-DNS steps:**
1. Go to repo Settings → Pages
2. Verify custom domain shows a green checkmark
3. Check **"Enforce HTTPS"** — GitHub auto-provisions a Let's Encrypt certificate (takes 5-30 min after DNS resolves)

### Phase 8: Verification

```bash
# DNS resolution (should return GitHub IPs)
nslookup yourdomain.com

# Site accessible
curl -sI https://yourdomain.com | head -5

# www redirects (GitHub Pages handles this automatically)
curl -sI https://www.yourdomain.com | head -5

# HTTPS enabled (should show a 200 or redirect to HTTPS)
curl -sI http://yourdomain.com | head -5
```

**Valid responses:**
- `HTTP/2 200` — site is live
- `HTTP/2 301` or `302` — redirect to HTTPS (expected for HTTP)
- `curl: (6) Could not resolve host` — DNS not propagated yet
- `curl: (7) Failed to connect` — DNS resolved but GH Pages not configured
- `curl: (35) SSL connect error` — HTTPS not provisioned yet, wait 5-30 min

**Browser-based image verification (deeper check than curl alone):**

After curl confirms the page loads, use the browser tools to verify images actually render:

```javascript
// Check all images are loaded and have real dimensions
[...document.querySelectorAll('img')].map(i => ({
  src: i.currentSrc || i.src,
  naturalWidth: i.naturalWidth,
  naturalHeight: i.naturalHeight,
  complete: i.complete,
  alt: i.alt
}))
// Expected: all "complete: true", none have "naturalWidth: 0"

// Check for JS errors
// Browser console should show 0 errors, 0 warnings

// Check the total image count matches expectations
document.querySelectorAll('img').length
```

**What each check catches:**
| Issue | curl detects | browser console detects |
|---|---|---|
| Page returns 404 | ✅ | ✅ (same) |
| Broken image URL (server returns 404) | ✅ | ✅ |
| Image loads but CSS hides it | ❌ | ✅ (`naturalWidth: 0`) |
| Image has no dimensions (broken `<img>` CSS) | ❌ | ✅ (`naturalWidth: 0` despite `complete: true`) |
| Console JS errors breaking interactivity | ❌ | ✅ |
| `<picture>` source mismatches | ❌ | ✅ (wrong `currentSrc`) |

**Run the companion script for automated verification:**
```bash
python scripts/verify-deployment.py yourdomain.com
```
This runs curl checks + image reference validation in one pass.

**⚠️ Local DNS cache often lags behind global propagation.** Even if `nslookup yourdomain.com 8.8.8.8` shows the correct GitHub IPs, your local machine may still resolve the old parking IP for hours. Fix:

```bash
# Windows
ipconfig /flushdns

# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Linux
sudo resolvectl flush-caches   # systemd-resolved
# or
sudo systemctl restart nscd    # nscd cache
```

After flushing, re-verify with `curl -I http://yourdomain.com`. If it still shows the old IP, use `--resolve` to bypass the local resolver entirely and force a connection to the correct GitHub IP:

```bash
# Bypass local DNS cache — connect directly to a known GitHub Pages IP
curl --resolve "yourdomain.com:80:185.199.108.153" -sI "http://yourdomain.com/"

# Expected: HTTP/2 200 with Server: GitHub.com
# If this works but the bare curl doesn't, the issue is DEFINITELY local DNS cache, not global propagation
```

**Debug flow when the site seems down:**
1. `nslookup yourdomain.com 8.8.8.8` → check global DNS (Google's resolver)
2. `curl --resolve "yourdomain.com:80:185.199.108.153" -sI "http://yourdomain.com/"` → force-connect to GitHub
3. If both pass → it's a local DNS cache issue → flush and retry
4. If global DNS shows old IPs → wait for propagation (registrar makes changes visible within 5-30 min typically)

### Phase 9: Domain Setup Guide

Write a `DOMAIN-SETUP.md` file with registrar-specific instructions. The user will handle DNS if they control the registrar. The guide must be:

- **Registrar-specific**: Don't say "your DNS provider" — name the exact registrar (Namecheap, GoDaddy, Cloudflare, etc.)
- **Step-by-step with UI labels**: "Click Advanced DNS tab (near the top of the page)"
- **Exact record types**: "Select 'A + Dynamic DNS' from the Type dropdown" (not just "add A record")
- **Include the delete step**: Explicitly tell them which record to delete
- **Troubleshooting section**: What to check when it doesn't work

**Section structure:**
```
# Domain Setup Guide — <Registrar Name>

## Step 1: Log in and find Domain List
## Step 2: Open Advanced DNS
## Step 3: Delete old [parking/placeholder] record
## Step 4: Add [N] new [record type] records
## Step 5: Add CNAME for www
## Step 6: Save and verify
## What I've done on my side
## Troubleshooting
```

---

## 🔁 Parallel Execution Within This Workflow

Deploy tools are sequential (DNS must wait for GH Pages, push must wait for code) but within a single site build:

| Can parallelize | Must be sequential |
|-----------------|-------------------|
| Image conversion + code refactor | DNS config → site is live |
| OG tag authoring + JSON-LD authoring | GH Pages enable → CNAME verification |
| CNAME file creation + .gitignore updates | Push → DNS propagation → verify |

---

## 📦 Key References

- See `references/namecheap-github-pages.md` for Namecheap-specific DNS setup for GitHub Pages
- See `HECS-ENHANCEMENT-REPORT.md` in the site repo for the full single-file vs framework comparison matrix

## 🔍 Troubleshooting

### "Domain not configured" in GitHub Pages
- CNAME file must be exactly `yourdomain.com` (no www, no https://, no trailing slash, no blank lines)
- DNS hasn't propagated — check `nslookup yourdomain.com`
- Wait 5-30 min after DNS changes

### Site loads but no HTTPS
- GitHub Pages auto-provisions Let's Encrypt; takes up to 30 min after first DNS detection
- "Enforce HTTPS" must be checked in repo Settings → Pages
- You may need to uncheck/recheck "Enforce HTTPS" to trigger certificate issuance

### Site 404s after adding CNAME (before DNS setup)
- **Root cause:** CNAME file disables the default `https://<user>.github.io/<repo>/` URL but the custom domain hasn't propagated yet
- **Fix:** Remove the `CNAME` file from the repo, push, wait for rebuild, and verify the default URL works again

### www subdomain doesn't work
- CNAME for `www` must point to `<user>.github.io` (not to `yourdomain.com`)
- GitHub Pages auto-redirects `www` → apex; no extra config needed

### Repo is private — can't enable Pages
- GitHub Free plan only supports Pages on public repos
- The API returns `422: Your current plan does not support GitHub Pages for this repository`
- Fix: `gh repo edit <owner>/<repo> --visibility public` (then re-enable Pages)
- Alternative: use Cloudflare Pages or Netlify (free tiers, support private repos)
