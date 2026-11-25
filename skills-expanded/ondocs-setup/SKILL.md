---
name: ondocs-setup
description: Add ondocs, open-source Ask AI for docs with an MCP server for agents, to a docs site built with Starlight or Astro, Docusaurus, VitePress, Next.js, Fumadocs, Nextra, or a static generator such as Hugo, Jekyll or MkDocs. Use when asked to add Ask AI, an AI search or chat box, an MCP server or llms.txt to a docs site, or to set up, try or deploy ondocs. Finds the framework, installs the peer dependencies, adds the plugin, tries it locally with no API key, then writes the endpoint for the host with ondocs init.
---

# Add ondocs to a docs site

ondocs builds one index, `ask-index.json`, with the site. An endpoint deployed next to the site answers from it: an "Ask AI" dialog for readers, an MCP server at `/api/mcp` for coding agents, and `llms.txt` with a Markdown copy of each page. There is no hosted service, and the model key is the site owner's.

Work in the docs site's folder, the one with its `package.json` and framework config. When you need more than this skill says, read the guide for the site's framework: every docs page has a Markdown copy at its URL plus `.md`, such as https://ondocs.vercel.app/docs/astro.md, and https://ondocs.vercel.app/llms.txt lists them all.

## 1. Find the framework

| The site has                                                               | It is              | What you add                                      |
| -------------------------------------------------------------------------- | ------------------ | ------------------------------------------------- |
| `astro.config.*` and `@astrojs/starlight` in `package.json`                | Starlight          | The plugin from `ondocs/starlight`                |
| `astro.config.*` without Starlight                                         | Astro              | The integration from `ondocs/astro`               |
| `docusaurus.config.*`                                                      | Docusaurus 3       | The plugin `ondocs/docusaurus`                    |
| `.vitepress/config.*` or `docs/.vitepress/config.*`                        | VitePress          | `withOndocs` from `ondocs/vitepress`              |
| `next.config.*` and `fumadocs-core` or `nextra` in `package.json`          | Fumadocs or Nextra | An index from the CLI, routes and `<AskDialog />` |
| `next.config.*`                                                            | Next.js            | An index from the CLI, routes and `<AskDialog />` |
| `hugo.toml`, `_config.yml`, `mkdocs.yml`, an Eleventy config, or only HTML | A static site      | An index from the CLI and one script tag          |

Before you install, check two things:

- ondocs needs Node.js 22.13 or later: run `node --version`.
- ondocs needs AI SDK 6 (6.0.16 or later) or 7 (7.0.95 or later). If `package.json` already has `ai` at version 5 or lower, stop and ask the user before you move it to 7. An older 6 or 7 only needs `ai` and its provider packages updated within that version.

## 2. Install the packages

Use the project's package manager: `pnpm add` where there is a `pnpm-lock.yaml`, `yarn add` with a `yarn.lock`, `bun add` with a `bun.lock`, and `npm i` otherwise. The packages are the same.

Starlight, Astro and VitePress, whose dialog comes with its own React:

```sh
npm i ondocs ai @ai-sdk/openai
```

Docusaurus, Next.js, Fumadocs and Nextra:

```sh
npm i ondocs ai @ai-sdk/openai @radix-ui/react-dialog cmdk
```

A static site needs nothing installed to build its index, because `npx ondocs` runs the CLI. `npx ondocs init`, in step 5, prints what its endpoint needs.

Install `ondocs` itself, not only `starlight-ondocs` or `docusaurus-plugin-ondocs`: with pnpm, those two alone give the project no `ondocs` command and no `ondocs/...` modules. If the version that installs is older than `npm view ondocs version`, the package manager's release-age gate held the newest back: see [Troubleshooting](https://ondocs.vercel.app/docs/troubleshooting#an-older-version-installs-or-none-does).

## 3. Add it to the site

Edit the config the site already has, and keep everything in it.

**Starlight.** Add the plugin to Starlight's `plugins` in `astro.config.mjs`:

