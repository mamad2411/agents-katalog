---
name: ai-science-diffusion-generative-models
description: "Code DDPM/DDIM diffusion samplers, linear/cosine noise schedules, and DDRM inverse-problem solving (denoising, inpainting, super-resolution) in NumPy/PyTorch. Use for forward/reverse diffusion, score matching, or DDIM sampling."
tool_type: python
primary_tool: PyTorch
---

# Diffusion Generative Models

## When to Use

- Explaining or implementing the forward/reverse diffusion process (DDPM), score matching, or noise schedules
- Writing a DDIM sampler to generate samples in fewer steps than the training trajectory
- Solving an inverse problem (denoising, inpainting, super-resolution) with a pretrained diffusion model as a prior (DDRM/DPS-style data consistency)
- Debugging why a diffusion model's samples are blurry, noisy, or diverging (schedule, clipping, or guidance-scale issues)
- Teaching/reviewing the math connecting score matching, Tweedie's formula, and the ε-prediction parameterization

## Version Compatibility

- Concepts and formulas apply to DDPM (Ho et al. 2020), improved schedules (Nichol & Dhariwal 2021), DDIM (Song et al. 2021), and DDRM (Kawar et al. 2022)
- Code below is pure NumPy (≥1.24) so it runs anywhere; for a trainable network use PyTorch ≥2.1 (`torch.nn`, `torch.optim`) or `diffusers` ≥0.27 for production pipelines
- Python ≥3.10

## Prerequisites

- `pip install numpy` (core); `pip install torch diffusers` if training/running a real UNet
- Familiarity with Gaussian conditioning, basic SVD, and gradient descent
- Related: `ai-science-esm2-embeddings` (protein language models), `bio-structural-biology-alphafold-predictions` (structure diffusion in AlphaFold3/RFdiffusion-style models)

## Key Concepts

- **Forward (q)**: adds noise deterministically. **Reverse (p_θ)**: denoises via a learned network.
- **αₜ vs ᾱₜ**: αₜ = 1 − βₜ (single step noise). ᾱₜ = ∏ₛ₌₁ᵗ αₛ (cumulative signal fraction). The forward closed form uses ᾱₜ, not αₜ — this is the single most common bug when reimplementing DDPM.
- **Cosine schedule** (Nichol & Dhariwal 2021): offset `s=0.008` prevents ᾱₜ from collapsing too fast near t=0, giving better sample quality than the original linear schedule.
- **DDIM η**: η=0 gives a deterministic ODE-like sampler (reproducible, fewer steps needed); η=1 recovers the original stochastic DDPM ancestral sampler.
- **Tweedie's formula**: `E[x0 | xt] = (xt − √(1−ᾱₜ)·ε) / √ᾱₜ` — the same formula the network's ε-prediction is plugged into at every reverse step.

## Score Matching

Learn the score ∇ₓ log p(xₜ) instead of p(xₜ) directly. Denoising score matching relates the score to the noise-prediction network:

$$\nabla_{x_t} \log p(x_t) \approx -\frac{\varepsilon_\theta(x_t, t)}{\sqrt{1-\bar\alpha_t}}$$

**DDPM training loss** (simplified, Ho et al. 2020): $\mathcal{L} = \mathbb{E}_{t, x_0, \varepsilon}\left[\|\varepsilon - \varepsilon_\theta(x_t, t)\|^2\right]$, where $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\varepsilon$.

**Goal:** build the noise schedules (`βₜ`, `αₜ`, `ᾱₜ`) that every diffusion step depends on.
**Approach:** precompute cumulative products once at setup time — never recompute `ᾱₜ` inside the sampling loop.

```python
import numpy as np


def linear_schedule(T=1000, beta_start=1e-4, beta_end=0.02):
    """Original DDPM (Ho et al. 2020) linear beta schedule."""
    betas = np.linspace(beta_start, beta_end, T)
    alphas = 1 - betas
    alpha_bars = np.cumprod(alphas)
    return betas, alphas, alpha_bars


def cosine_schedule(T=1000, s=0.008):
    """Improved cosine schedule (Nichol & Dhariwal 2021).

    Keeps signal-to-noise ratio decaying smoothly instead of collapsing
    near t=0 as the linear schedule does.
    """
    t = np.arange(T + 1)
    f = np.cos((t / T + s) / (1 + s) * np.pi / 2) ** 2
    alpha_bars = f / f[0]
    betas = 1 - alpha_bars[1:] / alpha_bars[:-1]
    betas = np.clip(betas, 0, 0.999)
    return betas, 1 - betas, alpha_bars[1:]


def forward_diffuse(x0, t, alpha_bars, seed=0):
    """Closed-form forward noising: x_t = sqrt(abar_t)*x0 + sqrt(1-abar_t)*eps."""
    rng = np.random.default_rng(seed)
    ab = alpha_bars[t]
    eps = rng.standard_normal(x0.shape)
    return np.sqrt(ab) * x0 + np.sqrt(1 - ab) * eps, eps
```

## DDIM Reverse Sampling

$$x_{t-1} = \sqrt{\bar\alpha_{t-1}}\, \hat{x}_0 + \sqrt{1 - \bar\alpha_{t-1} - \sigma_t^2}\, \varepsilon_\theta(x_t, t) + \sigma_t \varepsilon$$

