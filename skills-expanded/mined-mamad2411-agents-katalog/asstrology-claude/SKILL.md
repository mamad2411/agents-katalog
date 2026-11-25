# Asstrology.com - AI Assistant Guide

## Project Overview

**Asstrology.com** is a playful, cheeky astrology website focused on love and relationship compatibility. The site combines legitimate astrological insights with humor, using AI to generate personalized horoscopes and compatibility reports.

**Tagline:** "Astrology, but cheeky"

## Project Status

🚧 **Not Yet Started** - Project is in planning phase with comprehensive documentation ready for implementation.

## Tech Stack

### Core
- **React Router 7** - SSR framework with file-based routing
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Supabase** - Authentication, PostgreSQL database, storage

### Key Integrations
- **Anthropic Claude API** - AI-generated horoscopes and compatibility reports
- **OpenWeatherMap API** - Weather context for horoscopes
- **Google Maps APIs** - Geocoding and timezone for birth charts
- **NASA/Lunar APIs** - Moon phase data
- **Resend/SendGrid** - Email newsletters

### UI Libraries
- **Headless UI** or **Radix UI** - Accessible components
- **Framer Motion** - Animations
- **Lucide React** - Icons

## Project Structure

```
asstrology.com/
├── CLAUDE.md                    # This file - AI assistant guide
├── .env.example                 # Environment variables template
├── docs/                        # Detailed documentation
│   ├── implementation-guide.md  # Step-by-step implementation
│   ├── technical-specification.md  # Full tech spec
│   └── project-overview.md      # Project plan and strategy
├── app/                         # React Router 7 app (to be created)
│   ├── routes/                  # File-based routing
│   ├── components/              # React components
│   ├── lib/                     # Utilities and integrations
│   └── styles/                  # Global styles
├── public/                      # Static assets
└── supabase/                    # Database migrations
```

## Quick Start

1. **Initialize Project:**
   ```bash
   npx create-react-router@latest asstrology
   cd asstrology
   npm install @supabase/supabase-js @supabase/ssr @anthropic-ai/sdk framer-motion lucide-react
   ```

2. **Set Up Environment:**
   ```bash
   cp .env.example .env.local
   # Add your API keys to .env.local
   ```

3. **Configure Supabase:**
   - Create project at supabase.com
   - Run database migrations from `docs/implementation-guide.md`
   - Enable Google OAuth

4. **Start Development:**
   ```bash
   npm run dev
   ```

## Core Features

### Phase 1: Foundation (Weeks 1-2)
- Authentication (Google OAuth, email/password)
- 12 zodiac sign profile pages
- Basic layout with responsive navigation

### Phase 2: Zodiac Content (Week 3)
- Compatibility calculator for all sign pairings
- Element and modality-based scoring
- Shareable results

### Phase 3: AI Content (Week 4)
- Daily horoscopes generated with Claude API
- Caching system for horoscopes (24-hour TTL)
- Weather and lunar context integration

### Phase 4: Enhanced Features (Ongoing)
- Interactive quizzes
- User profiles with saved compatibilities
- Birth chart calculator (premium)
- Newsletter system

## Key Files to Reference

- **Implementation Guide** (`docs/implementation-guide.md`):
  - Step-by-step implementation instructions
  - Code snippets for Supabase setup, auth flow, compatibility calculator
  - Testing checklist and deployment steps

- **Technical Specification** (`docs/technical-specification.md`):
  - Complete database schema
  - API integration details
  - Authentication flow
  - React Router 7 SSR patterns

- **Project Overview** (`docs/project-overview.md`):
  - Feature roadmap
  - Design considerations
  - Marketing strategy
  - Content calendar ideas

## Database Schema (Supabase)

### Key Tables
- **profiles** - User data, birth chart info
- **saved_compatibilities** - User's saved compatibility checks
- **horoscope_cache** - Cached AI-generated horoscopes (24hr TTL)
- **quiz_results** - Quiz responses and results
- **newsletter_subscribers** - Email list

See `docs/technical-specification.md` for full schema.

## Authentication Flow

1. Google OAuth or email/password via Supabase Auth
2. Session management with Supabase SSR
3. Protected routes use server-side session validation in loaders
4. RLS policies enforce data access control

## Compatibility Algorithm

```typescript
// Simplified scoring:
- Element compatibility (Fire/Earth/Air/Water)
- Modality compatibility (Cardinal/Fixed/Mutable)
- Overall score: 0-100 across categories:
  - Romantic
  - Physical chemistry
  - Communication
  - Long-term potential
```

## AI Content Generation

### Horoscope Generation Flow
1. Check cache for today's horoscope
2. If not cached:
   - Fetch planetary positions, moon phase, weather
   - Generate with Claude API using contextual prompt
   - Cache for 24 hours
3. Return formatted horoscope with:
   - General outlook
   - Love focus
   - Lucky color/number
   - Cheeky tip

### Prompting Strategy
- Tone: Playful, self-aware, flirty but tasteful
- Focus: Love and relationships
- Include specific, actionable advice
- Use weather and lunar context for personalization

## Environment Variables

Required for MVP:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `ANTHROPIC_API_KEY`

See `.env.example` for full list with priority levels.

## Implementation Notes

### React Router 7 Patterns
- Use `loader` functions for server-side data fetching
- SSR-compatible Supabase client with cookie handling
- Protected routes via loader redirects
- Prerender static pages (sign profiles)

### Performance
- Cache horoscopes: 24 hours
- Cache compatibility: 7 days
- Weather/lunar data: 1 hour
- Code splitting for heavy components (birth chart viz)
- Image optimization (WebP with fallbacks)

### Tone & Voice
- Playful and witty
- Self-aware humor
- Inclusive and sex-positive
- Never crude or mean-spirited
- Balance entertainment with genuine insights

## Development Workflow

1. **Start with authentication** - Get Supabase auth working first
2. **Build static content** - Create all 12 sign pages
3. **Implement calculator** - Compatibility logic without AI
4. **Integrate Claude** - Add AI-generated descriptions
5. **Add caching** - Implement horoscope cache system
6. **Polish UI** - Animations, responsive design
7. **Deploy** - Vercel recommended for React Router 7

## Testing Checklist

- [ ] All authentication flows work (Google OAuth, email/password)
- [ ] All 12 sign pages load correctly
- [ ] Compatibility calculator works for all 144 pairings
- [ ] Horoscopes generate and cache properly
- [ ] Mobile responsive (375px, 768px, 1440px)
- [ ] Protected routes redirect correctly
- [ ] Social sharing works with proper meta tags

## Resources

- [React Router 7 Docs](https://reactrouter.com/dev)
- [Supabase Docs](https://supabase.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

## Support

For detailed implementation questions, refer to:
- `docs/implementation-guide.md` - Step-by-step instructions
- `docs/technical-specification.md` - Architecture details
- `docs/project-overview.md` - Feature planning

---

**Ready to make the stars align!** ✨
