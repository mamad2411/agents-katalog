---
name: list-page-patterns
description: UX patterns specific to list/browse pages including filters, sorting, pagination, and grid/table displays
license: MIT
---

# List Page UX Patterns

List pages display collections of items with filtering, sorting, and navigation capabilities.

## Required Components

### 1. Filter Card
Every list page MUST have a filter section.

```tsx
<Card className="mb-6">
  <div className="flex flex-col sm:flex-row gap-4">
    {/* Search - always first */}
    <div className="flex-1">
      <Input
        type="text"
        placeholder="Search by name..."
        value={filters.search}
        onChange={(e) => handleFilterChange('search', e.target.value)}
        aria-label="Search items"
      />
    </div>

    {/* Filter dropdowns */}
    <Select
      value={filters.status}
      onChange={(e) => handleFilterChange('status', e.target.value)}
      options={statusOptions}
      aria-label="Filter by status"
    />

    {/* Clear filters button */}
    <Button variant="secondary" onClick={clearFilters} className="text-xs">
      Clear
    </Button>
  </div>

  {/* Results count - REQUIRED */}
  <div className="mt-4 text-sm text-text-secondary">
    Showing {filteredItems.length} of {items.length} results
    {hasActiveFilters && (
      <span className="text-accent ml-1">(filtered)</span>
    )}
  </div>
</Card>
```

### 2. Results Display

#### Grid Layout (Cards)
```tsx
// For rich items with multiple data points
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => (
    <ItemCard key={item.id} item={item} onClick={() => handleClick(item)} />
  ))}
</div>
```

#### Table Layout (Data-dense)
```tsx
// For data-heavy lists needing sorting
<Card variant="dark" className="overflow-hidden">
  <div className="overflow-x-auto">
    <table className="w-full min-w-[800px]">
      <thead className="bg-surface-base">
        <tr className="text-left text-text-secondary text-xs uppercase">
          <SortableHeader column="name" />
          <SortableHeader column="status" />
          <SortableHeader column="date" />
        </tr>
      </thead>
      <tbody className="divide-y divide-border/50">
        {items.map(item => (
          <tr key={item.id} className="hover:bg-surface-raised/20">
            <td className="px-4 py-3">{item.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</Card>
```

### 3. Sortable Table Header
```tsx
interface SortableHeaderProps {
  label: string;
  column: string;
  currentColumn: string;
  direction: 'asc' | 'desc';
  onSort: (column: string) => void;
}

function SortableHeader({ label, column, currentColumn, direction, onSort }: SortableHeaderProps) {
  const isActive = column === currentColumn;
  
  return (
    <th
      className="px-4 py-3 font-medium cursor-pointer hover:text-white select-none"
      onClick={() => onSort(column)}
    >
      <span className="flex items-center gap-1">
        {label}
        {isActive && (
          <span className="text-accent text-xs">
            {direction === 'asc' ? '▲' : '▼'}
          </span>
        )}
      </span>
    </th>
  );
}
```

### 4. Pagination
```tsx
// Only show if totalPages > 1
{totalPages > 1 && (
  <div className="flex justify-center mt-6">
    <PaginationButtons
      currentPage={currentPage}
      totalPages={totalPages}
      onPageChange={setCurrentPage}
    />
  </div>
)}

function PaginationButtons({ currentPage, totalPages, onPageChange }) {
  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-3 py-1.5 rounded bg-surface-raised disabled:opacity-50"
      >
        Previous
      </button>
      
      <span className="text-sm text-text-secondary">
        Page {currentPage} of {totalPages}
      </span>
      
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-3 py-1.5 rounded bg-surface-raised disabled:opacity-50"
      >
        Next
      </button>
    </div>
  );
}
```

### 5. Empty State
```tsx
{filteredItems.length === 0 && (
  <EmptyState
    icon={<EmptyIcon />}
    title={hasFilters ? 'No items match your filters' : 'No items yet'}
    message={hasFilters ? 'Try adjusting your search or filters' : 'Create your first item to get started'}
    action={!hasFilters && (
      <Button variant="primary" onClick={handleCreate}>
        Create First Item
      </Button>
    )}
  />
)}
```

## Item Card Pattern

