---
name: syncfusion-winforms-bullet-graph
description: Implementation guide for Syncfusion Windows Forms Bullet Graph control for compact data visualization. Use this when working with bullet graphs, performance indicators, KPI visualization, comparative measures, or qualitative ranges in WinForms. This skill covers dashboard gauges, target vs actual comparisons, and performance range visualization in Windows Forms desktop applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms Bullet Graph

Expert guidance for implementing the Syncfusion Bullet Graph control in Windows Forms applications. The Bullet Graph is a compact, space-efficient data visualization control designed for dashboards, replacing traditional gauges and meters. It displays a primary measure (featured measure) compared to a target (comparative measure) within qualitative performance ranges.

## When to Use This Skill

Use this skill when you need to:
- Display KPIs (Key Performance Indicators) in a compact dashboard layout
- Show current performance against targets (actual vs goal)
- Visualize data with performance ranges (poor, satisfactory, good)
- Create revenue analysis or expense tracking visualizations
- Replace traditional gauges and meters with space-efficient alternatives
- Compare actual values to benchmarks or targets
- Build executive dashboards requiring high information density
- Implement year-to-date (YTD) metrics visualization

## Component Overview

The Bullet Graph consists of:
- **Featured Measure**: Primary data bar showing the current value (e.g., actual revenue)
- **Comparative Measure**: Target line showing the goal or benchmark (e.g., target revenue)
- **Qualitative Ranges**: Background bands indicating performance levels (e.g., poor, satisfactory, good)
- **Quantitative Scale**: Axis with ticks and labels showing numeric values
- **Caption**: Label describing what the graph represents

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet package installation
- Creating Bullet Graph programmatically in code
- Using Syncfusion Reference Manager for Visual Studio integration
- Basic initialization and first working example
- Required namespaces and assemblies

### Measures (Featured and Comparative)
📄 **Read:** [references/measures.md](references/measures.md)
- Featured measure: primary data bar configuration
- Featured measure customization (color, thickness)
- Comparative measure: target line configuration
- Comparative measure customization (symbol color, thickness)
- Visual hierarchy and positioning

### Qualitative Ranges
📄 **Read:** [references/qualitative-ranges.md](references/qualitative-ranges.md)
- Adding and configuring qualitative ranges collection
- Range properties (RangeEnd, RangeStroke, RangeCaption)
- Customizing range size and opacity
- Binding range colors to ticks and labels
- Performance indicator patterns (good, satisfactory, poor)

### Scale Ticks
📄 **Read:** [references/scale-and-ticks.md](references/scale-and-ticks.md)
- Major ticks and minor ticks configuration
- Tick customization (stroke, size, thickness)
- Tick positioning (Above, Below, Cross)
- Interval and MinorTicksPerInterval settings
- Visual customization examples

### Scale Labels
📄 **Read:** [references/scale-labels.md](references/scale-labels.md)
- Label properties and numeric values
- Label customization (font size, color, offset)
- Label formatting patterns (LabelFormat)
- Label positioning (Above, Below)

### Layout and Orientation
📄 **Read:** [references/layout-and-orientation.md](references/layout-and-orientation.md)
- Orientation (Horizontal, Vertical)
- Flow direction (Forward, Backward)
- Caption and caption positioning (Near, Far)
- Quantitative scale length customization
- Layout properties and docking

## Quick Start Example

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.BulletGraph;

namespace BulletGraphDemo
{
    public class MainForm : Form
    {
        public MainForm()
        {
            // Create Bullet Graph
            BulletGraph bullet = new BulletGraph();
            bullet.Dock = DockStyle.Fill;
            
            // Set orientation and flow
            bullet.FlowDirection = BulletGraphFlowDirection.Forward;
            bullet.Orientation = Orientation.Horizontal;
            
            // Configure measures
            bullet.FeaturedMeasure = 4.5;      // Actual value
            bullet.ComparativeMeasure = 7;     // Target value
            
            // Configure scale
            bullet.Minimum = 0;
            bullet.Maximum = 10;
            bullet.Interval = 2;
            bullet.MinorTicksPerInterval = 3;
            
            // Add qualitative ranges
            bullet.QualitativeRanges.Add(new QualitativeRange() 
            { 
                RangeEnd = 4, 
                RangeCaption = "Bad", 
                RangeStroke = Color.Red 
            });
            
            bullet.QualitativeRanges.Add(new QualitativeRange() 
            { 
                RangeEnd = 7, 
                RangeCaption = "Satisfactory", 
                RangeStroke = Color.Yellow 
            });
            
            bullet.QualitativeRanges.Add(new QualitativeRange() 
            { 
                RangeEnd = 10, 
                RangeCaption = "Good", 
                RangeStroke = Color.Green 
            });
            
            // Add caption
            bullet.Caption = "Revenue YTD\n$ in thousands";
            
            // Add to form
            this.Controls.Add(bullet);
        }
    }
}
```

## Common Patterns

### Revenue Tracking Dashboard

```csharp
BulletGraph revenueGraph = new BulletGraph();
revenueGraph.Dock = DockStyle.Top;
revenueGraph.Height = 100;
revenueGraph.Caption = "Revenue YTD\n$ in thousands";
revenueGraph.CaptionPosition = BulletGraphCaptionPosition.Near;

// Set actual vs target
revenueGraph.FeaturedMeasure = 275;     // Actual: $275k
revenueGraph.ComparativeMeasure = 300;  // Target: $300k

// Configure scale
revenueGraph.Minimum = 0;
revenueGraph.Maximum = 400;
revenueGraph.Interval = 100;
revenueGraph.LabelFormat = "$#0K";

