---
name: syncfusion-angular-query-builder
description: Implement the Syncfusion Angular Query Builder component for visual query construction, dynamic filtering, and rule management. Use this when building visual filter UIs, creating query conditions programmatically, importing/exporting SQL or MongoDB queries, or customizing query builder templates. This skill covers data binding, column configuration with operators, rule groups, theming, and Angular forms integration for the QueryBuilder (ejs-querybuilder) component.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Forms"
---

# Implementing Syncfusion Angular Query Builder

The Syncfusion Angular Query Builder (`ejs-querybuilder`) is a UI component for visually constructing complex filter queries. Users define conditions (field + operator + value) and combine them into groups with AND/OR logic. The resulting rules can be exported to JSON, SQL, or MongoDB formats for use in filtering or API queries.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing `@syncfusion/ej2-angular-querybuilder`
- Setting up CSS/theme imports (Material3)
- Creating a basic Query Builder with columns
- Rendering with an initial rule
- Running the Angular application

### Columns Configuration
📄 **Read:** [references/columns.md](references/columns.md)
- Defining columns with `field`, `label`, `type`
- Auto-generating columns from dataSource
- Configuring operators per column (full operators table)
- Setting step values for number fields
- Formatting date and number values
- Enabling validation (`allowValidation`, `isRequired`, `min`/`max`)

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding (JS arrays, `JsonAdaptor`)
- Remote data with `DataManager` (OData, OData v4, WebApiAdaptor)
- Using `getPredicate()` with DataManager for filtering
- Complex/nested data binding with sub-columns

### Filtering & Rules Management
📄 **Read:** [references/filtering-and-rules.md](references/filtering-and-rules.md)
- Adding/deleting conditions with `addRules` / `deleteRules`
- Adding/deleting groups with `addGroups` / `deleteGroups`
- Cloning rules/groups (`cloneRule`, `cloneGroup`)
- Locking rules/groups (`lockRule`, `lockGroup`)
- Separate connectors between rules (`enableSeparateConnector`)
- Restricting group nesting depth (`maxGroupCount`)
- Drag-and-drop rule reordering (`allowDragAndDrop`)
- Controlling button visibility (`showButtons`)

### Import & Export
📄 **Read:** [references/import-export.md](references/import-export.md)
- Importing from JSON (initial `rule` property + `setRules`)
- Importing from SQL (inline, parameterized, named parameterized)
- Importing from MongoDB (`setMongoQuery`)
- Exporting to JSON (`getRules`)
- Exporting to SQL (inline, parameterized, named parameterized)
- Exporting to MongoDB (`getMongoQuery`)

### Templates & Model Binding
📄 **Read:** [references/templates.md](references/templates.md)
- Custom header template with dropdown, split-button, NOT condition
- Column template with `create` / `write` / `destroy` pattern
- Using `NgTemplate` for column value inputs
- Rule template (`ruleTemplate` + `actionBegin` event)
- Model binding for field, operator, value inputs (`fieldModel`, `operatorModel`, `valueModel`)

### Style, Appearance & Layout
📄 **Read:** [references/style-and-appearance.md](references/style-and-appearance.md)
- CSS class customization table
- Theme Studio integration
- Display modes: horizontal (default) vs. vertical (`displayMode`)
- Summary view (`summaryView`)
- RTL support (`enableRtl`)
- State persistence (`enablePersistence`)

### Accessibility & Localization
📄 **Read:** [references/accessibility-and-localization.md](references/accessibility-and-localization.md)
- WCAG 2.2, Section 508, WAI-ARIA compliance
- Keyboard navigation shortcuts
- Localization setup and full locale key reference
- Sort columns display (`sortDirection`)

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- Complete Properties reference (40+ properties)
- Complete Methods reference (30+ methods)
- Complete Events reference (7 events)
- Type definitions and interfaces
- Official Syncfusion documentation links

---

## Quick Start Example

