# Coordinate General Project Rules

## CRITICAL: AI Model Versions
**ALWAYS USE THESE EXACT MODEL VERSIONS:**
- **Claude Sonnet 4.5**: Model identifier `claude-sonnet-4-5-20250929`
- **Gemini 2.5 Flash**: Model identifier `gemini-2.5-flash`
- **Claude Haiku 4.5**: Model identifier `claude-haiku-4-5-20251001`

**DO NOT** use older versions like:
- ❌ Claude 3.5 Sonnet
- ❌ Gemini 1.5 Flash  
- ❌ Gemini 2.0 Flash

These newer versions (4.5 for Claude, 2.5 for Gemini) are correct and available as of November 2, 2025.

## Project Context
This is a Next.js app that transforms text along two adjective dimensions using AI models.

## Tech Stack
- Next.js 14.1.4
- React 18 with hooks
- Claude Haiku 4.5 API (default)
- Claude Sonnet 4.5 API (optional)
- Gemini 2.5 Flash API (optional)
- sessionStorage for session management
- CSS Modules for styling
- No authentication/database

## API Configuration
- Anthropic endpoint: `https://api.anthropic.com/v1/messages`
- Google endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- Session-based generation (no database)
- Progressive ring-based generation (0→5)

## Code Style
- Functional components with hooks only
- File names: kebab-case
- CSS Modules for all styling
- Clear error handling with user-friendly messages
- No placeholder code - write everything completely
