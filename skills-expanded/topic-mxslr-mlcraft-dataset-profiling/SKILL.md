---
name: dataset-profiling
description: "Use as the FIRST step of any ML task, before choosing a model, to inspect and understand the actual dataset. Works for a LOCAL dataset (Claude reads the files directly) and for a KAGGLE dataset (Claude cannot read /kaggle/input from your machine, so it emits a small profiling cell you run on Kaggle and paste back, or downloads via the Kaggle API). Profiles structure, size, modality, schema, class balance, the entity for group splitting, and any official split. Triggers on 'my dataset', 'data is on kaggle', 'CSV', 'data folder', 'profile the data', 'what does the dataset look like', 'EDA', 'explore the data'."
---

# Dataset Profiling (understand the data first)

Never choose a model, metric, or split before inspecting the actual data. The profile drives every later decision.

## Where is the data? Pick the access path.

| Situation | How the assistant sees the data |
|---|---|
| Local files (a folder or CSV on this machine) | The assistant reads them directly with its file tools. Ask for the path. |
| Kaggle dataset (only on Kaggle) | The assistant CANNOT read `/kaggle/input` from your machine. Use option A or B below. |
| Google Colab (data in Drive) | Mount Drive, then treat it as local. |

`/kaggle/input` exists only inside a Kaggle kernel. During a Commit the notebook code reads it; the assistant running on your machine cannot.

### Kaggle option A (recommended, no download): run a profiling cell, paste the output back
Emit this cell for the user to run on Kaggle, then use the printed summary to decide method, metric, and split:
```python
import glob, os, pandas as pd
base = '/kaggle/input'
print('TREE (top levels):')
for r, d, f in os.walk(base):
    depth = r[len(base):].count(os.sep)
    if depth <= 2:
        print('  ' * depth, os.path.basename(r) or r, f'[{len(f)} files]')
for c in glob.glob(base + '/**/*.csv', recursive=True)[:5]:
    df = pd.read_csv(c, nrows=5)
    print('\nCSV', c, df.shape, list(df.columns))
    print(df.head(3).to_string())
imgs = glob.glob(base + '/**/*.jp*g', recursive=True) + glob.glob(base + '/**/*.png', recursive=True)
print('\nimage files:', len(imgs))
```
Ask the user to paste the output, then extend the cell as needed (class counts, image sizes, label joins).

### Kaggle option B: download locally with the Kaggle API
If the user has a `kaggle.json` token: `kaggle datasets download -d <owner/dataset>` (or `kaggle competitions download -c <name>`), unzip, then profile the local folder directly.

## What to profile (by modality)
- Tabular: shape, column dtypes, missing percentage, target distribution, high-cardinality columns, and columns that could leak the label.
- Images: count per class, image sizes and aspect ratios, color vs grayscale, corrupt files, folder layout, and a few sample views.
- Text: length distribution, label balance, duplicates, and language.
- Time-series: sampling frequency, gaps, time range, and count per series.
- Audio: sample rate, clip duration, and count per class.

## Always determine (these decide correctness)
- The ENTITY for a group split (patient, user, scene, document) so `data-rigor-and-leakage` can prevent leakage.
- Any OFFICIAL train and test split (often encoded in file names or a provided split file).
- Class balance and dataset size, which drive model capacity and augmentation.

## Output
A short data profile: modality, size, schema or class counts, the split entity, the official split if any, and quality issues. Hand it to `data-rigor-and-leakage` for the split, then to the matching domain skill for the method.
