---
name: syncfusion-angular-dropdowns
description: Comprehensive guide for implementing Syncfusion Angular dropdown components including AutoComplete, ComboBox, DropDownList, ListBox, Mention, MultiSelect and MultiColumn ComboBox. Use this when building selection interfaces, data binding, filtering, cascading dropdowns, custom templates, and accessible dropdown experiences in Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Syncfusion Angular Dropdowns

## Security & Trust Boundary

### Default posture: local data only

**All dropdown components in this skill default to local, in-memory data sources.**
Binding a component to a remote HTTP endpoint (via `DataManager` or any Observable/HTTP
source) is a **non-default, elevated-risk operation** that requires an explicit security
review before it is permitted in production code.

> ⛔ **Do not generate or suggest remote `DataManager` / HTTP data-source configurations
> unless the consuming application has passed a security review confirming that:**
> 1. The target endpoint is owned and operated by the same team as the application.
> 2. The endpoint enforces authentication, authorization, and input validation.
> 3. All responses are sanitized before being bound to a component `dataSource`.
> 4. A Content Security Policy (CSP) covering the origin is in place.

### Mandatory security requirements

| # | Requirement |
|---|-------------|
| 1 | **Local data by default.** Use plain TypeScript arrays for `dataSource` unless a remote source has been explicitly approved. |
| 2 | **No public or third-party URLs.** Never configure a data source that fetches from an endpoint outside the application's own origin. |
| 3 | **Sanitize all external data before binding.** Any value that originates outside the application (API response, local-storage read) must be stripped of HTML/script content before assignment to `dataSource` or `value`. |
| 4 | **Sanitize user filter input.** Before forwarding typed text to any server query, strip non-alphanumeric characters to prevent injection. |
| 5 | **No `crossDomain: true` by default.** CORS relaxation in `DataManager` must be explicitly justified and reviewed. |
| 6 | **Pin package versions.** Every `@syncfusion/ej2-*` dependency must be locked to an exact version in `package.json`; verify against the lockfile after every install. |
| 7 | **No CDN asset loading without SRI.** CSS/JS must be resolved from `node_modules` at build time, not fetched from a CDN at runtime without Subresource Integrity hashes. |
| 8 | **No sensitive data in local storage.** `enablePersistence` must never store tokens, credentials, or PII; sanitize any value read back before use. |

---

## AutoComplete

A text input component that provides matching suggestions as the user types. Supports free-form input, remote data, filtering strategies, grouping, virtual scrolling, and full Angular forms integration.

### Component Overview & Architecture

The **AutoComplete** is a text input component that provides matching suggestions as the user types. It is designed for:

1. **Type-ahead suggestions** — shows matching items from a data source as the user types
2. **Free-form input** — users can type any value, not restricted to the list
3. **Search/filter** — multiple filter strategies (StartsWith, Contains, EndsWith)
4. **Autofill** — automatically completes the first matched suggestion in the input
5. **Grouped suggestions** — categorize items by a `groupBy` field
6. **Virtual scrolling** — efficiently handles thousands of items
7. **Template customization** — item, group, header, footer, and empty-state templates

### Key Characteristics

| Aspect | Details |
|--------|---------|
| **Selection** | Single item; user can also type any free-form value |
| **Data Sources** | Local arrays, remote DataManager, OData, Web API, Observable (async pipe) |
| **Filtering** | Built-in filtering: `StartsWith`, `EndsWith`, `Contains` |
| **Autofill** | Completes the first match inline as the user types |
| **Performance** | Virtual scrolling for large datasets (1,000+ items) |
| **Forms** | Template-driven (`ngModel`) and reactive (`FormControl`) form integration |
| **Accessibility** | WCAG 2.2 compliant, full keyboard navigation, ARIA attributes |
| **Customization** | Item, group, header, footer, noRecords, actionFailure templates; CSS theming |

---

### Documentation Navigation Guide

#### 📄 Getting Started
**Read:** [references/autocomplete-getting-started.md](references/autocomplete-getting-started.md)
- Install `@syncfusion/ej2-angular-dropdowns` package
- Set up Angular 21+ project with standalone components
- Import `AutoCompleteModule` and required CSS themes
- Create your first AutoComplete with basic data binding
- Configure popup height, width, and placeholder
- Enable two-way binding with `[(value)]`

#### 📄 Data Binding
**Read:** [references/autocomplete-data-binding.md](references/autocomplete-data-binding.md)
- Bind to local arrays (strings, numbers, objects, complex objects)
- Map `value`, `text`, and `iconCss` fields via `fields` property
- Remote data using DataManager with OData, Web API adapters
- Async pipe pattern for RxJS Observables
- Object binding with `allowObjectBinding`
- Preselecting values using the `value` property

#### 📄 Filtering & Search
**Read:** [references/autocomplete-filtering-and-search.md](references/autocomplete-filtering-and-search.md)
- Configure `filterType` (StartsWith, Contains, EndsWith)
- Limit suggestion count with `suggestionCount`
- Minimum character threshold with `minLength`
- Case-sensitive filtering with `ignoreCase`
- Diacritics/accent-insensitive filtering with `ignoreAccent`
- Debounce delay to optimize remote filtering with `debounceDelay`
- Custom filtering via the `filtering` event with `updateData`

#### 📄 Grouping & Templates
**Read:** [references/autocomplete-grouping-and-templates.md](references/autocomplete-grouping-and-templates.md)
- Group suggestions by category using `fields.groupBy`
- Item templates for custom rendering
- Group header templates (inline and fixed)
- Header and footer templates for the popup
- Empty state with `noRecordsTemplate`
- Action failure template for remote data errors

#### 📄 Feature Configuration
**Read:** [references/autocomplete-feature-configuration.md](references/autocomplete-feature-configuration.md)
- Autofill: inline suggestion completion with `autofill` property
- Highlight matched characters with `highlight` property
- Disable individual items with `fields.disabled` or `disableItem` method
- Disable entire component with `enabled` property
- Resizable popup with `allowResize`
- Virtual scrolling for large datasets with `enableVirtualization`
- Show/hide popup button with `showPopupButton`
- Show/hide clear button with `showClearButton`
- RTL support with `enableRtl`
- Sort order with `sortOrder`

#### 📄 Form Support & Validation
**Read:** [references/autocomplete-form-support-and-validation.md](references/autocomplete-form-support-and-validation.md)
- Template-driven forms using `ngModel` and `FormsModule`
- Reactive forms using `FormControl`, `FormGroup`, and `ReactiveFormsModule`
- Binding and validation patterns
- Pre-selecting values via form model

#### 📄 Accessibility & Localization
**Read:** [references/autocomplete-accessibility-and-localization.md](references/autocomplete-accessibility-and-localization.md)
- WCAG 2.2, Section 508, and ADA compliance
- Full keyboard shortcuts (Arrow keys, Tab, Enter, Escape, Alt+Down/Up)
- ARIA attributes: `aria-haspopup`, `aria-expanded`, `aria-selected`, `aria-autocomplete`
- Screen reader support and focus management
- Localization with `L10n.load()` for `noRecordsTemplate` and `actionFailureTemplate`
- RTL language support

#### 📄 Advanced Patterns & How-To
**Read:** [references/autocomplete-advanced-patterns-how-to.md](references/autocomplete-advanced-patterns-how-to.md)
- Autofill feature with the `autofill` property
- Highlight searched characters with the `highlight` property
- Multi-field custom filtering with `Predicate` (filter by both Name and Code)
- Icon support via `fields.iconCss`
- Suggestion list on focus from browser local storage
  > ⚠️ **Security note:** Local storage is accessible to any JavaScript running on the same
  > origin and is a common XSS attack surface. Never store sensitive data (tokens, PII) in
  > local storage. Sanitize any values read from local storage before binding them to the
  > component's `dataSource` or `value`.
