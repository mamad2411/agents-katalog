---
name: ml-web-demo
description: >-
  Wrap a PyTorch ML model in a lightweight FastAPI web demo. Two display modes:
  Canvas bbox overlay or JSON comparison view. VLM API integration, image
  upload (HEIC supported). No Docker, no MySQL, no build tools — pure Python
  + vanilla JS. Includes checkpoint quality verification (multi-head collapse
  detection) before writing any demo code.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [fastapi, pytorch, web-demo, frontend, mlops]
    related_skills: [writing-plans, design-taste-frontend, bash-cli-patterns]
---

# ML Model Web Demo — Skill

## Overview

Take a trained PyTorch model (GNN, CNN, any `nn.Module`) and wrap it in a
working web demo: image upload → model inference → bbox overlay visualization.

The architecture is intentionally minimal — no Docker, no MySQL, no build
tools. Just FastAPI + vanilla HTML/CSS/JS.  Everything starts with a
feasibility verification pass before writing any code.

## Trigger

Use when the user asks to:
- "make a web demo" for a trained model
- "build a frontend" that uploads images and shows predictions
- "create a FastAPI server" wrapping an existing pipeline
- Wrap a PyTorch `InferencePipeline` in API endpoints

Do NOT use for:
- Full production deployment (reach for `docker-production-deployment`)
- Complex multi-page apps with auth/DB/auth (reach for Spring Boot pattern)

## Workflow

### Phase A: Feasibility Verification (run before writing any code)

Skip this phase only if already done in the active session.  The goal is to
surface blockers before the first line of code:

```python
# 1. PyTorch model loading
ckpt = torch.load('checkpoints/best_model.pt', map_location='cpu')
model = YourModel(…)
if 'model' in ckpt:
    model.load_state_dict(ckpt['model'], strict=True)
else:
    model.load_state_dict(ckpt, strict=True)

model.eval()
print(f'Model loaded: {sum(p.numel() for p in model.parameters()):,} params')

# 2. Full forward pass with synthetic data
with torch.no_grad():
    outputs = model(synthetic_data)
for k, v in outputs.items():
    print(f'  {k}: {v.shape}')

# 3. Check critical dependencies
for pkg in ['fastapi', 'uvicorn', 'pillow', 'requests']:
    try:
        __import__(pkg)
        print(f'{pkg}: OK')
    except ImportError:
        print(f'{pkg}: MISSING — pip install {pkg}')
```

**Must verify:**
- Checkpoint loads (handle both raw `state_dict` and wrapped `{'model': sd}`)
- Forward pass works
- Input/output shapes are as expected
- Python path mismatch (conda vs system python — verify with `which python3`)
- Dependencies exist in the same Python that will run the server

**Critical: Verify model head quality, not just shape.**
A forward pass that runs without error does NOT mean the model works.
Test each output head on controlled synthetic inputs and check it produces
*meaningful* scores, not near-constant values:

```python
# Load ALL available checkpoints, test each on the SAME synthetic data
for name, path in [("exp1", "checkpoints/exp1.pt"), ("exp2", ...)]:
    sd = torch.load(path, ...)
    m = Model(...)
    m.load_state_dict(sd if 'model' not in sd else sd['model'])
    m.eval()
    with torch.no_grad():
        out = m(synthetic_data)

    for head in ["existence", "violation", "proposal"]:
        s = out[head].squeeze().tolist()
        spread = max(s) - min(s)
        print(f"{name}/{head}: mean={sum(s)/len(s):.4f} range=[{min(s):.4f},{max(s):.4f}] spread={spread:.4f}")

# Working head → spread > 0.1 (meaningful discrimination).
# Broken head  → spread < 0.01 (near-constant — model is guessing).
# Report both before committing to a demo design.
```

Common failure modes this catches:
- Multi-task training collapsed one head (violation scores all ~0, existence all ~0.5)
- Existence head never saw realistic negatives (all scores ~0.45, no discrimination)
- Dataset mismatch made head outputs useless (trained on synthetic noise, tested on real data)

### Phase B: Build DemoPipeline

Create `api/pipeline.py` with a single class:

```python
class DemoPipeline:
    """Wrap model + preprocessing + postprocessing + overlay rendering."""

    def __init__(self, checkpoint_path, device='cpu'):
        # Load model, create builders, set thresholds
        ...

    def predict(self, img_bytes, **kwargs) -> dict:
        """Full pipeline: preprocess → model inference → postprocess."""
        ...

    def render_overlay(self, img_bytes, predictions) -> bytes:
        """Draw bboxes on image. Returns PNG bytes."""
        ...

    def health(self) -> dict:
        return {'status': 'ok', 'params': N}
```

**Key decisions:**
- If the model does NOT need visual features (element_dim=5), skip timm/DINOv2
- Set violation/existence thresholds from known validation data, not defaults
- Handle both pixel-coord and normalized bbox inputs

### Phase C: FastAPI Routes

Create `api/main.py`:

```python
from pathlib import Path
from dotenv import load_dotenv

# Load .env at startup — API keys from env, not user input
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

app = FastAPI(title='GUI-GNN Demo')
app.add_middleware(CORSMiddleware, allow_origins=['*'], …)

# Lazy-init avoids import-time GPU init
_pipeline = None
def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = DemoPipeline()
    return _pipeline

@app.get('/api/health')
@app.post('/api/predict')   # Full: upload → API → model → overlay
@app.post('/api/gnn-only') # Skip external API, use provided JSON
@app.get('/')              # Serve frontend index.html
```

**Important patterns:**

