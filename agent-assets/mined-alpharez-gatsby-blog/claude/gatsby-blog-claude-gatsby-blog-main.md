# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
- `npm run develop` or `npm start` - Start development server with hot reload
- `npm run build` - Build production version
- `npm run serve` - Serve built site locally
- `npm run clean` - Clean Gatsby cache and public directory
- `npm run format` - Format code using Prettier

### Code Quality
- `npm run format` - Format all JS, JSX, TS, TSX, JSON, and MD files with Prettier
- No linting or testing setup currently configured

## Architecture Overview

This is a Gatsby blog site (steveclement.me) built from the gatsby-starter-blog template with custom modifications.

### Content Structure
- Blog posts are stored as Markdown files in `content/blog/[post-name]/[post-name].md`
- Each post directory can contain images and other assets alongside the markdown file
- Draft posts are stored in `content/drafts/` (not processed by Gatsby)
- Posts use frontmatter with `title`, `date`, `layout`, and `categories` fields

### Key Architecture Components
- **gatsby-node.js**: Creates pages dynamically from markdown files, generates slugs, and sets up pagination between posts
- **gatsby-config.js**: Configures site metadata, plugins for markdown processing, image optimization, RSS feed generation, and PWA manifest
- **src/templates/blog-post.js**: Template for individual blog post pages with navigation to previous/next posts
- **src/components/**: Reusable components (bio, layout, seo)
- **src/pages/**: Static pages (index, about, 404)

### Data Flow
1. Gatsby sources markdown files from `content/blog/` via `gatsby-source-filesystem`
2. `gatsby-transformer-remark` processes markdown with plugins for images, code syntax highlighting (Prism.js), and responsive iframes
3. `gatsby-node.js` creates individual pages for each post using the blog-post template
4. GraphQL queries fetch post data and metadata in templates and pages

### Styling
- Uses CSS files (`normalize.css`, `style.css`) for styling
- No CSS-in-JS or component library framework
- Custom fonts loaded via @fontsource packages (Montserrat, Merriweather)

### Deployment
- Deployed to Netlify (badge shown in README)
- Static files (PDFs, favicon, robots.txt) served from `static/` directory