# Markdown

Markdown renderer used inside `MessageQuestion` / `MessageResponse`, plus syntax highlighting, tables, charts, redaction matchers, and remark/rehype plugins. Also exported standalone for custom use.

## Imports

```tsx
import {
  Markdown,
  CodeHighlighter,
  TableComponent,
  TableHeaderCell,
  TableDataCell,
  ChartRenderer,
  // remark plugins
  remarkCve,
  remarkComponent,
  remarkRedact,
  type RedactMatcher,
  // built-in matchers
  ssnMatcher,
  creditCardMatcher,
  bitcoinMatcher,
  commonRedactMatchers,
  // syntax themes
  dark,
  light
} from 'reachat';
```

## Markdown

Wrapper around `react-markdown` that wires reachat's default component overrides for code, tables, lists, headings, links, hr, redact tags, and reads the `theme` from `ChatContext`.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | — | Markdown source |
| `remarkPlugins` | `Plugin[]` | — | Remark plugins (passed through) |
| `rehypePlugins` | `Plugin[]` | `[rehypeRaw, rehypeKatex]` | Rehype plugins (math + raw HTML support) |
| `theme` | `ChatTheme` | from context | Theme override for class names |
| `customComponents` | `Components` | — | Component overrides; merged on top of `markdownComponents` from context, which is merged on top of defaults |

```tsx
<Markdown
  remarkPlugins={[remarkGfm, remarkRedact(commonRedactMatchers)]}
  customComponents={{ a: CustomLink }}
>
  {markdownString}
</Markdown>
```

The default `code` renderer detects fenced blocks (`language-xxx` className) and routes them through `CodeHighlighter`; inline code falls back to a plain `<code>` styled by `theme.messages.message.markdown.inlineCode`.

A custom `redact` element is also wired up to render `<Redact>` from reablocks (used by `remarkRedact`).

## CodeHighlighter

Standalone code-block renderer using `react-syntax-highlighter` (Prism build). Adds a toolbar with the language label and a copy button.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | — | Code content |
| `language` | `string` | — | Pass `language-xxx` (extracted automatically by `Markdown`) |
| `theme` | `Record<string, string>` | `dark` | Prism theme object (`dark` or `light` exported from reachat) |
| `copyIcon` | `ReactElement` | copy icon | Pass `null` to hide the copy button |
| `className` / `inlineClassName` / `copyClassName` / `toolbarClassName` | `string` | — | Tailwind class hooks |

When `language` does not match `language-(\w+)`, the component renders inline `<code>` only (no toolbar).

## Table components

Plain wrappers used by the markdown defaults; you can re-use them in custom components:

- `TableComponent` — `<table>` with class merging
- `TableHeaderCell` — `<th>`
- `TableDataCell` — `<td>`

## ChartRenderer

Renders a chart from a `ChartConfig`. Used internally by `createChartComponentDef()` and the redact-style chart fenced block. Reads `theme.chart` from `ChatContext`.

```ts
type ChartType =
  | 'bar' | 'line' | 'area' | 'pie'
  | 'radialBar' | 'radialArea' | 'sparkline';

interface ChartDataPoint { key: string; data: number | ChartDataPoint[]; }

interface ChartConfig {
  type: ChartType;
  data: ChartDataPoint[];
  width?: number;   // default 400
  height?: number;  // default 300
  title?: string;
}
```

```tsx
<ChartRenderer
  config={{
    type: 'bar',
    title: 'Active users',
    data: [{ key: 'Mon', data: 12 }, { key: 'Tue', data: 18 }]
  }}
/>
```

Empty data → renders a `ComponentError` with a "No chart data available" warning. Non-numeric data points → an error variant.

Charts are powered by `reaviz`, which is an **optional peer dependency** — install it when using `ChartRenderer` or `createChartComponentDef`.

## Remark plugins

### remarkCve

Auto-links CVE identifiers in markdown to MITRE.

```tsx
import { remarkCve } from 'reachat';

<Chat remarkPlugins={[remarkGfm, remarkCve]}>...</Chat>
```

Pattern: `CVE-YYYY-NNNN` (4–7 digits). Each match becomes a link to `https://cve.mitre.org/cgi-bin/cvename.cgi?name=...`.

### remarkComponent

Pass-through plugin that exists as the integration point for `componentCatalog()` — actual rendering happens in `ComponentPre`. Usually you don't import this directly; pass the `components` prop to `Chat` instead.

### remarkRedact

Replaces sensitive patterns with `<redact>` elements that the default markdown components render via reablocks `<Redact>`.

```ts
interface RedactMatcher {
  name: string;
  pattern: RegExp;        // must use the global flag
  validate?: (match: string) => boolean; // skip when returns false
}

remarkRedact(matchers: RedactMatcher[]): Plugin;
```

```tsx
import { remarkRedact, ssnMatcher, creditCardMatcher } from 'reachat';

<Chat remarkPlugins={[remarkRedact([ssnMatcher, creditCardMatcher])]}>...</Chat>
```

Built-in matchers exported from reachat:

- `ssnMatcher` — `123-45-6789`
- `creditCardMatcher` — 13–19 digit numbers; skips obvious non-cards (years, ages, phone hints)
- `bitcoinMatcher` — addresses starting with `1` or `3` (26–35 chars)
- `commonRedactMatchers` — array containing all three above

## Syntax highlighter themes

`dark` and `light` are Prism style objects re-exported for `CodeHighlighter`'s `theme` prop.

## Theme keys

```
theme.messages.message.markdown.{hr, p, a, table, th, td, code, inlineCode, toolbar, li, ul, ol, copy, h1..h6}
theme.chart.{base, title, content}
theme.chart.error.{base, title, code}
theme.chart.warning.{base, title}
```
