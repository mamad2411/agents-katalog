# Development Guidelines

## Code Quality Standards

### SOLID Principles (Strictly Enforced)
The codebase follows SOLID principles as a core architectural requirement:

1. **Single Responsibility Principle**
   - Each class has one clear, well-defined purpose
   - StateStore: Only manages state
   - MapService: Only handles map operations
   - RouteService: Only manages API calls
   - RideManager: Only tracks ride metrics
   - UIManager: Only controls UI rendering

2. **Open/Closed Principle**
   - Services are open for extension but closed for modification
   - New features added through new methods, not by changing existing ones

3. **Liskov Substitution Principle**
   - Services can be replaced with alternative implementations
   - Dependency injection allows for service swapping

4. **Interface Segregation Principle**
   - Each service exposes only necessary methods
   - No bloated interfaces with unused methods

5. **Dependency Inversion Principle**
   - High-level App class depends on abstractions (services)
   - Services receive dependencies through constructors
   - StateStore acts as the central dependency

### Separation of Concerns
- **HTML**: Structure and semantic markup only
- **CSS**: All styling, animations, and visual effects
- **JavaScript**: Behavior, logic, and interactivity
- **No inline styles**: Use Tailwind classes or custom CSS
- **No inline scripts**: All JavaScript in dedicated script block

### Code Formatting

#### JavaScript Conventions
```javascript
// Class names: PascalCase
class StateStore { }
class MapService { }

// Method names: camelCase
updateBoundary() { }
calculateTotalHours() { }

// Constants: SCREAMING_SNAKE_CASE
const SEGMENT_COLORS = [...];

// Variables: camelCase
let settingStart = true;
const totalDist = 0;

// Private-like properties: Regular camelCase (no underscore prefix)
this.store = store;
this.listeners = [];
```

#### HTML/CSS Conventions
```html
<!-- IDs: kebab-case -->
<div id="panel-planner"></div>
<button id="btn-calc-route"></button>

<!-- Classes: Tailwind utilities + custom classes -->
<div class="bg-gray-900/95 border-t border-gray-700 rounded-t-2xl"></div>

<!-- Data attributes: kebab-case -->
<div data-section-id="1"></div>
```

#### Indentation and Spacing
- **Indentation**: 4 spaces (JavaScript), 2 spaces (HTML)
- **Line breaks**: Between logical sections
- **Spacing**: Space after keywords (if, for, while)
- **Braces**: Same line for opening brace

### Naming Conventions

#### Descriptive and Purposeful
```javascript
// Good: Clear purpose
const startRatio = 0.0;
const endRatio = 1.0;
updateBoundary(boundaryIndex, newVal, isStartSlider)

// Avoid: Ambiguous names
const x = 0.0;
const y = 1.0;
update(i, v, b)
```

#### Element ID Patterns
- **Panels**: `panel-{name}` (panel-planner, panel-dashboard)
- **Buttons**: `btn-{action}` (btn-calc-route, btn-add-section)
- **Inputs**: `input-{field}` (input-start, input-end)
- **Values**: `val-{metric}` (val-speed, val-eta)
- **Text displays**: `txt-{field}-{index}` (txt-start-0, txt-end-1)
- **Sliders**: `slider-{type}-{index}` (slider-start-0, slider-end-1)

## Architectural Patterns

### Service-Oriented Architecture

#### Service Creation Pattern
```javascript
class ServiceName {
    constructor(dependencies) {
        // Store dependencies
        this.store = dependencies.store;
        this.otherService = dependencies.other;
        
        // Initialize internal state
        this.internalProperty = null;
    }
    
    // Public methods
    publicMethod() {
        // Implementation
    }
    
    // Helper methods (not truly private, but intended as internal)
    helperMethod() {
        // Implementation
    }
}
```

#### Dependency Injection Pattern
```javascript
class App {
    constructor() {
        // 1. Create state store first
        this.store = new StateStore();
        
        // 2. Create services with dependencies
        this.map = new MapService('map', this.store);
        this.route = new RouteService(this.store);
        
        // 3. Pass 'this' for cross-service communication
        this.ride = new RideManager(this);
        this.ui = new UIManager(this);
    }
}
```

### Observer Pattern (State Management)

