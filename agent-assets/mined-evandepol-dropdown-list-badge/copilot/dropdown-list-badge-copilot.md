# Copilot Instructions for dropdown-list-badge

## Project Overview
- Home Assistant Lovelace custom badge for selecting and displaying `input_select` entity values via a dropdown.
- Designed for user-specific UI, accessibility, and robust integration with Home Assistant and HACS.

## Architecture & Key Components
- Main source: `dropdown-list-badge.ts` (TypeScript)
  - Contains badge and editor components.
  - Registers custom elements globally via `globalThis.customCards` for Home Assistant discovery.
- Build output: `dist/dropdown-list-badge.js` (bundled via esbuild, IIFE format).
- Editor UI: Renders in shadow DOM, preserves focus/caret, supports live config changes.
- Versioning: Injected from `version.json` at build time.

## Developer Workflows
- **Build:**
  - `npm run build` (type-checks with `tsc --noEmit`, bundles with `esbuild`).
  - Version injected via `prebuild` script using `jq` and `sed`.
- **Test:**
  - `./run-test.sh` builds, serves, and runs Playwright tests in Docker/Colima.
  - Visual regression snapshots and HTML reports in `tests/` and `tests/html-report/`.
- **Environment:**
  - Use `./start-docker-env.sh` and `./stop-docker-env.sh` to manage Colima/Docker and required tools (e.g., `jq`).
- **CI/CD:**
  - GitHub Actions workflow (`validate.yaml`) uses Docker layer caching, builds/tests in a single job, and extracts/uploads artifacts from the built image.
  - Dist updates are committed via PR from `update-dist-artifact` branch.

## Project-Specific Patterns & Conventions
- **Custom Element Registration:**
  - Register via `globalThis.customCards` for Home Assistant compatibility.
- **TypeScript Exports:**
  - Export classes for Playwright tests, but bundle as IIFE for Home Assistant (no top-level exports in final JS).
- **User-Specific UI:**
  - Use per-user `input_select` helpers and Home Assistant’s conditional visibility for personalized dashboards.
- **Error Handling:**
  - Defensive guards in `_render()` and dropdown logic to avoid undefined `hass`/`states` errors.
- **Build Output:**
  - Only the bundled JS in `dist/` is used by Home Assistant/HACS; source TS is for development/testing only.

## Integration Points
- **Home Assistant:**
  - Badge loaded as Lovelace resource (via HACS, e.g., `/hacsfiles/dropdown-list-badge/dist/dropdown-list-badge.js`).
- **HACS:**
  - `hacs.json` must specify correct filename and `content_in_root: false` for proper deployment.
- **Playwright:**
  - UI and visual regression tests in `tests/badge.spec.ts`.
- **Colima/Docker:**
  - All dev/test tools run in containers; no global install required.

## Examples & References
- See `dropdown-list-badge.ts` for custom element registration and defensive rendering.
- See `run-test.sh` and `start-docker-env.sh` for local dev/test orchestration.
- See `README.md` for concise configuration and user-specific UI patterns.
- See `.github/workflows/validate.yaml` for CI/CD, Docker caching, and artifact handling.

---
**For AI agents:**
- Always reference the bundled JS in `dist/` for Home Assistant/HACS integration.
- Use Colima/Docker scripts for local dev/test; avoid global installs.
- Follow defensive rendering and registration patterns in `dropdown-list-badge.ts`.
- When updating workflows, preserve Docker caching and artifact extraction steps.
