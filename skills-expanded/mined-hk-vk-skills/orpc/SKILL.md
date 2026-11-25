---
name: orpc
description: Typesafe APIs Made Simple 🪄
metadata:
  source: llms.txt
  source_url: https://orpc.dev/llms.txt
  generated: 2026-03-17T03:37:29.371Z
---

# oRPC

> Typesafe APIs Made Simple 🪄

Easy to build APIs that are end-to-end type-safe and adhere to OpenAPI standards

## Available Resources

### Table of Contents

- **Define Contract**: Learn how to define a contract for contract-first development in oRPC
  - URL: /docs/contract-first/define-contract.md

- **Implement Contract**: Learn how to implement a contract for contract-first development in oRPC
  - URL: /docs/contract-first/implement-contract.md

- **Router to Contract**: Learn how to convert a router into a contract, safely export it, and prevent exposing internal details to the client.
  - URL: /docs/contract-first/router-to-contract.md

- **HTTP**: How to use oRPC over HTTP?
  - URL: /docs/adapters/http.md

- **Websocket**: How to use oRPC over WebSocket?
  - URL: /docs/adapters/websocket.md

- **Message Port**: Using oRPC with Message Ports
  - URL: /docs/adapters/message-port.md

- **Astro Adapter**: Use oRPC inside an Astro project
  - URL: /docs/adapters/astro.md

- **Browser Adapter**: Type-safe communication between browser scripts using Message Port Adapter
  - URL: /docs/adapters/browser.md

- **Electron Adapter**: Use oRPC inside an Electron project
  - URL: /docs/adapters/electron.md

- **Elysia Adapter**: Use oRPC inside an Elysia project
  - URL: /docs/adapters/elysia.md

- **Express.js Adapter**: Use oRPC inside an Express.js project
  - URL: /docs/adapters/express.md

- **Fastify Adapter**: Use oRPC inside an Fastify project
  - URL: /docs/adapters/fastify.md

- **H3 Adapter**: Use oRPC inside an H3 project
  - URL: /docs/adapters/h3.md

- **Hono Adapter**: Use oRPC inside an Hono project
  - URL: /docs/adapters/hono.md

- **Next.js Adapter**: Use oRPC inside an Next.js project
  - URL: /docs/adapters/next.md

- **Nuxt.js Adapter**: Use oRPC inside an Nuxt.js project
  - URL: /docs/adapters/nuxt.md

- **React Native Adapter**: Use oRPC inside a React Native project
  - URL: /docs/adapters/react-native.md

- **Remix Adapter**: Use oRPC inside an Remix project
  - URL: /docs/adapters/remix.md

- **Solid Start Adapter**: Use oRPC inside a Solid Start project
  - URL: /docs/adapters/solid-start.md

- **Svelte Kit Adapter**: Use oRPC inside an Svelte Kit project
  - URL: /docs/adapters/svelte-kit.md

- **TanStack Start Adapter**: Use oRPC inside a TanStack Start project
  - URL: /docs/adapters/tanstack-start.md

- **Web Workers Adapter**: Enable type-safe communication with Web Workers using oRPC.
  - URL: /docs/adapters/web-workers.md

- **Worker Threads Adapter**: Enable type-safe communication between Node.js Worker Threads using oRPC.
  - URL: /docs/adapters/worker-threads.md

- **CORS Plugin**: CORS Plugin for oRPC
  - URL: /docs/plugins/cors.md

- **Request Headers Plugin**: Request Headers Plugin for oRPC
  - URL: /docs/plugins/request-headers.md

- **Response Headers Plugin**: Response Headers Plugin for oRPC
  - URL: /docs/plugins/response-headers.md

- **Request Validation Plugin**: A plugin that blocks invalid requests before they reach your server. Especially useful for applications that rely heavily on server-side validation.
  - URL: /docs/plugins/request-validation.md

- **Response Validation Plugin**: A plugin that validates server responses against the contract schema to ensure that the data returned from your server matches the expected types defined in your contract.
  - URL: /docs/plugins/response-validation.md

- **Hibernation Plugin**: A plugin to fully leverage Hibernation APIs for your ORPC server.
  - URL: /docs/plugins/hibernation.md

- **Dedupe Requests Plugin**: Prevents duplicate requests by deduplicating similar ones to reduce server load.
  - URL: /docs/plugins/dedupe-requests.md

- **Batch Requests Plugin**: A plugin for oRPC to batch requests and responses.
  - URL: /docs/plugins/batch-requests.md

- **Client Retry Plugin**: A plugin for oRPC that enables retrying client calls when errors occur.
  - URL: /docs/plugins/client-retry.md

