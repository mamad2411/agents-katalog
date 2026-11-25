---
name: polaris-scrollable
description: Shopify Polaris Scrollable component. Use for long-form content container with scrolling. Often for terms, legal disclaimers.
---

# Scrollable

## When to use
Container for long-form content with independent scrolling. Use for terms of service, legal disclaimers, and other lengthy text. Provides visual cues for scrollable content.

## Props
- `children?` ReactNode - Content to display
- `vertical?` boolean - Scroll vertically. Defaults to true.
- `horizontal?` boolean - Scroll horizontally. Defaults to true.
- `shadow?` boolean - Add shadow when scrollable
- `hint?` boolean - Hint content on mount when scrollable
- `focusable?` boolean - Add tabIndex when children aren't focusable
- `scrollbarWidth?` 'none' | 'thin' | 'auto' - Scrollbar width. Defaults to 'thin'.
- `scrollbarGutter?` 'stable' | 'stableboth-edges' - Prevent layout shift
- `onScrolledToBottom?` () => void - Scrolled to bottom callback

## Examples
```jsx
import { Card, Scrollable } from '@shopify/polaris';

// Basic scrollable area
<Card title="Terms of service" sectioned>
  <Scrollable shadow style={{ height: '100px' }} focusable>
    <p>By signing up for the Shopify service...</p>
    <p>Long legal text continues...</p>
  </Scrollable>
</Card>

// Thin scrollbar with gutter
<Scrollable
  scrollbarWidth="thin"
  scrollbarGutter="stable"
  style={{ height: '200px' }}
>
  <p>Content that won't shift when scrollbar appears</p>
</Scrollable>

// Horizontal scrolling
<Scrollable horizontal style={{ width: '300px' }}>
  <table>
    {/* Wide table content */}
  </table>
</Scrollable>

// With bottom callback
<Scrollable
  onScrolledToBottom={() => loadMoreContent()}
  style={{ height: '300px' }}
>
  {items.map(item => <div key={item.id}>{item.content}</div>)}
</Scrollable>
```

## Best practices
- Use for lengthy text (terms, legal, disclaimers)
- Not for instructional/action-oriented text
- Provide visual cues (shadow) when content scrollable
- Set explicit height for scrollable container
- Use for independent scroll regions in modals/panes

## Content guidelines
- Long-form text only
- Terms, legal disclaimers, reference docs
- Not for instructional content
- Follow card content guidelines

## Accessibility
- Focusable allows Tab key entry
- Keyboard users can scroll with arrow keys
- Clear indication of scrollable content
- Shadow provides visual cue

## Related components
- Collapsible (for expand/collapse)
- Card (often wraps scrollable)
