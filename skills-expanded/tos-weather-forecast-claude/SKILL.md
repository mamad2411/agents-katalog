# TelemetryOS SDK Reference

**Application:** [Your App Name]
**Purpose:** [What this application does]

## Platform Architecture

TelemetryOS applications are web apps that run on digital signage devices. Applications have up to 4 components:

1. **Render** (`/render`) - Content displayed on devices (runs on device in Chrome/iframe)
2. **Settings** (`/settings`) - Config UI in Studio admin portal (runs in Studio browser)
3. **Workers** (optional) - Background JavaScript (runs on device, no DOM)
4. **Containers** (optional) - Docker containers for backend services (runs on device)

**Runtime Environment:**
- Chrome browser (platform-controlled version)
- Iframe sandbox execution
- Client-side only (no SSR, no Node.js APIs)
- Modern web APIs available (Fetch, WebSockets, WebGL, Canvas)
- External APIs require CORS proxy

**Communication:**
- Settings and Render share instance storage
- Settings saves config → Render subscribes to config
- Device storage only available in Render (not Settings)

## Project Structure

```
project-root/
├── telemetry.config.json       # Platform configuration
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
└── src/
    ├── main.tsx                # Entry point (configure SDK here)
    ├── App.tsx                 # Routing logic
    ├── views/
    │   ├── Settings.tsx        # /settings mount point
    │   └── Render.tsx          # /render mount point
    ├── components/             # Reusable components
    ├── hooks/
    │   └── store.ts            # Store state hooks (createUseStoreState)
    ├── types/                  # TypeScript interfaces
    └── utils/                  # Helper functions
```

## Configuration Files

### telemetry.config.json (project root)
```json
{
  "name": "app-name",
  "version": "1.0.0",
  "mountPoints": {
    "render": "/render",
    "settings": "/settings"
  },
  "backgroundWorkers": {
    "background": "workers/background.js"
  },
  "serverWorkers": {
    "api": "workers/api.js"
  },
  "devServer": {
    "runCommand": "vite --port 3000",
    "url": "http://localhost:3000"
  }
}
```

### package.json scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@telemetryos/sdk": "latest",
    "react": "latest",
    "react-dom": "latest"
  },
  "devDependencies": {
    "@types/react": "latest",
    "@types/react-dom": "latest",
    "@vitejs/plugin-react": "latest",
    "typescript": "latest",
    "vite": "latest"
  }
}
```

## Complete File Implementations

### src/main.tsx (Entry Point)
```typescript
import { configure } from '@telemetryos/sdk';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Configure SDK ONCE before React renders
// Name must match telemetry.config.json
configure('app-name');

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### src/App.tsx (Routing)
```typescript
import Settings from './views/Settings';
import Render from './views/Render';

export default function App() {
  const path = window.location.pathname;

  if (path === '/settings') return <Settings />;
  if (path === '/render') return <Render />;

  return <div>Invalid mount point: {path}</div>;
}
```

### src/hooks/store.ts (Store Hooks)
```typescript
import { createUseStoreState } from '@telemetryos/sdk/react'

// Create typed hooks for each store key
export const useTeamStoreState = createUseStoreState<string>('team', '')
export const useLeagueStoreState = createUseStoreState<string>('league', 'nfl')
```

### src/views/Settings.tsx (Complete Reference)
```typescript
import { store } from '@telemetryos/sdk'
import {
  SettingsContainer,
  SettingsField,
  SettingsLabel,
  SettingsInputFrame,
  SettingsSelectFrame,
} from '@telemetryos/sdk/react'
import { useTeamStoreState, useLeagueStoreState } from '../hooks/store'

export default function Settings() {
  const [isLoadingTeam, team, setTeam] = useTeamStoreState(store().instance)
  const [isLoadingLeague, league, setLeague] = useLeagueStoreState(store().instance)

  return (
    <SettingsContainer>
      <SettingsField>
        <SettingsLabel>Team Name</SettingsLabel>
        <SettingsInputFrame>
          <input
            type="text"
            placeholder="Enter team name..."
            disabled={isLoadingTeam}
            value={team}
            onChange={(e) => setTeam(e.target.value)}
          />
        </SettingsInputFrame>
      </SettingsField>

      <SettingsField>
        <SettingsLabel>League</SettingsLabel>
        <SettingsSelectFrame>
          <select
            disabled={isLoadingLeague}
            value={league}
            onChange={(e) => setLeague(e.target.value)}
          >
            <option value="nfl">NFL</option>
            <option value="nba">NBA</option>
            <option value="mlb">MLB</option>
            <option value="nhl">NHL</option>
          </select>
        </SettingsSelectFrame>
      </SettingsField>
    </SettingsContainer>
  )
}
```