- **Retry After Plugin**: A plugin for oRPC that automatically retries requests based on server Retry-After headers.
  - URL: /docs/plugins/retry-after.md

- **Rethrow Handler Plugin**: A plugin to catch and rethrow specific errors during request handling instead of handling them in the oRPC error flow.
  - URL: /docs/plugins/rethrow-handler.md

- **Compression Plugin**: A plugin for oRPC that compresses response bodies.
  - URL: /docs/plugins/compression.md

- **Body Limit Plugin**: A plugin for oRPC to limit the request body size.
  - URL: /docs/plugins/body-limit.md

- **Simple CSRF Protection Plugin**: Add basic Cross-Site Request Forgery (CSRF) protection to your oRPC application. It helps ensure that requests to your procedures originate from JavaScript code, not from other sources like standard HTML forms or direct browser navigation.
  - URL: /docs/plugins/simple-csrf-protection.md

- **Strict GET Method Plugin**: Enhance security by ensuring only procedures explicitly marked to accept `GET` requests can be called using the HTTP `GET` method for RPC Protocol. This helps prevent certain types of Cross-Site Request Forgery (CSRF) attacks.
  - URL: /docs/plugins/strict-get-method.md

- **Pino Integration**: Integrate oRPC with Pino for structured logging and request tracking.
  - URL: /docs/integrations/pino.md

- **Base64Url Helpers**: Functions to encode and decode base64url strings, a URL-safe variant of base64 encoding.
  - URL: /docs/helpers/base64url.md

- **Cookie Helpers**: Functions for managing HTTP cookies in web applications.
  - URL: /docs/helpers/cookie.md

- **Encryption Helpers**: Functions to encrypt and decrypt sensitive data using AES-GCM.
  - URL: /docs/helpers/encryption.md

- **Form Data Helpers**: Utilities for parsing form data and handling validation errors with bracket notation support.
  - URL: /docs/helpers/form-data.md

- **Publisher**: Listen and publish events with resuming support in oRPC
  - URL: /docs/helpers/publisher.md

- **Rate Limit**: Rate limiting features for oRPC with multiple adapters support.
  - URL: /docs/helpers/ratelimit.md

- **Signing Helpers**: Functions to cryptographically sign and verify data using HMAC-SHA256.
  - URL: /docs/helpers/signing.md

- **Server-Side Clients**: Call your oRPC procedures in the same environment as your server like native functions.
  - URL: /docs/client/server-side.md

- **Client-Side Clients**: Call your oRPC procedures remotely as if they were local functions.
  - URL: /docs/client/client-side.md

- **Error Handling in oRPC Clients**: Learn how to handle errors in a type-safe way in oRPC clients.
  - URL: /docs/client/error-handling.md

- **Event Iterator in oRPC Clients**: Learn how to use event iterators in oRPC clients.
  - URL: /docs/client/event-iterator.md

- **RPCLink**: Details on using RPCLink in oRPC clients.
  - URL: /docs/client/rpc-link.md

- **DynamicLink**: Dynamically switch between multiple oRPC's links.
  - URL: /docs/client/dynamic-link.md

- **AI SDK Integration**: Seamlessly use AI SDK inside your oRPC projects without any extra overhead.
  - URL: /docs/integrations/ai-sdk.md

- **Better Auth Integration**: Seamlessly use Better Auth inside your oRPC projects without any extra overhead.
  - URL: /docs/integrations/better-auth.md

- **Durable Iterator Integration**: Extends Event Iterator with durable event streams, automatic reconnections, and event recovery through a separate streaming service.
  - URL: /docs/integrations/durable-iterator.md

- **Hey API Integration**: Easily convert a Hey API generated client into an oRPC client to take full advantage of the oRPC ecosystem.
  - URL: /docs/integrations/hey-api.md

- **OpenTelemetry Integration**: Seamlessly integrate oRPC with OpenTelemetry for distributed tracing
  - URL: /docs/integrations/opentelemetry.md

- **Pinia Colada Integration**: Seamlessly integrate oRPC with Pinia Colada
  - URL: /docs/integrations/pinia-colada.md

- **Pino Integration**: Integrate oRPC with Pino for structured logging and request tracking.
  - URL: /docs/integrations/pino.md

- **React SWR Integration**: Integrate oRPC with React SWR for efficient data fetching and caching.
  - URL: /docs/integrations/react-swr.md

- **Sentry Integration**: Integrate oRPC with Sentry for error tracking and performance monitoring.
  - URL: /docs/integrations/sentry.md

- **Tanstack Query Integration**: Seamlessly integrate oRPC with Tanstack Query
  - URL: /docs/integrations/tanstack-query.md

