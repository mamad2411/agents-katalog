---
name: keyboard-shortcuts-patterns
description: Keyboard shortcuts, command palette (Cmd+K), and power user navigation patterns
license: MIT
---

# Keyboard Shortcuts & Command Palette Patterns

## 1. Command Palette (Cmd+K)

### Search UI Pattern
```tsx
interface CommandPaletteProps {
  items: CommandItem[];
  onSelect: (item: CommandItem) => void;
  placeholder?: string;
  recentItems?: CommandItem[];
}

interface CommandItem {
  id: string;
  label: string;
  category?: string;
  keywords?: string[];
  icon?: React.ReactNode;
  shortcut?: string;
}

// Fuzzy search with ranking
const fuzzyMatch = (search: string, item: CommandItem): number => {
  const text = `${item.label} ${item.keywords?.join(' ')}`.toLowerCase();
  const query = search.toLowerCase();
  let score = 0;
  let lastIndex = -1;
  
  for (const char of query) {
    const index = text.indexOf(char, lastIndex + 1);
    if (index === -1) return 0;
    score += 1 / (index - lastIndex);
    lastIndex = index;
  }
  return score;
};
```

### Categories & Recent Items
```tsx
const CommandPalette = ({ items, recentItems }: CommandPaletteProps) => {
  const [search, setSearch] = useState('');
  const filtered = search ? items.filter(i => fuzzyMatch(search, i) > 0) : items;
  const grouped = groupBy(filtered, 'category');
  
  return (
    <div className="fixed inset-0 z-50 bg-black/50" role="dialog">
      <div className="mx-auto mt-20 max-w-xl rounded-lg bg-white shadow-2xl">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search commands..."
          className="w-full border-b px-4 py-3 text-lg outline-none"
        />
        <div className="max-h-96 overflow-y-auto">
          {!search && recentItems && (
            <CommandGroup title="Recent" items={recentItems} />
          )}
          {Object.entries(grouped).map(([category, items]) => (
            <CommandGroup key={category} title={category} items={items} />
          ))}
        </div>
      </div>
    </div>
  );
};
```

## 2. Global Shortcuts

### Common Pattern Registry
```tsx
const GLOBAL_SHORTCUTS = {
  save: { key: 's', modifiers: ['meta'] },
  undo: { key: 'z', modifiers: ['meta'] },
  redo: { key: 'z', modifiers: ['meta', 'shift'] },
  find: { key: 'f', modifiers: ['meta'] },
  close: { key: 'Escape', modifiers: [] },
  commandPalette: { key: 'k', modifiers: ['meta'] },
} as const;

// Platform-aware modifier
const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
const metaKey = isMac ? 'Cmd' : 'Ctrl';
```

### useKeyboardShortcut Hook
```tsx
interface ShortcutConfig {
  key: string;
  modifiers?: ('meta' | 'ctrl' | 'shift' | 'alt')[];
  enabled?: boolean;
  preventDefault?: boolean;
}

const useKeyboardShortcut = (
  config: ShortcutConfig,
  callback: () => void
) => {
  useEffect(() => {
    if (!config.enabled ?? true) return;
    
    const handler = (e: KeyboardEvent) => {
      const modMatch = 
        (!config.modifiers?.includes('meta') || e.metaKey) &&
        (!config.modifiers?.includes('ctrl') || e.ctrlKey) &&
        (!config.modifiers?.includes('shift') || e.shiftKey) &&
        (!config.modifiers?.includes('alt') || e.altKey);
      
      if (e.key === config.key && modMatch) {
        if (config.preventDefault) e.preventDefault();
        callback();
      }
    };
    
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [config, callback]);
};
```

## 3. Contextual Shortcuts

### Focus-Based Shortcuts
```tsx
const useContextualShortcuts = (context: 'editor' | 'sidebar' | 'modal') => {
  const shortcuts = {
    editor: {
      'Cmd+B': 'Toggle bold',
      'Cmd+I': 'Toggle italic',
      'Cmd+/': 'Toggle comment',
    },
    sidebar: {
      'ArrowUp/Down': 'Navigate items',
      'Enter': 'Open item',
      '/': 'Focus search',
    },
    modal: {
      'Escape': 'Close modal',
      'Tab': 'Next field',
    },
  }[context];
  
  return shortcuts;
};
```

## 4. Shortcut Discovery

### Tooltip Hints
```tsx
const Button = ({ shortcut, children }: { shortcut?: string }) => (
  <button className="group relative px-4 py-2">
    {children}
    {shortcut && (
      <span className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-500 opacity-0 group-hover:opacity-100">
        {shortcut}
      </span>
    )}
  </button>
);

// Usage: <Button shortcut="⌘S">Save</Button>
```

