---
name: bun
description: Bun documentation and resources. Use this skill when working with Bun or when the user mentions bun.
metadata:
  source: llms.txt
  source_url: https://bun.sh/docs
  generated: 2026-08-29T14:00:22.493Z
---

# Bun

## Available Resources

### Docs

- **Welcome to Bun**: Bun is an all-in-one toolkit for developing modern JavaScript/TypeScript applications.
  - URL: https://bun.com/docs/index.md

- **Installation**: Install Bun with npm, Homebrew, Docker, or the official script.
  - URL: https://bun.com/docs/installation.md

- **Quickstart**: Build your first app with Bun
  - URL: https://bun.com/docs/quickstart.md

- **TypeScript**: Using TypeScript with Bun, including type definitions and compiler options
  - URL: https://bun.com/docs/typescript.md

- **TypeScript 6 and 7**: How to configure Bun's type definitions for TypeScript 6.0 and 7.0, which no longer auto-discover @types packages. Fix 'Cannot find name Bun' and other missing type errors after upgrading TypeScript.
  - URL: https://bun.com/docs/typescript-6.md

- **bun init**: Scaffold an empty Bun project with the interactive `bun init` command
  - URL: https://bun.com/docs/runtime/templating/init.md

- **bun create**: Create a new Bun project from a React component, a `create-<template>` npm package, a GitHub repo, or a local template
  - URL: https://bun.com/docs/runtime/templating/create.md

- **Bun Runtime**: Execute JavaScript/TypeScript files, package.json scripts, and executable packages with Bun's fast runtime.
  - URL: https://bun.com/docs/runtime/index.md

- **Watch Mode**: Automatic reloading in Bun with --watch and --hot modes
  - URL: https://bun.com/docs/runtime/watch-mode.md

- **Debugging**: Debug your Bun code with an interactive debugger using WebKit Inspector Protocol
  - URL: https://bun.com/docs/runtime/debugger.md

- **REPL**: An interactive JavaScript and TypeScript REPL with syntax highlighting, history, and tab completion
  - URL: https://bun.com/docs/runtime/repl.md

- **bunfig.toml**: Configure Bun's behavior using its configuration file bunfig.toml
  - URL: https://bun.com/docs/runtime/bunfig.md

- **File Types**: File types and loaders supported by Bun's bundler and runtime
  - URL: https://bun.com/docs/runtime/file-types.md

- **Module Resolution**: How Bun resolves modules and handles imports in JavaScript and TypeScript
  - URL: https://bun.com/docs/runtime/module-resolution.md

- **JSX**: Built-in JSX and TSX support in Bun with configurable transpilation options
  - URL: https://bun.com/docs/runtime/jsx.md

- **Auto-install**: Bun's automatic package installation feature for standalone script execution
  - URL: https://bun.com/docs/runtime/auto-install.md

- **Plugins**: Universal plugin API for extending Bun's runtime and bundler
  - URL: https://bun.com/docs/runtime/plugins.md

- **File System Router**: Bun provides a fast API for resolving routes against file-system paths
  - URL: https://bun.com/docs/runtime/file-system-router.md

- **Server**: Use `Bun.serve` to start a high-performance HTTP server in Bun
  - URL: https://bun.com/docs/runtime/http/server.md

- **Routing**: Define routes in `Bun.serve` using static paths, parameters, and wildcards
  - URL: https://bun.com/docs/runtime/http/routing.md

- **Cookies**: Work with cookies in HTTP requests and responses using Bun's built-in Cookie API.
  - URL: https://bun.com/docs/runtime/http/cookies.md

- **TLS**: Enable TLS in Bun.serve
  - URL: https://bun.com/docs/runtime/http/tls.md

- **Error Handling**: Learn how to handle errors in Bun's development server
  - URL: https://bun.com/docs/runtime/http/error-handling.md

- **Metrics**: Monitor server activity with built-in metrics
  - URL: https://bun.com/docs/runtime/http/metrics.md

- **Fetch**: Send HTTP requests with Bun's fetch API
  - URL: https://bun.com/docs/runtime/networking/fetch.md

- **WebSockets**: Server-side WebSockets in Bun
  - URL: https://bun.com/docs/runtime/http/websockets.md

- **TCP**: Use Bun's native TCP API to implement performance-sensitive systems like database clients, game servers, or anything that needs to communicate over TCP (instead of HTTP)
  - URL: https://bun.com/docs/runtime/networking/tcp.md

- **UDP**: Use Bun's UDP API to implement services with advanced real-time requirements, such as voice chat.
  - URL: https://bun.com/docs/runtime/networking/udp.md

- **DNS**: Use Bun's DNS module to resolve DNS records
  - URL: https://bun.com/docs/runtime/networking/dns.md

- **Cookies**: Use Bun's native APIs for working with HTTP cookies
  - URL: https://bun.com/docs/runtime/cookies.md

- **File I/O**: Bun provides a set of optimized APIs for reading and writing files.
  - URL: https://bun.com/docs/runtime/file-io.md

