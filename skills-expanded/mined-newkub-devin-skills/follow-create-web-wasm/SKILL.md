---
name: follow-create-web-wasm
description: Build websites with Rust WASM + Solid frontend via a Vite plugin
argument-hint: "[project-name]"
allowed-tools:
  - exec
  - read
  - edit
  - write
  - ask_user_question
related:
  - follow-create-rust-crate
  - follow-lib-solidjs
  - follow-tool-vite
  - follow-tool-cargo
  - deep-review-codebase
  - follow-create-plugins
  - follow-service-cloudflare
  - deploy-to-vercel
  - deploy-to-cloudflare
  - run-dev

---

## Goal

Build a website project that runs heavy Rust computation in the browser via WebAssembly, with SolidJS on Vite for the frontend

## Scope

Use when a task needs Rust performance in the browser without writing a backend, e.g. image/audio processing, simulation, cryptography, graph layout, or computational geometry

- Packages: `wasm-pack`, `wasm-bindgen`, `serde-wasm-bindgen`, `vite-plugin-wasm-pack` — always verify the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`); the `--target web` flow + `crate-type = ["cdylib"]` is still a requirement

## Execute

### 1. Review Tech Stack And Verify Toolchain

> Goal: Check the tech stack and confirm Rust and wasm-pack are ready

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest `wasm-pack`/`wasm-bindgen` versions, then run `/deep-review-codebase` to summarize the tech stack
2. Record the stack and library choices for future reference (web wasm)
4. Run `rustc --version` and `cargo --version`
5. Run `wasm-pack --version`; if missing → install with `cargo install wasm-pack`
6. Run `bun --version` or `node --version` for frontend tooling
7. If the `wasm32-unknown-unknown` target is missing → run `rustup target add wasm32-unknown-unknown`

### 2. Create Rust Crate

> Goal: Create a Rust library to compile to WASM

1. Run `cargo new --lib <project-name>-core`
2. Edit `Cargo.toml`:
   - `crate-type = ["cdylib"]`
   - Add `wasm-bindgen` and `serde` if you need to pass complex data
3. Create `src/lib.rs` with public functions, e.g.:
   ```rust
   use wasm_bindgen::prelude::*;

   #[wasm_bindgen]
   pub fn fibonacci(n: u32) -> u64 {
       match n {
           0 => 0,
           1 => 1,
           _ => fibonacci(n - 1) + fibonacci(n - 2),
       }
   }
   ```
4. Run `cargo check` to verify syntax

### 3. Build WASM Package

> Goal: Generate the `.wasm` and JS bindings from the Rust crate

1. Run `wasm-pack build <project-name>-core --target web --out-dir pkg`
2. Verify that `pkg/<project-name>_core.js`, `pkg/<project-name>_core_bg.wasm`, and `package.json` are generated
3. If `wasm-pack` dependencies are missing → rerun `wasm-pack build` after fixing `Cargo.toml`

### 4. Setup Vite + Solid Frontend

> Goal: Create the frontend project with Solid

1. Run `bun create vite@latest <project-name>-web --template solid-ts`
2. Enter `<project-name>-web` and run `bun install`
3. Install the wasm-pack Vite plugin: `bun add -D vite-plugin-wasm-pack`
4. Create a symlink or copy the crate's `pkg/` into `web/pkg`
5. Edit `package.json` to include the scripts:
   ```json
   "wasm": "wasm-pack build ../<project-name>-core --target web --out-dir pkg",
   "dev": "bun wasm && vite",
   "build": "bun wasm && tsc && vite build"
   ```

### 5. Configure Vite

> Goal: Configure Vite to load the WASM package

1. Edit `vite.config.ts`:
   ```ts
   import { defineConfig } from 'vite';
   import solid from 'vite-plugin-solid';
   import wasmPack from 'vite-plugin-wasm-pack';

   export default defineConfig({
     plugins: [
       solid(),
       wasmPack('../<project-name>-core'),
     ],
   });
   ```
2. If using `vite-plugin-wasm` instead, add the `topLevelAwait` plugin
3. Check that `tsconfig.json` supports the `esnext` module

### 6. Call Rust From Solid

> Goal: Use WASM functions in Solid components

1. In `src/App.tsx`, import functions from the crate:
   ```tsx
   import { createResource, Show } from 'solid-js';
   import * as wasm from '<project-name>-core';

   export default function App() {
     const [result] = createResource(async () => wasm.fibonacci(40));
     return (
       <div>
         <Show when={!result.loading} fallback={<p>computing...</p>}>
           <p>fibonacci(40) = {result()}</p>
         </Show>
       </div>
     );
   }
   ```
2. Use `createResource` when loading WASM asynchronously
3. If the plugin makes the import sync → a plain `createSignal` works

### 7. Add State And UX

> Goal: Build UI covering the Rust function's usage

1. Create `src/components/` for the input form, result display, and error boundary
2. Use `createStore` if state is complex
3. Use `<ErrorBoundary>` to handle WASM init errors
4. Follow `/follow-lib-solidjs` to check Solid patterns

### 8. Test And Build

> Goal: Confirm the project builds for both Rust and Vite

1. Run `cargo test` in the crate directory
2. Run `bun run build` in the web directory
3. Run `bun run dev` to check dev mode
4. Run `/run-test` for the frontend if test suites exist

### 9. Deploy And Ship

> Goal: Deploy the website to the chosen platform and deliver the project

1. If Vercel → `bunx vercel --prod`
2. If Cloudflare Pages → follow `/follow-service-cloudflare`
3. Verify `.wasm` files are served with the MIME type `application/wasm`
4. Test the production URL with a heavy function
5. Run `/ship`
6. If `ship` fails → report the status

## Rules

### 1. Rust Crate

- Use `wasm-bindgen` to expose functions to JS
- Use `serde-wasm-bindgen` if you need to pass objects/complex data
- Avoid `unwrap()` in library code
- `Cargo.toml` must have `crate-type = ["cdylib"]`
- Use `wasm-pack --target web` for browser ESM

### 2. Vite Plugin

- Use `vite-plugin-wasm-pack` for crates built with `wasm-pack`
- Use `vite-plugin-wasm` + `vite-plugin-top-level-await` if importing `.wasm` directly
- Don't commit `pkg/` or `target/` — add them to `.gitignore`

### 3. Solid Frontend

- Use `.tsx` for all components
- Never destructure props — use `mergeProps`/`splitProps`
- Use `createResource` for async WASM initialization
- Use `createSignal` for sync state

### 4. Performance

- Move heavy computation to Rust WASM, not the main thread
- Consider Web Workers for batch processing
- Check `cargo build --release` before deploying

### 5. Safety

- Don't expose raw pointers/memory to JS unless necessary
- Use `#[wasm_bindgen]` types supported by `wasm-bindgen`
- Don't commit secrets or API keys

- Use /follow-create-rust-crate if needed
- Use /follow-tool-vite if needed
- Use /follow-tool-cargo if needed
- Use /deep-review-codebase if needed
- Use /follow-create-vite-plugin if needed (create website rust)
- Use /deploy-to-vercel if needed
- Use /deploy-to-cloudflare if needed
- Use /run-dev if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- The Rust crate builds via `wasm-pack` and produces a `pkg/` usable in the browser
- The Vite + Solid project runs `bun run dev` without errors
- Rust functions are called from a Solid component and render results on the page
- The production build succeeds and is ready to deploy
- The project structure follows Rust + Vite + Solid conventions

