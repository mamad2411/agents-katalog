---
name: comparison-patterns
description: Side-by-side comparison, diff highlighting, and multi-item comparison patterns
license: MIT
---

# Comparison & Diff Patterns

Patterns for side-by-side comparison UIs, diff highlighting, synchronized scrolling, and multi-item comparison interfaces.

## 1. Comparison Layout

**Side-by-Side (2-4 items)**
```tsx
<div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => (
    <div key={item.id} className="border rounded-lg p-4">
      <ComparisonCard item={item} />
    </div>
  ))}
</div>
```

**Responsive Behavior**: Stack on mobile, 2-col on tablet, 3-4 on desktop. Use `min-w-[280px]` for item cards.

## 2. Item Selection

```tsx
interface ComparisonSlot {
  id: string;
  item: Item | null;
  isBaseline?: boolean;
}

// Empty slot with add button
<div className="border-2 border-dashed rounded-lg p-8 flex items-center justify-center">
  <button onClick={onAddItem} className="text-sm text-gray-500">
    + Add Item to Compare
  </button>
</div>

// Max items warning
{slots.length >= MAX_ITEMS && (
  <div className="text-sm text-amber-600">Maximum {MAX_ITEMS} items</div>
)}
```

## 3. Diff Highlighting

```tsx
interface DiffValue {
  previous: number | string;
  current: number | string;
  change: 'improved' | 'degraded' | 'neutral';
}

function DiffCell({ value, baseline }: { value: number; baseline: number }) {
  const diff = value - baseline;
  const isDegraded = diff < 0;
  const isImproved = diff > 0;
  
  return (
    <div className="flex items-center gap-2">
      <span>{value}</span>
      {diff !== 0 && (
        <span className={cn(
          "text-sm font-medium",
          isImproved && "text-green-600",
          isDegraded && "text-red-600"
        )}>
          {isImproved ? '▲' : '▼'} {Math.abs(diff)}
        </span>
      )}
    </div>
  );
}
```

**Color Coding**: Green = better/improved, Red = worse/degraded, Gray = neutral/unchanged.

## 4. Synchronized Scrolling

```tsx
function SyncScrollContainer({ children, enabled }: { enabled: boolean }) {
  const scrollRefs = useRef<HTMLDivElement[]>([]);
  const isScrolling = useRef(false);

  const handleScroll = (index: number) => (e: React.UIEvent<HTMLDivElement>) => {
    if (!enabled || isScrolling.current) return;
    
    isScrolling.current = true;
    const scrollTop = e.currentTarget.scrollTop;
    
    scrollRefs.current.forEach((ref, i) => {
      if (i !== index && ref) {
        ref.scrollTop = scrollTop;
      }
    });
    
    requestAnimationFrame(() => {
      isScrolling.current = false;
    });
  };

  return (
    <div className="flex gap-4">
      {React.Children.map(children, (child, i) => (
        <div
          ref={(el) => scrollRefs.current[i] = el!}
          onScroll={handleScroll(i)}
          className="flex-1 overflow-y-auto"
        >
          {child}
        </div>
      ))}
    </div>
  );
}

// Toggle sync control
<button onClick={() => setSyncEnabled(!syncEnabled)}>
  {syncEnabled ? '🔒 Synced' : '🔓 Independent'}
</button>
```

## 5. Comparison Table

```tsx
interface ComparisonRow {
  attribute: string;
  values: (string | number)[];
  hasDifference: boolean;
}

function ComparisonTable({ items, rows }: Props) {
  return (
    <table className="w-full">
      <thead className="sticky top-0 bg-white border-b">
        <tr>
          <th className="text-left p-3">Attribute</th>
          {items.map(item => (
            <th key={item.id} className="text-left p-3">{item.name}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map(row => (
          <tr key={row.attribute} className={cn(
            "border-b",
            row.hasDifference && "bg-yellow-50"
          )}>
            <td className="p-3 font-medium">{row.attribute}</td>
            {row.values.map((value, i) => (
              <td key={i} className="p-3">{value}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## 6. Attribute Grouping

```tsx
interface AttributeGroup {
  name: string;
  attributes: string[];
  collapsed: boolean;
}