// Performance ranges
revenueGraph.QualitativeRanges.Add(new QualitativeRange() 
    { RangeEnd = 200, RangeStroke = Color.FromArgb(255, 200, 200) });  // Poor
revenueGraph.QualitativeRanges.Add(new QualitativeRange() 
    { RangeEnd = 300, RangeStroke = Color.FromArgb(255, 255, 200) });  // Fair
revenueGraph.QualitativeRanges.Add(new QualitativeRange() 
    { RangeEnd = 400, RangeStroke = Color.FromArgb(200, 255, 200) });  // Good
```

### Vertical KPI Display

```csharp
BulletGraph kpiGraph = new BulletGraph();
kpiGraph.Orientation = Orientation.Vertical;
kpiGraph.FlowDirection = BulletGraphFlowDirection.Backward;
kpiGraph.Dock = DockStyle.Left;
kpiGraph.Width = 150;

kpiGraph.Caption = "Customer\nSatisfaction";
kpiGraph.CaptionPosition = BulletGraphCaptionPosition.Far;

kpiGraph.FeaturedMeasure = 8.5;   // Current score
kpiGraph.ComparativeMeasure = 9;  // Target score

kpiGraph.Minimum = 0;
kpiGraph.Maximum = 10;
kpiGraph.Interval = 2;
```

### Styled Bullet Graph with Custom Colors

```csharp
BulletGraph styledGraph = new BulletGraph();

// Customize featured measure bar
styledGraph.FeaturedMeasure = 65;
styledGraph.FeaturedMeasureBarStroke = Color.DarkBlue;
styledGraph.FeaturedMeasureBarStrokeThickness = 8;

// Customize comparative measure
styledGraph.ComparativeMeasure = 80;
styledGraph.ComparativeMeasureSymbolStroke = Color.Red;
styledGraph.ComparativeMeasureSymbolStrokeThickness = 3;

// Customize ticks and labels
styledGraph.MajorTickStroke = Color.Black;
styledGraph.MajorTickSize = 15;
styledGraph.MinorTickStroke = Color.Gray;
styledGraph.MinorTickSize = 10;
styledGraph.LabelFontSize = 12;
styledGraph.LabelStroke = Color.Black;
```

### Multiple Bullet Graphs in Dashboard

```csharp
// Stack multiple bullet graphs vertically
BulletGraph[] metrics = new BulletGraph[3];
string[] captions = { "Sales\n$ in thousands", "Profit\n$ in thousands", "Customers\ncount" };
double[] actuals = { 275, 45, 1250 };
double[] targets = { 300, 50, 1500 };

for (int i = 0; i < 3; i++)
{
    metrics[i] = new BulletGraph();
    metrics[i].Dock = DockStyle.Top;
    metrics[i].Height = 80;
    metrics[i].Caption = captions[i];
    metrics[i].FeaturedMeasure = actuals[i];
    metrics[i].ComparativeMeasure = targets[i];
    
    // Add standard ranges
    metrics[i].QualitativeRanges.Add(new QualitativeRange() 
        { RangeEnd = targets[i] * 0.6, RangeStroke = Color.LightCoral });
    metrics[i].QualitativeRanges.Add(new QualitativeRange() 
        { RangeEnd = targets[i] * 0.9, RangeStroke = Color.LightYellow });
    metrics[i].QualitativeRanges.Add(new QualitativeRange() 
        { RangeEnd = targets[i] * 1.2, RangeStroke = Color.LightGreen });
    
    this.Controls.Add(metrics[i]);
}
```

## Key Properties Reference

### Measures
| Property | Type | Description |
|----------|------|-------------|
| `FeaturedMeasure` | double | Primary value to display (current/actual) |
| `FeaturedMeasureBarStroke` | Color | Color of the featured measure bar |
| `FeaturedMeasureBarStrokeThickness` | int | Thickness of the featured measure bar |
| `ComparativeMeasure` | double | Target or benchmark value |
| `ComparativeMeasureSymbolStroke` | Color | Color of the comparative measure line |
| `ComparativeMeasureSymbolStrokeThickness` | int | Thickness of the comparative measure line |

### Scale
| Property | Type | Description |
|----------|------|-------------|
| `Minimum` | double | Starting value of the scale |
| `Maximum` | double | Ending value of the scale |
| `Interval` | double | Spacing between major ticks |
| `MinorTicksPerInterval` | int | Number of minor ticks between major ticks |

### Layout
| Property | Type | Description |
|----------|------|-------------|
| `Orientation` | Orientation | Horizontal or Vertical display |
| `FlowDirection` | BulletGraphFlowDirection | Forward or Backward flow |
| `Caption` | string | Label describing the metric |
| `CaptionPosition` | BulletGraphCaptionPosition | Near or Far caption placement |

### Ranges
| Property | Type | Description |
|----------|------|-------------|
| `QualitativeRanges` | QualitativeRangeCollection  | Collection of qualitative range objects |
| `QualitativeRangesSize` | int | Width/height of the range bands |

## Common Use Cases

1. **Executive Dashboards**: Display multiple KPIs in compact space
2. **Financial Reports**: Revenue, profit, and expense tracking
3. **Sales Performance**: Quota attainment visualization
4. **Customer Metrics**: Satisfaction scores, retention rates
5. **Operational KPIs**: Efficiency, throughput, quality metrics
6. **Project Management**: Budget vs actual, schedule performance
7. **Manufacturing**: Production targets, defect rates, utilization