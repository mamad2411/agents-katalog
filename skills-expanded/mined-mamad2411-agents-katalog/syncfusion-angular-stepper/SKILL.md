---
name: syncfusion-angular-stepper
description: Create and configure Syncfusion Angular Stepper component for multi-step workflows, wizards, forms, and onboarding flows. Use this skill when implementing step-by-step navigation, configuring step validation, handling step events, or customizing step appearance with icons, labels, and templates. This covers stepper-based wizard interfaces, progress tracking workflows, and multi-form configurations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular Stepper

The Syncfusion Angular Stepper component displays a step-by-step process or workflow, ideal for wizards, onboarding, or multi-step forms. This skill guides you through implementing, configuring, and customizing the Stepper component with complete control over step appearance, validation, events, and animations.

## When to Use This Skill

**Use this skill when:**
- Building multi-step wizards or workflows
- Creating step-by-step forms or onboarding flows
- Configuring step validation and linear flow
- Adding icons, labels, and custom templates to steps
- Handling step events (created, stepChanged, stepChanging, beforeStepRender, stepClick)
- Customizing step appearance with animations and styling
- Implementing tooltips, globalization, or RTL support

## Component Overview

The Stepper component provides:
- **Multiple step types**: Default (icons + labels), Indicator Only, Label Only
- **Two orientations**: Horizontal (default) and Vertical
- **Rich event system**: created, stepChanged, stepChanging, beforeStepRender, stepClick
- **Step validation**: Linear flow, completion states, conditional progression
- **Customization**: Icons, labels, templates, animations, tooltips
- **Accessibility**: WCAG compliance, keyboard navigation, RTL support

## Complete Table of Contents

### 🚀 Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package configuration
- Angular CLI setup and dependencies
- Basic stepper implementation in standalone Angular
- CSS imports and theme setup
- First render and initial configuration

### 📋 API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- **Stepper Component Properties**: `activeStep`, `animation`, `cssClass`, `enablePersistence`, `enableRtl`, `labelPosition`, `linear`, `locale`, `orientation`, `readOnly`, `showTooltip`, `stepType`, `steps`, `template`, `tooltipTemplate`
- **Step Model Properties**: `cssClass`, `disabled`, `iconCss`, `isValid`, `label`, `optional`, `status`, `text`
- **Animation Settings**: `enable`, `duration`, `delay`
- **Stepper Methods**: `destroy()`, `nextStep()`, `previousStep()`, `refreshProgressbar()`, `reset()`
- **Events Overview**: `created`, `stepChanged`, `stepChanging`, `stepClick`, `beforeStepRender`
- **Enumerations**: `StepType`, `StepStatus`, `StepLabelPosition`, `StepperOrientation`

### ⚙️ Configuring Steps
📄 **Read:** [references/steps-configuration.md](references/steps-configuration.md)
- Adding steps with `<e-step>` directive
- Configuring icons with `iconCss` property
- Setting labels and text content
- Setting active step with `activeStep`
- Optional steps and disabling steps
- Step read-only mode
- Step status tracking
- Step validation with `isValid` property
- Label positioning and alignment

### 🎨 Choosing Step Types
📄 **Read:** [references/step-types.md](references/step-types.md)
- Default type with indicators and labels
- Indicator Only type for compact layouts
- Label Only type for text-based navigation
- Label positions (Top, Bottom, Start, End)
- When to use each type
- Type selection patterns

### 📐 Setting Orientations
📄 **Read:** [references/orientations-and-layouts.md](references/orientations-and-layouts.md)
- Horizontal orientation (default)
- Vertical orientation for tall layouts
- Layout configuration and responsive design
- Orientation selection based on use case

### 🎯 Handling Events & Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- `created` event for initialization
- `stepChanged` event after step changes (with EventArgs)
- `stepChanging` event for step change prevention (with EventArgs)
- `beforeStepRender` event for pre-render customization (with EventArgs)
- `stepClick` event for click handling (with EventArgs)
- Complete EventArgs reference documentation
- Event handler patterns and best practices

### ✅ Validation and Flow Control
📄 **Read:** [references/validation-and-flow.md](references/validation-and-flow.md)
- Linear flow configuration for sequential progression
- Step validation and completion states
- Step status management
- Conditional step progression
- Error handling and state management

### 🎭 Templates and Styling
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Custom step templates using `<ng-template>`
- Template binding and data context
- CSS class customization (`cssClass` property)
- Layout and appearance customization
- Responsive styling patterns

