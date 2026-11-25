# Computational Pathology

Whole-slide image processing and slide-level modelling for cancer histopathology. Covers reading vendor formats with OpenSlide, the coordinate and resolution semantics that cause most WSI bugs, tissue detection, tile extraction, stain normalization, H&E colour deconvolution, pathology foundation models as tile encoders, multiple instance learning for slide-level prediction, cell segmentation and classification, spatial statistics on cell positions, and integration with molecular data.

## When to Use This Skill

Activate when the user requests:
- Reading `.svs`, `.ndpi`, `.mrxs`, `.scn`, or other whole-slide formats
- OpenSlide, TiaToolbox, histolab, or slideio pipelines
- Tissue detection or background removal on a slide
- Tile or patch extraction for downstream modelling
- Stain normalization across slides or scanners
- H&E colour deconvolution, or separating hematoxylin from eosin
- Working at a target magnification or microns-per-pixel
- Tile embeddings from UNI, CONCH, Virchow, Prov-GigaPath, H-optimus or Phikon
- Multiple instance learning with CLAM, DSMIL, TransMIL or attention pooling
- Slide-level prediction from tile features
- Splitting a pathology cohort without leakage
- Cell or nucleus segmentation (StarDist, HoVer-Net, Cellpose, InstanSeg)
- Tumour region or tertiary lymphoid structure detection
- Spatial statistics on segmented cell positions
- Correlating morphology with matched expression or mutation data

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Whole-slide image | `.svs`, `.ndpi`, `.mrxs`, `.tiff`, `.scn` | GDC (TCGA), CAMELYON, PANDA |
| Slide metadata | OpenSlide properties | embedded in the file |
| Annotations | GeoJSON, XML, `.qpdata` | QuPath, ASAP, pathologist review |
| Reference tile | RGB image | a slide chosen as the stain target |

---

## Environment

Versions verified 2026-08.

```bash
pip install openslide-python openslide-bin   # 1.4.6 and 4.0.1.2
```

```
openslide-python is a BINDING, not the library. Its only dependency is
Pillow, so `pip install openslide-python` alone gives you an import that
fails at load time with a missing-library error.

openslide-bin ships the compiled OpenSlide C library (4.0.1) as a wheel,
which is why the upstream README tells you to install both. Before it
existed you needed a system package (apt/brew/conda). If you inherit a
pipeline that documents `brew install openslide`, that still works; do not
mix the two in one environment.
```

| Package | Version | Use |
|---|---|---|
| `openslide-python` | 1.4.6 | reading vendor formats, the baseline |
| `openslide-bin` | 4.0.1.2 | the C library as a wheel |
| `tiatoolbox` | 2.1.3 | full pipeline: readers, tiling, models. Python 3.11-3.14 |
| `histolab` | 0.7.0 | tiling and tissue masks. **Capped at Python < 3.12**, last release 2024-02 |
| `slideio` | 2.8.1 | alternative reader, broader format support |
| `large-image` | 1.35.2 | tile server and multi-backend reader |
| `HistomicsTK` | 1.4.0 | stain deconvolution, maintained (pushed 2026-08) |
| `torchstain` | 1.4.1 | Macenko and Reinhard normalization on tensors |
| `staintools` | 2.1.2 | **abandoned.** Last release 2019-04-11, GitHub archived 2021-05-08 |
| `stardist` | 0.9.2 | H&E nuclei model; needs a TF backend via `csbdeep[tf]` |
| `hover_net` | git only | nuclei + cell type; MIT; last pushed 2023-10 |
| `cellpose` | 4.2.1.1 | generalist cell segmentation |
| `instanseg-torch` | 0.1.1 | newer PyTorch nucleus/cell segmentation |
| `squidpy` | 1.8.3 | spatial statistics; **Python >= 3.12** |
| `pointpats` | 2.6.0 | point-pattern statistics on plain coordinates |

Use `torchstain` or `HistomicsTK` instead of `staintools`. Tutorials still recommend it; it has been archived for five years.

---

## Reading a Slide

A WSI is a pyramid. Level 0 is full resolution and can be 100k x 100k pixels; each higher level is a downsampled copy.

```python
import openslide

slide = openslide.OpenSlide(path)
print(slide.level_count)         # number of pyramid levels
print(slide.level_dimensions)    # (width, height) per level
print(slide.level_downsamples)   # downsample factor per level
```

### The coordinate frame trap

```python
region = slide.read_region(location, level, size)
```

```
location is ALWAYS in the level 0 reference frame.
size     is in the frame of the level you are reading.

These are different frames in the same call. It is the single most common
WSI bug, and it fails silently: you get an image of the right shape showing
the wrong part of the slide.

To read a WxH tile at level L starting from tile index (i, j):
    d = slide.level_downsamples[L]
    location = (int(i * W * d), int(j * H * d))   # scaled to level 0
    tile = slide.read_region(location, L, (W, H)) # size NOT scaled

Reading at level 0 hides the bug, because the two frames coincide there.
Code that works on a level-0 prototype and breaks at level 2 is almost
always this.
```

