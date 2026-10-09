---
name: chaibuilder
description: ChaiBuilder Core extension patterns for Next.js. Use when extending the builder UI (custom sidebar panels, slots, lifecycle hooks, feature flags, block tabs, libraries), creating custom blocks, configuring the server, or implementing page rendering. Covers all top-level chaicore APIs.
---

# ChaiBuilder Core — Extension Patterns

## Skill Sections

| Section           | Prefix       | When to Use                                                     |
| ----------------- | ------------ | --------------------------------------------------------------- |
| **Extend UI**     | `extend-ui-` | Add panels, slots, hooks, flags, tabs, libraries to the builder |
| **Custom Blocks** | `blocks-`    | Define and register custom blocks with props schema             |
| **Server Setup**  | `server-`    | `buildChaiBuilderConfig`, server actions, `withChaiBuilder`     |
| **Render**        | `render-`    | `RenderChaiBlocks`, `ChaiPageCSS`, `getStylesForBlocks`         |

See `AGENTS.md` for full examples per section.

---

## Quick Reference: Page Rendering

All render imports from `chaicore/render`.

| API                                        | Where            | Description                       |
| ------------------------------------------ | ---------------- | --------------------------------- |
| `RenderChaiBlocks`                         | Page body        | Renders all blocks (async RSC)    |
| `ChaiPageCSS`                              | `<head>`         | Tailwind CSS + theme vars + fonts |
| `ChaiPageJSONLD`                           | `<head>`         | Structured data JSON-LD           |
| `PreviewBanner`                            | Page body        | Draft mode indicator (client)     |
| `getStylesForBlocks(blocks, includeBase?)` | Custom pipelines | Generate Tailwind CSS from blocks |
| `getChaiThemeCssVariables({ theme })`      | Custom pipelines | CSS vars string from theme object |
| `getMergedPartialBlocks(blocks, partials)` | Custom pipelines | Inline partial block references   |

**Minimal page:**

```tsx
// app/(public)/[[...slug]]/page.tsx
import { getChaiBuilder } from "@/chaibuilder.server";
import { RenderChaiBlocks, ChaiPageCSS, PreviewBanner } from "chaicore/render";

export default async function Page(props) {
  const slug = "/" + ((await props.params).slug?.join("/") ?? "");
  const cb = await getChaiBuilder(props);
  const { page, pageData, settings } = await cb.getPagePayload(slug);
  return (
    <>
      <ChaiPageCSS page={page} />
      <RenderChaiBlocks page={page} pageData={pageData} settings={settings} pageProps={{ slug }} />
      <PreviewBanner show={page.draft ?? false} />
    </>
  );
}
```

---

## Quick Reference: Server Setup

All server imports from `chaicore/server` or `chaicore/next`. Never import in client components.

| Step                    | File                        | API                                                                                     |
| ----------------------- | --------------------------- | --------------------------------------------------------------------------------------- |
| 1. Wrap Next.js config  | `next.config.ts`            | `withChaiBuilder(nextConfig)`                                                           |
| 2. Build server config  | `chaibuilder.config.ts`     | `buildChaiBuilderConfig({ db, ... })`                                                   |
| 3. Create server handle | `chaibuilder.server.ts`     | `createChaiBuilder(config, { context })` |
| 4. Use in pages/layouts | `app/**/page.tsx`           | `getChaiBuilder(props)`                                                                 |
| 5. Route handler        | `app/.../api/chai/route.ts` | `handleChaiActionRequest(req, cb.handleHttpAction)`                                     |

**Minimal setup:**

```ts
// next.config.ts
import { withChaiBuilder } from "chaicore/next";
export default withChaiBuilder({});

// chaibuilder.config.ts — plain data, no framework imports
import { buildChaiBuilderConfig } from "chaicore/server";
export const chaiConfig = buildChaiBuilderConfig({ db });

// chaibuilder.server.ts — owns auth/tenancy/draft; exports the handle entry points import
import { chaiConfig } from "@/chaibuilder.config";
import { createChaiBuilder } from "chaicore/server";
export const { getChaiBuilder } = createChaiBuilder(chaiConfig, {
  context: async ({ request }) => ({
    userId: await getUserIdFromCookies(request),
    role: "admin",
    permissions: ["*"], // omit to resolve membership from app_users instead
    draft: false,
  }),
});

// app/(builder)/api/chai/route.ts
import { getChaiBuilder } from "@/chaibuilder.server";
import { handleChaiActionRequest } from "chaicore/nextjs/server";
export async function POST(req, props) {
  const cb = await getChaiBuilder(props, req);
  return handleChaiActionRequest(req, cb.handleHttpAction);
}
```