1. **Lazy pipeline init** — avoids GPU init at import time; critical for fast dev reload cycles
2. **No StaticFiles mount at root** — use a simple `@app.get('/')` route that reads and returns `index.html` as `HTMLResponse`. Mount at root intercepts all API routes.
3. **GNN-only endpoint** — provide a secondary endpoint that takes pre-computed predictions as JSON, so users can test the model without paying for external API calls
4. **Return overlay as base64 data URL** — the frontend renders it immediately; no need for server-side file storage
5. **Load API key from env var via python-dotenv** — add `load_dotenv()` at app startup so the key is read from `.env`. Never require the user to type the key in the frontend.

### Phase D: Frontend — Choose Display Mode

Users have different needs for results display. Ask or observe which mode they want:

- **Mode A: Canvas bbox overlay** (default — spatial/visual inspection)
  Shows the image with bounding boxes drawn directly on canvas.
- **Mode B: JSON comparison view** (data inspection)
  Shows raw VLM JSON vs GNN-corrected JSON side-by-side. Good for debugging
  or data analysis. Trigger phrases: "看原始json和新json的对比", "show json".

Create `web/index.html` — a single-page app with one of the two layouts:

**Layout (Mode A — canvas overlay):**
```
┌─────────────────────────────────────────────────────┐
│  Config bar: VLM model select (API key from env)    │
├─────────────────────────────────────────────────────┤
│  Upload zone: drag/drop or click to select image    │
├─────────────────────┬───────────────────────────────┤
│  Before (VLM only)  │  After (VLM + GNN proposals)  │
│  Red bboxes         │  Red VLM + Blue dashed GNN    │
└─────────────────────┴───────────────────────────────┘
│  Stats: VLM count, constraints, violations, proposals│
└─────────────────────────────────────────────────────┘
```

**PREFERRED (user-mandated): screenshot and overlay are SEPARATE canvases.**
Do NOT draw boxes on top of the screenshot. The user explicitly rejected
that ("你不要直接在截图上画框 你在截图旁边再开一个矩形 在上面画框").
Each panel holds TWO same-sized canvases side by side: a clean screenshot
canvas + a dark-bg overlay canvas ("检测框") next to it, with a small label
above each. See Pitfall 30 for the exact 4-canvas pattern (HTML/CSS/JS).

**Layout (Mode B — JSON comparison):**
```
┌─────────────────────────────────────────────────────┐
│  Config bar: VLM model select (API key from env)    │
├─────────────────────────────────────────────────────┤
│  Upload zone                                          │
├──────────────────────┬──────────────────────────────┤
│  VLM Detection (raw) │  GNN Corrected                │
│  (dark code panel)   │  (dark code panel)            │
│                      │  VLM items + existence_score  │
└──────────────────────┴──────────────────────────────┘
│  Stats: VLM count, constraints, violations, proposals│
└─────────────────────────────────────────────────────┘
```

- **Mode C: multi-tab capability demo** (when end-to-end is weak but
  synthetic-benchmark capabilities are strong — the "honest demo" per
  Pitfalls 31–32). Three tabs: 端到端案例 (hero cases) / 置信度打分 /
  结构补全 (capability-validation panels). Tab switch toggles
  `.tab-btn.active` + `.tab-panel.active`; each panel lazy-loads on first
  activation via a `dataset.loaded` guard. Charts are hand-drawn on a
  `<canvas>` (grid + axes + legend + per-run scatter dots + mean line) —
  no chart library. Honest annotations are part of the layout, not an
  afterthought: amber `cap-note` at top stating the synthetic condition
  (what was injected), muted `cap-note` at bottom with the real-data
  comparison (e.g. "真实数据 AUROC ≈ 0.60"). Full HTML/CSS/JS pattern in
  `references/capability-tab-frontend.md`.

**Technical choices:**
- **No frameworks** — pure HTML + CSS + JS (Flexbox layout)
- **Canvas overlay** — draw on a SEPARATE `<canvas>` beside the clean
  screenshot canvas (user-mandated; see Pitfall 30). NOT on top of the image
- **Native drag/drop** — `dragenter/dragover/drop` events, no libraries
- **API key from env var** — never require manual key input in frontend unless explicitly asked. Load via `load_dotenv()` in the backend, not localStorage
- **Inline everything** — CSS in `<style>`, JS in `<script>`, no CDN deps
- **Responsive** — 2-column on desktop, 1-column on mobile (`@media max-width: 720px`)

**JSON rendering pattern (Mode B):**
```javascript
// Dark code panel with monospace font
.json-pane { background: #1e1e2e; border-radius: 10px; }
.json-pane pre { margin: 0; padding: 14px; overflow: auto;
  max-height: 500px; font-size: 0.78em; color: #cdd6f4; }

// Render: JSON.stringify(obj, null, 2)
vlmJson.textContent = JSON.stringify(data.vlm?.elements || [], null, 2);
correctedJson.textContent = JSON.stringify(corrected.elements || [], null, 2);
```

**Backend: build `corrected_json` in the pipeline class:**
```python
def build_corrected_json(self, vlm_elements, gnn_result):
    corrected = []
    # Annotate VLM elements with GNN existence scores
    for i, elem in enumerate(vlm_elements):
        corrected.append({
            "bbox": elem.get("bbox_xyxy") or elem.get("bbox", []),
            "label": elem.get("label", "unknown"),
            "source": "vlm",
            "existence_score": existence_scores[i],
        })
    # NOTE: GNN element-proposal head outputs are deliberately excluded
    # from corrected_json. They are research artifacts from masked-element
    # experiments — on real VLM output they produce giant nonsense bboxes
    # that clutter the display (see Pitfall 12). Existence scores on VLM
    # items are the only useful GNN signal for a demo.
    return {"elements": corrected, "vlm_count": len(vlm_elements)}
```

