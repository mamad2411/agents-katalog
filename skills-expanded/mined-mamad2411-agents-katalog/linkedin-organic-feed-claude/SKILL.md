# LinkedIn Organic Feed - Chrome Extension

## Project Overview

Chrome extension to filter algorithmic content from LinkedIn feed, showing only genuine organic posts from connections.

**Version:** 0.1.0 (Semantic Versioning)
**Status:** Working - filters suggested posts on LinkedIn feed

## Project Philosophy

This is a **minimal, Spartan learning project** focused on:
- Learning Chrome extension development
- Solving one specific problem: removing suggested posts from LinkedIn feed
- Writing clean, readable code for public showcase
- No gold plating, no premature optimization, no feature creep

The codebase will be shared on LinkedIn as an educational resource. Every line of code should be justified and purposeful.

## Technology Stack

**Language:** TypeScript
**Target:** Chrome Extensions Manifest V3
**Build Tool:** Webpack 5
**Package Manager:** npm

### Rationale

- TypeScript provides type safety and modern OOP features
- Manifest V3 is the current Chrome extension standard (V2 deprecated January 2024)
- Webpack enables TypeScript compilation, bundling, and development workflow
- Chrome Extensions API is well-documented and stable

## Architecture

### Component Overview

```
linkedin-organic-feed/
├── src/
│   ├── content/
│   │   ├── ContentScript.ts        # Main orchestrator (v0.1.0)
│   │   ├── DOMObserver.ts          # Monitors feed changes (v0.1.0)
│   │   └── filters/
│   │       ├── FilterStrategy.ts   # Interface (v0.1.0)
│   │       ├── SuggestedFilter.ts  # Filters suggested posts (v0.1.0)
│   │       └── FilterRegistry.ts   # Manages filters (simplified for v0.1.0)
│   ├── background/
│   │   └── ServiceWorker.ts        # Minimal lifecycle handling (v0.1.0)
│   ├── popup/
│   │   ├── PopupController.ts      # Simple toggle UI (v0.1.0)
│   │   ├── popup.html              # Minimal UI (v0.1.0)
│   │   └── popup.css               # Basic styling (v0.1.0)
│   ├── storage/
│   │   └── SettingsManager.ts      # Chrome storage (single boolean) (v0.1.0)
│   └── types/
│       └── index.ts                # Minimal type definitions (v0.1.0)
├── public/
│   ├── manifest.json               # Manifest V3 (v0.1.0)
│   └── icons/                      # Simple icon set (v0.1.0)
├── dist/                            # Build output (gitignored)
├── webpack.config.js               # Build config with source maps (v0.1.0)
├── tsconfig.json                   # TypeScript strict mode (v0.1.0)
├── package.json                    # Dependencies (v0.1.0)
├── generate-icons.js               # Icon generator using Sharp
├── icon-template.svg               # SVG icon source
├── .gitignore                      # Standard ignores (v0.1.0)
├── CLAUDE.md                       # This architecture document
└── README.md                       # User-facing documentation
```

**v0.1.0 Implementation:**
- `FilterRegistry` manages only one filter (SuggestedFilter)
- `SettingsManager` stores single boolean (enabled/disabled)
- No statistics, no per-filter configuration
- Popup shows only master ON/OFF toggle
- CSS-based hiding for performance
- `requestAnimationFrame` scheduling for efficient DOM observation

### Core Components

#### 1. Content Script (`ContentScript.ts`)

**Responsibility:** Entry point injected into LinkedIn pages, orchestrates filtering.

**Key Methods:**
- `initialize()`: Sets up DOM observation and filter registry
- `applyFilters()`: Iterates through feed posts and applies active filters
- `handleStateChange()`: Responds to extension toggle events

#### 2. DOM Observer (`DOMObserver.ts`)

**Responsibility:** Monitors LinkedIn feed for dynamic content changes.

**Implementation:**
- Uses `MutationObserver` API to watch feed container
- Detects new posts added by infinite scroll
- Uses `requestAnimationFrame` for efficient scheduling (faster than debounce)
- Prevents duplicate callbacks during same animation frame

#### 3. Filter System

**Pattern:** Strategy Pattern

##### `FilterStrategy` (Interface)
```typescript
interface FilterStrategy {
  name: string;
  enabled: boolean;
  matches(element: HTMLElement): boolean;
  hide(element: HTMLElement): void;
}
```

##### `SuggestedFilter` (Implementation)
**Responsibility:** Identifies and hides LinkedIn's suggested posts.

**Detection Strategy:**
1. Check LinkedIn metadata area (actor description classes) for "Suggested" text
2. Fallback to aria-label attributes
3. Does NOT check post content body (avoids false positives)

