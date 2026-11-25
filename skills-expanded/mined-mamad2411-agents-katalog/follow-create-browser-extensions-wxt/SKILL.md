---
name: follow-create-browser-extensions-wxt
description: "Build browser extensions with WXT + Manifest V3 on Chrome, Firefox, Edge"
argument-hint: "[scope]"
related:
  - follow-tasks
  - follow-lang-typescript
  - follow-tool-github-actions
  - run-dev

---

## Goal

Set up and develop Web Extensions with the WXT framework per best practices

## Scope

Use for creating, improving, and releasing Web Extensions with WXT; supports TypeScript and Bun

- Create a WXT project with the appropriate template
- Configure manifest, permissions, and build
- Separate pure logic from browser API integration
- Set up CI/CD for releasing to the Chrome Web Store

- Package: `wxt` (0.x — minor releases may break) — always confirm the latest version with `/deep-research` + `/follow-best-practice` (not pinned in files — per `/update-devin-global-skills`)

## Execute

### 1. Initialize Project

> Goal: Start a WXT project with the appropriate template

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `bunx wxt@latest init` to start the project
3. Choose the desired template (vanilla, react, vue, svelte, solid)
4. Install dependencies with `bun install`
5. Confirm `bun run dev` works (dev mode has HMR and opens a browser window automatically)

### 2. Configure WXT

> Goal: Set `wxt.config.ts` and the manifest

1. Edit `wxt.config.ts` per the requirements with `defineConfig()`
2. Define the manifest via the `manifest` option in `wxt.config.ts` (permissions and host permissions)
3. Set `srcDir` (default `.`) and `outDir` (default `.output`) if needed
4. For TypeScript configuration, run `/follow-lang-typescript`
5. Check that `wxt.config.ts` has no invalid paths

### 3. Structure Extension

> Goal: Create the extension structure with WXT file-based entrypoints that separate concerns clearly

1. Create `entrypoints/background.ts` for the background script (export default `defineBackground()`)
2. Create `entrypoints/content.ts` for the content script (export default `defineContentScript()`)
3. Create `entrypoints/popup/` for the popup UI (index.html + main script)
4. Keep pure logic in `utils/` (auto-imported) or `lib/`
5. Create browser API wrappers in `services/` or `utils/`
6. Have background/content/popup call the wrappers only
7. With `srcDir: "src"` → entrypoints move to `src/entrypoints/`

### 4. Setup CI/CD

> Goal: Set up GitHub Actions for build and release

1. Run `/follow-tool-github-actions` to set up CI/CD
2. Use the built-in `wxt submit` for automated publishing (run `bunx wxt submit init` to create `.env.submit` — add `.env.submit` to `.gitignore`)
3. Create `.github/workflows/release.yml` that runs `wxt zip` + `wxt submit` (use `chrome-webstore-upload-cli` only when a plain upload, separate from submit, is needed)
4. Set GitHub Secrets for the targeted stores (see Rules §5)
5. Confirm the workflow syntax is correct

### 5. Build And Release

> Goal: Build for production and release

1. Run `bun run build` to build for production into `.output/`
2. Run `bunx wxt zip` (and `wxt zip -b firefox` for Firefox — creates `*-firefox.zip` + `*-sources.zip`)
3. Test submission with `bunx wxt submit --dry-run` before the real release
4. Trigger the GitHub Actions workflow
5. Check store status (Chrome Web Store, Firefox AMO, Edge Add-ons)

## Rules

### 1. Project Structure

```text
project/
├── entrypoints/
│   ├── background.ts    # defineBackground()
│   ├── content.ts       # defineContentScript()
│   └── popup/           # index.html + main.ts
├── utils/               # auto-imported pure logic
├── services/            # browser API wrappers
├── public/              # copied as-is
├── .github/workflows/
├── wxt.config.ts
└── package.json
```

- The `utils/`, `composables/`, `components/`, `hooks/` directories are auto-imported by WXT
- `srcDir: "src"` works — entrypoints then live at `src/entrypoints/`

### 2. Separation Of Concerns

- Separate pure logic from browser API integration
- Pure logic lives in `utils/` or `lib/`
- Browser API wrappers live in `services/`
- Background/content/popup scripts call the wrappers only

### 3. Manifest Configuration

- Define only the minimum required permissions
- Prefer host permissions over `<all_urls>` when possible
- Version must follow semantic versioning
- Name and description must be clear
- Use Manifest V3 for Chrome/Edge — WXT builds Firefox as MV2 by default (`wxt build -b firefox` → `.output/firefox-mv2`); the manifest is defined via the `manifest` option in `wxt.config.ts`, not a raw `manifest.json`

### 4. Build Configuration

- Use Bun for reproducible builds
- `outDir` defaults to `.output/` — change it only when necessary
- Enable TypeScript strict mode
- Enable auto-imports for composables/utils

### 5. CI/CD Requirements

- A GitHub Actions workflow for release
- Use `wxt submit` for upload + submit review (Chrome, Firefox, Edge)
- Required secrets: `CHROME_EXTENSION_ID`, `CHROME_CLIENT_ID`, `CHROME_CLIENT_SECRET`, `CHROME_REFRESH_TOKEN` (+ `FIREFOX_EXTENSION_ID`, `FIREFOX_JWT_ISSUER`, `FIREFOX_JWT_SECRET` when targeting Firefox; `EDGE_PRODUCT_ID`, `EDGE_CLIENT_ID`, `EDGE_CLIENT_SECRET` for Edge)
- Use `CHROME_SKIP_SUBMIT_REVIEW=true` to upload without submitting for review
- The workflow must trigger on `workflow_dispatch`

### 6. Development Best Practices

- Use `bun run dev` for development mode
- Use TypeScript for type safety
- Write tests for pure logic
- Use ESLint and Prettier for code quality
- Use /run-dev if needed

## Expected Outcome

- The WXT project is installed and working
- The extension structure follows best practices
- The CI/CD workflow can release to the Chrome Web Store
- The code has high type safety and quality