Include `corrected_json` in the API response alongside `overlay_b64` and
`image_b64`. The frontend can then choose which to display without a second
API call.

**Canvas drawing pattern (Mode A):**
```javascript
// VLM bboxes (red solid)
ctx.strokeStyle = 'rgba(255, 50, 50, 0.85)';
ctx.lineWidth = 2;
ctx.strokeRect(x1, y1, w, h);
ctx.fillStyle = 'rgba(255, 50, 50, 0.15)';
ctx.fillRect(x1, y1, w, h);

// GNN proposals (blue dashed)
ctx.setLineDash([6, 4]);
ctx.strokeStyle = 'rgba(50, 130, 255, 0.9)';
ctx.strokeRect(x1, y1, w, h);
ctx.setLineDash([]);
```

### Phase E: Integration

The server serves both API and frontend:

```bash
# Start (with correct Python)
/usr/local/bin/python3 api/main.py
# → Uvicorn running on http://0.0.0.0:8765
```

**Verify with curl:**
```bash
curl http://localhost:8765/api/health
curl http://localhost:8765/ | head -5
curl -X POST http://localhost:8765/api/gnn-only \
  -F "file=@test.png" \
  -F 'vlm_json=[{"bbox": [10,20,100,50], "label": "button"}]'
```

## Pitfalls

0. **CRITICAL: Never substitute the user's chosen model without asking.**
   When a user names a specific model (e.g. "Florence-2-base"), use THAT
   model. If it fails due to version incompatibility, missing dependency, or
   config error:
   1. Diagnose the exact error from the traceback
   2. Fix the problem for the requested model (patch cached config files,
      pin transformers version, install missing deps)
   3. Only if fixing is impossible after multiple attempts, report the
      blocking error and ASK before trying alternatives
   Users who specify a model by name have a reason. Substituting without
   permission erodes trust. See `references/hf-model-compat-patching.md`
   for common HuggingFace compatibility fixes.

1. **Python path mismatch.** The `python3` on PATH may be conda's base env (no
   packages). Use `/usr/local/bin/python3` or check with `which python3 && python3 -c 'import fastapi'` before starting the server.
   Background shells (`terminal(background=true)`) may NOT inherit the
   interactive env's PATH — a foreground `python3 main.py` that imports
   fastapi fine can die with `ModuleNotFoundError` when launched in the
   background. For background servers, pass the absolute interpreter path:
   `/opt/homebrew/.../bin/python3 api/main.py`.

2. **StaticFile mount at `/` intercepts API routes.** FastAPI processes mount
   *after* the parent app's routes. A `StaticFiles(directory='web/')` mounted
   at `/` will catch `/api/health` and return 404. Use a simple `@app.get('/')`
   route that reads and returns `index.html` as `HTMLResponse`.

3. **Existence/threshold models trained on dataset A won't transfer to dataset
   B.** On the web demo, set thresholds low (~0.3) and display raw scores
   rather than hard-filtering. Label proposals as "experimental."

4. **Checkpoint format varies.** Some are raw state_dict, some have
   `{'model': sd, 'val_loss': ...}`, some have `{'model_state_dict': sd}`.
   Always print the keys and handle both patterns.

5. **VLM API latency.** Calls take 2–5s. Show a loader spinner + status text
   update ("Running VLM detection..." → "Waiting for API response..." →
   "Rendering overlay...") so the user knows progress is happening.

6. **Don't use `background=true` for pip install** — the tool detects it as a
   long-running process and blocks. Pre-check with `python3 -c 'import pkg'`.

7. **HEIC/HEIF uploads fail silently or canvas stays blank.**
   macOS/iOS screenshots are often HEIC, creating two problems:

   **a) Backend PIL can't open HEIC.** Install `pillow-heif`
   (`pip install pillow-heif`) and add to `api/main.py`:
   ```python
   import pillow_heif
   pillow_heif.register_heif_opener()  # explicit call required by v1.4+
   ```
   Add `pillow-heif>=0.21.0` to `api/requirements.txt`. For portability,
   wrap the import+register in try/except so the server still starts on
   machines without the package (HEIC uploads just return a 400 from PIL):
   ```python
   try:
       import pillow_heif
       pillow_heif.register_heif_opener()
   except ImportError:
       logger.warning("pillow_heif not installed — HEIC/HEIF unsupported")
   ```

   **b) Frontend canvas can't render HEIC blob URLs.**
   Even after PIL decodes HEIC on the server, `URL.createObjectURL(file)`
   creates a HEIC blob URL that the browser may not render on `<canvas>`
   via `ctx.drawImage()`. The canvas stays blank with no error message.
   Fix: have the backend convert the source image to JPEG base64 and return
   it alongside the overlay:
   ```python
   # In the API response
   jpeg_buf = BytesIO()
   pil_img.convert("RGB").save(jpeg_buf, format="JPEG", quality=85)
   image_b64 = base64.b64encode(jpeg_buf.getvalue()).decode("utf-8")
   response["image_b64"] = f"data:image/jpeg;base64,{image_b64}"
   ```
   The frontend draws from `data.image_b64` instead of `state.imageUrl`:
   ```javascript
   const srcImg = new Image();
   srcImg.onload = () => drawCanvas(canvas, srcImg, ...);
   srcImg.src = data.image_b64;  // JPEG base64, always canvas-safe
   ```

