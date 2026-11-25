---
name: data-density-patterns
description: Patterns for displaying dense information on screens without overlap, with proper scrolling, z-index management, and responsive condensing
license: MIT
---

# Data Density UX Patterns

When screens need to display a lot of information, proper density management prevents overlap, ensures readability, and maintains usability.

## Core Principles

### The Density Hierarchy
```
1. Essential information visible immediately (no scroll)
2. Important information accessible with minimal scroll
3. Secondary information in collapsible sections
4. Tertiary information behind "show more" or modals
```

### Screen Real Estate Budget
| Screen Size | Visible Height | Recommended Sections |
|-------------|----------------|---------------------|
| Mobile (< 640px) | ~500px | 2-3 collapsed sections |
| Tablet (768px) | ~600px | 3-4 sections with scrolling |
| Desktop (1024px+) | ~700px | Multi-column layout |
| Large (1440px+) | ~800px | Dashboard-style grid |

## Preventing Overlap

### Z-Index Scale (MUST FOLLOW)
```css
/* Establish consistent z-index layers */
:root {
  --z-base: 0;
  --z-dropdown: 10;      /* Dropdowns, tooltips */
  --z-sticky: 20;        /* Sticky headers, navigation */
  --z-overlay: 30;       /* Page overlays */
  --z-modal: 40;         /* Modal dialogs */
  --z-popover: 50;       /* Popovers on modals */
  --z-toast: 60;         /* Toast notifications */
  --z-tooltip: 70;       /* Tooltips (always on top) */
}
```

### Stacking Context Rules
```tsx
// RULE: Each layer creates a stacking context
// Avoid z-index wars by using proper containment

// BAD: Random z-index values
<div style={{ zIndex: 9999 }}>...</div>

// GOOD: Semantic layer classes
<div className="z-dropdown">...</div>
<div className="z-modal">...</div>
```

### Overlap Prevention Checklist
- [ ] Fixed/sticky elements don't overlap content
- [ ] Dropdowns don't get cut off by containers
- [ ] Modals appear above all page content
- [ ] Tooltips appear above modals when needed
- [ ] Toasts don't block important UI

## Ensuring Nothing Is Off-Screen

### Viewport-Aware Positioning
```tsx
function useViewportAwarePosition(elementRef: RefObject<HTMLElement>) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    if (!elementRef.current) return;
    
    const rect = elementRef.current.getBoundingClientRect();
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight,
    };

    let x = position.x;
    let y = position.y;

    // Prevent right overflow
    if (rect.right > viewport.width) {
      x -= (rect.right - viewport.width + 16);
    }
    // Prevent bottom overflow
    if (rect.bottom > viewport.height) {
      y -= (rect.bottom - viewport.height + 16);
    }
    // Prevent left overflow
    if (rect.left < 0) {
      x += Math.abs(rect.left) + 16;
    }
    // Prevent top overflow
    if (rect.top < 0) {
      y += Math.abs(rect.top) + 16;
    }

    setPosition({ x, y });
  }, [elementRef]);

  return position;
}
```

### Container Scroll Handling
```tsx
// RULE: Content containers must have explicit overflow handling

// Dense content area with scroll
<div className="
  max-h-[calc(100vh-200px)]  /* Account for header/footer */
  overflow-y-auto
  overflow-x-hidden
  scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent
">
  {/* Dense content */}
</div>

// Horizontal scroll for wide tables
<div className="overflow-x-auto -mx-4 px-4">
  <table className="min-w-[800px]">...</table>
</div>
```

### Safe Area Insets (Mobile)
```css
/* Account for notches, home indicators */
.page-container {
  padding-left: max(1rem, env(safe-area-inset-left));
  padding-right: max(1rem, env(safe-area-inset-right));
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}
```

## Readability in Dense Layouts

