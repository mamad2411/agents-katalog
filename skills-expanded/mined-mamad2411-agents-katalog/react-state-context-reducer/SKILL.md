---
name: react-state-context-reducer
description: Use when a piece of app state has multiple related fields and multiple ways to change it (loading/error/data, or several related entities) and plain useState calls are multiplying — Context + useReducer pattern.
metadata:
  origin: ECC (decomposed from frontend-patterns)
allowed-tools: Read, Edit, Grep, Glob
---

# Context + useReducer pattern

Use when a slice of state has several fields that change together and several distinct actions
that mutate it — a single `useReducer` with a typed action union beats N independent `useState`
calls that can drift out of sync.

```tsx
interface State {
  markets: Market[];
  selectedMarket: Market | null;
  loading: boolean;
}
type Action = { type: 'SET_MARKETS'; payload: Market[] } | { type: 'SELECT_MARKET'; payload: Market } | { type: 'SET_LOADING'; payload: boolean };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_MARKETS':
      return { ...state, markets: action.payload };
    case 'SELECT_MARKET':
      return { ...state, selectedMarket: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    default:
      return state;
  }
}

const MarketContext = createContext<{ state: State; dispatch: Dispatch<Action> } | undefined>(undefined);

export function MarketProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, { markets: [], selectedMarket: null, loading: false });
  return <MarketContext.Provider value={{ state, dispatch }}>{children}</MarketContext.Provider>;
}

export function useMarkets() {
  const ctx = useContext(MarketContext);
  if (!ctx) throw new Error('useMarkets must be used within MarketProvider');
  return ctx;
}
```

## When NOT to use this

- One or two independent booleans/strings that never change together → plain `useState`, this is
  overkill.
- State that's genuinely global/shared across route changes and needs persistence, devtools, or
  cross-tab sync → reach for Zustand/Redux instead of hand-rolled Context+reducer.
- Server-derived data with caching/revalidation needs → SWR/React Query, not this — this pattern
  is for client-owned UI state, not a data-fetching cache.

## Provider placement

Mount the provider as close as possible to the components that need it, not always at the app
root — a `MarketProvider` wrapping only the markets feature avoids re-rendering unrelated parts
of the tree on every dispatch (Context consumers re-render on any value change, not just the
field they read).