8. **Canvas resize on window resize.** Debounce the resize handler (300ms) and
   re-render both canvases from cached state.

9. **Never require API key input in the frontend.** Users won't retype a key
   every session. Use `load_dotenv()` + `DASHSCOPE_API_KEY` env var instead.
   The API route should read the key from `os.environ` — no `api_key` form
   parameter at all. Remove any localStorage persistence for API keys.

10. **JSON comparison mode requires corrected_json in the response.**
    The overlay-only response (`vlm.elements` + `overlay_b64`) is insufficient
    for the JSON view. Add a `corrected_json` field that annotates VLM elements
    with GNN scores. The response should carry both `overlay_b64` and
    `corrected_json` so the frontend can switch modes without a second API call.

11. **User may switch from visual to JSON view mid-session.**
    Don't hardcode one display mode into the frontend. Build the API response
    to support both from the start: return `overlay_b64` + `corrected_json` +
    `image_b64`. The frontend renders whichever mode fits the current need.

12. **GNN element-proposal outputs can be noise OR gold — verify loading first.**
    With a checkpoint whose architecture does NOT match the model (Pitfall 15),
    the proposal head produces structurally meaningless boxes (spanning
    near-full-image height) and the correct conclusion is "proposals are noise".
    With a correctly-loaded joint-trained checkpoint, proposals land precisely
    on VLM-missed elements (weather forecast rows, settings toggles) and are the
    MOST compelling demo feature (blue boxes filling red-X gaps). The earlier
    "proposals are noise" observation was itself an artifact of the broken
    loading. Do NOT pre-judge the proposal head — verify checkpoint loading,
    then inspect rendered overlays on real images before deciding whether
    proposals enter the demo.

13. **Multi-task training can collapse one head.**
    When a model has multiple prediction heads (violation + proposal + existence
    + coordinate) trained jointly, one head can silently collapse to near-constant
    output while others work. The model loads and forward-passes without error,
    but one head produces useless scores. Verify all heads independently:
    - Check mean and spread (max-min) for each head's output
    - Compare against a single-head-trained checkpoint if available
    - A collapsed head: spread < 0.01, all values ~0.5 (sigmoid saturation) or ~0

14. **Be upfront about model limitations in the demo.**
    If the model's existence/existence head doesn't discriminate on real data
    (all scores ~0.45), do not build UI that pretends it works. Choices:
    - Show raw scores with no visual encoding (no green/red coloring)
    - Add an honest note: "this head was trained on synthetic data and does
      not transfer to real inputs"
    - Remove the broken head's output from the demo entirely
    - Switch display mode (e.g., visual overlay → JSON comparison) when the
      spatial output is misleading
    Users will trust a demo that admits its limitations over one that
    confidently displays garbage.

15. **Checkpoint architecture mismatch → silent garbage results.**
    `load_state_dict(strict=False)` does NOT error on shape mismatch — it
    silently SKIPS mismatched keys and keeps random init. Loading a
    hidden_dim=16 checkpoint into a hidden_dim=128 model leaves 89% of
    weights random; the model forward-passes fine and produces scores that
    look meaningful (violation ~0.43 constant, proposals that mostly get
    filtered out). Any evaluation done with that model is meaningless — in
    the bipartite-gnn project this invalidated a documented "+2.9pp F1"
    result. ALWAYS count matched keys before trusting anything:
    ```python
    sd = torch.load(path, map_location='cpu')
    ms = model.state_dict()
    filtered = {k: v for k, v in sd.items() if k in ms and v.shape == ms[k].shape}
    print(f"Loaded {len(filtered)}/{len(sd)} keys")   # <100% → results suspect
    model.load_state_dict(filtered, strict=False)
    ```
    Quick probe of the checkpoint's real architecture:
    ```python
    hd = sd['encoder.e_to_c_convs.0.lin_l.weight'].shape[0]  # reveals hidden_dim
    ```
    If key count < 100%, re-train or find the right checkpoint — do NOT
    proceed with the demo.

16. **Single-head-trained checkpoints have untrained other heads.**
    A checkpoint named `*_violation_only` (or proposal-only / existence-only)
    only backpropagated one head — every other head is random init. On real
    data this shows up as: proposal boxes with x2<=x1 (filtered out → zero
    proposals), existence ~0.45 constant, violation ~0.43 constant. Test
    EVERY head the demo will display, not just the one the filename claims.

17. **Feature-dim mismatch is the same bug as hidden_dim mismatch.**
    A visual-fusion checkpoint expects 197-d element features (5 struct +
    192 ViT); feeding 5-d structure-only silently drops `element_proj` → the
    input layer is random → fake demo results. Either precompute/load the
    visual features (`builder.build(elems, constraints, visual_features=feats)`)
    or pick the matching non-visual checkpoint.

18. **Curate hero cases BEFORE building the demo UI.**
    Aggregate metrics can be weak (+1pp F1 across 200 images) while specific
    images show dramatic, verifiable improvement (TP +11 / FP +0, F1
    +0.15–0.26) — and some images get WORSE. Never demo random uploads as the
    primary path. Instead:
    1. Run the real pipeline over the full eval set with the verified checkpoint
    2. Rank by ΔTP ≥ threshold AND ΔFP small (cost of proposals)
    3. Generate before/after overlay images and visually inspect them
       (blue proposal boxes must land on real elements, not random spots)
    4. Ship 10–15 verified hero cases as the default demo flow; random upload
       becomes an optional secondary mode with an honest "效果因图而异" note
    Show the aggregate stats alongside the hero cases so the demo is honest
    about the average, not just the best.

