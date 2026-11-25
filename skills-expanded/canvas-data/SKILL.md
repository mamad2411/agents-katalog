---
name: canvas-data
description: "Holding and shaping data inside a standalone HTML page: localStorage done safely as a per-viewer convenience, a light/dark toggle that persists, importing and exporting JSON or CSV with no server, rendering a list or table from an array, and drawing a chart to scale. Read when a canvas page remembers, loads, saves or visualises data."
---

# Data in a standalone page, with no server

A page that opens from disk has no database and no backend. Everything it
remembers lives in the one browser it was opened in; everything it loads, the
person hands it as a file; everything it saves, it hands back as a file. This
skill is those four jobs: persist, toggle, move data in and out, and render
it.

## 1. localStorage, as a convenience only

`localStorage` is per-origin, per-browser, and for a `file://` page the origin
is fragile. Treat it as a nicety that may be absent, never as the source of
truth the page depends on.

```js
const store = {
  get(key, fallback) {
    try { const v = localStorage.getItem(key); return v == null ? fallback : JSON.parse(v); }
    catch { return fallback; }
  },
  set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private window, full quota */ }
  },
};
```

- Every read and write is wrapped in try/catch: a private window throws, a
  full quota throws, a blocked origin returns nothing. The page renders
  correctly when it comes back empty.
- Store per-viewer conveniences only: a remembered tab, a theme choice, a
  draft, the rows the person entered on this machine. Not anything that must
  be shared, must survive a move to another machine, or must be trusted.
- Namespace the key so two pages opened from the same folder do not collide:
  `tipsplitter.rows`, not `rows`.

## 2. A theme toggle that persists

Combine the OS default (the media query in the `canvas` skill) with an
explicit choice stored per viewer. Set the attribute before the first paint
so there is no flash.

```html
<script>
  // in <head>, before the body paints:
  try {
    const t = localStorage.getItem("app.theme");
    if (t === "dark" || t === "light") document.documentElement.dataset.theme = t;
  } catch {}
</script>
```

```js
function setTheme(t) {                 // "dark" | "light"
  document.documentElement.dataset.theme = t;
  store.set("app.theme", t);
}
toggle.addEventListener("click", () => {
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  const current = document.documentElement.dataset.theme || (dark ? "dark" : "light");
  setTheme(current === "dark" ? "light" : "dark");
});
```

The toggle itself is an icon button, a sun or a moon and no text beside
it, named by `aria-label` (and `title`) for what it does, updated on each
switch:

```html
<button id="theme" class="icon-button" type="button" aria-label="Switch to dark theme"
        title="Switch to dark theme">
  <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><!-- moon --></svg>
</button>
```

The CSS has the three blocks from the `canvas` skill: bare `:root` (light),
`@media (prefers-color-scheme: dark) :root` (OS dark), and
`:root[data-theme="dark"]` / `:root[data-theme="light"]` so the toggle wins
both ways.

## 3. Loading a file the person gives you

No `fetch`; the person chooses a file and the page reads it with `FileReader`
or the File API. This works from a `file://` page.

```js
fileInput.addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    const text = await file.text();
    const rows = file.name.endsWith(".csv") ? parseCsv(text) : JSON.parse(text);
    set({ rows });
  } catch (err) {
    showError("That file could not be read as " + (file.name.endsWith(".csv") ? "CSV" : "JSON") + ".");
  }
});
```

- Support drag and drop too when it suits: `dragover` (preventDefault) and
  `drop` (read `e.dataTransfer.files[0]`).
- Parsing can fail; wrap it and show a message on the page, never a thrown
  error or a silent nothing.
- A tiny CSV parser is fine for simple data; for quoted fields and embedded
  commas, load a small parser from a CDN rather than getting it subtly wrong.

## 4. Saving without a server

The page builds the file in memory and offers it as a download through a
`blob:` URL. This works from disk in a browser.

```js
function download(filename, text, type = "application/json") {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
}
saveBtn.addEventListener("click", () => {
  download("data.json", JSON.stringify(state.rows, null, 2));
});
```

- Export JSON for round-tripping (the page can load its own export), CSV for
  a spreadsheet. Offer whichever the person actually needs.
- Revoke the object URL after the click so it is not held forever.
- Note: a download started this way works in a normal browser opening the
  file; some embedded or locked-down viewers block it. For a page that is
  only ever opened as a local file in a browser, this is the right tool.

## 5. Rendering a list or table from an array

Render from the state array; rebuild the rows on change rather than mutating
them in place for a small list. Build nodes, do not concatenate HTML from
user data (an imported name with `<` must not become markup).

```js
function renderRows() {
  tbody.replaceChildren(...state.rows.map((r) => {
    const tr = document.createElement("tr");
    const name = document.createElement("td"); name.textContent = r.name;
    const amt = document.createElement("td");
    amt.textContent = r.amount.toFixed(2);
    amt.style.fontVariantNumeric = "tabular-nums";   // digits line up
    tr.append(name, amt);
    return tr;
  }));
}
```

- `textContent`, never `innerHTML`, for any value that came from a file or an
  input: it escapes automatically and closes the injection door.
- `font-variant-numeric: tabular-nums` on any column of figures so they align.
- An empty array renders a designed empty state ("No rows yet. Add one
  above, or load a file."), not a blank table.
- For a long list (thousands of rows), render the visible window and page or
  virtualise; a `file://` page still has one main thread.

## 6. Drawing a chart to scale

For a sparkline or one bar row, hand-drawn SVG is enough and stays inside the
file; for anything richer, load a charting library (`canvas-interactive`,
section 5). Whichever you use, the marks must be true.

- One scale maps data to pixels; every tick and label names a value the chart
  actually reaches. Compute the domain from the data
  (`Math.min`/`Math.max`), do not assume 0 to 100.
- Leave room in the SVG `viewBox` for the outermost labels, so they are not
  clipped.
- Colour chart text and lines from the theme tokens, so the chart is legible
  in both themes; give every drawn shape an explicit fill.
- Label the axes with the subject's real units (the detail the `canvas` skill
  asks for), not bare numbers.

```js
const xs = state.points, max = Math.max(...xs, 1), W = 300, H = 60;
const d = xs.map((v, i) => `${(i / (xs.length - 1)) * W},${H - (v / max) * H}`).join(" ");
spark.innerHTML = `<polyline fill="none" stroke="var(--accent)" stroke-width="2" points="${d}"/>`;
```

(`innerHTML` here is safe: the string is built from numbers the page
computed, never from user text.)

## 7. Check it

- Every `localStorage` read and write is wrapped; the page works with it
  empty.
- The theme choice persists and is set before first paint (no flash).
- Files are read with the File API and parsed inside a try/catch with a
  visible error on failure.
- Saving builds a `blob:` and revokes the URL; export can be re-imported.
- Rows render with `textContent`; figures use tabular numerals; an empty
  array shows a designed empty state.
- Charts are drawn to a scale computed from the data, with labels in real
  units, legible in both themes.
