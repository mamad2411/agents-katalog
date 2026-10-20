<!-- agent-notes: { ctx: "static site scaffold for GitHub Pages", deps: [CLAUDE.md], state: active, last: "sato@2026-02-12" } -->
Scaffold a static site for GitHub Pages: $ARGUMENTS

You are setting up this repository as a static website suitable for GitHub Pages hosting. Follow these steps:

## 0. Template Setup

Swap the storefront README for the project placeholder, move scaffolds into place, and clean up template-only files:

```bash
# Swap README: replace storefront with project placeholder
if [ -f README-template.md ]; then
  mv README-template.md README.md
fi

# Move stub docs from scaffolds/ to docs/ root
mv docs/scaffolds/*.md docs/ 2>/dev/null
rmdir docs/scaffolds 2>/dev/null

# Remove samples directory (only useful on the template repo itself)
rm -rf samples/ 2>/dev/null

# Remove template-specific ADRs (not relevant to inheriting projects)
rm -rf docs/adrs/template/

# Remove template research/comparison docs
rm -f docs/research/how-we-compare-*.md docs/research/agent-teams-comparison.md
rm -f docs/research/squad-vs-vteam-*.md docs/research/ux-gap-analysis-*.md
rm -f docs/research/what-*-can-learn-from-*.md docs/research/what-we-learn-from-*.md
```

## 1. Gather Requirements

Ask the user to choose their tech stack. Present these options:

**Site generator / framework:**
- **Astro** — Fast, content-focused, supports multiple UI frameworks, great for static (Recommended)
- **Next.js (static export)** — React-based, use `output: 'export'` for static HTML
- **Vite + vanilla/React/Svelte** — Lightweight SPA or multi-page, fast dev
- **Hugo** — Go-based, extremely fast builds, great for blogs/docs (no JS build step)
- **Eleventy (11ty)** — Simple, flexible, JS-based static site generator
- **Plain HTML/CSS/JS** — No build step, maximum simplicity
- **Other** — Let the user specify

**Styling:**
- **Tailwind CSS** (Recommended for most frameworks)
- **Plain CSS / CSS Modules**
- **SCSS/Sass**
- **Other**

**Content authoring (if content-heavy site):**
- **Markdown / MDX** (Recommended)
- **CMS integration** (headless CMS like Sanity, Contentful, etc.)
- **HTML only**

**Additional options to ask about:**
- Is this a blog, docs site, portfolio, landing page, or app?
- Do they want a custom domain? (affects CNAME setup)
- Do they want analytics? (Plausible, Umami, or none)
- CI/CD via GitHub Actions for automated deploy?
- Do they want development previews (e.g., PR previews)?

## 2. Create an ADR

Once choices are made, create an ADR at `docs/adrs/` documenting:
- The chosen framework and tooling
- Why these were selected
- Hosting constraints (GitHub Pages: static only, single repo, custom domain optional)

## 3. Scaffold the Project

Based on the choices, create the project structure appropriate to the framework.

### In all cases, also:
- Update `CLAUDE.md` with the chosen tech stack, how to dev/build/deploy, and conventions
- Update `README.md` with project description and setup instructions
- Add a `.gitignore` appropriate for the toolchain
- Create `.github/workflows/deploy.yml` for GitHub Pages deployment
- Include a starter page with minimal content so the site works immediately
- Configure the build output directory to match GitHub Pages expectations
- If custom domain requested, set up `CNAME` file in the public/static directory
- Add a starter test if the framework supports it
- Add agent-notes to all new files per `docs/methodology/agent-notes.md`

## 4. Verify

Install dependencies (if applicable), run the build, and confirm the output directory is generated correctly. Fix any issues.

## 5. Summary

Tell the user what was created and the key commands:
- How to install dependencies (if applicable)
- How to run the dev server
- How to build for production
- How to deploy (manual + CI/CD)
- How to add new pages or content
- How to set up GitHub Pages in repo settings (Settings > Pages > Source: GitHub Actions)
