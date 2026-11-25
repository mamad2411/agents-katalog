---
name: tablefinder-pro
description: Real-time restaurant and cafe table availability platform with 3D visualization, staff admin panel, and cross-tab live sync. Use this skill when building IoT-connected venue management systems, real-time occupancy dashboards, or interactive 3D floor plan viewers.
---

# TableFinder Pro

A real-time table availability platform for restaurants and cafes with interactive 3D floor plans.

## When to Use

- Building a real-time occupancy or availability dashboard
- Creating interactive 3D venue visualizations with Three.js
- Implementing cross-tab state synchronization (BroadcastChannel + localStorage)
- Designing staff/admin toggle interfaces for physical spaces
- Prototyping IoT sensor integrations for table/seat detection

## Architecture

The project uses a shared data layer (`js/data.js`) that synchronizes state between:
- **Customer view** (`index.html`) — 3D floor plan with live table status
- **Admin panel** (`admin.html`) — Tap-to-toggle interface for restaurant staff

State flows through `localStorage` + `BroadcastChannel` for instant cross-tab updates with no backend required.

## Key Patterns

### Cross-Tab Sync
```javascript
const channel = new BroadcastChannel('tablefinder-sync');
// Writer (admin)
channel.postMessage({ type: 'venues-updated', venues });
// Listener (customer)
channel.onmessage = (e) => { if (e.data.type === 'venues-updated') render(); };
```

### 3D Table Rendering (Three.js)
Tables are rendered as interactive 3D objects with:
- Color-coded status (green=empty, red=occupied, yellow=reserved)
- Size scaling based on seat count
- Raycaster click detection for table selection
- Orbit controls for camera rotation/zoom

### Admin Toggle Pattern
Single-tap toggles between states with bulk action support:
```javascript
function toggleTable(venueId, tableId) {
    const venues = loadVenues();
    const table = findTable(venues, venueId, tableId);
    table.status = table.status === 'empty' ? 'occupied' : 'empty';
    saveAndBroadcast(venues);
}
```

## File Structure

```
tablefinder-pro/
├── index.html      # Customer 3D viewer
├── admin.html      # Staff toggle panel
├── js/data.js      # Shared state layer
├── SKILL.md        # This file
├── README.md       # Documentation
└── LICENSE          # MIT
```

## Tech Stack

- Three.js r128 for 3D rendering
- Vanilla JavaScript (no build step)
- BroadcastChannel API for real-time sync
- localStorage for persistent state
- DM Sans + JetBrains Mono typography