### 🌟 Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation settings (duration, delay, enable) with StepperAnimationSettingsModel
- Tooltip configuration and tooltip templates
- Globalization and localization (i18n)
- RTL (Right-to-Left) support with `enableRtl`
- Accessibility features and keyboard navigation
- WCAG compliance and screen reader support

## Quick Start Example

```ts
import { Component } from "@angular/core";
import { StepperAllModule, StepperModule } from "@syncfusion/ej2-angular-navigations";

@Component({
  imports: [ StepperAllModule, StepperModule ],
  standalone: true,
  selector: 'app-root',
  template: `
    <div class="stepper-container">
      <ejs-stepper>
        <e-steps>
          <e-step label="Cart" iconCss="sf-icon-cart"></e-step>
          <e-step label="Delivery Address" iconCss="sf-icon-transport"></e-step>
          <e-step label="Payment" iconCss="sf-icon-payment"></e-step>
          <e-step label="Confirmation" iconCss="sf-icon-success"></e-step>
        </e-steps>
      </ejs-stepper>
    </div>
  `,
  styles: [`
    .stepper-container {
      padding: 20px;
      max-width: 800px;
      margin: 0 auto;
    }
  `]
})
export class AppComponent { }
```

## Common Patterns

### Pattern 1: Wizard with Form Validation
```html
<ejs-stepper (stepChanging)="onStepChanging($event)">
  <e-steps>
    <e-step label="Personal Info"></e-step>
    <e-step label="Contact Details"></e-step>
    <e-step label="Address"></e-step>
    <e-step label="Confirmation"></e-step>
  </e-steps>
</ejs-stepper>
```

Use the `stepChanging` event to validate form data before allowing step progression.

### Pattern 2: Dynamic Step Icons
```html
<ejs-stepper>
  <e-steps>
    <e-step *ngFor="let step of steps" 
            [label]="step.label" 
            [iconCss]="step.icon"></e-step>
  </e-steps>
</ejs-stepper>
```

Bind step data dynamically using `*ngFor` directive.

### Pattern 3: Linear Workflow
```html
<ejs-stepper [linear]="true">
  <e-steps>
    <e-step label="Step 1"></e-step>
    <e-step label="Step 2"></e-step>
    <e-step label="Step 3"></e-step>
  </e-steps>
</ejs-stepper>
```

Enable `linear` property to enforce sequential progression.

### Pattern 4: Event Handling
```ts
onStepChanged(args: StepperChangedEventArgs) {
  console.log(`Active step index: ${args.activeStep}`);
}

onStepChanging(args: StepperChangingEventArgs) {
  if (!isFormValid()) {
    args.cancel = true; // Prevent step change
  }
}
```

Use event handlers to track navigation and validate progress.

## Key Properties Summary

| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `stepType` | StepType | Default | Change display style: Default, Indicator, Label |
| `orientation` | Orientation | Horizontal | Set layout: Horizontal or Vertical |
| `linear` | boolean | false | Enforce sequential progression |
| `activeStep` | number | 0 | Set current active step (0-indexed) |
| `animation` | StepperAnimationSettingsModel | enabled | Configure transition animations |
| `showTooltip` | boolean | false | Display tooltips on step hover |
| `labelPosition` | string | Bottom | Position labels: Top, Bottom, Start, End |
| `readOnly` | boolean | false | Disable all step interactions |
| `cssClass` | string | - | Apply custom CSS classes |
| `enableRtl` | boolean | false | Enable RTL for Arabic, Hebrew, Urdu |
| `enablePersistence` | boolean | false | Persist state between page reloads |
| `locale` | string | en-US | Set language/culture |

**For complete API reference with code examples, see:** [📚 API Reference](references/api-reference.md)

## Common Use Cases

**Wizard Forms**: Implement multi-step form wizards with validation at each step
**Onboarding Flow**: Guide new users through setup or introduction steps
**Process Tracking**: Display workflow progress (order processing, job applications)
**Multi-Step Checkout**: Create shopping cart workflows with address and payment steps
**Setup Assistants**: Configure tools or services through guided step-by-step setup
**Document Submission**: Multi-step document upload with validation

---

**Next Steps:** Select a reference above based on what you need to implement. Start with [getting-started.md](references/getting-started.md) if this is your first time using the Stepper component.
