# Cursor Rules for jcmcginnis.com

## Project Overview

Personal website and blog for Jesse McGinnis, built with Bridgetown 2.0 and Tailwind CSS 4. Deployed to GitHub Pages via GitHub Actions.

**Live site:** https://jcmcginnis.com

## Tech Stack

- **Static Site Generator:** Bridgetown 2.0
- **CSS Framework:** Tailwind CSS 4 with @tailwindcss/typography plugin
- **Templating:** ERB templates with Ruby helpers
- **Fonts:** Inter variable font (loaded from rsms.me CDN)
- **Task Runner:** mise

## Development Commands

All commands use [mise](https://mise.jdx.dev/):

```bash
# Install dependencies
mise run up

# Start dev server (recommended)
mise run start

# Build for production
mise run build

# Lint and format code
mise run lint      # Check only
mise run lint -a   # Autocorrect
```

Dev server runs at `http://localhost:4000`

Tailwind CSS runs in parallel with Bridgetown via foreman. CSS automatically recompiles when any template or style file changes.

## Agent Instructions

**IMPORTANT:** Agents must always run `mise run lint -a` after making changes to ensure code is properly formatted. This runs Prettier and erb_lint with autocorrect.

## File Structure

```
bridgetown.config.yml  # Site configuration
config/initializers.rb # Plugin initialization and custom helpers
Gemfile               # Ruby dependencies
package.json          # Node dependencies (Tailwind CLI)
Procfile.dev          # Foreman config (Bridgetown + Tailwind parallel)
.config/mise/
  config.toml         # Mise tool versions and settings
  tasks/              # Task scripts: up, start, build, lint
src/
  _layouts/           # ERB templates: base.erb → default.erb → post.erb
  _partials/          # Reusable components (header, footer, etc.)
  _posts/             # Blog posts in Markdown
  _data/              # Structured data (menu.yml, site_metadata.yml)
  assets/css/         # Tailwind source (tailwind.css) and syntax highlighting
  category.erb        # Prototype page for auto-generated category archives
output/               # Build output (gitignored)
```

## Template Conventions

### ERB Templates
- Use `<%= %>` for output, `<% %>` for logic
- Partials are in `src/_partials/` with underscore prefix
- Render partials: `<%= render "shared/header", page: resource %>`

### Accessing Data
- Current resource: `resource` or `page`
- Resource data: `resource.data.title`, `resource.data.description`
- Collections: `collections.posts.resources`
- Site data: `site.data.menu.main`
- Site metadata: `site.data.site_metadata`

### Custom Helpers (in config/initializers.rb)
- `featured_post` - Returns featured post (recent or rotated)
- `posts_by_year` - Groups posts by year for blog index

## Writing Guidelines

### Blog Posts

Posts live in `src/_posts/` with naming: `YYYY-MM-DD-slug.md`

Required frontmatter:
```yaml
---
title: "Post Title"
permalink: /blog/post-slug/
---
```

Optional frontmatter:
```yaml
home: true           # Show in homepage rotation
description: "..."   # Subtitle displayed below title
image: /assets/img/post-image.jpg
categories:
  - Leadership       # Available: Leadership, Musings, Talks
```

### Categories (Prototype Pages)

Categories use Bridgetown's prototype pages feature via `src/category.erb`. Adding a new category to any post's frontmatter automatically creates an archive page at `/category/:slug/`.

Current categories: Leadership, Musings, Talks

## Styling Conventions

### Tailwind Classes
- Dark mode: `dark:` variant
- Typography: `prose` classes from @tailwindcss/typography
- Custom utility `prose-quoteless` removes blockquote decorations

### Color Palette
- **Primary accent:** Rose (`rose-700`, `rose-800`)
- **Background:** Zinc scale (`zinc-50` light, `black`/`zinc-900` dark)
- **Text:** Zinc scale (`zinc-700` light, `zinc-200` dark)
- **Gradient accent:** `bg-gradient-to-tr from-sky-500 via-indigo-500 to-rose-500`

## Plugins

- `bridgetown-feed` - RSS feed generation
- `bridgetown-seo-tag` - SEO meta tags

## Common Tasks

### Adding a new blog post
1. Create `src/_posts/YYYY-MM-DD-slug.md`
2. Add required frontmatter (title, permalink)
3. Add optional frontmatter (categories, image, description, home)
4. Write content in Markdown
5. Run `mise run lint -a` to format

### Adding a new category
Just add it to a post's `categories` array - the prototype page generates the archive automatically.

### Adding a navigation item
Edit `src/_data/menu.yml`

### Customizing theme
Edit `src/assets/css/tailwind.css` using Tailwind CSS 4 configuration
