---
name: syncfusion-angular-mention
description: Implement the Syncfusion Angular Mention component for user tagging with autocomplete suggestions in contenteditable elements. Covers data binding (local/remote), filtering, templates, sorting, disabled items, localization, accessibility, and popup customization. Use this when adding @mention or tag functionality to Angular applications, configuring trigger characters, customizing suggestion templates, or ensuring accessibility compliance.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Syncfusion Angular Mention Component

## Component Overview & Architecture

The **Mention** component renders an autocomplete suggestion popup when the user types a trigger character (default `@`) inside a target element (a `div[contenteditable]`, `textarea`, or similar). It is designed for:

1. **User tagging** — tag people, teams, or resources using `@`
2. **Hashtag suggestions** — use any custom character (`#`, `/`, etc.) as the trigger
3. **Rich text integration** — works with `contenteditable` divs and editors
4. **Data binding** — supports local arrays (strings, objects, complex objects) and remote DataManager sources
5. **Filtering** — `Contains`, `StartsWith`, `EndsWith` with configurable min-length, debounce, and spacing
6. **Template customization** — item, display, no-records, spinner, and group templates
7. **Disabled items** — mark individual list items as non-selectable
8. **Accessibility** — WCAG 2.2 compliant with full keyboard navigation and ARIA attributes

### Key Characteristics

| Aspect | Details |
|--------|---------|
| **Trigger** | Any single character via `mentionChar` (default `@`) |
| **Target** | Any `HTMLElement` or CSS selector string set via `target` |
| **Data Sources** | Local arrays (strings, objects), remote `DataManager` (OData, Web API) |
| **Filtering** | Built-in: `Contains`, `StartsWith`, `EndsWith`; configurable `minLength`, `allowSpaces` |
| **Display** | `showMentionChar` controls whether the trigger character is shown with selected text |
| **Suffix** | `suffixText` appends a space or newline after the selected item |
| **Accessibility** | WCAG 2.2, Section 508, ADA; keyboard shortcuts: Arrow keys, Enter, Tab, Escape |
| **Localization** | `L10n.load()` for `noRecordsTemplate` locale key |

---

## Documentation Navigation Guide

### 📄 Getting Started
**Read:** [references/getting-started.md](references/getting-started.md)
- Install `@syncfusion/ej2-angular-dropdowns` package
- Set up Angular 21+ project with standalone components
- Import `MentionModule` and required CSS themes
- Create a target `contenteditable` div
- Bind `target` and basic `dataSource`
- Display/customize the mention character with `showMentionChar` and `mentionChar`

### 📄 Data Binding
**Read:** [references/data-binding.md](references/data-binding.md)
- Bind to local arrays of strings, JSON objects, and complex objects
- Map `text`, `value`, `groupBy`, and `iconCss` via `fields` property
- Remote data with `DataManager` using `ODataV4Adaptor` and `WebApiAdaptor`
- Use the `query` property to scope remote requests

### 📄 Filtering
**Read:** [references/filtering.md](references/filtering.md)
- Control filter strategy with `filterType` (`Contains`, `StartsWith`, `EndsWith`)
- Set minimum input length before triggering with `minLength`
- Allow spaces in the middle of a mention search with `allowSpaces`
- Limit visible suggestion count with `suggestionCount`
- Tune debounce delay for remote sources with `debounceDelay`

### 📄 Templates
**Read:** [references/templates.md](references/templates.md)
- Customize suggestion list item layout with `itemTemplate`
- Customize the inserted text representation with `displayTemplate`
- Handle empty results with `noRecordsTemplate`
- Show a loading indicator while fetching remote data with `spinnerTemplate`
- Customize grouped items with `groupTemplate`