- **Streams**: Use Bun's streams API to work with binary data without loading it all into memory at once
  - URL: https://bun.com/docs/runtime/streams.md

- **Binary Data**: Working with binary data in JavaScript
  - URL: https://bun.com/docs/runtime/binary-data.md

- **Archive**: Create and extract tar archives with Bun's fast native implementation
  - URL: https://bun.com/docs/runtime/archive.md

- **SQL**: Bun provides native bindings for working with SQL databases through a unified Promise-based API that supports PostgreSQL, MySQL, and SQLite.
  - URL: https://bun.com/docs/runtime/sql.md

- **SQLite**: Bun natively implements a high-performance SQLite3 driver.
  - URL: https://bun.com/docs/runtime/sqlite.md

- **S3**: Bun provides fast, native bindings for interacting with S3-compatible object storage services.
  - URL: https://bun.com/docs/runtime/s3.md

- **Redis**: Use Bun's native Redis client with a Promise-based API
  - URL: https://bun.com/docs/runtime/redis.md

- **Workers**: Use Bun's Workers API to create and communicate with a new JavaScript instance running on a separate thread while sharing I/O resources with the main thread
  - URL: https://bun.com/docs/runtime/workers.md

- **Environment Variables**: Read and configure environment variables in Bun, including automatic .env file support
  - URL: https://bun.com/docs/runtime/environment-variables.md

- **Shell**: Use Bun's shell scripting API to run shell commands from JavaScript
  - URL: https://bun.com/docs/runtime/shell.md

- **Spawn**: Spawn child processes with `Bun.spawn` or `Bun.spawnSync`
  - URL: https://bun.com/docs/runtime/child-process.md

- **WebView**: Control a headless browser from Bun for automation, testing, and scraping — zero dependencies on macOS, Chrome DevTools Protocol everywhere else
  - URL: https://bun.com/docs/runtime/webview.md

- **Cron**: Schedule and parse cron jobs with Bun
  - URL: https://bun.com/docs/runtime/cron.md

- **Node-API**: Use Bun's Node-API module to build native add-ons to Node.js
  - URL: https://bun.com/docs/runtime/node-api.md

- **FFI**: Use Bun's FFI module to efficiently call native libraries from JavaScript
  - URL: https://bun.com/docs/runtime/ffi.md

- **C Compiler**: Compile and run C from JavaScript with low overhead
  - URL: https://bun.com/docs/runtime/c-compiler.md

- **Transpiler**: Use Bun's transpiler to transpile JavaScript and TypeScript code
  - URL: https://bun.com/docs/runtime/transpiler.md

- **CSRF Protection**: Generate and verify CSRF tokens with Bun's built-in API
  - URL: https://bun.com/docs/runtime/csrf.md

- **Secrets**: Use Bun's Secrets API to store and retrieve sensitive credentials securely
  - URL: https://bun.com/docs/runtime/secrets.md

- **Console**: The console object in Bun
  - URL: https://bun.com/docs/runtime/console.md

- **TOML**: Use Bun's built-in support for TOML files through both runtime APIs and bundler integration
  - URL: https://bun.com/docs/runtime/toml.md

- **YAML**: Use Bun's built-in support for YAML files through both runtime APIs and bundler integration
  - URL: https://bun.com/docs/runtime/yaml.md

- **Markdown**: Parse and render Markdown with Bun's built-in Markdown API, supporting GFM extensions and custom rendering callbacks
  - URL: https://bun.com/docs/runtime/markdown.md

- **JSON5**: Use Bun's built-in support for JSON5 files through both runtime APIs and bundler integration
  - URL: https://bun.com/docs/runtime/json5.md

- **XML**: Use Bun's built-in support for XML through both runtime APIs and bundler integration
  - URL: https://bun.com/docs/runtime/xml.md

- **JSONL**: Parse newline-delimited JSON (JSONL) with Bun's built-in streaming parser
  - URL: https://bun.com/docs/runtime/jsonl.md

- **HTMLRewriter**: Use Bun's HTMLRewriter to transform HTML documents with CSS selectors
  - URL: https://bun.com/docs/runtime/html-rewriter.md

- **Image**: Decode, transform, and encode images with a fast native pipeline
  - URL: https://bun.com/docs/runtime/image.md

- **Hashing**: Utility functions for hashing and verifying passwords with various cryptographically secure algorithms
  - URL: https://bun.com/docs/runtime/hashing.md

- **Glob**: Use Bun's fast native implementation of file globbing
  - URL: https://bun.com/docs/runtime/glob.md

- **Semver**: Use Bun's semantic versioning API
  - URL: https://bun.com/docs/runtime/semver.md

- **Color**: Format colors as CSS, ANSI, numbers, hex strings, and more
  - URL: https://bun.com/docs/runtime/color.md

- **Utils**: Use Bun's utility functions to work with the runtime
  - URL: https://bun.com/docs/runtime/utils.md

