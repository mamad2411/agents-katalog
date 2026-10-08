---
name: json-ui
description: |
  CRITICAL: Use for json-ui component rendering and development. Triggers on:
  json-ui, json render, component catalog, report render, HTML report,
  I18nString, i18n, bilingual, language switch, dual language,
  PaperHeader, AuthorList, Abstract, MetricsGrid, Section, Highlight,
  Zod schema, catalog.ts, cli.ts, components/index.tsx,
  "how to add a component", "how to render JSON",
  JSON 渲染, 组件目录, 报告渲染, 多语言, 中英文切换
---

# json-ui

> **Version:** 1.0.0 | **Last Updated:** 2026-01-29

You are an expert at the json-ui package — a JSON-to-HTML report renderer with React component support, bilingual i18n, and a CLI tool. Help users by:
- **Writing components**: Add new component types following existing patterns
- **Rendering reports**: Generate HTML from JSON report definitions
- **Debugging**: Fix rendering, build, or i18n issues
- **Answering questions**: Explain architecture, component catalog, data flow

## Quick Reference

| Task | File | Pattern |
|------|------|---------|
| Define component schema | `src/catalog.ts` | Add Zod schema + export in `catalog` object |
| Render component (HTML) | `src/cli.ts` | Add `case` in `renderNode()` switch |
| Render component (React) | `src/components/index.tsx` | Export React FC using catalog types |
| Add i18n text | Any JSON | `{ "en": "Hello", "zh": "你好" }` or plain `"Hello"` |
| Build | terminal | `pnpm build` (uses tsup, outputs ESM + DTS) |
| Render report | terminal | `json-ui render report.json [-o out.html] [--no-open]` |

## Documentation

Refer to local source files for detailed documentation:
- `packages/json-ui/src/catalog.ts` - All Zod schemas and type definitions
- `packages/json-ui/src/cli.ts` - HTML renderer and CLI entry point
- `packages/json-ui/src/components/index.tsx` - React component implementations

## IMPORTANT: Documentation Completeness Check

**Before answering questions, Claude MUST:**
1. Read the relevant source file(s) listed above
2. If file read fails: Inform user "本地文档不完整，建议更新"
3. Still answer based on SKILL.md patterns + built-in knowledge

## Architecture

### JSON Report Format

Reports are trees of nodes:

```json
{
  "type": "Report",
  "props": { "title": "My Report", "theme": "auto" },
  "children": [
    {
      "type": "Section",
      "props": { "title": "Overview", "icon": "bulb" },
      "children": [
        { "type": "Abstract", "props": { "text": "..." } }
      ]
    }
  ]
}
```

### Three Rendering Layers

| Layer | File | Output | Use Case |
|-------|------|--------|----------|
| Zod Schemas | `catalog.ts` | Type definitions | Validation, type safety |
| HTML Renderer | `cli.ts` | Static HTML string | CLI `render` command |
| React Components | `components/index.tsx` | React elements | Embedded usage |

### Data Flow

```
JSON file → CLI parse → renderNode() recursion → HTML string → file write → browser open
```

## Component Catalog (38 types)

### Layout

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Report` | `title?, theme` | Root wrapper, 800px max-width |
| `Section` | `title, icon?, collapsible?` | Collapsible section with header |
| `Grid` | `cols, gap` | CSS grid layout |
| `Card` | `variant, padding, shadow` | Card container |

### Paper Info

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `PaperHeader` | `title, arxivId, date, categories?` | Paper title + metadata |
| `AuthorList` | `authors, layout?, maxVisible?` | Author names + affiliations |
| `Abstract` | `text, highlights?, maxLength?` | Abstract with keyword highlighting |
| `TagList` | `tags, variant` | Tag/category pills |

### Content

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `ContributionList` | `items, numbered?` | Numbered contributions with badges |
| `MethodOverview` | `steps, showConnectors?` | Step-by-step method pipeline |
| `Highlight` | `text, type, source?` | Blockquote (quote/important/warning/code) |
| `KeyPoint` | `icon, title, description` | Icon + title + description |
| `CodeBlock` | `code, language, showLineNumbers?` | Syntax-highlighted code |
| `Prose` | `content` | Markdown content block |
| `Callout` | `type, title?, content` | Info/tip/warning/important/note box |

### Rich Content

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Image` | `src, alt?, caption?, width?` | Single image |
| `Figure` | `images, caption?, label?` | Multi-image figure |
| `Formula` | `latex, block?, label?` | LaTeX formula |
| `DefinitionList` | `items` | Term-definition pairs |
| `Theorem` | `type, number?, title?, content` | Theorem/lemma/proposition |
| `Algorithm` | `title, steps, caption?` | Algorithm pseudocode |
| `ResultsTable` | `columns, rows, highlights?` | Results with best-cell highlighting |

### Data Display

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Metric` | `label, value, trend?, icon?` | Single metric card |
| `MetricsGrid` | `metrics, cols?` | Grid of metric cards |
| `Table` | `columns, rows, striped?, caption?` | Data table |

### Interactive

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `LinkButton` | `href, label, icon?, external?` | Styled link button |
| `LinkGroup` | `links, layout?` | Group of link buttons |

### Brand

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `BrandHeader` | `badge?, poweredBy?, showBadge?` | AI-generated badge header |
| `BrandFooter` | `timestamp, attribution?, disclaimer?` | Footer with attribution |

## I18n System

### Backward-Compatible Bilingual Strings

The `I18nString` type accepts both plain strings and bilingual objects:

```typescript
// catalog.ts
export const I18nString = z.union([
  z.string(),
  z.object({ en: z.string(), zh: z.string() }),
]);
```

### JSON Usage

```json
// Plain string (backward compatible)
{ "title": "Hello World" }