### Downsamples are floats

```
level_downsamples is tuple[float, ...], not integers.

A level nominally "4x downsampled" is often 4.0000123, because the level
dimensions are rounded independently per axis. Do not assume powers of two,
and do not use == to pick a level.

    d = slide.level_downsamples[level]        # 4.0000123, not 4
    level = slide.get_best_level_for_downsample(target)   # use this

get_best_level_for_downsample returns the highest level whose downsample is
<= target, so it errs toward MORE resolution than asked. Read at that level
and resize down; never read at a coarser level and upscale.
```

### Magnification is not resolution

```python
props = slide.properties
mpp_x = float(props[openslide.PROPERTY_NAME_MPP_X])   # 'openslide.mpp-x'
power = props.get(openslide.PROPERTY_NAME_OBJECTIVE_POWER)  # '40'
```

```
"40x" is not a resolution. It is a nominal objective power, and the actual
microns per pixel varies by scanner: 40x is commonly ~0.25 um/px but ranges
roughly 0.23-0.28 across vendors. Training tiles at "40x" from two scanners
gives you two different physical scales, and the model learns the scanner.

Work in MICRONS PER PIXEL, not magnification. Pick a target mpp, compute the
downsample you need, and resize:

    target_mpp = 0.5
    scale = target_mpp / mpp_x
    level = slide.get_best_level_for_downsample(scale)

mpp-x and mpp-y can differ. Check both; non-square pixels exist.

Both properties are OPTIONAL. Some slides carry neither, and a KeyError on
'openslide.mpp-x' mid-run is a bad way to discover it. Validate up front and
skip or flag slides without mpp rather than guessing 0.25.
```

### Bounds

```
Some formats (notably MIRAX/.mrxs) store a small scanned region inside a
much larger canvas of empty space. openslide.bounds-x, bounds-y,
bounds-width and bounds-height give the non-empty rectangle.

Tiling over level_dimensions without checking bounds wastes most of the
run on blank canvas, and the blank area is not always white.
```

## Tissue Detection

Tile everything and most tiles are background. Detect tissue on a low
resolution level first, then map back.

```python
import numpy as np
from skimage.color import rgb2hsv
from skimage.filters import threshold_otsu

level = slide.level_count - 1                       # smallest level
thumb = np.array(slide.read_region((0, 0), level,
                                   slide.level_dimensions[level]).convert("RGB"))
sat = rgb2hsv(thumb)[..., 1]                        # saturation
mask = sat > threshold_otsu(sat)
```

```
Why saturation rather than intensity: background glass is bright AND
unsaturated, while tissue is coloured. A pure intensity threshold also
removes pale tissue such as adipose and mucin, which is real signal.

Otsu assumes a bimodal histogram. A slide that is almost entirely tissue,
or almost entirely background, has no valley to find and Otsu will split
noise. Sanity-check the resulting tissue fraction and fall back to a fixed
threshold when it lands outside a plausible range.

Pen marks, coverslip edges, air bubbles and out-of-focus regions all pass
a saturation threshold. They are a large fraction of real-world artefacts
and need explicit handling, not a better threshold.
```

## Tile Extraction

```python
def tile_grid(slide, level, size, overlap=0):
    """Yield level-0 locations for a tile grid at `level`."""
    d = slide.level_downsamples[level]
    w, h = slide.level_dimensions[level]
    step = size - overlap
    for y in range(0, h - size + 1, step):
        for x in range(0, w - size + 1, step):
            yield (int(x * d), int(y * d))          # level 0 frame
```

```
Overlap matters when a model has an effective receptive field near the tile
size, or when you stitch predictions back together. Without overlap,
objects on a tile boundary are split and counted twice or missed.

Discard tiles below a tissue fraction, but record the threshold. "Tiles with
>50% tissue" and "tiles with >10% tissue" produce different cohorts, and the
number is rarely reported.

read_region returns RGBA. The alpha channel is not decoration: on some
formats it marks unscanned area. Calling .convert("RGB") composites onto
black by default, which turns unscanned regions into black tissue-coloured
pixels. Composite onto white explicitly for H&E.
```

```python
from PIL import Image

rgba = slide.read_region(loc, level, (size, size))
bg = Image.new("RGB", rgba.size, (255, 255, 255))
bg.paste(rgba, mask=rgba.split()[3])       # composite on white, not black
tile = bg
```

## Stain Normalization

Two H&E slides from different labs differ in colour more than they differ in biology. A model trained on one scanner degrades on another.

```python
import torch
from torchstain.torch import MacenkoNormalizer     # 1.4.1

normalizer = MacenkoNormalizer(backend="torch")
normalizer.fit(reference_tile)                     # one target image
normalized, H, E = normalizer.normalize(I=tile, stains=True)
```

