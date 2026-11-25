---
name: polaris-pattern-resource-index-layout
description: Master resource lists—organize and manage products, orders, customers with proven index layout and filtering
---

# Resource Index Layout

Lets merchants organize and take action on resource objects.

## How it helps merchants

- **Single-column hierarchy**: Clear top-to-bottom hierarchy of tasks; horizontal space for resource data
- **Page actions**: Title and actions affecting the entire index at the top
- **Filter controls**: Filters, sorting, and multi-select actions affecting the list
- **Resource list**: Individual resource objects merchants want to view or manage

## Use when merchants need to:

- **Overview and manage resources**: Resource objects (products, orders, customers) are at the heart of merchants' businesses. While resource types differ, they share general activities: adding, finding, taking action. Use this pattern when merchants need to organize objects and carry out these activities. Example: Products page

## Components Used

- Card
- Badge
- ChoiceList
- IndexFilter
- IndexTable
- Page

## Page structure

```jsx
<Page
  title="Products"
  primaryAction={{ content: "Add product" }}
  secondaryActions={[
    { content: "Export", accessibilityLabel: "Export product list" },
    { content: "Import", accessibilityLabel: "Import product list" },
  ]}
>
  <Card padding="0">
    {/* Filter section */}
    <IndexFilters
      sortOptions={sortOptions}
      sortSelected={sortSelected}
      queryValue={queryValue}
      queryPlaceholder="Searching in all"
      onQueryChange={handleFiltersQueryChange}
      onSort={setSortSelected}
      primaryAction={primaryAction}
      tabs={tabs}
      selected={selected}
      filters={filters}
      appliedFilters={appliedFilters}
      onClearAll={handleFiltersClearAll}
    />

    {/* Table/list of resources */}
    <IndexTable
      resourceName={{ singular: "product", plural: "products" }}
      itemCount={products.length}
      selectedItemsCount={allResourcesSelected ? "All" : selectedResources.length}
      onSelectionChange={handleSelectionChange}
      sortable={[false, true, true, true, true, true, true]}
      headings={[
        { title: "" },
        { title: "Product" },
        { title: "Price", alignment: "end" },
        { title: "Status" },
        { title: "Inventory" },
        { title: "Type" },
        { title: "Vendor" },
      ]}
    >
      {/* Row markup */}
    </IndexTable>
  </Card>
</Page>
```

## Key patterns

### Tabs for views
Users can create, rename, duplicate, and delete custom views to organize their work.

### Filters
- Multiple filter types (status, type, search query)
- Apply filters that narrow the list
- Show clear applied filter chips with remove options
- "Clear all" action to reset all filters

### Sorting
- Multiple sort options with ascending/descending directions
- Label each sort option clearly (e.g., "Product", "Status", "Vendor")

### Selection
- Multi-select capability for batch actions
- Select all / deselect all functionality
- Show count of selected items or "All" for select all

### Primary action
- Add/create resource button in top right
- Use "Save as" for the first view (unsaved state) or "Save" for existing views

## Guidelines

- **Use resource type as page title** (e.g., "Products")
- **Always use primary action** in top right for resource creation (remove if no functionality)
- **Set page width to normal** if the index doesn't need full width
- **Show empty state** when resource index is empty (use Empty state component)

## Responsive behavior

Single-column layout with full-width resources ensures horizontal space for data display. Table/list adapts to screen size.

## Related patterns

- Pair with Resource detail layout pattern for complete resource management experience
- Use Empty state component when the resource index is empty
