# Glastonbury 2025 PWA - AI Development Instructions

## Quick Project Overview
React-based PWA for Glastonbury Festival 2025. Key features: lineup management, act discovery, stage navigation, offline functionality. Primary users are festival-goers on mobile devices with potentially poor connectivity.

## Critical Implementation Details

### Data Flow & State Management
```javascript
// LocalStorage keys used throughout the app
'hidePastActs' -> boolean (default: true)
'act_${actShort}' -> 'true' if saved by user

// Common data structure
const data = {
  locations: [
    {
      id: 1,
      name: "Pyramid Stage",
      events: [{ id, name, short, start, end, ... }]
    }
  ]
}
```

### Hide Past Acts Implementation
- **Hook**: `useHidePastActs()` returns `[hidePastActs, setHidePastActs]`
- **Filter**: `filterPastActs(acts, hidePastActs)` - compares `act.end` with `new Date()`
- **Component**: `<HidePastActsToggle />` shows current state, not action
- **Integration**: Added to Intro, Acts, and Stage components

### Time Handling Best Practices
```javascript
// ✅ Correct - dynamic dates in tests
const futureDate = new Date();
futureDate.setFullYear(futureDate.getFullYear() + 2);

// ❌ Incorrect - hardcoded dates will fail
const futureDate = '2025-12-25 12:00';

// ✅ Correct - mocked time for edge cases
jest.useFakeTimers();
jest.setSystemTime(new Date('2025-06-27 15:00:00'));
```

### Component Patterns

#### Responsive Toggle Button
```javascript
// Show state, not action: "Past hidden" vs "Show past"
// Mobile: icon only, Desktop: icon + text
// CSS: grid layout for perfect centering
const HidePastActsToggle = () => {
  const [hidePastActs, setHidePastActs] = useHidePastActs();
  return (
    <button 
      className={`ToggleButton ${hidePastActs ? 'ToggleButton--active' : ''}`}
      onClick={() => setHidePastActs(!hidePastActs)}
      title={`Currently ${hidePastActs ? 'hiding past acts' : 'showing all acts'}`}
    >
      <span className="ToggleButton-icon">{hidePastActs ? '🙈' : '👁️'}</span>
      <span className="ToggleButton-text">{hidePastActs ? 'Past hidden' : 'Past shown'}</span>
    </button>
  );
};
```

#### Perfect Title Centering
```css
/* Use CSS Grid instead of flexbox for true centering */
.PageHeader {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
}

.PageHeader-title {
  grid-column: 2;
  text-align: center;
}

.PageHeader-toggle {
  grid-column: 3;
  justify-self: end;
}
```

### Testing Requirements

#### Test Structure
```javascript
describe('Component/Feature', () => {
  beforeEach(() => {
    // Reset localStorage mocks
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
  });

  it('should handle feature correctly', () => {
    // Use dynamic dates
    const futureDate = new Date();
    futureDate.setFullYear(futureDate.getFullYear() + 1);
    
    // Test implementation
  });
});
```

#### Time-Based Testing
```javascript
// For edge cases requiring specific times
describe('Time Edge Cases', () => {
  beforeEach(() => jest.useFakeTimers());
  afterEach(() => jest.useRealTimers());

  it('should handle midnight transitions', () => {
    jest.setSystemTime(new Date('2025-06-28 23:59:00'));
    // Test logic
  });
});
```

### File Structure
```
src/
├── components/
│   ├── Acts/
│   │   ├── Acts.tsx
│   │   ├── Acts.test.tsx
│   │   └── Acts.css
│   ├── HidePastActsToggle/
│   │   ├── HidePastActsToggle.js
│   │   └── HidePastActsToggle.css
├── hooks/
│   ├── useHidePastActs.js
│   └── useHidePastActs.test.js
├── utils/
│   ├── actFilters.js
│   └── actFilters.test.js
```

### Performance Optimizations
```javascript
// Memoize expensive filtering operations
const filteredActs = useMemo(() => {
  return hidePastActs ? filterPastActs(acts, true) : acts;
}, [acts, hidePastActs]);

// Early return for performance
export const filterPastActs = (acts, hidePastActs) => {
  if (!hidePastActs) return acts; // Skip filtering entirely
  
  const now = new Date();
  return acts.filter(act => {
    const endTime = new Date(act.end);
    return endTime > now;
  });
};
```