```
Method choice:

  Macenko    SVD on the optical-density plane, picks stain vectors from
             percentile angles. Fast, deterministic, the default.
  Reinhard   matches mean and std in LAB space. Cheapest, ignores stain
             structure entirely; fine for mild shifts.
  Vahadane   sparse NMF, better on strong stain variation, much slower.

torchstain provides Macenko, MultiMacenko and Reinhard. It does NOT ship
Vahadane. For sparse-NMF separation use HistomicsTK's
separate_stains_xu_snmf, or Macenko where speed matters.

The reference tile is a parameter of your pipeline, not an implementation
detail. Every normalized value depends on it. Record which slide and which
tile, and reuse the same one across train and test, or you have introduced
a covariate shift you cannot see.

Normalization on a mostly-background tile estimates stain vectors from
glass and produces garbage. Run tissue detection first, and skip
normalization for tiles below the tissue threshold rather than normalizing
them badly.
```

## Colour Deconvolution

Separating H&E into its stain channels, via Beer-Lambert in optical-density space.

```python
from skimage.color import rgb2hed, hed2rgb, rgb_from_hed

hed = rgb2hed(tile)          # channels: Hematoxylin, Eosin, DAB
h = hed[..., 0]              # nuclei
e = hed[..., 1]              # cytoplasm and stroma
```

```
rgb2hed always returns THREE channels, H, E and DAB, because it uses a
fixed 3x3 stain matrix. On an H&E slide the DAB channel is not a stain
measurement; it absorbs whatever the H and E vectors cannot explain. Do not
interpret it as DAB positivity on a slide that never saw DAB.

The stain matrix is fixed, not fitted. rgb_from_hed rows are the H, E and
DAB absorption vectors from Ruifrok and Johnston. If your slides deviate
from those reference stains, an estimated matrix (Macenko or SNMF) is more
faithful than the built-in constant.

NEGATIVE CONCENTRATIONS ARE CLIPPED TO ZERO. separate_stains ends with
np.maximum(stains, 0), so any colour outside the cone spanned by the stain
vectors loses information silently.

Measured on scikit-image 0.26.0 with random RGB in [0.4, 0.9]:
    pixels with at least one clipped channel : 784 of 1024
    round-trip max error where NOT clipped   : 1.1e-16  (exact)
    round-trip max error where clipped       : 6.1e-01  (large)

So rgb2hed -> hed2rgb is exact only for colours the stain basis can
represent. Real H&E mostly lies inside the cone and clips far less than
random RGB, but the failure is silent either way. If you need a faithful
round trip, check for zeroed channels rather than assuming.

Input is also floored: np.maximum(rgb, 1e-6) avoids log(0), so pure black
is not preserved either.
```

## Feature Extraction

A slide is far too large for a single forward pass, so the standard pipeline encodes tiles independently and aggregates the embeddings. Tile encoders pretrained on histopathology beat ImageNet features by a wide margin, which is why they are worth the access friction below.

### Access is the first problem, not the last

```
Almost every pathology foundation model is GATED on HuggingFace. You must be
logged in and have accepted the model's terms before the weights download.

Verified anonymously, 2026-08:
    MahmoodLab/UNI    config.json -> HTTP 401
    owkin/phikon-v2   config.json -> HTTP 200

A script that works on the author's machine fails for a collaborator with a
401 that reads like a network error. Authenticate explicitly and fail loudly:

    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"])      # never hardcode the token
```

| Model | Gated | Licence | Kind |
|---|---|---|---|
| `MahmoodLab/UNI` | yes | CC-BY-NC-ND-4.0 | vision, self-supervised |
| `MahmoodLab/UNI2-h` | yes | CC-BY-NC-ND-4.0 | vision, larger |
| `MahmoodLab/CONCH` | yes | CC-BY-NC-ND-4.0 | **vision-language** |
| `paige-ai/Virchow` | yes | Apache-2.0 | vision |
| `paige-ai/Virchow2` | yes | CC-BY-NC-ND-4.0 | vision |
| `prov-gigapath/prov-gigapath` | yes | Apache-2.0 | tile + slide encoder |
| `bioptimus/H-optimus-0` | yes | Apache-2.0 | vision |
| `owkin/phikon` | **no** | other | vision, 768-dim |
| `owkin/phikon-v2` | **no** | other | vision, 1024-dim (DINOv2) |

```
LICENCES ARE NOT A FORMALITY HERE.

CC-BY-NC-ND covers UNI, UNI2-h, CONCH and Virchow2. NC forbids commercial
use. ND forbids distributing derivative works, which on a plain reading
includes a fine-tuned checkpoint. If your plan is to fine-tune and release
weights, or to deploy clinically, check the licence BEFORE you build on it.
Virchow v1, Prov-GigaPath and H-optimus-0 are Apache-2.0 and do not carry
those restrictions.

The ungated Owkin models are the ones to prototype with: no access request,
no 401, and phikon-v2 is a reasonable encoder. Swap in a gated model once
you have confirmed the pipeline and the licence.
```