- **Globals**: Use Bun's global objects
  - URL: https://bun.com/docs/runtime/globals.md

- **Bun APIs**: Overview of Bun's native APIs available on the Bun global object and built-in modules
  - URL: https://bun.com/docs/runtime/bun-apis.md

- **Web APIs**: Web-standard APIs supported by Bun for server-side JavaScript
  - URL: https://bun.com/docs/runtime/web-apis.md

- **Node.js Compatibility**: Bun's compatibility status with Node.js APIs, modules, and globals
  - URL: https://bun.com/docs/runtime/nodejs-compat.md

- **Roadmap**: Bun's roadmap and long-term plans
  - URL: https://bun.com/docs/project/roadmap.md

- **Benchmarking**: How to benchmark Bun
  - URL: https://bun.com/docs/project/benchmarking.md

- **Contributing**: Contributing to Bun
  - URL: https://bun.com/docs/project/contributing.md

- **Building Windows**: Building Bun on Windows
  - URL: https://bun.com/docs/project/building-windows.md

- **Bindgen**: Bindgen for Bun
  - URL: https://bun.com/docs/project/bindgen.md

- **License**: License for Bun
  - URL: https://bun.com/docs/project/license.md

- **bun install**: Install packages with Bun's fast package manager
  - URL: https://bun.com/docs/pm/cli/install.md

- **bun add**: Add packages to your project with Bun's fast package manager
  - URL: https://bun.com/docs/pm/cli/add.md

- **bun remove**: Remove dependencies from your project
  - URL: https://bun.com/docs/pm/cli/remove.md

- **bun update**: Update dependencies to the newest versions their ranges allow
  - URL: https://bun.com/docs/pm/cli/update.md

- **bun dedupe**: Remove duplicate versions of packages from bun.lock
  - URL: https://bun.com/docs/pm/cli/dedupe.md

- **bun prune**: Remove packages that are not in bun.lock from node_modules
  - URL: https://bun.com/docs/pm/cli/prune.md

- **bunx**: Run packages from npm
  - URL: https://bun.com/docs/pm/bunx.md

- **bun publish**: Use `bun publish` to publish a package to the npm registry
  - URL: https://bun.com/docs/pm/cli/publish.md

- **bun outdated**: Check for outdated dependencies
  - URL: https://bun.com/docs/pm/cli/outdated.md

- **bun why**: Explain why a package is installed
  - URL: https://bun.com/docs/pm/cli/why.md

- **bun audit**: Check your installed packages for known security vulnerabilities
  - URL: https://bun.com/docs/pm/cli/audit.md

- **bun info**: Display package metadata from the npm registry
  - URL: https://bun.com/docs/pm/cli/info.md

- **Workspaces**: Develop complex monorepos with multiple independent packages
  - URL: https://bun.com/docs/pm/workspaces.md

- **Catalogs**: Share common dependency versions across multiple packages in a monorepo
  - URL: https://bun.com/docs/pm/catalogs.md

- **bun link**: Link local packages for development
  - URL: https://bun.com/docs/pm/cli/link.md

- **bun pm**: Package manager utilities
  - URL: https://bun.com/docs/pm/cli/pm.md

- **bun patch**: Persistently patch node_modules packages in a git-friendly way
  - URL: https://bun.com/docs/pm/cli/patch.md

- **bun --filter**: Select packages by pattern in a monorepo using the --filter flag
  - URL: https://bun.com/docs/pm/filter.md

- **Global cache**: How Bun stores and manages packages in its global cache
  - URL: https://bun.com/docs/pm/global-cache.md

- **Global virtual store**: Install packages once. Every project links to the same copy.
  - URL: https://bun.com/docs/pm/global-store.md

- **Isolated installs**: Strict dependency isolation similar to pnpm's approach
  - URL: https://bun.com/docs/pm/isolated-installs.md

- **Lockfile**: Bun's lockfile format and configuration
  - URL: https://bun.com/docs/pm/lockfile.md

- **Lifecycle scripts**: How Bun handles package lifecycle scripts securely
  - URL: https://bun.com/docs/pm/lifecycle.md

- **Scopes and registries**: Configure private registries and scoped packages
  - URL: https://bun.com/docs/pm/scopes-registries.md

- **Overrides and resolutions**: Control metadependency versions with npm overrides and Yarn resolutions
  - URL: https://bun.com/docs/pm/overrides.md

- **Security Scanner API**
  - URL: https://bun.com/docs/pm/security-scanner-api.md

- **.npmrc support**
  - URL: https://bun.com/docs/pm/npmrc.md

- **Bundler**: Bun's fast native bundler for JavaScript, TypeScript, JSX, and more
  - URL: https://bun.com/docs/bundler/index.md

- **Fullstack dev server**: Build fullstack applications with Bun's integrated dev server that bundles frontend assets and handles API routes
  - URL: https://bun.com/docs/bundler/fullstack.md

- **Hot reloading**: Hot Module Replacement (HMR) for Bun's development server
  - URL: https://bun.com/docs/bundler/hot-reloading.md

