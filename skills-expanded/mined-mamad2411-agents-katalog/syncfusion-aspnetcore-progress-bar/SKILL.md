---
name: syncfusion-aspnetcore-progress-bar
description: Guide for implementing and customizing the Syncfusion Progress Bar component in ASP.NET Core applications. Use this skill when the user needs to create progress indicators showing task completion, file upload/download status, data loading states, circular progress visualizations, segmented progress tracking, or animated progress bars. Essential for building user-friendly feedback mechanisms that clearly communicate progress to end users.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Progress Bar

The Syncfusion Progress Bar component is a customizable control that visualizes the progress of a task with multiple shape options, animation support, and interactive features. It's ideal for displaying file uploads, downloads, data processing, and any scenario requiring clear visual feedback to users about task completion status.

## When to Use This Skill

Use this skill when you need to:
- Display linear or circular progress indicators
- Show task completion percentages with visual feedback
- Implement file upload/download progress tracking
- Create loading states with determinate or indeterminate modes
- Add secondary progress indicators for buffered operations
- Animate progress transitions smoothly
- Display progress annotations and labels
- Make progress bars accessible with WCAG compliance
- Add tooltips showing progress information
- Customize appearance with colors, thickness, and styling

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete ProgressBar class API documentation
- Property definitions with types and default values
- All available events and callbacks
- Configuration options and usage patterns
- Related settings classes and enumerations
- Official Syncfusion API reference links

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via NuGet package
- ASP.NET Core project setup
- Tag Helper configuration
- Adding stylesheets and scripts
- Basic progress bar initialization
- Rendering the first progress bar

### Types and Shapes
📄 **Read:** [references/types-and-shapes.md](references/types-and-shapes.md)
- Linear progress bars for standard horizontal progress
- Circular progress bars for compact representations
- Semi-circular progress bars for gauge-like displays
- Choosing the appropriate shape for your use case

### Modes and States
📄 **Read:** [references/modes-and-states.md](references/modes-and-states.md)
- Determinate mode for known progress estimation
- Indeterminate mode for unknown progress duration
- Buffer mode for secondary progress visualization
- Transitioning between different states

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Customizing colors and theming
- Adjusting thickness and sizing
- Radius and corner styling
- Segmentation for milestone tracking
- CSS-based customization options
- Advanced styling examples

### Animation and Effects
📄 **Read:** [references/animation-and-effects.md](references/animation-and-effects.md)
- Enabling and configuring animations
- Duration and timing control
- Easing functions and performance
- Smooth state transitions

### Labels and Annotations
📄 **Read:** [references/labels-and-annotations.md](references/labels-and-annotations.md)
- Adding text labels to progress bars
- Displaying progress percentages
- Annotation content for circular progress
- Dynamic label updates
- Positioning and styling labels

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- ValueChanged event handling
- ProgressCompleted event triggering
- Event binding and callbacks
- Integrating with application workflows

### Tooltip Support
📄 **Read:** [references/tooltip-support.md](references/tooltip-support.md)
- Enabling tooltip display
- Tooltip formatting and customization
- Showing tooltips on hover
- Custom tooltip content

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 compliance and standards
- ARIA attributes and roles
- Keyboard navigation support
- Screen reader compatibility
- Testing and validation

## Quick Start Example

Here's a minimal example of creating a basic linear progress bar in ASP.NET Core:

```cshtml
<!-- In your Razor page or layout -->
<ejs-progressbar id="linearProgress" 
                  type="Linear" 
                  value="50" 
                  minimum="0" 
                  maximum="100">
</ejs-progressbar>
```

This creates a progress bar showing 50% completion. The default type is Linear, with a range from 0 (minimum) to 100 (maximum).

## Common Patterns

### Pattern 1: File Upload Progress Tracking
```cshtml
<ejs-progressbar id="uploadProgress" 
                  type="Linear" 
                  value="0" 
                  minimum="0" 
                  maximum="100">
    <e-progressbar-animation enable="true" 
                              duration="1000" 
                              delay="0">
    </e-progressbar-animation>
</ejs-progressbar>

<button id="uploadBtn" type="button">Start Upload</button>
<script>
document.getElementById('uploadBtn').addEventListener('click', function() {
    var progressBar = document.getElementById('uploadProgress').ej2_instances[0];
    var interval = setInterval(function() {
        var currentValue = progressBar.value;
        if (currentValue < 100) {
            progressBar.value += 10;
        } else {
            clearInterval(interval);
        }
    }, 500);
});
</script>
```

### Pattern 2: Task Completion with Circular Progress
```cshtml
<ejs-progressbar id="taskProgress" 
                  type="Circular" 
                  value="75" 
                  minimum="0" 
                  maximum="100"
                  showProgressValue="true">
</ejs-progressbar>
```

### Pattern 3: Indeterminate Loading State
```cshtml
<ejs-progressbar id="loadingProgress" 
                  type="Linear" 
                  value="30"
                  isIndeterminate="true">
</ejs-progressbar>
```

Use this when the task duration is unknown but the application is actively processing data.

### Pattern 4: Segmented Progress for Multiple Steps
```cshtml
<ejs-progressbar id="stepsProgress" 
                  type="Linear" 
                  value="60" 
                  segmentCount="5"
                  minimum="0" 
                  maximum="100">
</ejs-progressbar>
```

Divides the progress bar into 5 segments, useful for multi-step processes.

## Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `type` | string | "Linear" | Shape of the progress bar: Linear, Circular, SemiCircular |
| `value` | number | 0 | Current progress value |
| `minimum` | number | 0 | Minimum range value |
| `maximum` | number | 100 | Maximum range value |
| `isIndeterminate` | boolean | false | Show indeterminate loading state |
| `segmentCount` | number | 1 | Divide progress bar into segments |
| `showProgressValue` | boolean | false | Display percentage label |
| `trackThickness` | number | 0 | Track bar thickness in pixels |
| `progressThickness` | number | 0 | Progress bar thickness in pixels |
| `cornerRadius` | string | "Auto" | Corner radius styling |
| `secondaryProgress` | number | NaN | Secondary progress value for buffer mode |
| `trackColor` | string | null | Track (background) color |
| `progressColor` | string | null | Primary progress fill color |
| `secondaryProgressColor` | string | "" | Secondary/buffer progress color |

## Key Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| `ValueChanged` | When progress value changes | Update UI, track progress milestones |
| `ProgressCompleted` | When value reaches maximum | Trigger next action, show completion message |

---

For detailed implementation guidance, refer to the reference files above. Each provides specific instructions, code examples, and best practices for its topic area.
