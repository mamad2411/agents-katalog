# Browser Module

Provides Playwright automation and scoped content-ingest for auth-walled/JS-gated sources.

- Tools are in the `browser` group for progressive disclosure.
- All interactive tools are classified as `dangerous` risk since they execute
  page-side JS and can trigger external side effects. `browser_close` is `safe`.
- Playwright is lazy-imported at first use via `playwright-loader.ts`. The
  module loads cleanly without Playwright installed and logs a warning.
- Each scope/session owns its Chromium process, authenticated context/pages, and
  authenticated loopback proxy. They close together on idle timeout or session
  cleanup; module unload closes only its scope's resources.
- Each session resolves browser configuration through the shared trusted config
  loader using its canonical scope directory and machine authority config path.
  It captures that profile for its lifetime, never another scope's module-load
  settings or the isolated writer's working directory.
- Chromium's proxy applies that session's captured outbound target policy and
  DNS-pins every connection, including redirects,
  click navigations, WebSocket tunnels, and subresources.
- `modules.browser.networkProfile` defaults to `public-untrusted`, rejecting
  loopback, private, link-local, and rebinding targets. Private access requires
  `configured-provider` with every page origin in `allowedOrigins`; the proxy
  still resolves and pins the connection-time address.

## Authenticated Browser Profile

Operators configure a persistent login session via `modules.browser`
(`storageStatePath`, `persistProfile`, `headless`).

- `storageStatePath` points at a Playwright [`storageState`](https://playwright.dev/docs/auth)
  JSON file containing cookies and localStorage for an authenticated session.
  Relative paths resolve against the invoking scope's scope directory. If
  the file exists, that session's browser context is created with it loaded;
  if it does not, the module falls back to an ephemeral context.
- Scope-escaping profile paths belong only to their configuring scope; other
  scopes stay ephemeral. Prefer scope-local paths.
- Profile persistence remains disabled pending qualification of the core
  private-file publisher on contained Linux. Explicit save and awaited close
  reject before collecting credentials; close still releases browser resources.
  Keep `persistProfile` false to load existing state without saving changes.
  Playwright's context port accepts no output path. Do not activate the candidate
  writer until positive private publication and adversarial boundary proof pass.
  Its supported layout requires an unprivileged Linux service, Python 3, procfs,
  anonymous temporary-file support, and administrator-protected ancestors above
  the destination directory. For example, an administrator can provision
  `/var/lib/kota-profiles` owned by the service user with mode `0700`, under
  protected `/var` and `/var/lib`. A future profile can be a direct child of that
  directory with a matching agent write grant. Nested writable workspace layouts
  remain unsupported because their ancestors can move. Agents must not alter
  host ownership or permissions to satisfy this requirement. The read-only
  source-access report does not certify persistence readiness.
- Never check storage-state files into source; keep them in the secrets surface.
- The scope-resolved profile source is shared by its tools; live cookies,
  localStorage, and page state remain isolated per scope and session.
- `headless` defaults to `true`. Set `modules.browser.headless=false` only
  for operator-run source-access captures where a vendor blocks headless
  automation but allows a normal headed browser session. This is an explicit
  operator capability setting, not a silent fallback.

## Content-Ingest Tools

- `browser_navigate` — URL navigation whose result includes the final URL and
  the remote page's title.
- `browser_get_text` — raw `innerText` extraction of a page or element. Use
  it for ad-hoc inspection of already-navigated pages.
- `x_post_read` — scoped X/Twitter status reader. Navigates until DOM content
  is available, waits for the tweet article, and returns post body + author +
  up to `max_replies` reply texts. Requires an authenticated profile for posts
  behind the X auth wall; without one the tool returns a typed failure
  ("redirected to X login" or "X displayed an auth-wall / login prompt"). X
  scraping outside of normal reading volumes is discouraged; this tool is
  intentionally narrow to one post per call.
- `rendered_article_read` — JS-gated article reader. Navigates, waits for
  DOM content plus a readable page container, and extracts article/main text
  (or selector/body fallback). Returns a typed failure for Cloudflare/JS
  challenges that never clear.

All four content-ingest tools are included in
`DEFAULT_TARGET_TOOLS` for the `injection-defense` middleware, so autonomous
runs see the standard "BEGIN UNTRUSTED CONTENT" annotation on suspicious
payloads.

## Source-Access Capability Reports

Operators can run `kota browser source-access-report` to produce the redacted
capability report used for auth-walled research unblock evidence. Pass
`--article-url` for `rendered_article_read`, `--x-url` for `x_post_read`, and
`--run-id auth-walled-source-access-live` when producing the canonical live
capture under `.kota/runs/auth-walled-source-access-live/`.

The command writes `source-access-report.json`, `source-access-summary.md`, and
`source-access-transcript.txt`. It records Playwright/profile readiness,
invokes the existing scoped reader tool names through tool middleware, and
persists only redacted messages and short sanitized excerpts. Do not add raw
cookies, localStorage, bearer tokens, storage-state JSON, or full source bodies
to these artifacts.

## Failure Modes

- Missing Playwright → the tool runner throws the same "Playwright is not
  installed" error path the interactive tools use.
- Missing profile for auth-walled content → typed failure explaining the
  configuration knob the operator needs to set.
- JS challenge still present after network idle → typed failure naming the
  gate so the caller can back off or route to a different tool.
- Navigation / extract timeout → typed failure with the observed timeout
  value so callers can decide whether to retry.

## Extending

- New content-ingest tools should be added to `DEFAULT_TARGET_TOOLS` in
  `src/modules/injection-defense/defense-middleware.ts`. Browser-driven text
  extraction carries the same injection risk as `web_fetch`.
- Scoped-site tools (future: Discord, LinkedIn, GitHub-private) follow the
  `x_post_read` shape — a narrow `*_read` tool with a URL whitelist regex,
  auth-gate detection, structured extraction, and a typed failure envelope.
  Do not generalise into a god-tool until a second scoped site lands.
- Vendor TOS: if a scoped tool reads a source whose terms forbid automated
  access, document it in the tool's description and route through operator
  approval, not the autonomy default.
