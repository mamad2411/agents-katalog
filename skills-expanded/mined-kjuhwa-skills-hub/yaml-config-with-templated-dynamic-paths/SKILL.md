---
name: yaml-config-with-templated-dynamic-paths
description: Load experiment config from YAML, then auto-resolve dependent paths via templates like "{base}/{exp_name}/tokenizer/best_model" unless the user overrides.
category: configuration
tags: [yaml, config-loader, templating, ml-experiments, path-resolution]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/shiyu-coder/Kronos.git
source_ref: master
source_commit: 67b630e67f6a18c9e9be918d9b4337c960db1e9a
source_project: Kronos
source_paths: [finetune_csv/config_loader.py, finetune_csv/configs/config_ali09988_candle-5min.yaml]
version: 1.0.0
version_origin: extracted
imported_at: 2026-04-18T00:00:00Z
---

# YAML config with auto-derived paths that stay overridable

## When to use
- You run many experiments, each with its own `exp_name`, where 90% of the output paths are `{base_path}/{exp_name}/...` and should just be derived automatically.
- You still want to allow a specific experiment to override any single path to point at a shared artifact.
- You want one `config.yaml` to capture data paths, training hyperparams, device, and distributed settings in one place — not scattered across a Python `Config()` class and CLI flags.

## Pattern
After `yaml.safe_load`, walk a small `path_templates` dict and fill in each path by one of three rules: (1) template string if the user left the key empty (`""` or `None`), (2) user's string if it contains `{exp_name}` (do a `.format`), (3) user's string verbatim. Expose flat getters (`get_data_config`, `get_training_config`, …) and a typed wrapper that bundles everything into one object.

```python
# finetune_csv/config_loader.py
def _resolve_dynamic_paths(self, config):
    exp_name  = config.get('model_paths', {}).get('exp_name', '')
    if not exp_name: return config
    base_path = config.get('model_paths', {}).get('base_path', '')
    path_templates = {
        'base_save_path':       f"{base_path}/{exp_name}",
        'finetuned_tokenizer':  f"{base_path}/{exp_name}/tokenizer/best_model",
    }
    for key, template in path_templates.items():
        if key in config['model_paths']:
            current = config['model_paths'][key]
            if current in ("", None):
                config['model_paths'][key] = template
            elif isinstance(current, str) and '{exp_name}' in current:
                config['model_paths'][key] = current.format(exp_name=exp_name)
    return config
```

The YAML shows both escape hatches side by side:

```yaml
# configs/config_ali09988_candle-5min.yaml
model_paths:
  exp_name:  "HK_ali_09988_kline_5min_all"
  base_path: "/xxx/Kronos/finetune_csv/finetuned/"
  base_save_path: ""                                          # way 1: auto-derived
  # finetuned_tokenizer: "/xxx/{exp_name}/tokenizer/best_model"   # way 2: template override
```

## Why it works / tradeoffs
Writers default to the convention (empty string → templated path) but power users can point at someone else's checkpoint with a literal. Storing `exp_name` + `base_path` at the top keeps paths diffable across experiments. The "empty string means use template" choice is a small gotcha — an accidental null could silently generate a wrong path — so prefer explicit `""` and document it. For deeper hierarchies, consider a library like Hydra, but this 50-line helper is often enough.

## References
- `finetune_csv/config_loader.py` in Kronos — `ConfigLoader._resolve_dynamic_paths`, `CustomFinetuneConfig`
- `finetune_csv/configs/config_ali09988_candle-5min.yaml` — example with both override styles
