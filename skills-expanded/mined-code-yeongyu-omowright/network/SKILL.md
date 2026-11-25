---
name: network
description: Read the network instead of the DOM. Snoop JSON API responses, wait for a request instead of sleeping, collect items while scrolling, record a QA flight trace (jsonl, HAR, screenshots), and intercept requests with routes.
---

# Network

Every page session already has the `Network` domain on, so watching traffic
costs nothing and pages can't see it. All four tools come from the package
entrypoint:

```js
const { createNetworkSnoop, collectWhileScrolling, createTrace, createRoutes } = await import("omowright");
```

## Snoop before you scrape

When a page renders a list, a table, or search results, the data almost always
arrived as JSON one request earlier. That JSON is complete, typed, and free of
truncated labels. Snapshot to find and click; snoop to read.

```js
const snoop = createNetworkSnoop(page, { match: { url: /\/api\//, mimeType: "json" } }); // strings match as substrings
await page.goto("https://example.com/search?q=widgets");
const results = snoop.popJson(); // parsed bodies, buffer drained
console.log(snoop.summary({ max: 20 })); // "GET 200 application/json 8123B https://..."
snoop.dispose();
```

Create the snoop before the navigation or click that produces the traffic.
Entries land when the response finishes, so `match` may test `status` and
`mimeType`. `pop()` gives raw entries; `peek()` copies without draining.

## Wait for the request, not the clock

A fixed sleep either wastes time or fails on a slow day. Wait for the response
you need instead:

```js
const saved = snoop.waitFor({ url: "/api/cart", method: "POST" }, { timeoutMs: 10000 });
await page.locator("e7").click();
const entry = await saved; // { status, body, ... }
if (entry.status !== 200) throw new Error(`cart save failed: ${entry.status} ${entry.statusText}`);
```

Start the wait first, then act; a response that finishes before `waitFor` is
called goes to the buffer, not the waiter.

## Collect while scrolling

Infinite lists load pages over XHR as you scroll. Drive the scroll and drain
the snoop in one loop:

```js
const snoop = createNetworkSnoop(page, { match: { url: /\/feed\?/ } });
const items = [];
const gen = collectWhileScrolling(page, snoop, {
  minItems: 200,
  maxScrolls: 15,
  extract: (json) => json.items ?? [],
  scroll: "wheel", // "end" jumps to the bottom instead
  settleMs: 800,
});
let step;
while (!(step = await gen.next()).done) items.push(step.value);
step.value; // { rounds, total, stoppedBecause }
```

`for await (const item of gen)` works too when you don't need the return
value. The loop drains first, then scrolls, and stops on `minItems`,
`maxScrolls`, or two consecutive rounds where the document height didn't grow
(`noGrowth`). The default `extract` accepts bodies that are already arrays.

## Flight recorder for QA

`createTrace` records what happened while you drove the page, so a failed run
is a directory to read rather than a memory to reconstruct:

```js
const trace = createTrace(page, { dir: "/tmp/checkout-trace" });
await trace.step("open cart", () => page.goto("https://example.com/cart"));
await trace.step("apply coupon", async () => {
  await page.locator("e3").fill("SAVE10");
  await page.locator("e4").click();
});
trace.mark("expected total", { total: "90.00" });
const summary = await trace.stop(); // { steps, events, network, startedAt, endedAt, url }
```

What lands in `dir`:

- `trace.jsonl`: one JSON object per line, ordered by `seq`. `kind` is one of
  `step` (name, `durationMs`, `error`, screenshot paths), `network`, `console`,
  `dialog`, `navigation`, `download`, `mark`, `warning`. Grep it:
  `rg '"kind":"console"' trace.jsonl` or `jq -c 'select(.kind=="step")'`.
- `trace.har`: HAR 1.2 of every finished request; open it in DevTools or any
  HAR viewer to see timings and bodies.
- `summary.json`: the object `stop()` returned.
- `screenshots/<seq>-<slug>-before.png` and `-after.png` for every step.

Steps rethrow, so call `stop()` in a `finally` to keep the evidence from a
failure. The recorder rides the existing network and console paths.

## Routes: intercept with care

`createRoutes(page)` blocks, rewrites, or fakes requests:

```js
const routes = createRoutes(page);
await routes.route("*/analytics/*", ({ abort }) => abort("BlockedByClient"));
await routes.route(/\/api\/flags$/, ({ fulfill }) =>
  fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ beta: true }) }),
);
await routes.route(
  ({ method }) => method === "POST",
  ({ request, continue: go }) => go({ headers: { ...request.headers, "x-test-run": "1" } }),
);
// ... drive the page ...
await routes.dispose(); // Fetch.disable
```

Glob strings use `*` and `?`; a string without either is a substring match. A
handler that throws or never settles lets the request continue, with a warning.

Stealth caveat: `Fetch.enable` goes out on the first `route()`, and
interception changes the timing and blocking patterns that bot defenses score.
Leave routes off for WAF-protected targets and stealth profiles; use the snoop,
which is passive, to read the same traffic.
