# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Slidev presentation project - a web-based slide deck framework built with Vue.js. Slidev allows creating developer-focused presentations using Markdown with Vue components, animations, and code highlighting.

## Development Commands

- `pnpm install` - Install dependencies
- `pnpm dev` - Start development server (opens at http://localhost:3030)
- `pnpm build` - Build the presentation for production
- `pnpm export` - Export slides to PDF or other formats

## Project Structure

- `slides.md` - Main presentation content written in Markdown with frontmatter configuration
- `components/` - Custom Vue components (e.g., Counter.vue)
- `snippets/` - External TypeScript code snippets referenced in slides
- `theme/` - Custom Slidev theme with layouts, components, and styles
- `pages/` - Additional slide pages that can be imported
- `netlify.toml` / `vercel.json` - Deployment configurations for hosting platforms

## Key Architecture

- **Slidev Framework**: Uses @slidev/cli as the core presentation engine
- **Vue 3**: Component system with Composition API (`<script setup>`)
- **Custom Theme**: Located in `./theme` directory with multiple layout options (cover, intro, section, quote, statement, fact)
- **TypeScript Support**: External snippets and component props use TypeScript
- **UnoCSS**: Utility-first CSS framework for styling (visible in component classes)

## Slide Content Structure

The main presentation is in `slides.md` with:
- YAML frontmatter for theme and configuration
- Markdown content with Vue directives (v-click, v-motion, v-drag)
- Embedded Vue components and TypeScript code blocks
- External snippet imports using `<<< @/snippets/external.ts#snippet`

## Deployment

Configured for both Netlify and Vercel with:
- Build command: `npm run build`
- Output directory: `dist`
- SPA routing redirects to handle client-side routing