### Loading a tile encoder

```python
import timm, torch

model = timm.create_model("hf-hub:MahmoodLab/UNI", pretrained=True,
                          init_values=1e-5, dynamic_img_size=True)
model.eval()
cfg = timm.data.resolve_data_config({}, model=model)
transform = timm.data.create_transform(**cfg)      # do NOT hand-roll this
```

```
Use the transform the model ships with. Each encoder was trained at a
specific input size with specific normalization constants, and substituting
ImageNet mean/std or a different resize silently degrades the embeddings.
Nothing errors; the features are just worse, and you will attribute the
drop to your data.

Embedding dimension is a property of the model, not a constant:
    phikon      768
    phikon-v2  1024
Read it from the model rather than hardcoding, because a downstream MIL head
sized for the wrong dimension either crashes or, worse, trains on a
misaligned view after a reshape.

    dim = model.num_features
```

### CONCH is a different kind of model

```
CONCH is vision-LANGUAGE, trained on image-caption pairs. That buys
zero-shot classification from text prompts, which the vision-only encoders
cannot do. It also means the image tower alone is not necessarily the best
pure vision encoder available; if you only need embeddings, compare against
UNI or H-optimus-0 rather than assuming the multimodal model dominates.
```

### CTransPath needs a forked timm

```
CTransPath is still widely cited, and its repository asks you to install a
MODIFIED timm 0.5.4 distributed as a tarball on a Google Drive link. Current
timm is 1.0.28.

That is a reproducibility and supply-chain problem: a pinned fork from a
file-sharing link, unversioned on PyPI, that conflicts with the timm every
other model in your pipeline needs. If you need CTransPath, isolate it in
its own environment. Prefer an encoder that loads from current timm.
```

## Multiple Instance Learning

You have a label per slide and no label per tile. That is exactly the MIL setting: a bag of instances carries one bag-level label.

```
bag       = one slide
instances = its tiles (hundreds to tens of thousands)
label     = slide-level (diagnosis, grade, mutation status, outcome)

The model must learn which instances matter without ever being told.
```

### Attention pooling

```python
import torch, torch.nn as nn

class ABMIL(nn.Module):
    """Attention-based MIL pooling (Ilse et al.). One bag at a time."""
    def __init__(self, dim, hidden=256, n_classes=2):
        super().__init__()
        self.attn = nn.Sequential(nn.Linear(dim, hidden), nn.Tanh(),
                                  nn.Linear(hidden, 1))
        self.head = nn.Linear(dim, n_classes)

    def forward(self, h):                    # h: (n_tiles, dim)
        a = torch.softmax(self.attn(h), dim=0)   # (n_tiles, 1)
        z = (a * h).sum(dim=0)                   # weighted bag embedding
        return self.head(z), a
```

```
Bag size varies by orders of magnitude across slides, so batching is not
straightforward. The usual answer is batch size 1 with gradient
accumulation. A fixed-size random subsample of tiles per bag is the common
alternative, and it changes what the model sees each epoch; state which you
used.

Softmax over instances means attention is a distribution: adding more
background tiles to a bag mathematically lowers the weight on the tiles that
matter. Tissue filtering is therefore not just a compute saving, it changes
the optimisation.
```

### Framework choice

| Framework | Licence | Note |
|---|---|---|
| CLAM | **GPL-3.0** | attention MIL plus instance-level clustering. Copyleft: check before embedding in a product |
| DSMIL | MIT | dual-stream, permissive |
| TransMIL | **none declared** | self-attention over instances. With no licence, default copyright applies and reuse rights are unclear |
| TRIDENT | see repo | the maintained Mahmood Lab pipeline, actively developed |
| `torchmil` | see repo | generic deep MIL for PyTorch, on PyPI |

```
`pip install trident` DOES NOT install the pathology TRIDENT. That name on
PyPI belongs to an astrophysics package for simulating UV observations.
The pathology one installs from source:

    git clone https://github.com/mahmoodlab/trident.git && cd trident
    pip install -e .
    pip install -e ".[patch-encoders]"      # CONCH, MUSK, CTransPath/CHIEF
    pip install -e ".[slide-encoders]"      # PRISM, GigaPath, Madeleine

A tutorial that says "pip install trident" was not run by its author.
```

### The split that decides whether any of this is real