### Minimum Spacing Rules
```css
/* NEVER go below these minimums */
--min-touch-target: 44px;     /* Minimum tappable area */
--min-text-spacing: 4px;      /* Between text lines */
--min-element-gap: 8px;       /* Between UI elements */
--min-section-gap: 16px;      /* Between sections */
```

### Typography for Dense Data
```tsx
// Data-dense typography scale
const denseTypography = {
  heading: 'text-base font-semibold',      // Smaller than normal
  label: 'text-xs font-medium uppercase tracking-wide text-text-muted',
  value: 'text-sm font-mono',              // Mono for data alignment
  secondary: 'text-xs text-text-secondary',
};

// Example: Dense stat display
<div className="grid grid-cols-4 gap-2">
  <div className="p-2 bg-surface-raised rounded">
    <span className={denseTypography.label}>Speed</span>
    <span className={denseTypography.value}>142</span>
  </div>
</div>
```

### Color Contrast in Dense UI
```tsx
// High contrast for dense data
const denseColors = {
  background: 'bg-surface-deep',           // Darkest background
  card: 'bg-surface-base',                 // Slightly lighter
  highlight: 'bg-accent/10',               // Subtle highlight
  border: 'border-border/50',              // Subtle borders
  text: 'text-white',                      // Maximum contrast
  muted: 'text-text-secondary',            // De-emphasized
};
```

## Condensing Information Patterns

### Collapsible Sections
```tsx
function CollapsibleDataSection({ title, defaultOpen = false, children }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-border rounded-lg overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-4 py-3 bg-surface-raised hover:bg-surface-raised/80"
      >
        <span className="text-sm font-medium text-white">{title}</span>
        <ChevronDownIcon className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      
      {isOpen && (
        <div className="px-4 py-3 bg-surface-base">
          {children}
        </div>
      )}
    </div>
  );
}
```

### Truncation with Expansion
```tsx
function TruncatedText({ text, maxLength = 100 }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const shouldTruncate = text.length > maxLength;

  return (
    <div>
      <p className="text-sm text-text-primary">
        {isExpanded || !shouldTruncate ? text : `${text.slice(0, maxLength)}...`}
      </p>
      {shouldTruncate && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs text-accent hover:underline mt-1"
        >
          {isExpanded ? 'Show less' : 'Show more'}
        </button>
      )}
    </div>
  );
}
```

### Progressive Disclosure
```tsx
// Show summary, expand for details
function DataCard({ summary, details }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="p-4 bg-surface-raised rounded-lg">
      {/* Always visible summary */}
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-medium text-white">{summary.title}</h4>
          <p className="text-xs text-text-muted">{summary.subtitle}</p>
        </div>
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="text-xs text-accent"
        >
          {showDetails ? 'Less' : 'More'}
        </button>
      </div>

      {/* Expandable details */}
      {showDetails && (
        <div className="mt-3 pt-3 border-t border-border text-xs space-y-2">
          {details.map((d, i) => (
            <div key={i} className="flex justify-between">
              <span className="text-text-muted">{d.label}</span>
              <span className="text-white">{d.value}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Dense Grid Layouts

### Responsive Dense Grid
```tsx
// Auto-fit columns based on available space
<div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
  {items.map(item => (
    <DenseCard key={item.id} item={item} />
  ))}
</div>

// Fixed minimum width columns
<div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))' }}>
  {items.map(item => (
    <DenseCard key={item.id} item={item} />
  ))}
