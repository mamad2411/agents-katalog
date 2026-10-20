# Technology Stack

## Programming Languages

### HTML5
- **Version**: HTML5 with modern semantic elements
- **Purpose**: Application structure and layout
- **Key Features Used**:
  - Canvas element for Chart.js rendering
  - Meta viewport for mobile responsiveness
  - Semantic structure with divs and sections

### CSS3
- **Framework**: Tailwind CSS (via CDN)
- **Version**: Latest (loaded from cdn.tailwindcss.com)
- **Custom Styling**:
  - Backdrop filters for glassmorphism effects
  - Custom range slider styling (WebKit-specific)
  - Transition animations for panel movements
  - Responsive utilities for mobile-first design
- **Key Techniques**:
  - Utility-first approach with Tailwind classes
  - Custom CSS for complex components (sliders, charts)
  - CSS transforms for smooth animations
  - Flexbox and Grid for layouts

### JavaScript (ES6+)
- **Version**: Modern ES6+ (Classes, Arrow Functions, Async/Await)
- **Paradigm**: Object-Oriented with Functional elements
- **Key Features Used**:
  - ES6 Classes for service architecture
  - Async/Await for API calls
  - Arrow functions for callbacks
  - Template literals for dynamic HTML generation
  - Destructuring for cleaner code
  - Array methods (map, filter, forEach, splice)
  - Spread operator for array cloning
  - DOM manipulation (createElement, innerHTML, classList)
  - Event listeners (addEventListener, onclick)
  - FileReader API for GPX parsing
  - DOMParser for XML parsing

### C# (Minimal)
- **Version**: C# 11 (.NET 8.0)
- **Purpose**: Development hosting wrapper only
- **Usage**: Minimal console application for project structure

## Frontend Libraries

### Leaflet
- **Version**: 1.9.4
- **Purpose**: Interactive map rendering
- **Source**: unpkg.com CDN
- **Features Used**:
  - Map initialization and controls
  - Marker management with custom icons
  - Polyline drawing for routes
  - Feature groups for segment management
  - Event handling (click, pan)
  - Bounds fitting for route display

### Chart.js
- **Version**: Latest (via jsdelivr CDN)
- **Purpose**: Elevation profile visualization
- **Features Used**:
  - Line chart with area fill
  - Custom interaction modes (index, non-intersect)
  - Dynamic data updates with performance mode ('none')
  - Hover events for map synchronization (onHover callback)
  - Axis scaling and panning (min/max control)
  - Responsive canvas rendering (maintainAspectRatio: false)
  - Segment-based styling (segment.borderColor and backgroundColor)
  - Custom canvas event listeners for touch/mouse gestures
  - Independent chart instances with separate view states

### Font Awesome
- **Version**: 6.4.0
- **Purpose**: Icon library
- **Source**: cdnjs.cloudflare.com
- **Usage**: UI icons for buttons and indicators

### Tailwind CSS
- **Version**: Latest (JIT compiler via CDN)
- **Purpose**: Utility-first CSS framework
- **Features Used**:
  - Responsive design utilities
  - Color system and theming
  - Spacing and sizing utilities
  - Flexbox and Grid utilities
  - Transition and animation classes

## External APIs

### Nominatim (OpenStreetMap)
- **Endpoint**: https://nominatim.openstreetmap.org/search
- **Purpose**: Geocoding and address autocomplete
- **Format**: JSON
- **Usage**: Convert text addresses to coordinates

### OSRM (Open Source Routing Machine)
- **Endpoint**: https://router.project-osrm.org/route/v1/driving/
- **Purpose**: Route calculation between points
- **Format**: GeoJSON
- **Features**: Full geometry, driving profile

### Open-Elevation API
- **Endpoint**: https://api.open-elevation.com/api/v1/lookup
- **Purpose**: Elevation data for route coordinates
- **Method**: POST with JSON body
- **Sampling**: Limited to 500 points for performance
- **Fallback**: Mock data generation on API failure (sine wave pattern)
- **Headers**: Content-Type and Accept application/json

## Build System

### .NET SDK
- **Version**: .NET 8.0
- **Project Type**: Console Application
- **Build Tool**: MSBuild (via Visual Studio)
- **Configuration**:
  - ImplicitUsings: Enabled
  - Nullable: Enabled
  - Target Framework: net8.0

### Project Files
- **CyclingTracker.csproj**: Minimal project configuration
- **CyclingTracker.sln**: Visual Studio solution file
- **No NuGet packages**: Pure client-side application

## Development Environment

### IDE Support
- **Primary**: Visual Studio 2022 (Version 17.14+)
- **Solution Format**: Visual Studio 2022
- **Minimum Version**: Visual Studio 2019 (10.0.40219.1)

### Browser Requirements
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Required Features**:
  - ES6+ JavaScript support (Classes, Async/Await, Arrow Functions)
  - Geolocation API (watchPosition with high accuracy)
  - Canvas API (for Chart.js rendering)
  - Fullscreen API (requestFullscreen/exitFullscreen)
  - Fetch API (for external API calls)
  - CSS Grid and Flexbox
  - FileReader API (for GPX file reading)
  - DOMParser (for XML parsing)
  - Touch Events (for mobile gesture support)

## Development Commands

### Build
```bash
dotnet build
```

### Run (Development)
```bash
dotnet run
```

### Clean
```bash
dotnet clean
```

## Deployment

### Static Hosting
- **Files Required**: index.html only
- **Server Requirements**: Any static file server
- **No Build Step**: Direct deployment of HTML file
- **CDN Dependencies**: All libraries loaded at runtime

### Hosting Options
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any web server (Apache, Nginx, IIS)

## Performance Considerations

### Optimization Techniques
- **Debouncing**: 500ms delay on autocomplete input
- **Sampling**: Elevation data limited to 500 points
- **Lazy Loading**: Libraries loaded via CDN
- **Event Throttling**: Geolocation updates controlled by browser
- **Efficient Rendering**: Chart updates use Chart.js update() method with 'none' mode for performance
- **Segment Coloring**: Dynamic segment colors using Chart.js segment styling API

### Mobile Optimization
- **Viewport**: Configured for mobile devices
- **Touch Events**: Full touch gesture support (drag to pan on charts)
- **Responsive Design**: Mobile-first approach
- **Performance**: Minimal JavaScript bundle (single file)
- **Custom Scrollbars**: Visible scrollbars for segment lists on mobile

## Security Considerations

### API Usage
- **Public APIs**: All APIs are public and CORS-enabled
- **No Authentication**: No API keys or tokens required
- **Client-Side Only**: No server-side secrets

### Browser APIs
- **Geolocation**: Requires user permission
- **Fullscreen**: Requires user gesture
- **HTTPS**: Recommended for Geolocation API

## Version Control

### Git Configuration
- **Solution GUID**: {DC42CB8B-3D48-40BD-AAAC-7400F94E9235}
- **Project GUID**: {5E67C903-41C4-46CC-9FB5-7FC8BA4E77B4}

## Future Technology Considerations

### Potential Enhancements
- Service Worker for offline support
- IndexedDB for route history
- Web Workers for heavy calculations
- Progressive Web App (PWA) manifest
- TypeScript for type safety
- Build tooling (Vite, Webpack) for optimization
