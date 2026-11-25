# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PEAS Stack (PostgreSQL, Express.js, Angular, Supabase) SaaS application for generating Media RSS feeds with AI-powered content generation and workflow management.

## Development Commands

### Backend (Express.js)
```bash
cd backend
npm install        # Install dependencies
npm run dev        # Start development server with nodemon
npm start          # Start production server
npm test           # Run tests with Jest
```

### Frontend (Angular)
```bash
cd frontend
npm install        # Install dependencies
npm start          # Start development server (ng serve)
ng serve           # Alternative start command
ng build           # Build for production
ng build --watch --configuration development  # Build with watch mode
```

### Docker Development
```bash
docker-compose up  # Start full stack with Docker
```

## Architecture

### Backend Structure
- `src/index.js` - Main Express application entry point
- `src/config/` - Configuration files (app.config.js, supabase.js)
- `src/controllers/` - Route controllers (ai.controller.js)
- `src/routes/v1/` - API routes organized by version
- `src/middleware/` - Custom middleware (error handling)
- `src/services/` - Business logic services (ollama.service.js)
- `src/database/migrations/` - Database migration files
- `src/utils/` - Utility functions (logger.js)

### Frontend Structure
- Angular 17 application with Material Design
- `src/app/features/` - Feature modules (ai, auth, dashboard, rss, media)
- `src/app/core/` - Core services and guards
- `src/app/shared/` - Shared components and utilities
- `src/app/layouts/` - Layout components
- Uses TailwindCSS for styling

### Key Integrations
- **Supabase** - Database, authentication, and storage
- **AI Services** - Ollama for local AI processing
- **Google Drive API** - File synchronization
- **RSS 2.0** - Feed generation
- **Docker** - Containerized deployment

## Technology Stack

- **Backend**: Node.js, Express.js, Winston (logging), Helmet (security)
- **Frontend**: Angular 17, Angular Material, TailwindCSS, RxJS
- **Database**: PostgreSQL via Supabase
- **Authentication**: Supabase Auth with Google OAuth
- **AI**: Ollama integration for content generation
- **Storage**: Supabase Storage for media files

## Development Notes

- The application uses a monorepo structure with separate backend and frontend directories
- Shared types and utilities are in the `shared/` directory
- API versioning is implemented with `/api/v1` prefix
- Error handling is centralized in middleware
- Logging is configured using Winston
- The project includes comprehensive documentation in the `docs/` directory