#### State Store Implementation
```javascript
class StateStore {
    constructor() {
        this.state = { /* initial state */ };
        this.listeners = [];
    }
    
    subscribe(listener) {
        this.listeners.push(listener);
    }
    
    update(key, value) {
        this.state[key] = value;
        this.notify(key, value);
    }
    
    get(key) {
        return this.state[key];
    }
    
    notify(key, value) {
        this.listeners.forEach(l => l(key, value));
    }
}
```

#### Subscribing to State Changes
```javascript
this.store.subscribe((key, val) => this.renderUpdate(key, val));
```

### Event Handling Patterns

#### Inline Event Handlers (for simple actions)
```html
<button onclick="app.ui.togglePanel('planner')">Toggle</button>
<input oninput="app.ui.updateBoundary(0, this.value, true)">
```

#### Programmatic Event Listeners (for complex logic)
```javascript
document.getElementById('btn-calc-route').onclick = async () => {
    // Complex async logic
};

canvas.addEventListener('mousedown', e => startDrag(e.clientX));
```

## UI/UX Patterns

### Panel Management

#### Panel Structure
```html
<div id="panel-{name}" class="panel pointer-events-auto bg-gray-900/95 ... transform translate-y-full absolute bottom-0">
    <!-- Header with toggle -->
    <div class="p-4 border-b border-gray-700" onclick="app.ui.togglePanel('{name}')">
        <h2>Panel Title</h2>
        <button><i class="fas fa-chevron-down"></i></button>
    </div>
    
    <!-- Content -->
    <div class="p-4 overflow-y-auto no-scrollbar">
        <!-- Panel content -->
    </div>
</div>
```

#### Panel Toggle Logic
```javascript
togglePanel(name) {
    // Hide all panels
    Object.values(this.panels).forEach(p => p.classList.add('translate-y-full'));
    
    // Show collapsed controls
    document.getElementById('collapsed-controls').classList.remove('opacity-0');
    
    // Toggle requested panel
    if (this.activePanel === name) {
        this.activePanel = null;
    } else {
        this.activePanel = name;
        this.panels[name].classList.remove('translate-y-full');
        document.getElementById('collapsed-controls').classList.add('opacity-0');
    }
}
```

### Dynamic HTML Generation

#### Template Literal Pattern
```javascript
container.innerHTML = sections.map((s, idx) => {
    const color = SEGMENT_COLORS[idx % SEGMENT_COLORS.length];
    const canDelete = sections.length > 1;
    
    return `
        <div class="bg-gray-800 p-2 rounded-lg" style="border-left-color: ${color}">
            <div class="flex justify-between items-center">
                <span>Segment ${idx + 1}</span>
                ${canDelete ? `
                    <button onclick="app.ui.removeSegment(${idx})">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                ` : ''}
            </div>
        </div>
    `;
}).join('');
```

#### Dynamic Element Creation
```javascript
const div = document.createElement('div');
div.className = "relative waypoint-item";
div.innerHTML = `<input type="text" id="input-wp-${idx}" value="${wp.address || ''}">`;
container.appendChild(div);
```

### Responsive Design Patterns

#### Mobile-First Approach
```html
<!-- Base styles for mobile -->
<div class="w-full p-4">
    <!-- Content -->
</div>

<!-- Responsive utilities when needed -->
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
    <!-- Responsive grid -->
</div>
```

#### Touch and Mouse Support
```javascript
// Support both touch and mouse events
canvas.addEventListener('mousedown', e => startDrag(e.clientX));
canvas.addEventListener('touchstart', e => startDrag(e.touches[0].clientX), { passive: true });

canvas.addEventListener('mousemove', e => moveDrag(e.clientX));
canvas.addEventListener('touchmove', e => moveDrag(e.touches[0].clientX), { passive: true });
```

## API Integration Patterns