- **HTML & static sites**: Build static sites, landing pages, and web applications with Bun's bundler
  - URL: https://bun.com/docs/bundler/html-static.md

- **Standalone HTML**: Bundle a single-page app into a single self-contained .html file with no external dependencies
  - URL: https://bun.com/docs/bundler/standalone-html.md

- **CSS**: Bun's bundler has built-in support for CSS with modern features
  - URL: https://bun.com/docs/bundler/css.md

- **Loaders**: Built-in loaders for the Bun bundler and runtime
  - URL: https://bun.com/docs/bundler/loaders.md

- **Single-file executable**: Generate standalone executables from TypeScript or JavaScript files with Bun
  - URL: https://bun.com/docs/bundler/executables.md

- **Plugins**: Universal plugin API for extending Bun's runtime and bundler
  - URL: https://bun.com/docs/bundler/plugins.md

- **Macros**: Run JavaScript functions at bundle-time with Bun macros
  - URL: https://bun.com/docs/bundler/macros.md

- **Bytecode Caching**: Speed up JavaScript execution with bytecode caching in Bun's bundler
  - URL: https://bun.com/docs/bundler/bytecode.md

- **Minifier**: Reduce bundle sizes with Bun's JavaScript and TypeScript minifier
  - URL: https://bun.com/docs/bundler/minifier.md

- **esbuild**: Migration guide from esbuild to Bun's bundler
  - URL: https://bun.com/docs/bundler/esbuild.md

- **Test runner**: Bun's fast, built-in, Jest-compatible test runner with TypeScript support, lifecycle hooks, mocking, and watch mode
  - URL: https://bun.com/docs/test/index.md

- **Writing tests**: Write tests with Bun's Jest-compatible API, including async tests, timeouts, and test modifiers
  - URL: https://bun.com/docs/test/writing-tests.md

- **Test configuration**: Configure bun test behavior with bunfig.toml and command-line options
  - URL: https://bun.com/docs/test/configuration.md

- **Runtime behavior**: Learn about Bun test's runtime integration, environment variables, timeouts, and error handling
  - URL: https://bun.com/docs/test/runtime-behavior.md

- **Finding tests**: Learn how Bun's test runner discovers and filters test files in your project
  - URL: https://bun.com/docs/test/discovery.md

- **Parallel & isolated test runs**: Run test files across CPU cores with --parallel, isolate files from each other with --isolate, run tests within a file concurrently, and split suites across CI machines with --shard and --timings
  - URL: https://bun.com/docs/test/parallel.md

- **Lifecycle hooks**: Learn how to use beforeAll, beforeEach, afterEach, and afterAll lifecycle hooks in Bun tests
  - URL: https://bun.com/docs/test/lifecycle.md

- **Mocks**: Learn how to create and use mock functions, spies, and module mocks in Bun tests
  - URL: https://bun.com/docs/test/mocks.md

- **Snapshots**: Learn how to use snapshot testing in Bun to save and compare output between test runs
  - URL: https://bun.com/docs/test/snapshots.md

- **Dates and times**: Learn how to manipulate time and dates in your Bun tests using setSystemTime and Jest compatibility functions
  - URL: https://bun.com/docs/test/dates-times.md

- **DOM testing**: Learn how to test DOM elements and components using Bun with happy-dom and React Testing Library
  - URL: https://bun.com/docs/test/dom.md

- **Code coverage**: Use Bun's built-in code coverage reporting to track test coverage and find untested code
  - URL: https://bun.com/docs/test/code-coverage.md

- **Test Reporters**
  - URL: https://bun.com/docs/test/reporters.md

- **Guides**: Code samples and walkthroughs for common tasks with Bun
  - URL: https://bun.com/docs/guides/index.md

- **Deploy a Bun application on Vercel**
  - URL: https://bun.com/docs/guides/deployment/vercel.md

- **Deploy a Bun application on Railway**: Deploy a Bun application to Railway from the CLI or dashboard, with optional PostgreSQL setup and automatic SSL
  - URL: https://bun.com/docs/guides/deployment/railway.md

- **Deploy a Bun application on Render**
  - URL: https://bun.com/docs/guides/deployment/render.md

- **Deploy a Bun application on AWS Lambda**
  - URL: https://bun.com/docs/guides/deployment/aws-lambda.md

- **Deploy a Bun application on DigitalOcean**
  - URL: https://bun.com/docs/guides/deployment/digital-ocean.md

- **Deploy a Bun application on Google Cloud Run**
  - URL: https://bun.com/docs/guides/deployment/google-cloud-run.md

- **Install TypeScript declarations for Bun**
  - URL: https://bun.com/docs/guides/runtime/typescript.md

- **Re-map import paths**
  - URL: https://bun.com/docs/guides/runtime/tsconfig-paths.md

- **Debugging Bun with the VS Code extension**
  - URL: https://bun.com/docs/guides/runtime/vscode-debugger.md