### 📄 Customization
**Read:** [references/customization.md](references/customization.md)
- Show/hide the trigger character alongside selected text with `showMentionChar`
- Append a suffix (space, newline) after selection with `suffixText`
- Resize the popup with `popupHeight` and `popupWidth`
- Change the trigger character with `mentionChar`
- Control leading space requirement with `requireLeadingSpace`
- Apply custom CSS classes with `cssClass`
- Highlight searched characters with `highlight`
- Configure `ignoreCase` and `ignoreAccent` for search behavior

### 📄 Sorting & Disabled Items
**Read:** [references/sorting-and-disabled-items.md](references/sorting-and-disabled-items.md)
- Sort suggestions with `sortOrder` (`None`, `Ascending`, `Descending`)
- Mark items as non-selectable via `fields.disabled`
- Dynamically disable items at runtime using the `disableItem` method

### 📄 Accessibility & Localization
**Read:** [references/accessibility-and-localization.md](references/accessibility-and-localization.md)
- WCAG 2.2, Section 508, and ADA compliance
- Full keyboard shortcuts (Arrow Down/Up, Enter, Tab, Escape)
- ARIA attributes: `aria-selected`, `aria-activedescendent`, `aria-owns`
- Localize `noRecordsTemplate` with `L10n.load()`
- RTL support with `enableRtl`

### 📄 API Reference
**Read:** [references/api.md](references/api.md)
- Complete properties reference with types, defaults, and descriptions
- All methods: `addItem`, `disableItem`, `getDataByValue`, `getItems`, `hidePopup`, `showPopup`, `search`, `destroy`
- All events: `dataBound`, `actionFailureTemplate`

---

## Quick Start Example

```typescript
// app.component.ts (Angular 21 Standalone)
import { Component } from '@angular/core';
import { MentionModule } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MentionModule],
  template: `
    <label style="font-size: 15px; font-weight: 600;">Comments</label>
    <div id="mentionElement"
         placeholder="Type @ and tag a user"
         style="min-height: 100px; border: 1px solid #D7D7D7; border-radius: 4px; padding: 8px;">
    </div>
    <ejs-mention [dataSource]="userData" [target]="mentionTarget"></ejs-mention>
  `
})
export class AppComponent {
  public userData: string[] = ['Selma Rose', 'Garth', 'Robert', 'William', 'Joseph'];
  public mentionTarget: string = '#mentionElement';
}
```

**Install the package:**
> ⚠️ **Security note:** Pin the package to a specific version to prevent unintended upgrades
> to potentially compromised releases. Verify the installed version against your lockfile
> (`package-lock.json` / `yarn.lock`) after installation.

```bash
ng add @syncfusion/ej2-angular-dropdowns@33.1.44
```

**Add CSS (`styles.css`):**
> ⚠️ **Security note:** These imports are resolved from `node_modules` at build time.
> Ensure the installed Syncfusion packages match your pinned versions in `package-lock.json`
> or `yarn.lock` before building. Do not source these files from a CDN without
> Subresource Integrity (SRI) hashes.

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-dropdowns/styles/material3.css';
```

---

## Common Patterns

### Pattern 1: Object Data with Field Mapping

```typescript
public userData: { [key: string]: Object }[] = [
  { Name: 'Selma Rose', EmailId: 'selma@gmail.com' },
  { Name: 'Maria', EmailId: 'maria@gmail.com' },
  { Name: 'Robert', EmailId: 'robert@gmail.com' }
];
public fields: Object = { text: 'Name' };
public mentionTarget: string = '#mentionElement';
```

```html
<ejs-mention [dataSource]="userData" [fields]="fields" [target]="mentionTarget"></ejs-mention>
```

### Pattern 2: Custom Trigger Character with showMentionChar

```html
<ejs-mention
  [dataSource]="userData"
  [target]="mentionTarget"
  [mentionChar]="'#'"
  [showMentionChar]="true">
</ejs-mention>
```

### Pattern 3: Remote Data with Popup Width

> ⚠️ **Security note:** Replace the URL below with your own API endpoint. Avoid enabling
> `crossDomain: true` unless your server explicitly requires it and you have validated the
> CORS policy. Always sanitize or restrict user input before it is forwarded to remote sources,
> and verify installed packages against your lockfile (`package-lock.json` / `yarn.lock`).

```typescript
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

