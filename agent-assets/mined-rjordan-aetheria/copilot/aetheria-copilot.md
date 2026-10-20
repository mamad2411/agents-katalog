# Copilot Instructions for Aetheria Project

## Project Overview

**Aetheria** is a rich fantasy world documentation site built with SolidJS, TypeScript, and Vite. The project serves as an interactive reference for a comprehensive fantasy RPG setting, including characters, classes, magic systems, politics, religion, and more.

# Aetheria World Data System - Development Guide

## Project Overview
Fantasy world reference system with SolidJS website and AI-optimized documentation generation. Built for both human consumption via GitHub Pages and AI systems via RAG/vector databases.

Above all, documents and components should prioritize AI consumption through comprehensive, well-structured markdown optimized for vector databases and RAG systems.

## Tech Stack

- **Frontend**: SolidJS with TypeScript
- **Build Tool**: Vite
- **Styling**: SCSS with custom design system
- **Data**: Static JSON files
- **Architecture**: Component-based with responsive design
- **Additional**: PWA support, service worker, AI-optimized documentation generation

## Project Structure

```
```
Aetheria/
├── site/                          # SolidJS application
│   ├── src/
│   │   ├── data/                  # JSON data files + TypeScript types
│   │   ├── pages/                 # SolidJS page components
│   │   └── components/            # Reusable UI components
│   └── public/
│       └── data/                  # Static JSON files
├── ai-docs/                       # Generated AI-optimized documentation
├── generate-ai-docs.js            # AI documentation generator
├── reference/                     # Source markdown documentation
└── dev.sh                         # Development workflow script
```
```

## Design System & Styling

### Color Palette
- **Primary**: `#667eea` (purple-blue gradient base)
- **Secondary**: `#764ba2` (purple)
- **Background**: `#f8f9fa` (light gray)
- **Text**: `#333` (dark gray)
- **Borders**: `#e9ecef` (light gray)

### Typography
- **Font Family**: System fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto"`)
- **Responsive**: Mobile-first approach with breakpoints at 768px and 400px

### Components

**Design Principles**:
- Prioritize compactness over visual heaviness
- Avoid excessive padding, backgrounds, and borders
- Maintain readability while maximizing information density
- Clean, minimal aesthetic preferred over decorative styling

#### Responsive Tables
- Custom `ResponsiveTable` component for mobile-friendly data display
- Priority-based column hiding on smaller screens
- Card-style layout on mobile devices

#### Entity Cards
- Consistent card layout for characters, creatures, equipment
- Rank badge system with color coding (F through SSS ranks)
- Responsive grid layouts

## Data Structure

### Core Entity Types
- **Characters**: NPCs, important figures with full stat blocks
- **Classes**: Character classes with specializations and descriptions
- **Creatures**: Monsters, animals, NPCs with combat stats
- **Equipment**: Weapons, armor, items with mechanical properties
- **Magic**: Spells, schools, magical theory and systems
- **Organizations**: Guilds, nations, political entities
- **Skills**: Abilities, proficiencies, mechanical systems

### JSON Schema Patterns
- All entities include `id`, `name`, `description` fields
- Rank system: `F, E, D, C, B, A, S, SS, SSS` for power scaling
- Consistent use of arrays for tags, categories, and relationships
- Standardized stat block format across entity types
- Properties in the JSON should follow consistent naming conventions and data types (camelCase)

## Development Guidelines

### CSS/SCSS Architecture
**CRITICAL: Always follow this hierarchy when organizing SCSS:**

1. **Variables** - All SCSS variables at the top
2. **Element Styles** - Base typography and layout elements (`p`, `h1-h6`, `a`, `button`, `table`, etc.)
3. **Class-Based Overrides** - Component and utility classes (`.container`, `.responsive-table`, etc.)
4. **Media Queries** - Responsive styles at the end

### Styling Philosophy
- **Element-first styling** - Set base styles on HTML elements
- **Classes for overrides** - Use classes for variations and components
- **IDs as last resort** - Avoid ID selectors (maintain low specificity)
- **Proper nesting** - Use SCSS nesting logically, don't over-nest
- **Always specify text color** on hover/active states for accessibility