---

## Quick Reference: Custom Blocks

All block imports from `chaicore/registry`. Register at module level.

| API                                        | Purpose                                                 |
| ------------------------------------------ | ------------------------------------------------------- |
| `registerChaiBlock(Component, Config)`     | Register a block component + config                     |
| `registerChaiBlockProps(schema)`           | Build RJSF props schema; returns `{ schema, uiSchema }` |
| `stylesProp(defaultClasses)`               | Create the Tailwind styles prop                         |
| `builderProp(options)`                     | Editor-only prop (hidden in rendered output)            |
| `closestBlockProp(blockType, prop)`        | Read prop from nearest ancestor block                   |
| `registerChaiServerBlock(Component, opts)` | Override server-side data provider only                 |

**Minimal block example:**

```tsx
import { registerChaiBlock, registerChaiBlockProps, stylesProp } from "chaicore/registry";
import type { ChaiBlockComponentProps, ChaiStyles } from "chaicore/types";

const MyBlock = ({ blockProps, styles, label }: ChaiBlockComponentProps<{ label: string; styles: ChaiStyles }>) => (
  <div {...blockProps} {...styles}>
    {label}
  </div>
);

registerChaiBlock(MyBlock, {
  type: "MyBlock",
  label: "My Block",
  group: "basic",
  props: registerChaiBlockProps({
    properties: {
      styles: stylesProp("p-4"),
      label: { type: "string", title: "Label", default: "Hello" },
    },
  }),
  i18nProps: ["label"],
  aiProps: ["label"],
});
```

---

## Quick Reference: Extend UI

All register calls are **client-only** — call at module level before `ChaiWebsiteBuilder` mounts.

| API                                       | Import             | Purpose                               |
| ----------------------------------------- | ------------------ | ------------------------------------- |
| `registerChaiSidebarPanel(id, opts)`      | `chaicore` | Add panel to builder sidebar          |
| `registerChaiSlot(slotId, Component)`     | `chaicore` | Inject component at a UI location     |
| `CHAI_SLOT_IDS`                           | `chaicore` | Enum of all valid slot IDs            |
| `registerChaiHook(hookName, fn)`          | `chaicore` | Lifecycle hook (pipeline)             |
| `CHAI_HOOKS`                              | `chaicore` | Enum of all valid hook names          |
| `registerChaiFeatureFlag(key, opts)`      | `chaicore` | Register toggleable flag              |
| `registerChaiFeatureFlags(map)`           | `chaicore` | Register multiple flags at once       |
| `registerChaiAddBlockTab(id, opts)`       | `chaicore` | Add tab to "Add Block" panel          |
| `registerChaiLibrary(id, config)`         | `chaicore` | Register custom block library         |
| `registerChaiBlockSettingWidget(id, C)`   | `chaicore` | Custom RJSF widget for block settings |
| `registerChaiBlockSettingField(id, C)`    | `chaicore` | Custom RJSF field                     |
| `registerChaiBlockSettingTemplate(id, C)` | `chaicore` | Custom RJSF template                  |
| `registerChaiSaveToLibrary(Component)`    | `chaicore` | Replace "Save to Library" dialog      |
| `registerChaiPreImportHTMLHook(fn)`       | `chaicore` | Transform HTML before block import    |

### Extend UI Setup Pattern

```ts
// chai-setup.ts  ← module-level, imported once before builder mounts
import { registerChaiSlot, CHAI_SLOT_IDS, registerChaiHook, CHAI_HOOKS } from "chaicore";

registerChaiSlot(CHAI_SLOT_IDS.TOPBAR_RIGHT, MyButton);
registerChaiHook(CHAI_HOOKS.BEFORE_SAVE_PAGE, myHook);
```

```tsx
// editor/page.tsx
"use client";
import "../chai-setup";
import { ChaiWebsiteBuilder } from "chaicore";
export default function EditorPage() {
  return <ChaiWebsiteBuilder {...props} />;
}
```
