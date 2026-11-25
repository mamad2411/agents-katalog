---
name: polaris-app-provider
description: Shopify Polaris App provider component. Wraps entire app. Provides theme, i18n, and feature configuration to all Polaris components.
---

# App Provider

## When to use
Wrap entire application once at root level. Provides theming, internationalization, and configuration. Required for Polaris components to function properly.

## Props
- `children` ReactNode - App content (required)
- `i18n?` I18nTranslations - Translation strings
- `theme?` Theme - Custom theme object
- `features?` Record<string, boolean> - Feature flags
- `linkComponent?` LinkComponent - Custom link wrapper
- `mediaQueryListByDefault?` boolean - Media query defaults
- `onLinksOverlayClick?` callback - Overlay click handler

## Examples
```jsx
import { AppProvider, Card } from '@shopify/polaris';
import translations from '@shopify/polaris/locales/en.json';

// Basic setup
<AppProvider i18n={translations}>
  <div>
    <Card title="My app">
      {/* App content */}
    </Card>
  </div>
</AppProvider>

// With custom theme
<AppProvider
  i18n={translations}
  theme={{
    colors: {
      surface: '#FFFFFF',
    },
  }}
>
  {/* App content */}
</AppProvider>

// With custom link component (Next.js)
import NextLink from 'next/link';

<AppProvider
  i18n={translations}
  linkComponent={NextLink}
>
  {/* App content */}
</AppProvider>
```

## Best practices
- Wrap entire app once at root
- Place before all Polaris components
- Provide i18n for proper translations
- Use custom link component for routing library
- Pass feature flags as needed

## Internationalization
- Provide translations object
- Import from @shopify/polaris/locales/{language}.json
- Supports multiple languages

## Theme customization
- Override design tokens
- Colors, typography, spacing
- Follow Polaris design system
- Use custom theme sparingly

## Accessibility
- Required for proper ARIA setup
- Enables focus management
- Sets up theme context

## Related components
- All Polaris components require AppProvider