- **Debugging Bun with the web debugger**
  - URL: https://bun.com/docs/guides/runtime/web-debugger.md

- **Inspect memory usage using V8 heap snapshots**
  - URL: https://bun.com/docs/guides/runtime/heap-snapshot.md

- **Build-time constants with --define**
  - URL: https://bun.com/docs/guides/runtime/build-time-constants.md

- **Define and replace static globals & constants**
  - URL: https://bun.com/docs/guides/runtime/define-constant.md

- **Install and run Bun in GitHub Actions**
  - URL: https://bun.com/docs/guides/runtime/cicd.md

- **Codesign a single-file JavaScript executable on macOS**: Fix the "can't be opened because it is from an unidentified developer" Gatekeeper warning when running your JavaScript executable.
  - URL: https://bun.com/docs/guides/runtime/codesign-macos-executable.md

- **Upgrade Bun to the latest version**
  - URL: https://bun.com/docs/guides/util/upgrade.md

- **Detect when code is executed with Bun**
  - URL: https://bun.com/docs/guides/util/detect-bun.md

- **Get the current Bun version**
  - URL: https://bun.com/docs/guides/util/version.md

- **Hash a password**
  - URL: https://bun.com/docs/guides/util/hash-a-password.md

- **Generate a UUID**
  - URL: https://bun.com/docs/guides/util/javascript-uuid.md

- **Encode and decode base64 data**
  - URL: https://bun.com/docs/guides/util/base64.md

- **Compress and decompress data with gzip**
  - URL: https://bun.com/docs/guides/util/gzip.md

- **Compress and decompress data with DEFLATE**
  - URL: https://bun.com/docs/guides/util/deflate.md

- **Escape an HTML string**
  - URL: https://bun.com/docs/guides/util/escape-html.md

- **Check if two objects are deeply equal**
  - URL: https://bun.com/docs/guides/util/deep-equals.md

- **Sleep for a fixed number of milliseconds**
  - URL: https://bun.com/docs/guides/util/sleep.md

- **Convert a file URL to an absolute path**
  - URL: https://bun.com/docs/guides/util/file-url-to-path.md

- **Convert an absolute path to a file URL**
  - URL: https://bun.com/docs/guides/util/path-to-file-url.md

- **Get the path to an executable bin file**
  - URL: https://bun.com/docs/guides/util/which-path-to-executable-bin.md

- **Get the directory of the current file**
  - URL: https://bun.com/docs/guides/util/import-meta-dir.md

- **Get the file name of the current file**
  - URL: https://bun.com/docs/guides/util/import-meta-file.md

- **Get the absolute path of the current file**
  - URL: https://bun.com/docs/guides/util/import-meta-path.md

- **Check if the current file is the entrypoint**
  - URL: https://bun.com/docs/guides/util/entrypoint.md

- **Get the absolute path to the current entrypoint**
  - URL: https://bun.com/docs/guides/util/main.md

- **Build an app with Astro and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/astro.md

- **Create a Discord bot**
  - URL: https://bun.com/docs/guides/ecosystem/discordjs.md

- **Containerize a Bun application with Docker**
  - URL: https://bun.com/docs/guides/ecosystem/docker.md

- **Use Drizzle ORM with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/drizzle.md

- **Use Gel with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/gel.md

- **Build an HTTP server using Elysia and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/elysia.md

- **Build an HTTP server using Express and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/express.md

- **Build an HTTP server using Hono and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/hono.md

- **Read and write data to MongoDB using Mongoose and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/mongoose.md

- **Use Neon Postgres through Drizzle ORM**
  - URL: https://bun.com/docs/guides/ecosystem/neon-drizzle.md

- **Use Neon's Serverless Postgres with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/neon-serverless-postgres.md

- **Build an app with Next.js and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/nextjs.md

- **Build an app with Nuxt and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/nuxt.md

- **Run Bun as a daemon with PM2**
  - URL: https://bun.com/docs/guides/ecosystem/pm2.md

- **Use Prisma with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/prisma.md

- **Use Prisma Postgres with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/prisma-postgres.md

- **Build an app with Qwik and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/qwik.md

- **Build a React app with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/react.md

- **Build an app with Remix and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/remix.md

- **Use TanStack Start with Bun**
  - URL: https://bun.com/docs/guides/ecosystem/tanstack-start.md

- **Add Sentry to a Bun app**
  - URL: https://bun.com/docs/guides/ecosystem/sentry.md

- **Build an app with SolidStart and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/solidstart.md

- **Server-side render (SSR) a React component**
  - URL: https://bun.com/docs/guides/ecosystem/ssr-react.md

- **Build an app with SvelteKit and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/sveltekit.md

- **Run Bun as a daemon with systemd**
  - URL: https://bun.com/docs/guides/ecosystem/systemd.md

- **Build a frontend using Vite and Bun**
  - URL: https://bun.com/docs/guides/ecosystem/vite.md

