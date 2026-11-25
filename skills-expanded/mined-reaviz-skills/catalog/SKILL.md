# ComponentCatalog

System for letting an LLM render custom React components by emitting fenced code blocks with JSON specs. The catalog ships a remark plugin, a `<pre>` override, and a system-prompt generator — all wired through `<Chat components={catalog} />`.

## Imports

```tsx
import {
  componentCatalog,
  ComponentRenderer,
  ComponentError,
  createComponentPre,
  createChartComponentDef,
  validateSpec,
  generatePrompt,
  type ComponentCatalog,
  type ComponentDefinition,
  type ComponentDefinitions,
  type ComponentSpec,
  type ComponentCatalogOptions,
  type ComponentCatalogError,
  type ComponentErrorProps
} from 'reachat';
import { z } from 'zod';
```

## componentCatalog()

Main factory. Takes a map of component definitions and returns a catalog object ready for `<Chat>`.

```ts
function componentCatalog(
  definitions: ComponentDefinitions,
  options?: ComponentCatalogOptions
): ComponentCatalog;

interface ComponentCatalogOptions {
  /** Fenced-code language tag (default: 'component') */
  language?: string;
  /** Custom error renderer — return ReactNode or undefined for default */
  onError?: (error: ComponentCatalogError) => ReactNode | undefined;
}

interface ComponentCatalog {
  remarkPlugin: Plugin;       // Pass-through plugin (rendering happens in <pre>)
  components: Components;     // { pre: ComponentPre } for react-markdown
  systemPrompt: () => string; // LLM instructions
  definitions: ComponentDefinitions;
}
```

`Chat` accepts a catalog directly via the `components` prop and wires everything in:

```tsx
<Chat sessions={sessions} components={catalog}>...</Chat>
```

For advanced control, splice the pieces yourself:

```tsx
<Chat
  sessions={sessions}
  remarkPlugins={[remarkGfm, catalog.remarkPlugin]}
  markdownComponents={{ ...catalog.components, pre: MyCustomPre }}
>...</Chat>
```

## ComponentDefinition

```ts
interface ComponentDefinition<TProps = Record<string, any>> {
  description: string;        // Used by systemPrompt
  props: z.ZodType<TProps>;   // Runtime validation + prompt schema
  component: FC<TProps & {
    children?: ReactNode;
    sendMessage?: (message: string) => void;
  }>;
}

type ComponentDefinitions = Record<string, ComponentDefinition>;
```

The `component` receives validated props plus:
- `children` — rendered nested specs
- `sendMessage` — pulled from `ChatContext` so the rendered UI can dispatch a follow-up message

## Quick example

```tsx
const catalog = componentCatalog({
  WeatherCard: {
    description: 'Displays weather for a city',
    props: z.object({
      city: z.string().describe('City name'),
      temperature: z.number().describe('Temp in Fahrenheit')
    }),
    component: ({ city, temperature, sendMessage }) => (
      <div className="rounded-xl border p-4">
        <h3>{city}</h3>
        <p>{temperature}°F</p>
        <button onClick={() => sendMessage?.(`Tell me more about ${city}`)}>
          Tell me more
        </button>
      </div>
    )
  }
});

<Chat sessions={sessions} components={catalog}>
  <SessionMessages />
  <ChatInput />
</Chat>
```

The LLM emits:

````markdown
```component
{ "type": "WeatherCard", "props": { "city": "SF", "temperature": 68 } }
```
````

## JSON spec format

```ts
interface ComponentSpec {
  type: string;                     // Must match a key in the catalog
  props: Record<string, any>;       // Validated against the Zod schema
  children?: ComponentSpec[];       // Optional nested specs
}
```

- **Single**: `{ "type": "Card", "props": {...} }`
- **Array**: `[ {...}, {...} ]` — multiple top-level components in one block
- **Nested**: `{ "type": "Row", "props": {}, "children": [ {...}, {...} ] }`

## Errors

Validation produces `ComponentCatalogError` with one of four `type`s:

| type | When |
|------|------|
| `invalid_json` | The fenced block is not valid JSON |
| `unknown_component` | `spec.type` is not in the catalog |
| `invalid_props` | Zod validation failed (issues passed through) |
| `render_error` | The component threw during render |

Each component is wrapped in a React error boundary so a single failure doesn't break the markdown stream. Provide a custom UI via `options.onError`:

```tsx
componentCatalog(defs, {
  onError: error =>
    error.type === 'invalid_props' ? (
      <pre>{JSON.stringify(error.issues, null, 2)}</pre>
    ) : undefined
});
```

## systemPrompt()

Generates LLM instructions describing the available components, their descriptions, and Zod-derived prop schemas. Useful as a system message when calling your model.

```ts
const prompt: string = catalog.systemPrompt();
```

## createChartComponentDef()

Pre-built definition that wraps `ChartRenderer`, allowing the LLM to render charts.

```tsx
import { componentCatalog, createChartComponentDef } from 'reachat';

const catalog = componentCatalog({
  Chart: createChartComponentDef()
});
```

LLM output:

````markdown
```component
{
  "type": "Chart",
  "props": {
    "type": "bar",
    "title": "Active users",
    "data": [{ "key": "Mon", "data": 12 }, { "key": "Tue", "data": 18 }]
  }
}
```
````

Supported `type`s: `bar`, `line`, `area`, `pie`, `radialBar`, `radialArea`, `sparkline`. Requires `reaviz` as a peer dependency.

## Lower-level helpers

- **`createComponentPre(definitions, options?)`** — returns the `<pre>` override component used in `catalog.components` (for advanced custom wiring)
- **`ComponentRenderer`** — renders a `ComponentSpec` directly (for custom dispatch outside of markdown)
- **`validateSpec(spec, definitions)`** — runs the four-step validation pipeline (JSON parse, type lookup, Zod, children)
- **`generatePrompt(definitions, language?)`** — bare prompt generator (catalog wraps this)
- **`ComponentError`** — default error UI; props in `ComponentErrorProps`

## Dependencies

- `zod` — required, used for runtime prop validation
- `reaviz` — peer-optional, only needed for `createChartComponentDef()`

## Theme key

```
theme.component.base
```
