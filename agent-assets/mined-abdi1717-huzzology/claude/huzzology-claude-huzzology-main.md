# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Setup and Installation
```bash
# Install all dependencies for monorepo
npm install && npm run setup

# Start development servers (client on :3000, server on :8000)
npm run dev

# Or start individually
npm run dev:client  # React app only
npm run dev:server  # API server only
```

### Build and Testing
```bash
# Build all workspaces
npm run build

# Run all tests
npm test

# Run specific workspace tests
npm run test:client
npm run test:server
npm run test:shared

# Run with coverage
npm run test:coverage
```

### Code Quality
```bash
# Lint all workspaces
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Type check (TypeScript)
npm run build  # Includes type checking
```

### Task Management with Taskmaster
```bash
# View current tasks
npm run tasks

# Get next task to work on
npm run tasks:next

# Show specific task details
npm run tasks:show <task-id>
```

## High-Level Architecture

### Project Structure
Huzzology is a **monorepo** with three main workspaces:
- **`client/`** - React 18 + TypeScript frontend with ReactFlow graph visualization
- **`server/`** - Node.js + Express backend with AI-powered content classification
- **`shared/`** - Common types, schemas, and utilities

### Core Domain: Archetype Mapping
The application maps **women's pop culture archetypes** through:
1. **Data Ingestion** - Scraping content from social platforms (TikTok, Twitter, Instagram, Reddit)
2. **AI Classification** - Using embeddings and LLMs to cluster content into archetypes
3. **Graph Visualization** - Interactive ReactFlow graphs showing archetype relationships
4. **Real-time Updates** - Live data feeds and trend analysis

### Key Data Models
```typescript
// Core archetype structure
interface ArchetypeNode {
  id: string;                    // kebab-case: 'clean-girl'
  label: string;                 // Display name: 'Clean Girl'
  description: string;
  keywords: string[];
  influences: string[];          // Related archetype IDs
  examples: ContentExample[];
  color: string;                 // Hex color for visualization
  metadata: {
    origin_date?: string;
    peak_popularity?: string;
    influence_score: number;     // 0-1 scale
    platforms: Platform[];
  };
}
```

### Architecture Layers

#### Frontend (React + ReactFlow)
- **Components**: `src/components/graph/` for ReactFlow nodes and edges
- **State Management**: Zustand store (`src/stores/archetypeStore.ts`)
- **UI System**: ShadCN components (`src/components/ui/`)
- **Graph Layouts**: Dagre, force-directed, circular algorithms
- **Theme System**: Light/dark mode with Tailwind CSS

#### Backend (Node.js + Express)
- **Classification Engine**: `src/classification/` with OpenAI embeddings and K-means clustering
- **Scrapers**: `src/scrapers/` with platform-specific implementations
- **Services**: `src/services/` for business logic (ArchetypeService, ClassificationService)
- **Database**: PostgreSQL with Drizzle ORM

#### Data Flow
```
Social Platforms → Scrapers → Classification Engine → Database → API → Frontend Graph
```

## Important Development Patterns

### Task Management with Taskmaster (MANDATORY)
- **ALWAYS use taskmaster** for task tracking and updates when working on tasks
- **Update task status** using the established pattern from Tasks 4-9
- **Document implementation** with `<info added>` sections in task files
- **Follow task dependencies** and subtask structure for organization
- **Create demo pages** for major features following existing patterns

### System Documentation Updates (ARCHITECTURE_OVERVIEW.md)
- **Update ONLY for major system changes** that significantly impact how the system works
- **Focus on holistic system overview** - describe how features work together, not individual task implementations
- **Avoid task-specific references** - documentation should read as a unified system description
- **Update when adding new core capabilities** like search systems, visualization engines, or data processing pipelines
- **LLMs should read this document first** to understand the complete system architecture before starting work

### Component Organization
- **Graph components** go in `client/src/components/graph/`
- **Archetype panels** go in `client/src/components/panels/`
- **Search/filter components** integrate with graph system
- **Reusable UI** follows ShadCN patterns in `client/src/components/ui/`
- **Custom hooks** for data fetching in `client/src/hooks/`
- **API client** logic in `client/src/lib/api-client.ts`

### State Management
Use **Zustand** for global state, not Redux:
```typescript
// Follow this pattern for new stores
interface ArchetypeStore {
  // State
  archetypes: ArchetypeNode[];
  selectedArchetype: string | null;
  
  // Actions
  setSelectedArchetype: (id: string | null) => void;
  updateArchetype: (archetype: ArchetypeNode) => void;
}
```

