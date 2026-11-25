---
name: polaris-layout
description: Shopify Polaris Layout component. Use to create main page layout with one-column, two-column, or annotated configurations.
---

# Layout

## When to use
Use to create the main page structure. Supports one-column (full width), two-column (primary + secondary), and annotated (settings pages) layouts.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Layout sections |
| sectioned | boolean | false | Auto-add sections with padding |

## Layout.Section Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | Required | Section content |
| secondary | boolean | false | Secondary width section |

## Layout.AnnotatedSection Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| title | string | - | Section title |
| description | string | - | Section description |
| children | ReactNode | Required | Card content |

## Examples

```jsx
import { Page, Layout, Card, Text } from '@shopify/polaris';

// One column (full width)
<Page fullWidth>
  <Layout>
    <Layout.Section>
      <Card>
        <Box padding="400">
          <Text variant="headingMd">Online store dashboard</Text>
          <p>View a summary of your online store's performance.</p>
        </Box>
      </Card>
    </Layout.Section>
  </Layout>
</Page>

// Two columns (2/3 primary + 1/3 secondary)
<Page fullWidth>
  <Layout>
    <Layout.Section>
      <Card>
        <Box padding="400">
          <Text variant="headingMd">Main content</Text>
          <p>Primary information goes here.</p>
        </Box>
      </Card>
    </Layout.Section>
    <Layout.Section secondary>
      <Card>
        <Box padding="400">
          <Text variant="headingMd">Secondary</Text>
          <p>Related information goes here.</p>
        </Box>
      </Card>
    </Layout.Section>
  </Layout>
</Page>

// Multiple sections in primary column
<Page fullWidth>
  <Layout>
    <Layout.Section>
      <BlockStack gap="400">
        <Card>
          <Box padding="400">
            <Text variant="headingMd">Sales</Text>
          </Box>
        </Card>
        <Card>
          <Box padding="400">
            <Text variant="headingMd">Orders</Text>
          </Box>
        </Card>
      </BlockStack>
    </Layout.Section>
    <Layout.Section secondary>
      <Card>
        <Box padding="400">
          <Text variant="headingMd">Statistics</Text>
        </Box>
      </Card>
    </Layout.Section>
  </Layout>
</Page>

// Annotated layout (settings)
<Page fullWidth>
  <Layout>
    <Layout.AnnotatedSection
      title="Store setup"
      description="Configure basic store settings"
    >
      <Card>
        <Box padding="400">
          <TextField label="Store name" />
        </Box>
      </Card>
    </Layout.AnnotatedSection>

    <Layout.AnnotatedSection
      title="Store location"
      description="Where your store is based"
    >
      <Card>
        <Box padding="400">
          <TextField label="Country" />
        </Box>
      </Card>
    </Layout.AnnotatedSection>
  </Layout>
</Page>

// Annotated with multiple cards
<Page fullWidth>
  <Layout>
    <Layout.AnnotatedSection title="Billing" description="Manage payment methods">
      <BlockStack gap="400">
        <Card>Payment method 1</Card>
        <Card>Payment method 2</Card>
      </BlockStack>
    </Layout.AnnotatedSection>
  </Layout>
</Page>

// With auto-sectioning
<Page>
  <Layout sectioned>
    <Layout.Section>
      <Text variant="headingMd">Quick stats</Text>
    </Layout.Section>
    <Layout.Section secondary>
      <Text variant="headingMd">Actions</Text>
    </Layout.Section>
  </Layout>
</Page>
```

## Best practices

- Use white backgrounds for primary content
- Use grey backgrounds for secondary content
- Center cards when no secondary section
- Group similar concepts in cards
- Separate different cards with dividers
- Use primary 2/3 for main info, secondary 1/3 for related tasks
- Equal-width layouts when sections have same importance
- Annotated layout only for settings pages
- Can combine one and two-column on same page

## Content guidelines

**Card content**: Follow card guidelines

**Annotated section titles**: Clear, action-oriented, follow heading guidelines

**Annotated descriptions**:
- Explain purpose of section
- Provide instructions for choices
- Short (1-3 sentences max)
- Don't repeat title
- Use complete sentences
- Link to Help Center with "Learn more"

## Related components

- [Page](../page) - page wrapper
- [Card](../card) - content grouping
- [BlockStack](../block-stack) - vertical arrangement
- [Grid](../grid) - complex multi-column
