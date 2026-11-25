---
name: local-vs-remote-reachability-probes
description: Lightweight probe dataclass that checks both local-target writability (dir + parent walk) and remote-target HTTP reachability with a 3-second timeout, returning a typed result the wizard can render uniformly.
category: cli
version: 1.0.0
version_origin: extracted
tags: [cli, probes, reachability, dataclass]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/cli/wizard/probes.py
imported_at: 2026-04-18T00:00:00Z
---

# Local vs Remote Reachability Probes

## When to use
Your CLI's onboarding wizard needs to confirm that (a) the local config dir is writable, and (b) the hosted backend URL is reachable, both in under 3 seconds, and surface the same result type for both.

## How it works
- `ProbeResult(target, reachable, detail)` is a frozen dataclass with `as_dict()` for JSON serialization.
- `probe_local_target` checks `os.access(path, os.W_OK)` and walks up to the first existing parent if the target file doesn't exist yet.
- `probe_remote_target` does a `urllib.request.urlopen(url, timeout=3.0)` and treats `2xx-4xx` as reachable (because a 401/404 still proves the host is up).
- Both return the same shape so the wizard renders them uniformly.

## Example
```python
@dataclass(frozen=True)
class ProbeResult:
    target: str
    reachable: bool
    detail: str
    def as_dict(self): return asdict(self)

def _is_writable(path: Path) -> bool:
    if path.exists(): return os.access(path, os.W_OK)
    parent = path.parent
    while not parent.exists() and parent != parent.parent:
        parent = parent.parent
    return os.access(parent, os.W_OK)

def probe_local_target(store_path: Path) -> ProbeResult:
    writable = _is_writable(store_path) and _is_writable(PROJECT_ENV_PATH)
    return ProbeResult(target="local", reachable=writable,
                       detail=f"Local config targets: {store_path} and {PROJECT_ENV_PATH}")

def probe_remote_target(timeout_seconds=3.0) -> ProbeResult:
    url = get_tracer_base_url()
    try:
        with urlopen(Request(url, method="GET"), timeout=timeout_seconds) as response:
            status = getattr(response, "status", 200)
            return ProbeResult("remote", 200 <= status < 500,
                               f"reachable at {url} (HTTP {status})")
    except URLError as err:
        return ProbeResult("remote", False, f"unreachable at {url}: {err.reason}")
```

## Gotchas
- A 4xx response still means the host is online — treat `200..499` as "reachable" so corporate firewalls that return 403 for anonymous GETs still pass the probe.
- For local probes, walk to the first existing parent to support the "config dir doesn't exist yet" case.
- Always use a short timeout (≤3s) so the wizard doesn't hang for a minute on a misconfigured corp proxy.