- **Implement Contract in NestJS**: Seamlessly implement oRPC contracts in your NestJS projects.
  - URL: /docs/openapi/integrations/implement-contract-in-nest.md

- **tRPC Integration**: Use oRPC features in your tRPC applications.
  - URL: /docs/openapi/integrations/trpc.md

- **Tanstack Query Integration**: Seamlessly integrate oRPC with Tanstack Query
  - URL: /docs/integrations/tanstack-query-old/basic.md

- **Tanstack Query Integration For React**: Seamlessly integrate oRPC with Tanstack Query for React
  - URL: /docs/integrations/tanstack-query-old/react.md

- **Tanstack Query Integration For Vue**: Seamlessly integrate oRPC with Tanstack Query for Vue
  - URL: /docs/integrations/tanstack-query-old/vue.md

- **Tanstack Query Integration For Solid**: Seamlessly integrate oRPC with Tanstack Query for Solid
  - URL: /docs/integrations/tanstack-query-old/solid.md

- **Tanstack Query Integration For Svelte**: Seamlessly integrate oRPC with Tanstack Query for Svelte
  - URL: /docs/integrations/tanstack-query-old/svelte.md

- **OpenAI Streaming Example**: Combine oRPC with the OpenAI Streaming API to build a chatbot
  - URL: /docs/examples/openai-streaming.md

- **Dedupe Middleware**: Enhance oRPC middleware performance by avoiding redundant executions.
  - URL: /docs/best-practices/dedupe-middleware.md

- **Monorepo Setup**: The most efficient way to set up a monorepo with oRPC
  - URL: /docs/best-practices/monorepo-setup.md

- **No Throw Literal**: Always throw `Error` instances instead of literal values.
  - URL: /docs/best-practices/no-throw-literal.md

- **Optimize Server-Side Rendering (SSR) for Fullstack Frameworks**: Optimize SSR performance in Next.js, SvelteKit, and other frameworks by using oRPC to make direct server-side API calls, avoiding unnecessary network requests.
  - URL: /docs/best-practices/optimize-ssr.md

- **Building Custom Plugins**: Create powerful custom plugins to extend oRPC handlers and links with interceptors.
  - URL: /docs/advanced/building-custom-plugins.md

- **Exceeds the Maximum Length Problem**: How to address the Exceeds the Maximum Length Problem in oRPC.
  - URL: /docs/advanced/exceeds-the-maximum-length-problem.md

- **Extend Body Parser**: Extend the body parser for more efficient handling of large payloads, extend the data types.
  - URL: /docs/advanced/extend-body-parser.md

- **Publish Client to NPM**: How to publish your oRPC client to NPM for users to consume your APIs as an SDK.
  - URL: /docs/advanced/publish-client-to-npm.md

- **RPC JSON Serializer**: Extend or override the standard RPC JSON serializer.
  - URL: /docs/advanced/rpc-json-serializer.md

- **RPC Protocol**: Learn about the RPC protocol used by RPCHandler.
  - URL: /docs/advanced/rpc-protocol.md

- **SuperJson**: Replace the default oRPC RPC serializer with SuperJson.
  - URL: /docs/advanced/superjson.md

- **Testing & Mocking**: How to test and mock oRPC routers and procedures?
  - URL: /docs/advanced/testing-mocking.md

- **Validation Errors**: Learn about oRPC's built-in validation errors and how to customize them.
  - URL: /docs/advanced/validation-errors.md

- **Migrating from tRPC**: A comprehensive guide to migrate your tRPC application to oRPC
  - URL: /docs/migrations/from-trpc.md

- **OpenAPI Reference Plugin (Swagger/Scalar)**: A plugin that serves API reference documentation and the OpenAPI specification for your API.
  - URL: /docs/openapi/plugins/openapi-reference.md

- **Smart Coercion Plugin**: Automatically converts input values to match schema types without manually defining coercion logic.
  - URL: /docs/openapi/plugins/smart-coercion.md

- **Zod Smart Coercion**: A refined alternative to `z.coerce` that automatically converts inputs to the expected type without modifying the input schema.
  - URL: /docs/openapi/plugins/zod-smart-coercion.md

- **OpenAPILink**: Details on using OpenAPILink in oRPC clients.
  - URL: /docs/openapi/client/openapi-link.md

- **Implement Contract in NestJS**: Seamlessly implement oRPC contracts in your NestJS projects.
  - URL: /docs/openapi/integrations/implement-contract-in-nest.md

- **tRPC Integration**: Use oRPC features in your tRPC applications.
  - URL: /docs/openapi/integrations/trpc.md