### ReactFlow Integration
- Custom node types in `client/src/components/graph/`
- Use `dagre` for automatic layout positioning
- Implement proper memoization for performance
- Handle both desktop and mobile interactions

### AI Classification Pipeline
The core intelligence is in `server/src/classification/`:
- **EmbeddingGenerator** - OpenAI text-embedding-ada-002
- **KMeansClusterer** - Dynamic cluster optimization
- **ArchetypeIdentifier** - LLM-based labeling
- **ContentClassifier** - Similarity-based assignment
- **InfluenceCalculator** - Multiple influence metrics

### API Design
Follow RESTful patterns:
```typescript
GET    /api/archetypes              // List all archetypes
GET    /api/archetypes/:id          // Get specific archetype
POST   /api/archetypes              // Create new archetype
PUT    /api/archetypes/:id          // Update archetype
GET    /api/archetypes/:id/examples // Get content examples
POST   /api/scrape/platform/:name  // Trigger scraping
```

### Archetype Detail Panels (Task 8)
Complete responsive panel system for archetype information:
```typescript
// Main panel with tabbed interface
<ArchetypePanel 
  archetype={selectedArchetype}
  onClose={handleClose}
  relatedArchetypes={relatedArchetypes}
  onArchetypeSelect={handleArchetypeSelect}
/>

// Components: ArchetypePanel, ContentExamples, InfluenceVisualization
// Features: Social media content, engagement metrics, influence mapping
// Integration: GraphVisualizationWithPanel for seamless UX
```

### API Integration & Filtering (Tasks 7.6 & 7.7)
Dynamic data loading with comprehensive filtering and search:
```typescript
// API-integrated graph with filtering
<FilteredGraphVisualization
  layout="dagre"
  enablePathfinding={true}
  enableRealTimeUpdates={false}
/>

// API data hook with caching and pagination
const { data, loading, error, fetchData, loadMore } = useGraphData({
  page: 1,
  limit: 20,
  search: 'aesthetic',
  platform: 'tiktok',
  sortBy: 'popularity'
});

// Components: FilteredGraphVisualization, GraphSearch, GraphFilterPanel
// Features: Real-time search, platform filtering, pathfinding, pagination
// Demo: /demo/filtered-graph for comprehensive feature showcase
```

## Project-Specific Guidelines

### Cultural Sensitivity
- Avoid stereotyping in archetype descriptions
- Include diverse representation in examples
- Implement content moderation for inappropriate content
- Regular review of potentially harmful classifications

### Performance Considerations
- Use React.memo for expensive graph components
- Implement virtual scrolling for large content lists
- Cache embeddings and classification results
- Optimize ReactFlow rendering with proper memoization

### Content Scraping
- Respect platform rate limits and terms of service
- Use rotating proxies for large-scale operations
- Implement comprehensive error handling and retry logic
- Store raw data before processing for debugging

### Testing Strategy
- **Unit tests** for classification algorithms and utilities
- **Component tests** for React components with React Testing Library
- **Integration tests** for API endpoints and scraper modules
- **E2E tests** for user journey flows

## Cursor Rules Integration

This project follows comprehensive development rules defined in `.cursor/rules/`:
- **huzzology-project.mdc** - Project-specific archetype mapping standards
- **core_system_rules.mdc** - Code quality and security standards
- **taskmaster.mdc** - Task management with Taskmaster tool

Key rules to follow:
- Always use TypeScript with strict type checking
- Follow ShadCN component patterns for UI consistency
- Implement proper error boundaries and loading states
- Use Taskmaster for project planning and task tracking
- Maintain mobile-first responsive design
- Ensure cultural sensitivity in all content-related features

## Environment Configuration

### Required Environment Variables
```bash
# AI Services (in .env)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here  # For Claude integration

# Database
DATABASE_URL=postgresql://...

# Development
NODE_ENV=development
```

### Workspace Dependencies
Each workspace (`client/`, `server/`, `shared/`) has its own `package.json` and should be built independently. Always run `npm run setup` after cloning to install all workspace dependencies.

## Quick Start for New Contributors

1. **Clone and setup**: `git clone <repo> && cd huzzology && npm run setup`
2. **Start development**: `npm run dev`
3. **Check current tasks**: `npm run tasks:next`
4. **Review architecture**: Read `docs/ARCHITECTURE_OVERVIEW.md`
5. **Follow project rules**: Check `.cursor/rules/huzzology-project.mdc`
6. **Run tests**: `npm test` before committing

The application should load with a working graph visualization showing sample archetypes and their relationships. The backend provides mock data during development.