- **Bun Redis with Upstash**
  - URL: https://bun.com/docs/guides/ecosystem/upstash.md

- **Common HTTP server usage**
  - URL: https://bun.com/docs/guides/http/server.md

- **Write a simple HTTP server**
  - URL: https://bun.com/docs/guides/http/simple.md

- **Send an HTTP request using fetch**
  - URL: https://bun.com/docs/guides/http/fetch.md

- **Hot reload an HTTP server**
  - URL: https://bun.com/docs/guides/http/hot.md

- **Start a cluster of HTTP servers**: Run multiple HTTP servers concurrently with the "reusePort" option to share the same port across multiple processes
  - URL: https://bun.com/docs/guides/http/cluster.md

- **Configure TLS on an HTTP server**
  - URL: https://bun.com/docs/guides/http/tls.md

- **Proxy HTTP requests using fetch()**
  - URL: https://bun.com/docs/guides/http/proxy.md

- **Stream a file as an HTTP Response**
  - URL: https://bun.com/docs/guides/http/stream-file.md

- **Upload files via HTTP using FormData**
  - URL: https://bun.com/docs/guides/http/file-uploads.md

- **fetch with unix domain sockets in Bun**
  - URL: https://bun.com/docs/guides/http/fetch-unix.md

- **Streaming HTTP Server with Async Iterators**
  - URL: https://bun.com/docs/guides/http/stream-iterator.md

- **Server-Sent Events (SSE) with Bun**
  - URL: https://bun.com/docs/guides/http/sse.md

- **Streaming HTTP Server with Node.js Streams**
  - URL: https://bun.com/docs/guides/http/stream-node-streams-in-bun.md

- **Build a simple WebSocket server**
  - URL: https://bun.com/docs/guides/websocket/simple.md

- **Build a publish-subscribe WebSocket server**
  - URL: https://bun.com/docs/guides/websocket/pubsub.md

- **Set per-socket contextual data on a WebSocket**
  - URL: https://bun.com/docs/guides/websocket/context.md

- **Enable compression for WebSocket messages**
  - URL: https://bun.com/docs/guides/websocket/compression.md

- **Spawn a child process**
  - URL: https://bun.com/docs/guides/process/spawn.md

- **Read stdout from a child process**
  - URL: https://bun.com/docs/guides/process/spawn-stdout.md

- **Read stderr from a child process**
  - URL: https://bun.com/docs/guides/process/spawn-stderr.md

- **Parse command-line arguments**
  - URL: https://bun.com/docs/guides/process/argv.md

- **Read from stdin**
  - URL: https://bun.com/docs/guides/process/stdin.md

- **Spawn a child process and communicate using IPC**
  - URL: https://bun.com/docs/guides/process/ipc.md

- **Listen for CTRL+C**
  - URL: https://bun.com/docs/guides/process/ctrl-c.md

- **Listen to OS signals**
  - URL: https://bun.com/docs/guides/process/os-signals.md

- **Get the process uptime in nanoseconds**
  - URL: https://bun.com/docs/guides/process/nanoseconds.md

- **Run a Shell Command**
  - URL: https://bun.com/docs/guides/runtime/shell.md

- **Set a time zone in Bun**
  - URL: https://bun.com/docs/guides/runtime/timezone.md

- **Set environment variables**
  - URL: https://bun.com/docs/guides/runtime/set-env.md

- **Read environment variables**
  - URL: https://bun.com/docs/guides/runtime/read-env.md

- **Add a dependency**
  - URL: https://bun.com/docs/guides/install/add.md

- **Add a development dependency**
  - URL: https://bun.com/docs/guides/install/add-dev.md

- **Add an optional dependency**
  - URL: https://bun.com/docs/guides/install/add-optional.md

- **Add a peer dependency**
  - URL: https://bun.com/docs/guides/install/add-peer.md

- **Add a Git dependency**
  - URL: https://bun.com/docs/guides/install/add-git.md

- **Add a tarball dependency**
  - URL: https://bun.com/docs/guides/install/add-tarball.md

- **Install a package under a different name**
  - URL: https://bun.com/docs/guides/install/npm-alias.md

- **Configuring a monorepo using workspaces**
  - URL: https://bun.com/docs/guides/install/workspaces.md

- **Override the default npm registry for bun install**
  - URL: https://bun.com/docs/guides/install/custom-registry.md

- **Configure a private registry for an organization scope with bun install**
  - URL: https://bun.com/docs/guides/install/registry-scope.md

- **Using bun install with an Azure Artifacts npm registry**
  - URL: https://bun.com/docs/guides/install/azure-artifacts.md

- **Using bun install with Artifactory**
  - URL: https://bun.com/docs/guides/install/jfrog-artifactory.md

- **Add a trusted dependency**
  - URL: https://bun.com/docs/guides/install/trusted.md

- **Generate a yarn-compatible lockfile**
  - URL: https://bun.com/docs/guides/install/yarnlock.md

- **Migrate from npm install to bun install**
  - URL: https://bun.com/docs/guides/install/from-npm-install-to-bun-install.md

