# LandmarkLocator — Claude Code Project Instructions

## Project Purpose
A deep learning sub-project within the mapThemVeins suite. Trains a heatmap-based landmark detection model to locate anatomical keypoints in *Drosophila* wing brightfield images — hinge landmarks (subcostal break, alula notch, L1/Rs junction, L4/L5 junction) and wing tip (L3 at distal edge). These landmarks define the hinge line and wing length, and anchor downstream vein identification in `identifyFeatures`.

## Relationship to other modules
LandmarkLocator produces a trained model that `preprocessing` loads as Stage 1, then passes the resulting landmarks GeoJSON to `HingeChopper` (Stage 2) and `identifyFeatures` (the analysis stage in TRACE). LandmarkLocator imports nothing from sibling modules at runtime.

## Architecture
Single-stage pipeline: full-wing heatmap regression (no canonicalization or cropping). ResNet18-encoder U-Net predicts one Gaussian heatmap per landmark directly on the resized input image.

```
LandmarkLocator/
├── landmark_locator/    # Installable Python package (pip install -e .)
│   ├── __init__.py      # Public API: LandmarkPredictor, predict_ensemble, etc.
│   ├── data/            # Dataset, augmentation, heatmap generation
│   │   ├── dataset.py   # LandmarkDataset, GeoJSON parsing, heatmap rendering
│   │   └── augmentation.py  # Train/val transform pipelines (albumentations)
│   ├── models/          # Neural network definitions
│   │   └── unet.py      # LandmarkUNet (ResNet18 encoder + decoder)
│   ├── training/        # Training loops, loss functions
│   │   ├── train.py     # CV splits, training orchestrator, evaluation
│   │   └── losses.py    # HeatmapMSELoss
│   ├── inference/       # Prediction pipeline
│   │   └── predict.py   # LandmarkPredictor, ensemble prediction
│   └── scripts/         # CLI entry points & GUI
│       ├── train.py     # landmark-train CLI
│       ├── predict.py   # landmark-predict CLI
│       ├── visualize.py # landmark-visualize CLI
│       └── gui.py       # PyQt5 GUI
├── configs/
│   └── default.yaml     # All hyperparameters
├── training_data/       # GeoJSON Point annotations (24 files)
├── training_data_pics/  # TIFF images (24 files, 5440×3648)
├── pyproject.toml       # Package metadata & build config
├── setup.py             # Editable install shim for older pip
├── CLAUDE.md
└── requirements.txt
```

## Key Landmarks (5 channels, canonical order)
| Channel | Landmark | Description |
|---------|----------|-------------|
| 0 | subcostal_break | Where the subcosta vein ends on the anterior margin |
| 1 | alula_notch | Indentation on the posterior margin at the hinge |
| 2 | l1_rs_junction | Where L1 meets the fused L2/L3 (radial sector) |
| 3 | l4_l5_junction | Where L4 and L5 diverge in the hinge region |
| 4 | wing_tip | Where L3 meets the distal wing edge |

## Annotation Format
GeoJSON FeatureCollection with Point features. One `.geojson` file per image in `training_data/`.
```json
{"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]},
 "properties": {"classification": {"name": "subcostal break"}}}
```
GeoJSON names → internal: `"subcostal break"` → `subcostal_break`, `"alula notch"` → `alula_notch`, `"L1-Rs"` → `l1_rs_junction`, `"L4-L5"` → `l4_l5_junction`, `"DTip"` → `wing_tip`.

**Known anomaly**: `PknCG736-lacZ_engal4_BL12322_0007.tif.geojson` has a MultiPoint geometry for DTip — parser takes first coordinate.

## Model Details
- **Encoder**: Pretrained ResNet18, features at 5 scales (stride 2/4/8/16/32)
- **Decoder**: 4 DecoderBlocks (upsample 2× → concat skip → 2×conv+BN+ReLU), final upsample to input size
- **Output**: (B, 5, 352, 512) — no activation, raw heatmaps
- **Input**: 512×352 (aspect ratio ~1.45:1, divisible by 32), ImageNet-normalized RGB

## Training Details
- **Heatmap targets**: Gaussian blobs (sigma=5px at model resolution) centered on landmark coordinates
- **Augmentation**: rotation ±30°, horizontal flip, scale ±15%, brightness/contrast, Gaussian blur, coarse dropout. Keypoints co-transformed via albumentations, heatmaps rendered after all transforms.
- **Loss**: MSE on heatmaps (HeatmapMSELoss with optional per-channel mask)
- **Optimizer**: AdamW (lr=1e-3, wd=1e-4), cosine LR schedule
- **Encoder freeze**: first 20 epochs, then unfreeze with 0.1× LR
- **CV**: 5-fold stratified by genotype, early stopping patience 50
- **Confidence**: peak value of predicted heatmap
- **Device**: auto-detect MPS (Apple Silicon) > CUDA > CPU

## Data
- 24 TIFF images (5440×3648, BGR uint8) in `training_data_pics/`
- 24 GeoJSON annotations in `training_data/`
- 3 genotype groups: CTRL (9), PknCG736 (10), en-PknRNAi (5)
- All coordinates in pixel space (origin top-left)

## Key Dependencies
- `torch`, `torchvision` — model training/inference, pretrained backbone
- `numpy`, `opencv-python` — image I/O and processing
- `albumentations` — augmentation pipeline with keypoint co-transforms
- `scikit-learn` — StratifiedKFold for CV splits
- `pyyaml` — config loading

## Conventions
- All image arrays are numpy (H, W, 3) uint8 BGR for OpenCV compatibility
- Model input tensors are (B, C, H, W) float32 normalized with ImageNet stats
- Do not hardcode file paths; use pathlib.Path throughout
- All public functions have type hints and a one-line docstring
- Coordinate convention: (x, y) in pixel space, origin top-left, matching OpenCV
