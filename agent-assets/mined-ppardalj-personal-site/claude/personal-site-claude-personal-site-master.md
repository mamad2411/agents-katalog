# Pedro Pardal personal site (Hugo)

- Design tokens, components and the Figma-screen → template map: `DESIGN.md`. Tokens live in `themes/ppardalj/assets/scss/foundation/_variables.scss`.
- A page is `content/**/*.md`: its `blocks:` list renders `themes/ppardalj/layouts/partials/blocks/<type>.html`. `className` on a block sets the section theme (`light`, `dark`, `dark aurora`).
- Dev server: `make dev`. Production build: `make publish`. A push to `master` deploys.
