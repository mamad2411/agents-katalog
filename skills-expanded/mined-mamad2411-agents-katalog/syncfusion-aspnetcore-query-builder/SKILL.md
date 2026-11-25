---
name: syncfusion-aspnetcore-query-builder
description: Complete guide to implementing the Syncfusion QueryBuilder component in ASP.NET Core applications. Use this when working with visual query/filter builders, rule-based filtering UI, SQL/JSON/MongoDB query generation, drag-and-drop rule reordering, or import/export of filter conditions using Syncfusion EJ2 TagHelpers.
metadata:
  author: "Syncfusion Inc"
  category: "Forms"
  version: "33.1.44"
---

# Implementing QueryBuilder in ASP.NET Core

The Syncfusion QueryBuilder is a UI component for creating and editing filter conditions visually. Users can define rules and groups, combine them with AND/OR connectors, and export them as JSON, SQL, or MongoDB queries — all using ASP.NET Core TagHelper syntax.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/querybuilder-getting-started.md)
- NuGet package installation and TagHelper setup
- CDN stylesheet and script references
- Basic QueryBuilder with columns
- Render with initial Rule (JSON)
- EmployeeView model class example

### Column Configuration
📄 **Read:** [references/columns.md](references/querybuilder-columns.md)
- Auto-generating columns from DataSource
- Labels, field mapping, data types
- Operators table (all supported types)
- Number step and date/number format
- Validation (isRequired, min, max)
- Column-level custom input templates

### Data Binding
📄 **Read:** [references/data-binding.md](references/querybuilder-data-binding.md)
- Local data binding (JSON array, DataManager)
- Remote data (OData, ODataV4, WebAPI, UrlAdaptor)
- Using getPredicate to filter data
- Grid integration via ruleChange event

### Import & Export
📄 **Read:** [references/import-export.md](references/querybuilder-import-export.md)
- Import from JSON (initial Rule / setRules)
- Import from SQL (Inline, Parameter, Named Parameter)
- Import from MongoDB (setMongoQuery)
- Export to JSON (getRules)
- Export to SQL variants and MongoDB

### Filtering & Rule Management
📄 **Read:** [references/filtering-and-rules.md](references/querybuilder-filtering-and-rules.md)
- ShowButtons configuration (ruleDelete, groupInsert, groupDelete, clone, lock)
- addRules / deleteRules / addGroups / deleteGroups methods
- cloneGroup / cloneRule methods
- lockGroup / lockRule methods
- EnableSeparateConnector between rules
- EnableNotCondition for NOT groups

### Templates & Appearance
📄 **Read:** [references/templates-and-appearance.md](references/querybuilder-templates-and-appearance.md)
- Header template customization
- Display mode (Horizontal / Vertical)
- Summary view (collapsed read-only display)
- Model binding (fieldModel, operatorModel, valueModel)
- CSS classes for styling customization

### Configuration & How-To
📄 **Read:** [references/configuration-and-how-to.md](references/querybuilder-configuration-and-how-to.md)
- Drag and drop (AllowDragAndDrop, events)
- MaxGroupCount to restrict nested groups
- SortDirection for column field ordering
- EnablePersistence (state saved in localStorage)
- EnableRtl for right-to-left languages
- ReadOnly mode, Width/Height, CssClass
- AutoSelectField, AutoSelectOperator, MatchCase

### Localization
📄 **Read:** [references/localization.md](references/querybuilder-localization.md)
- Setting the Locale property
- Full locale key reference table
- Example: Arabic / RTL localization

### API Reference
📄 **Read:** [references/api.md](references/querybuilder-api.md)
- Complete properties with types and defaults
- All events with descriptions
- QueryBuilderColumn sub-properties
- QueryBuilderShowButtons sub-properties
- TagHelper attribute naming conventions

## Quick Start Example

```cshtml
@* _ViewImports.cshtml must have: @addTagHelper *, Syncfusion.EJ2 *@

<ejs-querybuilder id="querybuilder" width="70%">
    <e-querybuilder-columns>
        <e-querybuilder-column field="EmployeeID" label="Employee ID" type="number"></e-querybuilder-column>
        <e-querybuilder-column field="FirstName" label="First Name" type="string"></e-querybuilder-column>
        <e-querybuilder-column field="Title" label="Title" type="string"></e-querybuilder-column>
        <e-querybuilder-column field="HireDate" label="Hire Date" type="date" format="dd/MM/yyyy"></e-querybuilder-column>
        <e-querybuilder-column field="Country" label="Country" type="string"></e-querybuilder-column>
    </e-querybuilder-columns>
</ejs-querybuilder>
```

## Common Patterns

### Render with Initial Rule
```cshtml
@using Syncfusion.EJ2.QueryBuilder
@{
    QueryBuilderRule rule = new QueryBuilderRule()
    {
        Condition = "and",
        Rules = new List<QueryBuilderRule>()
        {
            new QueryBuilderRule { Label = "First Name", Field = "FirstName", Type = "string", Operator = "startswith", Value = "Nancy" },
            new QueryBuilderRule { Label = "Country", Field = "Country", Type = "string", Operator = "equal", Value = "USA" }
        }
    };
    var dataSource = EmployeeView.GetAllRecords();
}
<ejs-querybuilder id="querybuilder" width="70%" rule="rule" dataSource="dataSource">
    <e-querybuilder-columns>
        <e-querybuilder-column field="EmployeeID" label="Employee ID" type="number"></e-querybuilder-column>
        <e-querybuilder-column field="FirstName" label="First Name" type="string"></e-querybuilder-column>
        <e-querybuilder-column field="Country" label="Country" type="string"></e-querybuilder-column>
    </e-querybuilder-columns>
</ejs-querybuilder>
```