- **Configure git to diff Bun's lockb lockfile**
  - URL: https://bun.com/docs/guides/install/git-diff-bun-lockfile.md

- **Install dependencies with Bun in GitHub Actions**
  - URL: https://bun.com/docs/guides/install/cicd.md

- **Run your tests with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/run-tests.md

- **Run tests in watch mode with Bun**
  - URL: https://bun.com/docs/guides/test/watch-mode.md

- **Migrate from Jest to Bun's test runner**
  - URL: https://bun.com/docs/guides/test/migrate-from-jest.md

- **Mock functions in `bun test`**
  - URL: https://bun.com/docs/guides/test/mock-functions.md

- **Spy on methods in `bun test`**
  - URL: https://bun.com/docs/guides/test/spy-on.md

- **Set the system time in Bun's test runner**
  - URL: https://bun.com/docs/guides/test/mock-clock.md

- **Use snapshot testing in `bun test`**
  - URL: https://bun.com/docs/guides/test/snapshot.md

- **Update snapshots in `bun test`**
  - URL: https://bun.com/docs/guides/test/update-snapshots.md

- **Generate code coverage reports with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/coverage.md

- **Set a code coverage threshold with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/coverage-threshold.md

- **Selectively run tests concurrently with glob patterns**: Set a glob pattern to decide which tests from which files run in parallel
  - URL: https://bun.com/docs/guides/test/concurrent-test-glob.md

- **Skip tests with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/skip-tests.md

- **Mark a test as a "todo" with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/todo-tests.md

- **Set a per-test timeout with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/timeout.md

- **Bail early with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/bail.md

- **Re-run tests multiple times with the Bun test runner**
  - URL: https://bun.com/docs/guides/test/rerun-each.md

- **Using Testing Library with Bun**
  - URL: https://bun.com/docs/guides/test/testing-library.md

- **Write browser DOM tests with Bun and happy-dom**
  - URL: https://bun.com/docs/guides/test/happy-dom.md

- **import, require, and test Svelte components with bun test**
  - URL: https://bun.com/docs/guides/test/svelte-test.md

- **Import a JSON file**
  - URL: https://bun.com/docs/guides/runtime/import-json.md

- **Import a TOML file**
  - URL: https://bun.com/docs/guides/runtime/import-toml.md

- **Import a YAML file**
  - URL: https://bun.com/docs/guides/runtime/import-yaml.md

- **Import a JSON5 file**
  - URL: https://bun.com/docs/guides/runtime/import-json5.md

- **Import an XML file**
  - URL: https://bun.com/docs/guides/runtime/import-xml.md

- **Import a HTML file as text**
  - URL: https://bun.com/docs/guides/runtime/import-html.md

- **Read a file as a string**
  - URL: https://bun.com/docs/guides/read-file/string.md

- **Read a file to a Buffer**
  - URL: https://bun.com/docs/guides/read-file/buffer.md

- **Read a file to a Uint8Array**
  - URL: https://bun.com/docs/guides/read-file/uint8array.md

- **Read a file to an ArrayBuffer**
  - URL: https://bun.com/docs/guides/read-file/arraybuffer.md

- **Read a JSON file**
  - URL: https://bun.com/docs/guides/read-file/json.md

- **Get the MIME type of a file**
  - URL: https://bun.com/docs/guides/read-file/mime.md

- **Check if a file exists**
  - URL: https://bun.com/docs/guides/read-file/exists.md

- **Watch a directory for changes**
  - URL: https://bun.com/docs/guides/read-file/watch.md

- **Read a file as a ReadableStream**
  - URL: https://bun.com/docs/guides/read-file/stream.md

- **Write a string to a file**
  - URL: https://bun.com/docs/guides/write-file/basic.md

- **Write a Blob to a file**
  - URL: https://bun.com/docs/guides/write-file/blob.md

- **Write a Response to a file**
  - URL: https://bun.com/docs/guides/write-file/response.md

- **Append content to a file**
  - URL: https://bun.com/docs/guides/write-file/append.md

- **Write a file incrementally**
  - URL: https://bun.com/docs/guides/write-file/filesink.md

- **Write a ReadableStream to a file**
  - URL: https://bun.com/docs/guides/write-file/stream.md

- **Write to stdout**
  - URL: https://bun.com/docs/guides/write-file/stdout.md

- **Write a file to stdout**
  - URL: https://bun.com/docs/guides/write-file/cat.md

- **Copy a file to another location**
  - URL: https://bun.com/docs/guides/write-file/file-cp.md

- **Delete a file**
  - URL: https://bun.com/docs/guides/write-file/unlink.md

- **Delete files**
  - URL: https://bun.com/docs/guides/runtime/delete-file.md

- **Delete directories**
  - URL: https://bun.com/docs/guides/runtime/delete-directory.md

- **Extract links from a webpage using HTMLRewriter**
  - URL: https://bun.com/docs/guides/html-rewriter/extract-links.md

