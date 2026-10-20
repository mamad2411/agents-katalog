# Obie Jukebox v2 - Copilot Instructions

This is a real-time jukebox system using Supabase as the single source of truth. All business logic runs server-side in Supabase Edge Functions and SQL RPCs.

## Architecture
- **Backend**: Supabase (Postgres + Realtime + Edge Functions)
- **Frontend**: Three separate Vite + React + TypeScript apps
- **State Management**: Server-driven via Supabase Realtime
- **Auth**: Supabase Auth with RLS policies
- **Free-tier optimized**: No polling, minimal function invocations

## Key Principles
- All state lives in Supabase
- Clients are stateless UIs that render Realtime data
- No localStorage or client-side queue logic
- Player must be online for system to function
- Priority queue plays before normal queue

## Components
1. **Admin App**: Queue management, playlists, settings, logs
2. **Player App**: Media playback, status reporting, heartbeat
3. **Kiosk App**: Public search interface, credit system, song requests
4. **Edge Functions**: Business logic (queue, player control, kiosk handler, playlist manager)
5. **SQL Schema**: Complete database with tables and RPCs

## Progress Tracking
- [x] Project structure created
- [x] Supabase configuration setup
- [x] Edge Functions implemented
- [x] Shared client library built
- [x] Admin frontend created
- [x] Player frontend created  
- [x] Kiosk frontend created
- [x] RLS policies implemented
- [x] Documentation completed