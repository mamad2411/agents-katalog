---
name: data-pipeline-check
description: Validate data pipeline integrity, check dataset format compatibility, verify data quality, and diagnose data loading issues. Trigger when user mentions data problems, format conversion, dataset validation, or says "检查数据", "数据格式", "data check", "数据质量", "数据对不对", "格式兼容吗", "数据结构", "数据长什么样", "action space对得上吗", "验证数据".
---

# Data Pipeline Checker

Validate and diagnose data pipelines for ML training workflows.

## When Triggered

- User is preparing data for training
- Data format conversion needed (e.g., HDF5, JSONL, ChatML, LeRobot)
- User reports data loading errors or training data issues
- Before starting a new training run (proactive check)
- User says "检查数据", "验证数据", "数据格式对不对"

## Execution Steps

### Step 1: Dataset Discovery

Locate and catalog all datasets in the project:

```bash
# Find common ML data formats
find <project_root> -name "*.hdf5" -o -name "*.h5" -o -name "*.json" -o -name "*.jsonl" -o -name "*.parquet" -o -name "*.arrow" -o -name "*.pkl" -o -name "*.npy" -o -name "*.npz" | head -30

# Check data directories
du -sh <data_dirs>
```

Report:
```markdown
| 数据路径 | 格式 | 大小 | 文件数 |
|---------|------|------|--------|
```

### Step 2: Schema Validation

For each dataset, inspect its schema:

**HDF5 files:**
```python
import h5py
with h5py.File(path, 'r') as f:
    def print_structure(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"  {name}: shape={obj.shape}, dtype={obj.dtype}")
    f.visititems(print_structure)
```

**JSON/JSONL files:**
```python
# Check first 3 entries for schema consistency
import json
with open(path) as f:
    for i, line in enumerate(f):
        if i >= 3: break
        obj = json.loads(line)
        print(f"Entry {i}: keys={list(obj.keys())}")
```

**Image directories:**
```python
from PIL import Image
# Check image sizes, formats, and corruption
```

### Step 3: Data Quality Checks

Run these checks and report issues:

1. **Completeness**: Any missing fields, NaN values, empty entries?
2. **Consistency**: Are all entries the same schema? Are image sizes consistent?
3. **Range**: Are numeric values in expected ranges? (e.g., actions in [-1,1])
4. **Distribution**: Basic statistics (mean, std, min, max) for key fields
5. **Corruption**: Can all images be opened? Any truncated files?
6. **Splits**: Train/val/test split ratios and overlap check

### Step 4: Compatibility Check

If a training script is provided, verify compatibility:

1. **Expected vs actual format**: Does the DataLoader expect the fields present in the data?
2. **Action space alignment**: Does the model's action space match the data's action dimensions?
3. **Image resolution**: Does the data's image resolution match the model's expected input?
4. **Tokenization**: For text data, is the tokenization compatible with the model?
5. **Coordinate frames**: For robot data, are coordinate frames consistent (world vs local)?

### Step 5: Report

Output:
```markdown
## 数据管道验证报告

### 数据集概览
[Table from Step 1]

### Schema 检查
- ✅ 格式一致性: PASS
- ⚠️ 图像尺寸: 3 images have different resolution
- ❌ 缺失字段: 12 entries missing 'action' field

### 质量指标
| 字段 | 均值 | 标准差 | 最小值 | 最大值 | NaN数 |
|------|------|--------|--------|--------|-------|

### 兼容性检查
- ✅ Action space: 7-dim matches model config
- ❌ Image resolution: data=640x480, model expects=256x256

### 建议修复
1. [Specific fix with code snippet]
```

## Common Data Patterns

### Robot Trajectory Data
- HDF5 with groups: observations (images + states), actions, rewards
- Check: action dim, image channels (RGB vs BGR), state normalization

### VLM Fine-tuning Data
- JSONL with ChatML format: system/user/assistant messages
- Check: image paths exist, token lengths within model limits, balanced categories

### Multi-modal Data
- Check: modality alignment (image timestamps match action timestamps)
- Check: missing modalities in some entries

## Key Rules

1. **Never modify data without confirmation** - report issues, suggest fixes, wait for approval
2. **Sample first** - for large datasets, check a random sample (100-1000 entries)
3. **Preserve originals** - always backup before any transformation
4. **Report in Chinese** - with English field names and technical terms