- **Extract social share images and Open Graph tags**
  - URL: https://bun.com/docs/guides/html-rewriter/extract-social-meta.md

- **Convert an ArrayBuffer to a string**
  - URL: https://bun.com/docs/guides/binary/arraybuffer-to-string.md

- **Convert an ArrayBuffer to a Buffer**
  - URL: https://bun.com/docs/guides/binary/arraybuffer-to-buffer.md

- **Convert an ArrayBuffer to a Blob**
  - URL: https://bun.com/docs/guides/binary/arraybuffer-to-blob.md

- **Convert an ArrayBuffer to an array of numbers**
  - URL: https://bun.com/docs/guides/binary/arraybuffer-to-array.md

- **Convert an ArrayBuffer to a Uint8Array**
  - URL: https://bun.com/docs/guides/binary/arraybuffer-to-typedarray.md

- **Convert a Buffer to a string**
  - URL: https://bun.com/docs/guides/binary/buffer-to-string.md

- **Convert a Buffer to an ArrayBuffer**
  - URL: https://bun.com/docs/guides/binary/buffer-to-arraybuffer.md

- **Convert a Buffer to a blob**
  - URL: https://bun.com/docs/guides/binary/buffer-to-blob.md

- **Convert a Buffer to a Uint8Array**
  - URL: https://bun.com/docs/guides/binary/buffer-to-typedarray.md

- **Convert a Buffer to a ReadableStream**
  - URL: https://bun.com/docs/guides/binary/buffer-to-readablestream.md

- **Convert a Blob to a string**
  - URL: https://bun.com/docs/guides/binary/blob-to-string.md

- **Convert a Blob to an ArrayBuffer**
  - URL: https://bun.com/docs/guides/binary/blob-to-arraybuffer.md

- **Convert a Blob to a Uint8Array**
  - URL: https://bun.com/docs/guides/binary/blob-to-typedarray.md

- **Convert a Blob to a DataView**
  - URL: https://bun.com/docs/guides/binary/blob-to-dataview.md

- **Convert a Blob to a ReadableStream**
  - URL: https://bun.com/docs/guides/binary/blob-to-stream.md

- **Convert a Uint8Array to a string**
  - URL: https://bun.com/docs/guides/binary/typedarray-to-string.md

- **Convert a Uint8Array to an ArrayBuffer**
  - URL: https://bun.com/docs/guides/binary/typedarray-to-arraybuffer.md

- **Convert a Uint8Array to a Buffer**
  - URL: https://bun.com/docs/guides/binary/typedarray-to-buffer.md

- **Convert a Uint8Array to a Blob**
  - URL: https://bun.com/docs/guides/binary/typedarray-to-blob.md

- **Convert a Uint8Array to a DataView**
  - URL: https://bun.com/docs/guides/binary/typedarray-to-dataview.md

- **Convert a Uint8Array to a ReadableStream**
  - URL: https://bun.com/docs/guides/binary/typedarray-to-readablestream.md

- **Convert a DataView to a string**
  - URL: https://bun.com/docs/guides/binary/dataview-to-string.md

- **Convert a ReadableStream to a string**
  - URL: https://bun.com/docs/guides/streams/to-string.md

- **Convert a ReadableStream to JSON**
  - URL: https://bun.com/docs/guides/streams/to-json.md

- **Convert a ReadableStream to a Blob**
  - URL: https://bun.com/docs/guides/streams/to-blob.md

- **Convert a ReadableStream to a Buffer**
  - URL: https://bun.com/docs/guides/streams/to-buffer.md

- **Convert a ReadableStream to an ArrayBuffer**
  - URL: https://bun.com/docs/guides/streams/to-arraybuffer.md

- **Convert a ReadableStream to a Uint8Array**
  - URL: https://bun.com/docs/guides/streams/to-typedarray.md

- **Convert a ReadableStream to an array of chunks**
  - URL: https://bun.com/docs/guides/streams/to-array.md

- **Convert a Node.js Readable to a string**
  - URL: https://bun.com/docs/guides/streams/node-readable-to-string.md

- **Convert a Node.js Readable to JSON**
  - URL: https://bun.com/docs/guides/streams/node-readable-to-json.md

- **Convert a Node.js Readable to a Blob**
  - URL: https://bun.com/docs/guides/streams/node-readable-to-blob.md

- **Convert a Node.js Readable to an Uint8Array**
  - URL: https://bun.com/docs/guides/streams/node-readable-to-uint8array.md

- **Convert a Node.js Readable to an ArrayBuffer**
  - URL: https://bun.com/docs/guides/streams/node-readable-to-arraybuffer.md

- **Feedback**: Share feedback, bug reports, and feature requests
  - URL: https://bun.com/docs/feedback.md

## Additional Resources (Optional)

### Optional

- **Reference**
  - URL: https://bun.com/reference

- **Blog**
  - URL: https://bun.com/blog

## How to Use This Skill

Reference these resources when working with Bun.