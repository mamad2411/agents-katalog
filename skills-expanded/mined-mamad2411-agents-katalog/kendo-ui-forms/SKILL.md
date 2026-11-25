---
name: kendo-ui-forms
description: Use when implementing or reviewing Kendo UI form widgets, Validator, model-driven validation, error messaging patterns, and multi-step form flows.
---

# Kendo UI Forms

## Specialization

Implement and review expert-level Kendo UI form patterns covering widget composition (NumericTextBox, DatePicker, DropDownList, MultiSelect, Upload, MaskedTextBox), Kendo UI Validator configuration, model-driven validation via DataSource schema, custom validation rules, error surfacing strategy, and multi-step form flows.

## Trigger Conditions

- Composing a data-entry form using Kendo UI input widgets.
- Configuring `kendo.ui.Validator` for synchronous client-side validation.
- Implementing custom validation rules that extend the Kendo UI Validator.
- Wiring form widget values to a DataSource model for CRUD Grid editing.
- Implementing a multi-step wizard using Kendo UI Stepper or sequential Dialog/Window components.
- Reviewing form error message placement and ARIA compliance.
- Handling server-side validation errors returned from DataSource transport and surfacing them in the form.
- Implementing file upload with server-side validation feedback via Kendo UI Upload.

## Scope Boundaries

In scope:

- Kendo UI input widget configuration: NumericTextBox, DatePicker, TimePicker, DateTimePicker, DateRangePicker, DropDownList, DropDownTree, ComboBox, AutoComplete, MultiSelect, MaskedTextBox, ColorPicker, Slider, RangeSlider, Switch, Upload.
- Kendo UI Validator: built-in rules, custom rules, message customization, validation trigger configuration.
- DataSource model validation: `required`, `type`, `min`, `max`, `pattern` field constraints.
- Error message display: inline validation messages, tooltip validation messages, summary panels.
- Server validation error routing: transport `error` callback → Validator or custom UI.
- ARIA compliance for form widgets and validation messages (coordinate with `kendo-ui-accessibility`).
- Multi-step form flows using Kendo UI Stepper.

Out of scope:

- DataSource transport and remote configuration (see `kendo-ui-data-binding`).
- Full accessibility audit (see `kendo-ui-accessibility`).
- Security review of form input handling (see `kendo-ui-security`).
- Server-side validation implementation.

## Inputs

- Form fields and their data types, constraints, and widget type.
- Validation rules: required, type, range, pattern, or custom.
- Error message placement preference: inline, tooltip, or summary.
- Server validation error response format.
- Kendo UI version in use.

## Required Outputs

- Widget composition with correct `name` attributes for Validator targeting.
- Validator configuration with all required rules and custom rule implementations.
- Error message template with accessible `aria-describedby` wiring.
- Server validation error routing strategy.
- Form submission guard: prevent submission when Validator reports invalid state.
- Multi-step flow state management if applicable.

## Core Patterns

### Kendo UI Validator Setup

```javascript
var validator = $("#myForm").kendoValidator({
    rules: {
        // Custom rule: must be future date
        futureDate: function(input) {
            if (input.is("[data-future-date-rule]")) {
                return kendo.parseDate(input.val()) > new Date();
            }
            return true;
        }
    },
    messages: {
        futureDate: "Date must be in the future.",
        required: function(input) {
            return input.attr("data-label") + " is required.";
        }
    }
}).data("kendoValidator");

// Guard form submission
$("#submitBtn").on("click", function() {
    if (validator.validate()) {
        // safe to submit
    }
});
```

### Widget Name Binding for Validator

```html
<!-- name attribute is required for Validator to target the widget -->
<input id="price" name="price" data-role="numerictextbox"
       data-min="0" data-required-msg="Price is required" required />

<span data-for="price" class="k-invalid-msg"></span>
```

### Server Validation Error Routing

```javascript
var dataSource = new kendo.data.DataSource({
    // ...
    error: function(e) {
        var errors = e.errors;
        if (errors) {
            // Surface server errors to validator or notification widget
            Object.keys(errors).forEach(function(field) {
                var input = $("[name='" + field + "']");
                input.attr("data-server-error", errors[field]);
            });
            validator.validate(); // Re-trigger to show server messages
        }
    }
});
```

### Multi-Step Form with Stepper

```javascript
$("#stepper").kendoStepper({
    steps: [
        { label: "Personal Info", icon: "user" },
        { label: "Address", icon: "map-marker" },
        { label: "Confirmation", icon: "check" }
    ]
});

// Validate current step before advancing
function advanceStep(stepper, currentStepValidator) {
    if (currentStepValidator.validate()) {
        stepper.next();
    }
}
```

## Validation Rule Priority

1. DataSource model field constraints (enforced on save).
2. Kendo UI Validator built-in rules (enforced on submit/blur).
3. Custom Validator rules (extend built-in for domain logic).
4. Server validation errors (routed back to the form after transport failure).

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Single form field with required validation | Validator blocks submission when empty; error message visible |
| L2 Practical | Full form with multiple widgets, type/range/pattern rules, and server error routing | All validation rules enforced; server errors surface in form |
| L3 Hardening | Accessible error messages with ARIA + server round-trip validation | ARIA `aria-describedby` wired; server errors displayed without page reload |
| L4 Expert | Multi-step wizard with per-step validation and shared DataSource model | Stepper advances only on valid step; final submit posts complete model |
