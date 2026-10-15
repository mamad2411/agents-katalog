---
name: syncfusion-aspnetcore-numerictextbox
description: Complete guide to implementing the Syncfusion NumericTextBox component in ASP.NET Core applications with Tag Helpers, currency/percentage formatting, range validation, and globalization support for building professional numeric input forms.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Input Controls"
  platform: "ASP.NET Core"
  framework: "Syncfusion.EJ2.AspNet.Core"
---

# Implementing NumericTextBox in ASP.NET Core

The NumericTextBox is a specialized input component for capturing numeric values with advanced features like currency/percentage formatting, range validation, spinner controls, precision settings, and globalization support. This skill guides you through implementing NumericTextBox in ASP.NET Core applications using Syncfusion's Tag Helper syntax.

## When to Use This Skill

Use this skill when you need to:
- Create numeric input fields with automatic value formatting
- Build currency and percentage input controls
- Implement range validation (min/max constraints)
- Display spinner buttons for increment/decrement operations
- Control decimal precision and number formatting
- Support international number formats and currencies
- Format numbers with locale-specific separators
- Implement salary, price, quantity, or percentage inputs
- Validate numeric ranges with visual feedback
- Create accessible numeric forms following WCAG 2.2 Level AA standards

## Key Features

| Feature | Use Case |
|---------|----------|
| **Number Formatting** | Format as currency, percentage, or custom formats (c2, p, n) |
| **Range Validation** | Set min/max constraints with automatic validation |
| **Precision Control** | Restrict decimal places and rounding behavior |
| **Spinner Buttons** | Increment/decrement values with up/down controls |
| **Step Values** | Define increment step size for spinner operations |
| **Currency Support** | Display and format multiple currencies (USD, EUR, GBP, etc.) |
| **Percentage Input** | Convert and display percentage values |
| **Globalization** | Support 150+ culture-specific number formats |
| **Localization** | Translate spinner button tooltips to user's language |
| **RTL Support** | Right-to-left text direction for Arabic, Hebrew, Persian |
| **Data Binding** | Two-way binding with ASP.NET Core models |
| **Event Handling** | Respond to Created, Change, Blur, and Focus events |

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- Installing Syncfusion.EJ2.AspNet.Core NuGet package
- Adding Tag Helpers to _ViewImports.cshtml
- Adding stylesheets and script resources via CDN
- Registering the script manager
- Creating your first NumericTextBox
- Binding to ASP.NET Core models
- Tag Helper syntax and attributes

### Number Formats
📄 **Read:** [references/number-formats.md](references/number-formats.md)
- Standard numeric format specifiers (c, p, n, e, f)
- Currency formatting with symbol and locale
- Percentage conversion and display
- Custom number format patterns
- Locale-specific formatting (en-US, de-DE, fr-FR)
- Output examples and edge cases
- Format string best practices

### Range Validation
📄 **Read:** [references/range-validation.md](references/range-validation.md)
- Setting minimum and maximum values
- Decimal precision configuration
- Step values and increment behavior
- Automatic value clamping within range
- Validation error handling
- Real-world validation patterns (salary, age, discount)
- Edge cases and boundary conditions

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)
- CSS customization of NumericTextBox wrapper
- Styling spinner up/down buttons
- Input height, font size, and color
- Adding icons and prepend/append templates
- Theme integration with Syncfusion themes
- Responsive design patterns
- Custom CSS classes for validation states

### Globalization and Localization
📄 **Read:** [references/globalization-localization.md](references/globalization-localization.md)
- Culture-based number formatting (CLDR support)
- Setting locale for specific regions
- Multi-currency formatting
- Spinner button tooltip localization
- RTL (right-to-left) language support
- Date and number format culture binding
- Timezone and locale detection

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Data binding with ASP.NET Core models
- Programmatic NumericTextBox creation with C# and JavaScript
- Event handling patterns (Created, Change, Blur, Focus)
- Composite validation scenarios
- Integration with Forms and Model Validation
- Two-way binding with observable models
- Security: XSS prevention and input sanitization

## Quick Start Example