</div>
```

### Dense Stats Grid
```tsx
function StatsGrid({ stats }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-1">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="p-2 bg-surface-raised/50 rounded text-center"
        >
          <div className="text-lg font-bold text-white font-mono">
            {stat.value}
          </div>
          <div className="text-[10px] text-text-muted uppercase tracking-wide">
            {stat.label}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## Dense Tables

### Compact Table Pattern
```tsx
function DenseTable({ columns, data }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead>
          <tr className="bg-surface-raised">
            {columns.map((col) => (
              <th
                key={col.key}
                className="px-2 py-1.5 text-left font-medium text-text-muted uppercase tracking-wide whitespace-nowrap"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-border/30">
          {data.map((row, i) => (
            <tr key={i} className="hover:bg-surface-raised/30">
              {columns.map((col) => (
                <td
                  key={col.key}
                  className="px-2 py-1.5 text-text-primary whitespace-nowrap"
                >
                  {row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Virtualized Long Lists
```tsx
// For lists with 100+ items, use virtualization
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualizedList({ items, renderItem, itemHeight = 40 }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => itemHeight,
  });

  return (
    <div
      ref={parentRef}
      className="h-[400px] overflow-auto"
    >
      <div
        style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {renderItem(items[virtualRow.index])}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Navigation in Dense UIs

### Sticky Section Headers
```tsx
function StickySection({ title, children }) {
  return (
    <div className="relative">
      <div className="sticky top-0 z-10 bg-surface-deep/95 backdrop-blur-sm py-2 -mx-4 px-4 border-b border-border">
        <h3 className="text-sm font-semibold text-white">{title}</h3>
      </div>
      <div className="pt-3">
        {children}
      </div>
    </div>
  );
}
```

### Jump Navigation
```tsx
function JumpNav({ sections, activeSection, onJump }) {
  return (
    <nav className="sticky top-0 z-20 bg-surface-deep border-b border-border py-2 -mx-4 px-4 mb-4">
      <div className="flex gap-1 overflow-x-auto scrollbar-none">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => onJump(section.id)}
            className={`
              px-2.5 py-1 text-xs font-medium rounded-md whitespace-nowrap
              ${activeSection === section.id
                ? 'bg-accent/20 text-accent'
                : 'text-text-muted hover:text-white hover:bg-surface-raised'}
            `}
          >
            {section.label}
          </button>
        ))}
      </div>
    </nav>
  );
}
```

## Responsive Density Adjustments

### Breakpoint-Based Density
```tsx
// More dense on larger screens, less on mobile
const densityClasses = {
  mobile: 'p-4 space-y-4 text-sm',      // Looser spacing
  desktop: 'p-2 space-y-2 text-xs',     // Tighter spacing
};

<div className={`
  ${densityClasses.mobile}
  lg:${densityClasses.desktop}
`}>
  {content}
</div>
```

### Hide Secondary Info on Mobile
```tsx
<div className="flex items-center gap-4">
  <span className="text-white">{primary}</span>
  <span className="hidden sm:inline text-text-muted">{secondary}</span>
  <span className="hidden lg:inline text-text-muted">{tertiary}</span>
</div>
```

## Audit Checklist for Dense UIs

### Critical (Must Fix)
- [ ] Z-index values follow established scale - elements hidden/overlapping
- [ ] Modals/dialogs appear above all content - blocked interactions
- [ ] All content accessible via scroll - data inaccessible
- [ ] Text meets minimum size (12px body, 10px labels) - unreadable
- [ ] Sufficient contrast ratios maintained - accessibility violation

### Major (Should Fix)
- [ ] Fixed elements don't overlap scrollable content - content hidden
- [ ] Dropdowns/popovers don't get clipped - unusable controls
- [ ] No horizontal scroll unless intentional (tables) - poor mobile UX
- [ ] Tooltips/popovers stay within viewport - information cut off
- [ ] Mobile safe areas respected - notch/home bar overlap
- [ ] Adequate spacing between elements - hard to tap/click
- [ ] Long lists are virtualized (100+ items) - performance issues
- [ ] No layout shift during loading - disorienting jumps

### Minor (Nice to Have)
- [ ] Line height appropriate for text size - readability polish
- [ ] Jump navigation for long pages - convenience
- [ ] Section headers are sticky - navigation convenience
- [ ] Current section is highlighted - orientation
- [ ] Scroll position preserved on back navigation - continuity
- [ ] Images are lazy loaded - performance optimization
- [ ] Animations are reduced in dense areas - performance polish
