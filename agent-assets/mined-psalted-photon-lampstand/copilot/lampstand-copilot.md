# Lampstand - AI Agent Instructions

## Project Overview
Lampstand is a Next.js 16 application that analyzes news articles through a biblical lens using local AI (Ollama). It fetches news from RSS feeds, allows users to analyze articles with AI, and displays thematic connections to Bible passages with scripture text fetched from API.Bible.

## Architecture & Data Flow

### Core Components
- **Frontend**: Next.js App Router (`app/`) with client-side React components (`components/`)
- **API Routes**: `/api/analyze` (streaming AI analysis), `/api/news/[category]` (RSS aggregation), `/api/scripture/[reference]` (Bible verses)
- **Database**: SQLite (`lampstand.db`) via `better-sqlite3` - caches articles and analyses
- **AI Backend**: Ollama running locally (default: `qwen2.5:32b` model at `http://localhost:11434`)
- **Bible API**: API.Bible for scripture text (temporary - planned migration to local SWORD modules)

### Data Flow
1. User selects category → Fetches RSS feeds via `lib/rss-parser.ts` → Deduplicates & formats articles
2. User clicks article → Displays content & "Analyze with Bible" button
3. Analysis request → Checks `db.ts` cache → If miss, streams from Ollama → Saves to DB
4. AI returns JSON themes → Client fetches scripture text from API.Bible → Displays with "Prophetic Parallel" badges

## Key Patterns & Conventions

### Type System (`lib/types.ts`)
All data structures are strictly typed. Key types:
- `NewsArticle`: Unified format for RSS and custom articles
- `Theme`: AI analysis output with nested `Passage[]`
- `Category`: 9 predefined categories with CATEGORY_QUERIES defining RSS search terms
- Never modify these without checking all usages in `components/` and `app/api/`

### RSS Feed Strategy (`lib/rss-feeds.ts`, `lib/rss-parser.ts`)
- `RSS_FEEDS` maps categories to feed URLs (BBC, NYT, Times of Israel, etc.)
- Parser uses `fast-xml-parser` to handle various RSS/Atom formats
- Deduplication by title/link comparison in `fetchCategoryNews()`
- Fallback images per category in `CATEGORY_IMAGES`

### AI Analysis Pipeline (`app/api/analyze/route.ts`)
- **Caching**: Always check `getArticleByUrl()` and `getAnalysisByArticleId()` before calling Ollama
- **Streaming**: Uses Server-Sent Events (SSE) with `data:` prefix, not WebSockets
- **Prompt Engineering**: Instructs Ollama to return JSON with `themes[].passages[].isProphetic` flag
- **Error Handling**: Full response accumulated in `fullResponse` variable before parsing JSON (may be wrapped in markdown code blocks)

### Database Patterns (`lib/db.ts`)
- SQLite with synchronous API (no async/await needed for DB calls)
- `INSERT OR IGNORE` pattern for articles - returns existing ID if duplicate
- Three tables: `articles` (source content), `analyses` (cached AI responses), `favorites` (user bookmarks)
- Database is created automatically on first run - no migrations needed

### Component State Management
- All client components use `'use client'` directive (required for Next.js 16 App Router)
- Main state in `app/page.tsx`: `articles`, `selectedArticle`, `customArticle`
- `ArticleView.tsx` manages analysis state: `analyzing`, `streamingText`, `analysis`, `scriptures`
- No global state library - prop drilling is acceptable for this app size

## Environment Configuration

Required in `.env.local`:
```env
BIBLE_API_KEY=your_api_bible_key
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:32b
```

**IMPORTANT**: Never commit `.env.local` - it's gitignored

## Development Workflow

### Running the App
```bash
npm run dev          # Start at localhost:3000
npm run build        # Production build
npm run lint         # ESLint check
```

### Before Starting Development
1. Ensure Ollama is running: `ollama list` (should show installed models)
2. Verify `.env.local` has `BIBLE_API_KEY` and correct `OLLAMA_MODEL`
3. Check `lampstand.db` exists (auto-created on first API call)

### Adding New Categories
1. Add to `Category` union type in `lib/types.ts`
2. Add label to `CATEGORY_LABELS` and search query to `CATEGORY_QUERIES`
3. Add RSS feeds to `RSS_FEEDS` in `lib/rss-feeds.ts`
4. Add fallback image URL to `CATEGORY_IMAGES` in `lib/rss-parser.ts`

### Modifying AI Prompts
- Edit the prompt string in `app/api/analyze/route.ts` (lines ~25-50)
- Test with different models via `OLLAMA_MODEL` env var
- Response MUST be valid JSON matching `AnalysisResponse` interface in `lib/types.ts`

## Common Pitfalls

1. **Streaming API**: Don't use `NextResponse.json()` in `/api/analyze` - it breaks streaming. Return `new Response(stream, headers)`
2. **Bible References**: Format must match `Book Chapter:Verse` or `Book Chapter:Verse-Verse` for API.Bible parsing
3. **RSS Parsing**: Different feeds have different XML structures - test new feeds with `console.log()` before deploying
4. **Ollama Errors**: If analysis fails silently, check terminal for Ollama logs. Common issue: model not pulled (`ollama pull <model>`)
5. **SQLite Lock Errors**: Only one write at a time - never parallelize `saveArticle()` or `saveAnalysis()` calls
6. **Font Loading**: Custom fonts (Milonga, Cinzel, Libre Baskerville) are defined in `app/layout.tsx` - use CSS variables `--font-milonga`, etc.

## Future Migrations (Planned)

- **SWORD Bible Modules**: Replace API.Bible with local modules (code scaffolded in `lib/sword-bible.ts`, not yet integrated)
- **Full-Text Search**: Add FTS5 to SQLite for article search
- **User Accounts**: Expand `favorites` table for multi-user support

## Tech Stack Reference

- **Next.js 16**: App Router, Server Components, API Routes with streaming
- **React 19**: New JSX transform, updated hooks
- **TypeScript 5**: Strict mode enabled
- **Tailwind CSS 4**: Utility-first styling, config in `postcss.config.mjs`
- **better-sqlite3**: Synchronous SQLite bindings (faster than async alternatives)
- **fast-xml-parser**: Handles RSS/Atom feeds with attribute preservation