```typescript
import { QueryBuilderModule } from '@syncfusion/ej2-angular-querybuilder';
import { Component } from '@angular/core';

@Component({
  imports: [QueryBuilderModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-querybuilder width="70%" [rule]="importRules">
      <e-columns>
        <e-column field="EmployeeID" label="Employee ID" type="number"></e-column>
        <e-column field="FirstName" label="First Name" type="string"></e-column>
        <e-column field="Title" label="Title" type="string"></e-column>
        <e-column field="HireDate" label="Hire Date" type="date" format="dd/MM/yyyy"></e-column>
        <e-column field="Country" label="Country" type="string"></e-column>
      </e-columns>
    </ejs-querybuilder>
  `
})
export class App {
  public importRules = {
    condition: 'and',
    rules: [
      { field: 'EmployeeID', label: 'Employee ID', type: 'number', operator: 'equal', value: 1 },
      { field: 'Country', label: 'Country', type: 'string', operator: 'equal', value: 'USA' }
    ]
  };
}
```

Install with:
```bash
ng add @syncfusion/ej2-angular-querybuilder
```

---

## Common Patterns

### Pattern 1: Export rules to SQL for backend use
```typescript
// In your component
import { QueryBuilderComponent } from '@syncfusion/ej2-angular-querybuilder';
import { ViewChild } from '@angular/core';

@ViewChild('querybuilder') qb!: QueryBuilderComponent;

getSqlQuery(): string {
  return this.qb.getSqlFromRules(this.qb.getRules());
}
```

### Pattern 2: Load rules at runtime
```typescript
// After component renders, update rules dynamically
this.qb.setRules({
  condition: 'or',
  rules: [
    { field: 'City', operator: 'equal', value: 'London' },
    { field: 'Country', operator: 'equal', value: 'UK' }
  ]
});
```

### Pattern 3: Programmatically add a condition
```typescript
// Add a rule to the root group
this.qb.addRules([{ field: 'Title', operator: 'contains', value: 'Manager' }], 'querybuilder_group0');
```

### Pattern 4: Enable drag-and-drop + clone + lock
```html
<ejs-querybuilder [allowDragAndDrop]="true" [showButtons]="showButtons">
</ejs-querybuilder>
```
```typescript
public showButtons = { ruleDelete: true, groupInsert: true, groupDelete: true, ruleInsert: true, cloneRule: true, cloneGroup: true, lockRule: true, lockGroup: true };
```

---

## Key Properties

| Property | Type | Purpose |
|---|---|---|
| `[rule]` | RuleModel | Initial query rules to render |
| `[columns]` | ColumnsModel[] | Column definitions (field, label, type, operators) |
| `[dataSource]` | object[] / DataManager | Data for auto-column generation and predicate |
| `[allowDragAndDrop]` | boolean | Enable drag-and-drop rule/group reordering |
| `[enableSeparateConnector]` | boolean | Different AND/OR per rule instead of per group |
| `[enableNotCondition]` | boolean | Show NOT condition toggle on groups |
| `[summaryView]` | boolean | Show human-readable summary of current query |
| `[enablePersistence]` | boolean | Persist rules to localStorage across refreshes |
| `[enableRtl]` | boolean | Right-to-left layout for RTL languages |
| `[displayMode]` | string | `'Horizontal'` (default) or `'Vertical'` layout |
| `[maxGroupCount]` | number | Max number of nested groups (default: 5) |
| `[sortDirection]` | string | Sort field dropdown: `'Ascending'` or `'Descending'` |
| `[allowValidation]` | boolean | Enable field/operator/value validation |
| `[showButtons]` | ShowButtons | Control visibility of action buttons |

## Key Methods

| Method | Purpose |
|---|---|
| `getRules()` | Get current rules as JSON RuleModel |
| `setRules(rules)` | Set rules programmatically at runtime |
| `getSqlFromRules(rules)` | Export rules to inline SQL string |
| `setRulesFromSql(sql)` | Import inline SQL string into Query Builder |
| `getMongoQuery(rules)` | Export rules to MongoDB query string |
| `setMongoQuery(query)` | Import MongoDB query string |
| `addRules(rules, groupID)` | Add rules to a specific group |
| `deleteRules(ruleIDs)` | Remove rules by ID |
| `addGroups(groups, groupID)` | Add sub-groups to a group |
| `deleteGroups(groupIDs)` | Remove groups by ID |
| `cloneRule(ruleID)` | Clone a rule adjacent to the original |
| `cloneGroup(groupID)` | Clone a group with all its rules |
| `lockRule(ruleID)` | Make a rule read-only |
| `lockGroup(groupID)` | Make a group and its contents read-only |
| `validateFields()` | Trigger validation on all fields |

## Common Use Cases

- **Admin dashboards:** Let users build custom data filters without writing SQL
- **Report builders:** Generate WHERE clause conditions for dynamic reports
- **Search interfaces:** Visual query construction for complex search forms
- **Data export tools:** Build MongoDB/SQL filters from a UI, pass to API
- **Saved searches:** Export rules to JSON, store, and reload with `setRules`