```
SPLIT BY SLIDE, AND BY PATIENT. NEVER BY TILE.

Tiles from one slide are near-duplicates of each other. If tiles from the
same slide land in both train and test, the model memorises the slide and
reports near-perfect accuracy that collapses on new cases. This is the
single most common way a computational pathology result turns out to be
worthless.

Patient, not just slide: one patient often contributes several slides, and
two slides from the same block share more than biology.

Stratify by site as well when the cohort is multi-institutional. Scanner and
staining protocol are site-specific, so a model can separate outcomes by
learning the site. Report performance on a held-out SITE, not only a
held-out patient, whenever the data allows it.
```

```
Baselines, as always:
  - mean-pooled tile embeddings with logistic regression
  - max-pooled embeddings
Attention MIL that does not beat mean pooling has not earned its complexity.
Report the baseline in the same table.

Attention weights are NOT an explanation. They show what the pooling
up-weighted for that prediction, which is not the same as evidence a
pathologist would accept, and they are unstable across seeds. Show them as a
hypothesis to review, and report agreement with annotation when you have it.
```

## Cell Segmentation

Slide- and tile-level embeddings are one route; the other is to segment individual cells and reason about their positions and types. The two answer different questions, and the second needs the tissue at high resolution.

```
Segment at the RIGHT magnification. Nuclear segmentation needs ~0.25 um/px
(nominal 40x). Run it on a 20x or downsampled tile and small nuclei merge
or vanish. This is the mpp discipline from the reading section, now
load-bearing: the wrong scale silently changes the cell count.
```

### Tool choice

| Tool | Install | Output | Note |
|---|---|---|---|
| StarDist | `pip install stardist` | star-convex nuclei | ships an H&E model; needs a TF backend |
| HoVer-Net | **git clone**, not PyPI | nuclei + type | classifies cell type; heavier; stale |
| Cellpose | `pip install cellpose` 4.2 | general cells | strong generalist, not H&E-specific |
| InstanSeg | `pip install instanseg-torch` | nuclei/cells | newer, fast, PyTorch |
| TIAToolbox | `pip install tiatoolbox` | wraps several | maintained, integrates with the WSI reader |

### StarDist for H&E nuclei

```python
from stardist.models import StarDist2D
from csbdeep.utils import normalize

model = StarDist2D.from_pretrained("2D_versatile_he")   # H&E nuclei model
labels, details = model.predict_instances(normalize(tile))
```

```
`pip install stardist` DOES NOT install a deep-learning backend. StarDist
runs on TensorFlow through csbdeep, which pulls it only via the csbdeep[tf]
extra. A bare install imports fine and then fails at model.predict with a
missing-backend error, not at install. Install the backend explicitly.

Normalize with csbdeep.utils.normalize (a percentile normalization), not a
0-1 rescale. The pretrained model was trained on percentile-normalized input;
feeding it raw or min-max-scaled tiles degrades segmentation silently.

The `2D_versatile_he` model is trained for H&E. Do not use `2D_versatile_fluo`
on brightfield; it expects fluorescence and will undersegment.
```

### HoVer-Net when you need cell TYPES

```
HoVer-Net segments AND classifies (epithelial, inflammatory, connective,
etc.), which StarDist's versatile model does not. It is not on PyPI: install
from the git repository (MIT licensed). The repository was last updated
2023-10, so pin your environment and expect dependency friction with current
PyTorch.

Its cell types come from the training panel (PanNuke, CoNSeP, MoNuSAC).
Those are the classes you get, and they may not match your tumour type.
A "connective" class trained on colorectal tissue is not a validated label
on a lymph node.
```

### Segmentation is not free of the same traps

```
Report cells per mm^2, not cells per tile. Tile size in microns varies with
mpp, so a raw count per tile is not comparable across slides or scanners.

Boundary double-counting: a nucleus straddling two tiles is segmented in
both. Deduplicate on the stitched coordinates, or segment with overlap and
keep only cells whose centroid falls in the tile interior.

Validate against a counted region. Segmentation F1 on a held-out annotated
patch is the number to report, per cell type where the model classifies.
"It looks right" is not validation.
```

## Region and Structure Detection

### Tumour region

```
Two routes:
  Supervised     a tile classifier (tumour vs stroma vs necrosis vs normal)
                 trained on pathologist annotation, then applied per tile.
  Foundation     cluster the tile embeddings from the encoder; label the
                 clusters against a few annotated regions.

The supervised route needs annotation, which is expensive; the foundation
route needs far less but gives regions defined by embedding similarity, not
by a pathologist's category. State which, because a reviewer will ask whether
"tumour region" means annotated tumour or a cluster you called tumour.
```

### Tertiary lymphoid structures

```
TLS are dense aggregates of lymphocytes, sometimes with a germinal centre,
and they carry prognostic and immunotherapy-response signal. Detecting them
is a density-and-organisation problem, not a single-cell one:

  1. segment and classify cells (lymphocytes specifically)
  2. find dense lymphocyte aggregates (density threshold or clustering)
  3. distinguish a true TLS from diffuse infiltration by size and compactness

A lymphocyte-rich tile is not a TLS. Diffuse infiltration and an organised
follicle look similar in aggregate counts and differ in spatial
organisation, which is exactly what the spatial statistics below measure.
Maturity (germinal-centre presence) needs additional markers and is not
callable from H&E alone with confidence.
```