**Supported Languages:**
- English: "Suggested"
- Spanish: "Sugerido"
- French: "Suggéré"
- German: "Vorgeschlagen"

##### `FilterRegistry`
**Responsibility:** Manages all filter instances, handles enable/disable state.

**Methods:**
- `register(filter: FilterStrategy): void`
- `getActiveFilters(): FilterStrategy[]`
- `updateFilterState(name: string, enabled: boolean): void`

#### 4. Settings Manager (`SettingsManager.ts`)

**Responsibility:** Abstracts Chrome storage API for settings persistence.

**Methods:**
- `getSettings(): Promise<Settings>`
- `updateSettings(settings: Partial<Settings>): Promise<void>`
- `onSettingsChanged(callback: (settings: Settings) => void): void`

#### 5. Service Worker (`ServiceWorker.ts`)

**Responsibility:** Background process for extension lifecycle events.

**Functions:**
- Listen for installation/update events
- Handle toolbar icon clicks
- Manage extension state across browser sessions
- No filtering logic (violates Manifest V3 architecture)

#### 6. Popup UI (`PopupController.ts`)

**Responsibility:** Manages extension popup interface.

**Features (v0.1.0):**
- Single master toggle (enable/disable extension)
- Visual indicator of current state
- Sync with `SettingsManager`

**Future features:** Individual filter toggles, statistics display

### Data Flow

```
User Visits LinkedIn
    ↓
ContentScript Initializes
    ↓
DOMObserver Watches Feed Container
    ↓
New Posts Detected (MutationObserver)
    ↓
ContentScript → FilterRegistry.getActiveFilters()
    ↓
For Each Filter → matches(element)
    ↓
If Match → hide(element)
```

### Settings Structure (v0.1.0)

```typescript
interface Settings {
  enabled: boolean;  // Master toggle only
}
```

**Note:** Future versions will expand to include per-filter settings and statistics.

## DOM Detection Strategy

### LinkedIn Post Identification

LinkedIn's DOM structure uses:
- Feed container: `div.feed-shared-update-v2`
- Post wrapper: `div[data-urn]` attributes
- Suggested posts markers:
  - Span/div containing "Suggested" text
  - `aria-label` attributes with suggestion indicators
  - Class patterns like `feed-shared-actor__description`

### Detection Approach

1. **Primary:** DOM attribute selectors (most reliable)
2. **Secondary:** Text content pattern matching
3. **Tertiary:** Structural heuristics (class name patterns)

**Robustness:**
- Multiple detection methods provide fallback resilience
- Configurable selectors stored in filter classes (easy updates)
- Future consideration: Rule-based selector updates via remote config

## Key Design Principles

### 1. Separation of Concerns
- Content filtering logic separate from DOM observation
- UI state management separate from storage
- Each filter is independent and self-contained

### 2. Strategy Pattern for Filters
- Easy to add new filter types (anniversaries, promotions, etc.)
- Each filter encapsulates its detection logic
- Enable/disable filters independently

### 3. Observer Pattern for DOM Changes
- Decouple DOM monitoring from filtering execution
- Efficient handling of LinkedIn's dynamic content loading
- Performance optimization through debouncing

### 4. Single Responsibility
- Each class has one clear purpose
- No god objects or kitchen-sink utilities
- Testable components with minimal dependencies

### 5. Dependency Injection
- `FilterRegistry` receives filter instances
- `ContentScript` receives `DOMObserver` and `FilterRegistry`
- Facilitates unit testing with mocks

## Performance Considerations

### 1. Efficient Scheduling
- `requestAnimationFrame` instead of debounce (synced with browser rendering)
- Prevents multiple filter runs in same frame
- Typical latency: ~16ms vs 100-300ms debounce

### 2. CSS-Based Hiding
- Injected CSS rule for `display: none` on marked elements
- No JavaScript style manipulation per element
- Browser handles hiding efficiently

### 3. Targeted Selectors
- Only queries `[data-urn]` elements (LinkedIn posts)
- Specific class selectors for metadata area
- Avoids scanning entire post content

### 4. Memory Management
- Clean up event listeners on extension disable
- Disconnect `MutationObserver` when not needed
- Remove injected CSS on disable
- Clear processing markers for clean state reset

### 5. Prevents Re-Processing
- `data-lof-processed` attribute marks checked posts
- `data-lof-hidden` attribute marks hidden posts
- Skip already-processed elements

## Security & Privacy

### 1. No Data Collection
- All filtering happens locally
- No external API calls
- No telemetry or analytics

### 2. Minimal Permissions
- `activeTab`: Access current tab only when extension activated
- `storage`: Persist user settings
- `scripting`: Inject content script (Manifest V3 requirement)

