---
name: ui-stack-astro
description: "Building with Astro: when it fits, zero JavaScript by default, islands with client directives, content collections with schemas, layouts and components, images with astro:assets, view transitions, integrations for React, Vue or Svelte, server output and adapters, and build checks. Read when the project uses Astro or is a content site choosing a stack."
---

# Astro

Astro used by habit becomes a single-page app in a wrapper: `client:load` on
every component, content typed into arrays, full-size images in `public/`,
a menu script that dies after the first client-side navigation. Its point
is the reverse: HTML from the server, JavaScript only where a part must
behave. This covers Astro 6 and 7 (current in 2026, Node 22.12 or later);
check `package.json`, as Astro 5 still had `Astro.glob` and
`<ViewTransitions />`.

## 1. When it fits

- Content read more than operated: docs, blogs, product sites, portfolios,
  a local business, a catalogue. Not an app behind a sign-in with shared
  state on every screen: Vite with React, SvelteKit or Next.js instead
  (`ui-stack-react`, `ui-stack-svelte`, `ui-stack-next`).
- `npm create astro@latest` starts a project; `npx astro add <name>`
  installs an integration and edits the config.

```
src/pages/           routes: index.astro, blog/[...id].astro, rss.xml.ts, 404.astro
src/layouts/         Base.astro: <html lang>, head, header, footer, <slot />
src/components/      .astro components; islands in their framework (Search.tsx)
src/content/         Markdown, MDX, data; the schemas in src/content.config.ts
src/assets/          images Astro optimises (public/ is served untouched)
```

## 2. Components

```astro
---
// The frontmatter runs on the server (build or request time), never in the browser.
import type { HTMLAttributes } from "astro/types";
interface Props extends HTMLAttributes<"a"> { variant?: "primary" | "quiet" }
const { variant = "quiet", class: className, ...rest } = Astro.props;
---
<a class:list={["button", `button--${variant}`, className]} {...rest}><slot /></a>
```

- Named slots (`<slot name="aside" />`) with fallback content;
  `Astro.slots.has("aside")` drops an empty wrapper. `<style>` is scoped to
  the component; Markdown rendered inside is not its markup, so reach it
  with `:global()` from a wrapper (`.prose :global(h2)`).
- Expressions are escaped; `set:html` is not, so it takes only trusted or
  sanitised HTML. `is:inline` scripts skip bundling: only for tiny head
  scripts, such as setting the theme before the first paint.
- Astro 7's compiler errors on unclosed tags and no longer repairs invalid
  nesting, and its default `compressHTML: "jsx"` drops whitespace between
  inline elements as JSX does: write `{" "}` where a space must stay.

## 3. Islands: JavaScript only where it behaves

A framework component with no directive renders to HTML and ships nothing;
a `client:` directive makes it an island that hydrates.

| Directive | Hydrates | For |
|---|---|---|
| none | never | anything that only displays |
| `client:visible` | when scrolled into view | below the fold: a chart, a carousel, comments |
| `client:idle` | when the browser is idle | low-priority parts already in view |
| `client:media="(max-width: 767px)"` | when the query matches | a phone-only menu |
| `client:load` | at once | what the first screen needs now: search, the menu button |
| `client:only="react"` | in the browser, no server HTML | parts that need `window` (a map), with a fallback |

- The laziest that works (`client:visible={{ rootMargin: "200px" }}` starts
  early); `client:load` everywhere is a single-page app with extra steps.
  Props are serialised (plain data, no functions); children arrive as HTML.
  Islands share no context: use Nano Stores (`nanostores` with
  `@nanostores/react` or `@nanostores/vue`).
- Small behaviour needs no framework. A `<script>` in an `.astro` file is
  bundled, typed and run once as a module; as a custom element it works
  for every instance and after client-side navigation:

```astro
<copy-code data-code={code}><button type="button">Copy</button></copy-code>
<script>
  customElements.define("copy-code", class extends HTMLElement {
    connectedCallback() {
      const button = this.querySelector("button")!;
      button.onclick = async () => {
        await navigator.clipboard.writeText(this.dataset.code ?? "");
        button.textContent = "Copied";
      };
    }
  });
</script>
```

## 4. Content collections

```ts
// src/content.config.ts
import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/blog" }),
  schema: ({ image }) => z.object({
    title: z.string().max(70), description: z.string().max(160),
    published: z.coerce.date(), cover: image().optional(),
    draft: z.boolean().default(false),
  }),
});
export const collections = { blog };
```

```astro
---
// src/pages/blog/[...id].astro
import { getCollection, render } from "astro:content";
export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  return posts.map((post) => ({ params: { id: post.id }, props: { post } }));
}
const { post } = Astro.props;
const { Content } = await render(post);
---
<article class="prose"><h1>{post.data.title}</h1><Content /></article>
```

- A file that breaks the schema fails the build, naming file and field;
  types come with it (`CollectionEntry<"blog">`). `render()` also returns
  `headings`; `reference("authors")` links collections; `file()` loads one
  JSON or YAML file; live collections (Astro 6 and later) load per request.
