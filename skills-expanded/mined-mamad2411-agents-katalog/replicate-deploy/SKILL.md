---
name: replicate-deploy
description: Ship models to production on Replicate, deployments with autoscaling and dedicated hardware, and packaging custom models with Cog (cog.yaml, predict.py, cog push). Use when the user wants stable throughput, private endpoints, or to publish their own model.
---

# Deployments and custom models

## Deployments: production control for any model

A deployment wraps a model (public or your own) in a private, dedicated
endpoint with control over hardware and scaling. Create one in the web UI
or via the API.

- Run predictions:
  `POST /v1/deployments/{owner}/{name}/predictions` (same body as normal
  predictions; `Prefer: wait` supported, 60 second hold).
- Update scaling:
  `PATCH /v1/deployments/{owner}/{name}` with
  `{"min_instances": 1, "max_instances": 10}`.
- Hardware: choose CPU or GPUs (T4, A100, H100 classes) and switch without
  code changes.
- `min_instances >= 1` keeps an instance warm and kills cold starts;
  `min_instances: 0` scales to zero but pays the cold start on the next
  request.
- Rolling updates, canaries, and rollbacks are built in; you can also only
  delete a deployment after it has been offline and unused for about 15
  minutes.

Cost reality: deployments bill for provisioned time. At high utilization
they cost about the same as pay-per-use; an idle always-on H100 burns
several dollars per hour doing nothing. Size `min_instances` from real
traffic.

## Cog: package your own model

Cog (https://cog.run, open source) turns arbitrary ML code into a
production container Replicate can run. Two files:

`cog.yaml`:

```yaml
build:
  gpu: true
  python_version: "3.13"
  python_requirements: requirements.txt
predict: "predict.py:Predictor"
```

`predict.py`:

```python
from cog import BasePredictor, Input, Path

class Predictor(BasePredictor):
    def setup(self):
        self.model = load_model("./weights")  # runs once per boot

    def predict(self, image: Path = Input(description="Input image"),
                scale: float = Input(default=1.5)) -> Path:
        return run(self.model, image, scale)
```

Typed inputs become the model's public API schema automatically. With
`gpu: true`, Cog picks compatible CUDA/cuDNN versions from your framework
versions.

## Test locally, then push

```bash
cog predict -i image=@input.jpg     # builds the image and runs one prediction
cog login
cog push r8.im/<username>/<model-name>
```

Create the model page first at https://replicate.com/create; the username
and model name in the push target must match it. Useful flags:
`--separate-weights` (weights in their own layer for faster iteration) and
`--use-cog-base-image` (faster cold boots). For CI, the
`replicate/setup-cog` GitHub Action installs Docker buildx, Cog, and CUDA
tooling.

After push, Replicate auto-generates the API server; the model runs
pay-per-use immediately, and you add a deployment when you need dedicated
scaling.

## Gotchas

- Keep `setup()` fast and deterministic; everything slow there is your
  cold start.
- Bake weights into the image or a mounted layer; downloading weights in
  `setup()` at boot is the most common cold start mistake.
- Private models plus a deployment is the standard pattern for proprietary
  weights: nothing public, dedicated endpoint, API token gated.
