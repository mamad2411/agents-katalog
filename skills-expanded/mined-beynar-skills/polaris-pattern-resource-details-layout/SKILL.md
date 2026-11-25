---
name: polaris-pattern-resource-details-layout
description: Build resource detail pages merchants know—create, view, edit with proven two-column layout and card organization
---

# Resource Details Layout

Lets merchants create, view, and edit resource objects.

## How it helps merchants

- **Full-width page header**: Easy access to actions and navigation, shows these actions represent the entire page
- **Two-column layout**: Primary content (left, 2/3 width) and secondary content (right, 1/3 width)
- **Card-based organization**: Similar content grouped in same card; helps merchants find and focus on specific subtasks

## Use when merchants need to:

- **View and edit resource objects**: Typically paired with resource index layout. Merchants learn the pattern when creating their first product, then use it for orders, customers, and other resources. Use for any individual resource object including specialized ones: discounts, shipping labels, newsletters
- **Create resource objects**: Using resource detail layout when creating new resources teaches merchants what the page looks like and how to edit it later

## Components Used

- Card
- BlockStack
- InlineGrid
- Page

## Layout structure

```jsx
<Page
  backAction={{ content: "Products", url: "/products" }}
  title="Product"
  secondaryActions={[
    { content: "Duplicate", icon: DuplicateIcon },
    { content: "Archive", icon: ArchiveIcon },
    { content: "Delete", icon: DeleteIcon, destructive: true },
  ]}
  pagination={{ hasPrevious: true, hasNext: true }}
>
  <InlineGrid columns={{ xs: 1, md: "2fr 1fr" }} gap="400">
    {/* Primary column (2/3 width) */}
    <BlockStack gap="400">
      <Card roundedAbove="sm">
        <BlockStack gap="400">
          {/* Main content sections */}
        </BlockStack>
      </Card>
      <Card roundedAbove="sm">
        <BlockStack gap="400">
          {/* More main content */}
        </BlockStack>
      </Card>
    </BlockStack>

    {/* Secondary column (1/3 width) */}
    <BlockStack gap={{ xs: "400", md: "200" }}>
      <Card roundedAbove="sm">
        <BlockStack gap="400">
          {/* Supporting info: status, metadata, summaries */}
        </BlockStack>
      </Card>
      <Card roundedAbove="sm">
        <BlockStack gap="400">
          {/* More supporting content */}
        </BlockStack>
      </Card>
    </BlockStack>
  </InlineGrid>
</Page>
```

## Guidelines

- **Always use default width**: Full width tends to waste space and makes the page harder to parse
- **Group similar content**: Place related information in the same card
- **Primary column placement**: Put information that defines the resource object (the "what")
- **Secondary column placement**: Put supporting information like status, metadata, and summaries
- **Order by importance**: Arrange content from most to least important
- **Action ordering**: Place unique page actions at top of action list; typical object actions at bottom

## Responsive behavior

The layout uses responsive columns:
- **Mobile (xs)**: Single column (1 column)
- **Tablet and up (md)**: Two-column "2fr 1fr" ratio (2/3 and 1/3)

## Related patterns

- Pair with Resource index layout pattern for complete resource management experience
- Complements Resource list component
