# embedder.example

## Design Rationale

### Purpose

Embedder is the worked example for the framework's in-process Python integration via
[`github.com/microbus-io/pyvenv`](https://github.com/microbus-io/pyvenv). It shows the full
Go-Python bridge end-to-end: a real sentence-transformers model loaded in a Python venv that
the microservice owns directly, two typed Go endpoints (`Embed`, `Similarity`) that delegate
via `pyvenv.Venv.Call`, and a demo HTML page that exercises both endpoints from a browser.

It exists primarily as documentation and as a smoke test that the manual-subscription pattern
works in practice. It is intentionally NOT bundled in `main/main.go` by default — the guided
tour adds it explicitly so dev environments without Python remain unaffected.

### Why sentence-transformers

The MiniLM all-MiniLM-L6-v2 model is the lightest realistic AI workload that demonstrates the
framework's value proposition: there is no good Go equivalent for sentence embeddings, the
model is ~80MB on disk, runs in milliseconds on CPU, and downloads in seconds on first use.
It exercises pip install (a non-trivial install), Python module-level model loading (loads
on import inside the worker), and JSON-frame call/response (sub-second turnaround) without
requiring a GPU or any external API key.

### Why in-process pyvenv

The microservice owns its Python subprocess the same way it owns its SQL connection (compare
`microbus-io/sequel`). Local pipe, no bus round-trip per call, no envID/callID indirection,
no idle eviction or keep-alive heartbeats — `pyvenv.Venv.Call` returns synchronously and the
operational surface is "a library import." This is the right shape because the relationship
is 1:1 in practice: one upstream replica owns one venv, identical seeding across replicas,
load balancing distributes requests. Bus-level multi-tenancy buys nothing the canonical
pattern uses.

### How the lifecycle works

The flow is:

1. `OnStartup` reads embedded `*.py` sources and `requirements.txt`, constructs a
   `pyvenv.Venv` with `MaxWorkers` and a `LivenessCallback`, and returns. The venv is
   **not** started yet — the demo page surfaces an "Initialize Python VM" button that
   triggers the actual start. This is intentional: it makes the multi-second cost of
   `pip install sentence-transformers` and the model download obvious, and surfaces the
   pip output in the UI's tailed-log pane.
2. `OnStartup` sets `initStatus = "not_started"`.
3. The user opens `/demo`. The page calls `GET /demo/status`, sees `"not_started"`, and
   shows the Initialize button.
4. The user clicks Initialize. `POST /demo/init` flips `initStatus` to `"pending"` and
   launches `svc.venv.Start(ctx)` via `svc.Go`. The endpoint returns immediately.
5. The page polls `GET /demo/status` (long-polled, ETag-driven). Each response includes the
   current status plus the most recent stdout+stderr from the venv (via
   `svc.venv.TailStdOut()` / `TailStdErr()`).
6. When `pyvenv.Venv.Start` finishes successfully — bootstrap, pip install (skipped on
   repeat starts via the requirements marker), Define the embedded sources, worker ready
   — the `LivenessCallback` fires `StateReady`. That handler activates the python-tagged
   subscriptions via `svc.ActivateSubscription` and flips `initStatus` to `"ready"`.
7. On failure (pip install fails, model import fails, ctx expires before ready) `Start`
   returns an error to the goroutine in `DemoInit`, which flips `initStatus` to `"error"`
   with the message. The `LivenessCallback` does **not** fire `StateDied` in this case
   — pyvenv's contract is that StateDied only follows StateReady.
8. If the worker dies post-Ready (subprocess crash), the `LivenessCallback` fires
   `StateDied`. The handler deactivates the python-tagged subscriptions and flips
   `initStatus` to `"error"` so the demo page surfaces the failure.

`Embed` and `Similarity` are subscribed with `sub.Manual()` and `sub.Tag("python")` so they
don't accept traffic until `activatePythonSubs` brings them online from inside the
LivenessCallback. The 503 guard on `!svc.venv.Ready()` inside each handler is defense-in-depth.
The `/demo` web endpoints are untagged and activate normally during startup, so the UI stays
reachable even while the venv is starting or recovering.

`OnShutdown` calls `svc.venv.Close(ctx)`, which kills the subprocess, drains pending calls
with `ErrClosed`, and removes the on-disk venv directory.

### Why the demo page is one HTML file

Same convention as `chatbox.example` and the other tour examples. One self-contained HTML file
with vanilla JS that drives three endpoints: `POST /demo/init` to kick off venv start, `GET
/demo/status` to poll progress and pull tailed logs, and `GET /embed` + `GET /similarity` to
run the action endpoints once the venv is ready. The page hides the action cards behind a
setup card until `status == "ready"`, then swaps them in.

Splitting the page into `setup.html` and `actions.html` templates was considered but the JS
already has to switch between the two states reactively for polling-driven transitions, so a
single-page approach with `.hidden` toggles is simpler than two templates plus client-side
navigation.

### Result handling in Go

`pyvenv.Venv.Call` takes a `result any` argument and runs `json.Unmarshal` against the JSON
returned by the Python function. So `Embed` passes `&embedderapi.EmbedOut{}`, lets pyvenv
unmarshal directly, and returns `out.Vector`. No double-marshal through `map[string]any`
like the previous core-service version. The Python functions still return dicts (`{"vector":
[...]}`, `{"score": float}`) — those map to the `json:"vector"` / `json:"score"` tags on
`EmbedOut` / `SimilarityOut`.

### Testing

`service_test.go` covers the Service-interface mocking pattern only (`TestEmbedder_Mock`
exercises `MockEmbed` and `MockSimilarity`). End-to-end coverage of the Python path lives in
pyvenv's own integration tests, which spawn real Python and exercise pip-install, define,
call, and recovery.

### When not to use as a template

If you are writing a non-AI Python microservice (data-frame transforms, pandas pipelines,
scientific computing), copy the structure of this example but write your own `service.py` and
`requirements.txt`. The pyvenv module is generic; only the Python side is domain-specific.

If you need sub-millisecond latency, pyvenv is not the right primitive — local pipe + JSON
round-trip costs hundreds of microseconds even on the fastest workloads.
