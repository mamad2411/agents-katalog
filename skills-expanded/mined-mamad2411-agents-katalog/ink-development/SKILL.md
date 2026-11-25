---
name: Ink Development
description: Build CLI applications using Ink and React.
---

# React Ink Development Skill

Build CLI applications using React components with [Ink](https://github.com/vadimdemedes/ink).

## Overview

Ink is a React renderer for the terminal. It provides the same component-based UI building experience that React offers in the browser, but for command-line applications. Ink uses Yoga (Facebook's Flexbox layout engine) for layouts, so CSS-like properties are available.

## When to Use This Skill

- Building interactive CLI tools with React
- Creating terminal UIs with Flexbox layouts
- Developing command-line applications that need real-time updates
- Building tools similar to Jest, Gatsby CLI, or Prisma CLI

## Key Concepts

### Every Element is a Flexbox Container

Think of it as if every `<div>` in the browser had `display: flex`. All text must be wrapped in a `<Text>` component.

### Core Components

- `<Text>` - Display and style text (color, bold, italic, underline)
- `<Box>` - Flexbox container for layout (like `<div style="display: flex">`)
- `<Newline>` - Add newline characters within `<Text>`
- `<Spacer>` - Flexible space that expands along the major axis
- `<Static>` - Render permanent output above dynamic content
- `<Transform>` - Transform string output before rendering

### Essential Hooks

- `useInput` - Handle keyboard input
- `useApp` - Access app methods (exit)
- `useFocus` / `useFocusManager` - Manage focus between components
- `useStdin` / `useStdout` / `useStderr` - Access streams

## Quick Start

```bash
# Using Bun
bun install ink react

# Or using npm
npm install ink react
```

## Basic Example

```tsx
import React, { useState, useEffect } from 'react';
import { render, Text, Box } from 'ink';

const App = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <Box flexDirection="column">
      <Text color="green">Counter: {count}</Text>
      <Text dimColor>Press Ctrl+C to exit</Text>
    </Box>
  );
};

render(<App />);
```

## Project Structure

```
my-cli/
├── src/
│   ├── index.tsx      # Entry point with render()
│   ├── App.tsx        # Main app component
│   └── components/    # Reusable components
├── package.json
└── tsconfig.json
```

## Best Practices

1. **Wrap all text in `<Text>`** - Never render raw strings directly
2. **Use `<Static>` for logs** - Permanent output like completed tasks
3. **Handle exit gracefully** - Use `useApp().exit()` for clean shutdown
4. **Use `useInput` for keyboard handling** - More convenient than raw stdin
5. **Leverage Flexbox** - Use `justifyContent`, `alignItems`, `flexDirection`

## Integration with Bun

When using Bun, you can run Ink applications directly:

```bash
bun run src/index.tsx
```

No transpilation step needed - Bun handles TSX natively.

## References

- [API Reference](./references/api.md) - Complete component and hook documentation
- [Demo Examples](./references/demo.md) - Practical code examples

## Notable Projects Using Ink

- Claude Code (Anthropic)
- Gemini CLI (Google)
- GitHub Copilot CLI
- Cloudflare Wrangler
- Prisma CLI
- Gatsby CLI
- Shopify CLI