### Mobile-First Considerations
```css
/* Base styles for mobile - SUIT CSS methodology */
.ToggleButton {
  padding: 8px 12px;
  font-size: 14px;
  min-height: 44px; /* Touch target size */
  border: none;
  background: transparent;
  cursor: pointer;
}

.ToggleButton--active {
  background-color: #f0f0f0;
  border-radius: 4px;
}

/* Text hidden on small screens */
.ToggleButton-text {
  display: none;
}

/* Show text on larger screens */
@media (min-width: 480px) {
  .ToggleButton-text {
    display: inline;
    margin-left: 8px;
  }
}

/* Utility classes */
.u-textCenter {
  text-align: center;
}

.u-hidden {
  display: none;
}

.u-visuallyHidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### CSS Architecture Best Practices
```css
/* Component structure following SUIT CSS */

/* 1. Component base class */
.ActGrid {
  display: grid;
  gap: 16px;
  padding: 16px;
}

/* 2. Sub-components (single hyphen) */
.ActGrid-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
}

.ActGrid-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
}

.ActGrid-time {
  color: #666;
  font-size: 14px;
}

/* 3. Modifiers (double hyphen) */
.ActGrid--compact {
  gap: 8px;
  padding: 8px;
}

.ActGrid-item--saved {
  border: 2px solid #007bff;
}

.ActGrid-item--past {
  opacity: 0.6;
}

/* 4. State classes */
.ActGrid.is-loading {
  opacity: 0.5;
  pointer-events: none;
}

/* 5. Responsive variations */
@media (min-width: 768px) {
  .ActGrid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
  
  .ActGrid--compact {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}
```

### Component CSS Organization
```javascript
// Prefer CSS classes over inline styles
// ❌ Avoid inline styles
const BadComponent = () => (
  <div style={{ padding: '16px', backgroundColor: '#f0f0f0' }}>
    <h2 style={{ fontSize: '18px', marginBottom: '8px' }}>Title</h2>
  </div>
);

// ✅ Use CSS classes with SUIT methodology
const GoodComponent = () => (
  <div className="ComponentName">
    <h2 className="ComponentName-title">Title</h2>
  </div>
);
```

### CSS File Structure
```
src/
├── components/
│   ├── Acts/
│   │   ├── Acts.tsx
│   │   ├── Acts.css        /* Component-specific styles */
│   │   └── Acts.test.tsx
│   ├── HidePastActsToggle/
│   │   ├── HidePastActsToggle.js
│   │   └── HidePastActsToggle.css
├── styles/
│   ├── base.css           /* Base styles, resets */
│   ├── utilities.css      /* Utility classes (u-*) */
│   ├── layout.css         /* Grid systems, containers */
│   └── variables.css      /* CSS custom properties */
```

### Error Handling Patterns
```javascript
// Graceful degradation for invalid dates
const filterPastActs = (acts, hidePastActs) => {
  if (!hidePastActs) return acts;
  
  const now = new Date();
  return acts.filter(act => {
    try {
      const endTime = new Date(act.end);
      return !isNaN(endTime.getTime()) && endTime > now;
    } catch {
      // Invalid dates are filtered out for safety
      return false;
    }
  });
};

// Handle localStorage errors
const useHidePastActs = () => {
  const [hidePastActs, setHidePastActsState] = useState(() => {
    try {
      return localStorage.getItem('hidePastActs') !== 'false';
    } catch {
      return true; // Default fallback
    }
  });
  
  const setHidePastActs = (value) => {
    try {
      localStorage.setItem('hidePastActs', value.toString());
      setHidePastActsState(value);
    } catch {
      // Still update state even if storage fails
      setHidePastActsState(value);
    }
  };
  
  return [hidePastActs, setHidePastActs];
};
```

### Common Integration Points
1. **Page Headers**: Add toggle using CSS Grid layout
2. **Act Lists**: Apply `filterPastActs` before rendering
3. **Empty States**: Show appropriate message for "no acts" vs "no upcoming acts"
4. **URL Sharing**: Include filter state in shared URLs where relevant

### Performance Monitoring
- Monitor `filterPastActs` execution time with large datasets
- Test localStorage quota limits
- Verify no memory leaks from event listeners
- Check bundle size impact of new features

### Browser Compatibility
- ES6+ features OK (modern mobile browsers)
- Use polyfills for critical PWA features
- Test on iOS Safari, Chrome Android, Firefox Mobile
- Verify touch interactions work correctly 