---
name: table-patterns
description: Data table patterns — sorting, filtering, pagination, virtualization, accessibility standards
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js", "**/*.html"]
alwaysApply: false
---

# Data Table Patterns

Data tables display structured information. Good tables are sortable, filterable, accessible, and performant even with thousands of rows.

---

## Basic Table Structure

**ALWAYS**:
- Use semantic HTML: `<table>`, `<thead>`, `<tbody>`, `<th>`, `<tr>`, `<td>`
- Add `scope` attribute to headers (scope="col", scope="row")
- Use `aria-sort` for sortable columns (ascending, descending, none)
- Provide `aria-label` for table (describes purpose)
- Make table responsive on mobile (horizontal scroll or cards)

**NEVER**:
- Use div/span to fake table structure
- Skip table headers (accessibility breaks)
- Forget `scope` attributes
- Make huge tables that crash on scroll

### ✅ GOOD Table Structure

```typescript
import { useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  status: 'active' | 'inactive';
  joined: Date;
}

export function UsersTable({ users }: { users: User[] }) {
  const [sortBy, setSortBy] = useState<keyof User>('joined');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const handleSort = (column: keyof User) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  const sortedUsers = [...users].sort((a, b) => {
    const aVal = a[sortBy];
    const bVal = b[sortBy];
    const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const getSortIcon = (column: keyof User) => {
    if (sortBy !== column) return '⇅';
    return sortOrder === 'asc' ? '↑' : '↓';
  };

  return (
    <div className="overflow-x-auto">
      <table
        className="w-full border-collapse"
        aria-label="User accounts with status and join date"
      >
        <thead className="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th scope="col" className="px-4 py-3 text-left font-semibold">
              <button
                onClick={() => handleSort('name')}
                className="hover:text-primary-600 flex items-center gap-1"
                aria-sort={sortBy === 'name' ? (sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'}
              >
                Name {getSortIcon('name')}
              </button>
            </th>
            <th scope="col" className="px-4 py-3 text-left font-semibold">
              <button
                onClick={() => handleSort('email')}
                className="hover:text-primary-600"
                aria-sort={sortBy === 'email' ? (sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'}
              >
                Email {getSortIcon('email')}
              </button>
            </th>
            <th scope="col" className="px-4 py-3 text-left font-semibold">
              <button
                onClick={() => handleSort('status')}
                className="hover:text-primary-600"
                aria-sort={sortBy === 'status' ? (sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'}
              >
                Status {getSortIcon('status')}
              </button>
            </th>
            <th scope="col" className="px-4 py-3 text-left font-semibold">
              <button
                onClick={() => handleSort('joined')}
                className="hover:text-primary-600"
                aria-sort={sortBy === 'joined' ? (sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'}
              >
                Joined {getSortIcon('joined')}
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedUsers.map((user) => (
            <tr
              key={user.id}
              className="border-b hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              <td className="px-4 py-3">{user.name}</td>
              <td className="px-4 py-3">{user.email}</td>
              <td className="px-4 py-3">
                <span
                  className={`px-2 py-1 rounded text-sm font-medium ${
                    user.status === 'active'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {user.status}
                </span>
              </td>
              <td className="px-4 py-3">
                {user.joined.toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### ❌ BAD Table Structure

```typescript
// ❌ Using div instead of table
<div className="table">
  <div className="table-row">
    <div className="table-cell">Name</div>
    <div className="table-cell">Email</div>
  </div>
</div>

// ❌ Missing semantic HTML
<div>
  {users.map((user) => (
    <div key={user.id} className="flex">
      <div>{user.name}</div>
      <div>{user.email}</div>
    </div>
  ))}
</div>

// ❌ No headers
<table>
  <tr>
    <td>Name</td>
    <td>Email</td>
  </tr>
</table>
```

---

## Filtering & Search

**ALWAYS**:
- Filter on client-side for < 1000 rows
- Filter server-side for >= 1000 rows
- Debounce search input (300ms)
- Show result count ("23 of 156 results")
- Provide clear filters (dropdown, checkbox, date range)
- Show active filters clearly (badges, reset button)

**NEVER**:
- Filter on every keystroke (kills performance)
- Hide applied filters
- Make filters unclear (ambiguous options)

### ✅ GOOD Filtering Pattern

```typescript
import { useCallback, useMemo, useState } from 'react';
import { debounce } from 'lodash';

interface TableFilters {
  search: string;
  status: 'all' | 'active' | 'inactive';
  joined: { from: Date | null; to: Date | null };
}

export function FilteredUsersTable({ users }: { users: User[] }) {
  const [filters, setFilters] = useState<TableFilters>({
    search: '',
    status: 'all',
    joined: { from: null, to: null },
  });

  // Debounced search
  const debouncedSearch = useMemo(
    () =>
      debounce((value: string) => {
        setFilters((f) => ({ ...f, search: value }));
      }, 300),
    []
  );

  // Memoized filtered results
  const filteredUsers = useMemo(() => {
    return users.filter((user) => {
      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        if (
          !user.name.toLowerCase().includes(searchLower) &&
          !user.email.toLowerCase().includes(searchLower)
        ) {
          return false;
        }
      }

      // Status filter
      if (filters.status !== 'all' && user.status !== filters.status) {
        return false;
      }

      // Date range filter
      if (filters.joined.from && user.joined < filters.joined.from) {
        return false;
      }
      if (filters.joined.to && user.joined > filters.joined.to) {
        return false;
      }

      return true;
    });
  }, [users, filters]);

  return (
    <div className="space-y-4">
      {/* Filter controls */}
      <div className="flex flex-wrap gap-4">
        <input
          type="text"
          placeholder="Search by name or email..."
          onChange={(e) => debouncedSearch(e.target.value)}
          className="px-4 py-2 border rounded-lg flex-1 min-w-[200px]"
        />
        <select
          value={filters.status}
          onChange={(e) =>
            setFilters((f) => ({
              ...f,
              status: e.target.value as TableFilters['status'],
            }))
          }
          className="px-4 py-2 border rounded-lg"
        >
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        <button
          onClick={() =>
            setFilters({
              search: '',
              status: 'all',
              joined: { from: null, to: null },
            })
          }
          className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
        >
          Reset Filters
        </button>
      </div>

      {/* Active filters display */}
      {(filters.search || filters.status !== 'all') && (
        <div className="flex gap-2 flex-wrap">
          {filters.search && (
            <span className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">
              Search: {filters.search} ✕
            </span>
          )}
          {filters.status !== 'all' && (
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              Status: {filters.status} ✕
            </span>
          )}
        </div>
      )}

      {/* Result count */}
      <p className="text-sm text-gray-600">
        {filteredUsers.length} of {users.length} results
      </p>

      {/* Table */}
      <UsersTable users={filteredUsers} />
    </div>
  );
}
```

---

## Pagination

**ALWAYS**:
- Show: previous/next buttons + page numbers + goto page input
- Show items per page selector (10, 25, 50, 100)
- Show total count ("Showing 1-25 of 256")
- Disable prev/next at boundaries
- Preserve filters when paging
- Scroll to table top on page change

**NEVER**:
- Infinite scroll for huge datasets (pagination is clearer)
- Load entire dataset at once
- Forget to disable buttons at boundaries

### ✅ GOOD Pagination Pattern

```typescript
import { useCallback } from 'react';

