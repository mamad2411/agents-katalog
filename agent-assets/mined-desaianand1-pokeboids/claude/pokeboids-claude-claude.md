# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PokéBoids is an educational artificial life simulation implementing Craig Reynolds' classic boids algorithm with enhanced biological characteristics and predator-prey dynamics. Built with SvelteKit and Phaser 3, it visualizes emergent flocking behaviors using Pokémon sprites, serving as both an interactive learning tool for AI/ML concepts and a platform for behavioral experimentation.

### Key Goals

- Demonstrate emergent behaviors in complex systems through interactive visualization
- Model biological systems with realistic predator-prey dynamics
- Provide educational value for students learning about AI and complex systems
- Maintain 60 FPS performance with hundreds of active boids

## Development Commands

### Essential Commands

- `pnpm dev` - Start development server with hot module replacement
- `pnpm build` - Build production bundle
- `pnpm preview` - Preview production build locally
- `pnpm test` - Run test suite with Vitest in watch mode
- `pnpm test:run` - Run tests once (CI mode)
- `pnpm lint` - Run Prettier and ESLint checks
- `pnpm format` - Auto-format code with Prettier
- `pnpm check` - Run SvelteKit sync and type checking

### Version Management

- `pnpm version:patch` - Bump patch version
- `pnpm version:minor` - Bump minor version
- `pnpm version:major` - Bump major version
- After version bump, `scripts/update-version.js` auto-updates version across the codebase

## Architecture

### Design Philosophy

The codebase follows a **separation of concerns** principle with framework-agnostic core logic. This allows the simulation algorithms to be independent of rendering frameworks, making the code more testable and maintainable.

### Core Systems

1. **Boid System** (`src/lib/boid/`)
   - `FlockLogic` - Framework-agnostic core flocking implementation with group-based filtering
   - `PhaserFlock` - Phaser-specific wrapper managing boid lifecycle
   - `PhaserBoid` - Individual boid implementation with animation support and group IDs
   - Behaviors (`behaviors/`) - Modular behavior system using Strategy pattern:
     - `AlignmentBehavior` - Align velocity with neighbors
     - `CohesionBehavior` - Move toward center of neighbors
     - `SeparationBehavior` - Avoid crowding
     - `BoundaryAvoidanceBehavior` - Handle world boundaries (supports multiple modes)
     - `CompositeBehavior` - Combines all behaviors with configurable weights

2. **Animation System** (`src/lib/boid/animation/`)
   - `BoidAnimationController` - 8-directional sprite animation management
   - `BoidSpriteManager` - Singleton for sprite database and flavor management
   - `types.ts` - TypeScript interfaces for animation configuration
   - JSON-based sprite configuration (`src/assets/sprites/sprite-config.json`)
   - Support for 3 animation states: walk (idle), attack, hurt

3. **Spatial Partitioning** (`src/lib/boid/spatial/`)
   - `QuadTreePartitioning` - Efficient neighbor queries for O(n log n) performance
   - Critical for maintaining 60 FPS with large boid populations

4. **Game Management** (`src/lib/game/`)
   - `scenes/game.ts` - Main game scene coordinating all managers
   - Managers:
     - `BackgroundManager` - Day/night cycle and backgrounds
     - `DebugManager` - Debug visualization (FoV cones, statistics)
     - `EffectsManager` - Visual effects (collision flashes, etc.)
     - `ObstacleManager` - World boundary management

5. **Strategy System** (`src/lib/strategies/`)
   - `SimulationModeStrategyFactory` - Creates behavior strategies for different simulation modes
   - `UIDisplayStrategyFactory` - Creates UI display strategies for conditional rendering
   - Concrete strategies: `SimpleBoidsStrategy`, `PredatorPreyStrategy`, `SimpleBoidsUIStrategy`, `PredatorPreyUIStrategy`
   - Clean separation between Simple Boids and Predator-Prey modes without if/else chains

6. **Event System** (`src/lib/events/`)
   - `EventBus` - Central event bus for decoupled communication
   - Type-safe events for simulation control, boid updates, flavor changes, and UI interactions
   - Enables loose coupling between UI and game logic

7. **UI Components** (`src/lib/components/`)

   **New Architecture (Post-Major Refactoring)**:
   - `dock/FloatingDock.svelte` - Central control hub with theme switcher, controls, help, and audio buttons
   - `onboarding/WelcomeDialog.svelte` - Comprehensive onboarding system with tabbed tutorial
   - `shared/` - Reusable components (ParameterSlider, TabInfoPopover, ThemeSwitcher)
   - `sidebar/` - Organized sidebar panels in dedicated subdirectories
     - `SidebarLayout.svelte` - Responsive sidebar system with mobile drawer support
     - `sim-panel/` - Simulation controls (playback, population, speed, flavor, boundary modes)
     - `boid-config-panel/` - Real-time parameter adjustment panels
     - `stats-panel/` - FPS monitoring, population counts, and event debug panel
     - `credits-panel/` - Proper attributions for sprites and research references
   - `ui/` - shadcn-svelte components for consistent design system

   **Technical Improvements**:
   - **ResponsiveDialog**: Enhanced responsive dialog component with nested drawer support, optimized snap points, and proper full-screen sizing
   - **Nested Drawer System**: Clean implementation using Svelte 5 snippets and `nested` prop for mobile dialogs within sidebar drawers
   - **Sprite Frame Extraction** (`sprite-frame-extractor.ts`): New utility for dynamic sprite display in onboarding
   - **Enhanced Theme Integration**: Seamless theme switching with improved visual feedback
   - **Mobile Optimization**: Better responsive design with touch-friendly controls and improved drawer UX