19. **Verify the docs' numbers against the checkpoint before quoting them.**
    TASK.md / README experiment tables can be stale or produced by a broken
    loading path. Before writing a strategy doc or demo copy that cites a
    metric (F1 gain, AUROC), re-run the eval with the shape-filtered loading
    from Pitfall 15 and confirm the number reproduces. 试清楚 — run the
    pipeline, look at actual outputs, then write the plan.

20. **Sweep the threshold before fixing it in the demo.**
    Demo thresholds must come from a sweep over the real eval set, not from
    training-time defaults (0.3/0.5 flood FPs). On the bipartite-gnn joint
    model, sweeping violation threshold 0.30→0.90 over 200 real VLM images:
    F1 gain stayed ~+0.5–1.0pp at EVERY threshold, but the FP cost per TP
    improved from 1:5 (thresh 0.30) to 1:3.3 (thresh 0.75) — higher threshold
    = same gain, fewer garbage proposals. Sweep script pattern:
    ```python
    for thresh in [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90]:
        run full eval; record ΔTP, ΔFP, ΔF1, n_proposals
    # pick: best ΔF1 with acceptable ΔFP/ΔTP ratio; report the table
    ```
    Then use that threshold in `DemoPipeline.__init__` AND in the hero-case
    prep script so demo numbers match the eval numbers.

21. **Rebuild via parallel subagents: contract-first, non-overlapping files.**
    For a demo rebuild (backend + data prep + frontend), dispatch 3 parallel
    `delegate_task` subagents, one per non-overlapping file group, instead of
    one agent doing everything serially:
    - A: `api/pipeline.py` + `api/main.py` (backend: checkpoint fix + API)
    - B: `scripts/prepare_demo_cases.py` (data prep, writes `demo_data/`)
    - C: `web/index.html` (frontend rewrite)
    The shared spec is the strategy doc + review-plan doc you wrote first
    (see `references/demo-rebuild-orchestration.md` for the full recipe:
    API contract, per-agent prompts, verification commands). Requirements:
    - Every agent's prompt must be SELF-CONTAINED (no conversation memory):
      absolute paths, checkpoint facts, threshold, API contract, doc sections
      to follow, exact verify commands to run, report in Chinese.
    - Give each agent the verified facts (which checkpoint is trustworthy,
      which are broken) so they don't re-discover or contradict them.
    - File groups must not overlap; agents run in parallel and never touch
      the same file.
    - The backend agent also fixes packaging (`pyproject.toml` demo extra,
      `.gitignore` generated dirs like `demo_data/`) — small edits the
      orchestrator can also do itself while waiting.
    - After the batch returns, VERIFY every claim yourself (read the files,
      run the commands) — subagent summaries are self-reports.

22. **Hardened checkpoint loader: fail loudly, don't just count keys.**
    Beyond Pitfall 15's probe, ship a production `_safe_load_state()` in the
    pipeline so a wrong checkpoint can never silently degrade the demo:
    - `_detect_hidden_dim(path)`: read `encoder.element_proj.weight`
      shape[0] (fallback `encoder.e_to_c_convs.0.lin_l.weight`) → build the
      model with the checkpoint's REAL hidden_dim (compat hd=16/128).
    - Shape-filter as in Pitfall 15, THEN enforce: matched keys ≥ 30 (floor)
      AND every critical layer present (`encoder.element_proj.weight`,
      `violation_head.network.3.weight`, `proposal_head.network.3.weight`).
      Raise `RuntimeError` on either failure — a wrong checkpoint must kill
      startup, not produce fake proposals.
    - Handle all wrap formats in one loader: raw sd, `{'model': sd}`,
      `{'state_dict': sd}`, and `model.`-prefixed keys (strip prefix).
    Verified working code + real test transcript (44/44 keys, hd=128,
    220439 params; hd=16 ckpt loads; visual-fusion ckpt raises) in
    `references/checkpoint-loading-recipe.md`.

23. **Verify head output FORMAT from the head source — xywh vs xyxy kills.**
    A bbox head may emit center-xywh OR post-sigmoid `[x1,y1,x2,y2]`; with
    per-coordinate sigmoids, x1>x2 / y1>y2 happens routinely. In this
    project the pipeline wrongly passed the head's already-xyxy output
    through `_xywh_to_xyxy`, silently corrupting every proposal. Rules:
    - Read the head's `forward()` before writing the post-processor; never
      assume the bbox format.
    - Always filter invalid boxes at proposal-build time:
      `bbox = [clamp(v) for v in raw]; if bbox[2] <= bbox[0] or bbox[3] <= bbox[1]: continue`.
    - To test the filter when real data won't trigger the violation path,
      monkeypatch `model.forward` to emit fabricated outputs (one invalid
      bbox, one valid, one below threshold) and assert only the valid one
      survives — script in the reference file.

24. **API-contract hygiene when reshaping demo endpoints.**
    - When aligning a response to a new schema (e.g. hero-case JSON), keep
      the old fields (`vlm`, `gnn`, `corrected_json`) alongside — the old
      frontend keeps working until it's rewritten.
    - Removing a `Form` param is safe: FastAPI silently ignores undeclared
      form fields, so a stale frontend still posting `vlm_model` doesn't break.
    - Drop `image_b64` from responses once the frontend renders the
      locally-selected file (`URL.createObjectURL`) — no 2MB payload for
      nothing. (Supersedes Pitfall 7b's server-conversion for such
      frontends; keep 7b's JPEG conversion only if the browser can't decode
      the local HEIC blob.)
    - Pre-computed demo data must degrade gracefully: missing `cases.json`
      → `/api/cases` returns `[]` (200, never 500); unknown id → 404 with a
      message; screenshots fall back through candidate extensions
      (`.jpg`/`.png`/`.jpeg`) and honor the case's `screenshot` field.
    - Optional image-codec deps (pillow-heif): wrap import in try/except so
      the server starts without them (see Pitfall 7).