### Async/Await for API Calls
```javascript
async getRoute(start, end) {
    const url = `https://router.project-osrm.org/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`;
    const res = await fetch(url);
    const json = await res.json();
    
    if (json.code !== 'Ok') throw new Error("Routing failed");
    
    // Process and update state
    const coords = json.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
    this.store.update('routeGeometry', coords);
    
    return coords;
}
```

### Error Handling with Fallbacks
```javascript
try {
    const res = await fetch('https://api.open-elevation.com/api/v1/lookup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({ locations: samples })
    });
    if (!res.ok) throw new Error(`Elevation API returned ${res.status}`);
    const data = await res.json();
    this.store.update('elevationData', data.results);
} catch (e) {
    // Fallback to mock data
    const mockData = samples.map((c, i) => ({
        latitude: c.latitude,
        longitude: c.longitude,
        elevation: 50 + Math.sin(i / 5) * 30 + Math.random() * 5
    }));
    this.store.update('elevationData', mockData);
}
```

### Debouncing User Input
```javascript
let debounceTimer;
input.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    const query = e.target.value;
    if (query.length < 3) { list.classList.add('hidden'); return; }
    
    debounceTimer = setTimeout(async () => {
        const results = await this.route.geocode(query);
        // Process results
    }, 500);
});
```

## Performance Optimization

### Data Sampling
```javascript
// Limit elevation data points to 500 for performance
const targetPoints = 500;
const step = Math.max(1, Math.floor(coords.length / targetPoints));
const samples = coords.filter((_, i) => i % step === 0).map(c => ({ 
    latitude: c[0], 
    longitude: c[1] 
}));
```

### Efficient Chart Updates
```javascript
// Update chart data without recreating
this.chart.data.labels = data.map((_, i) => i);
this.chart.data.datasets[0].data = data.map(d => d.elevation);
this.chart.update(); // Efficient update method
```

### Conditional Rendering
```javascript
// Only render when necessary
if (key === 'elevationData') this.updateChart(val);
if (key === 'rideStatus') this.updateRideControls(val);
```

## Code Documentation

### Minimal Comments, Self-Documenting Code
```javascript
// Good: Code explains itself
const prevEndRatio = idx === 0 ? 0 : sections[idx - 1].endRatio;
const segmentDistKm = distKm * (s.endRatio - prevEndRatio);

// Only comment when necessary
// --- 1. Clamping Logic ---
// Min Constraint for START handle (idx-1): prev-prev end or 0
const minRatioStart = (idx > 1) ? sections[idx - 2].endRatio + 0.01 : 0.00;
```

### Section Headers for Organization
```javascript
// --- 1. STATE STORE ---
class StateStore { }

// --- 2. MAP SERVICE ---
class MapService { }