## Spatial Statistics on Cell Positions

Once cells have positions and types, the questions become spatial: are two cell types closer than chance, does a type cluster, how does density vary with distance.

```python
import squidpy as sq       # 1.8.3, Python >= 3.12

# adata: cells as observations, with spatial coords and a cell-type column
sq.gr.spatial_neighbors(adata, coord_type="generic", delaunay=True)
sq.gr.nhood_enrichment(adata, cluster_key="cell_type")     # who neighbours whom
sq.gr.co_occurrence(adata, cluster_key="cell_type")        # co-occurrence vs distance
sq.gr.ripley(adata, cluster_key="cell_type", mode="L")     # clustering vs dispersion
```

```
squidpy needs Python >= 3.12 (verified 2026-08). It is built for spatial
transcriptomics, but cell positions from a segmented WSI fit its data model:
put centroids in adata.obsm["spatial"] and the cell type in adata.obs.

Ripley's K (and its variance-stabilised L) tests clustering against complete
spatial randomness. Two failure modes:
  - the study region must be the TISSUE, not the slide bounding box. CSR
    over a rectangle that is half glass reports clustering that is just the
    tissue outline. Mask to tissue and use an edge correction.
  - it assumes homogeneity. Tissue is not homogeneous, so significant
    "clustering" often just reflects that cells live where tissue is. An
    inhomogeneous null or a within-region analysis is the honest comparison.

nhood_enrichment permutes cluster labels on a fixed graph, so its null is
"same graph, shuffled types". That controls for cell density but not for
tissue architecture. Read its z-scores as relative, and do not compare them
across slides with different graphs.
```

```
Point-pattern tooling if you are not in the squidpy/anndata world:
  pointpats 2.6.0   Ripley, quadrat, and nearest-neighbour statistics on
                    plain coordinate arrays. Python >= 3.12.
```

## Integration With Molecular Data

The payoff is usually correlating morphology with molecular measurements on the same tumour.

```
The registration question decides what is possible:

  SAME section       H&E and spatial transcriptomics on one slide (Visium,
                     Xenium). Coordinates are directly registrable; this is
                     the tightest link. See the spatial-transcriptomics skill.
  ADJACENT section   H&E and a molecular assay on serial cuts. Cells do NOT
                     correspond one-to-one; a cell in one section is not in
                     the next. Integrate at the REGION level, not the cell.
  SAME case, bulk    slide-level features vs bulk RNA-seq or mutation. No
                     spatial correspondence at all; correlate summaries.

Matching a per-cell H&E label to a per-spot expression value across adjacent
sections is a common and invalid shortcut. State the registration level and
integrate at the coarsest one the data honestly supports.
```

```
Confounds specific to this integration:
  - Slide-level morphology features correlate with tumour purity, and purity
    drives bulk expression. A "morphology predicts expression" result is
    often morphology predicts purity predicts expression. Adjust for purity.
  - Scanner and stain, again: if morphology and molecular data were generated
    at different sites, site is a confounder for both.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `tiles/` | PNG or a tile store | extracted tiles, named by level-0 coordinates |
| `tile_index.csv` | CSV | slide_id, level-0 x/y, level, size, mpp, tissue fraction |
| `tissue_mask.png` | PNG | binary mask at the detection level |
| `slide_manifest.csv` | CSV | slide_id, vendor, mpp-x, mpp-y, objective power, level dims |
| `stain_reference.png` | PNG | the exact reference tile used for normalization |
| `qc_flags.csv` | CSV | slides missing mpp, failed Otsu, or with extreme tissue fraction |
| `features.h5` | HDF5 | tile embeddings per slide, with level-0 coordinates alongside |
| `encoder_manifest.json` | JSON | model id, revision, embedding dim, transform config |
| `splits.csv` | CSV | slide and patient assignment per fold, with site where known |
| `attention.h5` | HDF5 | per-tile attention weights, stored as hypotheses not explanations |
| `cells.parquet` | Parquet | per-cell centroid (level-0), type, and source tile |
| `cell_density.csv` | CSV | cells per mm² by type and region |
| `spatial_stats.csv` | CSV | Ripley/co-occurrence/enrichment with the null stated |
| `regions.geojson` | GeoJSON | tumour, stroma, TLS regions with how each was defined |

Name tiles by their **level 0** coordinates and record the level and mpp beside them. A tile named by level-2 coordinates cannot be located on the slide without knowing which level produced it.

## Validation Checks

```
Reading
  location passed to read_region is scaled to level 0; size is not.
  Level chosen with get_best_level_for_downsample, never by == on a float.
  mpp-x and mpp-y both read and validated; slides missing them are flagged.
  bounds-* honoured for formats that use them.

