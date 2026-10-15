---
name: syncfusion-aspnetcore-timeline
description: Display temporal sequences with Syncfusion Timeline component. Supports vertical/horizontal orientations, flexible item alignment (Before/After/Alternate), rich templating for content and dots, content positioning strategies, and comprehensive event handling for item rendering lifecycle. Essential for chronological visualization in ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Skill: Syncfusion Timeline Component

## Overview

The Timeline component presents a sequence of events or activities arranged chronologically. It enables developers to visualize temporal relationships and progressions in a configurable layout. Timeline supports both vertical and horizontal orientations, flexible content alignment strategies (Before, After, Alternate, AlternateReverse), and rich templating capabilities. It is commonly used for displaying project milestones, process flows, historical events, or any chronological progression in web applications.

## Functional Scope

**Component Responsibility (Timeline owns):**
- Rendering the visual timeline structure (dots, connectors, timeline line)
- Managing item layout according to specified orientation and alignment
- Handling directional support (RTL mode)
- Triggering lifecycle events during rendering and initialization
- Applying CSS-based customization to visual elements
- Parsing and rendering templated content for items

**Developer Responsibility (You control):**
- Preparing item data with content and configuration properties
- Designing content templates (HTML structure, formatting)
- Styling dots, connectors, and timeline elements via CSS classes
- Handling events (created, beforeItemRender) for custom behavior
- Managing dynamic data updates
- Ensuring accessibility attributes on templated content
- Defining application-specific logic triggered by events

**What Timeline Does NOT Handle:**
- Animation or transition effects between states (CSS responsibility)
- Responsive layout breakpoints (CSS media queries required)
- Data persistence or state management across page reloads (application layer)
- Infinite scrolling or virtualization for very large datasets (100,000+ items)
- Accessibility markup generation (you must ensure proper ARIA labels)
- Filtering or sorting of items (pre-process data before passing to Timeline)

## How It Works

**Rendering Flow:**
1. **Initialization**: Timeline receives `items` array and configuration properties (align, orientation, reverse, etc.)
2. **Layout Calculation**: Component determines item positioning based on orientation (Vertical/Horizontal) and alignment (Before/After/Alternate/AlternateReverse)
3. **Event Firing**: `created` event fires when component rendering is complete
4. **Item Rendering**: For each item, `beforeItemRender` event fires before the item DOM element is created (allows modification of item properties before rendering)
5. **DOM Construction**: Timeline builds the visual structure:
   - Timeline line/connector connecting items
   - Dot elements at each item position
   - Content containers positioned according to alignment
   - Opposite content positioned opposite to main content
6. **CSS Application**: All CSS classes specified in `cssClass`, item-level `cssClass`, and dot-level `dotCss` are applied

**Orientation Impact:**
- **Vertical** (default): Items stack top-to-bottom. Before/After alignment controls left/right positioning of content.
- **Horizontal**: Items arrange left-to-right. Before/After alignment controls top/bottom positioning of content.

**Alignment Behavior:**
- **Before**: Content on one side, oppositeContent on the other (orientation-dependent)
- **After**: Content swapped to opposite side from Before
- **Alternate**: Items alternate sides regardless of orientation
- **AlternateReverse**: Items alternate sides in reverse order

**Data Binding:**
- Items are rendered in the order they appear in the `items` array
- `reverse` property reverses the display order without modifying source data
- Content can be static strings or dynamically generated via functions with itemIndex context

## Configuration and Usage


### Required Configuration

```cshtml
@using Syncfusion.EJ2.Layouts;

<ejs-timeline id="timeline">
    <e-timeline-items>
        <e-timeline-item content="Initial Release"></e-timeline-item>
        <e-timeline-item content="Version 2.0"></e-timeline-item>
        <e-timeline-item content="Latest Update"></e-timeline-item>
    </e-timeline-items>
</ejs-timeline>
```


### Optional Configuration