- `z` is Zod 4 from `astro/zod` (`z.email()`, `z.url()`); `Astro.glob` is
  gone (a collection, or `import.meta.glob`). MDX via `npx astro add mdx`.
- Shiki highlights Markdown code (`markdown.shikiConfig.themes`, light and
  dark, `ui-themes`). Astro 7 renders Markdown with Sätteri: remark and
  rehype plugins need `markdown.processor: unified({ remarkPlugins,
  rehypePlugins })`, `unified` imported from `@astrojs/markdown-remark`.

## 5. Routing and rendering

- File-based (`src/pages/about.astro` is `/about`), `404.astro`, endpoints
  such as `rss.xml.ts` exporting `GET`. Static by default; a page run per
  request (search, a signed-in area, a form) needs an adapter (`npx astro
  add node`, `vercel`, `netlify`, `cloudflare`) and `export const prerender
  = false`; `output: "server"` only when most pages are dynamic.
- `<Recommendations server:defer>` with a `slot="fallback"` placeholder (a
  server island) puts one per-person part on an otherwise cached page.
- `src/middleware.ts` (`defineMiddleware`) for sessions and redirects via
  `Astro.locals`; Actions (`astro:actions`) for form posts, validated on
  the server. `astro:env` types the environment; `PUBLIC_` variables ship
  to every browser, so secrets never carry that prefix.

## 6. Images and fonts

```astro
---
import { Picture } from "astro:assets";
import shopFront from "../assets/shop-front.jpg";
---
<Picture src={shopFront} formats={["avif", "webp"]} alt="The shop front on [street]"
  widths={[480, 800, 1200]} sizes="(min-width: 1024px) 50vw, 100vw" priority />
```

- Images imported from `src/` are optimised and sized from the file;
  `public/` is copied untouched; remote ones need `image.remotePatterns`;
  `alt` is required (empty for decoration). Both are lazy by default:
  `priority` (eager, high fetch priority) only on the first screen's
  largest image; `layout="constrained"` writes `srcset` and `sizes`.
- The Fonts API self-hosts at build: `fonts: [{ provider:
  fontProviders.fontsource(), name: "Fraunces", cssVariable:
  "--font-display" }]` in the config, `<Font cssVariable="--font-display"
  preload />` (from `astro:assets`) in the head, preload above the fold only.

## 7. Styles, themes, view transitions

- Tokens as custom properties in one file the base layout imports;
  Tailwind v4 via `npx astro add tailwind` (tokens in `@theme`,
  `ui-stack-tailwind`); an `is:inline` head script sets the theme before
  the first paint (`ui-themes`).
- Between pages, the browser's own transitions and no script:
  `@view-transition { navigation: auto; }` inside `@media
  (prefers-reduced-motion: no-preference)` (Chromium, Safari 18.2 and
  later; others just load) (`motion-interface`).
- `<ClientRouter />` (`astro:transitions`) when state must survive
  navigation (`transition:persist`, `transition:name`); it turns its
  animations off under reduced motion. Its trap: bundled scripts run once,
  so page setup goes in `document.addEventListener("astro:page-load",
  setup)` or in custom elements.

## 8. Head, docs, other frameworks

- A head component: `<title>`, description, canonical
  (`new URL(Astro.url.pathname, Astro.site)`), Open Graph; `site` in the
  config (canonical, `@astrojs/sitemap` and `@astrojs/rss` need it); `lang`
  on `<html>`; `i18n` routing (`frontend-seo`, `i18n`); `prefetch: true`;
  `security: { csp: true }` for a Content Security Policy.
- Docs: `npm create astro@latest -- --template starlight` (sidebar, Pagefind
  search, both themes, code blocks with copy, `:::note` asides, `<Tabs
  syncKey="pkg">`, edit links; `ui-page-docs`), themed through
  `--sl-color-accent`, `--sl-font` and component overrides.
- `npx astro add react` (or `vue`, `svelte`): one framework, following its
  skill (`ui-stack-react`, `ui-stack-vue`, `ui-stack-svelte`).

## Check it

- `npx astro check` (it offers to install `@astrojs/check` and
  `typescript`): types in `.astro` files, props, collections.
- `npx astro build` fails on a schema mismatch, a broken import, a missing
  `alt` or an unclosed tag; in `dist/`, display-only pages load no script.
- The `preview` tool: `url` `http://localhost:4321/`, `start` `npm run dev
  -- --port 4321`. With `<ClientRouter />`, navigate three pages and use
  each interactive part again. Then `ui_check`.

## Avoid

`client:load` on every component; a whole React app in one island for a
content page; `client:only` for content that belongs in the HTML; content
in hand-typed arrays; `Astro.glob`; content images in `public/`;
`set:html` with anything unsanitised; secrets under `PUBLIC_`; `output:
"server"` for a site that could be static; scripts that die after a
client-side navigation; a font stylesheet from a CDN blocking first paint.