Tiling
  Tissue detection run before tiling.
  Tissue fraction threshold recorded in the manifest.
  RGBA composited onto white, not converted straight to RGB.
  Tile coordinates stored in the level 0 frame.

Stain handling
  Reference tile recorded and reused across train and test.
  Normalization skipped for tiles below the tissue threshold.
  DAB channel not interpreted as a stain on H&E-only slides.
  Clipped channels checked when a faithful round trip matters.

Feature extraction
  Model loaded with its own timm transform, not a hand-rolled one.
  Embedding dimension read from the model, never hardcoded.
  Model id AND revision recorded; gated models authenticated explicitly.
  Licence checked before fine-tuning or deployment.

Multiple instance learning
  Splits made by PATIENT, never by tile. Site held out when available.
  Mean-pooling baseline reported beside the attention model.
  Bag construction stated: all tiles, or a subsample of fixed size.
  Attention weights presented as hypotheses, with annotation agreement
  where annotation exists.

Cell analysis
  Segmentation run at ~0.25 um/px; counts reported per mm², not per tile.
  Boundary cells deduplicated on stitched coordinates.
  Segmentation validated against a counted region, per type where classified.
  TLS distinguished from diffuse infiltration by organisation, not count.

Spatial statistics
  Study region masked to tissue, not the slide bounding box.
  Ripley/CSR inhomogeneity acknowledged; within-region or inhomogeneous null.
  Enrichment z-scores treated as relative, not compared across graphs.

Molecular integration
  Registration level stated (same section, adjacent, or bulk).
  Cell-to-spot matching not claimed across adjacent sections.
  Tumour purity adjusted for when correlating morphology with bulk expression.

Reproducibility
  Slide manifest records vendor and mpp per slide, so scanner effects can
  be tested as a covariate later.
