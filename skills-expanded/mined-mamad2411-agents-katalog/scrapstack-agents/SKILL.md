# ScrapStack - Agent Guide

## Project Overview

ScrapStack is an interactive coding platform with:
- **Scripts**: User-created scripts with tree-based file management
- **Visual Composer**: Node-based editor connecting scripts as data pipelines
- **Multi-language support**: Clojure (Scittle) and Lua (Fengari) in the browser
- **Lesson + Challenge format**: Each slot teaches a concept then tests it
- **P2P presence**: Shows connected peers using Ledger (WebRTC + CRDT)
- **Local persistence**: IndexedDB for scripts, compositions, progress

## Current Architecture

### Core Files

**Configuration:**
- `slot-config.js` - Languages (`LANGUAGES`) and slots (`SLOTS`) organized by language

**Language System:**
- `shared/language-registry.js` - Language abstraction layer
- `shared/languages/clojure.js` - Clojure runtime (Scittle)
- `shared/languages/lua.js` - Lua runtime (Fengari)

**Slot System:**
- `slot-engine.js` - Executes code via language registry, validates tests
- `slot-persistence.js` - IndexedDB wrapper (version 4)

**UI:**
- `index.html` - Scripts view with tree sidebar + code editor
- `composer.html` - Visual block composer for connecting scripts
- `slot-template.html` - Lesson display + challenge UI (loads via `?lang=X&slot=N`)
- `shared/styles.css` - All styling including lesson markdown

**P2P:**
- `app.js` - Minimal P2P presence (shows peer count)

### Deprecated Files

- `demo-scripts.js` - Old chat bot scripts (not used)
- `shared/lua-runtime.js` - Old Lua runtime (replaced by `languages/lua.js`)

## Slot Configuration Format

```javascript
export const LANGUAGES = {
  clojure: {
    name: 'clojure',
    displayName: 'Clojure',
    description: 'Functional programming with immutable data',
    icon: '(λ)'
  },
  lua: { ... }
};

export const SLOTS = {
  clojure: [
    {
      id: 1,
      title: "Expressions & Values",
      description: "Learn how Clojure expressions work",
      difficulty: "beginner",
      language: "clojure",
      lesson: `
# Lesson Title

Markdown content with code examples...

## Your Challenge
What the user needs to do.
      `,
      inputs: ["test1", "test2"],
      validate: function(index, output) {
        return output === expected;
      },
      starterCode: `; Starter code`,
      hint: "Helpful hint",
      tags: ["topic"]
    }
  ],
  lua: [ ... ]
};
```

### Helper Functions

```javascript
getLanguages()                    // Returns array of language configs
getLanguage(name)                 // Get specific language config
getSlotsForLanguage(language)     // Get all slots for a language
getSlot(language, id)             // Get specific slot
getNextSlotId(language, current)  // Navigation helper
getPreviousSlotId(language, current)
getTotalSlots(language)           // Count of slots
```

## Adding a New Language

1. Create `shared/languages/yourlang.js`:
```javascript
export const yourlang = {
  name: 'yourlang',
  displayName: 'Your Lang',
  fileExtension: '.yl',

  async init(onLog) {
    // Initialize runtime, store onLog callback
  },

  isReady() {
    return /* runtime initialized */;
  },

  async execute(code, context) {
    // context = { input, slot_id }
    // Return { success: boolean, output: any, error: string|null }
  }
};
```

2. Add to `LANGUAGES` in `slot-config.js`
3. Register in `slot-template.html`:
```javascript
import { yourlang } from './shared/languages/yourlang.js';
registerLanguage(yourlang);
```
4. Add CDN script in `<head>` if needed

## Clojure Runtime Notes

### Lazy Sequence Handling

Clojure's `filter` and `map` return lazy sequences. The runtime wraps user code to force realization:

```javascript
const wrappedCode = `
  (let [__result__ (do ${code})]
    (clj->js (if (seq? __result__) (vec __result__) __result__)))
`;
```

This ensures lazy sequences become vectors before JS conversion.

### Context Variables

User code has access to:
- `input` - Test input value (converted from JS to Clojure)
- `log` - Function to output to console

## Persistence Schema

**IndexedDB: `scrapstack-slots` (version 4)**

| Store | Key | Fields |
|-------|-----|--------|
| `slot_code` | `language:slotId` | language, slotId, code, updatedAt |
| `slot_progress` | `language:slotId` | language, slotId, completed, completedAt |
| `preferences` | `selectedLanguage` | value (language name) |
| `user_scripts` | `id` | id, name, language, code, createdAt, updatedAt |
| `compositions` | `id` | id, name, blocks[], connections[], createdAt, updatedAt |

### Script Schema

```javascript
{
  id: "script_1234567890_abc123",
  name: "my-transform",
  language: "clojure",  // or "lua"
  code: "(str/upper-case input)",
  createdAt: "2024-01-01T00:00:00.000Z",
  updatedAt: "2024-01-01T00:00:00.000Z"
}
```

### Composition Schema