```cshtml
<ejs-timeline id="timeline" align="Alternate" orientation="Horizontal" reverse="false" enableRtl="false" enablePersistence="false" cssClass="custom-timeline" locale="en-US">
    <e-timeline-items>
        <e-timeline-item content="Phase 1" oppositeContent="Q1 2024" dotCss="e-icons e-check" cssClass="phase-active"></e-timeline-item>
        <e-timeline-item content="Phase 2" oppositeContent="Q2 2024" dotCss="e-icons e-pending"></e-timeline-item>
    </e-timeline-items>
</ejs-timeline>
```

### Defaults

| Property | Default Value | Behavior |
|----------|---------------|----------|
| `align` | `TimelineAlign.After` | Content placed bottom/right by default |
| `orientation` | `TimelineOrientation.Vertical` | Items stack vertically |
| `reverse` | `false` | Items display in source order |
| `enableRtl` | `false` | Left-to-right text direction |
| `enablePersistence` | `false` | No state saved between sessions |
| `locale` | `'en-US'` | English localization |
| `items` | `[]` (empty) | No items rendered if empty |

## Key APIs

### Timeline Component Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `items` | `TimelineItemModel[]` | Array of timeline items to render | `[]` |
| `align` | `TimelineAlign` enum | Content alignment strategy (Before/After/Alternate/AlternateReverse) | `After` |
| `orientation` | `TimelineOrientation` enum | Display direction (Vertical/Horizontal) | `Vertical` |
| `reverse` | `boolean` | Reverse item display order | `false` |
| `template` | `string` | HTML template selector for custom item rendering | N/A |
| `enableRtl` | `boolean` | Enable right-to-left text direction | `false` |
| `enablePersistence` | `boolean` | Persist state between page reloads | `false` |
| `cssClass` | `string` | CSS class(es) applied to Timeline container | `''` |
| `locale` | `string` | Culture/localization identifier | `'en-US'` |

### TimelineItem Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `content` | `string` \| `Function` | Main item text or template (receives itemIndex) | `''` |
| `oppositeContent` | `string` \| `Function` | Secondary content opposite main content (receives itemIndex) | `''` |
| `dotCss` | `string` | CSS class(es) for dot element (icons, images, styling) | `''` |
| `disabled` | `boolean` | Disable this item visually/interactively | `false` |
| `cssClass` | `string` | CSS class(es) for this item container | `''` |

### Events

| Event | Trigger Point | Use Case |
|-------|--------------|----------|
| `created` | After component rendering completes | Initialize custom behaviors, access rendered elements |
| `beforeItemRender` | Before each item's DOM element is created | Modify item properties conditionally, apply dynamic styling |

**Event Arguments:**
- `created`: No custom properties
- `beforeItemRender`: Provides `element` (HTMLElement), `index` (number), `name` ('beforeItemRender')

### Alignment Enum (TimelineAlign)

```csharp
public enum TimelineAlign
{
    Before,           // Content on first side (left/top depending on orientation)
    After,            // Content on second side (right/bottom) — DEFAULT
    Alternate,        // Items alternate sides in order
    AlternateReverse  // Items alternate sides in reverse order
}
```

### Orientation Enum (TimelineOrientation)

```csharp
public enum TimelineOrientation
{
    Vertical,        // Items stack top-to-bottom (default)
    Horizontal       // Items arrange left-to-right
}
```


## Example

**Scenario**: Display a product release timeline with milestone dates and status indicators.

```cshtml
@using Syncfusion.EJ2.Layouts;

<ejs-timeline id="release-timeline" align="Alternate" orientation="Vertical" cssClass="release-timeline">
    <e-timeline-items>
        <e-timeline-item content="Alpha Release" oppositeContent="January 2024" dotCss="e-icons e-info"></e-timeline-item>
        <e-timeline-item content="Beta Release" oppositeContent="March 2024" dotCss="e-icons e-check"></e-timeline-item>
        <e-timeline-item content="Production Release" oppositeContent="June 2024" dotCss="e-icons e-star"></e-timeline-item>
    </e-timeline-items>
</ejs-timeline>
```

**Template Example:**