// --- 3. ROUTE SERVICE ---
class RouteService { }
```

## Testing Considerations

### Testable Service Design
- Services are independent and can be tested in isolation
- State management is centralized and predictable
- API calls can be mocked by replacing RouteService
- UI updates are reactive to state changes

### Manual Testing Checklist
1. Route planning with valid addresses and autocomplete
2. Map-based point selection (alternating start/end)
3. Waypoint addition and removal with rerouting
4. GPX file upload and parsing
5. Segment creation and deletion (minimum 1 segment enforced)
6. Speed adjustment and ETA/ETT calculation
7. Dual-slider boundary adjustment with clamping
8. Ride start/pause/resume/stop functionality
9. Elevation graph zoom and pan (both charts independently)
10. Segment highlighting on map (dashboard checkbox)
11. Mobile touch gestures (drag to pan on charts)
12. Fullscreen mode toggle
13. Draggable markers with automatic rerouting
14. Click-on-route to add waypoints
15. Toast notifications and modal dialogs
16. Loading overlay during async operations

## UI/UX Enhancement Patterns

### Toast Notifications
```javascript
showToast(msg, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = "toast bg-gray-900/90 text-white px-4 py-2 rounded-lg";
    toast.innerHTML = `<i class="fas fa-info-circle"></i><span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), duration);
}
```

### Modal Dialogs
```javascript
showModal(options) {
    document.getElementById('modal-title').innerText = options.title;
    document.getElementById('modal-message').innerText = options.message;
    this.modalCallback = options.onConfirm;
    modal.classList.remove('hidden');
}
```

### Loading Overlays
```javascript
showLoading(msg) {
    document.getElementById('loading-message').innerText = msg;
    overlay.classList.remove('hidden');
}
```

## Chart.js Advanced Patterns

### Segment-Based Coloring
```javascript
segment: {
    borderColor: (ctx) => {
        const sections = this.store.get('sections');
        const ratio = ctx.p0DataIndex / elevData.length;
        for (let i = 0; i < sections.length; i++) {
            const prevEnd = i === 0 ? 0 : sections[i - 1].endRatio;
            if (ratio >= prevEnd && ratio <= sections[i].endRatio) {
                return SEGMENT_COLORS[i % SEGMENT_COLORS.length];
            }
        }
        return '#3b82f6';
    }
}
```

### Dual Chart Management
```javascript
// Create separate charts with independent view states
this.plannerChart = this.createChart('elevationChartPlanner', 'plannerViewState');
this.dashboardChart = this.createChart('elevationChartDashboard', 'dashboardViewState');

// Update both charts simultaneously
[this.plannerChart, this.dashboardChart].forEach(chart => {
    chart.data.labels = data.map((_, i) => i);
    chart.data.datasets[0].data = data.map(d => d.elevation);
});
```

### Chart Gesture Controls
```javascript
let isDragging = false, lastX = 0;
canvas.addEventListener('mousedown', e => { isDragging = true; lastX = e.clientX; });
canvas.addEventListener('mousemove', e => {
    if (isDragging) this.panChart(chart, viewState, (lastX - e.clientX) / width * 2);
});
canvas.addEventListener('touchstart', e => startDrag(e.touches[0].clientX), { passive: true });
```

## File Handling Patterns

### GPX File Parsing
```javascript
const reader = new FileReader();
reader.onload = async (ev) => {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(ev.target.result, "text/xml");
    const trkpts = xmlDoc.getElementsByTagName("trkpt");
    const latlngs = [];
    for (let i = 0; i < trkpts.length; i++) {
        latlngs.push([parseFloat(trkpts[i].getAttribute("lat")), 
                      parseFloat(trkpts[i].getAttribute("lon"))]);
    }
};
reader.readAsText(file);
```

## Common Patterns and Idioms

### Array Manipulation
```javascript
// Filter with step for sampling
const samples = coords.filter((_, i) => i % step === 0);

// Map for transformation
const elevations = data.map(d => d.elevation);

// Slice for segments
const segmentCoords = fullRoute.slice(startIdx, endIdx + 1);
```

### Conditional Class Application
```javascript
// Ternary for conditional classes
<div class="${isFirst ? 'locked' : ''}">

// Template literal for dynamic styles
<div style="border-left-color: ${color}">
```

### State-Driven UI Updates
```javascript
renderUpdate(key, val) {
    if (key === 'currentSpeed') document.getElementById('val-speed').innerText = val.toFixed(1);
    if (key === 'avgSpeed') document.getElementById('val-avg').innerText = val.toFixed(1);
    if (key === 'rideStatus') this.updateRideControls(val);
    if (key === 'waypoints') this.renderWaypoints();
    if (key === 'elevationData') this.updateCharts(val);
}
```

### Draggable Markers with Callbacks
```javascript
const marker = L.marker(latlng, { draggable: true });
marker.on('dragend', async (e) => {
    const newPos = e.target.getLatLng();
    const pointData = await this.app.route.resolvePoint(newPos);
    this.store.update('startPoint', pointData);
    await this.app.ui.triggerRouteCalc();
});
```

## Security Best Practices

### No Sensitive Data in Client
- All API calls are to public endpoints
- No API keys or credentials in code
- No user data stored permanently

### User Permission Requests
```javascript
// Request geolocation permission
navigator.geolocation.watchPosition(
    (pos) => this.processPosition(pos),
    (err) => console.error(err),
    { enableHighAccuracy: true }
);
```

## Accessibility Considerations

### Semantic HTML
```html
<button> for interactive elements
<input> with proper type attributes
<label> for form controls (when applicable)
```

### Touch-Friendly Targets
```css
/* Minimum 44x44px touch targets */
.w-14 h-14  /* 56x56px for circular buttons */
py-3        /* Adequate padding for buttons */
```

### Visual Feedback
```javascript
// Active states for buttons
active:scale-95 transition-transform

// Hover states for interactive elements
hover:bg-blue-700
```

## Maintenance Guidelines

### Adding New Features
1. Determine which service should own the feature
2. Add state properties to StateStore if needed
3. Implement logic in appropriate service
4. Update UI to reflect new state
5. Add event listeners in App.initListeners()

### Modifying Existing Features
1. Identify the responsible service
2. Update state structure if needed
3. Modify service methods
4. Update UI rendering logic
5. Test state propagation

### Code Review Checklist
- [ ] Follows SOLID principles
- [ ] Proper separation of concerns
- [ ] Consistent naming conventions
- [ ] Error handling implemented
- [ ] Mobile-friendly interactions (touch events)
- [ ] State updates trigger UI changes
- [ ] No inline styles or scripts
- [ ] Comments only where necessary
- [ ] Chart updates use performance mode ('none')
- [ ] Modals and toasts for user feedback
- [ ] Loading states for async operations
