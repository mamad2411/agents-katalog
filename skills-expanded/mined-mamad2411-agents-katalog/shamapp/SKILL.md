# Cursor Rules for Sham Project

## Database Migrations
- NEVER create or modify Supabase migration files automatically
- NEVER write new migration files without explicit user request
- If database schema changes are needed, ask the user first before creating any migration files
- Migration files should only be created manually by developers

## General Development Rules
- Always ask before creating new files, especially in sensitive directories like migrations
- Prefer editing existing files over creating new ones
- When working with Supabase, be extra careful with database-related operations
- Always confirm with the user before making structural changes to the database

## File Creation Guidelines
- Ask permission before creating any new files
- Be especially cautious with:
  - Migration files (supabase/migrations/)
  - Configuration files
  - Database schema files
  - Any files that could affect the development environment

## Code Quality
- Follow existing code patterns and conventions
- Maintain consistency with the current codebase
- Always test changes when possible
- Document significant changes when appropriate