**Goal:** turn a trained (or oracle) ε-predictor into samples, in far fewer than `T` steps.
**Approach:** re-derive `x̂0` from `ε_θ` at every step (Tweedie's formula), then step deterministically (η=0) or stochastically (η=1).

```python
def ddim_step(xt, eps_pred, t, t_prev, alpha_bars, eta=0.0):
    """One DDIM reverse step. eta=0 -> deterministic; eta=1 -> DDPM ancestral."""
    ab_t = alpha_bars[t]
    ab_prev = alpha_bars[t_prev] if t_prev >= 0 else 1.0

    x0_pred = (xt - np.sqrt(1 - ab_t) * eps_pred) / (np.sqrt(ab_t) + 1e-9)
    x0_pred = np.clip(x0_pred, -1.5, 1.5)  # match training data range

    sigma = eta * np.sqrt((1 - ab_prev) / (1 - ab_t + 1e-9) * (1 - ab_t / ab_prev))
    noise = sigma * np.random.randn(*xt.shape) if eta > 0 else 0.0
    xt_prev = (np.sqrt(ab_prev) * x0_pred
               + np.sqrt(max(1 - ab_prev - sigma**2, 0)) * eps_pred
               + noise)
    return xt_prev, x0_pred


def run_ddim(xT, x0_true, alpha_bars, n_steps=20, eta=0.0):
    """Sample by running ddim_step along a strided timestep schedule.

    x0_true is only used here to build an oracle denoiser (for teaching /
    unit tests); replace `oracle_denoiser` with a real network's eps_theta(xt, t).
    """
    def oracle_denoiser(xt, t):
        ab = alpha_bars[t]
        return (xt - np.sqrt(ab) * x0_true) / np.sqrt(1 - ab + 1e-9)

    T = len(alpha_bars)
    timesteps = np.linspace(T - 1, 1, n_steps).astype(int)
    xt = xT.copy()
    for i, t in enumerate(timesteps[:-1]):
        t_prev = timesteps[i + 1]
        eps_pred = oracle_denoiser(xt, t)
        xt, x0_pred = ddim_step(xt, eps_pred, t, t_prev, alpha_bars, eta=eta)
    return xt, x0_pred
```

## DDRM: Solving Inverse Problems with a Diffusion Prior

Degradation operator `H` examples: denoising (H=I), inpainting (H=binary mask), super-resolution (H=downsampling). At every DDIM step, project `x̂0` onto the measurement subspace using the pseudoinverse of `H` (via its SVD):

$$\hat{x}_0^{\text{proj}} = \hat{x}_0 + V \cdot \frac{s^2}{s^2 + \sigma_y^2} \cdot \frac{U^T y - U^T H\hat{x}_0}{s}$$

**Goal:** pull the diffusion trajectory toward a noisy or partial measurement `y` while still using the model's learned prior to fill in the rest.
**Approach:** after each `ddim_step` produces `x0_pred`, blend it toward `y` at the observed coordinates before continuing.

```python
def ddrm_data_consistency(x0_pred, y_obs, H_type="identity", sigma_obs=0.3):
    """DDRM data-consistency step. H=I case: SVD is trivial (U=V=I, s=1)."""
    if H_type == "identity":
        scale = 1 / (1 + sigma_obs**2)
        return x0_pred + scale * (y_obs - x0_pred)
    raise NotImplementedError(f"H_type '{H_type}' not implemented")


def ddrm_inpainting_step(x0_pred, y_masked, mask, sigma_obs=0.05):
    """DDRM for inpainting: pull observed positions toward y, leave the rest
    to the diffusion prior (mask==1 means observed)."""
    scale = 1 / (1 + sigma_obs**2)
    x0_proj = x0_pred.copy()
    obs = mask == 1
    x0_proj[obs] = x0_pred[obs] + scale * (y_masked[obs] - x0_pred[obs])
    return x0_proj
```

Usage sketch: inside the DDIM loop, after computing `x0_pred`, call `x0_proj = ddrm_data_consistency(x0_pred, y_obs)` (or the inpainting variant), then feed `x0_proj` back through the same forward-noising formula to get the next `xt` — this is what keeps the sample consistent with the measurement at every step, not just at the end.

## Pitfalls

- Confusing forward (q, adds noise) with reverse (p_θ, denoises) — the network is only ever trained to predict noise added by `q`.
- Using `αₜ` where `ᾱₜ` is needed in the forward closed form — this silently produces samples that are far too noisy or too clean.
- Attributing the cosine schedule to Ho et al. 2020 — it's from Nichol & Dhariwal 2021 ("Improved Denoising Diffusion Probabilistic Models").
- Forgetting to clip `x̂0_pred` to the training data range — unclipped predictions cause visible artifacts/divergence in early sampling steps.
- Running DDRM data consistency only on the final sample instead of every reverse step — the prior and the measurement need to be reconciled at each `t`, not once at the end.

## See Also

- `ai-science-esm2-embeddings` — protein language model embeddings, another generative/representation-learning foundation model
- `bio-structural-biology-alphafold-predictions` — structure-prediction models that use diffusion-style refinement (AlphaFold3, RFdiffusion)
- `ai-science-vision-rag` — retrieval-augmented generation over scientific figures/images
- `torch-geometric` — graph neural nets, often paired with diffusion for molecule/structure generation