25. **VLM API coordinate baseline ≠ recorded image size — verify before normalizing.**
    Some VLM APIs (qwen3-vl-flash confirmed) return bbox coords in a FIXED
    internal frame (1080×960) regardless of the input image size, while the
    generation script records the ORIGINAL image size (1080×1920) in
    `image_width`/`image_height`. Normalizing with the recorded size halves
    all y coords → every box sits in the top half of the screen, user sees
    "红框没拉伸充满截图，相对位置对但整体偏小". Detection is NOT the
    problem — the coordinate frame is. Diagnose numerically, never by eye:
    ```python
    # For every prediction file, compare coord maxima against claimed dims
    for f in glob('data/vlm_predictions/**/*.json'):
        d = json.load(open(f)); xs, ys = [], []
        for e in d['elements']:
            b = e.get('bbox_xyxy') or e.get('bbox') or e.get('bbox_2d')
            if b and len(b)==4: xs.append(b[2]); ys.append(b[3])
        print(f, 'x_max', max(xs), 'y_max', max(ys),
              'x/claimed_w', max(xs)/d['image_width'],
              'y/claimed_h', max(ys)/d['image_height'])
    # All files y_max ≈ 960 while claimed_h = 1920 → baseline is 1080×960
    ```
    Confirm with a live API call on a differently-sized input: if a 540×960
    image returns x_max≈974 (> 540), the frame is fixed at 1080 wide, not the
    input width. Fix: normalize by the VLM frame constant
    (`VLM_COORD_W=1080, VLM_COORD_H=960`) in EVERY consumer — pipeline,
    API response normalizer, hero-case prep script, visualization script —
    and ignore the JSON's recorded size. After the fix, re-run hero-case
    selection: previously "verified" cases can drop (12→6) because some TPs
    were fake matches from a loose threshold (0.1 = 192px) on misaligned boxes.