```js
// astro.config.mjs
import starlight from '@astrojs/starlight';
import ondocs from 'ondocs/starlight';
import { defineConfig } from 'astro/config';

export default defineConfig({
  integrations: [starlight({ title: 'Acme Docs', plugins: [ondocs()] })],
});
```

**Astro without Starlight.** Add the integration to `integrations`:

```js
// astro.config.mjs
import ondocs from 'ondocs/astro';
import { defineConfig } from 'astro/config';

export default defineConfig({ integrations: [ondocs()] });
```

**Docusaurus.** Add the plugin to `plugins`:

```ts
// docusaurus.config.ts
export default {
  // …
  plugins: ['ondocs/docusaurus'],
};
```

**VitePress.** Wrap the config in `withOndocs`:

```ts
// .vitepress/config.mts
import { defineConfig } from 'vitepress';
import { withOndocs } from 'ondocs/vitepress';

export default withOndocs(
  defineConfig({
    title: 'Acme Docs',
    // ...the rest of your config, as it is
  }),
);
```

After every build, the plugins index the pages the site serves, write `llms.txt` and the `.md` copies, and add an "Ask AI" button that opens the dialog, also with ⌘I (Ctrl+I outside macOS). The index is written to `dist/ask-index.json` for Astro and Starlight (`dist/client/ask-index.json` with an SSR adapter), `build/ask-index.json` for Docusaurus, and `.vitepress/dist/ask-index.json` for VitePress. There is nothing to commit.

**Next.js.** Build the index with the CLI before every build, from the folder that holds the pages, with `--base-url` set to the path the app serves them at. The OpenAI embedding needs `OPENAI_API_KEY` where the site builds:

```json
{
  "scripts": {
    "index": "ondocs index content --base-url /docs -e openai:text-embedding-3-small --dimensions 512 --llms-txt public",
    "prebuild": "npm run index"
  }
}
```

Then render the dialog once: put this client component in `app/ask.tsx`, and render `<Ask />` in `app/layout.tsx`:

```tsx
// app/ask.tsx
'use client';
import { AskDialog } from 'ondocs/react';
import 'ondocs/react/styles.css';
import 'ondocs/embed/launcher.css';
import { useRouter } from 'next/navigation';

export function Ask() {
  const router = useRouter();
  return (
    <AskDialog
      launcher
      suggestions={['How do I install it?', 'Which runtimes are supported?']}
      onNavigate={(url, event) => {
        event.preventDefault();
        router.push(url);
      }}
    />
  );
}
```

