---
name: polaris-pattern-app-settings-layout
description: Build merchant settings pages fast—scan & organize app configuration with proven two-column layout patterns
---

# App Settings Layout

Lets merchants scan and find groups of settings in apps.

## How it helps merchants

- **Left column**: Glanceable labels and descriptions for easy scanning to find settings quickly
- **Right column**: Settings grouped in cards for easier configuration and grouping of related settings

## Use when merchants need to:

- **Find and change app settings**: Used specifically for finding and updating individual app settings within the Shopify admin

## Components Used

- BlockStack
- Card
- InlineGrid
- Box

## Layout structure

```jsx
<Page>
  <BlockStack gap={{ xs: "800", sm: "400" }}>
    <InlineGrid columns={{ xs: "1fr", md: "2fr 5fr" }} gap="400">
      {/* Left section: labels & descriptions */}
      <Box as="section" paddingInlineStart={{ xs: 400, sm: 0 }} paddingInlineEnd={{ xs: 400, sm: 0 }}>
        <BlockStack gap="400">
          <Text as="h3" variant="headingMd">Setting Group Title</Text>
          <Text as="p" variant="bodyMd">Description of the setting group</Text>
        </BlockStack>
      </Box>

      {/* Right section: form inputs in card */}
      <Card roundedAbove="sm">
        <BlockStack gap="400">
          <TextField label="Setting field" />
          <TextField label="Another setting" />
        </BlockStack>
      </Card>
    </InlineGrid>
  </BlockStack>
</Page>
```

## Guidelines

- Don't include a description unless it's helpful
- Place grouped settings within cards
- Stack all setting groups vertically on the page
- Use responsive breakpoints to collapse to single column on mobile (xs: "1fr")

## Related patterns

- See another two-column layout in Resource detail layout
- See a single-column layout in Resource index layout
