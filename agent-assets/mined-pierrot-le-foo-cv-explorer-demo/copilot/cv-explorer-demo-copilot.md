# CV Explorer - AI Copilot Instructions

## Project Overview
CV Explorer is an AI-powered resume screening application built with Next.js 15, featuring a split-pane interface with chat-based interactions and resume browsing. The app uses OpenAI for conversational AI and PostgreSQL with pgvector for vector-based resume search.

## Architecture & Key Components

### Core Structure
- **Split-pane layout**: `app/page.tsx` renders `Chat` (left) and `Resumes` (right) components
- **AI Chat Interface**: Uses `@ai-sdk/react` with custom AI Elements components in `/components/ai-elements/`
- **Database**: PostgreSQL with pgvector extension for vector similarity search
- **Styling**: Tailwind CSS v4 with Radix UI components

### AI Elements System
The project uses a sophisticated AI Elements component library (installed via `npx ai-elements@latest`):
- **Conversation components**: `Conversation`, `ConversationContent`, `ConversationScrollButton` for chat layout
- **Message components**: `Message`, `MessageContent`, `MessageAvatar` for individual messages  
- **Input components**: `PromptInput`, `PromptInputTextarea`, `PromptInputSubmit` for user input
- **Response handling**: `Response` component for AI message rendering

### Database & Vectors
```prisma
model Resume {
  id       String                 @id @default(cuid())
  content  String
  vector   Unsupported("vector")?  // pgvector for semantic search
}
```

## Development Workflows

### Environment Setup
```bash
# Database setup with pgvector
sudo docker-compose up  # Uses pgvector/pgvector:pg16 image on port 5490
npx prisma migrate dev   # Run after schema changes
```

### Key Commands
- `pnpm dev` - Uses Next.js 15 with Turbopack for fast development
- `pnpm build` - Production build with Turbopack
- `pnpm lint` - ESLint configuration

### Database Management
- Custom Prisma client output: `prisma/client/` (not default location)
- Extended client with Accelerate: `prisma/prisma.ts` exports extended client
- Vector extension setup: Docker uses `pgvector/pgvector:pg16` with custom init scripts

## Project-Specific Patterns

### Component Architecture
- **AI Elements Integration**: Components in `/components/ai-elements/` provide pre-built chat UI primitives
- **Type-safe Messages**: Uses `UIMessage` type from `ai` package for message handling
- **Streaming Responses**: API route at `/app/api/chat/route.ts` implements streaming with 30s timeout

### State Management
- **useChat Hook**: Primary chat state via `@ai-sdk/react` with custom initial assistant message
- **No Global State**: Component-level state using React hooks
- **Message Structure**: Messages have `parts` array with `type` and `text` properties

### Styling Conventions
- **Utility-first**: Heavy use of Tailwind classes with `cn()` utility from `lib/utils.ts`
- **Component Variants**: Uses `class-variance-authority` for component styling variants
- **Responsive Layout**: Split-pane with `flex-1` classes for equal distribution

## External Dependencies & Integration

### AI & LLM
- **OpenAI Integration**: Uses `@ai-sdk/openai` with `gpt-4o` model
- **Streaming**: Implements `streamText` for real-time responses
- **Message Conversion**: `convertToModelMessages` for API compatibility

### Database Integration
- **Prisma Client**: Custom output directory requires importing from `./client`
- **Vector Search**: Prepared for semantic search with pgvector extension
- **Connection Pooling**: Uses Prisma Accelerate extension for performance

### Resume Processing
- **File Storage**: PDF resumes stored in `/resumes/` directory
- **Processing Pipeline**: Prepared for text extraction and vectorization (currently using sample data)

## Development Notes

### File Conventions
- **Client Components**: Explicitly marked with `'use client'` directive
- **API Routes**: Follow App Router conventions in `/app/api/`
- **Component Structure**: Separate directories for UI components vs AI-specific components

### Common Patterns
- **Error Handling**: Built into AI SDK hooks (`error`, `status` states)
- **Loading States**: Use `status` from `useChat` for UI feedback
- **Form Submission**: Manual form handling with `e.preventDefault()` pattern

### Vector Search Setup
When implementing vector search:
1. Ensure pgvector extension is enabled in PostgreSQL
2. Use `Unsupported("vector")` type in Prisma schema
3. Implement text chunking and embedding generation for resume content
4. Add similarity search queries using pgvector operators