`npx ondocs init`, in step 5, writes the routes: `app/api/ask/route.ts` and `app/api/mcp/route.ts`. Fumadocs and Nextra have URL rules of their own, so take the index command from [Fumadocs](https://ondocs.vercel.app/docs/fumadocs) or [Nextra](https://ondocs.vercel.app/docs/nextra).

**Static sites.** Build the site, then index the HTML it built, into the folder it deploys: `public` after Hugo, `_site` after Jekyll or Eleventy, and `site` after MkDocs. On a GitHub Pages project site, such as `https://user.github.io/repo`, add `--base-url /repo`.

```sh
npx ondocs index public -o public/ask-index.json -e none   # keyword-only; leave out -e none to embed with OPENAI_API_KEY
```

`npx ondocs init`, in step 5, prints the script tag to add to the base template, with the current version. A plain HTML site has no config for it to find, so pass the folder with `--out`, as in `npx ondocs init --out public`.

## 4. Try it locally, with no API key

`ondocs dev` serves the ask endpoint and the MCP server on your machine, from the index. Without `OPENAI_API_KEY` or `AI_GATEWAY_API_KEY`, a mock model answers by quoting the docs, with citations.

With a plugin, build the site once with its `build` script. Without a key, the build prints "No embedding model: building a keyword-only index", which is expected. Then run `npx ondocs dev` in the site's folder: it finds the index where the plugin wrote it.

With the CLI, index with the mock model: put the folder the pages are in where `./docs` is, and add the `--base-url` from step 3 if there is one. Then start the server:

```sh
npx ondocs index ./docs -e mock   # writes ask-index.json
npx ondocs dev                    # serves POST http://localhost:8787/api/ask
```

`ondocs dev` runs until it is stopped, so start it in the background. Ask it a question in words from one of the pages:

```sh
curl -sN http://localhost:8787/api/ask -H 'content-type: application/json' -d '{"question":"How do I install it?"}'
```

The answer streams back as `data:` lines: `source-url` parts with the URLs of the pages it cites, then `text-delta` parts with the answer. An "I don't know" answer means no page shares enough words with the question. To see the dialog, start the site's own dev server with `ASK_ENDPOINT=http://localhost:8787/api/ask` set (the plugins post there when it is set), or pass it to `<AskDialog />` as `endpoint`, or to the script tag as `data-endpoint`. Stop `ondocs dev` when you are done.

The mock `ask-index.json` is only for trying it out. In a Next.js app, where it is the file the routes import, build it again with the command from step 3 before you commit or deploy, because the endpoint refuses an index built with another embedding model. Elsewhere, delete it when you are done.

## 5. Write the endpoint for the host

`npx ondocs init` writes the ask endpoint and the MCP endpoint for the host, each with a rate limit and a daily budget. Look at what it would write first:

```sh
npx ondocs init --dry-run   # prints every file it would write, and writes nothing
npx ondocs init
```

- **The host.** It finds the host from `vercel.json`, `netlify.toml`, a wrangler config or a GitHub Pages workflow. When it cannot tell, it asks, or, with no terminal to ask in, stops and names the flag. Ask the user where the site is hosted, then pass `--host vercel`, `--host netlify`, `--host cloudflare` or `--host github-pages`. `github-pages` also covers any other host that only serves files.
- **GitHub Pages.** It writes a Cloudflare Worker in `ondocs-worker/` that reads the index from the live site and answers with Workers AI, with no API key. Pass the site's public URL with `--site-url https://user.github.io/repo` when its config has none.
- **Astro or Starlight with an SSR adapter.** It writes nothing, and says so: the integration serves `/api/ask` and `/api/mcp` itself.
- **Files that already exist.** A file it would replace, such as an `api/ask.ts` the site already has, stays as it is unless you pass `--yes`. Show the user the difference before you do.

It prints each file it wrote, the environment variables to set and where, and the steps left: the packages to install, the dialog to add and the deploy. Do the steps that change the project, and leave the deploy to the user. It exits with 0 when everything is written, 1 when it left a file or an edit for you to make by hand, and 2 on a usage error.

## 6. Hand over to the user

Don't deploy, create accounts or write a model key into any file. Tell the user:

- To set `OPENAI_API_KEY` where the site builds and where the endpoint runs, unless the endpoint is the GitHub Pages Worker on Workers AI, and to set a spend limit with the model provider, which is the only hard cap.
- How to deploy, as `npx ondocs init` printed it.
- That once it is live, agents connect to the site's MCP server, as in `claude mcp add --transport http acme-docs https://docs.acme.dev/api/mcp` with the site's URL.

## When something fails

[Troubleshooting](https://ondocs.vercel.app/docs/troubleshooting) lists the messages a new site shows most often, with the cause and the fix of each. The most common:

- `ondocs: command not found`, or `Rolldown failed to resolve import "ondocs/react/styles.css"`: install `ondocs` itself, as in step 2. See [ondocs: command not found](https://ondocs.vercel.app/docs/troubleshooting#ondocs-command-not-found).
- An option or import from the docs does nothing or fails: the installed version is older than the docs. Check it with `npm ls ondocs`. See [An option from these docs does nothing](https://ondocs.vercel.app/docs/troubleshooting#an-option-from-these-docs-does-nothing).
- The dialog shows an error: the endpoint's log has the cause, which the browser never gets.