```cshtml
@using Syncfusion.EJ2.Layouts;

<div class="container" style="height: 350px">
    <ejs-timeline id="timeline">
        <e-timeline-items>
            <e-timeline-item content="#content-template"></e-timeline-item>
            <e-timeline-item content="#content-template"></e-timeline-item>
            <e-timeline-item content="#content-template"></e-timeline-item>
            <e-timeline-item content="Out for Delivery"></e-timeline-item>
        </e-timeline-items>
    </ejs-timeline>
</div>

<script id="content-template" type="text/x-jsrender">
    <div class="content-container">
        <div class="title">
            ${if(itemIndex==0)} Shipped
            ${else if(itemIndex==1)} Departed
            ${else if(itemIndex==2)} Arrived
            ${/if}
        </div>
        <span class="description">
            ${if(itemIndex==0)} Package details received
            ${else if(itemIndex==1)} In-transit
            ${else if(itemIndex==2)} Package arrived at nearest hub
            ${/if}
        </span>
        <div class="info">
            ${if(itemIndex==0)} - Awaiting dispatch
            ${else if(itemIndex==1)} (International warehouse)
            ${else if(itemIndex==2)} (New york - US)
            ${/if}
        </div>
    </div>
</script>

<style>
    .content-container {
        position: relative;
        width: 180px;
        padding: 10px;
        margin-left: 5px;
        box-shadow: rgba(9, 30, 66, 0.25) 0px 4px 8px -2px, rgba(9, 30, 66, 0.08) 0px 0px 0px 1px;
        background-color: ghostwhite;
    }

    .content-container::before {
        content: '';
        position: absolute;
        left: -8px;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        border-top: 5px solid transparent;
        border-bottom: 5px solid transparent;
        border-right: 8px solid silver;
    }

    .content-container .title {
        font-size: 16px;
    }
    .content-container .description {
        color: #999999;
        font-size: 12px;
    }
    .content-container .info {
        color: #999999;
        font-size: 10px;
    }
</style>

## Edge Cases and Constraints

1. **Empty Items Array**: Timeline renders no visible content if `items` is empty or null. Component container still renders (empty HTML). Always validate data before passing to Timeline.

2. **Very Large Datasets (1000+ items)**: Timeline renders all items in DOM without virtualization. Performance degrades linearly with item count. For large datasets, implement pagination or filter items client-side before binding.

3. **Template Functions with Side Effects**: If `content` or `oppositeContent` are function-type properties with side effects (logging, API calls), functions execute during rendering. Ensure functions are idempotent and fast (no async operations).

4. **RTL (enableRtl=true) with Horizontal Orientation**: Timeline correctly reverses layout direction. Test content alignment thoroughly—Alternate alignment behavior reverses in RTL mode.

5. **Disabled Items Styling**: Setting `disabled=true` does not automatically style items visually. You must define CSS for `.e-disabled` or custom class to show disabled state (e.g., opacity, strikethrough).

6. **Dot CSS Class Conflicts**: If `dotCss` specifies both icon class (e.g., `e-icons e-check`) and custom class, ensure no CSS conflicts. Icon fonts may fail to load if CDN is unreachable.

7. **Dynamic Content Updates**: If you modify `items` array after rendering, the Timeline does not automatically refresh. You must re-instantiate or call update methods. Changes to item objects alone do not trigger re-render.

8. **Accessibility with Templates**: Custom templates (using `template` property) are developer-controlled. Component does not auto-generate ARIA labels. You must include `role`, `aria-label`, `aria-describedby` attributes in templates.

9. **Locale Fallback**: If specified `locale` is not registered, Timeline falls back to `en-US`. Ensure locale data is loaded before Timeline initialization.

10. **Reverse Property Logic**: `reverse=true` reverses visual order only; source `items` array order is unchanged. This affects user perception of chronological flow but does not modify underlying data.

## Testing Checklist

- [ ] **Visual Rendering**: All items render with correct content, opposite content, and dots in DOM
- [ ] **Orientation Switch**: Timeline correctly renders in both Vertical and Horizontal modes
- [ ] **Alignment Modes**: All four alignment modes (Before/After/Alternate/AlternateReverse) position content correctly
- [ ] **RTL Mode**: With `enableRtl=true`, content direction reverses and layout mirroring is correct
- [ ] **Reverse Property**: With `reverse=true`, items display in reverse visual order (verify against items array)
- [ ] **Empty Dataset**: Timeline handles empty or null `items` without JavaScript errors
- [ ] **Large Dataset Performance**: Timeline renders 500+ items without browser freezing (baseline test)
- [ ] **Event Firing**: `created` event fires once after rendering; `beforeItemRender` fires for each item
- [ ] **CSS Application**: Custom CSS classes (component-level `cssClass` and item-level `cssClass`) apply correctly
- [ ] **Dot Customization**: Dot CSS classes (icons, images, text) render without font failures
- [ ] **Template Rendering**: Custom templates (if using `template` property) render content without script errors
- [ ] **Accessibility (Keyboard)**: Timeline structure is keyboard-navigable; focus management works (if interactive)
- [ ] **Accessibility (Screen Reader)**: Screen reader announces items in logical order; ARIA labels present (if configured)
- [ ] **Disabled Items**: Items with `disabled=true` render but are visually distinguishable (if styled)
- [ ] **Persistence**: With `enablePersistence=true`, state is restored on page reload (verify localStorage)
- [ ] **Dynamic Updates**: Modifying `items` after render requires manual refresh; verify no auto-refresh (expected behavior)
- [ ] **Locale Switching**: Changing `locale` property updates localized strings correctly
- [ ] **Browser Compatibility**: Timeline renders correctly in Chrome, Firefox, Safari, Edge (latest versions)

## Best Practices

1. **Pre-process Data Before Binding**: Sort, filter, and validate item data before passing to Timeline. Timeline renders items in order received—apply business logic (sorting by date, filtering by status) at the data layer, not in the component.

2. **Use Opposite Content Strategically**: Reserve opposite content for supplementary information (dates, metadata, statuses). Keep opposite content brief; use main content for primary narrative. This prevents visual clutter and maintains chronological clarity.

3. **Choose Alignment Based on Content Volume**: Use `Before` or `After` for simple, short content. Use `Alternate` when content is substantial and you need to balance visual weight. `AlternateReverse` is rarely needed; use only for specific design requirements (e.g., reverse chronological with intentional mirroring).

4. **Customize Dots with Icons, Not Text**: Leverage `dotCss` with icon fonts (Material Icons, Syncfusion icons) for visual status indicators. Avoid long text in dots; instead, encode meaning via icon and color. Icons are faster to recognize than text.

5. **Style Disabled Items Explicitly**: If using `disabled=true` for historical or read-only items, define clear CSS to visually differentiate them (e.g., reduced opacity, grayscale, strikethrough). Users must immediately recognize disabled state without hovering.

6. **Leverage Templates for Complex Layouts**: For items requiring rich HTML (images, nested lists, interactive elements), use the `template` property instead of string content. Templates offer full control; ensure templates remain self-contained and do not create accessibility barriers.

7. **Handle Accessibility in Custom Templates**: If using custom templates, manually include `role="article"`, `aria-label`, and `aria-describedby` attributes. Test with screen readers (NVDA, JAWS) to ensure content is announced in expected order and context is clear.

8. **Monitor Performance with Large Datasets**: If binding 500+ items, profile rendering time in browser DevTools. If rendering takes >500ms, consider pagination, lazy loading, or filtering. Inform users of rendering delay with a loading indicator.

9. **Test RTL Rendering If Supporting Right-to-Left Languages**: Set `enableRtl=true` and verify all alignment modes, dot positioning, and content placement mirror correctly. Test on actual right-to-left content (Arabic, Hebrew, Persian) to catch subtle layout issues.

10. **Validate Event Handlers Are Idempotent**: If `beforeItemRender` handler modifies component state, ensure modifications are safe to repeat. Handlers may fire multiple times if component re-renders; avoid side effects that compound.

