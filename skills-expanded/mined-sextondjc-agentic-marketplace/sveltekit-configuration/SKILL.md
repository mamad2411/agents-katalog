---
name: sveltekit-configuration
description: Use when configuring svelte.config.js for a SvelteKit application including base paths, aliases, CSP headers, CSRF settings, preload strategies, version management, and kit-level build options.
---

# SvelteKit Configuration

## Specialization

Expert guidance for `svelte.config.js` configuration in SvelteKit. Covers the full `kit` config object: `paths.base` and `paths.assets` for sub-path deployment, `alias` for import shortcuts, `files.*` for custom source layout, `csrf.checkOrigin`, `csp` (Content Security Policy), `version.name` and `version.pollInterval` for deployment versioning, `preloadStrategy`, `embedded` mode, `inlineStyleThreshold`, and `env.privatePrefix` / `env.publicPrefix`.

## Trigger Conditions

- Deploying a SvelteKit app at a sub-path (e.g. `https://example.com/my-app/`) and links or assets are broken.
- Configuring a Content Security Policy (CSP) for a SvelteKit application.
- Setting up path aliases (e.g. `$components`, `$utils`) beyond the built-in `$lib`.
- Customising the SvelteKit source directory layout (non-default `src/routes` or `src/lib` paths).
- Disabling or adjusting CSRF origin checking for a specific deployment context.
- Implementing deployment version detection so SvelteKit can prompt users to reload after a new release.
- Diagnosing broken asset URLs, alias resolution failures, or CSP violation errors in a SvelteKit app.

## Scope Boundaries

In scope:

- `svelte.config.js` structure: `kit` key and all its documented sub-keys.
- `paths.base`: sub-path prefix; effect on `$app/paths`, asset URLs, and navigation.
- `paths.assets`: separate asset CDN origin.
- `alias`: custom import aliases added to Vite's `resolve.alias` via `svelte.config.js`.
- `files.routes`, `files.lib`, `files.appTemplate`, `files.errorTemplate`, `files.hooks.server`, `files.hooks.client`, `files.serviceWorker`, `files.assets`: customising source layout.
- `csrf.checkOrigin`: when and why to adjust the default `true` setting.
- `csp.mode` (`'auto'` | `'hash'` | `'nonce'`), `csp.directives`, `csp.reportOnly`.
- `version.name` and `version.pollInterval` for `updated` store integration.
- `preloadStrategy` (`'modulepreload'` | `'preload-js'` | `'preload-mjs'`).
- `embedded`: disabling top-level navigation handling for embedded SvelteKit apps.
- `inlineStyleThreshold`: CSS inlining threshold in bytes.
- `env.dir`, `env.privatePrefix`, `env.publicPrefix`: environment variable loading customisation.
- `Vite` config integration via the `vite` key in `svelte.config.js`.

Out of scope:

- Adapter configuration — covered by `sveltekit-adapters`.
- Environment variable access at runtime — covered by `sveltekit-environment`.
- SvelteKit library packaging (`@sveltejs/package`) — covered by `sveltekit-packaging`.
- Svelte compiler options (the `compilerOptions` key) — Svelte core concern.

## Inputs

- Deployment target URL structure (root vs. sub-path).
- Custom source layout requirements (non-default routes or lib paths).
- CSP policy requirements (nonce-based, hash-based, or auto).
- Import alias requirements beyond `$lib`.
- Version management and polling requirements.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| `svelte.config.js` | Correctly configured file for the stated requirements |
| Sub-path deployment fix | `paths.base` set; all internal links and asset references updated |
| CSP configuration | `csp.mode` and `csp.directives` set to satisfy policy requirements |
| Alias declarations | `alias` entries added and verified against Vite resolution |
| Configuration quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Set a custom alias and confirm it resolves | `alias` entry added; TypeScript path mapping updated in `tsconfig.json` |
| L2 Practical Delivery | Sub-path deployment with correct asset paths | `paths.base` set; `base` from `$app/paths` used in all internal `href` values |
| L3 Specialist Hardening | CSP with nonce or hash mode and CSRF configuration | `csp.directives` correct; no CSP violations; `csrf.checkOrigin` rationale documented |
| L4 Expert Standardisation | Full production `svelte.config.js` with version management, CDN assets, and custom layout | All keys documented; version polling configured; asset CDN origin set |

