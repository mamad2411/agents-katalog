---
description: 
globs: 
alwaysApply: false
---
# GitHub Copilot Instructions: Muncak.id Project

## Project Overview

**Muncak.id** is a curated hiking trail directory across Indonesia. The site offers:
- Clean, readable info about mountain hiking routes
- Weather forecasts and elevation insights
- SEO-optimized pages for discoverability
- Users can log in (Google/Facebook) and leave reviews
- No complex client-side interaction—focus on performance and accessibility

## Technology Stack

| Technology       | Version | Purpose                      |
|------------------|---------|------------------------------|
| PHP              | 8.3     | Backend                      |
| Laravel          | 12      | Web framework                |
| Blade            | -       | Static SSR rendering         |
| Inertia.js       | 2.x     | Routing/data transport       |
| Alpine.js        | 3.x     | Frontend interactivity       |
| Tailwind CSS     | 4.x     | Styling framework            |
| MySQL            | 8.x     | Relational DB                |
| Screaming Frog   | -       | SEO testing tool             |
| Laravel Dusk     | -       | Performance testing (client) |
| Apache Bench     | -       | Performance testing (server) |

## Technology Guidelines

### Laravel
- Use Laravel Resource Controllers + Routes
- Use Laravel Dusk for browser-based benchmarks
- Follow Laravel naming conventions
- Prefer `@foreach` over `@for` unless index is needed
- Always eager load relationships to avoid N+1

### Blade
- Use for static, SEO-focused pages
- Prefer simple loops and includes
- Use `@includeIf` or `@once` where possible
- Keep logic out of templates — push to controller

### Inertia.js
- Used only for dynamic pages (e.g., review form, dashboard)
- Pass only the necessary props to the frontend
- Avoid over-fetching—keep props light

### Alpine.js
- Use for dropdowns, toggles, and minor reactivity
- Don't go overboard — avoid stateful complexity
- Always initialize Alpine via `x-data` inside the component

### Tailwind CSS
- Stick to utility-first principles
- Use spacing tokens like gap-4, mt-6, px-2
- Use prose class for markdown-styled content
- Theme colors should follow Shadcn-style token naming

### SEO Principles
- Always define meta.title, meta.description, and meta.image
- Prefer Laravel Blade for crawlable content
- Use Laravel’s built-in route caching and sitemap tools
- Use structured data (Schema.org) for trail info where relevant

### General Guidelines
- Use .env for all config values
- All trails are stored with slug, latitude, longitude, and elevation
- Pages must be responsive, readable, and mobile-first
- Do not use Vue or React for this project
- Keep every page fast and lightweight
- Avoid unnecessary JS — optimize for TTFB and LCP