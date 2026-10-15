---
name: syncfusion-aspnetcore-stepper
description: Create and configure ASP.NET Core Stepper controls to support multi-step workflows and progressive user interfaces. This skill should be applied when implementing step navigation, wizards, progress trackers, form flows, checkout processes, or any sequential step-based UI. It is also relevant whenever requirements involve steppers, step validation, step navigation, linear flows, or step-based state management.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Controls"
---

# Implementing ASP.NET Core Stepper Control

The Syncfusion ASP.NET Core Stepper is a navigation component that guides users through a series of logical steps in a sequential workflow. Use it for wizards, multi-step forms, checkout processes, and any experience requiring step-by-step progression.

## When to Use This Skill

- **Multi-step forms or wizards** - Guide users through sequential data collection
- **Checkout flows** - Show shopping cart → shipping → payment → confirmation
- **Progress tracking** - Display task or process completion status
- **Linear workflows** - Enforce sequential step progression (e.g., registration, onboarding)
- **Status visualization** - Show which steps are completed, in-progress, or pending
- **Step validation** - Display validation state (success/error) for each step

## Control Overview

**Key Capabilities:**
- Sequential step navigation with automatic or manual progression
- Multiple step display types (default with indicators + labels, label-only, indicator-only)
- Horizontal and vertical orientations for different layouts
- Step status management (NotStarted, InProgress, Completed)
- Step validation with success/error indicators
- Linear mode for enforcing sequential progression
- Rich templating for custom step content
- Events for step changes, validation, and interactions
- Tooltips with custom templates for additional guidance
- Animation effects for smooth transitions
- Localization and RTL support

---

## Installation and Setup

**Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation
- TagHelper registration in _ViewImports.cshtml
- CDN and NPM resource includes
- Basic project setup

---

## Creating Your First Stepper

**Quick Start Example - Basic horizontal stepper with 4 steps:**

```html
<ejs-stepper id="stepper" activeStep="0">
    <e-stepper-steps>
        <e-stepper-step iconCss="sf-icon-cart" label="Shopping Cart" text="Review items"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-transport" label="Shipping" text="Enter address"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-payment" label="Payment" text="Select payment"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-success" label="Confirmation" text="Order complete"></e-stepper-step>
    </e-stepper-steps>
</ejs-stepper>
```

**Vertical stepper:**

```html
<ejs-stepper id="stepper" orientation="Vertical">
    <e-stepper-steps>
        <e-stepper-step iconCss="sf-icon-cart" label="Cart"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-transport" label="Shipping"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-payment" label="Payment"></e-stepper-step>
    </e-stepper-steps>
</ejs-stepper>
```

---

## Stepper Properties

**Complete reference:** [references/stepper-properties-reference.md](references/stepper-properties-reference.md)

**Key Stepper-Level Properties (15 total):**
- `activeStep` - Current step index (0-based)
- `animation` - Step transition animation configuration
- `cssClass` - CSS class for component styling
- `enablePersistence` - Persist state across page reloads
- `enableRtl` - Right-to-left layout support
- `labelPosition` - Label placement (Top, Bottom, Start, End)
- `linear` - Sequential-only progression mode
- `locale` - Localization culture setting
- `orientation` - Horizontal or Vertical layout
- `readOnly` - Disable all interactions
- `showTooltip` - Display tooltips on hover
- `stepType` - Visual style (Default, Label, Indicator)
- `steps` - Array of step definitions
- `template` - Custom step content template
- `tooltipTemplate` - Custom tooltip template

---

## Step Properties

**Complete reference:** [references/stepper-properties-reference.md](references/stepper-properties-reference.md)

**Step-Level Properties (8 total):**
- `cssClass` - CSS class for individual step
- `disabled` - Disable specific step
- `iconCss` - Icon CSS class
- `isValid` - Validation state (true/false/null)
- `label` - Step label text
- `optional` - Mark step as optional
- `status` - Step status (NotStarted, InProgress, Completed)
- `text` - Step descriptive text

---

## Animation Properties

**Animation Configuration (3 properties):**
- `enable` - Enable/disable animation
- `duration` - Animation duration in milliseconds
- `delay` - Delay before animation starts

**Example:**
```html
<ejs-stepper id="stepper">
    <e-stepper-animation enable="true" duration="1000" delay="500"></e-stepper-animation>
    <e-stepper-steps>
        <e-stepper-step label="Step 1"></e-stepper-step>
        <e-stepper-step label="Step 2"></e-stepper-step>
    </e-stepper-steps>
</ejs-stepper>
```

---

## Stepper Methods

**Complete reference:** [references/stepper-methods-reference.md](references/stepper-methods-reference.md)

**Available Methods (12 total):**
- `nextStep()` - Move to next step programmatically
- `previousStep()` - Move to previous step
- `addEventListener(eventName, handler)` - Add event listener
- `removeEventListener(eventName, handler)` - Remove event listener
- `dataBind()` - Apply pending property changes
- `refresh()` - Re-render component
- `refreshProgressbar()` - Update progress bar position
- `reset()` - Reset to first step
- `getRootElement()` - Get root DOM element
- `destroy()` - Clean up component
- `appendTo(selector)` - Append to target element

