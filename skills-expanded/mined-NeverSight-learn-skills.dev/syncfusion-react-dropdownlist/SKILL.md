---
name: syncfusion-react-dropdownlist
description: Implement Syncfusion React DropDownList component for single-value selection from predefined lists. Use this when working with dropdowns, select boxes, or single-select lists. This skill covers installation, data binding (local arrays, JSON objects, remote/OData), filtering, grouping, templates, value binding, virtual scrolling, cascading dropdowns, accessibility, styling, and localization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "DropDowns"
---

# Syncfusion React DropDownList

The DropDownList component provides a list of predefined values from which users can select a single value. It supports local and remote data binding, filtering, grouping, custom templates, virtual scrolling, accessibility, and rich customization.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (`@syncfusion/ej2-react-dropdowns`)
- CSS imports with tailwind3 theme
- Basic DropDownList (functional and class components)
- Binding a data source
- Configuring popup height and width

### Data Binding & Value Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding primitive arrays (strings, numbers)
- Binding JSON object arrays with `fields` mapping (`text`, `value`, `groupBy`, `iconCss`)
- Remote data with `DataManager` (OData, ODataV4, WebAPI adaptors)
- Value binding: preselecting values, binding primitive vs. complex objects
- Disabling individual items with `fields.disabled`

### Filtering
📄 **Read:** [references/filtering.md](references/filtering.md)
- Enabling `allowFiltering` for search-as-you-type
- Handling the `filtering` event with `updateData`
- Filter types: `startswith`, `contains`, case-sensitive options
- Remote/server-side filtering
- Minimum search length (`minLength`)
- Highlight filtered text, custom search logic

### Grouping & Templates
📄 **Read:** [references/grouping-and-templates.md](references/grouping-and-templates.md)
- Grouping items with the `groupBy` field
- Fixed and inline group headers
- Custom group header template
- Item template, value (selected) template
- Header and footer templates
- No-records and action-failure templates

### Features & Configuration
📄 **Read:** [references/features-and-configuration.md](references/features-and-configuration.md)
- Sorting (`sortOrder`: ascending, descending)
- Virtual scrolling for large lists (`enableVirtualization`)
- Popup resize (`allowResize`)
- Incremental search, clear button, readonly, disabled
- RTL support, Preact usage

### Accessibility, Styling & Localization
📄 **Read:** [references/accessibility-styling-localization.md](references/accessibility-styling-localization.md)
- WCAG 2.2 / Section 508 compliance
- Keyboard navigation shortcuts
- ARIA roles and attributes
- CSS class customization
- Localization (`L10n`, `noRecordsTemplate`, `actionFailureTemplate`)

### How-To Patterns
📄 **Read:** [references/how-to.md](references/how-to.md)
- Add, remove, or modify items dynamically
- Cascading (dependent) dropdowns
- Multiple cascading dropdowns
- Remote data how-to
- Close popup on scroll, tooltip on items, icons in items
- Value change event, clearing selected value

---

## Quick Start Example

```tsx
// 1. Install
// npm install @syncfusion/ej2-react-dropdowns --save

// 2. CSS in src/App.css
// @import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";

import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

export default function App() {
  const sportsData: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <DropDownListComponent
      id="ddlelement"
      dataSource={sportsData}
      placeholder="Select a game"
    />
  );
}
```

## Common Patterns

### JSON Object Data with Fields Mapping
```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const countryData = [
    { Id: 'au', Country: 'Australia' },
    { Id: 'br', Country: 'Brazil' },
    { Id: 'cn', Country: 'China' },
    { Id: 'in', Country: 'India' },
  ];
  const fields = { text: 'Country', value: 'Id' };

  return (
    <DropDownListComponent
      dataSource={countryData}
      fields={fields}
      placeholder="Select a country"
    />
  );
}
```

### Filtering (Search-as-you-type)
```tsx
import { DropDownListComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';

export default function App() {
  const searchData = [
    { Index: 's1', Country: 'Alaska' },
    { Index: 's2', Country: 'California' },
    { Index: 's3', Country: 'Florida' },
  ];
  const fields = { text: 'Country', value: 'Index' };

  function onFiltering(args: FilteringEventArgs) {
    let query = new Query();
    query = args.text !== '' ? query.where('Country', 'startswith', args.text, true) : query;
    args.updateData(searchData, query);
  }

  return (
    <DropDownListComponent
      dataSource={searchData}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      placeholder="Select a country"
    />
  );
}
```

### Preselect a Value
```tsx
<DropDownListComponent
  dataSource={sportsData}
  value="Cricket"
  placeholder="Select a game"
/>
```

### Grouped Items
```tsx
const vegetableData = [
  { Vegetable: 'Cabbage', Category: 'Leafy and Salad', Id: 'item1' },
  { Vegetable: 'Chickpea', Category: 'Beans', Id: 'item6' },
  { Vegetable: 'Garlic',   Category: 'Bulb and Stem', Id: 'item9' },
];
const fields = { groupBy: 'Category', text: 'Vegetable', value: 'Id' };

<DropDownListComponent dataSource={vegetableData} fields={fields} placeholder="Select a vegetable" />
```

## Key Props

| Prop | Type | Purpose |
|---|---|---|
| `dataSource` | `any[] \| DataManager` | Data for the list items |
| `fields` | `FieldSettingsModel` | Maps `text`, `value`, `groupBy`, `iconCss`, `disabled` |
| `value` | `string \| number` | Selected/preselected value |
| `placeholder` | `string` | Input placeholder text |
| `allowFiltering` | `boolean` | Enables search filtering |
| `filtering` | `event` | Handler for custom filter logic |
| `popupHeight` | `string` | Popup list height (default auto) |
| `popupWidth` | `string` | Popup list width (default matches input) |
| `sortOrder` | `SortOrder` | `'None'`, `'Ascending'`, `'Descending'` |
| `enableVirtualization` | `boolean` | Virtual scroll for large data |
| `allowResize` | `boolean` | User-resizable popup |
| `enabled` | `boolean` | Enable/disable entire component |
| `readonly` | `boolean` | Read-only mode |
| `showClearButton` | `boolean` | Shows ✕ button to clear selection |
| `enableRtl` | `boolean` | Right-to-left layout |

## Common Use Cases

**Simple static list** → Pass `string[]` to `dataSource`, done.

**Data from API** → Use `DataManager` with `WebApiAdaptor`; read `references/data-binding.md`.

**Search/filter as user types** → Set `allowFiltering={true}`, handle `filtering` event; read `references/filtering.md`.

**Categorized items** → Map `groupBy` field; read `references/grouping-and-templates.md`.

**Custom item layout** → Use `itemTemplate`; read `references/grouping-and-templates.md`.

**Large dataset (10k+ items)** → Enable `enableVirtualization` + inject `VirtualScroll`; read `references/features-and-configuration.md`.

**Dependent dropdowns** → Reload second dropdown's `dataSource` on first's `change` event; read `references/how-to.md`.
