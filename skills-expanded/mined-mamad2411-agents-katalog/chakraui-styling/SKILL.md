---
name: chakraui-styling
description: Apply Chakra UI v3 styling patterns, style props, and responsive design. Use when the user asks about Chakra styling, CSS props (padding, margin, bg, color), responsive breakpoints, conditional styles (_hover, _focus, _dark), or layout styling. Triggers for "how to style", "make it responsive", "add hover effect", "dark mode styles", "center a div", or when using style props like p="", m="", bg="", rounded="", or responsive syntax.
---

# Chakra UI v3 Styling Skill

## Quick Reference

### Core Principles
- **Shorthand Props**: Use `p` for `padding`, `m` for `margin`, `bg` for `background`
- **Token System**: All values reference theme tokens (colors, spacing, sizes)
- **Mobile-First Responsive**: Use object/array syntax for breakpoints
- **Conditional Props**: Underscore prefix for states (`_hover`, `_focus`, `_dark`)
- **Logical Properties**: Use `Start`/`End` instead of `Left`/`Right` for RTL support

### Essential Shorthands
| Prop | Full | Example |
|------|------|---------|
| `p`, `px`, `py` | padding | `p="4"` `px="6"` |
| `m`, `mx`, `my` | margin | `m="2"` `mx="auto"` |
| `bg` | background | `bg="blue.500"` |
| `rounded` | borderRadius | `rounded="md"` |
| `shadow` | boxShadow | `shadow="lg"` |
| `flexDir` | flexDirection | `flexDir="column"` |
| `pos` | position | `pos="relative"` |
| `w`, `h` | width, height | `w="full"` `h="100vh"` |

### Color Opacity
```tsx
<Box bg="blue.500/40" />           // 40% opacity
<Box borderColor="red.300/20" />   // 20% opacity
```

### Responsive Syntax
```tsx
<Box fontSize={{ base: "sm", md: "md", lg: "lg" }} />
<Box hideFrom="md" />              // Hide from md and up
<Box hideBelow="md" />             // Hide below md
```

### Conditional Styles
```tsx
<Button _hover={{ bg: "blue.600" }} _focus={{ ring: "2px" }} />
<Box bg="white" _dark={{ bg: "gray.800" }} />
<Box className="group">
  <Box _groupHover={{ opacity: 1 }} />
</Box>
```

### Color Palette (Virtual Color)
```tsx
<Box colorPalette="blue" bg="colorPalette.500" _hover={{ bg: "colorPalette.600" }}>
  Themeable component
</Box>
```

## Common Component Patterns

### Dashboard Card
```tsx
<Box
  p="6"
  rounded="xl"
  bg="white"
  shadow="md"
  border="1px solid"
  borderColor="gray.100"
  _dark={{ bg: "gray.800", borderColor: "gray.700" }}
  transition="all 0.2s"
  _hover={{ shadow: "lg", transform: "translateY(-2px)" }}
>
  <Heading size="md" mb="2">Title</Heading>
  <Text color="gray.600" _dark={{ color: "gray.400" }}>Content</Text>
</Box>
```

### Navigation Item
```tsx
<HStack
  px="4"
  py="3"
  rounded="md"
  cursor="pointer"
  color="gray.600"
  _hover={{ bg: "gray.100", color: "gray.900" }}
  _dark={{ color: "gray.400", _hover: { bg: "gray.700", color: "white" } }}
>
  <Icon />
  <Text fontWeight="medium">Label</Text>
</HStack>
```

### Metric Display
```tsx
<VStack align="flex-start" gap="1">
  <Text fontSize="sm" color="gray.500">Label</Text>
  <Heading size="2xl">$1,234.56</Heading>
  <HStack color="green.500">
    <ArrowUpIcon />
    <Text fontWeight="medium">+12.5%</Text>
  </HStack>
</VStack>
```

### Status Badge
```tsx
<Badge
  colorPalette={status === 'success' ? 'green' : 'error' ? 'red' : 'yellow'}
  px="2"
  py="0.5"
  rounded="full"
  fontSize="xs"
>
  {status}
</Badge>
```

## Best Practices

1. **Use semantic tokens** for colors that adapt to dark mode (`bg.subtle`, `fg.muted`)
2. **Prefer `colorPalette`** for component variants instead of hardcoded colors
3. **Use logical properties** (`start`/`end`) for RTL support
4. **Keep responsive values DRY** with text/layer styles
5. **Use `truncate`** or `lineClamp` for text overflow
6. **Use explicit breakpoints** (`smDown`, `md`) for variants to avoid style leaking

## Detailed References

- **[style-props.md](references/style-props.md)** - Complete style props reference (spacing, sizing, typography, layout, effects, filters, transforms, etc.)
- **[responsive-design.md](references/responsive-design.md)** - Breakpoints, object/array syntax, hide utilities, responsive patterns
- **[conditional-styles.md](references/conditional-styles.md)** - Pseudo classes, dark mode, group selectors, data attributes, CSS variables, focus ring
- **[patterns.md](references/patterns.md)** - Chakra factory, virtual color, text/layer styles, animation styles, common UI patterns

## Full Reference

- **[llms-styling.txt](references/llms-styling.txt)** - Full reference of all Styling "very large File 4400 lines".