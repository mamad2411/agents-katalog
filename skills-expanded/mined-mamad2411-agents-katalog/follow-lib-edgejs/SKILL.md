---
name: follow-lib-edgejs
description: Set up and use the Edge.js template engine for Node.js
argument-hint: "[scope]"
related:
  - report
  - deep-validate
  - follow-lib-react
  - follow-lib-solidjs
---

## Goal

Set up and use the Edge.js template engine for Node.js with its near-JavaScript syntax, components, slots, partials, and state management, per the official documentation

## Scope

For Node.js/Bun projects that need an ESM-only backend template engine with no build step — standalone or inside AdonisJS — use this skill only when rendering HTML server-side with `.edge` templates

- If you need an interactive UI or client-side component framework → use `/follow-lib-react` or `/follow-lib-solidjs` instead
- If the project is AdonisJS full-stack → follow AdonisJS view conventions, which already use Edge as the engine

- Install `edge.js` via `bun` or `npm`
- Create an `Edge` instance, mount disks, and enable cache
- Write templates with `.edge` syntax
- Use conditionals, loops, partials, components, slots, and layouts
- Manage template state: globals, locals, rendering data, inline variables
- Extend with plugins and custom tags when needed

- Latest: `edge.js@6.5.1` (verified 2026-09-13)

## Execute

### 1. Check Precondition

> Goal: verify the environment before starting

1. Confirm there is a `package.json` and the project uses ESM (`"type": "module"` or `.mjs` files)
2. Confirm a latest Bun or Node.js version that supports ESM is available
3. Check the `edge.js` version in `package.json` or at https://www.npmjs.com/package/edge.js
4. If there is no project → stop and `/ask-me` to create one first

### 2. Install Edge.js

> Goal: install `edge.js` in the project

1. Run `bun add edge.js` (runtime dependency — if the project uses another package manager, use the equivalent command)
2. Verify `edge.js` is in `dependencies` of `package.json`
3. With TypeScript, verify `tsconfig.json` supports ESM (`module: "NodeNext"` or `"ESNext"`)
4. Never hardcode credentials or secrets in templates or config

### 3. Configure Edge Instance

> Goal: create and configure the Edge instance

1. Create `edge.ts` or `edge.js` for the singleton instance
2. Use `Edge.create()` and `edge.mount(new URL('./views', import.meta.url))`
3. Enable cache in production to avoid repeated re-compilation

```ts
import { Edge } from 'edge.js'

export const edge = Edge.create({
  cache: process.env.NODE_ENV === 'production'
})

edge.mount(new URL('./views', import.meta.url))
```

4. With multiple disks/themes use `edge.mount('diskName', new URL('path', import.meta.url))` and render with `diskName::template`
5. Beware the reserved keywords `template`, `$context`, `state`, `$filename` — don't use them as state names

### 4. Write Templates

> Goal: write `.edge` files per the syntax

1. Create `.edge` files in `views/` or `templates/`
2. Use `{{ expression }}` for interpolation — the expression can be any JavaScript
3. Use `@if(condition)`, `@elseif`, `@else`, `@end` for conditionals
4. Use `@each(item in items)` or `@each((item, index) in items)` for loops
5. Use `@include('partial')` for partials and `@includeIf(condition, 'partial')` for conditional include
6. Use `{{-- comment --}}` for comments
7. See the API surface in `references/apis.md`

### 5. Use Components and Layouts

> Goal: build reusable UI with components and slots

1. Create components in `views/components/<name>.edge`
2. Use `@component('components/button', { props })` or `@!component('components/button', { props })` for auto-close
3. Use `@<componentTag>()` when the component lives in the `components/` directory
4. Use `$props` for props handling and `$slots.main()` for slots
5. Create layouts with `@layout.app({ title: '...' })` and `@slot('main')` / `@endslot`
6. See the API surface in `references/apis.md`

### 6. Manage Template State

> Goal: pass data to templates correctly

1. Use `edge.global(name, value)` for state shared across every template
2. Use `edge.createRenderer().share({ ... })` for isolated per-request locals
3. Use `await edge.render('view', data)` for rendering data not shared with components
4. Use `@let(name = value)` and `@assign(name = newValue)` for inline variables
5. See the API surface in `references/apis.md`

### 7. Render and Integrate

> Goal: render templates at runtime

1. Use `await edge.render('home', data)` to render from a disk
2. Use `await edge.renderRaw(templateString, data)` for in-memory templates
3. Use `renderSync` / `renderRawSync` if synchronous is required, but async is recommended
4. Integrate with an HTTP server by returning the `html` string to the client

```ts
import { createServer } from 'node:http'
import { edge } from './edge.js'

const server = createServer(async (req, res) => {
  const html = await edge.render('home', { username: 'virk' })
  res.setHeader('content-type', 'text/html')
  res.end(html)
})

server.listen(3000)
```

### 8. Extend Edge

> Goal: extend capabilities with plugins and custom tags

1. Use `edge.use(plugin)` for plugins such as `edge-iconify` for SVG icons
2. Install `edge-iconify` and `@iconify-json/<set>` if using icons
3. Use `edge.registerTag(tagContract)` for specialized custom tags
4. See custom tag details in the official documentation

### 9. Validate and Ship

> Goal: verify correctness before delivery

1. Run `bun run typecheck` or `tsc --noEmit` if using TypeScript
2. Run `bun test` or the existing test suite
3. Verify no reserved keywords are overridden
4. Run `/report table` summarizing status with columns: `No.`, `Check`, `Status`, `Notes`
5. Run `/deep-validate` then `/ship`

## Rules

### 1. ESM Only

- `edge.js` is an ESM-only package — use `import`, never `require`
- Set `"type": "module"` in `package.json` or use the `.mjs` extension

### 2. Template Files

- Use the `.edge` extension for template files
- Keep templates in `views/` or `templates/` per the project convention
- Use `edge.mount()` to register a disk before rendering

### 3. Security

- `{{ }}` output is HTML-escaped by default, preventing XSS
- Use `{{{ }}` or `html.safe()` only with trusted content
- Never put secrets, credentials, or hardcoded API keys in templates

### 4. Syntax Discipline

- Edge tags (`@if`, `@each`, `@component`, etc.) must be on their own line
- Append `~` to a tag when you want to swallow the newline
- Prefix a tag name with `!` for auto-closing block tags, e.g. `@!component(...)`
- Comments use `{{-- ... --}}`

### 5. Performance

- Enable cache in production with `cache: process.env.NODE_ENV === 'production'`
- Avoid re-rendering the same template many times in a loop
- Prefer async `render`

### 6. State Management

- Never use `template`, `$context`, `state`, `$filename` as template state names
- Separate globals, locals, rendering data, and inline variables by the correct scope

### 7. Package Manager

- Default to `bun add` for JS/TS projects
- If the project uses another package manager, follow its ecosystem (`npm i`, `pnpm add`, `yarn add`)

- Use /report if needed
- Use /deep-validate if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `edge.js` is installed and configured correctly with ESM
- The `Edge` instance mounts disks and enables cache in production
- Templates work with interpolation, conditionals, loops, partials, components, slots
- Template state is managed via globals, locals, rendering data, and inline variables
- Production has cache enabled
- Typecheck and tests pass
