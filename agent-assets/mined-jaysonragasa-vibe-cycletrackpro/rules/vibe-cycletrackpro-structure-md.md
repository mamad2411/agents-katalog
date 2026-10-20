# Project Structure

## Directory Organization

```
CyclingTracker/
├── .amazonq/
│   └── rules/
│       ├── memory-bank/          # AI-generated documentation
│       └── appspecification.md   # Product requirements and specifications
├── CyclingTracker/
│   ├── bin/                      # Build output directory
│   │   └── Debug/
│   ├── obj/                      # Intermediate build files
│   │   └── Debug/
│   ├── CyclingTracker.csproj     # .NET project file (minimal, used for hosting)
│   ├── index.html                # Main application (single-page web app)
│   ├── Program.cs                # .NET console host (minimal)
│   └── specs.md                  # Duplicate specification file
└── CyclingTracker.sln            # Visual Studio solution file
```

## Core Components

### Single-Page Application (index.html)
The entire application is contained in a single HTML file with embedded CSS and JavaScript, following a modular architecture pattern.

### Architecture Pattern: Service-Oriented with SOLID Principles

The application is structured around six main classes that follow separation of concerns:

#### 1. StateStore (State Management)
- Centralized state container using observer pattern
- Manages all application state (route data, ride metrics, UI state, waypoints)
- Provides subscribe/update/get methods for reactive updates
- Notifies listeners when state changes occur

#### 2. MapService (Map Rendering & Interaction)
- Manages Leaflet map instance and all map-related operations
- Handles marker placement (start, end, waypoints, user location, hover)
- Draggable markers with automatic rerouting on drag-end and segment reset
- Click-on-route to add waypoints dynamically with automatic rerouting
- Draws routes and colored segments on the map
- Provides route highlighting for graph interactions (dashboard only)
- Updates user location during active rides
- Shows toast notifications during marker drag operations

#### 3. RouteService (External API Integration)
- Geocoding via Nominatim API (OpenStreetMap)
- Reverse geocoding for coordinate-to-address resolution
- Route calculation via OSRM with multi-waypoint support
- Elevation data fetching via Open-Elevation API
- GPX file parsing and route extraction
- Handles API errors with fallback mock data

#### 4. RideManager (Ride Tracking Logic)
- Manages ride lifecycle (start, pause, resume, stop)
- Integrates with browser Geolocation API with high accuracy
- Calculates moving time vs ride time (moving threshold: 2 km/h)
- Updates speed metrics in real-time (current and average)
- Controls timer intervals for time tracking (1 second intervals)
- Processes geolocation position updates with speed conversion

#### 5. UIManager (User Interface Controller)
- Manages panel visibility and transitions (planner, advanced, dashboard)
- Renders dynamic UI elements (sections, metrics, waypoints)
- Handles dual Chart.js elevation graphs (planner and dashboard) with independent view states
- Implements independent zoom/pan/reset controls for each graph
- Calculates and displays ETA and ETT based on segment speeds
- Manages segment creation/deletion/modification with dual-slider interface
- Custom modal system for alerts and confirmations (two types: alert and confirm)
- Toast notification system with auto-dismiss and fade animations
- Loading overlay with status messages for async operations
- Waypoint management (add, remove, render) with autocomplete
- Real-time boundary updates with clamping logic for segment sliders
- Optional segment highlighting on map (dashboard chart only, checkbox-controlled)

#### 6. App (Main Orchestrator)
- Initializes all services with dependency injection
- Sets up event listeners and user interactions
- Coordinates communication between services
- Manages autocomplete functionality for start, end, and waypoints
- Handles GPX file upload and parsing
- Handles fullscreen mode

## Component Relationships

```
App (Orchestrator)
├── StateStore (Data)
├── MapService (Visualization)
│   └── Uses: StateStore
├── RouteService (API)
│   └── Uses: StateStore
├── RideManager (Tracking)
│   └── Uses: StateStore, App (for map updates)
└── UIManager (Interface)
    └── Uses: StateStore, App (for map updates)
```

## Key Design Patterns

### Observer Pattern
- StateStore notifies all subscribers when state changes
- UI components automatically update when relevant state changes

### Dependency Injection
- Services receive dependencies through constructor
- App instance passed to RideManager and UIManager for cross-service communication

### Single Responsibility Principle
- Each class has one clear purpose
- Map operations separated from UI logic
- API calls isolated in RouteService
- State management centralized in StateStore

### Separation of Concerns
- HTML structure defines layout
- CSS handles styling and animations
- JavaScript manages behavior and logic
- External libraries loaded via CDN

## Data Flow

1. **User Input** → App event listeners
2. **App** → Updates StateStore
3. **StateStore** → Notifies subscribers (UI, Map)
4. **Services** → Perform operations (API calls, calculations)
5. **Services** → Update StateStore with results
6. **StateStore** → Triggers UI re-render
7. **UI** → Reflects updated state to user

## External Dependencies

### CDN-Loaded Libraries
- **Tailwind CSS**: Utility-first styling framework
- **Leaflet**: Interactive map rendering (OpenStreetMap)
- **Chart.js**: Elevation profile graph visualization
- **Font Awesome**: Icon library for UI elements

### External APIs
- **Nominatim**: Geocoding and address search
- **OSRM**: Route calculation and navigation
- **Open-Elevation**: Elevation data for route profiles

## Build System

The project uses a minimal .NET 8.0 console application as a hosting wrapper, but the actual application is a standalone HTML file that can run in any modern web browser without compilation.

### Project Configuration
- **Target Framework**: .NET 8.0
- **Output Type**: Console executable
- **Purpose**: Development hosting only (not required for deployment)

## Deployment Model

The application is designed for static hosting:
- Single HTML file can be served from any web server
- No server-side processing required
- All logic runs client-side in the browser
- APIs accessed directly from client (CORS-enabled public APIs)