### Export Rules to SQL
```javascript
var queryBuilder = ej.base.getInstance(document.getElementById("querybuilder"), ejs.querybuilder.QueryBuilder);

// Get JSON rules
var jsonRules = queryBuilder.getRules();

// Get Inline SQL
var sql = queryBuilder.getSqlFromRules(jsonRules);

// Get Parameterized SQL
var paramSql = queryBuilder.getParameterizedSql(jsonRules);
```

### Grid Integration with QueryBuilder
```javascript
// In ruleChange event handler:
function ruleChanged(args) {
    var qryBldrObj = ej.base.getInstance(document.getElementById("querybuilder"), ejs.querybuilder.QueryBuilder);
    var gridObj = ej.base.getInstance(document.getElementById("Grid"), ejs.grids.Grid);
    gridObj.query = qryBldrObj.getDataManagerQuery(qryBldrObj.getRules());
    gridObj.refresh();
}
```

### Drag and Drop Enabled
```cshtml
<ejs-querybuilder id="querybuilder" allowDragAndDrop="true" width="70%">
    <e-querybuilder-columns>
        <e-querybuilder-column field="FirstName" label="First Name" type="string"></e-querybuilder-column>
        <e-querybuilder-column field="Country" label="Country" type="string"></e-querybuilder-column>
    </e-querybuilder-columns>
</ejs-querybuilder>
```

## Key Properties Quick Reference

| Property | TagHelper Attribute | Purpose |
|----------|-------------------|---------|
| `Columns` | `e-querybuilder-columns` | Define filterable fields |
| `Rule` | `rule="rule"` | Initial rule — C# `QueryBuilderRule` object |
| `DataSource` | `dataSource` | Bind local/remote data |
| `AllowDragAndDrop` | `allowDragAndDrop` | Enable rule reordering |
| `AllowValidation` | `allowValidation` | Validate rule inputs |
| `EnableSeparateConnector` | `enableSeparateConnector` | Per-rule AND/OR connectors |
| `EnableNotCondition` | `enableNotCondition` | NOT group operator |
| `MaxGroupCount` | `maxGroupCount` | Limit nested group depth |
| `SummaryView` | `summaryView` | Show collapsed rule summary |
| `DisplayMode` | `displayMode` | Horizontal or Vertical layout |
| `EnablePersistence` | `enablePersistence` | Save state to localStorage |
| `EnableRtl` | `enableRtl` | Right-to-left layout |
| `SortDirection` | `sortDirection` | Sort column field list |
| `Readonly` | `readonly` | Disable all interactions |
| `Width` / `Height` | `width` / `height` | Component dimensions |

## Common Use Cases

- **Data grid filter UI** → QueryBuilder + Grid integration via `ruleChange`
- **Save/restore conditions** → `getRules` + `setRules` with localStorage or backend
- **SQL WHERE clause builder** → `getSqlFromRules` / `getParameterizedSql`
- **MongoDB filter** → `getMongoQuery` / `setMongoQuery`
- **Read-only filter display** → `summaryView="true"` + `readonly="true"`
- **Mobile-friendly layout** → `displayMode="Vertical"` + `maxGroupCount="2"`
- **Localized UI** → `locale` property + L10n translation object

## Security & Trust Boundary

### External Dependency: CDN-Based JavaScript Execution

The Syncfusion QueryBuilder requires runtime execution of external JavaScript from the official CDN endpoint (`https://cdn.syncfusion.com/ej2/*/dist/ej2.min.js`). This is a **required trusted dependency** with the following security considerations:

#### Risk Mitigation Strategies

1. **Use HTTPS Only**
   - Always reference CDN resources via HTTPS to prevent man-in-the-middle attacks
   - Verify your layout template uses `https://` scheme

2. **Subresource Integrity (SRI)**
   - Include SRI hash attributes to validate script integrity:
   ```html
   <script src="https://cdn.syncfusion.com/ej2/23.1.43/dist/ej2.min.js" 
           integrity="sha384-[HASH]" 
           crossorigin="anonymous"></script>
   ```

3. **Content Security Policy (CSP)**
   - Add Syncfusion CDN to your CSP whitelist:
   ```
   script-src 'self' https://cdn.syncfusion.com;
   style-src 'self' https://cdn.syncfusion.com;
   ```

4. **Vendor Lock & Trust Assessment**
   - **Trusted Vendor**: Syncfusion is an established commercial component vendor with industry adoption
   - **No Open-Source Alternatives**: QueryBuilder functionality is specialized; evaluate internal development costs vs. vendor dependency
   - **Consider Bundling**: For enhanced control, bundle Syncfusion scripts locally instead of using CDN (download and host on your own domain)

5. **Version Pinning**
   - Always pin the specific version instead of using wildcard versions:
   ```
   ❌ https://cdn.syncfusion.com/ej2/latest/dist/ej2.min.js
   ✅ https://cdn.syncfusion.com/ej2/23.1.43/dist/ej2.min.js
   ```

6. **Update Management**
   - Regularly update Syncfusion NuGet packages and verify corresponding CDN versions match
   - Subscribe to Syncfusion security announcements
   - Test updates in staging environment before production deployment

#### Acceptable Risk Assessment
- **Severity**: Medium (requires trust boundary evaluation at deployment)
- **Mitigation**: Implement SRI + CSP + version pinning
- **Approval**: Obtain security team sign-off for use in compliant applications

---

**Start here:** Read [references/getting-started.md](references/querybuilder-getting-started.md) to set up your first QueryBuilder.
```
