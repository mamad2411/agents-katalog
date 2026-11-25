---
name: seo
description: >-
  SEO, social sharing metadata, sitemap/robots, heading/keyword structure,
  analytics attribution (gclid, utm_*), and Lighthouse performance — primarily
  public marketing surfaces. Use when building or reviewing metadata or
  analytics hooks.
---

# SEO & Growth Tracking

**Primary focus:** public **landing / marketing pages** — maximize organic and paid reach. Secondary: shareable metadata on other **public** routes. **Do not index** authenticated, wizard, results, or admin flows unless product policy says otherwise.

Also read: marketing/copy docs when present, `.agents/skills/ux-ui-review/SKILL.md` (headings overlap), and optional Next.js skill if applicable.

---

## Scope by route (adapt to your app)

| Route type                     | Index?  | SEO priority           |
| ------------------------------ | ------- | ---------------------- |
| Marketing / landing            | **Yes** | **High**               |
| Trust pages (privacy, terms)   | Yes     | Medium                 |
| Multi-step wizards / app flows | **No**  | Low — `noindex`        |
| Private results / user data    | **No**  | None                   |
| Admin                          | **No**  | None — block in robots |

---

## Metadata

Use your framework’s metadata API (e.g. Next.js Metadata API) or equivalent.

### Required on primary landing

| Field                      | Rule                                                    |
| -------------------------- | ------------------------------------------------------- |
| `<title>`                  | Unique, ≤60 chars; primary keyword + brand              |
| `description`              | 150–160 chars; value prop + CTA hint                    |
| `metadataBase` / canonical | Production site URL from env                            |
| `openGraph`                | title, description, url, siteName, locale, type, images |
| `twitter.card`             | `summary_large_image`; match OG                         |
| `robots`                   | `index, follow` on public marketing only                |

OG image: typically 1200×630 — coordinate with `/visual-designer` and `seo` / `visual-design` skills.

---

## Sitemap & robots

- Sitemap: include public marketing/trust URLs only.
- Robots: allow public; disallow admin, private, and funnel steps.
- Use a single site URL env var for absolute links.

---

## On-page SEO

- One **`h1`** per page; logical `h2`/`h3` hierarchy; do not skip levels.
- Keywords used naturally — **no stuffing**.
- Primary CTA as visible control with descriptive text (not “Click here”).
- Images: descriptive `alt` when informative.

---

## Analytics & attribution

- Load analytics container ID from env — **never hardcode**.
- Capture marketing query params on first entry (`utm_*`, `gclid`, etc.) into session storage; attach to events and relevant API payloads.
- Never log raw PII in the data layer.
- Gate third-party scripts behind consent when a CMP exists.

Recommended events (adapt names): `page_view`, `cta_click`, funnel start/complete events with opaque IDs only.

---

## Lighthouse & Core Web Vitals

Target primary landing (mobile + desktop): Performance / Accessibility / Best Practices ≥ 90; SEO ≥ 95 when practical.

Tactics: minimize client JS on marketing pages; optimized images; deferred analytics; avoid layout shift.

---

## Review self-check (landing changes)

- [ ] title, description, OG, Twitter set and locale-accurate
- [ ] OG image exists and resolves (1200×630)
- [ ] sitemap and robots correct
- [ ] Single `h1`; logical heading hierarchy
- [ ] Private/admin/funnel routes `noindex`
- [ ] Attribution captured on entry; key events fire
- [ ] Site URL and analytics IDs documented in `.env.example`