public searchData: DataManager = new DataManager({
  url: 'https://your-api-endpoint.example.com/api/',
  adaptor: new ODataV4Adaptor
  // crossDomain: true — enable only if your server requires it and CORS is properly configured
});
public query: Query = new Query().from('Customers').select(['ContactName', 'CustomerID']).take(6);
public fields: Object = { text: 'ContactName', value: 'CustomerID' };
public popupWidth: string = '250px';
```

### Pattern 4: Allow Spaces in Mention Search

```html
<ejs-mention
  [dataSource]="userData"
  [fields]="fields"
  [allowSpaces]="true"
  [target]="mentionTarget">
</ejs-mention>
```

---

## Key Properties Quick Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `target` | HTMLElement \| string | — | Target element where mention suggestions appear |
| `dataSource` | Array \| DataManager | `[]` | Source data for suggestions |
| `fields` | FieldSettingsModel | `{ text: null, value: null }` | Map data columns to component |
| `mentionChar` | string | `'@'` | Character that triggers the suggestion popup |
| `showMentionChar` | boolean | `false` | Show trigger character with inserted text |
| `suffixText` | string | `null` | Text appended after the selected item |
| `filterType` | FilterType | `'Contains'` | How suggestions are matched |
| `minLength` | number | `0` | Minimum chars to trigger filtering |
| `allowSpaces` | boolean | `false` | Allow spaces in mid-mention search |
| `suggestionCount` | number | `25` | Max number of suggestions shown |
| `debounceDelay` | number | `300` | Delay (ms) before filtering fires |
| `sortOrder` | SortOrder | `'None'` | Sort suggestions order |
| `popupHeight` | string \| number | `'300px'` | Popup list height |
| `popupWidth` | string \| number | `'auto'` | Popup list width |
| `highlight` | boolean | `false` | Highlight matched characters |
| `ignoreCase` | boolean | `true` | Case-insensitive search |
| `ignoreAccent` | boolean | — | Ignore diacritics in search |
| `requireLeadingSpace` | boolean | `true` | Require space before trigger character |
| `cssClass` | string | `null` | Custom CSS class(es) on the component |
| `locale` | string | `'en-US'` | Localization culture |
| `enableRtl` | boolean | `false` | Right-to-left rendering |
| `enablePersistence` | boolean | `false` | Persist state between reloads |
| `zIndex` | number | `1000` | Popup z-index |

---

## Workflow Decision Tree

```
Need to implement Mention / @mention tagging?
│
├─ What's your data source?
│   ├─ Local strings/array  → See Data Binding: "Array of simple data"
│   ├─ Local objects        → See Data Binding: "Array of JSON data" + fields mapping
│   └─ Remote API           → See Data Binding: "Binding remote data"
│
├─ Custom trigger character (not @)?
│   └─ YES → [mentionChar]="'#'" (or any single char)
│
├─ Show trigger char in inserted text?
│   └─ YES → [showMentionChar]="true"
│
├─ Multi-word names (e.g., "John Doe")?
│   └─ YES → [allowSpaces]="true"
│
├─ Custom item layout in popup?
│   └─ YES → See Templates: itemTemplate / displayTemplate
│
├─ Need sorted suggestions?
│   └─ YES → See Sorting & Disabled Items: sortOrder
│
├─ Some items should not be selectable?
│   └─ YES → See Sorting & Disabled Items: fields.disabled / disableItem
│
├─ Filtering behavior?
│   ├─ By default (Contains)  → No extra config
│   ├─ StartsWith / EndsWith  → filterType="StartsWith"
│   └─ Minimum typed chars    → [minLength]="3"
│
└─ Need accessibility or localization?
    └─ YES → See Accessibility & Localization reference
```