### src/views/Render.tsx (Complete Reference)
```typescript
import { useEffect, useState } from 'react'
import { proxy } from '@telemetryos/sdk'
import { store } from '@telemetryos/sdk'
import { useTeamStoreState, useLeagueStoreState } from '../hooks/store'

interface GameScore {
  homeTeam: string
  awayTeam: string
  homeScore: number
  awayScore: number
  status: string
}

export default function Render() {
  // Use same hooks as Settings - automatically syncs when Settings changes
  const [isLoadingTeam, team] = useTeamStoreState(store().instance)
  const [isLoadingLeague, league] = useLeagueStoreState(store().instance)

  const [score, setScore] = useState<GameScore | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Fetch scores when config changes
  useEffect(() => {
    if (!team) return

    const fetchScore = async () => {
      setLoading(true)
      setError(null)

      try {
        // Platform handles caching automatically - no manual cache needed
        const response = await proxy().fetch(
          `https://api.sportsdata.io/v3/${league}/scores/json/GamesByTeam/${team}`
        )

        if (!response.ok) throw new Error(`API error: ${response.status}`)

        const data = await response.json()
        if (data.length > 0) {
          const game = data[0]
          setScore({
            homeTeam: game.HomeTeam,
            awayTeam: game.AwayTeam,
            homeScore: game.HomeScore,
            awayScore: game.AwayScore,
            status: game.Status,
          })
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchScore()
  }, [team, league])

  // Loading state
  if (isLoadingTeam || isLoadingLeague) return <div>Loading config...</div>
  if (!team) return <div>Configure team in Settings</div>
  if (loading && !score) return <div>Loading scores...</div>
  if (error && !score) return <div>Error: {error}</div>

  return (
    <div>
      <h1>{team} - {league.toUpperCase()}</h1>
      {score && (
        <div>
          <div>{score.awayTeam} @ {score.homeTeam}</div>
          <div>{score.awayScore} - {score.homeScore}</div>
          <div>{score.status}</div>
        </div>
      )}
    </div>
  )
}
```

## SDK API Reference

Import from `@telemetryos/sdk`.

### Initialization

```typescript
configure(applicationName: string): void
```
- Call once in main.tsx before React renders
- Name must match telemetry.config.json
- Throws if called multiple times

### Storage API

**Type Signatures:**
```typescript
store().application.set<T>(key: string, value: T): Promise<boolean>
store().application.get<T>(key: string): Promise<T | undefined>
store().application.subscribe<T>(key: string, handler: (value: T | undefined) => void): Promise<boolean>
store().application.unsubscribe<T>(key: string, handler?: (value: T | undefined) => void): Promise<boolean>
store().application.delete(key: string): Promise<boolean>

// Same methods for instance, device, shared(namespace)
```

**Four Scopes:**

1. **application** - Shared across all instances of app in account
```typescript
await store().application.set('companyLogo', 'https://...');
const logo = await store().application.get<string>('companyLogo');
```

2. **instance** - This specific app instance (Settings ↔ Render communication)
```typescript
// Settings saves
await store().instance.set('config', { city: 'NYC' });

// Render subscribes
const handler = (newConfig) => updateDisplay(newConfig);
await store().instance.subscribe('config', handler);

// Later: unsubscribe
await store().instance.unsubscribe('config', handler);
```

3. **device** - This physical device only (NOT available in Settings)
```typescript
// Only in Render mount point
await store().device.set('cache', data);
const cached = await store().device.get<CacheType>('cache');
```

4. **shared(namespace)** - Inter-app communication
```typescript
// App A publishes
await store().shared('weather').set('temp', '72°F');

// App B subscribes
store().shared('weather').subscribe('temp', (temp) => console.log(temp));
```

**Constraints:**
- All operations timeout after 30 seconds (throws Error)
- Returns `Promise<boolean>` for set/delete/subscribe/unsubscribe (true = success)
- Returns `Promise<T | undefined>` for get
- To unsubscribe, call `unsubscribe(key, handler)` with the same handler function
- Device scope throws Error in Settings mount point

### Proxy API

```typescript
proxy().fetch(url: string, options?: RequestInit): Promise<Response>
```

- Same interface as standard fetch()
- Use when external APIs don't include CORS headers
- Returns standard Response object
- Regular `fetch()` works fine when CORS is not an issue (and has advanced caching in the player)

**Example:**
```typescript
import { proxy } from '@telemetryos/sdk';