### Adapter Pattern

The project uses dependency injection via adapters (`src/lib/adapters/`) to decouple core logic from Phaser:

- `phaser-vector.ts` - Vector math implementation
- `phaser-system.ts` - System services (random, time, physics)
- `phaser-events.ts` - Event emitter wrapper

### State Management

- **Svelte 5 Runes** (`src/lib/config/simulation-signals.svelte.ts`) - Reactive state for UI controls
  - CRITICAL: Only use Svelte 5 runes syntax - NEVER use Svelte stores or Svelte 4 patterns
  - Use `$state`, `$derived`, `$effect` for reactive state management
- **Phaser Signals** (`src/lib/game/phaser-signals.svelte.ts`) - Game state synchronization

## Testing Strategy

Tests use Vitest with JSDOM environment. Key patterns:

- Mock implementations in `tests/implementations/` for framework-agnostic testing
- Unit tests alongside source files (`*.test.ts`)
- Test utilities in `tests/utils/` for common setup

Run specific test:

```bash
pnpm test -- alignment-behavior
```

## Path Aliases

The project uses path aliases for clean imports:

- `$components` → `src/lib/components`
- `$boid` → `src/lib/boid`
- `$game` → `src/lib/game`
- `$config` → `src/lib/config`
- `$events` → `src/lib/events`
- `$interfaces` → `src/lib/interfaces`
- `$strategies` → `src/lib/strategies`
- `$adapters` → `src/lib/adapters`
- `$utils` → `src/lib/utils`
- `$ui` → `src/lib/components/ui`
- `$sidebar` → `src/lib/components/sidebar`
- `$shared` → `src/lib/components/shared`
- `$tests` → `tests`

## Key Implementation Details

### Boid Behavior Flow

1. `PhaserFlock.update()` called each frame
2. `FlockLogic.update()` processes all boids:
   - Updates spatial partitioning (QuadTree)
   - Finds neighbors for each boid (considering field of view and group IDs)
   - Calculates forces via `CompositeBehavior`
   - Applies forces to boids
3. `PhaserBoid.syncWithPhaser()` updates sprite positions and animations

### Field of View System

The simulation implements biologically-inspired vision patterns:

- **Predators**: Narrow FoV (70% of base) with extended perception range (130%)
- **Prey**: Wide FoV (130% of base) with reduced perception range (80%)
- Visual debugging available with FoV cone visualization
- Configurable base FoV angle via UI controls

### Event-Driven Architecture

- UI controls emit events → Game scene listens and updates
- Game state changes emit events → UI components react
- Decouples UI from game logic for maintainability
- Type-safe event definitions prevent runtime errors

### Animation System

The boids support 8-directional sprite animations with multiple states:

- **Animation Controller**: Manages direction mapping from velocity vectors
- **Sprite States**: walk (idle), attack, hurt with proper state machine
- **Group-based Flocking**: Boids only flock with same-group members
- **JSON Configuration**: Sprite sheets and timing data in `src/assets/sprites/sprite-config.json`
- **Flavor Support**: Air, land, water environments with different sprite sets

### Performance Optimizations

- QuadTree spatial partitioning for efficient neighbor queries (O(n log n) vs O(n²))
- Animation key caching to avoid string concatenation in update loops
- Group-based neighbor filtering reduces flocking calculations
- Configurable perception/separation radii to limit calculations
- GPU-accelerated rendering via Phaser 3

## Current Development Status (v1.3.0+)

### Completed Features ✅

- **Core flocking behaviors** (alignment, cohesion, separation) with real-time parameter adjustment
- **Framework-agnostic architecture** with adapter pattern for maintainable, testable code
- **Spatial partitioning** using QuadTree for O(n log n) performance with large populations
- **Field of view perception system** with biologically-inspired predator/prey vision patterns
- **Animation system** with 8-directional sprite support and state machine (walk, attack, hurt)
- **Group-based flocking** with auto-generated group IDs for species-specific behavior
- **Environment flavor system** (air/land/water) with UI controls and themed backgrounds
- **JSON-based sprite configuration** system for dynamic sprite management
- **FloatingDock control system** - new central control hub replacing static sidebar approach
- **WelcomeDialog onboarding** - comprehensive tutorial system with tabbed interface (Intro, Creatures, Controls, Tips)
- **Responsive UI architecture** with new component organization (dock/, onboarding/, shared/, sidebar/)
- **Event-driven state management** with centralized EventBus and type-safe communication
- **Professional CI/CD pipeline** with automated testing, semantic versioning, and GitHub Pages deployment
- **Theme integration** with automatic day/night backgrounds and seamless theme switching
- **Semantic versioning system** with automated version management

