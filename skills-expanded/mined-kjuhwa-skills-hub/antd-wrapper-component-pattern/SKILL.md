---
tags: [design, antd, wrapper, component, pattern]
name: antd-wrapper-component-pattern
description: Wrap Ant Design components with a custom design system layer (Sirius pattern) that extends props, enforces standards, and maintains upgrade compatibility
category: design
trigger: When building a design system on top of Ant Design, or wrapping any third-party component library with custom defaults and extended props
version: 1.0.0
source_project: lucida-ui
linked_knowledge:
  - sirius-wraps-antd-design-system
---

# Ant Design Wrapper Component Pattern

## Context
Instead of replacing Ant Design, wrap each component with a thin layer that adds custom props (standardLayout, padding, size), enforces design tokens, and passes through all original Ant props via `...rest`.

## Steps

1. **Create wrapper component** matching Ant's export name:
   ```tsx
   // Card.tsx (Sirius)
   import { Card as AntCard, CardProps as AntCardProps } from 'antd';

   interface SiriusCardProps extends AntCardProps {
     standardLayout?: boolean;
     padding?: 'none' | 'sm' | 'md' | 'lg';
   }

   export const Card = ({ standardLayout, padding, className, ...rest }: SiriusCardProps) => {
     const mergedClassName = classNames(className, {
       'sirius-card-standard': standardLayout,
       [`sirius-card-padding-${padding}`]: padding,
     });
     return <AntCard className={mergedClassName} {...rest} />;
   };
   ```

2. **Re-export from design system barrel**:
   - `export { Card } from './data-display/card/Card'`
   - Consumers import from `@design-system` instead of `antd` directly

3. **Apply to all wrapped components** (Card, Collapse, Tabs, Button, Modal, Drawer, etc.):
   - Each wrapper: extend props interface, add `classNames` logic, pass through rest
   - Maintain same prop API — consumers can still use any Ant prop

4. **Handle compound components**:
   - For `Tabs.TabPane`, `Collapse.Panel`: re-export sub-components or compose
   - Attach as static properties: `Card.Meta = AntCard.Meta`

5. **StyleProvider integration**:
   - Wrap app root with Ant's `StyleProvider` (`hashPriority="high"`) for CSS-in-JS priority

## Benefits
- Ant Design upgrades only require updating the wrapper layer
- Design token enforcement at the wrapper level (className injection)
- Consumers get typed custom props + full Ant prop passthrough
