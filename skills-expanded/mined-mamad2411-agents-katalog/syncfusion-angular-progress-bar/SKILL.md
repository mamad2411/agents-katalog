---
name: syncfusion-angular-progress-bar
description: Implement Angular Progress Bar components for visual progress tracking. Use when you need to show determinate, indeterminate, or buffered progress in linear or circular shapes with animations, customization, and accessibility support.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Notifications"
---

# Implementing Syncfusion Angular Progress Bar

The Angular Progress Bar is a lightweight component that visually represents the progress of a task or process. It supports multiple shapes (linear, circular, semi-circular), progress modes (determinate, indeterminate, buffer), animations, and comprehensive customization options.

## When to Use This Skill

**Use this skill when:**
- You need to display progress of a task in Angular
- You want to show loading states with animations
- You need different progress bar shapes (linear, circular)
- You're building download/upload progress UI
- You need accessibility-compliant progress indicators
- You want to display multiple progress states (primary + secondary)

**Don't use this skill for:**
- Spinners (use Skeleton Loader for loading states)
- Step indicators (use Stepper component)
- Timeline visualization (use Timeline component)

## Component Overview

The Syncfusion Progress Bar provides:
- **Multiple Shapes**: Linear, Circular, SemiCircular
- **Progress Modes**: Determinate, Indeterminate, Buffer
- **Animations**: Smooth progress transitions with customizable duration and delay
- **Customization**: Colors (progress, track, secondary), thickness, segments, corner radius, ranges
- **Segment Support**: Divide progress into segments with adjustable spacing
- **Accessibility**: Full WCAG compliance, keyboard navigation, ARIA attributes
- **Events**: Progress completion, value changes, text rendering
- **Reactive**: Works seamlessly with Angular's change detection

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Angular dependencies and imports
- Basic progress bar implementation
- CSS theme configuration
- Minimal working example
- Common setup patterns

### Types and Shapes
📄 **Read:** [references/types-and-shapes.md](references/types-and-shapes.md)
- Linear progress bar
- Circular progress bar
- Semi-circular progress bar
- Shape-specific properties
- When to use each type
- Switching between types

### Progress Modes
📄 **Read:** [references/progress-modes.md](references/progress-modes.md)
- Determinate mode (known progress)
- Indeterminate mode (unknown progress)
- Buffer mode (primary + secondary progress)
- Mode selection guidelines
- Real-world scenarios for each mode

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Sizing and thickness
- Color configuration (progress and track)
- Min, Max, and Value properties
- Radius and InnerRadius
- Segments and segments spacing
- Advanced styling patterns

### Features and Interactions
📄 **Read:** [references/features-and-interactions.md](references/features-and-interactions.md)
- Annotations and labels
- Animation configuration
- Tooltip support
- Event handling (valueChanged, progressComplete)
- Range indicators
- Reactive data binding

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance
- WAI-ARIA attributes
- Keyboard navigation support
- Screen reader considerations
- Testing accessibility
- Best practices

## Quick Start Example

```typescript
import { Component } from '@angular/core';
import { ProgressBarModule } from '@syncfusion/ej2-angular-progressbar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ProgressBarModule],
  template: `
    <div style="margin: 20px;">
      <!-- Linear Progress -->
      <h4>File Download</h4>
      <ejs-progressbar
        [value]="65"
        height="20"
        type="Linear"
        style="width: 300px;">
      </ejs-progressbar>

      <!-- Circular Progress -->
      <h4 style="margin-top: 20px;">Task Completion</h4>
      <ejs-progressbar
        [value]="65"
        type="Circular"
        height="200"
        width="200">
      </ejs-progressbar>

      <!-- Semi-Circular Progress -->
      <h4 style="margin-top: 20px;">System Status</h4>
      <ejs-progressbar
        [value]="65"
        type="SemiCircular"
        height="200"
        width="200">
      </ejs-progressbar>
    </div>
  `
})
export class AppComponent {
}
```

## Common Patterns

### Pattern 1: File Upload Progress
```typescript
export class FileUploadComponent {
  uploadProgress = 0;

  onFileUpload(file: File) {
    // Simulate upload
    const interval = setInterval(() => {
      this.uploadProgress += Math.random() * 30;
      if (this.uploadProgress >= 100) {
        this.uploadProgress = 100;
        clearInterval(interval);
      }
    }, 500);
  }
}
```

### Pattern 2: Loading State with Animation
```typescript
export class LoadingComponent {
  @Input() isLoading = false;
}
```

Template:
```html
<ejs-progressbar
  *ngIf="isLoading"
  [isIndeterminate]="true"
  [height]="4"
  [animation]="{ enable: true, duration: 2000, delay: 0 }">
</ejs-progressbar>
```

### Pattern 3: Multiple Progress States
```typescript
export class DownloadComponent {
  primaryProgress = 35;
  secondaryProgress = 65;
}
```

Template:
```html
<ejs-progressbar
  [value]="primaryProgress"
  [secondaryProgress]="secondaryProgress"
  type="Linear">
</ejs-progressbar>
```

## Key Props Reference

| Property | Type | Purpose |
|----------|------|---------|
| `value` | number | Current progress value (0-100 or custom min/max) |
| `type` | string | Shape: 'Linear', 'Circular', 'SemiCircular' |
| `isIndeterminate` | boolean | Show indeterminate state when true |
| `secondaryProgress` | number | Buffer/secondary progress value |
| `minimum` | number | Minimum value of progress range (default: 0) |
| `maximum` | number | Maximum value of progress range (default: 100) |
| `height` | number\|string | Progress bar height in pixels or percentage |
| `width` | number\|string | Progress bar width in pixels or percentage |
| `trackThickness` | number | Track line thickness |
| `progressThickness` | number | Progress bar thickness |
| `secondaryProgressThickness` | number | Secondary progress thickness |
| `progressColor` | string | Progress bar color (hex, rgb, etc) |
| `secondaryProgressColor` | string | Secondary progress color |
| `trackColor` | string | Track background color |
| `cornerRadius` | string | 'Round' \| 'Square' - Corner style |
| `radius` | number\|string | Outer radius for circular/semi-circular bars |
| `innerRadius` | number\|string | Inner radius for donut-style appearance |
| `segmentCount` | number | Divide progress into N segments |
| `segmentSpacing` | number | Space between segments in pixels |
| `showProgressValue` | boolean | Display progress percentage text |
| `animation` | AnimationModel | Animation config: {enable, duration, delay} |
## Events Reference

The Progress Bar component emits several important events:

| Event | Description | Args |
|-------|-------------|------|
| `valueChanged` | Fired when progress value changes | `IProgressValueEventArgs` |
| `progressCompleted` | Fired when progress reaches 100% | `IProgressValueEventArgs` |
| `textRender` | Fired before rendering progress text | `ITextRenderEventArgs` |

**Note:** Use `(textRender)` event to customize the progress label display format.

## API Reference

A complete API reference for the Syncfusion Angular `ProgressBar` is available in the `references` folder. It includes property types, method anchors, and event arg links that map to the official docs.

Read the API reference: [references/api-reference.md](references/api-reference.md)

## Related Components

- **Skeleton Loader** - For general loading indicators
- **Spinner** - For indeterminate loading states
- **Stepper** - For step-by-step progress
- **Toast** - For progress notifications