- Custom search and highlight styling

#### 📄 API Reference
**Read:** [references/autocomplete-api.md](references/autocomplete-api.md)
- Complete properties reference with types, defaults, and descriptions
- All methods with signatures and usage
- All events with payload types and handler examples

---

### Quick Start Example

```typescript
// app.component.ts (Angular 21 Standalone)
import { Component } from '@angular/core';
import { AutoCompleteModule } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AutoCompleteModule],
  template: `
    <ejs-autocomplete
      id="sports"
      [dataSource]="sportsData"
      placeholder="Find a sport"
      [(value)]="selectedValue">
    </ejs-autocomplete>
  `
})
export class AppComponent {
  public sportsData: string[] = [
    'Badminton', 'Basketball', 'Cricket',
    'Football', 'Golf', 'Hockey', 'Tennis'
  ];
  public selectedValue: string = '';
}
```

**Install the package:**
> ⚠️ **Security note:** Pin the package to a specific version to prevent unintended upgrades
> to potentially compromised releases. Verify the installed version against your lockfile
> (`package-lock.json` / `yarn.lock`) after installation.

```bash
ng add @syncfusion/ej2-angular-dropdowns@<version>
```

**Add CSS (styles.css):**
> ⚠️ **Security note:** These imports are resolved from `node_modules` at build time.
> Ensure the installed Syncfusion packages match your pinned versions in `package-lock.json`
> or `yarn.lock` before building. Do not source these files from a CDN without
> Subresource Integrity (SRI) hashes.

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
```

---

### Common Patterns

#### Pattern 1: Filter with Complex Object Data

```typescript
// Map fields for object array
public fields: Object = { value: 'Game' };
public sportsData: { [key: string]: Object }[] = [
  { Id: 'Game1', Game: 'Badminton' },
  { Id: 'Game2', Game: 'Cricket' }
];
```

```html
<ejs-autocomplete [dataSource]="sportsData" [fields]="fields" placeholder="Find a game">
</ejs-autocomplete>
```

**When to use:** Whenever your data is an array of objects and you need to display one field as the suggestion text.

---

#### Pattern 2: Autofill + Highlight

```html
<ejs-autocomplete
  [dataSource]="data"
  [autofill]="true"
  [highlight]="true"
  filterType="StartsWith">
</ejs-autocomplete>
```

**When to use:** Search bars where users expect inline completion and visual emphasis on matched text.

---

#### Pattern 3: Remote Data with Debounce

> 🔒 **Security policy — remote data is a restricted pattern.**
> Binding AutoComplete to a remote endpoint requires a security review (see
> [Security & Trust Boundary](#security--trust-boundary) above) before use in production.
> Remote data binding details and requirements are documented in
> [references/autocomplete-data-binding.md](references/autocomplete-data-binding.md).
> **No remote `DataManager` example is provided here by default.**

**When to use:** API-backed autocomplete where you want to reduce request frequency — only after the endpoint and data pipeline have been reviewed per the security requirements above.

---

#### Pattern 4: Virtual Scrolling for Large Datasets

```typescript
import { AutoCompleteComponent, VirtualScroll } from '@syncfusion/ej2-angular-dropdowns';
AutoCompleteComponent.Inject(VirtualScroll);
```

```html
<ejs-autocomplete
  [dataSource]="records"
  [fields]="fields"
  [enableVirtualization]="true"
  popupHeight="200px">
</ejs-autocomplete>
```

**When to use:** Datasets with 1,000+ items where rendering all DOM elements at once is costly.

---

### Key Properties Quick Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `dataSource` | Array \| DataManager | `[]` | Source data for suggestions |
| `fields` | FieldSettingsModel | `{ value: null }` | Map data columns to component |
| `placeholder` | string | `null` | Hint text when empty |
| `value` | string \| number \| boolean \| object | `null` | Selected/typed value |
| `filterType` | FilterType | `'Contains'` | How suggestions are matched |
| `minLength` | number | `1` | Minimum chars to trigger suggestions |
| `suggestionCount` | number | `20` | Max suggestions shown |
| `autofill` | boolean | `false` | Inline completion of first match |
| `highlight` | boolean | `false` | Highlight matched characters |
| `ignoreCase` | boolean | `true` | Case-insensitive filtering |
| `ignoreAccent` | boolean | — | Ignore diacritics in filtering |
| `debounceDelay` | number | `300` | Delay (ms) before filtering fires |
| `enableVirtualization` | boolean | `false` | Virtual scroll for large data |
| `allowResize` | boolean | `false` | Resizable popup |
| `showClearButton` | boolean | `true` | Show ✕ to clear value |
| `showPopupButton` | boolean | `false` | Show dropdown toggle button |
| `enabled` | boolean | `true` | Enable/disable entire component |
| `readonly` | boolean | `false` | Prevent user edits |
| `allowObjectBinding` | boolean | `false` | Bind value as full object |
| `sortOrder` | SortOrder | `null` | Sort suggestions (Ascending/Descending) |
| `popupHeight` | string \| number | `'300px'` | Popup list height |
| `popupWidth` | string \| number | `'100%'` | Popup list width |
| `locale` | string | `'en-US'` | Localization culture |
| `enableRtl` | boolean | `false` | Right-to-left rendering |

---

### Workflow Decision Tree

```
Need to implement AutoComplete?
│
├─ What's your data source?
│   ├─ Local array → See Data Binding: "Array of string" or "Array of object"
│   └─ Remote API  → See Data Binding: "Bind to remote data"
│
├─ How should filtering work?
│   ├─ Default (Contains)   → No extra config needed
│   ├─ StartsWith           → filterType="StartsWith"
│   ├─ Custom multi-field   → See Advanced Patterns: "Custom filtering"
│   └─ Accent-insensitive   → [ignoreAccent]="true"
│
├─ Need autofill (inline completion)?
│   └─ YES → [autofill]="true" + filterType="StartsWith"
│
├─ Highlight matched text?
│   └─ YES → [highlight]="true"
│
├─ Large dataset (1,000+ items)?
│   └─ YES → [enableVirtualization]="true" + inject VirtualScroll
│
├─ Using inside a form?
│   ├─ Template-driven → See Form Support: "ngModel"
│   └─ Reactive        → See Form Support: "FormControl"
│
└─ Need accessibility or localization?
    └─ YES → See Accessibility & Localization reference
