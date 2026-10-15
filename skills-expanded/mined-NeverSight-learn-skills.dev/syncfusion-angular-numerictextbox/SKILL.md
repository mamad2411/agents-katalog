---
name: syncfusion-angular-numerictextbox
description: Comprehensive guide for implementing Syncfusion Angular NumericTextBox component. Use this when building numeric input controls with validation, formatting, spin buttons, adornments, and accessibility features. This skill covers number formatting, spinners, numeric form validation, and advanced patterns for Angular applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Inputs"
---

# Implementing Syncfusion Angular NumericTextBox

## Component Overview

The Syncfusion Angular NumericTextBox is a specialized input control for numeric values. It provides:
- **Numeric validation** with min/max ranges and strict mode
- **Formatting** (currency, percentage, decimals)
- **Spin buttons** for value adjustment
- **Adornments** (prepend/append templates for icons, labels)
- **Accessibility** (WCAG 2.2, ARIA, keyboard navigation)
- **Localization** (multiple cultures and RTL support)
- **Form integration** (reactive forms, template-driven forms)

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Angular 21+ standalone component setup
- Basic NumericTextBox implementation
- CSS imports and theme configuration
- Range validation with min/max
- Simple formatting example
- Precision and decimals control
- Two-way binding setup
- Reactive forms integration

### Formats and Number Styling
📄 **Read:** [references/formats-styling.md](references/formats-styling.md)
- Standard formats (currency `c2`, percentage `p`, numbers `n`)
- Custom numeric format strings
- Decimal place control
- Currency symbols and localization
- Styling NumericTextBox wrapper and icons
- CSS customization patterns

### Spinners and Step Control
📄 **Read:** [references/spinners-and-step.md](references/spinners-and-step.md)
- Spin button visibility (`showSpinButton`)
- Step value configuration (`step` property)
- Customizing spin up/down arrow icons
- Arrow key interactions
- Disabling spin buttons

### Adornments and Templates
📄 **Read:** [references/adornments-and-templates.md](references/adornments-and-templates.md)
- Adding prefix/suffix with `prependTemplate` and `appendTemplate`
- Currency symbols and unit labels
- Action buttons and icons
- Status indicators without affecting validation
- Template usage patterns

### Validation and Form Integration
📄 **Read:** [references/validation-and-forms.md](references/validation-and-forms.md)
- Range validation (min/max with strictMode)
- Custom validation rules
- Error and warning states
- Reactive forms patterns

### Advanced Patterns and Edge Cases
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Maintaining trailing zeros on focus
- Preventing nullable input (always require a value)
- Nullable input configuration
- Clear button behavior
- Read-only and disabled states
- Focus and blur event handling
- Float label types (Always, Auto, Never)
- Performance optimization

### Accessibility and Migration
📄 **Read:** [references/accessibility-and-migration.md](references/accessibility-and-migration.md)
- WCAG 2.2 Level AA compliance
- ARIA attributes (spinbutton role, aria-valuemin, aria-valuemax, etc.)
- Keyboard navigation (Arrow Up/Down)
- Screen reader support
- RTL support for right-to-left languages
- EJ1 to EJ2 API migration guide
- Localization and globalization

### Globalization and Localization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Locale property configuration
- Culture-specific number formatting
- RTL (right-to-left) support
- International number formats

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- All component properties with types, defaults, and descriptions
- All public methods with signatures and usage examples
- All events with argument interface details
- `ChangeEventArgs`, `NumericBlurEventArgs`, `NumericFocusEventArgs` interfaces
- Complete summary tables for quick lookup

---

## Quick Start Example

```typescript
import { NumericTextBoxModule } from '@syncfusion/ej2-angular-inputs';
import { Component } from '@angular/core';

@Component({
  imports: [NumericTextBoxModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-numerictextbox
      value="100"
      min="10"
      max="1000"
      step="5"
      format="c2"
      placeholder="Enter amount">
    </ejs-numerictextbox>
  `
})
export class AppComponent {}
```

---

## Common Patterns

### Currency Input with Validation
```typescript
<ejs-numerictextbox
  value="50.00"
  format="c2"
  currency="USD"
  min="0"
  max="10000"
  decimals="2"
  strictMode="true">
</ejs-numerictextbox>
```

### Percentage Input
```typescript
<ejs-numerictextbox
  value="25"
  format="p"
  min="0"
  max="100"
  step="1">
</ejs-numerictextbox>
```

### With Adornments (Unit Label)
```typescript
<ejs-numerictextbox
  value="100"
  [appendTemplate]="appendUnit">
</ejs-numerictextbox>

<ng-template #appendUnit>
  <span class="unit-label">kg</span>
</ng-template>
```

### Two-Way Binding with Form Control
```typescript
<ejs-numerictextbox
  [(ngModel)]="quantity"
  min="1"
  max="100"
  step="1">
</ejs-numerictextbox>
```

---

## Key Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `value` | number | Current numeric value | `null` |
| `min` | number | Minimum allowed value | `Number.MIN_VALUE` |
| `max` | number | Maximum allowed value | `Number.MAX_VALUE` |
| `step` | number | Increment/decrement amount | `1` |
| `decimals` | number | Decimal places allowed | `null` |
| `format` | string | Number format (e.g., 'c2', 'n2', 'p') | `null` |
| `currency` | string | Currency code (e.g., 'USD', 'EUR') | `null` |
| `strictMode` | boolean | Enforce min/max validation | `false` |
| `showSpinButton` | boolean | Show up/down spinner buttons | `true` |
| `showClearButton` | boolean | Show clear button | `false` |
| `readonly` | boolean | Prevent editing | `false` |
| `disabled` | boolean | Disable the component | `false` |
| `locale` | string | Culture code (e.g., 'de-DE', 'fr-FR') | `'en-US'` |
| `enableRtl` | boolean | Enable right-to-left mode | `false` |
| `placeholder` | string | Hint text | `null` |
| `floatLabelType` | string | Label float behavior ('Auto', 'Always', 'Never') | `'Never'` |

---

## Common Use Cases

1. **E-Commerce Quantity Input** — Product quantity selector with min/max validation
2. **Financial Forms** — Currency input with currency symbol and decimal places
3. **Scientific Applications** — High-precision decimal inputs
4. **Survey/Form Data** — Percentage inputs with 0-100 range
5. **Multi-Language Support** — Numbers formatted per user locale
6. **Accessibility-First Forms** — WCAG-compliant numeric inputs
7. **Mobile-Friendly** — Touch-friendly spin buttons and keyboard input

---

## See Also

- [Syncfusion Angular Input Controls](https://www.syncfusion.com/angular-components/angular-textbox)
- [Angular Forms Documentation](https://angular.dev/guide/forms)
- [WCAG 2.2 Accessibility Guidelines](https://www.w3.org/TR/WCAG22/)
- [Syncfusion Theme Studio](https://ej2.syncfusion.com/angular/documentation/appearance/theme-studio)
