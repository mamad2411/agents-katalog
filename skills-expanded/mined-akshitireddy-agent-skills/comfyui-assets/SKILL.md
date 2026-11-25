---
name: comfyui-assets
description: Generate textures, cutouts, or coordinated bitmap assets when the task calls for local ComfyUI generation.
---

# ComfyUI assets

Use ComfyUI for bitmap generation when the project already has, or explicitly
chooses, a local ComfyUI workflow. Prefer the project's existing server, models,
custom nodes, and output conventions. Do not install models, custom nodes, or a
separate integration merely because this skill was selected.

Keep the server bound to loopback unless the user has requested and secured
remote access. Custom nodes and model tooling execute third-party code locally;
review their source and provenance before adding them to an environment.

## Submit bounded jobs

ComfyUI commonly exposes `/prompt`, `/history/{prompt_id}`, and `/view`. Submit a
workflow in API format, retain every returned `prompt_id`, and bound both each
HTTP request and the overall wait:

```js
async function requestJson(url, init = {}) {
  const response = await fetch(url, {
    ...init,
    signal: AbortSignal.timeout(10_000),
  });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}

const baseUrl = "http://127.0.0.1:8188";
const queued = await requestJson(`${baseUrl}/prompt`, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ prompt: workflow, client_id: clientId }),
});
if (typeof queued.prompt_id !== "string" || !queued.prompt_id) {
  throw new Error("ComfyUI did not return a prompt ID");
}

const deadline = Date.now() + 5 * 60_000;
let result;
while (Date.now() < deadline) {
  const history = await requestJson(
    `${baseUrl}/history/${encodeURIComponent(queued.prompt_id)}`,
  );
  result = history[queued.prompt_id];
  if (result) break;
  await new Promise((resolve) => setTimeout(resolve, 700));
}
if (!result) throw new Error(`Timed out waiting for ${queued.prompt_id}`);
if (result.status?.status_str === "error" || result.status?.completed === false) {
  throw new Error(`ComfyUI job ${queued.prompt_id} failed`);
}
```

Choose timeout values from the expected local model latency and batch size.
A timeout ends the wait, not the server job. Check the owned job's state before
retrying so a lost response does not create duplicate generation work.
Inspect the returned status/messages when reporting a failure. Encode every
`/view` query parameter and write response bytes only to a chosen output
directory; never treat a server-returned filename or subfolder as a trusted
local path.

On a shared server, delete only queued prompt IDs submitted by this task. The
common `/interrupt` endpoint affects the active server job globally, so use it
only on an isolated server or after confirming that the active job is yours.
Keep a record of owned prompt IDs rather than clearing the whole queue or
history.

## Select models by a local comparison

Inspect what is already installed, then render a small representative comparison
when model choice affects quality or cost. Compare prompt adherence, style fit,
latency, peak memory, and output consistency on the actual machine. SDXL, FLUX,
and their variants have different strengths, but quantization, resolution,
sampler, accelerator, and implementation can reverse generic speed or memory
claims. Record the chosen model, workflow, seed, sampler, steps, and settings
needed to reproduce shipped assets.

## Match the asset pipeline

- **Runtime-lit materials:** request flat, even illumination and reject baked
  highlights or shadows that fight the runtime light. Baked lighting can be
  intentional for unlit or stylized pipelines.
- **Seamless textures:** use a workflow that provides circular/tiling behavior,
  then inspect a 3×3 composite for seams and distracting repetition.
- **Cutouts:** generate against a separable background, remove it with an
  existing segmentation tool, trim transparent margins, and inspect edge halos
  at final display scale.
- **Libraries and variants:** hold the art direction and relevant generation
  settings stable enough for coherence. Vary them deliberately when a local
  comparison shows that one setup does not serve every asset class.

Generate only enough candidates to make the decision. Use contact sheets for
large batches, inspect anomalies and likely rejects closely, and inspect every
asset selected for shipping at its intended size and beside its siblings. Check
dimensions, alpha, tiling where applicable, value range, compression, and file
weight.

## Publication and privacy

ComfyUI images can embed the workflow, prompt, model names, node configuration,
and source paths in metadata. Before committing, publishing, or sending an
asset, inspect the publication copy and remove metadata that is not intentionally
part of the deliverable. Keep prompts, workflow JSON, seeds, input images, and
model details private unless the user wants them distributed and they have been
reviewed for credentials, personal data, private paths, and licensing terms.

Preserve a reproducibility manifest in an approved project location when it is
useful, but do not assume it belongs beside public assets. Report which outputs
were visually inspected and which were assessed only through a contact sheet or
automated checks.
