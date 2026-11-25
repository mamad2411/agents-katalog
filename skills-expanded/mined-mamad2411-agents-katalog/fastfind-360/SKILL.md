# FastFind360 - Satellite-Powered Property Intelligence System

## Project Context
Building Africa's first AI-native property detection system using satellite imagery. 
Focus: Detect and classify buildings in Gombe State, Nigeria using satellite data and AI.

## Core Technologies
- Frontend: React 18+ with TypeScript
- Build Tool: Vite
- Mapping: Mapbox GL JS
- Satellite Data: Microsoft Building Footprints / Generated sample data
- Styling: Tailwind CSS
- State Management: React hooks (useState, useContext)

## Critical Requirements
1. NEVER use localStorage/sessionStorage for core app state
2. All state must use React hooks (useState, useContext)
3. Focus on WORKING functionality over perfect UI
4. Prioritize building detection accuracy and performance
5. Use realistic building data - generated or from Microsoft dataset

## Code Style
- Functional components only
- TypeScript for type safety
- Async/await for API calls
- Error boundaries for data loading failures
- Loading states for all async operations
- Proper type definitions for all props and state

## MVP Features Priority (Build in this order)
1. Interactive map with Gombe State centered (10.2897°N, 11.1672°E)
2. Generate/load building footprint data (12,847 buildings)
3. Building classification visualization with color coding
4. Statistics dashboard with live metrics
5. Search/filter functionality
6. Building interaction (hover/click details)

## Building Classification Rules
- **Residential**: 50-300 sq meters, regular shape → Blue (#3B82F6)
- **Commercial**: 200-1000 sq meters, near roads → Orange (#F59E0B)
- **Industrial**: >1000 sq meters, large footprint → Purple (#8B5CF6)
- **Institutional**: >500 sq meters, regular/compound shape → Green (#10B981)

## Performance Targets
- Map load: < 3 seconds
- Building data generation: < 2 seconds
- Display 12,847+ building polygons without lag
- Support clustering for zoomed-out views
- Search response: < 500ms

## Environment Variables
- VITE_MAPBOX_TOKEN: Mapbox API token (required)

## What NOT to do
- Don't build authentication yet (post-MVP)
- Don't optimize prematurely
- Don't add fancy animations before core works
- Don't use complex state management (Redux/Zustand) yet
- Don't focus on mobile-first until desktop works

## Testing Approach
- Test with Gombe coordinates: 10.2897°N, 11.1672°E
- Validate building distribution looks realistic
- Test with 100, 1000, 12847 building markers
- Browser: Chrome/Edge (primary)

## When Stuck
1. Check if Mapbox token is valid
2. Console.log all data before rendering
3. Test with simplified mock data first
4. Verify TypeScript types are correct
5. Check browser console for errors
