---
name: "Search Experience Designer"
version: "1.0.0"
description: "Designs search experiences with autocomplete, faceted filtering, result highlighting, and relevance tuning."
author: "workspace"
activated: false
---

# Search Experience Designer

Designs search experiences with autocomplete, faceted filtering, result highlighting, and relevance tuning.

## Decision Framework

### When to Apply
Use when: Product search, content search, filtering interfaces, autocomplete needed

### When NOT to Apply
Don't use when: Simple find-in-array operations, no search requirements

## Anti-Patterns

### 1. No Debouncing
```javascript
// BAD: Fires on every keystroke
input.addEventListener('input', (e) => search(e.target.value));

// GOOD: Debounced
const debouncedSearch = debounce((q) => search(q), 300);
input.addEventListener('input', (e) => debouncedSearch(e.target.value));
```

### 2. Searching on Empty Query
```javascript
// BAD: Shows all results for empty query
if (query.length >= 0) { fetchResults(query); }

// GOOD: Minimum query length
if (query.length >= 2) { fetchResults(query); }
```


## Trigger Phrases

- "Add search"
- "Autocomplete"
- "Search filtering"
- "Faceted search"
- "Search results"

## Patterns

### Search Hook
```javascript
function useSearch(searchFn, options = {}) {
  const { debounce: delay = 300, minLength = 2 } = options;
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const search = useMemo(() => debounce(async (q) => {
    if (q.length < minLength) { setResults([]); return; }
    setLoading(true);
    try { setResults(await searchFn(q)); }
    finally { setLoading(false); }
  }, delay), [searchFn, delay, minLength]);

  useEffect(() => { search(query); }, [query, search]);

  return { query, setQuery, results, loading };
}
```

### Autocomplete
```javascript
const Autocomplete = ({ onSelect }) => {
  const { query, setQuery, results, loading } = useSearch(fetchSuggestions);
  const [highlighted, setHighlighted] = useState(-1);

  return (
    <div role="combobox" aria-expanded={results.length > 0}>
      <input
        type="text" value={query} onChange={e => setQuery(e.target.value)}
        aria-autocomplete="list" aria-activedescendant={highlighted >= 0 ? `option-${highlighted}` : undefined}
      />
      {results.length > 0 && (
        <ul role="listbox">
          {results.map((r, i) => (
            <li key={r.id} id={`option-${i}`} role="option" aria-selected={i === highlighted}
                onClick={() => onSelect(r)}>{r.label}</li>
          ))}
        </ul>
      )}
    </div>
  );
};
```

## Integration
- Works with: accessibility-pattern-library, performance-budget-enforcer, dashboard-composition-engine