26. **User-reported visual bug → ask first, then read the coordinate code.**
    When the user says boxes don't match elements, do NOT spiral into
    vision-analyze loops or repeated API experiments. The user's first two
    corrections in a row were: "直接去读代码就好了啊" (just read the code)
    and "为什么不问我呢" (why didn't you ask me). Correct order:
    1. ASK where they see it (web page vs static overlay image vs upload
       mode) and HOW it looks (all cases? one direction? size wrong?) — a
       one-line `clarify` beats ten screenshots.
    2. READ the coordinate pipeline end-to-end: raw VLM JSON → normalization
       → storage → frontend mapBBox/canvas transform. Verify the numeric
       chain (raw px → normalized → back to px) with a script.
    3. Only then run a decisive probe (A/B render of two candidate
       baselines, or a live API call) to pick between remaining hypotheses.
    Data-link correctness ("numbers round-trip") is NOT the same as visual
    correctness — the bug can live in the data source (wrong baseline) while
    every conversion step is lossless.

27. **Color every proposal by its GT-match status, or the demo reads as noise.**
    If the frontend draws all GNN proposals in one color (e.g. uniform blue
    dashed), the user cannot tell recovered elements from false positives —
    real feedback: "蓝色框的逻辑很混乱，不知道在干什么". The hero-case prep
    script must annotate each proposal with whether it matches GT, and emit
    derived arrays for the frontend:
    ```python
    proposal_list.append({"bbox": ..., "violation_score": ...,
                          "matched": matched})   # matched = any(center_distance(p.bbox, ge.bbox) <= 0.1 for ge in gt_elems)
    gt_matches = [p["bbox"] for p in proposal_list if p["matched"]]  # green = GNN recovered
    missed     = [gt_elems[j].bbox for j in fn_b]                    # red X = VLM missed (left pane)
    ```
    Legend then reads: red solid = VLM detection, green solid = GNN recovered
    (proposal matched GT), blue dashed = GNN proposal unmatched (honest FP).
    Trap: the `after` Hungarian's matched-GT indices include VLM's own TPs —
    for `gt_matches` use only the MATCHED PROPOSALS (the `matched` flag), not
    all after-TPs, or green boxes outnumber blue and the "recovered" story
    blurs. The `missed` list can be large (46/72 GT) — that IS the honest
    "VLM missed most elements" story; keep red X marks on the left pane only.

28. **Green/GT boxes must use the GT element's real bbox — never the
    proposal's predicted bbox.** Drawing `gt_matches` from the proposal bbox
    puts the green box at the GNN's noisy prediction (MSE ~0.05–0.08), which
    reads as "绿框错位了" even though every coordinate step is lossless.
    Match each matched proposal to its nearest GT element and emit THAT bbox:
    ```python
    gt_matches = []
    for p in proposals:
        if not any(center_distance(p.bbox, ge.bbox) <= 0.1 for ge in gt_elems):
            continue
        best = min(gt_elems, key=lambda ge: center_distance(p.bbox, ge.bbox))
        gt_matches.append([r4(v) for v in best.bbox])
    ```

29. **GT/screenshot aspect-ratio mismatch misaligns every GT box — filter the
    data, not the frontend.** RICO view-hierarchy resolution can differ from
    the screenshot in RATIO, not just scale (10005: GT 1440×2392 ratio 0.602
    vs screenshot 1080×1920 ratio 0.5625). GT normalized coords are relative
    to the hierarchy's own dims, so mapping onto the screenshot displaces
    every box (buttons half-covered, boxes in empty space) with zero frontend
    bugs. Diagnose by comparing ratios numerically, never by eye:
    ```python
    parsed = parse_rico_vh(gt_path); rw, rh = parsed["width"], parsed["height"]
    shot_w, shot_h = Image.open(jpg).size
    if abs(rw / rh - shot_w / shot_h) > 1e-3:  # GT coords unusable vs this shot
        skip_this_image()
    ```
    Add this filter in the hero-case prep loop; fallout: evaluated 200→128,
    cases 6→5. Most RICO files are 1440×2560 vs 1080×1920 (both 9:16, fine);
    watch for 1440×2392 / 1440×1281 outliers.

30. **NEVER draw boxes on top of the screenshot — separate overlay canvas
    (user-mandated).** After the coordinate bugs were fixed, the user still
    rejected the layout: "你不要直接在截图上画框 你在截图旁边再开一个矩形
    在上面画框" — boxes on the image occlude the UI you're trying to inspect.
    The final layout has FOUR canvases, two per panel, all sized identically
    by the same `sizeCanvases()` (contain-fit on the screenshot aspect):
    ```
    ┌─ Panel "VLM 检测" ────────────┐
    │ 截图 (clean)  │ 检测框 (dark bg) │
    │ canvasLeft    │ canvasLeftOv    │
    └───────────────┴─────────────────┘
    ┌─ Panel "VLM + GNN" ──────────┐
    │ canvasRight  │ canvasRightOv   │
    └───────────────┴─────────────────┘
    ```
    Implementation essentials:
    - HTML: each `.cv-col` = label (`截图` / `检测框`) + `<canvas>`; overlay
      canvases carry `class="ov"`.
    - CSS: `.canvas-box { display:flex; gap:14px; justify-content:center; }`
      and `.canvas-box canvas.ov { background:#1c1f33; }` (dark bg so colored
      boxes read clearly; the screenshot canvas keeps the image itself).
    - JS: `sizeCanvases()` calls `setupCanvas` on ALL FOUR with the same
      cssW/cssH (from contain-fit on the screenshot), so the same normalized
      bbox → `mapBBox(bbox, T)` transform maps to all canvases identically.
    - `drawLeft()`: screenshot → `ctxLeft` (clean `drawImageFit`), then ALL
      boxes (VLM red + red-X missed) → `ctxLeftOv` after filling its bg
      `#1c1f33`. `drawRight()` same split: clean image on `ctxRight`, red +
      green + blue-dashed on `ctxRightOv`. The image canvas gets NO strokes.
    - Keep `getTransform()` keyed off the screenshot canvas dims; since all
      four share cssW/cssH this stays consistent.
    - `drawOverlayText`/empty-state hints go on the overlay canvas, not the
      image. Verify with `node --check` on the extracted script + browser
      screenshot: image canvases must show zero colored strokes.

31. **Headline metrics from synthetic benchmarks can collapse on real data —
    re-verify BEFORE shaping the demo around them.** The report's flashiest
    numbers are often measured under synthetic conditions and may not survive
    real end-to-end data. In bipartite-gnn the user (correctly) said "端到端
    反而做得不好，你应该展示置信度打分和结构补全" — but re-measuring on real
    VLM data (200 RICO images, 2918 elements, real GT) showed BOTH collapse:
    - **Confidence scoring**: reported AUROC 0.989 (random-imposter synthetic
      test) → joint existence head **0.489** (≈random), dedicated
      confidence_scoring model **0.603** on real data. Real VLM false
      positives look like genuine elements; only randomly-placed imposters
      are structurally separable.
    - **Structure completion**: reported GNN IoU 0.123 vs NN 0.088 (+40–56%,
      synthetic element-dropping) → on real misses GNN proposals mean IoU
      **0.198 vs NN baseline 0.212** (GNN NOT better). Dropped-element
      reconstruction has an interpolation shortcut that real VLM misses lack.
    Rules:
    - Before building ANY demo UI around a reported metric, re-run the
      measurement on REAL end-to-end data (real predictions + real GT), not
      the synthetic eval it was reported on. One AUROC/IoU script beats an
      hour of demo design.
    - Synthetic-benchmark numbers remain valid as METHOD validation — in the
      demo label them explicitly (what was injected, what conditions), never
      present them as end-to-end effect.
    - When the user cites "we have good results in X and Y, showcase those":
      re-verify first; if the data contradicts the report, bring the
      re-verification table (synthetic vs real AUROC, GNN-vs-NN IoU) to the
      user immediately — this user's zero-tolerance-for-fabrication stance
      means real numbers up front beat either building a fake showcase or a
      bare refusal. Then the honest ranking decides what the demo shows.
    Full re-verification recipe + numbers in
    `references/synthetic-vs-real-metric-collapse.md`.

32. **Honest-demo asset traps: biased sigmoid thresholds and unpersisted
    benchmark weights.** When building the "capability validation" panels that
    replace the fake end-to-end showcase (Pitfall 31), two traps recur:
    - **Biased sigmoid → 0.5 threshold labels everything real.** The
      dedicated confidence model scored real elements mean 0.693 vs imposters
      0.543 — but EVERY score was > 0.5, so `score > 0.5` gave tn=0 fn=0
      (acc 0.667, looks broken) while AUROC was 0.984–0.999 (ordering fine).
      Never classify a sigmoid head with a fixed 0.5 cutoff: compute the
      per-image optimal threshold via Youden's J (maximize TPR−FPR over a
      grid) and report AUROC + that threshold. thr=0.55 → acc 0.944–0.990.
    - **Benchmark JSON exists but model weights were never persisted → no
      single-image demo.** `completion_results.json` came from per-run
      training inside the eval script; the checkpoint on disk is a different
      artifact (mask-task, no proposal head). Substituting the joint
      checkpoint for a single-image drop demo is actively misleading: GNN
      IoU 0.000 vs NN 0.411 (opposite direction from the real eval). Show
      the aggregate curve from the results JSON only; never fake a
      single-image demo with a different checkpoint.
    - **Show ALL benchmark runs, including the negatives.** The completion
      curve is honest AND interesting when every drop ratio is shown: GNN
      loses at drop 0.2/0.4 (−17%/−28%) and wins at 0.6/0.8 (+39%/+57%) —
      the real claim is "GNN's structural prior only pays off when the
      layout is severely depleted". Cherry-picking the good ratios would
      have reproduced the original deception.
    Full recipe + numbers in `references/honest-demo-assets.md`.