const response = await proxy().fetch('https://api.example.com/data');
const json = await response.json();
```

### Media API

```typescript
media().getAllFolders(): Promise<MediaFolder[]>
media().getAllByFolderId(folderId: string): Promise<MediaContent[]>
media().getAllByTag(tagName: string): Promise<MediaContent[]>
media().getById(id: string): Promise<MediaContent>

interface MediaContent {
  id: string;
  contentFolderId: string;
  contentType: string;
  name: string;
  description: string;
  thumbnailUrl: string;
  keys: string[];
  publicUrls: string[];
  hidden: boolean;
  validFrom?: Date;
  validTo?: Date;
  createdAt: Date;
  updatedAt: Date;
}

interface MediaFolder {
  id: string;
  parentId: string;
  name: string;
  size: number;
  default: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

### Playlist API

```typescript
playlist().nextPage(): Promise<boolean>
playlist().previousPage(): Promise<boolean>
playlist().setDuration(duration: number): Promise<boolean>  // duration in milliseconds
```

### Overrides API

```typescript
overrides().setOverride(name: string): Promise<boolean>
overrides().clearOverride(name: string): Promise<boolean>
```

Note: Override names must be pre-configured in Freeform Editor.

### Platform Information

```typescript
accounts().getCurrent(): Promise<Account>
users().getCurrent(): Promise<User>
devices().getInformation(): Promise<DeviceInformation>  // Render only

interface DeviceInformation {
  deviceSerialNumber: string;
  deviceModel: string;
  deviceManufacturer: string;
  devicePlatform: string;
}
```

### Environment API

```typescript
environment().getColorScheme(): Promise<'light' | 'dark' | 'system'>
environment().subscribeColorScheme(handler: (scheme: 'light' | 'dark' | 'system') => void): void
environment().unsubscribeColorScheme(handler: (scheme: 'light' | 'dark' | 'system') => void): void
```

**Example:**
```typescript
import { environment } from '@telemetryos/sdk';

// Get current color scheme
const scheme = await environment().getColorScheme();

// Subscribe to color scheme changes
environment().subscribeColorScheme((newScheme) => {
  document.body.className = newScheme;
});
```

### Weather API

```typescript
weather().getConditions(params: WeatherRequestParams): Promise<WeatherConditions>
weather().getDailyForecast(params: DailyForecastParams): Promise<WeatherForecast[]>
weather().getHourlyForecast(params: HourlyForecastParams): Promise<WeatherForecast[]>

interface WeatherRequestParams {
  city?: string;           // City name (e.g., "New York" or "London, UK")
  postalCode?: string;     // Alternative to city
  lat?: string;            // Latitude (if city not provided)
  lon?: string;            // Longitude (if city not provided)
  units?: 'imperial' | 'metric';
  language?: string;
}

interface DailyForecastParams extends WeatherRequestParams {
  days?: number;           // Number of days to forecast
}

interface HourlyForecastParams extends WeatherRequestParams {
  hours?: number;          // Number of hours to forecast
}
```

**Example:**
```typescript
import { weather } from '@telemetryos/sdk';

// Get current conditions
const conditions = await weather().getConditions({
  city: 'New York',
  units: 'imperial'
});
console.log(`${conditions.Temp}°F - ${conditions.WeatherText}`);

// Get 5-day forecast
const forecast = await weather().getDailyForecast({
  city: 'London',
  units: 'metric',
  days: 5
});
```

### Applications API

```typescript
applications().getAllByMountPoint(mountPoint: string): Promise<Application[]>
applications().getByName(name: string): Promise<Application | null>
applications().setDependencies(specifiers: string[]): Promise<{ ready: string[], unavailable: string[] }>

interface Application {
  name: string;
  mountPoints: Record<string, { path: string }>;
}
```

**Example:**
```typescript
import { applications } from '@telemetryos/sdk';

// Find all apps with a specific mount point
const widgets = await applications().getAllByMountPoint('widget');

// Get a specific app by name
const mapApp = await applications().getByName('interactive-map');

// Declare dependencies before loading sub-apps
const result = await applications().setDependencies(['app-specifier-hash']);
if (result.ready.includes('app-specifier-hash')) {
  // Safe to load in iframe
}
```

## React Hooks for Store

Import from `@telemetryos/sdk/react`. These hooks simplify store interactions by handling subscriptions, loading states, and cleanup automatically.

### useStoreState

Syncs React state with a store key. Handles subscription/unsubscription automatically.

```typescript
import { useStoreState } from '@telemetryos/sdk/react'
import { store } from '@telemetryos/sdk'

function MyComponent() {
  const [isLoading, value, setValue] = useStoreState<string>(
    store().instance,  // Store slice
    'myKey',           // Key name
    'default value',   // Initial state (optional)
    300                // Debounce delay in ms (optional)
  )

  return (
    <input
      disabled={isLoading}
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  )
}
```

**Returns:** `[isLoading: boolean, value: T, setValue: Dispatch<SetStateAction<T>>]`

- `isLoading` - `true` until first value received from store
- `value` - Current value (from store or local optimistic update)
- `setValue` - Updates both local state and store (with optional debounce)

### createUseStoreState

Factory function to create reusable, typed hooks for specific store keys. **This is the recommended pattern.**

```typescript
// hooks/store.ts
import { createUseStoreState } from '@telemetryos/sdk/react'

// Create typed hooks for each store key
export const useTeamStoreState = createUseStoreState<string>('team', '')
export const useLeagueStoreState = createUseStoreState<string>('league', 'nfl')
export const useRefreshIntervalStoreState = createUseStoreState<number>('refreshInterval', 30)
```

```typescript
// views/Settings.tsx
import { store } from '@telemetryos/sdk'
import { useTeamStoreState, useLeagueStoreState } from '../hooks/store'

function Settings() {
  const [isLoadingTeam, team, setTeam] = useTeamStoreState(store().instance)
  const [isLoadingLeague, league, setLeague] = useLeagueStoreState(store().instance)
  // ... use in components
}
```

**Benefits:**
- Type-safe: TypeScript knows the exact type of each store key
- Reusable: Same hook works in Settings and Render
- Automatic cleanup: No manual subscribe/unsubscribe needed
- Immediate sync: Changes sync to store automatically (no save button needed)

### Store Data Patterns

**Recommended: Separate store entry per field**
```typescript
// hooks/store.ts
export const useTeamStoreState = createUseStoreState<string>('team', '')
export const useLeagueStoreState = createUseStoreState<string>('league', 'nfl')
export const useShowScoresStoreState = createUseStoreState<boolean>('showScores', true)
```

**Alternative: Rich data object** (for tightly related data like slideshow items)
```typescript
// hooks/store.ts
interface SportsSlide {
  team: string
  league: string
  displaySeconds: number
}

export const useSlidesStoreState = createUseStoreState<SportsSlide[]>('slides', [])
```

## Settings Components

Import from `@telemetryos/sdk/react`. These components ensure your Settings UI matches the Studio design system.

**Important:** Always use these components for Settings. Raw HTML won't look correct in Studio.

### Container & Layout

#### SettingsContainer

Root wrapper for all Settings content. Handles color scheme synchronization with Studio.

```typescript
import { SettingsContainer } from '@telemetryos/sdk/react'

function Settings() {
  return (
    <SettingsContainer>
      {/* All settings content goes here */}
    </SettingsContainer>
  )
}
```

#### SettingsBox

Container with border for grouping related settings.

```typescript
import { SettingsBox } from '@telemetryos/sdk/react'

<SettingsBox>
  {/* Group of related fields */}
</SettingsBox>
```

#### SettingsDivider

Horizontal rule separator between sections.

```typescript
import { SettingsDivider } from '@telemetryos/sdk/react'

<SettingsDivider />
```

### Field Structure

#### SettingsField, SettingsLabel

Wrapper for each form field with its label.

```typescript
import { SettingsField, SettingsLabel } from '@telemetryos/sdk/react'

<SettingsField>
  <SettingsLabel>Field Label</SettingsLabel>
  {/* Input component goes here */}
</SettingsField>
```

### Text Inputs

#### SettingsInputFrame (Text Input)

```typescript
import { store } from '@telemetryos/sdk'
import {
  SettingsContainer,
  SettingsField,
  SettingsLabel,
  SettingsInputFrame,
} from '@telemetryos/sdk/react'
import { useTeamStoreState } from '../hooks/store'

function Settings() {
  const [isLoading, team, setTeam] = useTeamStoreState(store().instance)

  return (
    <SettingsContainer>
      <SettingsField>
        <SettingsLabel>Team Name</SettingsLabel>
        <SettingsInputFrame>
          <input
            type="text"
            placeholder="Enter team name..."
            disabled={isLoading}
            value={team}
            onChange={(e) => setTeam(e.target.value)}
          />
        </SettingsInputFrame>
      </SettingsField>
    </SettingsContainer>
  )
}
```

#### SettingsTextAreaFrame (Multiline Text)

```typescript
import { SettingsTextAreaFrame } from '@telemetryos/sdk/react'
import { useDescriptionStoreState } from '../hooks/store'

const [isLoading, description, setDescription] = useDescriptionStoreState(store().instance)

<SettingsField>
  <SettingsLabel>Description</SettingsLabel>
  <SettingsTextAreaFrame>
    <textarea
      placeholder="Enter description..."
      disabled={isLoading}
      value={description}
      onChange={(e) => setDescription(e.target.value)}
      rows={4}
    />
  </SettingsTextAreaFrame>
</SettingsField>
```

### Selection Inputs

#### SettingsSelectFrame (Dropdown)

```typescript
import { SettingsSelectFrame } from '@telemetryos/sdk/react'
import { useLeagueStoreState } from '../hooks/store'

const [isLoading, league, setLeague] = useLeagueStoreState(store().instance)

<SettingsField>
  <SettingsLabel>League</SettingsLabel>
  <SettingsSelectFrame>
    <select
      disabled={isLoading}
      value={league}
      onChange={(e) => setLeague(e.target.value)}
    >
      <option value="nfl">NFL</option>
      <option value="nba">NBA</option>
      <option value="mlb">MLB</option>
      <option value="nhl">NHL</option>
    </select>
  </SettingsSelectFrame>
</SettingsField>
```

#### SettingsSliderFrame (Range Slider)

```typescript
import { SettingsSliderFrame } from '@telemetryos/sdk/react'
import { useVolumeStoreState } from '../hooks/store'

const [isLoading, volume, setVolume] = useVolumeStoreState(store().instance)

<SettingsField>
  <SettingsLabel>Volume</SettingsLabel>
  <SettingsSliderFrame>
    <input
      type="range"
      min="0"
      max="100"
      disabled={isLoading}
      value={volume}
      onChange={(e) => setVolume(Number(e.target.value))}
    />
    <span>{volume}%</span>  {/* Optional value label */}
  </SettingsSliderFrame>
</SettingsField>
```

The frame uses flexbox layout, so you can optionally add a `<span>` after the input to display the current value.

### Toggle Inputs

#### SettingsSwitchFrame, SettingsSwitchLabel (Toggle Switch)

```typescript
import { SettingsSwitchFrame, SettingsSwitchLabel } from '@telemetryos/sdk/react'
import { useShowScoresStoreState } from '../hooks/store'

const [isLoading, showScores, setShowScores] = useShowScoresStoreState(store().instance)

<SettingsField>
  <SettingsSwitchFrame>
    <input
      type="checkbox"
      role="switch"
      disabled={isLoading}
      checked={showScores}
      onChange={(e) => setShowScores(e.target.checked)}
    />
    <SettingsSwitchLabel>Show Live Scores</SettingsSwitchLabel>
  </SettingsSwitchFrame>
</SettingsField>
```

#### SettingsCheckboxFrame, SettingsCheckboxLabel (Checkbox)

```typescript
import { SettingsCheckboxFrame, SettingsCheckboxLabel } from '@telemetryos/sdk/react'
import { useAutoRefreshStoreState } from '../hooks/store'

const [isLoading, autoRefresh, setAutoRefresh] = useAutoRefreshStoreState(store().instance)

<SettingsField>
  <SettingsCheckboxFrame>
    <input
      type="checkbox"
      disabled={isLoading}
      checked={autoRefresh}
      onChange={(e) => setAutoRefresh(e.target.checked)}
    />
    <SettingsCheckboxLabel>Enable Auto-Refresh</SettingsCheckboxLabel>
  </SettingsCheckboxFrame>
</SettingsField>
```

#### SettingsRadioFrame, SettingsRadioLabel (Radio Buttons)

```typescript
import { SettingsRadioFrame, SettingsRadioLabel } from '@telemetryos/sdk/react'
import { useDisplayModeStoreState } from '../hooks/store'

const [isLoading, displayMode, setDisplayMode] = useDisplayModeStoreState(store().instance)

<SettingsField>
  <SettingsLabel>Display Mode</SettingsLabel>
  <SettingsRadioFrame>
    <input
      type="radio"
      name="displayMode"
      value="compact"
      disabled={isLoading}
      checked={displayMode === 'compact'}
      onChange={(e) => setDisplayMode(e.target.value)}
    />
    <SettingsRadioLabel>Compact</SettingsRadioLabel>
  </SettingsRadioFrame>
  <SettingsRadioFrame>
    <input
      type="radio"
      name="displayMode"
      value="expanded"
      disabled={isLoading}
      checked={displayMode === 'expanded'}
      onChange={(e) => setDisplayMode(e.target.value)}
    />
    <SettingsRadioLabel>Expanded</SettingsRadioLabel>
  </SettingsRadioFrame>
</SettingsField>
```

### Actions

#### SettingsButtonFrame

```typescript
import { SettingsButtonFrame } from '@telemetryos/sdk/react'

<SettingsField>
  <SettingsButtonFrame>
    <button onClick={handleReset}>Reset to Defaults</button>
  </SettingsButtonFrame>
</SettingsField>
```

## Hard Constraints

**These cause runtime errors:**

1. **Device storage in Settings**
   - Settings runs in Studio browser, not on devices
   - `store().device.*` throws Error in Settings
   - Use `store().instance` or `store().application` instead

2. **CORS errors on external APIs**
   - Some external APIs don't include CORS headers
   - Use `proxy().fetch()` when you encounter CORS errors
   - Regular `fetch()` is fine when CORS is not an issue (and has advanced caching in the player)

3. **Missing configure()**
   - SDK methods throw "SDK not configured" Error
   - Call `configure()` once in main.tsx before React renders

4. **Subscription memory leaks**
   - Store a reference to your handler function
   - Must call `unsubscribe(key, handler)` on component unmount
   - Call unsubscribe in useEffect cleanup

5. **Timeout errors**
   - All SDK operations timeout after 30 seconds
   - Throws Error with message containing 'timeout'
   - Handle with try/catch

## TypeScript Patterns

**Define interfaces for all configs and data:**
```typescript
interface AppConfig {
  city: string;
  units: 'celsius' | 'fahrenheit';
  refreshInterval: number;
}

const config = await store().instance.get<AppConfig>('config');
if (config) {
  console.log(config.city);  // TypeScript knows this exists
}
```

**Component with proper types:**
```typescript
interface Props {
  data: WeatherData;
  onRefresh: () => void;
}

export default function WeatherCard({ data, onRefresh }: Props) {
  return <div>{data.temperature}</div>;
}
```

## React Patterns

**Prefer SDK hooks over manual store operations:**
```typescript
// RECOMMENDED: Use SDK hooks
import { useTeamStoreState } from '../hooks/store'
const [isLoading, team, setTeam] = useTeamStoreState(store().instance)

// AVOID: Manual subscription (only for special cases)
const [team, setTeam] = useState('')
useEffect(() => {
  const handler = (value) => setTeam(value)
  store().instance.subscribe('team', handler)
  return () => store().instance.unsubscribe('team', handler)
}, [])
```

**Subscription behavior:**
When you call `subscribe()`, the handler is immediately called with the current value. No separate `get()` call is needed:
```typescript
// WRONG - unnecessary get() call
useEffect(() => {
  store().instance.get('config').then(setConfig)  // Not needed!
  store().instance.subscribe('config', handler)
  // ...
}, [])

// CORRECT - subscribe handles initial value
useEffect(() => {
  const handler = (value) => setConfig(value)
  store().instance.subscribe('config', handler)  // Immediately receives current value
  return () => store().instance.unsubscribe('config', handler)
}, [])
```

**No manual caching needed:**
The platform automatically caches SDK API calls, `fetch()`, and `proxy().fetch()` requests. Don't implement your own cache:
```typescript
// WRONG - manual caching
const response = await fetch(url)
await store().device.set('cached', data)  // Don't do this!

// CORRECT - just fetch, platform handles caching
const response = await fetch(url)
```

**Error handling:**
```typescript
const [error, setError] = useState<string | null>(null)

try {
  await store().instance.set('key', value)
} catch (err) {
  setError(err instanceof Error ? err.message : 'Unknown error')
}
```

**Loading states:**
```typescript
const [loading, setLoading] = useState(false)

const handleAction = async () => {
  setLoading(true)
  try {
    await someAsyncOperation()
  } finally {
    setLoading(false)
  }
}
```

## Low-Level Store API (Alternative)

For special cases where SDK hooks don't fit, you can use the store API directly. This requires manual subscription management.

**Manual subscription pattern:**
```typescript
import { useEffect, useState } from 'react'
import { store } from '@telemetryos/sdk'
import {
  SettingsContainer,
  SettingsField,
  SettingsLabel,
  SettingsInputFrame,
} from '@telemetryos/sdk/react'

interface Config {
  team: string
  league: string
}

export default function Settings() {
  const [config, setConfig] = useState<Config>({ team: '', league: 'nfl' })
  const [isLoading, setIsLoading] = useState(true)

  // Subscribe on mount - subscribe() immediately sends current value
  useEffect(() => {
    const handler = (value: Config | undefined) => {
      if (value) setConfig(value)
      setIsLoading(false)
    }
    store().instance.subscribe<Config>('config', handler)

    return () => {
      store().instance.unsubscribe('config', handler)
    }
  }, [])

  // Update store on change
  const updateConfig = (updates: Partial<Config>) => {
    const newConfig = { ...config, ...updates }
    setConfig(newConfig)
    store().instance.set('config', newConfig)
  }

  return (
    <SettingsContainer>
      <SettingsField>
        <SettingsLabel>Team Name</SettingsLabel>
        <SettingsInputFrame>
          <input
            type="text"
            value={config.team}
            onChange={(e) => updateConfig({ team: e.target.value })}
            disabled={isLoading}
          />
        </SettingsInputFrame>
      </SettingsField>
    </SettingsContainer>
  )
}
```

**Form submission pattern** (for cases requiring validation before save):
```typescript
import { useState, FormEvent } from 'react'
import { store } from '@telemetryos/sdk'
import {
  SettingsContainer,
  SettingsField,
  SettingsLabel,
  SettingsInputFrame,
} from '@telemetryos/sdk/react'

export default function Settings() {
  const [team, setTeam] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError(null)

    try {
      // Validate before saving
      if (team.length < 2) throw new Error('Team name too short')

      const success = await store().instance.set('team', team)
      if (!success) throw new Error('Storage operation failed')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setSaving(false)
    }
  }

  return (
    <SettingsContainer>
      <form onSubmit={handleSubmit}>
        {error && <div style={{ color: 'red' }}>{error}</div>}
        <SettingsField>
          <SettingsLabel>Team Name</SettingsLabel>
          <SettingsInputFrame>
            <input
              type="text"
              value={team}
              onChange={(e) => setTeam(e.target.value)}
            />
          </SettingsInputFrame>
        </SettingsField>
        <button type="submit" disabled={saving}>
          {saving ? 'Saving...' : 'Save'}
        </button>
      </form>
    </SettingsContainer>
  )
}
```

**When to use low-level API:**
- Complex validation logic before saving
- Batching multiple store operations
- Custom debouncing behavior
- Integration with form libraries

**When to use SDK hooks (recommended):**
- Most Settings components
- Simple form fields
- Real-time sync between Settings and Render

## Code Style

**Naming:**
- Components: PascalCase (`WeatherCard.tsx`)
- Functions: camelCase (`fetchWeatherData`)
- Constants: UPPER_SNAKE_CASE (`API_BASE_URL`)
- Interfaces: PascalCase (`WeatherData`, `AppConfig`)

**Imports order:**
```typescript
// 1. SDK imports
import { configure, store, proxy } from '@telemetryos/sdk'
import {
  SettingsContainer,
  SettingsField,
  SettingsLabel,
  SettingsInputFrame,
} from '@telemetryos/sdk/react'

// 2. React imports
import { useEffect, useState } from 'react'

// 3. Local imports (hooks, components, types)
import { useTeamStoreState } from '../hooks/store'
import ScoreCard from '@/components/ScoreCard'
import type { GameScore } from '@/types'
```

**TypeScript:**
- Use strict mode
- Define interfaces for all configs and data
- Use generics with storage: `get<Type>(key)`
- Prefer `interface` over `type` for objects

**React:**
- Functional components only
- Use hooks (useState, useEffect, useMemo, useCallback)
- Implement loading, error, empty states
- Clean up subscriptions in useEffect return

## Development Commands

```bash
# Install dependencies
npm install

# Start local dev server
tos serve
# Or: npm run dev

# Build for production
npm run build

# Type check
tsc --noEmit
```

**Local testing:**
- Settings: http://localhost:3000/settings
- Render: http://localhost:3000/render

**Deployment:**
```bash
git add .
git commit -m "Description"
git push origin main
# GitHub integration auto-deploys
```

## Common Errors

**"SDK not configured"**
→ Call `configure('app-name')` in main.tsx before React renders

**"device storage not available"**
→ Using `store().device` in Settings - use `store().instance` instead

**CORS error**
→ External API doesn't include CORS headers - use `proxy().fetch()` for that API

**"Request timeout"**
→ SDK operation exceeded 30 seconds - handle with try/catch

**Render not updating**
→ Missing subscription - use `store().instance.subscribe()` in Render

**Memory leak**
→ Not calling `unsubscribe(key, handler)` in useEffect cleanup

## Project-Specific Context

[Add your project details here:]

**Application Name:** [Your app name]
**External APIs:**
- [API name]: [endpoint]
  - Authentication: [method]
  - Rate limits: [limits]

**Custom Components:**
- [ComponentName]: [purpose]
  - Location: [path]
  - Props: [interface]

**Business Logic:**
- [Key algorithms or calculations]
- [Data transformation rules]

## Technical References

**Getting Started:**
- [Quick Start Guide](https://docs.telemetryos.com/docs/quick-start) - Build TelemetryOS applications in minutes
- [SDK Getting Started](https://docs.telemetryos.com/docs/sdk-getting-started) - Build custom screen applications
- [Building Applications](https://docs.telemetryos.com/docs/applications) - Build custom web applications for TelemetryOS
- [Generate New Application](https://docs.telemetryos.com/docs/generate-new-application) - Use the CLI to scaffold projects

**SDK Method Reference:**
- [SDK Method Reference](https://docs.telemetryos.com/docs/sdk-method-reference) - Complete reference for all SDK methods
- [Storage Methods](https://docs.telemetryos.com/docs/storage-methods) - Complete storage scope reference
- [Platform Methods](https://docs.telemetryos.com/docs/platform-methods) - Proxy, media, accounts, users, devices
- [Media Methods](https://docs.telemetryos.com/docs/media-methods) - Media content queries
- [Playlist Methods](https://docs.telemetryos.com/docs/playlist-methods) - Page navigation methods
- [Overrides Methods](https://docs.telemetryos.com/docs/overrides-methods) - Dynamic content control
- [Proxy Methods](https://docs.telemetryos.com/docs/proxy-methods) - Fetch external content through TelemetryOS proxy
- [Weather Methods](https://docs.telemetryos.com/docs/weather-methods) - Access weather data and forecasts
- [Client Methods](https://docs.telemetryos.com/docs/client-methods) - Low-level messaging for advanced use cases

**Application Structure:**
- [Application Components](https://docs.telemetryos.com/docs/application-components) - Modular pieces of a TelemetryOS application
- [Mount Points](https://docs.telemetryos.com/docs/mount-points) - /render vs /settings execution contexts
- [Rendering](https://docs.telemetryos.com/docs/rendering) - Visual component displayed on playlist pages
- [Settings](https://docs.telemetryos.com/docs/settings) - Configuration UI in Studio side panel
- [Workers](https://docs.telemetryos.com/docs/workers) - Background JavaScript patterns
- [Containers](https://docs.telemetryos.com/docs/containers) - Docker integration patterns
- [Configuration](https://docs.telemetryos.com/docs/configuration) - telemetry.config.json schema

**Development:**
- [Local Development](https://docs.telemetryos.com/docs/local-development) - Develop and test locally before deployment
- [CORS Guide](https://docs.telemetryos.com/docs/cors) - Why proxy().fetch() is required
- [Code Examples](https://docs.telemetryos.com/docs/code-examples) - Complete working examples
- [AI-Assisted Development](https://docs.telemetryos.com/docs/ai-assisted-development) - Accelerate development with Claude Code
- [GitHub Integration](https://docs.telemetryos.com/docs/github-integration) - Automated Git-to-Screen deployment

**Platform Context:**
- [Offline Capabilities](https://docs.telemetryos.com/docs/offline-capabilities) - How apps run locally on devices
- [Languages Supported](https://docs.telemetryos.com/docs/languages-supported) - Runtime environment constraints
- [Use Cases](https://docs.telemetryos.com/docs/use-cases) - Real-world applications and use cases
- [Platform Architecture](https://docs.telemetryos.com/docs/platform-architecture) - Technical deep dive

**AI & Automation:**
- [LLMS.txt](https://docs.telemetryos.com/llms.txt) - Complete documentation index for AI agents
- [MCP Server](https://docs.telemetryos.com/docs/mcp-server) - Model Context Protocol server integration
- [Using AI with TelemetryOS](https://docs.telemetryos.com/docs/using-ai-with-telemetryos) - AI tools overview

**API Reference (for backend integrations):**
- [API Introduction](https://docs.telemetryos.com/reference/introduction) - Get started with the TelemetryOS API
- [Authentication](https://docs.telemetryos.com/reference/authentication) - API security and credentials
- [API Tokens](https://docs.telemetryos.com/docs/api-tokens) - Token management for programmatic access