### Biological Features - Scaffolding Present but Non-Functional ⚠️

**Current Status**: Progress made on biological systems with collision work completed:

- **✅ Predator-prey combat**: Collision detection and damage dealing now functional with proper event system
- **✅ Attack/hurt animations**: Animation states properly trigger during encounters with visual feedback
- **✅ Health/stamina system**: Damage system working with proper event emission and visual effects
- **❌ Death mechanics**: No system to remove boids when health reaches zero
- **❌ Reproduction system**: Progress tracking exists but no actual boid creation occurs
- **❌ Visual feedback**: No health/stamina indicators or damage effects visible to user (beyond hit flashes)

### Critical Priority - Biological System Activation 🔥

Remaining high priority biological system tasks:

- **Add death mechanics** to remove boids when health reaches zero
- **Activate reproduction system** to create new boids when thresholds are met
- **Add visual health indicators** in UI or on boids themselves (health bars, status indicators)
- **Enhance visual feedback** beyond collision flashes (health/stamina UI elements)

### Known Issues

- Frame rate drops with very large boid populations
- Memory usage spikes during reproduction events
- ~~Some boundary collision edge cases~~ ✅ **FIXED**: Boundary collision prevention now robust with position clamping

## Current Development Priorities

### Immediate Tasks (From TODO.md)

**✅ COMPLETED: Welcome Dialog & Startup Flow (Task #1)**

- Strategy pattern implementation for clean mode separation
- UI display strategies for conditional component rendering
- Mode switching with confirmation dialogs and restart behavior
- Session-based welcome dialog management

**✅ COMPLETED: Simulation Runtime & Stats (Task #2)**

- Runtime timer now pauses when simulation pauses (tracks active runtime only)
- Granular runtime formatting with hybrid approach (MM:SS under 1hr, adaptive format above)

**✅ COMPLETED: Boid Collisions & Hit Effects (Task #3)**

- Enhanced EffectsManager with priority-based effect queue system
- Standardized white flash colors for all collision types (boundary and hurt effects)
- Fixed event architecture with clean BoidBehavior → PhaserBoid event translation
- Improved hurt animation integration with automatic triggering via takeDamage()
- Strengthened boundary collision prevention with position clamping and velocity reflection
- Maintained comprehensive type safety with proper TypeScript interfaces

**1. UI: Drawer, Layout & Nested Drawers ✅ COMPLETED**

- Fixed responsive drawer full-screen issues and snap points
- Configured nested drawer support for mobile (Reset, Restart, Change Environment dialogs)
- Implemented clean nested drawer pattern using Svelte 5 snippets and `nested` prop
- Optimized drawer sizing with proper height constraints and improved snap points

**2. Panels & Settings ✅ COMPLETED**

- ✅ Renamed "Fun" tab to "Advanced Settings"
- ✅ Moved Boundary Settings to Advanced Settings tab
- ✅ Added Predator-Prey Mechanics toggle with proper mode switching
- ✅ Integrated with existing event system and UI patterns

**3. Slider Labels & User Guidance**

- Add concise explanatory labels under sliders for user comprehension

### Critical Priority - Biological System Activation 🔥

Transform existing scaffolding into functional gameplay:

- **Fix predator-prey collision detection** and make attacks actually work
- **Activate combat animations** to trigger properly during encounters
- **Implement working damage system** with visual feedback
- **Add death mechanics** to remove boids when health reaches zero
- **Complete reproduction system** to spawn new boids

## Important Constraints

1. **Framework Requirements**
   - MUST use Svelte 5 runes syntax exclusively (no stores)
   - Use latest Phaser 3 syntax only
   - Strict TypeScript with no implicit any
   - shadcn-svelte@next for Svelte 5 compatibility

2. **Performance Targets**
   - Maintain 60 FPS with 100+ boids
   - Efficient memory management
   - GPU acceleration where possible

3. **Code Quality**
   - Interface-driven development
   - Comprehensive test coverage
   - Clean separation of concerns
   - Type-safe event system

4. **Development Infrastructure**
   - **CI/CD Pipeline**: Automated testing, building, and deployment with GitHub Actions
   - **Semantic Release**: Automated version management following SemVer 2.0.0
   - **GitHub Pages**: Static site deployment with custom domain support
   - **Quality Gates**: ESLint, Prettier, TypeScript checks, and comprehensive testing

5. **Commit Guidelines**
   - NEVER add Claude as a contributor to commits
   - NO mentions of Claude in commit messages or footers
   - Use clean, conventional commit format only