- **Customizing Error Response Format**: Learn how to customize the error response format in oRPC OpenAPI to match your application's requirements and improve client compatibility.
  - URL: /docs/openapi/advanced/customizing-error-response.md

- **Disabling Output Validation**: Learn how to disable output validation in oRPC procedures for improved performance while maintaining OpenAPI specification generation.
  - URL: /docs/openapi/advanced/disabling-output-validation.md

- **Expanding Type Support for OpenAPI Link**: Learn how to extend OpenAPILink to support additional data types beyond JSON's native capabilities using the Response Validation Plugin and schema coercion.
  - URL: /docs/openapi/advanced/expanding-type-support-for-openapi-link.md

- **OpenAPI JSON Serializer**: Extend or override the standard OpenAPI JSON serializer.
  - URL: /docs/openapi/advanced/openapi-json-serializer.md

- **Redirect Response**: Standard HTTP redirect response in oRPC OpenAPI.
  - URL: /docs/openapi/advanced/redirect-response.md

- **Overview of Mini oRPC**: A brief introduction to Mini oRPC, a simplified version of oRPC designed for learning purposes.
  - URL: /learn-and-contribute/mini-orpc/overview.md

- **Procedure Builder in Mini oRPC**: Learn how Mini oRPC's procedure builder provides an excellent developer experience for defining type-safe procedures.
  - URL: /learn-and-contribute/mini-orpc/procedure-builder.md

- **Server-side Client in Mini oRPC**: Learn how to turn a procedure into a callable function in Mini oRPC, enabling server-side client functionality.
  - URL: /learn-and-contribute/mini-orpc/server-side-client.md

- **Client-side Client in Mini oRPC**: Learn how to implement remote procedure calls (RPC) on the client side in Mini oRPC.
  - URL: /learn-and-contribute/mini-orpc/client-side-client.md

- **Beyond the Basics of Mini oRPC**: Explore advanced features you can implement in Mini oRPC.
  - URL: /learn-and-contribute/mini-orpc/beyond-the-basics.md

- **Bracket Notation**: Represent structured data in limited formats such as URL queries and form data.
  - URL: /docs/openapi/bracket-notation.md

- **Comparison**: How is oRPC different from other RPC or REST solutions?
  - URL: /docs/comparison.md

- **Context**: Understanding context in oRPC
  - URL: /docs/context.md

- **Ecosystem**: oRPC ecosystem & community resources
  - URL: /docs/ecosystem.md

- **Error Handling**: Manage errors in oRPC using both traditional and type‑safe strategies.
  - URL: /docs/error-handling.md

- **Event Iterator (SSE)**: Learn how to streaming responses, real-time updates, and server-sent events using oRPC.
  - URL: /docs/event-iterator.md

- **File Upload and Download**: Learn how to upload and download files using oRPC.
  - URL: /docs/file-upload-download.md

- **Getting Started**: Quick guide to oRPC
  - URL: /docs/getting-started.md

- **Getting Started with OpenAPI**: Quick guide to OpenAPI in oRPC
  - URL: /docs/openapi/getting-started.md

- **Input/Output Structure**: Control how input and output data is structured in oRPC
  - URL: /docs/openapi/input-output-structure.md

- **Metadata**: Enhance your procedures with metadata.
  - URL: /docs/metadata.md

- **Middleware**: Understanding middleware in oRPC
  - URL: /docs/middleware.md

- **OpenAPI Error Handling**: Handle errors in your OpenAPI-compliant oRPC APIs
  - URL: /docs/openapi/error-handling.md

- **OpenAPI Handler**: Comprehensive Guide to the OpenAPIHandler in oRPC
  - URL: /docs/openapi/openapi-handler.md

- **OpenAPI Routing**: Configure procedure routing with oRPC.
  - URL: /docs/openapi/routing.md

- **OpenAPI Specification**: Generate OpenAPI specifications for oRPC with ease.
  - URL: /docs/openapi/openapi-specification.md

- **Playgrounds**: Interactive development environments for exploring and testing oRPC functionality.
  - URL: /docs/playgrounds.md

- **Procedure**: Understanding procedures in oRPC
  - URL: /docs/procedure.md

- **Router**: Understanding routers in oRPC
  - URL: /docs/router.md

- **RPC Handler**: Comprehensive Guide to the RPCHandler in oRPC
  - URL: /docs/rpc-handler.md

- **Scalar (Swagger)**: Create a beautiful API client for your oRPC effortlessly.
  - URL: /docs/openapi/scalar.md

- **Server Action**: Integrate oRPC procedures with React Server Actions
  - URL: /docs/server-action.md

## How to Use This Skill

Reference these resources when working with oRPC.