```

## Common Pitfalls

### Reading
1. **Mixing coordinate frames in `read_region`**: `location` is level 0, `size` is the target level. The result has the right shape and the wrong content, and it only appears once you move off level 0. Scale the location by `level_downsamples[level]`.
2. **Treating `level_downsamples` as integers**: they are floats such as 4.0000123 because level dimensions round per axis. Use `get_best_level_for_downsample` rather than an equality test.
3. **Reading at a coarser level and upscaling**: `get_best_level_for_downsample` errs toward more resolution. Read finer and resize down; upscaling invents detail.
4. **Assuming `openslide.mpp-x` exists**: it is optional and absent on some slides. Validate up front and flag, rather than defaulting to 0.25 and silently mixing scales.
5. **Ignoring `bounds-*` on MIRAX slides**: the scanned region can be a small part of a much larger canvas, so most tiles are empty space.
6. **Installing only `openslide-python`**: it is a binding whose sole dependency is Pillow. Without `openslide-bin` or a system OpenSlide it fails at load.

### Scale
7. **Treating "40x" as a resolution**: nominal objective power maps to roughly 0.23-0.28 µm/px depending on scanner. Tiles from two scanners at "40x" are at different physical scales and the model learns the scanner. Work in mpp.
8. **Ignoring anisotropic pixels**: mpp-x and mpp-y can differ. Check both.

### Tiling
9. **Converting RGBA straight to RGB**: `.convert("RGB")` composites onto black, turning unscanned area into dark tissue-coloured pixels. Composite onto white explicitly.
10. **Tiling without tissue detection**: most of a slide is glass, and background tiles dominate the cohort.
11. **Not recording the tissue-fraction threshold**: ">50% tissue" and ">10% tissue" are different datasets, and the number is rarely reported.
12. **Zero overlap when stitching predictions**: objects on a boundary are split. Use overlap when the receptive field approaches the tile size.

### Stain
13. **Using `staintools`**: last released 2019-04-11 and archived on GitHub in 2021. Use `torchstain` or HistomicsTK.
14. **Expecting Vahadane from torchstain**: it ships Macenko, MultiMacenko and Reinhard only. Sparse NMF lives in HistomicsTK as `separate_stains_xu_snmf`.
15. **Not recording the stain reference tile**: every normalized value depends on it. An unrecorded reference makes the pipeline unreproducible and can shift train against test.
16. **Normalizing background tiles**: stain vectors estimated from glass are meaningless. Detect tissue first.
17. **Reading the DAB channel on an H&E slide**: `rgb2hed` always returns three channels, and the third absorbs residual. It is not DAB positivity.
18. **Assuming `rgb2hed`/`hed2rgb` round-trips**: negatives are clipped to zero, so the inverse is exact only where nothing clipped (measured: 1.1e-16 unclipped, 6.1e-01 clipped). Check for zeroed channels when it matters.

### Feature extraction
19. **Assuming the weights just download**: nearly every pathology foundation model is gated. Anonymously, `MahmoodLab/UNI` returns HTTP 401 while `owkin/phikon-v2` returns 200. Authenticate explicitly, or a collaborator hits a 401 that looks like a network fault.
20. **Ignoring the licence**: UNI, UNI2-h, CONCH and Virchow2 are CC-BY-NC-ND — non-commercial *and* no-derivatives, which on a plain reading covers a fine-tuned checkpoint. Virchow v1, Prov-GigaPath and H-optimus-0 are Apache-2.0. Check before building, not after.
21. **Hand-rolling the preprocessing transform**: each encoder ships its own input size and normalization. Substituting ImageNet constants degrades embeddings silently. Use `timm.data.create_transform` on the model's own config.
22. **Hardcoding the embedding dimension**: it is a model property (phikon 768, phikon-v2 1024). Read `model.num_features`, or a MIL head sized wrongly will crash or train on a misaligned view.
23. **Installing CTransPath beside a modern stack**: it requires a forked timm 0.5.4 from a Google Drive link while current timm is 1.0.28. Isolate it, or pick an encoder that loads from current timm.
24. **`pip install trident`**: that name on PyPI is an astrophysics package. The pathology TRIDENT installs from its git repository.

### Multiple instance learning
25. **Splitting by tile**: tiles from one slide are near-duplicates, so tile-level splits let the model memorise the slide and report accuracy that collapses on new cases. Split by patient.
26. **Splitting by slide but not patient**: one patient contributes several slides, and slides from the same block share more than biology.
27. **Ignoring site in a multi-institution cohort**: scanner and staining are site-specific, so a model can separate outcomes by learning the site. Hold out a site when the data allows.
28. **Omitting the mean-pooling baseline**: attention MIL that does not beat mean-pooled embeddings with logistic regression has not earned its complexity.
29. **Presenting attention weights as explanations**: they show what pooling up-weighted, are unstable across seeds, and are not evidence a pathologist would accept. Report them as hypotheses, with annotation agreement where it exists.
30. **Leaving background tiles in the bag**: attention is a softmax over instances, so background tiles mathematically dilute the weight on informative ones. Tissue filtering changes the optimisation, not just the runtime.

### Cell analysis
31. **Segmenting at the wrong magnification**: nuclear segmentation needs ~0.25 µm/px. Run it downsampled and small nuclei merge or vanish, silently changing the count.
32. **`pip install stardist` and expecting it to run**: it has no deep-learning backend. TensorFlow comes only via `csbdeep[tf]`, so a bare install fails at `predict`, not at install.
33. **Normalizing StarDist input with a 0–1 rescale**: the pretrained model expects `csbdeep.utils.normalize` percentile normalization. Min-max scaling degrades segmentation silently.
34. **Expecting HoVer-Net from PyPI**: it is git-only, MIT, and last updated 2023-10. Its cell types come from its training panel and may not transfer to your tumour type.
35. **Reporting cells per tile**: tile area in microns varies with mpp. Report cells per mm². Deduplicate nuclei that straddle tile boundaries.
36. **Calling a lymphocyte-rich tile a TLS**: diffuse infiltration and an organised follicle have similar counts and different spatial organisation. Distinguish by size and compactness, not density alone.

### Spatial statistics
37. **Running Ripley's K over the slide bounding box**: CSR over a rectangle that is half glass reports the tissue outline as clustering. Mask to tissue and edge-correct.
38. **Ignoring tissue inhomogeneity**: Ripley assumes homogeneity, so "clustering" often just means cells live where tissue is. Use a within-region analysis or an inhomogeneous null.
39. **Comparing `nhood_enrichment` z-scores across slides**: its null is the shuffled labels on that slide's graph. Different graphs are not comparable.

### Molecular integration
40. **Matching cells to spots across adjacent sections**: serial cuts do not share cells one-to-one. Integrate at the region level, and state the registration level explicitly.
41. **Reading morphology-expression correlation as biology**: slide morphology tracks tumour purity, and purity drives bulk expression. Adjust for purity before claiming a direct link.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): the molecular data that slide-level features are usually correlated against
- [`spatial-transcriptomics`](../spatial-transcriptomics/SKILL.md): H&E images registered to the same tissue section
- [`foundation-models`](../foundation-models/SKILL.md): the baseline discipline that applies equally to pathology encoders
- [`survival-analysis`](../survival-analysis/SKILL.md): consumes slide-level features as prognostic covariates

## Public Datasets for Testing

| Dataset | Content | Access |
|---------|---------|--------|
| OpenSlide test data | Small slides in every supported vendor format | open, openslide.cs.cmu.edu |
| TCGA diagnostic slides | ~30k H&E WSIs across tumour types | GDC portal, open |
| CAMELYON16 / 17 | Lymph node metastasis, with annotations | grand-challenge, registration |
| PANDA | Prostate biopsies with ISUP grades | Kaggle |