```

## ComboBox

A flexible dropdown component that allows users to select from a predefined list or enter a custom value. Supports filtering, grouping, templates, virtual scrolling, and full Angular forms integration.

### Component Overview & Architecture

The **ComboBox** is a flexible dropdown component that allows users to:
1. **Select from a list** of predefined options
2. **Enter custom values** when `allowCustom` is enabled
3. **Search/filter** items as they type
4. **Group items** by category
5. **Customize display** with templates for items, groups, headers, footers

### Key Characteristics

| Aspect | Details |
|--------|---------|
| **Selection** | Single item from predefined list or custom value |
| **Data Sources** | Local arrays, remote DataManager, OData, Web API, async data |
| **Filtering** | Built-in filtering with configurable strategies (StartsWith, Contains, EndsWith) |
| **Performance** | Virtual scrolling for large datasets (10,000+ items) |
| **Forms** | Works with template-driven forms (ngModel) and reactive forms (FormControl) |
| **Accessibility** | WCAG 2.2 compliant, full keyboard navigation, ARIA attributes |
| **Customization** | Templates for items, groups, headers; CSS theming support |

---

### Documentation Navigation Guide

#### 📄 Getting Started
**Read:** [references/combobox-getting-started.md](references/combobox-getting-started.md)
- Install `@syncfusion/ej2-angular-dropdowns` package
- Set up Angular 21+ project with standalone components
- Import required modules and CSS themes
- Create your first ComboBox with minimal code
- Basic event handlers and configuration

#### 📄 Data Binding & Sources
**Read:** [references/combobox-data-binding.md](references/combobox-data-binding.md)
- Bind to local arrays (strings, numbers, objects)
- Map text and value fields for complex data
- Remote data from Web APIs, OData services
- DataManager configuration for different data adapters
- Async pipe for RxJS Observables
- Handling dynamic data updates

#### 📄 Filtering & Search
**Read:** [references/combobox-filtering-and-search.md](references/combobox-filtering-and-search.md)
- Enable filtering with `allowFiltering` property
- Configure filter types (StartsWith, Contains, EndsWith, etc.)
- Case-sensitive filtering for strict matching
- Diacritics filtering for accent-insensitive search
- Debounce delay to optimize remote requests
- Minimum filter character requirements
- Custom filtering with remote queries

#### 📄 Grouping & Templates
**Read:** [references/combobox-grouping-and-templates.md](references/combobox-grouping-and-templates.md)
- Group items by category using `groupBy` field
- Item templates for custom item rendering
- Group header templates (inline and fixed)
- Footer templates for additional information
- Combining multiple templates effectively
- Template performance optimization

#### 📄 Advanced Feature Configuration
**Read:** [references/combobox-feature-configuration.md](references/combobox-feature-configuration.md)
- Disable specific items or the entire component
- Read-only mode for display-only scenarios
- Virtual scrolling for thousands of items
- Dynamic resize behavior
- Allow custom values not in the list
- Styling and theme integration
- RTL support for Arabic/Hebrew

#### 📄 Form Support & Validation
**Read:** [references/combobox-form-support-and-validation.md](references/combobox-form-support-and-validation.md)
- Two-way binding with template-driven forms (ngModel)
- Reactive forms with FormControl and FormGroup
- Built-in and custom validators
- Form submission and validation state
- Disabled ComboBox in form context
- Error message display patterns

#### 📄 Accessibility & Localization
**Read:** [references/combobox-accessibility-and-localization.md](references/combobox-accessibility-and-localization.md)
- WCAG 2.2, Section 508, and ADA compliance
- Keyboard navigation shortcuts (arrow keys, Tab, Enter, Escape)
- Screen reader support with ARIA attributes
- Focus management and visual indicators
- Localization strings for different languages
- Right-to-left (RTL) language support

#### 📄 Advanced Patterns & How-To Guides
**Read:** [references/combobox-advanced-patterns-and-how-to.md](references/combobox-advanced-patterns-and-how-to.md)
- Autofill suggestions for autocomplete behavior
- Cascading ComboBoxes with dependent dropdowns
- Icons and emoji support in list items
- Resizable popup for better visibility
- Real-world patterns (search, live data, grouping)
- Performance optimization techniques

#### 📄 API Reference
**Read:** [references/combobox-api.md](references/combobox-api.md)
- Complete properties reference with types, defaults, and examples
- All methods with signatures, parameters, and usage examples
- All events with payload types and handler examples
- Notes on template syntax, two-way binding, and virtual scrolling
- Links to official Syncfusion documentation

---

### Quick Start Example

#### Minimal Setup (5 minutes)

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ComboBoxComponent, ComboBoxModule } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ComboBoxModule],
  template: `
    <ejs-combobox
      [dataSource]="data"
      fields="{ text: 'text', value: 'id' }"
      placeholder="Select a language"
      [(ngModel)]="selectedValue">
    </ejs-combobox>
  `
})
export class AppComponent {
  selectedValue = '';
  data = [
    { id: '1', text: 'JavaScript' },
    { id: '2', text: 'TypeScript' },
    { id: '3', text: 'Angular' },
    { id: '4', text: 'React' }
  ];
}
```

**What's happening:**
1. Import `ComboBoxComponent` from `@syncfusion/ej2-angular-dropdowns`
2. Define data array with objects (id, text)
3. Use `fields` to map text and value fields
4. Bind selected value with `[(ngModel)]`
5. Set placeholder for empty state

---

### Common Patterns & Workflows

#### Pattern 1: Autocomplete with Autofill

```typescript
[autofill]="true"              // Auto-complete suggestions
[allowFiltering]="true"        // Enable typing
filterType="StartsWith"        // Match from beginning
```

**When to use:** Skills, tags, email domains (user types 'j', sees 'JavaScript')

