---
name: polaris-page
description: Shopify Polaris Page component. Use as outer page wrapper with title, actions, pagination, breadcrumbs for detail pages and lists.
---

# Page

## When to use
Use as the main page wrapper. Provides title, page actions (primary/secondary), pagination, and breadcrumbs. Essential for detail pages and resource lists.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | Page content |
| title | string | - | Large page title |
| subtitle | string | - | Subtitle in regular type |
| titleMetadata | ReactNode | - | Status badge/info after title |
| titleHidden | boolean | false | Visually hide title (screenreaders see it) |
| compactTitle | boolean | false | Remove spacing between title/subtitle |
| fullWidth | boolean | false | Remove max-width constraint |
| narrowWidth | boolean | false | Smaller max-width for single column |
| primaryAction | any | - | Main page action button |
| secondaryActions | any[] | - | Additional page actions |
| actionGroups | MenuGroupDescriptor[] | - | Grouped secondary actions |
| pagination | PaginationProps | - | Previous/next object pagination |
| backAction | LinkAction \| CallbackAction | - | Back navigation link |

## Examples

```jsx
import { Page, Layout, Card, Button, Badge } from '@shopify/polaris';

// Basic page with title
<Page title="Products">
  <Layout>
    <Layout.Section>
      <Card>
        <Box padding="400">
          <Text>Product list content</Text>
        </Box>
      </Card>
    </Layout.Section>
  </Layout>
</Page>

// Product detail with status badge
<Page
  title="3/4 inch Leather pet collar"
  titleMetadata={<Badge tone="success">Paid</Badge>}
  primaryAction={{
    content: 'Save',
  }}
  secondaryActions={[
    {
      content: 'Duplicate',
      onAction: () => alert('Duplicated'),
    },
    {
      content: 'View on store',
      onAction: () => alert('Viewing'),
    },
  ]}
>
  <Layout>
    <Layout.Section>
      <Card>Product details</Card>
    </Layout.Section>
    <Layout.Section secondary>
      <Card>Related info</Card>
    </Layout.Section>
  </Layout>
</Page>

// With pagination
<Page
  title="Order #1001"
  pagination={{
    hasPrevious: true,
    hasNext: true,
  }}
  primaryAction={{
    content: 'Fulfill',
  }}
>
  <Card>Order content</Card>
</Page>

// With action groups
<Page
  title="Inventory"
  primaryAction={{
    content: 'Add inventory',
  }}
  actionGroups={[
    {
      title: 'Import',
      actions: [
        { content: 'From CSV', onAction: () => {} },
        { content: 'From supplier', onAction: () => {} },
      ],
    },
    {
      title: 'Export',
      actions: [
        { content: 'Export as CSV', onAction: () => {} },
      ],
    },
  ]}
>
  <Card>Inventory list</Card>
</Page>

// Full width
<Page title="Dashboard" fullWidth>
  <Grid>
    <Grid.Cell columnSpan={{ xs: 12, md: 6 }}>
      <Card>Widget 1</Card>
    </Grid.Cell>
    <Grid.Cell columnSpan={{ xs: 12, md: 6 }}>
      <Card>Widget 2</Card>
    </Grid.Cell>
  </Grid>
</Page>

// Narrow for single column
<Page title="Settings" narrowWidth>
  <Layout>
    <Layout.Section>
      <Card>Single column content</Card>
    </Layout.Section>
  </Layout>
</Page>

// With subtitle and compact
<Page
  title="Orders"
  subtitle="Manage customer orders"
  compactTitle
  primaryAction={{
    content: 'Create order',
  }}
>
  <Card>Orders content</Card>
</Page>

// Hidden title (for custom header)
<Page titleHidden pageReadyAccessibilityLabel="Products page">
  <Card>Content with custom header elsewhere</Card>
</Page>
```

## Best practices

- Always provide meaningful page title
- Use breadcrumbs for navigation (deprecated - use App Bridge)
- Provide primary action if page has main task
- Limit to 1 primary action
- Use secondary actions for related tasks
- Include pagination for detail pages
- Group similar secondary actions
- Center page width appropriately
- Consider mobile layout

## Content guidelines

**Title**:
- Describe page in few words
- Plural noun for lists (Orders, Products)
- Not truncated
- Follow heading guidelines

**Breadcrumbs**: Link content matches page title

**Page actions**:
- Clear, predictable, strong verbs
- Verb + noun format (except common actions)
- Scannable (no articles)
- Action-led
- Examples:
  - "Create order" ✓
  - "Import" ✓ (clear in context)
  - "Create" ✗ (too vague)

## Related components

- [Layout](../layout) - page content structure
- [Card](../card) - content grouping
- [ButtonGroup](../button-group) - action arrangement
