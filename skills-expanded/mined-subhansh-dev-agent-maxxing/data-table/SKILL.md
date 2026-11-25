---
name: data-table
description: Generate data tables with sorting, striped rows, hover states, and responsive horizontal scroll.
---

# Data Table Component

```css
.data-table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
}

.data-table th:hover {
  color: rgba(255, 255, 255, 0.7);
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.8);
}

.data-table tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

.data-table tr:last-child td {
  border-bottom: none;
}
```

Rules:
- Sortable columns: add `data-sort` attribute + click handler
- Responsive: wrap in `.data-table-wrapper` with `overflow-x: auto`
- Zebra striping optional: `tr:nth-child(even) td`
