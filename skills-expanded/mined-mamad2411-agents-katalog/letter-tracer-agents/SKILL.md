# Working in this repo

## Clear the cache before any browser test

**This app is a PWA. Its service worker precaches the whole build and serves it
back cache-first.** A browser that has ever loaded this app will keep serving
the old bundle after you rebuild — so a fix you just made looks like it did
nothing, and you go round in circles editing code that was never running. This
has burned several sessions. Clear the cache first, every time.

Before driving the app in a browser:

1. **Restart the preview server after every `npm run build`.** A `vite preview`
   started before the rebuild serves an `index.html` pointing at chunk hashes
   that no longer exist. The client then fails to hydrate _silently_: the page
   still renders the prerendered HTML, so it looks fine, but no JS runs and
   every interaction does nothing.

   ```sh
   npm run build
   pkill -f "vite preview"; npx vite preview --port 4173 --strictPort &
   ```

2. **Unregister the service worker and empty the caches in the test browser:**

   ```js
   await navigator.serviceWorker
   	.getRegistrations()
   	.then((r) => Promise.all(r.map((x) => x.unregister())));
   await caches.keys().then((k) => Promise.all(k.map((c) => caches.delete(c))));
   ```

3. **Disable the HTTP cache too** — over CDP, `Network.setCacheDisabled`. The
   service worker is not the only cache in the way: GitHub Pages serves the HTML
   shell with `max-age=600`, so the browser's own HTTP cache can hand back a
   ten-minute-old page even when the worker asks the network for a fresh one.

4. **Add a cache-busting query param** to the navigation URL
   (`?c=A&t=${Date.now()}`).

5. **Confirm which build you are actually testing** before trusting any result.
   The semver badge in the bottom-right corner is there for exactly this: if it
   does not show the version you just built, stop — you are testing old code.

The same applies on the live site. When checking a deploy, a single relaunch is
enough to pick up a new build (see `src/service-worker.ts`), but confirm it with
the version badge rather than assuming.

## Bump the version with the change

**Bump `version` in `package.json` in the same commit as any user-visible
change** — a fix, a new letter, a redrawn picture. Patch for a fix or a
content change; minor only when the app gains something it could not do
before. Redrawing a picture is a patch, however different it looks. The badge
is the only way to tell which build is in front of you, and a change that
ships without a bump makes it lie: the badge shows the version you already
had, so a correct fix looks like it never deployed.

## Verify, don't assume

Silent failures are the norm in this codebase, not the exception: cached
bundles, `Edit` calls that no-op after prettier reflows a line, SVG geometry
that only _approaches_ its control points, CSS contrast too low to read, and
`npm run check | tail` masking a non-zero exit code. Check the thing you changed
actually changed:

- Measure geometry programmatically (glyph ink extents, bounding rects, computed
  styles, contrast ratios) rather than eyeballing a screenshot.
- Drive the real UI with synthetic `PointerEvent`s for anything touch-related.
  The tracing engine's unit tests are pure geometry and cannot catch a component
  wiring bug.
- Check exit codes without piping through `tail`.
- After a string-substitution edit, confirm the new text is in the file.

## Tests

```sh
npm run check   # svelte-check, must be 0 errors and 0 warnings
npm test        # vitest, engine unit tests
npm run build
```

`src/lib/trace/engine.ts` is deliberately DOM-free so it can be unit tested;
keep it that way and put anything needing browser geometry in
`src/lib/glyphs/measure.ts` or the component.
