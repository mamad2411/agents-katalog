---
name: ae-nerf-3d-manipulation-eval
description: Evaluates a model's ability to reconstruct 3D objects from single 2D images and disentangle/manipulate specific 3D attributes (shape, appearance, camera pose) while preserving high visual fidelity. Use when the user wants to benchmark on CARLA, Photoshapes, or asks about evaluating this task. Reports FID.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2204.13426
  bibtex_key: kim2022aenerf
  confidence: high
---

# ae-nerf-3d-manipulation-eval

> AE-NeRF: Auto-Encoding Neural Radiance Fields for 3D-Aware Object Manipulation — Kim et al. (2022) (arXiv:2204.13426, 2022)

## What this evaluates

Evaluates a model's ability to reconstruct 3D objects from single 2D images and disentangle/manipulate specific 3D attributes (shape, appearance, camera pose) while preserving high visual fidelity.

## Datasets

- **CARLA** — total 10000; splits: test (1000)
- **Photoshapes** — total 150000; splits: test (1000)

## Metrics

- `FID` **(primary)** — range: other
  - Fréchet Inception Distance measuring the distance between feature distributions of real and generated images. Lower values indicate higher reconstruction fidelity.
- `Perceptual distance` — range: other
  - Perceptual distance between the manipulated source image and the target image for a specific attribute (shape, appearance, or camera pose). Lower values indicate better attribute matching.

## Input / output format

**Input**: Single 2D RGB image (256x256) of a 3D object (car or chair).

**Output**: Reconstructed 2D image, or manipulated 2D image with swapped shape, appearance, or camera pose attributes.

## Scoring recipe

```python
def compute_fid(real_imgs, gen_imgs):
    real_feats = inception_model(real_imgs)
    gen_feats = inception_model(gen_imgs)
    mu_r, sigma_r = real_feats.mean(0), np.cov(real_feats, rowvar=False)
    mu_g, sigma_g = gen_feats.mean(0), np.cov(gen_feats, rowvar=False)
    diff = mu_r - mu_g
    covmean, _ = scipy.linalg.sqrtm(sigma_r.dot(sigma_g), disp=False)
    fid = diff.dot(diff) + np.trace(sigma_r + sigma_g - 2 * covmean)
    return np.real(fid)

def compute_perceptual_dist(swapped_img, target_img):
    return perceptual_model(swapped_img, target_img)
```

## Common pitfalls

- FID is computed on a fixed 1K random subset of CARLA and Photoshapes, not the full datasets.
- Perceptual distance is reported separately for shape, appearance, and camera pose swaps rather than as a single aggregate score.
- The custom test subset for attribute swapping (pairs sharing one attribute) is not publicly released.

## Evidence (verbatim from paper)

> To measure the model performance of disentangling 3D attributes from a given image, we use Fréchet Inception Distance (FID) score to measure the degree of fidelity for generated images on 1k dataset of CARLA whose optimized style codes are offered by EditNeRF. We quantitatively evaluate the image quality and accuracy of auto-encoding results using the Frechet Inception Distances (FID) by reconstructing randomly selected 1K images for CARLA Dataset and 1K images for Photoshapes Dataset.

## Citation

```bibtex
@misc{kim2022aenerf,
  title={AE-NeRF: Auto-Encoding Neural Radiance Fields for 3D-Aware Object Manipulation},
  author={Kim et al. (2022)},
  year={2022},
  note={arXiv:2204.13426}
}
```

- arXiv: 2204.13426
