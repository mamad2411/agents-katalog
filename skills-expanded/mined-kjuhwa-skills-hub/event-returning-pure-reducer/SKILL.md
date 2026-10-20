---

name: event-returning-pure-reducer
description: State reducer that returns `{state, events, done}` so UI layer renders new state and appends to a log in one pass without the reducer touching DOM.
category: arch
triggers:
  - event returning pure reducer
tags: [arch, event, returning, pure, reducer]
version: 1.0.0
---

# event-returning-pure-reducer

In `18-velvet-cartographers-voyage/app.js`, `step(state, action)` deep-clones with `JSON.parse(JSON.stringify(s))`, mutates the clone, and **also** pushes plain `{k, m}` records into a local `out` array for every side-effect it observes ("storm bites", "pity 14/60", "charted constellation X"). It returns `{state:n, events:out, done:n.fuel<=0}`. The wrapper `apply(action)` then assigns `state=res.state`, iterates `res.events` prepending `<li class={k}>{m}</li>` to the log, calls `render()`, and checks `done`.

This is the useful middle ground between Redux-style pure reducers (which force observers/selectors to diff for user-visible messages) and imperative game loops (which scatter `logMessage()` calls through mutation code). The reducer stays pure-ish — same inputs produce same `{state,events}` — while humans-readable narrative falls out naturally. Multiple events per tick (weather change + movement + frozen-streak warning) all accumulate in one array, preserving their order without timestamps.

Use when your domain produces narrative side-effects worth displaying (turn-based games, workflow engines, simulation ticks). Keep `events` as plain data (`{k:"err"|"ok"|"", m:string}`) not DOM nodes, so the same reducer can be unit-tested headlessly and replayed against different renderers.