### 3. Content Security Policy
- Strict CSP in manifest.json
- No inline scripts or eval()
- No remote code execution

## Testing Strategy

### Unit Tests
- Filter detection logic (mocked DOM elements)
- Settings manager (mocked Chrome storage)
- Filter registry state management

### Integration Tests
- Content script with DOM observer
- End-to-end settings flow

### Manual Testing
- Test on LinkedIn feed with various content types
- Verify performance with infinite scroll
- Cross-browser compatibility (Chrome, Edge)

## Future Extensibility

### Additional Filters (Phase 2+)
- Work anniversaries
- Job changes
- Promoted posts
- "People you may know"
- Polls
- Collaborative articles

### Advanced Features
- Whitelist specific accounts (always show)
- Keyword-based filtering
- Custom filter rules (power users)
- Export/import filter configurations

### Architecture Support
- New filters implement `FilterStrategy` interface
- Register in `FilterRegistry`
- Add toggle in popup UI
- Update `Settings` interface

No changes to core architecture required for new filters.

## Development Workflow

### Setup
```bash
npm install
npm run build:dev    # Development build with source maps
npm run watch        # Auto-rebuild on file changes
```

### Testing
```bash
npm run test         # Jest unit tests
npm run lint         # ESLint + TypeScript checks
```

### Production Build
```bash
npm run build:prod   # Minified production bundle
```

### Loading in Chrome
1. Navigate to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `dist/` directory

## Architecture Decisions

### 1. Filter Behavior
**Decision:** CSS-based hiding via `data-lof-hidden` attribute and CSS rule
**Rationale:** Better performance than inline style manipulation, cleaner state management

### 2. Scheduling Strategy
**Decision:** `requestAnimationFrame` instead of debounce/throttle
**Rationale:** Syncs with browser rendering cycle, faster response (~16ms), prevents redundant work

### 3. Detection Scope
**Decision:** Only check LinkedIn metadata area, not post body content
**Rationale:** Avoids false positives (e.g., user writes "suggested" in their post)

### 4. Webpack Configuration
**Decision:** Use `cheap-module-source-map` instead of default `eval`
**Rationale:** Manifest V3 Content Security Policy blocks `eval()`, source maps still available for debugging

### 5. False Positive Prevention
**Decision:** Target specific CSS selectors for LinkedIn's actor description area
**Rationale:** Balance between detection accuracy and avoiding collateral hiding

### 6. Icon Generation
**Decision:** Use Sharp library for SVG→PNG conversion with transparency
**Rationale:** macOS `qlmanage` was adding white backgrounds, Sharp properly preserves alpha channel

### 7. Minimalism Trade-off
**Decision:** Keep Strategy pattern and separate classes despite being "over-architected" for one filter
**Rationale:** Code clarity and educational value for public showcase outweigh file count reduction

## v0.1.0 Scope (Minimal Release)

### In Scope
- Single filter: Suggested posts only
- Simple toggle in popup (ON/OFF for entire extension)
- CSS-based hiding with `display: none`
- Structural DOM detection (metadata area only, not post content)
- TypeScript + Webpack 5 build system
- Manifest V3 compliance
- Green LinkedIn icon with transparent background
- Multilingual support (EN, ES, FR, DE)
- Performance-optimized with `requestAnimationFrame`
- Clean, documented code

### Explicitly Out of Scope
- Multiple filters (anniversaries, promotions, etc.)
- Statistics tracking
- Per-filter configuration
- Visual feedback/placeholders ("X posts hidden")
- Auto-update mechanisms
- Unit tests (will be added post-v0.1.0)
- Settings export/import
- Whitelist functionality

### Success Criteria (All Met)
✓ Extension loads in Chrome without errors
✓ Suggested posts are hidden on LinkedIn feed
✓ Toggle works and persists across sessions
✓ No false positives (user posts with "suggested" text remain visible)
✓ Minimal flash when scrolling (< 20ms with requestAnimationFrame)
✓ Code is readable and well-structured for showcase
✓ Ready for LinkedIn article discussion

## Versioning Strategy

**Current:** 0.1.0
**Scheme:** Semantic Versioning (semver.org)

- **MAJOR:** Breaking changes to extension behavior or API
- **MINOR:** New filters or features (backward compatible)
- **PATCH:** Bug fixes, performance improvements

## Conclusion

This is a **minimal learning project** designed to teach Chrome extension development while solving a real problem. The architecture is intentionally simple for v0.1.0 but structured to allow future extensibility. Code quality and readability are prioritized over features.

The extension will serve as:
1. A functional tool to remove suggested posts from LinkedIn
2. An educational codebase for discussing Chrome extension development
3. A portfolio piece demonstrating clean TypeScript and OOP principles