// Bilingual object
{ "title": { "en": "Hello World", "zh": "你好世界" } }
```

### HTML Rendering (cli.ts)

For HTML output, i18n strings render as dual spans:

```typescript
// renderI18n() outputs:
<span class="i18n-en">Hello</span><span class="i18n-zh">你好</span>

// CSS controls visibility:
html[lang="en"] .i18n-zh { display: none; }
html[lang="zh"] .i18n-en { display: none; }
```

For HTML attributes (alt, title) where only a plain string works:

```typescript
// resolveI18n() picks one language:
const alt = resolveI18n(props.alt, 'en'); // returns plain string
```

### React Rendering (components/index.tsx)

```typescript
// Use <I18nText> component for JSX:
<I18nText value={props.title} />

// Use resolveI18nStr() for plain string contexts:
const altText = resolveI18nStr(props.alt, 'en');
```

### Language Switcher

- Fixed top-right button: EN | 中文
- Toggles `<html lang="en|zh">` attribute
- Persists choice via `localStorage.getItem('json-ui-lang')`

## Key Patterns

### Pattern 1: Adding a New Component

1. **Define schema** in `catalog.ts`:
```typescript
export const MyWidgetSchema = z.object({
  label: I18nString,        // Use I18nString for user-visible text
  count: z.number(),        // Use z.string()/z.number() for data
  variant: VariantType.default('default'),
});

// Add to catalog object:
export const catalog = {
  // ...existing...
  MyWidget: MyWidgetSchema,
} as const;

// Export type:
export type MyWidgetProps = z.infer<typeof MyWidgetSchema>;
```

2. **Add HTML renderer** in `cli.ts` `renderNode()` switch:
```typescript
case 'MyWidget': {
  const { label, count, variant } = props;
  return `<div class="my-widget ${variant}">
    <span>${renderI18n(label)}</span>
    <strong>${escapeHtml(String(count))}</strong>
  </div>`;
}
```

3. **Add React component** in `components/index.tsx`:
```typescript
export const MyWidget: React.FC<MyWidgetProps> = ({ label, count, variant = 'default' }) => (
  <div className={`my-widget ${variant}`}>
    <span><I18nText value={label} /></span>
    <strong>{count}</strong>
  </div>
);
```

### Pattern 2: Handling I18n in Special Cases

For text that needs processing (e.g., Abstract highlights):

```typescript
// HTML (cli.ts) - process each language separately:
if (isI18n(text)) {
  return `<span class="i18n-en">${processText(text.en)}</span>
          <span class="i18n-zh">${processText(text.zh)}</span>`;
} else {
  return processText(String(text));
}

// React (components/index.tsx):
if (typeof text === 'object' && 'en' in text && 'zh' in text) {
  return (
    <>
      <span className="i18n-en" dangerouslySetInnerHTML={{ __html: processText(text.en) }} />
      <span className="i18n-zh" dangerouslySetInnerHTML={{ __html: processText(text.zh) }} />
    </>
  );
}
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| `Type 'I18nStringType' is not assignable to 'ReactNode'` | Passing i18n object directly to JSX | Wrap with `<I18nText value={...} />` |
| `Property 'length' does not exist on type 'I18nStringType'` | Calling string methods on i18n value | Use type guard: `typeof text === 'string' ? text : text.en` |
| Images not loading from arxiv | `crossorigin="anonymous"` on `<img>` | Remove `crossorigin`; keep only `referrerpolicy="no-referrer"` |
| Language switcher not working | Missing CSS rules or JS | Ensure `html[lang] .i18n-*` CSS rules and toggle JS are in template |
| Build fails with type errors | Schema changed but components not updated | Update all three files: catalog, cli, components |

## CRITICAL: Image Handling

**Do NOT use `crossorigin="anonymous"` on `<img>` tags.**

Sites like arxiv.org do not send CORS headers. Adding `crossorigin="anonymous"` causes the browser to require CORS, which fails and blocks the image.

```html
<!-- WRONG - breaks images from arxiv and similar sites -->
<img src="..." referrerpolicy="no-referrer" crossorigin="anonymous" />

<!-- CORRECT -->
<img src="..." referrerpolicy="no-referrer" />
```

## Chinese Translation Guidelines

When writing Chinese translations for ML/AI papers:

| Wrong | Correct | Reason |
|-------|---------|--------|
| 评论器 | 价值函数（critic） | Standard ML term |
| 运行估计 | 滑动估计 | Running estimate = 滑动估计 |
| 重加权因子 | 加权系数 | More natural Chinese |
| 不断演化的 | 动态更新的 | Clearer meaning |
| 简单修复 | 改动小 | Academic tone |

## Build & CLI

```bash
# Build (ESM + DTS via tsup)
cd packages/json-ui && pnpm build

# Render report to HTML
node dist/cli.js render example-report-rich.json

# With options
node dist/cli.js render report.json -o output.html --no-open
```

## When Writing Code

1. Always use `I18nString` for user-visible text properties in schemas
2. Always handle both string and `{en, zh}` forms in renderers
3. Never use `crossorigin="anonymous"` on img tags
4. Keep `referrerpolicy="no-referrer"` on img tags for privacy
5. Test with `pnpm build` after any schema or component changes
6. Update all three layers (catalog, cli, components) when adding components