function CollapsibleGroup({ group, onToggle }: Props) {
  return (
    <div className="border rounded-lg mb-4">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-4 hover:bg-gray-50"
      >
        <span className="font-medium">{group.name}</span>
        <span>{group.collapsed ? '▶' : '▼'}</span>
      </button>
      {!group.collapsed && (
        <div className="p-4 border-t">
          {group.attributes.map(attr => (
            <ComparisonRow key={attr} attribute={attr} />
          ))}
        </div>
      )}
    </div>
  );
}
```

## 7. Baseline Selection

```tsx
function BaselineSelector({ items, baselineId, onChange }: Props) {
  return (
    <div className="flex items-center gap-2 mb-4">
      <label className="text-sm font-medium">Baseline:</label>
      <select
        value={baselineId}
        onChange={(e) => onChange(e.target.value)}
        className="border rounded px-3 py-1"
      >
        <option value="">None</option>
        {items.map(item => (
          <option key={item.id} value={item.id}>{item.name}</option>
        ))}
      </select>
    </div>
  );
}

// Show baseline badge on item card
{isBaseline && (
  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
    Baseline
  </span>
)}
```

## 8. Quick Actions

```tsx
function ComparisonCardActions({ item, isBaseline, onRemove, onSetBaseline }: Props) {
  return (
    <div className="flex gap-2 mt-4 pt-4 border-t">
      <button
        onClick={onRemove}
        className="text-sm text-red-600 hover:text-red-800"
      >
        Remove
      </button>
      {!isBaseline && (
        <button
          onClick={onSetBaseline}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Set as Baseline
        </button>
      )}
      <button
        onClick={() => router.push(`/items/${item.id}`)}
        className="text-sm text-gray-600 hover:text-gray-800 ml-auto"
      >
        View Detail →
      </button>
    </div>
  );
}
```

## 9. Code Examples

**ComparisonGrid Component**
```tsx
interface ComparisonGridProps {
  items: Item[];
  baselineId?: string;
  maxItems?: number;
  onRemove: (id: string) => void;
  onAdd: () => void;
}

function ComparisonGrid({ items, baselineId, maxItems = 4, onRemove, onAdd }: ComparisonGridProps) {
  const canAddMore = items.length < maxItems;
  
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Comparing {items.length} items</h2>
        <button onClick={() => items.forEach(i => onRemove(i.id))} className="text-sm text-gray-600">
          Clear All
        </button>
      </div>
      
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {items.map(item => (
          <ComparisonCard
            key={item.id}
            item={item}
            isBaseline={item.id === baselineId}
            onRemove={() => onRemove(item.id)}
          />
        ))}
        
        {canAddMore && (
          <button onClick={onAdd} className="border-2 border-dashed rounded-lg p-8 hover:bg-gray-50">
            + Add Item
          </button>
        )}
      </div>
    </div>
  );
}
```

## 10. Audit Checklist

**Layout & Structure** [MAJOR]
- [ ] Responsive grid (stack mobile, 2-col tablet, 3-4 desktop)
- [ ] Minimum card width prevents over-cramping
- [ ] Empty slots show clear "add item" affordance
- [ ] Max items limit enforced (typically 4)

**Diff Visualization** [CRITICAL]
- [ ] Color-coded changes (green=better, red=worse)
- [ ] Direction indicators (▲/▼) for numeric changes
- [ ] Baseline comparison clearly labeled
- [ ] Neutral/unchanged values visually distinct

**Scroll Behavior** [MAJOR]
- [ ] Synchronized scrolling option available
- [ ] Toggle control visible and labeled
- [ ] Pinned header row remains visible
- [ ] Independent scrolling works when sync disabled

**Item Management** [MAJOR]
- [ ] Remove button on each item card
- [ ] Clear all action present
- [ ] Add item flow intuitive
- [ ] Baseline selection accessible

**Difference Highlighting** [CRITICAL]
- [ ] Rows with differences visually distinguished
- [ ] Consistent color scheme across all diffs
- [ ] Numeric diff magnitude shown
- [ ] Percentage changes for relevant metrics

**Grouping & Organization** [MINOR]
- [ ] Related attributes grouped logically
- [ ] Collapsible sections for long lists
- [ ] Group headers descriptive
- [ ] Expand/collapse state persists during session

**Quick Actions** [MINOR]
- [ ] Set/unset baseline action available
- [ ] View detail link per item
- [ ] Actions contextual and clear
- [ ] Confirmation for destructive actions

**Accessibility** [MAJOR]
- [ ] Keyboard navigation works across comparison
- [ ] Screen reader announces diff direction/magnitude
- [ ] Color not sole indicator of difference
- [ ] Focus management when adding/removing items

**Performance** [MINOR]
- [ ] Smooth scrolling with many attributes
- [ ] Efficient re-renders on item add/remove
- [ ] Debounced scroll sync to prevent jank
- [ ] Lazy loading for large comparison tables