See: [Advanced Patterns](references/combobox-advanced-patterns-and-how-to.md#autofill-suggestions)

---

#### Pattern 2: Cascading Dependent Dropdowns

```typescript
// Country → State → City relationship
onCountryChange() {
  this.states = this.getStatesFor(country);
}

onStateChange() {
  this.cities = this.getCitiesFor(state);
}
```

**When to use:** Address selection, hierarchical data (country/state/city)

See: [Advanced Patterns](references/combobox-advanced-patterns-and-how-to.md#cascading-comboboxes)

---

#### Pattern 3: Grouped Items with Icons

```typescript
fields = { 
  text: 'Name', 
  value: 'Id', 
  groupBy: 'Category',
  iconCss: 'Icon'
};
```

**When to use:** Visual organization (languages with icons, file types)

See: [Advanced Patterns](references/combobox-advanced-patterns-and-how-to.md#icons-in-items)

---

#### Pattern 4: Resizable Dropdown for Long Content

```typescript
[allowResize]="true"           // Enable resize handle
itemTemplate="customTemplate"  // Show rich content
```

**When to use:** Product listings, descriptions, detailed information

See: [Advanced Patterns](references/combobox-advanced-patterns-and-how-to.md#resizable-popup)

---

### Key Props & Configuration

#### Essential Properties

| Property | Type | Default | When to Use |
|----------|------|---------|-----------|
| `dataSource` | Array \| DataManager | `[]` | Specify items to display |
| `fields` | Object | `{ text, value }` | Map data structure to ComboBox |
| `placeholder` | string | `''` | Show hint when empty |
| `allowFiltering` | boolean | `false` | Enable search/filter |
| `allowCustom` | boolean | `false` | Allow values not in list |
| `readonly` | boolean | `false` | Prevent editing |
| `enabled` | boolean | `true` | Disable entire component |
| `[(ngModel)]` | any | undefined | Two-way value binding |

#### Advanced Properties

| Property | Type | When to Use |
|----------|------|-----------|
| `itemTemplate` | string \| TemplateRef | Custom item rendering |
| `groupTemplate` | string \| TemplateRef | Custom group header display |
| `footerTemplate` | string \| TemplateRef | Add info below list |
| `enableVirtualization` | boolean | 10,000+ items (performance) |
| `groupBy` | string | Organize items by category |
| `filterType` | string | StartsWith \| Contains \| EndsWith |
| `debounceDelay` | number | Remote data request delay |

---

### Component Lifecycle

```
1. CREATE: Component initialized
   ↓
2. DATA BIND: dataSource loaded & displayed
   ↓
3. USER INTERACTION: typing, clicking, keyboard
   ↓
4. FILTER/SEARCH: items filtered based on input
   ↓
5. SELECT: user chooses item or enters custom value
   ↓
6. VALUE UPDATE: ngModel updates, events fire
   ↓
7. DESTROY: component cleaned up
```

**Key events to handle:**
- `change`: When selected value changes
- `filtering`: When user types (filter queries)
- `select`: When item is selected
- `focus`: When component gets focus
- `blur`: When component loses focus

---

### Workflow Decision Tree

**Need to implement ComboBox? Follow this decision tree:**

```
1. Do you have data to display?
   ├─ YES: Go to "Data Binding & Sources" reference
   └─ NO: Define your data array first

2. Do users need to search/filter?
   ├─ YES: Go to "Filtering & Search" reference
   └─ NO: allowFiltering = false (default)

3. Do you need to group items?
   ├─ YES: Go to "Grouping & Templates" reference
   └─ NO: Skip grouping configuration

4. Are you using a form?
   ├─ YES: Go to "Form Support & Validation" reference
   └─ NO: Use standalone ComboBox

5. Is accessibility required?
   ├─ YES: Go to "Accessibility & Localization" reference
   └─ NO: Still recommended for compliance

6. Performance issues with large datasets?
   ├─ YES: Enable virtual scrolling + pagination
   └─ NO: Standard rendering is fine
```

---

### Next Steps

1. **Start here:** [Getting Started](references/combobox-getting-started.md) - Set up your first ComboBox
2. **Bind data:** [Data Binding & Sources](references/combobox-data-binding.md) - Connect to your data
3. **Add search:** [Filtering & Search](references/combobox-filtering-and-search.md) - Enable user filtering
4. **Customize:** [Grouping & Templates](references/combobox-grouping-and-templates.md) - Style and organize display
5. **Advanced:** [Advanced Patterns & How-To](references/combobox-advanced-patterns-and-how-to.md) - Autofill, cascading, icons, resizing
6. **Features:** [Feature Configuration](references/combobox-feature-configuration.md) - Enable advanced features
7. **Integrate:** [Form Support](references/combobox-form-support-and-validation.md) - Connect to forms
8. **Polish:** [Accessibility](references/combobox-accessibility-and-localization.md) - Ensure compliance
9. **Reference:** [API Reference](references/combobox-api.md) - Full properties, methods, and events reference

---

### Additional Resources

- [Syncfusion Angular ComboBox API Reference](https://ej2.syncfusion.com/angular/documentation/api/combo-box/)
- [Angular Version Support](https://ej2.syncfusion.com/angular/documentation/system-requirement#angular-version-compatibility)
- [DataManager Documentation](https://ej2.syncfusion.com/angular/documentation/data/data-manager/overview/)
- [Component Themes & Styling](https://ej2.syncfusion.com/angular/documentation/introduction/themes/)

## DropDownList

A single-value selection component from a predefined list. Supports local and remote data sources, filtering, grouping, custom templates, virtualization for large datasets, and full Angular forms integration.

### Documentation Navigation Guide

#### Getting Started
📄 **Read:** [references/dropdownlist-getting-started.md](references/dropdownlist-getting-started.md)
- Installation and Angular CLI setup
- Installing `@syncfusion/ej2-angular-dropdowns`
- CSS/theme imports for Material3
- Adding `<ejs-dropdownlist>` to the template
- Basic data binding with `[dataSource]`
- Popup height/width configuration
- Two-way binding with `[(value)]`

#### Data Binding
📄 **Read:** [references/dropdownlist-data-binding.md](references/dropdownlist-data-binding.md)
- Binding primitive arrays (strings, numbers)
- Binding arrays of objects with `[fields]` mapping
- Binding to nested/complex objects
- Remote data via `DataManager` (OData, Web API)
- Async pipe with Observable data streams
- Value binding (primitive and object types with `allowObjectBinding`)

#### Filtering
📄 **Read:** [references/dropdownlist-filtering.md](references/dropdownlist-filtering.md)
- Enabling search with `[allowFiltering]`
- Using the `filtering` event and `updateData()` method
- Minimum character threshold before filtering starts
- Filter types: `contains`, `startsWith`, `endsWith`
- Case-sensitive filtering
- Diacritics/accent-insensitive filtering
- Debounce delay for performance optimization

#### Templates
📄 **Read:** [references/dropdownlist-templates.md](references/dropdownlist-templates.md)
- Item template: customize each list item
- Value template: customize the selected value display
- Group template: customize group header appearance
- Header template: static element at popup top
- Footer template: static element at popup bottom
- No-records template: empty state display
- Action failure template: error state display

#### Grouping & Virtualization
📄 **Read:** [references/dropdownlist-grouping-and-virtualization.md](references/dropdownlist-grouping-and-virtualization.md)
- Grouping items with `groupBy` field
- Inline and fixed floating group headers
- Virtual scrolling with `[enableVirtualization]` for large lists
- Virtual scrolling with remote data
- Combining filtering and virtualization
- Customizing item count in virtual mode

#### Disabled Items & Forms
📄 **Read:** [references/dropdownlist-disabled-items-and-forms.md](references/dropdownlist-disabled-items-and-forms.md)
- Disabling specific items via `fields.disabled`
- Dynamic `disableItem()` method (by value, index, or element)
- Disabling the entire component with `[enabled]="false"`
- Template-driven forms with `[(ngModel)]`
- Reactive forms with `FormControl` and `FormGroup`

#### Customization & Styling
📄 **Read:** [references/dropdownlist-customization-and-styling.md](references/dropdownlist-customization-and-styling.md)
- CSS overrides for wrapper, icon, focus states
- Outline theme focus customization
- Popup appearance and list item styles
- Float label and placeholder styling
- Mandatory asterisk pattern
- Localization with `L10n` class
- RTL (right-to-left) support

#### How-To Recipes
📄 **Read:** [references/dropdownlist-how-to.md](references/dropdownlist-how-to.md)
- Add / remove / clear items dynamically
- Close popup programmatically
- Cascading DropDownLists
- Customize group header template
- Highlight filtered characters
- Incremental search behavior
- Modify remote data results
- Remote data item count display
- Tooltip on list items
- Value change event handling
- Icon support in list items

#### API Reference
📄 **Read:** [references/dropdownlist-api.md](references/dropdownlist-api.md)
- Complete properties reference with types, defaults, and usage examples
- All methods with signatures, parameters, and return types
- All events with argument interfaces and usage examples
- Interface details: `FieldSettingsModel`, `ChangeEventArgs`, `SelectEventArgs`, `PopupEventArgs`, `FilteringEventArgs`
- Quick-reference summary tables for properties, methods, and events

### Quick Start Example

```typescript
import { Component, OnInit } from '@angular/core';
import { DropDownListModule } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  standalone: true,
  imports: [DropDownListModule],
  selector: 'app-root',
  template: `
    <ejs-dropdownlist
      id="ddl"
      [dataSource]="sports"
      [fields]="fields"
      placeholder="Select a sport"
      [(value)]="selectedValue"
      (change)="onChange($event)">
    </ejs-dropdownlist>
    <p>Selected: {{ selectedValue }}</p>
  `
})
export class AppComponent implements OnInit {
  public sports: { id: number; name: string }[] = [];
  public fields = { text: 'name', value: 'id' };
  public selectedValue: number = 2;

  ngOnInit() {
    this.sports = [
      { id: 1, name: 'Badminton' },
      { id: 2, name: 'Cricket' },
      { id: 3, name: 'Football' },
      { id: 4, name: 'Tennis' }
    ];
  }

  onChange(args: any) {
    this.selectedValue = args.value;
  }
}
```

### Common Patterns

#### Searchable Dropdown
```typescript
// Enable filtering in template
// <ejs-dropdownlist [allowFiltering]="true" (filtering)="onFilter($event)">
import { FilteringEventArgs } from '@syncfusion/ej2-angular-dropdowns';
import { Query } from '@syncfusion/ej2-data';

onFilter(args: FilteringEventArgs) {
  let query = new Query();
  query = args.text !== '' 
    ? query.where('name', 'contains', args.text, true) 
    : query;
  args.updateData(this.sports, query);
}
```

#### Remote Data Dropdown

> 🔒 **Security policy — remote data is a restricted pattern.**
> Binding DropDownList to a remote endpoint requires a security review (see
> [Security & Trust Boundary](#security--trust-boundary)) before use in production.
> Remote data binding details and requirements are documented in
> [references/dropdownlist-data-binding.md](references/dropdownlist-data-binding.md).
> **No remote `DataManager` example is provided here by default.**

#### Reactive Form Integration
```typescript
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { DropDownListModule } from '@syncfusion/ej2-angular-dropdowns';

// In component:
form = this.fb.group({ sport: ['Cricket', Validators.required] });
// In template:
// <form [formGroup]="form">
//   <ejs-dropdownlist formControlName="sport" [dataSource]="sports"></ejs-dropdownlist>
// </form>
```

### Key Props

| Property | Type | Description |
|---|---|---|
| `dataSource` | `any[] \| DataManager` | Data for the list |
| `fields` | `FieldSettingsModel` | Maps text, value, groupBy, disabled, iconCss |
| `value` | `string \| number \| boolean \| object` | Selected value (supports two-way binding) |
| `placeholder` | `string` | Input placeholder text |
| `allowFiltering` | `boolean` | Enable search box in popup |
| `filterType` | `'contains' \| 'startsWith' \| 'endsWith'` | Filter match strategy |
| `enableVirtualization` | `boolean` | Virtual scrolling for large lists |
| `popupHeight` / `popupWidth` | `string \| number` | Popup dimensions |
| `enabled` | `boolean` | Enable/disable entire component |
| `allowObjectBinding` | `boolean` | Bind full object as value |
| `ignoreCase` | `boolean` | Case-insensitive filtering (default: true) |
| `ignoreAccent` | `boolean` | Diacritics-insensitive filtering |
| `debounceDelay` | `number` | Delay (ms) before filter triggers |
| `itemTemplate` | `string` | Template for list items |
| `valueTemplate` | `string` | Template for selected value display |
| `noRecordsTemplate` | `string` | Empty state message |

### Common Use Cases

**Form field with validation** → See [references/dropdownlist-disabled-items-and-forms.md](references/dropdownlist-disabled-items-and-forms.md)

**Large list (1000+ items)** → Enable `[enableVirtualization]="true"` — see [references/dropdownlist-grouping-and-virtualization.md](references/dropdownlist-grouping-and-virtualization.md)

**Country/State/City cascading** → See [references/dropdownlist-how-to.md](references/dropdownlist-how-to.md#cascading-dropdownlists)

**Custom item rendering** (icons, multi-column) → See [references/dropdownlist-templates.md](references/dropdownlist-templates.md)

**Remote API data** → See [references/dropdownlist-data-binding.md](references/dropdownlist-data-binding.md#binding-remote-data)

## ListBox

A list-based selection component enabling single or multi-item selection. Supports data binding, templates, drag-and-drop reordering and transfer, sorting, grouping, and comprehensive accessibility features.

### Component Overview

The Syncfusion ListBox is a high-performance dropdown list replacement with advanced features:

| Feature | Benefit |
|---------|---------|
| **Multiple Selection Modes** | Single, multiple, or checkbox selection |
| **Data Binding** | Local arrays, complex objects, or remote services |
| **Drag & Drop** | Reorder items or transfer between lists |
| **Customization** | Icons, templates, grouping, sorting |
| **Accessibility** | WCAG 2.2, screen readers, keyboard navigation |
| **Performance** | Efficient rendering with large datasets |

### Documentation Navigation Guide

#### Getting Started
📄 **Read:** [references/listbox-getting-started.md](references/listbox-getting-started.md)
- Installation and package setup
- Angular standalone vs NgModule patterns
- Basic component initialization
- CSS imports and theme selection
- Binding local data sources
- Running and testing the application

#### Selection Modes and Interactions
📄 **Read:** [references/listbox-selection-modes.md](references/listbox-selection-modes.md)
- Single item selection
- Multiple item selection with SHIFT/CTRL
- Checkbox selection mode
- Select all functionality
- Handling change events
- Getting selected items programmatically

#### Data Binding and Field Mapping
📄 **Read:** [references/listbox-data-binding.md](references/listbox-data-binding.md)
- Binding array of strings
- Binding array of objects
- Binding complex nested objects
- Remote data with DataManager and Query
- Field mapping (text, value, groupBy, iconCss)
- Troubleshooting data binding issues

#### Drag-and-Drop Features
📄 **Read:** [references/listbox-drag-and-drop-features.md](references/listbox-drag-and-drop-features.md)
- Single ListBox drag-and-drop reordering
- Dual ListBox drag-and-drop transfer
- Drag and drop events (dragStart, drag, drop)
- Scope configuration for multiple lists
- Event handling and item manipulation
- Real-world dual ListBox patterns

#### Customization and Styling
📄 **Read:** [references/listbox-customization.md](references/listbox-customization.md)
- Icons and iconCss field mapping
- Custom item templates
- Grouping items by category
- Sorting items (ascending/descending)
- CSS styling and theming
- Theme Studio integration
- Responsive design

#### Practical Implementation Examples
📄 **Read:** [references/listbox-practical-examples.md](references/listbox-practical-examples.md)
- Filtering ListBox items
- Form submission with selected items
- Enable/disable items conditionally
- Scroller for large datasets
- Real-world use cases
- Common troubleshooting scenarios

#### How-To Guides and Common Tasks
📄 **Read:** [references/listbox-how-to-guides.md](references/listbox-how-to-guides.md)
- Add items programmatically
- Select items programmatically
- Enable or disable items dynamically
- Enable scroller for large datasets
- Filter ListBox data with input
- Submit selected items in forms

#### API Reference
📄 **Read:** [references/listbox-api.md](references/listbox-api.md)
- All component properties with types, defaults, and examples
- All public methods with parameter signatures and usage examples
- All events with event argument interfaces and handler patterns
- Interface definitions: `FieldSettingsModel`, `SelectionSettingsModel`, `ToolbarSettingsModel`
- Event arg interfaces: `ListBoxChangeEventArgs`, `DragEventArgs`, `DropEventArgs`, `BeforeItemRenderEventArgs`, `FilteringEventArgs`, `SourceDestinationModel`
- Enum definitions: `SelectionMode`, `SortOrder`, `FilterType`, `ToolBarPosition`, `CheckBoxPosition`

### Quick Start Example

#### Basic ListBox with Local Data

```typescript
import { Component, OnInit } from '@angular/core';
import { ListBoxModule } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  imports: [ListBoxModule],
  standalone: true,
  selector: 'app-listbox',
  template: `
    <ejs-listbox 
      [dataSource]="items"
      [selectionSettings]="{ mode: 'Multiple' }">
    </ejs-listbox>
  `
})
export class ListBoxComponent implements OnInit {
  public items: { [key: string]: Object }[] = [];

  ngOnInit(): void {
    this.items = [
      { text: 'Option 1', id: '1' },
      { text: 'Option 2', id: '2' },
      { text: 'Option 3', id: '3' }
    ];
  }
}
```

#### With Styles

> ⚠️ **Security note:** These imports are resolved from `node_modules` at build time.
> Ensure the installed Syncfusion packages match your pinned versions in `package-lock.json`
> or `yarn.lock` before building. Do not source these files from a CDN without
> Subresource Integrity (SRI) hashes.

```css
/* In your global styles.css */
@import '@syncfusion/ej2-base/styles/material3.css';
@import '@syncfusion/ej2-dropdowns/styles/material3.css';
@import '@syncfusion/ej2-inputs/styles/material3.css';
@import '@syncfusion/ej2-lists/styles/material3.css';
```

### Common Patterns

#### Selection with Change Event

```typescript
import { ListBoxChangeEventArgs } from '@syncfusion/ej2-dropdowns';

selectedValues: string[] = [];

onSelectionChange(args: ListBoxChangeEventArgs): void {
  this.selectedValues = args.value as string[];
}
```

Template:
```html
<ejs-listbox
  [dataSource]="items"
  (change)="onSelectionChange($event)">
</ejs-listbox>
```

#### Dual ListBox for Transfer

```typescript
sourceItems = [
  { text: 'Available Item 1', id: '1' },
  { text: 'Available Item 2', id: '2' }
];

selectedItems = [];
```

Template:
```html
<div style="display: flex; gap: 20px;">
  <div>
    <h4>Available Items</h4>
    <ejs-listbox
      [dataSource]="sourceItems"
      allowDragAndDrop="true"
      scope="transfer-list">
    </ejs-listbox>
  </div>
  
  <div>
    <h4>Selected Items</h4>
    <ejs-listbox
      [dataSource]="selectedItems"
      allowDragAndDrop="true"
      scope="transfer-list">
    </ejs-listbox>
  </div>
</div>
```

#### Filtered ListBox

```typescript
allItems = [
  { text: 'Apple', category: 'Fruit' },
  { text: 'Carrot', category: 'Vegetable' },
  { text: 'Banana', category: 'Fruit' }
];

get filteredItems() {
  return this.allItems.filter(item => 
    item.text.toLowerCase().includes(this.searchTerm.toLowerCase())
  );
}
```

### Key Props

#### Selection Configuration
- **`selectionSettings`**: `{ mode: 'Single' | 'Multiple', showCheckbox: boolean, showSelectAll: boolean, checkboxPosition: 'Left' | 'Right' }`  > **Note:** When using `showCheckbox: true`, you must inject `CheckBoxSelection`:
  > ```typescript
  > import { ListBoxComponent, CheckBoxSelection, ListBoxModule } from '@syncfusion/ej2-angular-dropdowns';
  > ListBoxComponent.Inject(CheckBoxSelection);
  > @Component({ imports: [ListBoxModule] })
  > ```- **`maximumSelectionLength`**: Limit how many items can be selected
- **`value`**: Get or set selected values (`string[] | number[] | boolean[]`)

#### Data and Display
- **`dataSource`**: Array or DataManager with items
- **`fields`**: `{ text, value, groupBy, iconCss, disabled, htmlAttributes }`
- **`itemTemplate`**: Template for rendering each list item
- **`noRecordsTemplate`**: Template shown when no items match

#### Interactions
- **`allowDragAndDrop`**: Enable drag-and-drop reordering/transfer
- **`scope`**: Identify related ListBoxes for drag-drop transfer
- **`allowFiltering`**: Show built-in filter search bar
- **`filterBarPlaceholder`**: Placeholder text for the filter bar
- **`filterType`**: `'StartsWith' | 'EndsWith' | 'Contains'`
- **`toolbarSettings`**: Configure toolbar buttons for dual-ListBox transfer

#### Appearance
- **`height`**: Height of the ListBox
- **`sortOrder`**: `'None' | 'Ascending' | 'Descending'`
- **`enabled`**: Enable/disable component
- **`enableRtl`**: Right-to-left rendering
- **`cssClass`**: Additional CSS class

### Next Steps

1. **Get Started**: Read [references/listbox-getting-started.md](references/listbox-getting-started.md) for setup instructions
2. **Choose Selection Mode**: Review [references/listbox-selection-modes.md](references/listbox-selection-modes.md) for your use case
3. **Bind Data**: See [references/listbox-data-binding.md](references/listbox-data-binding.md) for data source options
4. **Add Interactions**: Explore [references/listbox-drag-and-drop-features.md](references/listbox-drag-and-drop-features.md) for advanced features
5. **Customize**: Check [references/listbox-customization.md](references/listbox-customization.md) for styling options
6. **See Examples**: Review [references/listbox-practical-examples.md](references/listbox-practical-examples.md) for real-world implementations
7. **API Reference**: Consult [references/listbox-api.md](references/listbox-api.md) for the complete properties, methods, events, and interface definitions

### Common Use Cases

- **Selection Forms**: Multi-select dropdown replacement
- **Transfer Lists**: Move items between lists (dual ListBox)
- **Categories**: Group-based item organization
- **Filtering**: Filter large datasets
- **Data Display**: Show structured list data
- **Accessibility**: Compliant selection interfaces

## Mention

An autocomplete suggestion popup triggered by a typed character (default `@`) inside a target element. Supports user tagging, custom trigger characters, rich text integration, remote data, templates, and full accessibility.

### Component Overview & Architecture

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

### Documentation Navigation Guide

#### 📄 Getting Started
**Read:** [references/mention-getting-started.md](references/mention-getting-started.md)
- Install `@syncfusion/ej2-angular-dropdowns` package
- Set up Angular 21+ project with standalone components
- Import `MentionModule` and required CSS themes
- Create a target `contenteditable` div
- Bind `target` and basic `dataSource`
- Display/customize the mention character with `showMentionChar` and `mentionChar`

#### 📄 Data Binding
**Read:** [references/mention-data-binding.md](references/mention-data-binding.md)
- Bind to local arrays of strings, JSON objects, and complex objects
- Map `text`, `value`, `groupBy`, and `iconCss` via `fields` property
- Remote data binding (restricted — requires security review; see [Security & Trust Boundary](#security--trust-boundary))
- Use the `query` property to scope remote requests

#### 📄 Filtering
**Read:** [references/mention-filtering.md](references/mention-filtering.md)
- Control filter strategy with `filterType` (`Contains`, `StartsWith`, `EndsWith`)
- Set minimum input length before triggering with `minLength`
- Allow spaces in the middle of a mention search with `allowSpaces`
- Limit visible suggestion count with `suggestionCount`
- Tune debounce delay for remote sources with `debounceDelay`

#### 📄 Templates
**Read:** [references/mention-templates.md](references/mention-templates.md)
- Customize suggestion list item layout with `itemTemplate`
- Customize the inserted text representation with `displayTemplate`
- Handle empty results with `noRecordsTemplate`
- Show a loading indicator while fetching remote data with `spinnerTemplate`
- Customize grouped items with `groupTemplate`

#### 📄 Customization
**Read:** [references/mention-customization.md](references/mention-customization.md)
- Show/hide the trigger character alongside selected text with `showMentionChar`
- Append a suffix (space, newline) after selection with `suffixText`
- Resize the popup with `popupHeight` and `popupWidth`
- Change the trigger character with `mentionChar`
- Control leading space requirement with `requireLeadingSpace`
- Apply custom CSS classes with `cssClass`
- Highlight searched characters with `highlight`
- Configure `ignoreCase` and `ignoreAccent` for search behavior

#### 📄 Sorting & Disabled Items
**Read:** [references/mention-sorting-and-disabled-items.md](references/mention-sorting-and-disabled-items.md)
- Sort suggestions with `sortOrder` (`None`, `Ascending`, `Descending`)
- Mark items as non-selectable via `fields.disabled`
- Dynamically disable items at runtime using the `disableItem` method

#### 📄 Accessibility & Localization
**Read:** [references/mention-accessibility-and-localization.md](references/mention-accessibility-and-localization.md)
- WCAG 2.2, Section 508, and ADA compliance
- Full keyboard shortcuts (Arrow Down/Up, Enter, Tab, Escape)
- ARIA attributes: `aria-selected`, `aria-activedescendent`, `aria-owns`
- Localize `noRecordsTemplate` with `L10n.load()`
- RTL support with `enableRtl`

#### 📄 API Reference
**Read:** [references/mention-api.md](references/mention-api.md)
- Complete properties reference with types, defaults, and descriptions
- All methods: `addItem`, `disableItem`, `getDataByValue`, `getItems`, `hidePopup`, `showPopup`, `search`, `destroy`
- All events: `dataBound`, `actionFailureTemplate`

---

### Quick Start Example

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
ng add @syncfusion/ej2-angular-dropdowns@<version>
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

### Common Patterns

#### Pattern 1: Object Data with Field Mapping

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

#### Pattern 2: Custom Trigger Character with showMentionChar

```html
<ejs-mention
  [dataSource]="userData"
  [target]="mentionTarget"
  [mentionChar]="'#'"
  [showMentionChar]="true">
</ejs-mention>
```

#### Pattern 3: Remote Data with Popup Width

> 🔒 **Security policy — remote data is a restricted pattern.**
> Binding Mention to a remote endpoint requires a security review (see
> [Security & Trust Boundary](#security--trust-boundary)) before use in production.
> Remote data binding details and requirements are documented in
> [references/mention-data-binding.md](references/mention-data-binding.md).
> **No remote `DataManager` example is provided here by default.**

#### Pattern 4: Allow Spaces in Mention Search

```html
<ejs-mention
  [dataSource]="userData"
  [fields]="fields"
  [allowSpaces]="true"
  [target]="mentionTarget">
</ejs-mention>
```

---

### Key Properties Quick Reference

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

### Workflow Decision Tree

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

## MultiSelect

A multi-value selection dropdown (`ejs-multiselect`) supporting four visual modes (Default/Box/Delimiter/CheckBox), rich filtering, templates, grouping, remote data, virtualization, and full Angular form integration.

### Component Overview

| Mode | Behavior | Use When |
|------|----------|----------|
| `Default` | Selected items shown as chips in input | Standard multi-select |
| `Box` | Same as Default, explicit box display | Visual clarity needed |
| `Delimiter` | Selected items as comma-separated text | Space-constrained layouts |
| `CheckBox` | Popup shows checkboxes per item | Bulk selection workflows |

### Documentation Navigation Guide

#### Getting Started
📄 **Read:** [references/multiselect-getting-started.md](references/multiselect-getting-started.md)
- Installation and package setup (`ng add`)
- CSS imports and theme configuration
- Basic `<ejs-multiselect>` in standalone Angular component
- Popup height/width configuration
- Angular version notes (standalone default in Angular 19+)

#### Data Binding & Value Binding
📄 **Read:** [references/multiselect-data-binding.md](references/multiselect-data-binding.md)
- Local arrays (strings, numbers, objects)
- `fields` mapping: `text`, `value`, `groupBy`, `iconCss`, `disabled`
- Remote data with DataManager (OData, Web API)
- Pre-selecting values programmatically
- Object binding with `allowObjectBinding`

#### Selection Modes, Chips & Item Control
📄 **Read:** [references/multiselect-selection-modes.md](references/multiselect-selection-modes.md)
- `mode` property: Default / Box / Delimiter / CheckBox
- CheckBox mode: `CheckBoxSelection`, `showSelectAll`, `maximumSelectionLength`
- Chip customization via `tagging` event
- Custom values with `allowCustomValue`
- Disabling specific items: `fields.disabled`, `disableItem()`
- `addTagOnBlur` and `changeOnBlur` behaviors

#### Filtering
📄 **Read:** [references/multiselect-filtering.md](references/multiselect-filtering.md)
- Enabling `allowFiltering` + `filtering` event + `updateData()`
- `filterType`: `startsWith`, `contains`, `endsWith`
- Minimum character threshold before query fires
- Remote filtering with DataManager
- Case-insensitive matching

#### Templates
📄 **Read:** [references/multiselect-templates.md](references/multiselect-templates.md)
- `itemTemplate` — custom list item rendering with `ng-template`
- `valueTemplate` — customize chip/selected value display
- `groupTemplate` — custom group header content
- `headerTemplate` / `footerTemplate` — popup top/bottom
- `noRecordsTemplate` / `actionFailureTemplate`

#### Grouping & Cascading
📄 **Read:** [references/multiselect-grouping-and-items.md](references/multiselect-grouping-and-items.md)
- `fields.groupBy` — organize items into categories
- Fixed vs inline group headers
- `enableGroupCheckBox` for group-level Select All
- Cascading MultiSelect: parent `change` event → filter child data
- Country → State → City cascade pattern

#### Form Integration
📄 **Read:** [references/multiselect-form-support.md](references/multiselect-form-support.md)
- Template-driven forms: `FormsModule`, `ngModel`, two-way binding
- Reactive forms: `ReactiveFormsModule`, `FormGroup`, `FormControl`
- `formControlName` usage and validation
- Required field and custom validator patterns

#### Advanced Features
📄 **Read:** [references/multiselect-advanced-features.md](references/multiselect-advanced-features.md)
- Virtualization for large datasets (`enableVirtualization`)
- Popup resize (`allowResize`, resize events)
- Icons in list items (`iconCss` field)
- Localization (`L10n.load()`, locale key overrides)
- Accessibility: WAI-ARIA, keyboard navigation, WCAG 2.2
- RTL support

#### API Reference
📄 **Read:** [references/multiselect-api.md](references/multiselect-api.md)
- Complete list of all properties with types and defaults
- All public methods with signatures, parameters, and return types
- All events with argument types and usage examples
- Module injection notes (`CheckBoxSelectionService`)

### Quick Start

> ⚠️ **Security note:** Pin the package to a specific version to prevent unintended upgrades
> to potentially compromised releases. Verify the installed version against your lockfile
> (`package-lock.json` / `yarn.lock`) after installation.

```bash
ng add @syncfusion/ej2-angular-dropdowns@<version>
```

```typescript
// app.component.ts — Standalone Angular 19+
import { Component } from '@angular/core';
import { MultiSelectModule } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  standalone: true,
  imports: [MultiSelectModule],
  selector: 'app-root',
  template: `
    <ejs-multiselect
      [dataSource]="skills"
      [fields]="fields"
      placeholder="Select skills"
      [(value)]="selectedSkills"
      (change)="onChange($event)">
    </ejs-multiselect>
  `
})
export class AppComponent {
  public skills = [
    { id: 1, name: 'Angular' },
    { id: 2, name: 'React' },
    { id: 3, name: 'TypeScript' },
    { id: 4, name: 'Node.js' },
  ];
  public fields = { text: 'name', value: 'id' };
  public selectedSkills: number[] = [1, 3]; // pre-select Angular & TypeScript

  onChange(args: any): void {
    this.selectedSkills = args.value;
  }
}
```

> ⚠️ **Security note:** These imports are resolved from `node_modules` at build time.
> Ensure the installed Syncfusion packages match your pinned versions in `package-lock.json`
> or `yarn.lock` before building. Do not source these files from a CDN without
> Subresource Integrity (SRI) hashes.

```css
/* styles.css */
@import '@syncfusion/ej2-base/styles/material3.css';
@import '@syncfusion/ej2-buttons/styles/material3.css';
@import '@syncfusion/ej2-inputs/styles/material3.css';
@import '@syncfusion/ej2-lists/styles/material3.css';
@import '@syncfusion/ej2-popups/styles/material3.css';
@import '@syncfusion/ej2-dropdowns/styles/material3.css';
@import '@syncfusion/ej2-angular-dropdowns/styles/material3.css';
```

### Common Patterns

#### Checkbox Mode with Select All
```typescript
import { MultiSelectModule, CheckBoxSelectionService } from '@syncfusion/ej2-angular-dropdowns';

@Component({
  standalone: true,
  imports: [MultiSelectModule],
  providers: [CheckBoxSelectionService],
  template: `
    <ejs-multiselect
      [dataSource]="items"
      mode="CheckBox"
      [showSelectAll]="true"
      selectAllText="Select All"
      unSelectAllText="Unselect All"
      [maximumSelectionLength]="5">
    </ejs-multiselect>
  `
})
```

#### Filtering with Remote Data

> 🔒 **Security policy — remote data is a restricted pattern.**
> Binding MultiSelect to a remote endpoint requires a security review (see
> [Security & Trust Boundary](#security--trust-boundary)) before use in production.
> Remote filtering details and requirements are documented in
> [references/multiselect-filtering.md](references/multiselect-filtering.md).
> **No remote `DataManager` example is provided here by default.**

#### Reactive Form Integration
```typescript
import { ReactiveFormsModule, FormControl } from '@angular/forms';

// In component:
public skillsControl = new FormControl([1, 3]); // pre-selected IDs

// In template:
// <ejs-multiselect [formControl]="skillsControl" [dataSource]="skills" [fields]="fields">
// </ejs-multiselect>
```

### Key Props

| Property | Type | Purpose |
|---|---|---|
| `dataSource` | `any[] \| DataManager` | Items to display |
| `fields` | `FieldSettingsModel` | Maps `text`, `value`, `groupBy`, `disabled`, `iconCss` |
| `value` | `any[]` | Currently selected values (use `[(value)]` for two-way) |
| `mode` | `string` | `Default`, `Box`, `Delimiter`, `CheckBox` |
| `allowFiltering` | `boolean` | Enables search within the dropdown |
| `filterType` | `string` | `startsWith`, `contains`, `endsWith` |
| `showSelectAll` | `boolean` | Shows Select All in CheckBox mode |
| `maximumSelectionLength` | `number` | Caps the number of selectable items |
| `allowCustomValue` | `boolean` | Lets users add values not in the list |
| `enableVirtualization` | `boolean` | Optimizes rendering for large lists |
| `popupHeight` / `popupWidth` | `string` | Constrains popup dimensions |
| `allowResize` | `boolean` | Lets users drag-resize the popup |
| `placeholder` | `string` | Input hint text |

## MultiColumn ComboBox

The MultiColumn ComboBox (`ejs-multicolumncombobox`) is a dropdown component that displays data in a multi-column grid-like popup. It supports column configuration, data binding (local/remote), filtering, sorting, grouping, templates, virtualization, events, and accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/multicolumn-combobox-getting-started.md)
- Installation and package setup (`ng add @syncfusion/ej2-angular-multicolumn-combobox@<version>`)
  > ⚠️ **Security note:** Pin the package to a specific version to prevent unintended upgrades
  > to potentially compromised releases. Verify the installed version against your lockfile
  > (`package-lock.json` / `yarn.lock`) after installation.
- CSS/theme imports for Material and other themes
- Basic standalone component usage with `<ejs-multicolumncombobox>`
- Binding `dataSource` and `fields` properties
- Configuring `<e-columns>` and `<e-column>` child elements
- Popup height and width configuration (`popupHeight`, `popupWidth`)

#### Columns Configuration
📄 **Read:** [references/columns.md](references/multicolumn-combobox-columns.md)
- Defining columns with `field`, `header`, `width`
- Setting text alignment with `textAlign`
- Using column `template` with `ng-template`
- Displaying boolean values as checkboxes with `displayAsCheckBox`
- Applying custom CSS attributes via `customAttributes`
- Custom column headers with `headerTemplate`
- Formatting values with `format`

#### Data Binding
📄 **Read:** [references/data-binding.md](references/multicolumn-combobox-data-binding.md)
- Binding local object arrays via `dataSource`
- Remote data binding (restricted — requires security review; see [Security & Trust Boundary](#security--trust-boundary))
- Mapping `fields`: `text`, `value`, and `groupBy`
- Using the `query` property to filter/limit remote results

#### Items and Display Configuration
📄 **Read:** [references/items.md](references/multicolumn-combobox-items.md)
- Setting pre-selected text with `text` property
- Setting pre-selected value with `value` property
- Setting selected item by index with `index` property
- Placeholder text with `placeholder`
- Float label behavior with `floatLabelType` (Never/Always/Auto)
- Adding HTML attributes via `htmlAttributes`
- Setting component width with `width`
- Configuring popup dimensions (`popupWidth`, `popupHeight`)
- Show/hide clear button with `showClearButton`
- Applying custom CSS class with `cssClass`
- Disabled state with `disabled`
- Read-only mode with `readonly`
- Configuring grid settings (`gridSettings`: `gridLines`, `rowHeight`, `enableAltRow`)

#### Filtering
📄 **Read:** [references/filtering.md](references/multicolumn-combobox-filtering.md)
- Enable/disable filtering with `allowFiltering`
- Changing filter type with `filterType` (StartsWith/EndsWith/Contains)

#### Sorting
📄 **Read:** [references/sorting.md](references/multicolumn-combobox-sorting.md)
- Enable/disable sorting with `allowSorting`
- Setting initial sort order with `sortOrder` (None/Ascending/Descending)
- Sorting single vs. multiple columns with `sortType`

#### Grouping
📄 **Read:** [references/grouping.md](references/multicolumn-combobox-grouping.md)
- Grouping items using the `groupBy` field in `fields` property

#### Templates
📄 **Read:** [references/templates.md](references/multicolumn-combobox-templates.md)
- Customizing row items with `itemTemplate`
- Custom column headers with `headerTemplate`
- Group headers with `groupTemplate`
- Footer content with `footerTemplate`
- No-records placeholder with `noRecordsTemplate`
- Remote failure display with `actionFailureTemplate`

#### Events
📄 **Read:** [references/events.md](references/multicolumn-combobox-events.md)
- `actionBegin`, `actionComplete`, `actionFailure` — data lifecycle events
- `select` — item selection event
- `change` — value change event
- `filtering` — text input filtering event
- `open` / `close` — popup state events
- `created` — component rendered event

#### Virtualization
📄 **Read:** [references/virtualization.md](references/multicolumn-combobox-virtualization.md)
- Enabling virtual scrolling with `enableVirtualization`
- Virtual scrolling with local and remote large datasets

#### Accessibility and Localization
📄 **Read:** [references/accessibility.md](references/multicolumn-combobox-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA attributes used by the component
- Keyboard navigation shortcuts
- RTL support with `enableRtl`
- Localization of `noRecordsTemplate` text using `L10n`

#### API Reference
📄 **Read:** [references/api.md](references/multicolumn-combobox-api.md)
- Complete list of properties, methods, and events
- `ColumnModel` interface properties
- `GridSettingsModel` interface
- Methods: `showPopup`, `hidePopup`, `focusIn`, `focusOut`, `getDataByValue`, `getItems`, `addItems`

### Quick Start

```typescript
import { Component } from '@angular/core';
import { MultiColumnComboBoxModule } from '@syncfusion/ej2-angular-multicolumn-combobox';

@Component({
  imports: [MultiColumnComboBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-multicolumncombobox
      id='multicolumn'
      [dataSource]='empData'
      [fields]='fields'
      [placeholder]='waterMark'>
      <e-columns>
        <e-column field='EmpID' header='Employee ID' width='100'></e-column>
        <e-column field='Name' header='Name' width='90'></e-column>
        <e-column field='Designation' header='Designation' width='100'></e-column>
        <e-column field='Country' header='Country' width='90'></e-column>
      </e-columns>
    </ejs-multicolumncombobox>`
})
export class AppComponent {
  public empData: Object[] = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' }
  ];
  public fields: Object = { text: 'Name', value: 'EmpID' };
  public waterMark: string = 'Select an employee';
}
```

### Common Patterns

#### Remote data with DataManager
When data comes from an API, use `DataManager` → Read `references/data-binding.md`

#### Large datasets (150+ rows)
Enable `enableVirtualization` to avoid performance issues → Read `references/virtualization.md`

#### Rich row display
Use column `template` with `ng-template` for images, badges, or custom HTML → Read `references/columns.md`

#### Grouped dropdown
Set `groupBy` in `fields` to categorize items → Read `references/grouping.md`

#### Programmatic open/close
Use `showPopup()` / `hidePopup()` methods → Read `references/api.md`
