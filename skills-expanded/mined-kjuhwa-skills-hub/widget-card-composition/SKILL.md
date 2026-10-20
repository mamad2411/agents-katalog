---
tags: [design, widget, card, composition]
name: widget-card-composition
description: Dashboard widget composition pattern using a CardWidget chrome wrapper with domain-specific Card* content components, resize tracking, and popover menus
category: design
trigger: When building a dashboard with configurable widget cards that share chrome (title, actions, resize) but differ in content (chart, table, availability)
version: 1.0.0
source_project: lucida-ui
linked_knowledge:
  - widget-high-prop-count-debt
---

# Widget Card Composition Pattern

## Architecture

```
CardWidget (chrome: title, description, popover menu, resize observer)
  └── Card* (content: CardChart | CardTable | CardAvailability | CardTopologyMap | ...)
        └── Visualization (ChartNew | ag-grid | custom SVG | ...)
```

## Steps

1. **Define CardWidget** as the shared wrapper:
   - Props: `titleCard`, `widthCard`, `description`, `isDisplayIconMore`, `resizeItem`
   - Renders: title with tooltip, description, popover menu (copy/edit/delete), children slot
   - Resize: `ResizeObserver` on container, calls `onResizeContainer` callback with new dimensions

2. **Create domain-specific Card*** components:
   - `CardChart`: receives `datas`, `type`, `customChartOptions`, renders ChartNew/ScatterChart
   - `CardTable`: receives grid column defs + row data, renders ag-grid
   - `CardAvailability`: receives availability metrics, renders status indicators
   - Each focuses solely on data → visualization mapping

3. **Compose in dashboard page**:
   ```tsx
   <CardWidget title={widget.title} description={widget.desc}>
     <CardChart datas={widget.chartData} type={widget.chartType} />
   </CardWidget>
   ```

4. **Extension points** (render props for per-instance customization):
   - `renderTooltipIndividual` — custom tooltip renderer
   - `customChartOptions` — override chart options per widget
   - `customRenderNameScatter` — custom scatter point labels

5. **State management**: Recoil atoms for time mode, dispatch callbacks for CRUD operations.

## Pitfalls
- Card* components can accumulate 100+ props — consider splitting into options objects
- Each remote implements its own dashboard grid — consider extracting shared layout logic
