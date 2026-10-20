# Copilot instructions for `shiny_deckgl`

A pure-Python bridge from [Shiny for Python](https://shiny.posit.co/py/) to
[deck.gl](https://deck.gl/) (v9.4.0) + [MapLibre GL JS](https://maplibre.org/)
(v6.11.2), with **no Java dependency**. The Python side builds layer/config
dicts and pushes them to a browser-side JS runtime over Shiny custom messages.
Targeted at marine science / GIS (Baltic Sea, WMS/EMODnet/HELCOM, food-web and
individual-based models).

## Build / test / lint

Source layout is `src/`, so imports resolve only after an editable install or
with `PYTHONPATH=src`.

- Install (editable): `pip install -e ".[dev]"` (extras: `binary` for numpy,
  `geopandas` for GeoDataFrame support).
- Full test suite: `pytest -q` (config: `pyproject.toml [tool.pytest.ini_options]`,
  `testpaths = ["tests"]`).
- Single file / test: `pytest tests/test_views.py -q` or
  `pytest tests/test_basic.py::test_name -q`.
- Type check: `python src/shiny_deckgl/run_mypy.py` (or `mypy src`); config in
  `[tool.mypy]`, `python_version = 3.10`.
- Lint/format: `ruff check .` / `ruff format .` (`line-length = 100`, `py310`).
- Run the demo app: `shiny_deckgl-demo` (entry point → `shiny_deckgl.cli:main`).

On this Windows machine the source-tree tests run via the `shiny` micromamba env:
`$env:PYTHONPATH = "<repo>\src"; micromamba run -n shiny python -m pytest tests\test_views.py -q`.

CI (`.github/workflows/python-package.yml`) runs `pytest -q` + `python -m build`
on Python 3.11–3.13; keep public behavior working across those versions (code
still targets 3.10 syntax).

## Architecture — the big picture

The whole library is a **serialization + messaging contract** between Python and
one JS file. Understanding it requires reading both sides together:

- **`src/shiny_deckgl/map_widget.py`** — the `MapWidget` class (the core, ~2000
  lines). Every server-side method serializes its arguments and calls
  `session.send_custom_message("deck_<action>", payload)` (e.g. `deck_update`,
  `deck_partial_update`, `deck_fly_to`, `deck_add_maplibre_layer`).
- **`src/shiny_deckgl/resources/deckgl-init.js`** — the browser runtime. Each
  `deck_*` message has a matching `Shiny.addCustomMessageHandler("deck_*", ...)`.
  It initializes MapLibre, overlays deck.gl, resolves accessors, and builds layers.
  **A new server method that sends a `deck_*` message needs a matching JS handler,
  and vice-versa** — this is the most common place for breakage.
- **Browser → Python** happens through Shiny inputs. `MapWidget` exposes
  `*_input_id` properties (`click_input_id`, `hover_input_id`,
  `view_state_input_id`, `drawn_features_input_id`, …). Read them in the server as
  `input[widget.click_input_id]()`.
- **Layer/view/widget/control/effect/extension helpers** (`layers.py`, `views.py`,
  `widgets.py`, `controls.py`, `effects.py`, `extensions.py`) are plain factory
  functions that return dicts — no rendering logic. They pass `**kwargs` straight
  through to the corresponding deck.gl/MapLibre class named on the client.

## Conventions and gotchas

- **`@@` accessor convention**: a Python string like `"@@d"`, `"@@d.position"`, or
  `"@@=expr"` is resolved on the client (`resolveAccessors` in the JS) into a JS
  arrow function. `@@=expr` expressions are validated against a safe-pattern
  whitelist before `new Function()` — do not loosen that check.
- **`components.py` is a backward-compat re-export shim only.** The old monolith
  was split into focused modules (`colors`, `layers`, `views`, `widgets`,
  `controls`, `extensions`, `_data_utils`, `_transitions`, `map_widget`). Add new
  symbols to the focused module and re-export from `__init__.py`; keep old
  `from shiny_deckgl.components import X` imports working.
- **`MapWidget` is a single monolithic class** — edit `map_widget.py`. (The old
  `_mixins/` reference copy was removed in 1.11.0: it had drifted and still held
  fixed security bugs.)
- **Version is single-sourced** in `src/shiny_deckgl/_version.py` (read by
  `pyproject.toml` dynamic version and `conda.recipe/meta.yaml`).
- **CDN URLs are single-sourced** in `_cdn.py`; `ui.py::head_includes()` injects
  the pinned scripts plus local `resources/*.js|css`. Keep deck.gl/MapLibre
  versions pinned and consistent between `_cdn.py`, README, and this file.
- **Security-sensitive code**: HTML that reaches the DOM (tooltips, popups,
  markers, `to_html()` export) goes through `sanitizeHtml` / HTML-escaping;
  `tooltip` dicts must contain an `"html"` key (validated, raises `ValueError`).
  Preserve these guards when touching that code.
- **Optional deps are soft**: numpy (`[binary]`) and geopandas (`[geopandas]`) are
  imported lazily/guarded; core must import and run without them.
- **Server methods are `async`** and take `session` first, e.g.
  `await widget.update(session, layers)`, `await widget.fly_to(session, ...)`.
- Tests use `tests/conftest.py::_FakeSession`, which captures
  `send_custom_message(handler, payload)` calls — assert on the emitted `deck_*`
  handler name and payload rather than on a live browser.

## Demo app (the `shiny_deckgl-demo` entry point)

The demo lives at `src/shiny_deckgl/app.py` but is **split into four modules** (v1.4.0+); `app.py` is a thin lazy-construction entry point that re-exports for backward compat. Edit the split modules, not `app.py`:

- `_app_widgets.py` — one `MapWidget` instance per tab (`gallery_widget`, `maplibre_widget`, `events_widget`, `palette_widget`, `adv_widget`, `draw_widget`, `three_d_widget`, `seal_widget`, `widgets_gallery_widget`, …).
- `_app_ui.py` — `build_ui()` assembles the sidebar/tab layout.
- `_app_server.py` — `server(input, output, session)` holds all reactive logic; each tab's `@reactive.Effect` builds layers and calls `await <widget>.update(session, ...)`.
- `_demo_data.py` — cached data factories (ports, routes, MPA GeoJSON, seal trips, fish, bathymetry). Use `@functools.lru_cache` / `random.Random()` instances — **do not** call the global `random.seed()` (thread-safety in cached factories).
- `_demo_css.py` — marine-themed CSS + UI helpers.

Tabs are documented in the `app.py` docstring (deck.gl Layers, MapLibre Controls, Events & Tooltips, Colour Scales, Advanced, Export, Drawing, 3-D Visualisation, Seal IBM, Widgets Gallery, plus an optional HexSim fish tab). When adding a tab, wire all three: a widget in `_app_widgets.py`, UI in `_app_ui.py`, server logic in `_app_server.py`.

The optional **HexSim** demo data is gated behind env vars — set `SHINY_DECKGL_HEXSIM_WORKSPACE` or `SHINY_DECKGL_HEXSIM_ROOT` (`_demo_data.py:2183`); never hard-code local HexSim paths. Tests skip when unset.

## IBM / seal simulation

Two distinct pieces — keep them straight:

- **`ibm.py`** = visualisation + Shiny glue (public API). `SPECIES_COLORS`, `ICON_ATLAS`, `ICON_MAPPING` (9 Baltic species), `format_trips(paths, loop_length=600, ...)` (raw `[lon,lat]` paths → `trips_layer()` dicts with timestamps), and the reusable Shiny module pair `trips_animation_ui()` / `trips_animation_server()` which wires Play/Pause/Reset + speed/trail sliders to `MapWidget.trips_control(session, "resume"|"pause"|"reset")`.
- **`_sealmove.py`** = the movement model itself (private, numpy+pandas required, raises `ImportError` with an install hint if missing). Implements McConnell, Smout & Wu (2017): `simulate_IHTR(IHTRConfig)` (Markov inter-haulout transitions) and the mechanistic `SealIBM(env: Environment, params: IBMParams, n_agents, rng)` with at-sea/haulout states, energy budget, and habitat-gradient-biased movement. `SealIBM.run(T)` returns a tidy DataFrame (`t, agent, x, y, energy, at_sea, haulout_site`), pre-allocating arrays for speed.

The demo bridges them in `_demo_data.py`: `make_seal_trips_ibm()` runs `SealIBM` and `make_seal_trips()` is the simpler synthetic version; `_app_server.py` picks between them via `input.seal_model_type()` and feeds the result through `trips_animation_server`. Simulation state (`x/y` in grid units) is model-space, not lon/lat — conversion to map coordinates happens in the demo-data layer.

## SHYFEM mesh parsers (`parsers.py`)

Parses SHYFEM finite-element `.grd` grids. Two public entry points reading the same internal `_read_grd()`:

- `parse_shyfem_grd(path)` → `list[dict]` for a deck.gl **PolygonLayer**: each element becomes a closed `polygon` (list of `[lon,lat]`) plus `depth`, `element_id`, and a depth-ramped blue `color` `[r,g,b,a]`.
- `parse_shyfem_mesh(path, z_scale=50.0)` → dict of flat geometry arrays (`positions`, `normals`, `colors`, `indices`, `center`, `depth_range`) for a **SimpleMeshLayer**. Positions are **metres relative to the mesh centre**, meant for the `METER_OFFSETS` coordinate system (`coordinateSystem=2`) — pair with `layers.custom_geometry()` (in `layers.py`) to build the layer kwargs.

Gotchas: **coordinate auto-detection** — if node X > 100 000 the mesh is treated as UTM Zone 33N (EPSG:32633) and converted via a lazily-loaded, `lru_cache`d `pyproj` transformer; if pyproj is absent it returns `None` and coords are used as-is. The `.grd` reader is hardened (UTF-8 with replace fallback, bounds checks) — preserve that when editing.

## JS layer-building flow (the Python→browser pipeline)

Understanding how a Python layer dict becomes a rendered deck.gl layer is the single most useful thing for debugging this library. Flow:

1. **Python side** — `layer(type, id, data, **kwargs)` in `layers.py` returns a plain dict. It forcibly sets `type`/`id` last so stray `type=`/`id=` kwargs can't clobber them, serialises `data` via `_serialise_data()` (DataFrame/GeoDataFrame → records/GeoJSON), and normalises `extensions` into `@@extensions` specs (string → name, `[name, opts]` pair → `{"@@extClass", "@@extOpts"}`). Typed helpers (`scatterplot_layer`, etc.) just call `layer()` with sensible defaults.
2. **Transport** — `MapWidget.update()` sends the layer list as a `deck_update` custom message (partial updates go via `deck_partial_update`).
3. **JS side** — `buildDeckLayers(layersData, targetId)` in `resources/deckgl-init.js` maps each dict through, in order: `resolveAccessors` (`@@d`, `@@d.prop`, `@@=expr`), `resolveExtensions` (`@@extensions` → `new deck[Name]()`), `resolveBinaryAttributes`, then handles `@@animate` markers (RAF-driven globals), `@@easing` in transitions, and default pick/hover wiring.
4. **Class resolution** — the layer is instantiated via `deck[layerProps.type] || deck['_' + layerProps.type]` (the `_` prefix covers experimental/underscored deck.gl exports). Unknown types are warned and skipped, not fatal. Same `deck[...]`/`deck['_'+...]` lookup is used for views (`buildViews`), widgets (`buildWidgets`), extensions, and effects (`buildEffects`).

Key implications when adding features:
- A new layer/widget/view/effect type only needs the deck.gl class to exist on the global `deck` object — no JS change is required for a new *type*. But a new **message action** (`deck_*`) always needs a new `Shiny.addCustomMessageHandler`.
- Pickable layers auto-wire `onClick`/`onHover` → `Shiny.setInputValue(targetId + "_click"/"_hover", ...)`; raster types (`RASTER_TYPES`) are excluded. Tooltips read `mapInstances[targetId].tooltipConfig` **live** (not the build-time closure) so `update_tooltip()` takes effect without rebuilding layers.
- `getPosition: "@@d"` expects data items that are `[lon, lat]` arrays; `"@@d.position"` expects dicts. This must match the shape produced by `_serialise_data`.

## Color / palette system (`colors.py`)

deck.gl expects colors as `[R, G, B, A]` int lists — everything here produces that shape. Building blocks:

- **Palettes** are lists of `[R,G,B]` stops (6 each): `PALETTE_VIRIDIS/PLASMA/OCEAN/THERMAL/CHLOROPHYLL` plus 5 ramp palettes (`PALETTE_BLUES/GREENS/REDS/YELLOW_RED/BLUE_WHITE`), with short-name aliases (`VIRIDIS`, `OCEAN_DEPTH`, `BLUES`, …). Default palette everywhere is `PALETTE_VIRIDIS`.
- `color_range(n, palette)` — linearly interpolates the palette into `n` colors `[R,G,B,255]`. This is the primitive the two classifiers build on.
- `color_bins(values, n_bins, palette)` — **equal-width** binning: `idx = int((v-lo)/span * n_bins)`, clamped to `n_bins-1`. (The `n_bins` vs `n_bins-1` factor was a corrected bug — keep the `n_bins` scale.)
- `color_quantiles(values, n_bins, palette)` — **equal-count** binning via sorted breakpoints; each bin holds ~equal numbers of values.
- `depth_color(elevation, max_depth=459.0, alpha=210)` — standalone bathymetric dark-navy↔teal ramp (default max ≈ Baltic Landsort Deep); returns a single `[R,G,B,A]`, not a list.

Convention: color scales are computed **server-side in Python** and passed as pre-computed per-datum colors (e.g. `getFillColor` accessor over a `color` field), rather than relying on client-side color functions — see `docs/performance-patterns.md` for the static/dynamic split. Basemap style URL constants (`CARTO_*`, `OSM_LIBERTY`) also live in this module.

## Where things live

`layers.py` (33 layer helpers) · `map_widget.py` (`MapWidget`) · `colors.py`
(palettes + `color_bins/range/quantiles`) · `parsers.py` (SHYFEM `.grd`/mesh) ·
`ibm.py` + `_sealmove.py` (individual-based-model demo) · `_demo_*` + `app.py`
(demo app) · `docs/` (user manual, api reference, performance patterns).