## Workflow

1. Start with the minimal config: `import adapter from '...'` and `export default { kit: { adapter } }`.
2. For sub-path deployment, set `kit.paths.base` to the path prefix (e.g. `'/my-app'`); import `base` from `$app/paths` and prepend it to every internal `href` and `src` attribute.
3. For a separate asset origin (CDN), set `kit.paths.assets` to the CDN base URL; SvelteKit will prepend it to all generated asset URLs.
4. For import aliases, add entries to `kit.alias`: `{ '$components': 'src/components' }`; also add matching `paths` entries to `tsconfig.json` so TypeScript resolves them.
5. To customise source layout, override `kit.files.*` keys; verify that the `handle` hook paths, routes directory, and app template all resolve correctly after the change.
6. For CSP, set `kit.csp.mode`:
   - `'auto'`: SvelteKit chooses hash or nonce based on adapter support.
   - `'hash'`: works with static/prerendered pages; SvelteKit inlines hashes for inline scripts and styles.
   - `'nonce'`: requires a server that can inject a per-request nonce; add nonce generation in the `handle` hook.
7. Set `kit.csp.directives` with a `script-src` and `style-src` appropriate for your deployment; include `'self'` and any required CDN origins.
8. For deployment version management, set `kit.version.name` to a build identifier (e.g. `process.env.GIT_SHA`); set `kit.version.pollInterval` (in ms) for automatic client-side checking. The `updated` signal in `$app/state` becomes active.
9. For `csrf.checkOrigin`, leave at default `true` unless the app is served from a context where the `Origin` header is legitimately absent (e.g. certain native webview integrations); document the rationale explicitly.
10. Run the configuration quality checklist.

## Configuration Quality Checklist

- [ ] `paths.base` is set for all sub-path deployments; no hardcoded absolute paths remain in template code.
- [ ] All internal `href` and `src` attributes in templates prepend `base` from `$app/paths` when `paths.base` is non-empty.
- [ ] `alias` entries in `svelte.config.js` have matching `paths` entries in `tsconfig.json`.
- [ ] `csp.mode` is set explicitly; default (`undefined`) is not used in production.
- [ ] `csp.directives` does not contain `'unsafe-inline'` for `script-src` unless no other option exists and it is documented.
- [ ] `csrf.checkOrigin` is `true`; any `false` override is documented with a security rationale.
- [ ] `version.name` is set to a build-time identifier (not a static string) for production deployments.
- [ ] `kit.files.*` overrides are intentional and all referenced paths exist in the repository.
- [ ] `env.privatePrefix` and `env.publicPrefix` match the variable naming convention in use across the project.

## Security Notes

- `csrf.checkOrigin: false` disables SvelteKit's built-in CSRF protection for form actions. Only set this when you have an explicit alternative CSRF mitigation and have documented the justification.
- `csp.directives` with `'unsafe-inline'` on `script-src` negates most of the security benefit of CSP. Use `'nonce'` or `'hash'` mode instead.
- `paths.assets` pointing to a third-party CDN domain means that domain can serve arbitrary content as your assets. Verify the CDN provider's security controls.
- `version.pollInterval` sends periodic requests from the client to your server; ensure the version endpoint does not expose sensitive deployment information.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Sub-path deployment | Workflow steps 2–3 |
| Import aliases | Workflow step 4 |
| Custom source layout | Workflow step 5 |
| CSP configuration | Workflow steps 6–7 |
| Deployment version management | Workflow step 8 |
| CSRF configuration | Workflow step 9 |
| Security hardening | Security Notes + checklist |
| Quality validation | Configuration Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