---

## Events and Event Arguments

**Complete reference:** [references/events-and-interactions.md](references/events-and-interactions.md)

**Available Events (5 total):**

### created
Fires after stepper rendering completes.
- **Args:** Event object

### stepChanged
Fires after active step successfully changes.
- **Args:** `activeStep`, `element`, `event`, `isInteracted`, `name`

### stepChanging
Fires before active step changes (allows cancellation for validation).
- **Args:** `activeStep`, `cancel`, `element`, `event`, `isInteracted`

### stepClick
Fires when user clicks a step.
- **Args:** `activeStep`, `previousStep`, `element`, `event`, `name`

### beforeStepRender
Fires before rendering each step (allows dynamic modifications).
- **Args:** `index`, `element`, `name`

---

## Step Types and Orientations

**Read:** [references/step-types-and-styles.md](references/step-types-and-styles.md)
- Default step type (icons + labels)
- Label-only step type with label positioning (Top, Bottom, Start, End)
- Indicator-only step type
- Horizontal orientation (side-by-side steps)
- Vertical orientation (stacked steps)
- Visual appearance customization

---

## Step Configuration

**Read:** [references/steps-configuration.md](references/steps-configuration.md)
- Defining step icons with iconCss property
- Adding text content and labels to steps
- Optional step indicator
- Disabling steps to prevent interaction
- Setting active step with activeStep property
- Step status values (NotStarted, InProgress, Completed)
- Applying CSS classes for custom styling
- Step validation with isValid property

---

## Events and Interactions

**Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Created event when stepper finishes rendering
- stepChanged event after active step changes
- stepChanging event before step change (validation point)
- stepClick event when user clicks a step
- beforeStepRender event for dynamic step modification
- Linear navigation mode for sequential-only progression
- Event pattern examples

---

## Templates and Customization

**Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Custom step templates with step model context
- Tooltip configuration and display
- Tooltip templates for detailed step information
- CSS class customization
- CSS properties for styling
- Theme and appearance customization
- Animation effects with duration and delay

---

## Advanced Features

**Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation configuration (enable, duration, delay)
- Linear flow for sequential-only step progression
- Localization and locale customization
- RTL (right-to-left) layout support
- Readonly mode to disable all interactions
- Accessibility considerations
- Performance optimization

---

## Step Validation

**Read:** [references/steps-validation.md](references/steps-validation.md)
- Step validation patterns (isValid property)
- Form validation with stepChanging event
- Async validation patterns with fetch API
- Real-time validation on user input
- Validation state values (true/false/null)

---

## Common Patterns

### Wizard Pattern with Linear Navigation
For forms that require sequential step completion, enable linear mode:

```html
<ejs-stepper id="wizard" linear="true">
    <e-stepper-steps>
        <e-stepper-step iconCss="sf-icon-cart" label="Cart"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-transport" label="Shipping"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-payment" label="Payment"></e-stepper-step>
    </e-stepper-steps>
</ejs-stepper>
```

### Step Validation Pattern
Validate form content before allowing step progression using `stepChanging` event:

```html
<ejs-stepper id="wizard" linear="true" stepChanging="validateStep">
    <e-stepper-steps>
        <e-stepper-step iconCss="sf-icon-cart" label="Cart"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-transport" label="Shipping"></e-stepper-step>
        <e-stepper-step iconCss="sf-icon-payment" label="Payment"></e-stepper-step>
    </e-stepper-steps>
</ejs-stepper>

<script>
function validateStep(args) {
    var form = document.getElementById('stepForm');
    if (!form.checkValidity()) {
        args.cancel = true;  // Prevent step change
        alert('Please complete all required fields');
    }
}
</script>
```

### Dynamic Content Pattern
Load and display different content based on active step:

```html
<ejs-stepper id="stepper" activeStep="@Model.CurrentStep" stepChanged="onStepChanged">
    <e-stepper-steps>
        <!-- Steps here -->
    </e-stepper-steps>
</ejs-stepper>

<div id="content">
    <!-- Content loads dynamically based on active step -->
</div>

<script>
function onStepChanged(args) {
    loadContentForStep(args.activeStep);
}

function loadContentForStep(stepIndex) {
    // Load content via AJAX or from pre-loaded data
}
</script>
```

---

## Common Use Cases

1. **E-commerce checkout** - Cart → Address → Payment → Confirmation
2. **User registration** - Account info → Email verification → Profile → Complete
3. **Application wizard** - Requirements → Configuration → Review → Deploy
4. **Onboarding flow** - Welcome → Profile → Preferences → Start
5. **Task workflow** - Analyze → Plan → Execute → Review
6. **Multi-form survey** - Demographics → Questions part 1 → Questions part 2 → Summary
