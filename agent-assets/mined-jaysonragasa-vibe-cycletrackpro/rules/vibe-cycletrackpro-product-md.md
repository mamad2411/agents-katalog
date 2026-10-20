# Product Overview

## Project Purpose
CycleTrack Pro is a mobile-first web application designed for cyclists to plan, track, and analyze their cycling routes with advanced speed planning and real-time tracking capabilities. The application provides comprehensive route planning with elevation profiles, speed segment management, and live ride tracking.

## Value Proposition
- **Advanced Route Planning**: Plan cycling routes with customizable speed targets for different segments
- **Real-Time Tracking**: Track current speed, average speed, moving time, and ride time during active rides
- **Elevation Awareness**: Visualize elevation profiles with interactive graphs and map integration
- **Mobile-Optimized**: Designed specifically for mobile browsers with touch-friendly controls and fullscreen support
- **Map-Centric Interface**: Floating collapsible panels that keep the map as the primary focus

## Key Features

### Route Planning
- Point A to Point B route calculation using OpenStreetMap and OSRM routing
- Address autocomplete with geocoding suggestions (500ms debounce)
- Interactive map-based point selection (tap/click to set start and end points)
- Multiple waypoint support for complex routes with add/remove functionality
- Draggable markers for real-time route adjustments with automatic segment reset
- GPX file import for pre-planned routes with full parsing and elevation fetching
- Click-on-route to add waypoints dynamically with automatic rerouting
- Automatic route visualization with elevation data (500 sample points)
- Toast notifications for user feedback during route operations

### Advanced Speed Planning
- Segment-based speed planning with visual color coding (8 distinct colors)
- Adjustable speed targets (10-60 km/h) for each route segment
- Dual-slider interface for precise segment boundary control with clamping logic
- Real-time ETA and ETT calculation based on planned speeds
- Add/remove segments dynamically to customize planning (minimum 1 segment)
- Segment boundaries constrained to prevent overlap
- Real-time visual feedback with colored highlight bars
- Automatic segment adjustment when boundaries are modified
- Distance display for each segment in kilometers

### Live Ride Dashboard
- Current speed and average speed monitoring
- Dual time tracking:
  - **Moving Time**: Only counts when in motion (speed > 2 km/h)
  - **Ride Time**: Total elapsed time including stops
- Estimated Time of Arrival (ETA) based on advance planning
- Estimated Travel Time (ETT) showing remaining duration
- Dual elevation profile graphs (planner and dashboard)
- Interactive elevation profile with zoom, pan, and reset controls
- Segment visualization toggle for active graph highlighting
- Start/Pause/Resume/Stop ride controls

### Elevation Profile
- Dual charts: Planner view and Dashboard view with independent view states
- Color-coded segments matching route planner configuration (segment-based coloring)
- Interactive graph with hover-to-map synchronization (shows hover marker)
- Zoom in/out functionality for detailed elevation analysis (0.05x to 1.0x zoom)
- Pan left/right when zoomed for precise navigation (constrained panning)
- Reset view button to restore default zoom/pan (1.0 zoom, 0.0 pan)
- Touch and mouse gesture support (drag to pan on canvas)
- Real-time position marker during active rides
- Optional segment highlighting on map (dashboard only, checkbox-controlled)
- Chart updates use performance mode ('none') for smooth interactions
- Independent zoom/pan state management for each chart

### User Experience
- Collapsible floating panels with circular button indicators
- Custom modal dialogs for confirmations and alerts
- Toast notifications for user feedback
- Loading overlay with status messages
- Fullscreen mode for distraction-free riding
- "Heads Up" map orientation (north-facing) during rides
- Smooth animations and transitions
- Dark theme optimized for outdoor visibility
- Custom scrollbar styling for segment lists

## Target Users
- Recreational cyclists planning weekend rides
- Fitness enthusiasts tracking performance metrics
- Commuters optimizing route timing
- Cycling groups coordinating pace and segments
- Anyone needing detailed route planning with elevation awareness

## Use Cases
1. **Pre-Ride Planning**: Plan a route with realistic speed expectations for different terrain sections
2. **Training Sessions**: Set target speeds for interval training on specific route segments
3. **Group Rides**: Share planned routes with segment-based pace expectations
4. **Performance Analysis**: Compare planned vs actual speeds and times
5. **Commute Optimization**: Calculate accurate ETAs for daily cycling commutes
6. **Adventure Planning**: Explore new routes with elevation profiles before riding