```javascript
{
  id: "comp_1234567890_abc123",
  name: "My Pipeline",
  blocks: [
    { id: "block_1", type: "input", x: 100, y: 100, value: "hello" },
    { id: "block_2", type: "script", x: 300, y: 100, scriptId: "script_..." },
    { id: "block_3", type: "output", x: 500, y: 100 }
  ],
  connections: [
    { id: "conn_1", fromBlock: "block_1", toBlock: "block_2" },
    { id: "conn_2", fromBlock: "block_2", toBlock: "block_3" }
  ],
  createdAt: "2024-01-01T00:00:00.000Z",
  updatedAt: "2024-01-01T00:00:00.000Z"
}
```

### Block Types

| Type | Ports | Purpose |
|------|-------|---------|
| `input` | output only | User enters a text value |
| `output` | input only | Displays received value |
| `script` | both | Runs a script, passes output downstream |

## Composer Architecture

The composer (`composer.html`) is a visual node editor for chaining scripts.

### Key Concepts

**Canvas**: SVG overlay for connections + positioned block elements
**Blocks**: Draggable elements with input/output ports
**Connections**: Bezier curves between ports stored as `{fromBlock, toBlock}`

### Chain Execution Flow

```javascript
async function runBlock(blockId) {
  // 1. Get input from upstream connection (if any)
  const upstream = connections.find(c => c.toBlock === blockId);
  const input = upstream ? blockOutputs[upstream.fromBlock].value : '';

  // 2. Execute block (input, script, or output type)
  const result = await executeBlock(block, input);
  blockOutputs[blockId] = result;

  // 3. Trigger all downstream blocks
  const downstream = connections.filter(c => c.fromBlock === blockId);
  for (const conn of downstream) {
    await runBlock(conn.toBlock);
  }
}
```

### Cycle Prevention

Before adding a connection, check if it would create a cycle:
```javascript
function wouldCreateCycle(fromBlock, toBlock) {
  // BFS from toBlock's outputs - if we can reach fromBlock, it's a cycle
}
```

## Ledger API (from ../rtc_battery)

**Events:**
- `'connected'` - Connected to signaling server
- `'peer-ready'` - Peer WebRTC connection established
- `'peer-leave'` - Peer disconnected

**Methods:**
- `db.getNodeId()` - Get this peer's ID
- `db.getPeers()` - Get array of connected peer IDs
- `db.isConnected()` - Check connection status

## Common Issues & Fixes

### URL Handling
- Use clean URLs without `.html` extension (`npx serve` uses cleanUrls)
- Link to `slot-template?lang=X&slot=N` not `slot-template.html?...`

### P2P Peer Counting
- Use `'peer-ready'` event (not `'peer-join'`)
- Use `db.getPeers().length` (not `db.peers.size`)
- Use `db.getNodeId()` (not `db.peerId`)

### Initialization Order
In `slot-template.html`, order matters:
1. `persistence.init()`
2. Create `SlotEngine`
3. `slotEngine.initialize()`
4. `displaySlotInfo()` (needs slotEngine ready)

### Empty Arrays in Lua
`luaTableToJS` must check for truly empty tables to return `[]` not `{}`.

## File Structure

```
scrapstack/
├── index.html              # Scripts view (tree sidebar + editor)
├── composer.html           # Visual block composer
├── slot-template.html      # Lesson + challenge UI
├── slot-config.js          # LANGUAGES + SLOTS definitions
├── slot-engine.js          # Code execution + validation
├── slot-persistence.js     # IndexedDB wrapper (version 4)
├── app.js                  # P2P presence
├── shared/
│   ├── styles.css          # All styles + lesson markdown
│   ├── language-registry.js # switchLanguage, executeCode, etc.
│   └── languages/
│       ├── clojure.js      # Scittle runtime
│       └── lua.js          # Fengari runtime
├── README.md               # User documentation
├── AGENTS.md               # Same as CLAUDE.md (for other AI agents)
└── CLAUDE.md               # This file
```

## External Dependencies

| Dependency | Purpose | CDN |
|------------|---------|-----|
| Scittle | Clojure interpreter | `cdn.jsdelivr.net/npm/scittle@0.7.30` |
| Fengari | Lua interpreter | `cdn.jsdelivr.net/npm/fengari-web@0.1.4` |
| Marked | Markdown renderer | `cdn.jsdelivr.net/npm/marked@12.0.0` |
| Ledger | P2P CRDT | `esm.sh/@drifting-ink/ledger` |

Signaling server: `wss://drifting.ink/ws/signal`

## Development Workflow

1. **Adding a slot**: Edit `slot-config.js`, add to appropriate language array
2. **Adding a language**: See "Adding a New Language" section
3. **Testing P2P**: Open multiple tabs, peer count should increment
4. **Debugging**: Use `log(value)` in user code, check browser console
5. **Scripts**: Main view in `index.html`, CRUD via `persistence.saveScript()` etc.
6. **Composer**: Block-based editor in `composer.html`, uses `persistence.saveComposition()`

### Scripts System

- Scripts stored in IndexedDB `user_scripts` store
- Tree view groups scripts by language with branch lines (├─ └─)
- Editor auto-saves on input with debounce
- Execution via `language-registry.js` same as lessons

### Composer System

- Compositions stored in IndexedDB `compositions` store
- Drag scripts from sidebar to create blocks
- Connect ports by dragging from output (green) to input (blue)
- Chain execution propagates data downstream automatically
- Built-in blocks: Text Input (📥) and Text Output (📤)
