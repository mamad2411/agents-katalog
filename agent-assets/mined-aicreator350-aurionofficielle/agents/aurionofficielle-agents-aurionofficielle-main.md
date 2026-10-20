## Project Summary
Aurion Studio is a focused AI-powered studio for creatives — especially photographers, designers and visual artists. Our first vertical is **Portfolios for Creatives**: a workflow that transforms your images into a visual identity, responsive portfolio, SEO-ready copy, and a live site in minutes.

## Tech Stack
- **Frontend**: React, TypeScript, Vite
- **Styling**: Tailwind CSS, Framer Motion, Lucide React
- **Authentication**: Clerk
- **Database**: Supabase
- **Payments**: Stripe
- **State Management**: Zustand, React Query
- **Routing**: React Router v6

## Architecture
- **Feature-Based Modular Architecture**: Organized by features.
- **Landing Page**: New high-end interface cloned from Pleur (https://pleur.framer.website/), located in `src/components/sections/`.
- **Separation of Concerns**: UI components (`components/ui`), business logic (`services/`, `hooks/`), and layouts (`layouts/`).
- **Security-First**: Integrated encryption, sanitization, and rate limiting layers.
- **11 Tools**: Each deployed independently on Vercel in `tools-deploy/`. Each has its own `CLAUDE.md`.
- **Claude Code**: 16 skills + 30 slash commands (8 namespaces) + 14 agents + hooks for automated quality checks + 3 MCP servers (blender, paper, figma). Archive in `.claude/_archive/` (recoverable).

## User Preferences
- **Aesthetic**: Modern Minimalist Boutique Studio (Monochrome #F2F2F2 background, #0D0D0D text), high contrast, heavily rounded corners (radius: 24px) for cards.
- **Typography**: Elegant Serif Italic for display (Newsreader/Serif style), clean Sans-Serif for body (Inter). Massive fluid headlines.
- **Design Inspiration**: Pleur (https://pleur.framer.website/).

## Project Guidelines
- **No Comments**: Avoid adding comments to code unless explicitly requested.
- **Clean UI**: Maintain generous whitespace and use horizontal dashed dividers for sectioning.
- **Performance**: Keep the interface fluid and responsive.
- **Security**: Always use the provided security utilities for input handling and data storage.
- **TypeScript**: Zero `any`, strict mode enforced.
- **CSRF**: Required on all auth'd POST requests (X-CSRF-Token header).

## Common Patterns
- **Floating Pill Nav**: Glassmorphism effect for the sticky header navigation.
- **Vertical Workflow**: Linear progression steps (01, 02, etc.) with rounded number boxes.
- **Pulsing CTAs**: Small indicator dots with pulse animations for active call-to-actions.
- **Bento Grid**: Results-oriented feature display with floating UI cards.
- **High-End Contrast**: Use #0D0D0D for solid buttons and footer backgrounds against light backgrounds.