### Basic NumericTextBox with Currency Format (Tag Helper)

```html
<!-- Views/Home/Index.cshtml -->
<div class="form-group">
    <ejs-numerictextbox id="salary" 
        name="salary" 
        placeholder="Enter salary"
        format="c2"
        min="0"
        max="1000000"
        float-label-type="Auto">
    </ejs-numerictextbox>
</div>
```

### In _ViewImports.cshtml (one-time setup)

```html
@addTagHelper *, Syncfusion.EJ2
```

### In _Layout.cshtml (one-time setup)

```html
<head>
    <link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/24.1.48/fluent.css" />
</head>
<body>
    @RenderBody()
    
    <script src="https://cdn.syncfusion.com/ej2/24.1.48/dist/ej2.min.js"></script>
    <ejs-scripts></ejs-scripts>
</body>
```

### Result

User sees:
1. NumericTextBox with "$0.00" format
2. Spinner buttons (↑↓) to increment/decrement values
3. On entry of "5000", displays as "$5,000.00"
4. Values outside 0-1000000 range are auto-corrected
5. When blurred, number formatted to currency with 2 decimal places

## Common Patterns

### Pattern 1: Employee Salary Form with Validation

```html
<!-- Views/Employee/Create.cshtml -->
<form asp-action="SaveEmployee" asp-controller="Employee" method="post">
    <div class="form-group">
        <label asp-for="Salary"></label>
        <ejs-numerictextbox asp-for="Salary"
            format="c2"
            min="20000"
            max="500000"
            step="1000"
            float-label-type="Auto"
            css-class="e-outline">
        </ejs-numerictextbox>
        <small class="form-text text-muted">Salary range: $20,000 - $500,000</small>
    </div>

    <div class="form-group">
        <label asp-for="Bonus"></label>
        <ejs-numerictextbox asp-for="Bonus"
            format="c2"
            min="0"
            max="50000"
            step="100"
            float-label-type="Auto">
        </ejs-numerictextbox>
    </div>

    <button type="submit" class="btn btn-primary">Save Employee</button>
</form>
```

### Pattern 2: Product Pricing with Percentage Discount

```html
<div class="row">
    <div class="col-md-6">
        <div class="form-group">
            <label asp-for="OriginalPrice"></label>
            <ejs-numerictextbox asp-for="OriginalPrice"
                placeholder="Original price"
                format="c2"
                min="0"
                step="0.01"
                float-label-type="Auto">
            </ejs-numerictextbox>
        </div>
    </div>

    <div class="col-md-6">
        <div class="form-group">
            <label asp-for="DiscountPercent"></label>
            <ejs-numerictextbox asp-for="DiscountPercent"
                placeholder="Discount %"
                format="p2"
                min="0"
                max="100"
                step="5"
                float-label-type="Auto"
                change="onDiscountChange">
            </ejs-numerictextbox>
        </div>
    </div>
</div>

<div class="form-group">
    <label>Final Price</label>
    <ejs-numerictextbox id="finalPrice"
        format="c2"
        read-only="true"
        float-label-type="Auto">
    </ejs-numerictextbox>
</div>

<script>
    function onDiscountChange(args) {
        var originalPrice = document.querySelector('input[id="originalPrice"]').value;
        var discountPercent = args.value;
        var finalPrice = originalPrice * (1 - discountPercent / 100);
        
        var finalPriceControl = document.querySelector('input[id="finalPrice"]');
        var finalPriceInstance = finalPriceControl.ej2_instances[0];
        finalPriceInstance.value = finalPrice;
    }
</script>
```

### Pattern 3: Quantity Input with Stock Constraint