### Standard Card Structure
```tsx
function ItemCard({ item, onClick }) {
  return (
    <div
      onClick={onClick}
      className="
        group relative p-5 rounded-xl border-2 transition-all cursor-pointer
        bg-gradient-to-br from-surface-raised/60 to-surface-raised/30
        border-border hover:border-accent/50 hover:shadow-lg
        hover:scale-[1.02] hover:-translate-y-0.5
      "
    >
      {/* Accent line at top */}
      <div className="absolute top-0 left-4 right-4 h-0.5 bg-accent/30 group-hover:bg-accent rounded-full" />

      {/* Header with title and badge */}
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-bold text-white truncate group-hover:text-accent">
            {item.name}
          </h3>
          {item.subtitle && (
            <p className="text-accent/80 text-sm truncate">{item.subtitle}</p>
          )}
        </div>
        <StatusBadge status={item.status} />
      </div>

      {/* Stats or metadata */}
      <div className="flex items-center justify-between text-sm text-text-secondary">
        <span>{item.count} items</span>
        <span>{item.date}</span>
      </div>

      {/* Hover arrow indicator */}
      <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
        <ChevronRightIcon className="w-5 h-5 text-accent" />
      </div>
    </div>
  );
}
```

## Filter State Management

### Standard Filter Pattern
```tsx
interface FilterState {
  search: string;
  status: string;
  category: string;
}

function useFilters<T>(items: T[], filterFn: (item: T, filters: FilterState) => boolean) {
  const [filters, setFilters] = useState<FilterState>({
    search: '',
    status: '',
    category: '',
  });

  const filteredItems = useMemo(() => {
    return items.filter(item => filterFn(item, filters));
  }, [items, filters, filterFn]);

  const hasActiveFilters = Object.values(filters).some(v => v !== '');

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({ search: '', status: '', category: '' });
  };

  return { filters, filteredItems, hasActiveFilters, handleFilterChange, clearFilters };
}
```

## Sort State Management

### Standard Sort Pattern
```tsx
type SortDirection = 'asc' | 'desc';

interface SortState<T extends string> {
  column: T;
  direction: SortDirection;
}

function useSort<T, C extends string>(items: T[], sortFn: (a: T, b: T, column: C) => number) {
  const [sort, setSort] = useState<SortState<C>>({
    column: 'name' as C,
    direction: 'asc',
  });

  const sortedItems = useMemo(() => {
    const sorted = [...items];
    sorted.sort((a, b) => {
      const result = sortFn(a, b, sort.column);
      return sort.direction === 'asc' ? result : -result;
    });
    return sorted;
  }, [items, sort, sortFn]);

  const handleSort = (column: C) => {
    setSort(prev => ({
      column,
      direction: prev.column === column && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  return { sort, sortedItems, handleSort };
}
```

## Advanced Filters Panel

### Expandable Advanced Filters
```tsx
const [showAdvanced, setShowAdvanced] = useState(false);
const hasAdvancedFilters = filters.dateMin || filters.dateMax || filters.valueMin;

<Button
  variant="ghost"
  onClick={() => setShowAdvanced(!showAdvanced)}
  className={hasAdvancedFilters ? 'text-accent' : ''}
>
  {showAdvanced ? '▼' : '▶'} Advanced
  {hasAdvancedFilters && ' •'}
</Button>

{showAdvanced && (
  <div className="mt-4 pt-4 border-t border-border">
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {/* Range filters */}
      <div>
        <label className="block text-xs text-text-secondary mb-1.5 uppercase">
          Date Range
        </label>
        <div className="flex items-center gap-2">
          <Input type="date" value={filters.dateMin} onChange={...} />
          <span className="text-text-muted">–</span>
          <Input type="date" value={filters.dateMax} onChange={...} />
        </div>
      </div>
    </div>
  </div>
)}
```

## Audit Checklist for List Pages

### Critical (Must Fix)
- [ ] Has search input with aria-label - accessibility violation
- [ ] Handles empty initial state - users see nothing, think app is broken
- [ ] Loading state while fetching - users think app froze
- [ ] Cards link to detail pages - dead end without navigation

### Major (Should Fix)  
- [ ] Has relevant filter dropdowns - can't find items efficiently
- [ ] Shows results count - users don't know if search worked
- [ ] Handles empty filtered results - confusing when no matches
- [ ] Grid is responsive (1-4 columns) - mobile users blocked
- [ ] Pagination works correctly - can't access all data
- [ ] Create button in header - no clear path to add items

### Minor (Nice to Have)
- [ ] Indicates when filters are active - visual clarity
- [ ] Has clear filters button - convenience
- [ ] Cards have hover states - interaction feedback
- [ ] Table has sortable headers (if using table) - power user feature
