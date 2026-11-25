---
name: vscode-extension-publishing
description: Use when publishing a VS Code extension to the marketplace.
license: MIT
metadata:
  hermes:
    tags:
    - vscode
    - extension
    - marketplace
    - publishing
    - vsce
    related_skills:
    - vscode-extension-webview-dev
    - vscode-extension-review
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
  imported_from: hermes
---

# VS Code Extension Publishing

End-to-end workflow for preparing and publishing a VS Code extension to the Visual Studio Marketplace. Built from the dsh-for-vs-code v0.1.0 publishing session (2026-08-19).

## When to Use

- Publishing a VS Code extension to the Visual Studio Marketplace
- Preparing package.json, README, CHANGELOG for marketplace submission
- Converting SVG assets to PNG for marketplace compatibility
- Capturing real webview screenshots for README documentation
- Troubleshooting vsce package/publish errors (name conflicts, SVG rejection, missing fields)

## package.json Requirements

The following fields are required or strongly recommended for publishing:

```json
{
  "name": "extension-name",           // Must be unique on marketplace
  "displayName": "Human Readable Name", // Must be unique on marketplace
  "description": "Short description",
  "version": "0.1.0",
  "publisher": "your-publisher-id",    // Must match marketplace publisher
  "license": "MIT",
  "icon": "media/icon.png",           // PNG only, 128x128 or 256x256
  "private": false,                    // MUST be false for publishing
  "engines": { "vscode": "^1.95.0" },
  "extensionKind": ["workspace"],      // Required for webview extensions
  "author": { "name": "Your Name" },
  "keywords": ["keyword1", "keyword2"],
  "categories": ["Other"],
  "homepage": "https://github.com/...",
  "bugs": { "url": "https://github.com/.../issues" },
  "repository": { "type": "git", "url": "git+https://github.com/..." },
  "scripts": {
    "vscode:prepublish": "pnpm run build && pnpm run build:shell"
  }
}
```

### Critical Pitfalls

- **`private: true` blocks publishing** — `vsce publish` refuses to publish private packages
- **SVG icons rejected** — vsce errors: `SVGs can't be used as icons`. Convert to PNG with `rsvg-convert -w 128 icon.svg -o icon.png` or `sips -z 128 128 icon.png`
- **Name conflicts** — both `name` and `displayName` are checked for uniqueness. If either is taken, marketplace rejects with "already exists" or "display name is taken"
- **`vscode:prepublish` required** — runs automatically before `vsce package` and `vsce publish`. Without it, dist/ may be stale

## .vscodeignore

Create `apps/vscode/.vscodeignore` to exclude dev files from VSIX:

```
node_modules/
*.vsix
src/
web/
test/
scripts/
**/*.map
**/*.tsbuildinfo
tsconfig.json
vitest.config.ts
.oxlintrc.json
dist/web/dsh-plugins/
```

**Pitfall**: `.vscodeignore` only excludes what's listed. Unlisted files (`.eslintrc.json`, etc.) are auto-included. Use `vsce ls --tree` to verify VSIX contents.

## README Format

Marketplace README must follow these rules:

- **No SVG images** — vsce rejects them with "SVGs are restricted in README.md". Use PNG only
- **Bilingual format** (for Chinese projects): Chinese first, then English, as bullet points (`- ` prefix)
- **Feature sections**: Use `###` H3 headings
- **Images**: Place in `media/docs/` directory, reference as `![Alt](media/docs/image.png)`
- **Diagrams**: Use Mermaid code blocks for architecture/flow diagrams (rendered by marketplace)

Example structure:
```markdown
# Extension Name

- 中文简介
- English description

## 功能 / Features

### Feature Name

- 中文描述
- English description

![Screenshot](media/docs/screenshot.png)
```

## CHANGELOG.md

Required for marketplace listing. Use Keep a Changelog format:

```markdown
# Changelog

## [0.1.0] — 2026-08-19

### Added

- Feature 1
- Feature 2
```

## Publishing Workflow

### 1. First-time Setup

```bash
# Install vsce (if not installed)
npm install -g @vscode/vsce

# Create publisher at https://marketplace.visualstudio.com/manage/publishers/
# Create PAT at https://aex.dev.azure.com/app/register/personalaccesstokens
# Scopes: Marketplace → Manage

# Login
vsce login <publisher-id>
# Paste PAT when prompted
```

### 2. Package and Test

```bash
cd apps/vscode

# Package (runs vscode:prepublish automatically)
npx vsce package --out ~/Desktop/

# Test locally
code --install-extension ~/Desktop/extension-name-0.1.0.vsix
```

### 3. Publish

```bash
# Publish to marketplace
npx vsce publish

# Or publish from VSIX
npx vsce publish --packagePath ~/Desktop/extension-name-0.1.0.vsix
```

### 4. Version Updates

```bash
# Auto-bump version
npx vsce publish patch   # 0.1.0 → 0.1.1
npx vsce publish minor   # 0.1.0 → 0.2.0
npx vsce publish major   # 0.1.0 → 1.0.0

# Or specify version
npx vsce publish 0.2.0
```

## PAT Authentication

- PATs are created at Azure DevOps: https://aex.dev.azure.com/app/register/personalaccesstokens
- Organization: "All accessible organizations"
- Scopes: "Marketplace" → "Manage"
- PATs are displayed only once — copy immediately
- **PAT retirement**: Azure DevOps Global PAT retiring 2026-12-01. For CI/CD, use Microsoft Entra ID / workload identity federation

## CI/CD Publishing

For GitHub Actions, use `vsce publish` with PAT stored as secret:

```yaml
- name: Publish
  run: npx vsce publish
  env:
    VSCE_PAT: ${{ secrets.VSCE_PAT }}
```

**Note**: PAT-based CI/CD will need migration to Entra ID after 2026-12-01.

## Smoke Test Screenshot Capture

For capturing real webview screenshots (not SVG mockups):

```bash
# Requires: dsh web instance running on port 3080
# Uses Playwright from vendor/deepseek-harness

cd apps/vscode
node --input-type=module -e "
import { createServer } from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const SHELL = 'dist/web/dsh-shell';
const UPSTREAM = 'http://127.0.0.1:3080';
const SHELL_PORT = 8957;
const RELAY_PORT = 8958;

// Static server + relay proxy (same as smoke-shell.mjs)
// ... (see smoke-shell.mjs for full setup)

// Launch Chrome, navigate, wait for render
await page.goto('http://127.0.0.1:' + SHELL_PORT + '/index.html');
await page.waitForTimeout(12000);

// For session management view:
await page.evaluate(() => {
  if (window.__dshBridge?.setView) window.__dshBridge.setView('sessions');
});
await page.waitForTimeout(5000);

await page.screenshot({ path: 'media/docs/screenshot.png' });
"
```

**Key points**:
- Set `__DSH_WEB_URL__` to relay proxy (bypasses Origin restrictions)
- Set `__DSH_HOST__` and `__DSH_BOOT_SESSION__` for proper initialization
- Use `bridge.setView('sessions')` to switch to session management view
- Wait 10-12 seconds for full render before capturing

## Verification Checklist

Before publishing, verify:

- [ ] `private: false` in package.json
- [ ] `vscode:prepublish` script exists and works
- [ ] Icon is PNG (not SVG)
- [ ] `name` and `displayName` are unique on marketplace
- [ ] README has no SVG images
- [ ] CHANGELOG.md exists
- [ ] `.vscodeignore` excludes dev files
- [ ] `vsce ls --tree` shows correct VSIX contents
- [ ] VSIX installs and works locally