33. **Browser caches the old index.html — user reports "没看到新界面" while
    the server is serving the new code.** FastAPI's plain `HTMLResponse`
    sends NO cache-control headers, so after any frontend change the browser
    may keep showing the stale page (no tabs, old layout, "界面有区别吗" /
    "没看到tab"). This is the FIRST suspect when the user says they don't
    see your changes and your own browser session (fresh context) shows them
    fine. Fix in the `/` route — never debug frontend-cache symptoms as
    code bugs:
    ```python
    @app.get("/", response_class=HTMLResponse)
    async def index():
        html = index_path.read_text()
        return HTMLResponse(html, headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        })
    ```
    Debug order for "user doesn't see the change": (1) `curl -s <host>/ |
    grep -c 'new-marker'` — confirm the server actually returns the new
    HTML; (2) check the browser's live DOM for the element (`getElementById`)
    — if absent in a fresh session it's a JS error (verify with `node
    --check` on the extracted `<script>` and cross-check every
    `getElementById`/`$('id')` reference against `id="..."` in the HTML —
    a missing ID throws and blanks the page); (3) if server+DOM are fine but
    the user still sees the old page, it's browser cache → add the headers
    above and tell the user to hard-refresh (Cmd+Shift+R).

## Related Skills

- `writing-plans` — use for the planning phase before implementing
- `design-taste-frontend` — when frontend needs visual polish
- `bash-cli-patterns` — for test/startup scripts
- `docker-production-deployment` — when ready to containerize

## References
- `references/web-demo-phase11.md` — the full Phase 11 development report [...]
- `references/demo-rebuild-orchestration.md` — parallel-subagent rebuild recipe: 3-agent file split (backend/data/frontend), API contract, self-contained prompt requirements, post-batch verification checklist
- `references/checkpoint-investigation-pattern.md` — systematic methodology for
  verifying multi-head model checkpoints before building a demo; includes real
  example of joint-training head collapse discovery
- `references/hf-model-compat-patching.md` — patching HuggingFace model custom
  code for transformers version compatibility (forced_bos_token_id,
  _supports_sdpa, einops); fix rather than substitute the user's chosen model
- `references/checkpoint-loading-recipe.md` — verified production loader
  (`_detect_hidden_dim` + `_safe_load_state` with ≥30-key floor and critical
  layers), real 44/44-key test transcript, xywh-vs-xyxy head-format bug,
  monkeypatch-forward filter validation, degenerate-input fallbacks, and
  API-contract notes (Pitfalls 22–24)
- `references/vlm-coordinate-baseline.md` — qwen3-vl-flash returns coords in
  a fixed 1080×960 frame regardless of input size; diagnosing via coord-range
  stats + live API probe + A/B render; the 4-file fix; hero cases 12→6 fallout
  (Pitfalls 25–26)
- `references/proposal-matched-flag.md` — annotating each proposal with its
  GT-match status so the frontend can color green=recovered / blue=unmatched;
  the matched-GT-vs-matched-proposal trap; green boxes must use the GT
  element's real bbox (not the proposal's); GT/screenshot aspect-ratio
  mismatch filter (1440×2392 vs 1080×1920) (Pitfalls 27–29)
- `references/screenshot-overlay-separated.md` — user-mandated 4-canvas
  layout: clean screenshot canvas + dark-bg overlay canvas per panel
  (HTML/CSS/JS diff, verified output) (Pitfall 30)
- `references/synthetic-vs-real-metric-collapse.md` — re-verification recipe:
  report AUROC 0.989 / +40–56% IoU were synthetic-condition results that
  collapsed on real VLM data (0.489–0.603 AUROC; GNN IoU 0.198 < NN 0.212);
  scripts for existence-AUROC and proposal-vs-NN IoU on real data (Pitfall 31)
- `references/honest-demo-assets.md` — building the capability-validation
  panels: Youden's-J threshold for biased sigmoid heads, curve-only demos
  when benchmark weights were never persisted, showing all runs incl.
  negatives (Pitfall 32)
- `references/capability-tab-frontend.md` — Mode C frontend: 3-tab layout
  (tabs + lazy-loaded panels), hand-drawn canvas line chart (grid/axes/
  legend/run-scatter), honest-annotation placement (amber condition note +
  muted real-data note), `/api/demo/*` endpoints serving pre-computed JSON/PNG
