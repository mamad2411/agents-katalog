#!/usr/bin/env python3
"""mcp-guard.py — jaga MCP tetap on-demand (read-only kecuali --apply).

Aturan: MCP hanya nyala saat dipakai. Idle > 7 hari -> parkir.
Maksimum 2 MCP nyala bersamaan (di luar kebutuhan sesi).

Pakai:
  python3 mcp-guard.py            # laporan 1 baris + daftar nyala
  python3 mcp-guard.py --verbose
  python3 mcp-guard.py --apply    # parkir yang idle >7 hari (via mcp-lifecycle --gc 7)
"""
import json
import os
import subprocess
import sys
import time

AG = os.path.expanduser("~/.agents")
CFG = os.path.expanduser("~/.config/opencode/opencode.json")
USAGE = f"{AG}/mcp-usage.json"
LC = f"{AG}/mcp-lifecycle.py"
IDLE_DAYS = 7
MAX_ON = 2


def enabled_servers():
    """Sumber utama: `mamat-mcp list` (state nyata). Fallback: config opencode."""
    try:
        r = subprocess.run(["mamat-mcp", "list"], capture_output=True, text=True, timeout=10)
        on = [l.split()[1] for l in r.stdout.splitlines()
              if l.strip().startswith("ON") and len(l.split()) > 1]
        if on:
            return sorted(set(on))
    except Exception:
        pass
    try:
        d = json.load(open(CFG))
    except Exception:
        return []
    out = []
    for key in ("mcp", "mcpServers"):
        v = d.get(key)
        if isinstance(v, dict):
            for name, cfg in v.items():
                if isinstance(cfg, dict) and cfg.get("enabled") is False:
                    continue
                out.append(name)
        elif isinstance(v, list):
            out.extend(v)
    return sorted(set(out))


def usage():
    try:
        d = json.load(open(USAGE))
    except Exception:
        return {}
    return {k: v for k, v in d.items() if isinstance(v, dict)}


TOOL_HINT = {
    "ast-grep": ("ast_grep",),
    "codebase-memory": ("search_graph", "trace_path", "get_code_snippet", "query_graph",
                        "index_status", "search_code", "get_architecture", "compare_graphs"),
    "playwright": ("browser_", "playwright"),
    "better-design": ("design_", "better_design"),
    "skill-catalog": ("skill_for_task", "skill_load", "skills_available"),
}


def age_days(name, u):
    ts = u.get(name, {}).get("last_used")
    if not ts:
        hints = TOOL_HINT.get(name, ())
        best = None
        for k, v in u.items():
            if k == name or any(k.startswith(h) for h in hints) or k.startswith(name):
                t = v.get("last_used")
                if t and (best is None or float(t) > float(best)):
                    best = t
        ts = best
    if not ts:
        return None
    return (time.time() - float(ts)) / 86400


def main():
    verbose = "--verbose" in sys.argv
    apply_ = "--apply" in sys.argv
    on = enabled_servers()
    u = usage()
    idle = []
    unknown = []
    for n in on:
        a = age_days(n, u)
        if a is None:
            unknown.append(n)          # tak ada data usage: jangan auto-park
        elif a > IDLE_DAYS:
            idle.append((n, a))

    print(f"MCP nyala: {len(on)} -> {', '.join(on) or '(tidak ada)'}")
    if idle:
        print("idle >7h: " + ", ".join(f"{n}({a:.0f}h)" for n, a in idle))
    if unknown:
        print("tanpa data pakai: " + ", ".join(unknown) + " (tidak diparkir otomatis)")
    if len(on) > MAX_ON:
        print(f"PERINGATAN: {len(on)} MCP nyala — parkirkan yang tidak dipakai "
              f"(mamat-mcp off <nama>)")

    if verbose:
        for n in on:
            a = age_days(n, u)
            cnt = u.get(n, {}).get("count", "?")
            print(f"  - {n}: dipakai {cnt}x, terakhir {'tidak ada data' if a is None else f'{a:.0f} hari lalu'}")

    if apply_ and idle:
        names = [n for n, _ in idle]
        print(f"parkir: {', '.join(names)}")
        subprocess.run(["python3", LC, "--gc", str(IDLE_DAYS)], check=False)
        for n in names:
            subprocess.run(["python3", LC, "--off", n], check=False)
        print("selesai — jalankan `mamat-mcp restart` lalu buka ulang mamat")
    return 0


if __name__ == "__main__":
    sys.exit(main())
