---
name: pydantic-basemodel-deep-copy-versioning
description: Clone nested Pydantic configs via model_copy(deep=True) for safe per-component field overrides
category: config
version: 1.0.0
tags: [pydantic, config, deep-copy, model-architecture, python]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/OpenBMB/VoxCPM.git
source_ref: main
source_commit: 13605c5a0e6b99d6d3527a43bd1a4e0e69c8800e
source_project: VoxCPM
source_paths:
  - src/voxcpm/model/voxcpm2.py
  - src/voxcpm/model/voxcpm.py
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
---

# Clone nested Pydantic configs via model_copy(deep=True) for safe field overrides

## When to use
Use this pattern when a model has multiple sub-components (encoder, decoder, cross-attention) that share a base configuration but need differing field values (e.g., different `num_heads`, `hidden_size`). Instead of constructing separate config objects from scratch, deep-copy the shared base and override specific fields. This keeps the defaults DRY while making each component's deviations explicit.

Also needed when Pydantic `BaseModel` subclasses are defined after the base, requiring `model_rebuild()` to update forward references.

## Pattern

### Define the base config
```python
from pydantic import BaseModel
from typing import Optional

class LMConfig(BaseModel):
    hidden_size: int = 2048
    num_heads: int = 16
    num_layers: int = 24
    intermediate_size: int = 5632
    vocab_size: int = 32000
    max_position_embeddings: int = 4096
    rope_theta: float = 10000.0
    dropout: float = 0.0
```

### Deep-copy and override for sub-components
```python
class VoxCPM2Config(BaseModel):
    lm_config: LMConfig = LMConfig()
    latent_dim: int = 64
    patch_size: int = 320

    # Derived configs are created in __init__ or as a factory method
    def build_encoder_config(self) -> LMConfig:
        """Encoder shares most LM settings but has fewer layers."""
        cfg = self.lm_config.model_copy(deep=True)
        cfg.num_layers = 6          # override: encoder is shallower
        cfg.dropout = 0.1           # override: encoder uses dropout
        return cfg

    def build_cross_attn_config(self) -> LMConfig:
        """Cross-attention uses the same hidden size but fewer heads."""
        cfg = self.lm_config.model_copy(deep=True)
        cfg.num_heads = 8           # override: cross-attention has fewer heads
        cfg.intermediate_size = 2048
        return cfg
```

### Usage in model __init__
```python
class VoxCPM2Model(nn.Module):
    def __init__(self, config: VoxCPM2Config):
        super().__init__()
        self.config = config

        encoder_config    = config.build_encoder_config()
        cross_attn_config = config.build_cross_attn_config()

        self.encoder    = TransformerEncoder(encoder_config)
        self.cross_attn = CrossAttentionBlock(cross_attn_config)
        self.lm         = LanguageModel(config.lm_config)
```

### model_rebuild() after subclass definitions
Pydantic V2 requires `model_rebuild()` when a model references another model defined later in the file, or after you've monkey-patched a `BaseModel` subclass:

```python
# Define all subclasses first
class LoRAConfigV2(BaseModel):
    r: int = 8
    alpha: float = 16.0
    enable_lm: bool = True
    enable_dit: bool = True
    enable_proj: bool = False

# Then rebuild the parent to resolve forward references
VoxCPM2Config.model_rebuild()
```

### Serialization round-trip
```python
# Save
cfg_dict = config.model_dump()
with open("config.json", "w") as f:
    json.dump(cfg_dict, f, indent=2)

# Load
with open("config.json") as f:
    data = json.load(f)
config = VoxCPM2Config(**data)
# Nested configs are re-instantiated automatically by Pydantic
```

## Source reference
- Upstream: `OpenBMB/VoxCPM` @ `main` / `13605c5a`
- Key files:
  - `src/voxcpm/model/voxcpm2.py:91-142` — `VoxCPM2Config` with deep-copy pattern and `model_rebuild()` calls
  - `src/voxcpm/model/voxcpm.py:99-142` — V1 equivalent

## Notes
- `model_copy(deep=True)` is Pydantic V2 API; in Pydantic V1 use `.copy(deep=True)`.
- Mutating a shallow copy (`model_copy(deep=False)`) will mutate nested objects in the original — always use `deep=True` when overriding nested fields.
- `model_rebuild()` is a class method and is idempotent; safe to call multiple times.
