# Cursor Rules for Hard Times Music League Data

## Code Style
- Use TypeScript for all new files
- Use functional components with hooks
- Use Tailwind CSS for styling
- Use Lucide React icons instead of emojis

## Naming Conventions
- Use PascalCase for component names
- Use camelCase for variables and functions
- Use kebab-case for file names

## UI Guidelines
- NO EMOJIS in titles, headings, or navigation text
- Use Lucide React icons for visual elements
- Keep titles clean and professional
- Use consistent color scheme (green-400 for primary, gray-800/700 for backgrounds)

## Data Handling
- Process CSV data server-side in Next.js API routes
- Use proper TypeScript interfaces for data types
- Cache data when appropriate for performance
- **CRITICAL**: Some CSV files have malformed line breaks that break parsing
- Always use the custom CSV parser that handles these line break issues
- Never use standard CSV parsing libraries - they will fail on this data
- The csv-parser.ts handles the specific line break problems in this dataset

## Component Structure
- Keep components focused and single-purpose
- Use proper TypeScript props interfaces
- Export components as default exports
- Use meaningful component names

## Performance
- Use Next.js server-side rendering for data pages
- Implement proper loading states
- Use efficient data structures and algorithms

## TypeScript Best Practices
- NEVER use `any` type - always specify proper types
- Add null checks for Map.get() and array access
- Use proper interface definitions for all props
- Avoid unused variables - remove them immediately

## Next.js App Router Rules
- searchParams is always Promise<{ [key: string]: string | string[] | undefined }>
- Use 'use client' directive for client components with hooks
- Server components cannot use useState, useEffect, or event handlers
- Always await searchParams before using them

## React Best Practices
- Escape quotes in JSX: use &quot; instead of "
- Remove unused state variables and imports
- Use proper dependency arrays in useEffect
- Handle async operations in useEffect properly

## Error Prevention
- Always check for undefined/null before accessing properties
- Use proper TypeScript strict mode
- Add proper error boundaries for data loading
- Validate data before processing

## CRITICAL: Normalization Factors
- **NEVER NEVER NEVER change the normalization factors from what is listed in the Seasons tab**
- The Seasons tab is the SOURCE OF TRUTH for normalization factors
- Do NOT recalculate normalization factors in leaderboards or other components
- Use the existing normalization data from the Seasons tab
- Season 21 should ALWAYS be exactly 1.000x normalization factor

## CRITICAL: Best Seasons Calculation
- **ALWAYS use the EXACT same logic as the Seasons tab for calculating season scores**
- Use `seasonVotes.filter(v => v.season === season)` to get votes for that season only
- Use `seasonVotes.filter(vote => vote.spotifyUri === submission.spotifyUri)` for submission votes
- **NEVER use `votes.filter()` without season filtering - this counts votes from ALL seasons**
- The variable `seasonVotes` must be defined in scope before using it

## CRITICAL: Server vs Client Components
- **NEVER use `GlassCard` in server components** - it causes Safari infinite reload issues
- Always use `SimpleGlassCard` in server components (pages)
- `GlassCard` is a client component with animations - only use in client components
- This prevents hydration mismatches and Safari crashes
