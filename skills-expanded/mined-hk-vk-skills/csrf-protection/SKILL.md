---
name: csrf-protection
description: [!NOTE]
For the RPC types to work properly in a monorepo, in both the Client's and Server's tsconfig.json files, set `"strict": true` in `compilerOptions`. [Read more.](https://github.com/honojs/hono/issues/2270#issuecomment-2143745118)
metadata:
  source: llms.txt
  source_url: https://hono.dev/llms-full.txt
  generated: 2026-06-28T07:26:25.408Z
---

# CSRF Protection

> [!NOTE]
For the RPC types to work properly in a monorepo, in both the Client's and Server's tsconfig.json files, set `"strict": true` in `compilerOptions`. [Read more.](https://github.com/honojs/hono/issues/2270#issuecomment-2143745118)

[!NOTE]
For the RPC types to work properly in a monorepo, in both the Client's and Server's tsconfig.json files, set `"strict": true` in `compilerOptions`. [Read more.](https://github.com/honojs/hono/issues/2270#issuecomment-2143745118)

## Available Resources

### Quick Start

### Features

### Use-cases

### Who is using Hono?

- **Drivly**
  - URL: https://driv.ly/

- **repeat.dev**
  - URL: https://repeat.dev/

### Hono in 1 minute

### Ultrafast

### Lightweight

### Multiple routers

### Web Standards

### Middleware & Helpers

- **Basic Authentication**
  - URL: /docs/middleware/builtin/basic-auth

- **Bearer Authentication**
  - URL: /docs/middleware/builtin/bearer-auth

- **Body Limit**
  - URL: /docs/middleware/builtin/body-limit

- **Cache**
  - URL: /docs/middleware/builtin/cache

- **Compress**
  - URL: /docs/middleware/builtin/compress

- **Context Storage**
  - URL: /docs/middleware/builtin/context-storage

- **Cookie**
  - URL: /docs/helpers/cookie

- **CORS**
  - URL: /docs/middleware/builtin/cors

- **ETag**
  - URL: /docs/middleware/builtin/etag

- **html**
  - URL: /docs/helpers/html

- **JSX**
  - URL: /docs/guides/jsx

- **JWT Authentication**
  - URL: /docs/middleware/builtin/jwt

- **Logger**
  - URL: /docs/middleware/builtin/logger

- **Language**
  - URL: /docs/middleware/builtin/language

- **Pretty JSON**
  - URL: /docs/middleware/builtin/pretty-json

- **Secure Headers**
  - URL: /docs/middleware/builtin/secure-headers

- **SSG**
  - URL: /docs/helpers/ssg

- **Streaming**
  - URL: /docs/helpers/streaming

- **GraphQL Server**
  - URL: https://github.com/honojs/middleware/tree/main/packages/graphql-server

- **Firebase Authentication**
  - URL: https://github.com/honojs/middleware/tree/main/packages/firebase-auth

- **Sentry**
  - URL: https://github.com/honojs/middleware/tree/main/packages/sentry

### Developer Experience

### Throwing HTTPExceptions

### Handling HTTPExceptions

### param()

### query()

### queries()

### header()

### parseBody()

### json()

### text()

### arrayBuffer()

### blob()

### formData()

### valid()

### routePath

### matchedRoutes

### path

### url

### method

### raw

### cloneRawRequest()

### req

### status()

### header()

### body()

### text()

### json()

### html()

### notFound()

### redirect()

### res

### set() / get()

### var

### render() / setRenderer()

### executionCtx

### event

### env

### error

### ContextVariableMap

### Basic

### Path Parameter

### Regexp

### Including slashes

### Chained route

### Grouping

### Grouping without changing base

### Base path

### Routing with hostname

### Routing with `host` Header value

### Routing priority

### Grouping ordering

### Methods

### Not Found

### Error Handling

### fire()

### fetch()

### request()

### mount()

### strict mode

### router option

### Generics

### `hono`

### `hono/quick`

### `hono/tiny`

### Which preset should I use?

### Is there an official Renovate config for Hono?

### Contributing

### Sponsoring

- **Sponsor @yusukebe on GitHub Sponsors**
  - URL: https://github.com/sponsors/yusukebe

- **Sponsor @usualoma on GitHub Sponsors**
  - URL: https://github.com/sponsors/usualoma

### Other Resources

- **Link**: GitHub repository: <a href="
  - URL: https://github.com/honojs">https://github.com/honojs</a>

- **Link**: npm registry: <a href="
  - URL: https://www.npmjs.com/package/hono">https://www.npmjs.com/package/hono</a>

- **Link**: JSR: <a href="
  - URL: https://jsr.io/@hono/hono">https://jsr.io/@hono/hono</a>

### Settings

### Usage

### Metadata hoisting

### Fragment

### `PropsWithChildren`

### Inserting Raw HTML

### Memoization

### Context

### Async Component

### Suspense <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### ErrorBoundary <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### StreamingContext <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### Integration with html Middleware

### With JSX Renderer Middleware

### Override type definitions

### Available Helpers

- **Accepts**
  - URL: /docs/helpers/accepts

- **Adapter**
  - URL: /docs/helpers/adapter

- **Cookie**
  - URL: /docs/helpers/cookie

- **css**
  - URL: /docs/helpers/css

- **Dev**
  - URL: /docs/helpers/dev

- **Factory**
  - URL: /docs/helpers/factory

- **html**
  - URL: /docs/helpers/html

- **JWT**
  - URL: /docs/helpers/jwt

- **SSG**
  - URL: /docs/helpers/ssg

- **Streaming**
  - URL: /docs/helpers/streaming

- **Testing**
  - URL: /docs/helpers/testing

- **WebSocket**
  - URL: /docs/helpers/websocket

### Definition of Middleware

### Execution order

### Built-in Middleware

### Custom Middleware

### Context access inside Middleware arguments

### Third-party Middleware

### Request and Response

### Env

### Manual validator

### Multiple validators

### With Zod

### Zod Validator Middleware

### Standard Schema Validator Middleware

### Counter example

### `render()`

### Hooks compatible with React

### `startViewTransition()` family

- **the `finish` promise becomes fulfilled**
  - URL: https://developer.mozilla.org/en-US/docs/Web/API/ViewTransition/finished

### The `hono/jsx/dom` runtime

### Server

### Client

### Status code

### Global Response

### Not Found

### Path parameters

### Headers

### `init` option

### `$url()`

### `$path()`

### File Uploads

### Custom `fetch` method

### Custom query serializer

### Infer

### Parsing a Response with type-safety helper

### Using SWR

### Using RPC with larger applications

### Known issues

### Don't make "Controllers" when possible

### `factory.createHandlers()` in `hono/factory`

### Building a larger application

### HEAD Request Best Practices

### Passing arguments:

### Commonly used arguments

### Example flows

### Troubleshooting & tips

### Links & references

- **create-hono**
  - URL: https://github.com/honojs/create-hono

### Usage

### toSSG

### Generate File

### Middleware

### Plugins

### Import

### `sign()`

### `verify()`

### `decode()`

### Payload Validation

### Custom Error Types

### Supported AlgorithmTypes

### `getRouterName()`

### `showRoutes()`

### Options

### Import

### Usage

### Options

### `__Secure-` and `__Host-` prefix

### Following the best practices

- **RFC6265bis-13**
  - URL: https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-13

- **CHIPS-01**
  - URL: https://www.ietf.org/archive/id/draft-cutler-httpbis-partitioned-cookies-01.html

### Import

### `upgradeWebSocket()`

### RPC-mode

### Examples

### Import

### `testClient()`

### Import

### `createFactory()`

### `createMiddleware()`

### `factory.createHandlers()`

### `factory.createApp()`

### Import

### `stream()`

### `streamText()`

### `streamSSE()`

### Error Handling

### Import

### `env()`

- **`Deno.env`**
  - URL: https://docs.deno.com/runtime/manual/basics/env_variables

- **`Bun.env`**
  - URL: https://bun.com/guides/runtime/set-env

- **Environment Variables on Vercel**
  - URL: https://vercel.com/docs/projects/environment-variables

- **Environment Variables on AWS Lambda**
  - URL: https://docs.aws.amazon.com/lambda/latest/dg/samples-blank.html#samples-blank-architecture

- **not supported**
  - URL: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/add-origin-custom-headers.html

- **Netlify Contexts**
  - URL: https://docs.netlify.com/site-deploys/overview/#deploy-contexts

### `getRuntimeKey()`

### Import

### Usage

### Type Definitions

### Import

### Usage

### `matchedRoutes()`

### `routePath()`

### `baseRoutePath()`

### `basePath()`

### Import

### `accepts()`

### Options

### Import

### `html`

### `raw()`

### Tips

- **Link**: <
  - URL: https://marketplace.visualstudio.com/items?itemName=bierner.lit-html>

- **Link**: <
  - URL: https://github.com/MaxMEllon/vim-jsx-pretty>

### Import

### `proxy()`

### Import

### `css` <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### `keyframes` <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### `cx` <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### Usage in combination with [Secure Headers](/docs/middleware/builtin/secure-headers) middleware

### `createCssContext` <Badge style="vertical-align: middle;" type="warning" text="Experimental" />

### Security

### Tips

### Routers

### Cloudflare Workers

- **benchmarks/handle-event**
  - URL: https://github.com/honojs/hono/tree/main/benchmarks/handle-event

### Deno

- **benchmarks/deno**
  - URL: https://github.com/honojs/hono/tree/main/benchmarks/deno

- **Link**: Method: `bombardier --fasthttp -d 10s -c 100 '
  - URL: http://localhost:8000/user/lookup/username/foo'`

### Bun

- **SaltyAom/bun-http-framework-benchmark**
  - URL: https://github.com/SaltyAom/bun-http-framework-benchmark

### RegExpRouter

### TrieRouter

### SmartRouter

### LinearRouter

### PatternRouter

### Motivation

### RPC

- **Zod**
  - URL: https://zod.dev

- **Zod Validator Middleware**
  - URL: https://github.com/honojs/middleware/tree/main/packages/zod-validator

### Writing API

### Validation with Zod

### Sharing the Types

### Client

### With React

### 1. Setup

### 2. Hello World

### 3. Run

- **Link**: Make a GET request using cURL or Postman to `
  - URL: http://127.0.0.1:54321/functions/v1/hello-world/hello`:

### 4. Deploy

### 1. Install CLI

- **Install the Azure Functions Core Tools | Microsoft Learn**
  - URL: https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-typescript?pivots=nodejs-model-v4#install-the-azure-functions-core-tools

### 2. Setup

### 3. Hello World

### 4. Run

### 5. Deploy

### 1. Setup

### 2. Hello World

### 3. Deploy

### Serve Binary data

### Access AWS Lambda Object

### Access RequestContext

### Lambda response streaming

### 1. Install Bun

### 2. Setup

### 3. Hello World

### 4. Run

### Change port number

### Serve static files

### Testing

### 1. Setup

### 2. Hello World

### 3. Run

### 4. Deploy

- **Cloudflare dashboard**
  - URL: https://dash.cloudflare.com

### Bindings

### Client-side

### Cloudflare Pages Middleware

### 1. Setup

### 2. Hello World

### 3. Run

### Change port number

### WebSocket

### Access the raw Node.js APIs

### Serve static files

### http2

### Building & Deployment

### 1. Setup

### 2. Hello World

### 3. Setup serverless-devs

### 4. Deploy

### 1. Setup

### 2. Hello World

### 3. Run

### 4. Deploy

### Pages Router

### 1. Setup

### 2. Hello World

### 3. Run

### 4. Deploy

### Using Hono with other event handlers

### Serve static files

### Types

### Testing

### Bindings

### Using Variables in Middleware

### Deploy from GitHub Actions

### Load env when local development

### 1. Setup

### 2. Hello World

### 3. Run

### 4. Deploy

### Further reading

### 1. Setup

### 2. Hello World

### 3. Run

### 4. Deploy

### Bindings

### 1. Setup

### 2. Hello World

### 3. Deploy

### Callback

### 1. Setup

### 2. Hello World

### 3. Run

### 4. Deploy

### `Context`

### 1. Install Deno

### 2. Setup

### 3. Hello World

### 4. Run

### Change port number

### Serve static files

### Deno Deploy

### Testing

### npm and JSR

### 1. Setup

### 2. Set up WIT interface & dependencies

### 3. Hello Wasm

### 4. Build

### 5. Run

### More information

- **Bytecode Alliance Zulip**
  - URL: https://bytecodealliance.zulipchat.com

- **Jco repository**
  - URL: https://github.com/bytecodealliance/jco

- **componentize-js repository**
  - URL: https://github.com/bytecodealliance/componentize-js

### Starter

### Hello World

### Return JSON

### Request and Response

### Return HTML

### Return raw Response

### Using Middleware

### Adapter

### Next step

### 1. Setup

### 2. Hello World

### 3. Run

### 1. Install the CLI

### 2. Project setup

### 3. Hello World

### 4. Deploy

### Changing runtimes

- **Node.js**
  - URL: /docs/getting-started/nodejs#building-deployment

- **Bun**
  - URL: https://bun.com/guides/ecosystem/docker

- **Deno**
  - URL: https://docs.deno.com/examples/google_cloud_run_tutorial

- **Auth.js(Next Auth)**
  - URL: https://github.com/honojs/middleware/tree/main/packages/auth-js

- **Casbin**
  - URL: https://github.com/honojs/middleware/tree/main/packages/casbin

- **Clerk Auth**
  - URL: https://github.com/honojs/middleware/tree/main/packages/clerk-auth

- **Cloudflare Access**
  - URL: https://github.com/honojs/middleware/tree/main/packages/cloudflare-access

- **OAuth Providers**
  - URL: https://github.com/honojs/middleware/tree/main/packages/oauth-providers

- **OIDC Auth**
  - URL: https://github.com/honojs/middleware/tree/main/packages/oidc-auth

- **Firebase Auth**
  - URL: https://github.com/honojs/middleware/tree/main/packages/firebase-auth

- **Verify RSA JWT (JWKS)**
  - URL: https://github.com/wataruoguchi/verify-rsa-jwt-cloudflare-worker

- **Stytch Auth**
  - URL: https://github.com/honojs/middleware/tree/main/packages/stytch-auth

- **Ajv Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/ajv-validator

- **ArkType Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/arktype-validator

- **Class Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/class-validator

- **Conform Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/conform-validator

- **Effect Schema Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/effect-validator

- **Standard Schema Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/standard-validator

- **TypeBox Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/typebox-validator

- **Typia Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/typia-validator

- **unknownutil Validator**
  - URL: https://github.com/ryoppippi/hono-unknownutil-validator

- **Valibot Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/valibot-validator

- **Zod Validator**
  - URL: https://github.com/honojs/middleware/tree/main/packages/zod-validator

- **Zod OpenAPI**
  - URL: https://github.com/honojs/middleware/tree/main/packages/zod-openapi

- **Scalar**
  - URL: https://github.com/scalar/scalar/tree/main/integrations/hono

- **Swagger UI**
  - URL: https://github.com/honojs/middleware/tree/main/packages/swagger-ui

- **Swagger Editor**
  - URL: https://github.com/honojs/middleware/tree/main/packages/swagger-editor

- **Hono OpenAPI**
  - URL: https://github.com/rhinobase/hono-openapi

- **hono-zod-openapi**
  - URL: https://github.com/paolostyle/hono-zod-openapi

- **ESLint Config**
  - URL: https://github.com/honojs/middleware/tree/main/packages/eslint-config

- **SSG Plugin Essential**
  - URL: https://github.com/honojs/middleware/tree/main/packages/ssg-plugins-essential

- **Apitally (API monitoring & analytics)**
  - URL: https://docs.apitally.io/frameworks/hono

- **Highlight.io**
  - URL: https://www.highlight.io/docs/getting-started/backend-sdk/js/hono

- **LogTape (Logging)**
  - URL: https://logtape.org/manual/integrations#hono

- **OpenTelemetry**
  - URL: https://github.com/honojs/middleware/tree/main/packages/otel

- **Prometheus Metrics**
  - URL: https://github.com/honojs/middleware/tree/main/packages/prometheus

- **Sentry**
  - URL: https://github.com/honojs/middleware/tree/main/packages/sentry

- **Pino logger**
  - URL: https://github.com/maou-shonen/hono-pino

- **GraphQL Server**
  - URL: https://github.com/honojs/middleware/tree/main/packages/graphql-server

- **oRPC**
  - URL: https://orpc.dev/docs/adapters/hono

- **tRPC Server**
  - URL: https://github.com/honojs/middleware/tree/main/packages/trpc-server

- **Bun Transpiler**
  - URL: https://github.com/honojs/middleware/tree/main/packages/bun-transpiler

- **esbuild Transpiler**
  - URL: https://github.com/honojs/middleware/tree/main/packages/esbuild-transpiler

- **Qwik City**
  - URL: https://github.com/honojs/middleware/tree/main/packages/qwik-city

- **React Compatibility**
  - URL: https://github.com/honojs/middleware/tree/main/packages/react-compat

- **React Renderer**
  - URL: https://github.com/honojs/middleware/tree/main/packages/react-renderer

- **GlideMQ (Message Queue REST API + SSE)**
  - URL: https://github.com/avifenesh/glidemq-hono

- **Intlayer i18n**
  - URL: https://intlayer.org/doc/environment/hono

- **Bun Compress**
  - URL: https://github.com/honojs/middleware/tree/main/packages/bun-compress

- **Cap Checkpoint**
  - URL: https://capjs.js.org/guide/middleware/hono.html

- **Event Emitter**
  - URL: https://github.com/honojs/middleware/tree/main/packages/event-emitter

- **Geo**
  - URL: https://github.com/ktkongtong/hono-geo-middleware/tree/main/packages/middleware

- **Hono Rate Limiter**
  - URL: https://github.com/rhinobase/hono-rate-limiter

- **Hono Problem Details (RFC 9457)**
  - URL: https://github.com/paveg/hono-problem-details

- **Hono Simple DI**
  - URL: https://github.com/maou-shonen/hono-simple-DI

- **InferDI**
  - URL: https://github.com/inferdi/inferdi/tree/main/packages/hono

- **Idempotency (Stripe-style idempotency keys)**
  - URL: https://github.com/paveg/hono-idempotency

- **idempot-js**
  - URL: https://js.idempot.dev

- **jsonv-ts (Validator, OpenAPI, MCP)**
  - URL: https://github.com/dswbx/jsonv-ts

- **MCP**
  - URL: https://github.com/honojs/middleware/tree/main/packages/mcp

- **RONIN (Database)**
  - URL: https://github.com/ronin-co/hono-client

- **Session**
  - URL: https://github.com/honojs/middleware/tree/main/packages/session

- **tsyringe**
  - URL: https://github.com/honojs/middleware/tree/main/packages/tsyringe

- **User Agent based Blocker**
  - URL: https://github.com/honojs/middleware/tree/main/packages/ua-blocker

### Import

### Usage

### Options

### Platform specific Request IDs

- **AWS documentation: Context object**
  - URL: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html

- **Cloudflare Ray ID
  **
  - URL: https://developers.cloudflare.com/fundamentals/reference/cloudflare-ray-id/

- **Request ID on the Deno Blog**
  - URL: https://deno.com/blog/zero-config-debugging-deno-opentelemetry#:~:text=s%20automatically%20have-,unique%20request%20IDs,-associated%20with%20them

- **Fastly documentation: req.xid**
  - URL: https://www.fastly.com/documentation/reference/vcl/variables/client-request/req-xid/

### Import

### Usage

### tryGetContext

### Import

### Usage

### Options

### Usage with Bun for large requests

### Import

### Usage

### Supported Options

### Middleware Conflict

### Setting Content-Security-Policy

### Setting Permission-Policy

### Import

### Usage

### Options

### Environment-dependent CORS configuration

### Using with Vite

### Import

### Usage

### Logging Details

### PrintFunc

### Options

### Import

### Usage

### Options

### Import

### Usage

### Options

### Import

### Usage

### Options

### Import

### Usage

### For example

### Options

### Import

### Usage

### The retained headers

### Options

### Import

### Usage

### Import

### Usage

### Options

### More Options

### Recipes

### Import

### Usage

### Options

### Nested Layouts

### `useRequestContext()`

### Extending `ContextRenderer`

### Import

### Usage

### Options

### Note

### Import

### Usage

### Notes

### Middleware Conflicts

### Import

### Usage

### Options

### Import

### Basic Usage

### Default Configuration

### Key Behaviors

### Advanced Configuration

### Options Reference

### Validation & Error Handling

### Common Recipes

### Import

### Usage

### Options

### What this middleware validates

### Import

### Usage

### Using `verifyWithJwks` outside of middleware

### Configuring JWKS fetch request options

### Options

### Import

### Usage

### Rules

### Error handling

### Import

### Usage

### Result

### Options

### Import

### Usage

### Options

- **Link**: **`string`**: Single allowed origin (e.g., `'
  - URL: https://example.com'`)

## Additional Resources (Optional)

### Optional Parameter

## How to Use This Skill

Reference these resources when working with CSRF Protection.