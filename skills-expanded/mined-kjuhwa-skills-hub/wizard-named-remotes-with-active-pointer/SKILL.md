---
name: wizard-named-remotes-with-active-pointer
description: CLI config store that holds many named remote endpoints plus an "active" pointer, persisted as JSON, so users can opensre-style register/list/switch between deployments and have subsequent commands target the active one by default.
category: cli
version: 1.0.0
version_origin: extracted
tags: [config-store, cli, named-remotes, json]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/cli/wizard/store.py
imported_at: 2026-04-18T00:00:00Z
---

# Named Remotes with an Active Pointer

## When to use
Your CLI deploys to multiple environments (dev, staging, prod) or multiple cloud providers (Railway, EC2, LangSmith). Users should be able to register them by name once and then run `opensre remote ops status` against the active one without retyping the URL.

## How it works
- Single JSON file at `~/.opensre/opensre.json`.
- Top-level shape: `{version, wizard, targets, probes, remote: {url, active_name, remotes: {<name>: {url, source, updated_at}}}}`.
- `save_named_remote(name, url, set_active=True)` upserts and optionally marks active.
- `set_active_remote(name)` flips the active pointer; raises if name unknown.
- `load_active_remote_name()` returns the current default for downstream commands.
- All writes are versioned with a `_VERSION` constant so future schema migrations are detectable.

## Example
```python
def save_named_remote(name, url, *, set_active=False, source="manual", path=None):
    store_path = path or get_store_path()
    data = _load_raw(store_path)
    remotes = data.setdefault("remote", {}).setdefault("remotes", {})
    remotes[name] = {
        "url": url, "source": source,
        "updated_at": datetime.now(UTC).isoformat(),
    }
    if set_active:
        data["remote"]["url"] = url
        data["remote"]["active_name"] = name
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

def set_active_remote(name, path=None):
    store_path = path or get_store_path()
    data = _load_raw(store_path)
    entry = data.get("remote", {}).get("remotes", {}).get(name)
    if not entry or not entry.get("url"):
        raise KeyError(f"No remote named '{name}'")
    url = str(entry["url"])
    data["remote"]["url"] = url
    data["remote"]["active_name"] = name
    store_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return url
```

## Gotchas
- Keep the JSON file deeply nested with a versioned schema; a future migration is much easier than guessing flat key conventions.
- Tag each remote with a `source` (e.g. `"manual"`, `"discovered"`, `"wizard"`) so the UX can show provenance.
- Always write with `mkdir(parents=True, exist_ok=True)` since users wipe their config dir periodically.
- Print the active remote in any command's output so users don't accidentally target prod thinking they're on staging.