```html
<div class="form-group">
    <label asp-for="OrderQuantity"></label>
    <ejs-numerictextbox asp-for="OrderQuantity"
        placeholder="Order quantity"
        min="1"
        max="100"
        step="1"
        float-label-type="Auto"
        css-class="e-outline"
        change="checkInventory">
    </ejs-numerictextbox>
    <small>Available stock: 100 units</small>
</div>

<div class="form-group">
    <label>Unit Price: $25.00</label>
    <ejs-numerictextbox id="totalPrice"
        format="c2"
        read-only="true"
        float-label-type="Auto">
    </ejs-numerictextbox>
</div>

<script>
    document.querySelector('input[asp-for="OrderQuantity"]').addEventListener('change', function(e) {
        var quantity = parseInt(e.target.value) || 0;
        var unitPrice = 25;
        var totalPrice = quantity * unitPrice;
        
        var totalPriceControl = document.querySelector('input[id="totalPrice"]');
        var totalPriceInstance = totalPriceControl.ej2_instances[0];
        totalPriceInstance.value = totalPrice;
    });
</script>
```

### Pattern 4: International Currency Selection with Culture

```html
<div class="row">
    <div class="col-md-6">
        <div class="form-group">
            <label asp-for="Currency"></label>
            <select asp-for="Currency" id="currencySelect" class="form-control">
                <option value="en-US">USD ($)</option>
                <option value="de-DE">EUR (€)</option>
                <option value="fr-FR">GBP (£)</option>
            </select>
        </div>
    </div>

    <div class="col-md-6">
        <div class="form-group">
            <label asp-for="Amount"></label>
            <ejs-numerictextbox asp-for="Amount"
                placeholder="Enter amount"
                format="c2"
                float-label-type="Auto">
            </ejs-numerictextbox>
        </div>
    </div>
</div>

<script>
    document.getElementById('currencySelect').addEventListener('change', function(e) {
        var culture = e.target.value;
        var amountControl = document.querySelector('input[asp-for="Amount"]');
        var amountInstance = amountControl.ej2_instances[0];
        amountInstance.locale = culture;
    });
</script>
```

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `min` | decimal | -∞ | Minimum acceptable value |
| `max` | decimal | +∞ | Maximum acceptable value |
| `step` | decimal | 1 | Increment/decrement step for spinner |
| `value` | decimal | null | Initial numeric value |
| `format` | string | "n2" | Number format (c, p, n, e, f) |
| `decimals` | int | 2 | Number of decimal places |
| `placeholder` | string | - | Placeholder text |
| `read-only` | bool | false | Prevent manual input while allowing spinner |
| `disabled` | bool | false | Completely disable input |
| `show-spin-button` | bool | true | Display up/down spinner buttons |
| `float-label-type` | enum | Never | Label animation (Auto, Always, Never) |
| `css-class` | string | - | CSS classes for styling |
| `created` | string | - | Event handler for NumericTextBox created |
| `change` | string | - | Event handler for value change |
| `blur` | string | - | Event handler for blur event |

## Common Use Cases

### Use Case 1: Financial Forms (Payroll, Invoicing)
Create payroll or invoicing forms with currency formatting and validation:
- **When:** Building financial transaction forms
- **Reference:** [range-validation.md](references/range-validation.md) + [number-formats.md](references/number-formats.md)
- **Key Features:** Currency format (c2), min/max validation, step control

### Use Case 2: International E-Commerce
Build multi-currency shopping carts with locale-aware formatting:
- **When:** Creating international sales platforms
- **Reference:** [globalization-localization.md](references/globalization-localization.md)
- **Key Features:** Culture-based formatting, multiple currencies, localized tooltips

### Use Case 3: Data Entry Forms with Constraints
Create data entry forms with strict numeric ranges and precision:
- **When:** Building inventory, survey, or analytics forms
- **Reference:** [range-validation.md](references/range-validation.md)
- **Key Features:** Min/max validation, decimal precision, step values

### Use Case 4: Scientific/Engineering Calculations
Implement precision numeric inputs for technical applications:
- **When:** Building calculation tools, scientific software
- **Reference:** [advanced-patterns.md](references/advanced-patterns.md)
- **Key Features:** High precision decimals, custom formats, event-driven calculations

---

**Next Steps:**
1. Review [getting-started.md](references/getting-started.md) to set up your first NumericTextBox
2. Choose your use case and follow the corresponding reference guide
3. Copy code examples and adapt to your project
4. Refer to [advanced-patterns.md](references/advanced-patterns.md) for complex scenarios
