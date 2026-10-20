---
tags: [design, grid, custom, filter, system]
name: ag-grid-custom-filter-system
description: ag-grid Enterprise wrapper with GridContext provider, custom filter components (Boolean, Number, DateRange, SelectMulti), and pagination state management
category: design
trigger: When wrapping ag-grid with a design system, adding custom filter UI components, or managing grid pagination state via React context
version: 1.0.0
source_project: lucida-ui
---

# ag-grid Custom Filter System

## Steps

1. **Create GridProvider + GridContext**:
   ```tsx
   const GridContext = createContext<GridContextType>(null);
   const GridProvider = ({ children }) => {
     const [pagination, setPagination] = useState({ page: 1, pageSize: 20, total: 0 });
     return <GridContext.Provider value={{ pagination, setPagination }}>{children}</GridContext.Provider>;
   };
   ```

2. **Wrap ag-grid in design system component**:
   - Import `AllEnterpriseModule` for full feature set
   - Apply `GridOptions` template (column defaults, row selection mode, etc.)
   - Register custom cell renderers: `DotIconRenderer`, `LinkRenderer`, `SwitchRenderer`

3. **Create custom filter components** (New* pattern):
   - `NewBooleanFilter` — toggle true/false/all
   - `NewNumberFilter` — min/max range inputs
   - `NewDateRangeFilter` — date picker pair with range validation
   - `NewSelectMultiFilter` — multi-select dropdown with search
   - Each renders a filter form, applies criteria to ag-grid `FilterModel`

4. **Wire pagination** via GridContext:
   - `GridPagination` component reads/writes pagination state from context
   - Grid `onPaginationChanged` event syncs with context

5. **InfiniteScroll variant** for dashboards:
   - Use `InfiniteRowModelModule` with `getRows` datasource callback
   - Server-side lazy loading with configurable page size

## Key details
- License key should be externalized to config (not inline in component)
- Custom filters follow `New*` naming convention for distinction from ag-grid built-ins
- GridContext enables pagination state sharing between Grid and external controls