### Component Development
- Use TypeScript interfaces for all component props
- Implement responsive design from mobile-first perspective
- Prefer semantic HTML elements
- Keep components focused and reusable

### Styling Best Practices
- Use SCSS variables for consistent theming
- Avoid inline styles; prefer Element styles complimented with CSS classes
- Implement mobile-first responsive design
- Prioritize performance and accessibility
- **Avoid bulky styling**: Prefer minimal, clean designs over heavily decorated ones

### Data Management
- Maintain consistency in JSON structure across all data files
- Use meaningful IDs and consistent naming conventions
- Implement proper error handling for missing or malformed data
- Keep data files organized and well-documented
- **Shared Architecture**: `/public/data/` serves both static site and AI documentation generation
- **Single Source of Truth**: All world information centralized

### SolidJS Component Patterns
- **TypeScript interfaces** for component props
- **Reactive data** with createSignal/createMemo
- **Clean separation** between data and presentation
- **File Organization**: Element styles first, component classes grouped, responsive at end

### UI Components Architecture
- **OfflineIndicator** - Status display with responsive design and color coding
- **ResponsiveTable** - JavaScript-controlled responsive tables with priority columns
- **Layout** - Main structure with header, nav, main, footer (mobile-first)
- **EntityCard** - Consistent display for characters, creatures, equipment
- **AlignmentDisplay** - Four-axis character profile system rendering

## Content Guidelines

### Writing Style
- Clear, concise descriptions
- Consistent tone and voice across all content
- Proper fantasy world terminology
- Balance detail with readability

### World Building Consistency
- Maintain consistent lore and naming conventions
- Ensure political, religious, and magical systems interconnect logically
- Regular updates to relationship and cross-reference data

## Technical Architecture

### AI Documentation Generation
- **Purpose**: Generates comprehensive world context for RAG systems and vector databases
- **Location**: `/generate-ai-docs.js` with Node.js implementation
- **Output**: Consolidated markdown files optimized for AI consumption and chunking
- **Priority**: All content should prioritize AI consumption through comprehensive, well-structured documentation

### PWA Implementation
- **Technology**: vite-plugin-pwa with Workbox for intelligent caching
- **Strategy**: NetworkFirst for data files, runtime caching configured
- **Migration**: Successfully migrated from custom service worker to plugin-based approach
- **Features**: Offline functionality, app manifest, service worker management

### Documentation Generation
- **Source**: Live GitHub Pages deployment crawling
- **Output**: Static markdown documents for AI model contexts
- **Purpose**: Downloadable content for direct AI consumption
- **Tools**: Custom crawling scripts in `/site/crawl-github-pages.js`

### Deployment Pipeline

### Performance
- Lazy loading for images and heavy content
- Efficient bundle splitting with Vite
- Service worker for offline functionality
- Optimized asset delivery

### Accessibility
- Semantic HTML structure
- Proper ARIA labels and roles
- Keyboard navigation support
- Color contrast compliance

### Mobile Experience
- Touch-friendly interface elements
- Readable font sizes on small screens
- Efficient information hierarchy
- Fast loading on mobile networks

## Future Enhancements

### Planned Features
- Interactive maps and visualizations
- Better cross-reference linking system
- Advanced PWA features

### Technical Debt
- Regular review and cleanup of unused CSS
- Component refactoring for better reusability
- Data validation and schema enforcement
- Performance monitoring and optimization

## Development Workflow

1. **Local Development**: Use `npm run dev` for hot-reload development server
2. **Building**: `npm run build` creates optimized production build
3. **Testing**: Regular cross-browser and mobile device testing
4. **Deployment**: Static site deployment to GitHub Pages

## Key Principles

1. **User Experience First**: Prioritize readability and usability
2. **Mobile Responsive**: Design for mobile devices first
3. **Performance Conscious**: Optimize for fast loading and smooth interactions
4. **Maintainable Code**: Write clean, documented, reusable code
5. **Consistent Design**: Maintain visual and functional consistency
6. **Minimal Styling**: Prefer clean, uncluttered designs over decorative elements

---

*This document should be updated as the project evolves and new decisions are made.*