### Keyboard Shortcut Modal
```tsx
const ShortcutHelpModal = ({ shortcuts }: { shortcuts: Record<string, string> }) => (
  <div className="rounded-lg bg-white p-6 shadow-xl">
    <h2 className="mb-4 text-xl font-bold">Keyboard Shortcuts</h2>
    <div className="grid gap-2">
      {Object.entries(shortcuts).map(([key, description]) => (
        <div key={key} className="flex justify-between border-b pb-2">
          <span className="text-gray-700">{description}</span>
          <kbd className="rounded bg-gray-100 px-2 py-1 font-mono text-sm">{key}</kbd>
        </div>
      ))}
    </div>
  </div>
);
```

## 5. Shortcut Conflicts

### Browser Defaults to Avoid [CRITICAL]
- **Cmd+W** (close tab), **Cmd+T** (new tab), **Cmd+R** (reload)
- **Cmd+L** (address bar), **Cmd+D** (bookmark)
- Use `e.preventDefault()` cautiously

### Platform Differences
```tsx
const formatShortcut = (shortcut: string): string => {
  const isMac = navigator.platform.includes('Mac');
  return shortcut
    .replace('Cmd', isMac ? '⌘' : 'Ctrl')
    .replace('Alt', isMac ? '⌥' : 'Alt')
    .replace('Shift', '⇧');
};
```

## 6. Focus Management

### Focus Trap in Modals [CRITICAL]
```tsx
const useFocusTrap = (containerRef: RefObject<HTMLElement>) => {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    
    const focusable = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusable[0] as HTMLElement;
    const last = focusable[focusable.length - 1] as HTMLElement;
    
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    
    container.addEventListener('keydown', handler);
    first.focus();
    return () => container.removeEventListener('keydown', handler);
  }, [containerRef]);
};
```

### Focus Restoration [MAJOR]
```tsx
const Modal = ({ onClose }: { onClose: () => void }) => {
  const previousFocus = useRef<HTMLElement | null>(null);
  
  useEffect(() => {
    previousFocus.current = document.activeElement as HTMLElement;
    return () => previousFocus.current?.focus();
  }, []);
  
  return <div role="dialog">...</div>;
};
```

## 7. Accessibility

### Screen Reader Announcements [CRITICAL]
```tsx
const useLiveRegion = () => {
  const announce = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
    const region = document.getElementById('live-region');
    if (region) {
      region.setAttribute('aria-live', priority);
      region.textContent = message;
    }
  };
  return announce;
};

// In root: <div id="live-region" className="sr-only" aria-live="polite" />
```

### Visible Focus Indicators
```tsx
// globals.css
.focus-visible:focus {
  @apply outline-none ring-2 ring-blue-500 ring-offset-2;
}
```

## 8. Shortcut Registry

### Centralized Management
```tsx
class ShortcutRegistry {
  private shortcuts = new Map<string, () => void>();
  
  register(key: string, callback: () => void, context?: string) {
    const id = context ? `${context}:${key}` : key;
    this.shortcuts.set(id, callback);
  }
  
  unregister(key: string, context?: string) {
    const id = context ? `${context}:${key}` : key;
    this.shortcuts.delete(id);
  }
  
  handle(e: KeyboardEvent, context?: string) {
    const key = this.formatKey(e);
    const contextKey = context ? `${context}:${key}` : key;
    const handler = this.shortcuts.get(contextKey) || this.shortcuts.get(key);
    if (handler) {
      e.preventDefault();
      handler();
    }
  }
  
  private formatKey(e: KeyboardEvent): string {
    const mods = [
      e.metaKey && 'Cmd',
      e.ctrlKey && 'Ctrl',
      e.shiftKey && 'Shift',
      e.altKey && 'Alt',
    ].filter(Boolean);
    return [...mods, e.key].join('+');
  }
}

export const shortcuts = new ShortcutRegistry();
```

## 9. Audit Checklist

### Command Palette [CRITICAL]
- [ ] Cmd+K opens palette
- [ ] Fuzzy search works
- [ ] Recent items shown when empty
- [ ] Categories clearly separated
- [ ] Keyboard navigation (arrows, Enter, Escape)

### Global Shortcuts [MAJOR]
- [ ] Platform detection (Mac vs Windows)
- [ ] Shortcuts displayed in UI (tooltips, help modal)
- [ ] No conflicts with browser defaults
- [ ] preventDefault used appropriately

### Focus Management [CRITICAL]
- [ ] Focus trapped in modals
- [ ] Focus restored after modal close
- [ ] Visible focus indicators on all interactive elements
- [ ] Tab order is logical

### Accessibility [CRITICAL]
- [ ] Screen reader announces shortcut actions
- [ ] Skip to content link available
- [ ] All shortcuts documented in help
- [ ] Alternative non-keyboard methods available

### Contextual Shortcuts [MAJOR]
- [ ] Shortcuts change based on focus
- [ ] Conflicts resolved between contexts
- [ ] Help shows context-specific shortcuts

### Discovery [MINOR]
- [ ] Shortcut hints in tooltips
- [ ] Help modal accessible (Cmd+? or ?)
- [ ] Shortcuts shown in command palette
- [ ] Onboarding highlights key shortcuts

### Performance [MINOR]
- [ ] Debounced search in command palette
- [ ] Keyboard handlers cleaned up properly
- [ ] No memory leaks from event listeners