interface PaginationState {
  pageSize: number;
  currentPage: number;
}

export function PaginatedTable({
  users,
  totalCount,
}: {
  users: User[];
  totalCount: number;
}) {
  const [pagination, setPagination] = useState<PaginationState>({
    pageSize: 25,
    currentPage: 1,
  });

  const totalPages = Math.ceil(totalCount / pagination.pageSize);
  const startIndex = (pagination.currentPage - 1) * pagination.pageSize;
  const endIndex = Math.min(
    startIndex + pagination.pageSize,
    totalCount
  );

  const handlePageChange = useCallback((newPage: number) => {
    setPagination((p) => ({ ...p, currentPage: newPage }));
    // Scroll to table
    document.querySelector('table')?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const handlePageSizeChange = useCallback((newSize: number) => {
    setPagination({
      pageSize: newSize,
      currentPage: 1, // Reset to first page
    });
  }, []);

  return (
    <div className="space-y-4">
      {/* Table */}
      <UsersTable users={users} />

      {/* Pagination controls */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-2">
          <label htmlFor="pageSize" className="text-sm">
            Rows per page:
          </label>
          <select
            id="pageSize"
            value={pagination.pageSize}
            onChange={(e) => handlePageSizeChange(Number(e.target.value))}
            className="px-2 py-1 border rounded"
          >
            <option value={10}>10</option>
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </div>

        <p className="text-sm text-gray-600">
          Showing {startIndex + 1}-{endIndex} of {totalCount} results
        </p>

        <div className="flex items-center gap-2">
          <button
            onClick={() => handlePageChange(pagination.currentPage - 1)}
            disabled={pagination.currentPage === 1}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            ← Previous
          </button>

          {/* Page numbers */}
          <div className="flex gap-1">
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              const page = i + 1;
              return (
                <button
                  key={page}
                  onClick={() => handlePageChange(page)}
                  className={`px-3 py-1 rounded ${
                    pagination.currentPage === page
                      ? 'bg-primary-500 text-white'
                      : 'border hover:bg-gray-100'
                  }`}
                >
                  {page}
                </button>
              );
            })}
            {totalPages > 5 && <span className="px-2">…</span>}
          </div>

          {/* Go to page */}
          <input
            type="number"
            min={1}
            max={totalPages}
            placeholder="Go to"
            onChange={(e) => {
              const page = Number(e.target.value);
              if (page >= 1 && page <= totalPages) {
                handlePageChange(page);
              }
            }}
            className="px-2 py-1 border rounded w-16"
          />

          <button
            onClick={() => handlePageChange(pagination.currentPage + 1)}
            disabled={pagination.currentPage === totalPages}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## Virtualization (Large Datasets)

**ALWAYS**:
- Use virtualization for > 500 rows
- Only render visible rows (huge performance gain)
- Use react-window or react-virtual
- Keep item height consistent
- Show loading state for async data

**NEVER**:
- Render 10,000+ rows in DOM (browser crashes)
- Use virtualization for small datasets (overkill)

### ✅ GOOD Virtualization Pattern

```typescript
import { FixedSizeList as List } from 'react-window';

interface VirtualTableProps {
  items: User[];
  itemSize: number; // Height of each row
}

export function VirtualTable({ items, itemSize = 50 }: VirtualTableProps) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => {
    const user = items[index];
    return (
      <div style={style} className="flex border-b px-4 py-3">
        <div className="flex-1">{user.name}</div>
        <div className="flex-1">{user.email}</div>
        <div className="flex-1">{user.status}</div>
      </div>
    );
  };

  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={itemSize}
      width="100%"
    >
      {Row}
    </List>
  );
}
```

---

## Table Accessibility

**ALWAYS**:
- Provide `aria-label` for table purpose
- Use `scope="col"` for headers
- Use `scope="row"` for row headers (if applicable)
- Make sortable columns keyboard accessible (Enter/Space)
- Announce sort changes with `aria-live` region

**NEVER**:
- Skip headers
- Make tables non-keyboard navigable
- Use color alone to indicate status

### ✅ GOOD Accessible Table

```typescript
export function AccessibleTable({ users }: { users: User[] }) {
  const [sortInfo, setSortInfo] = useState<{
    column: string;
    direction: 'asc' | 'desc';
  } | null>(null);

  return (
    <div role="region" aria-live="polite" aria-label="Table sorted">
      {sortInfo && (
        <p className="sr-only">
          Table sorted by {sortInfo.column} in {sortInfo.direction}ending order
        </p>
      )}
      <table aria-label="User list with status and join date">
        <thead>
          <tr>
            <th scope="col">
              <button
                onClick={() => setSortInfo({ column: 'name', direction: 'asc' })}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    setSortInfo({ column: 'name', direction: 'asc' });
                  }
                }}
              >
                Name
              </button>
            </th>
            {/* More headers */}
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.name}</td>
              {/* More cells */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## Data Table Checklist

- [ ] Semantic HTML (`<table>`, `<thead>`, `<th>`, scope attributes)
- [ ] Sortable columns with `aria-sort`
- [ ] Filterable with debounced search
- [ ] Pagination with prev/next + page numbers
- [ ] Items per page selector
- [ ] Result count display
- [ ] Active filters shown
- [ ] Responsive on mobile (horizontal scroll or cards)
- [ ] Virtualization for > 500 rows
- [ ] Keyboard accessible (Tab, Enter, arrows)
- [ ] WCAG AA contrast
- [ ] Accessible sort announcements

---

## Summary

Good data tables:
1. **Semantic** — Proper HTML structure with scope attributes
2. **Sortable** — Click column headers to sort
3. **Filterable** — Search and status filters
4. **Paginated** — Manageable page sizes
5. **Performant** — Virtualized for large datasets
6. **Accessible** — Keyboard nav, ARIA labels, screen readers

Master these patterns for professional data display.
