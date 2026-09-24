#!/usr/bin/env python3
"""MCP Lifecycle Manager — MCP cuma nyala saat dipakai, idle otomatis mati.

Konsep (tanpa daemon berat):
- usage log: ~/.agents/mcp-usage.json  {server: {last_used, count}}
- enable set  : server 'aktif' (masuk config provider)   <= yang dipakai
- disable set : server 'parkir' (disimpan di mcp-parked.json, TIDAK di config)
- activate/deactivate manual: --on <name> / --off <name>
- --gc N : parkir otomatis server tak terpakai > N hari
- --on-demand : cek usage log lalu nyalakan yang diminta, parkir sisanya

Ringan: stdlib only, jalan saat dibutuhkan, bukan 24 jam.
"""
import json, os, sys, time, shutil

AGENTS = os.path.expanduser("~/.agents")
USAGE_F = os.path.join(AGENTS, "mcp-usage.json")
PARKED_F = os.path.join(AGENTS, "mcp-parked.json")

CONFIGS = {  # provider -> (file, wrapper_key)
    "claude":   (os.path.expanduser("~/.claude.json"), "mcpServers"),
    "codex":    (os.path.expanduser("~/.codex/config.toml"), None),  # toml: skip
    "gemini":   (os.path.expanduser("~/.gemini/settings.json"), "mcpServers"),
    "codebuddy":(os.path.expanduser("~/.codebuddy/mcp.json"), "mcpServers"),
    "windsurf": (os.path.expanduser("~/.windsurf/mcp.json"), "mcpServers"),
    "continue": (os.path.expanduser("~/.continue/mcp.json"), "mcpServers"),
    "aider":    (os.path.expanduser("~/.aider/mcp.json"), "mcpServers"),
    "opencode": (os.path.expanduser("~/.opencode/mcp.json"), "mcpServers"),
    "hermes":   (os.path.expanduser("~/.hermes/mcp.json"), "mcpServers"),
    "copilot":  (os.path.expanduser("~/.copilot/mcp.json"), "mcpServers"),
    "roo":      (os.path.expanduser("~/.roo/mcp.json"), "mcpServers"),
    "cline":    (os.path.expanduser("~/.cline/mcp.json"), "mcpServers"),
}

def load(p, default):
    try: return json.load(open(p))
    except Exception: return default

def save(p, d):
    shutil.copy2(p, p + ".bak-lifecycle") if os.path.exists(p) else None
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)

def usage(): return load(USAGE_F, {})
def parked(): return load(PARKED_F, {})

def record(server):
    u = usage(); e = u.get(server, {"count": 0, "last_used": 0})
    e["count"] += 1; e["last_used"] = time.time(); u[server] = e
    save(USAGE_F, u); print(f"[usage] {server}: count={e['count']}")

def activate(name):
    """Pindahkan server dari parked ke config JSON provider."""
    p = parked()
    if name not in p:
        print(f"'{name}' tidak ada di parkiran. Tersedia: {', '.join(sorted(p)) or '(kosong)'}"); return
    cfg = p.pop(name)
    for prov, (f, key) in CONFIGS.items():
        if not key or not os.path.exists(f): continue
        d = load(f, {}); d.setdefault(key, {})
        if name in d[key]: continue
        d[key][name] = cfg; save(f, d)
    save(PARKED_F, p); print(f"[ON] {name} -> {sum(1 for _,(f,k) in CONFIGS.items() if k) } provider JSON")

def deactivate(name):
    """Parkirkan: hapus dari semua config JSON, simpan di mcp-parked.json."""
    p = parked(); found = None
    for prov, (f, key) in CONFIGS.items():
        if not key or not os.path.exists(f): continue
        d = load(f, {})
        if name in d.get(key, {}):
            found = d[key].pop(name); save(f, d)
    if found is None:
        print(f"'{name}' tidak ditemukan aktif di config JSON mana pun."); return
    p[name] = found; save(PARKED_F, p)
    print(f"[OFF] {name} diparkir (tidak jalan, bisa --on kapan saja)")

def keep_set():
    """Server yang selalu nyala (core): mcp-allowlist.txt + skill-catalog."""
    keep = {"skill-catalog"}
    af = os.path.join(AGENTS, "mcp-allowlist.txt")
    if os.path.exists(af):
        keep |= {l.strip() for l in open(af) if l.strip() and not l.startswith("#")}
    return keep

def gc(days):
    """Parkir semua server yang tak terpakai > N hari (batch, tanpa nulis berulang).

    Bootstrap grace: server aktif yang belum punya entri usage dianggap baru
    dipasang (last_used = sekarang) supaya GC tidak membantai hari ini.
    """
    u = usage(); cutoff = time.time() - days * 86400; off = 0
    keep = keep_set()
    active = []
    for f, key in [c for c in CONFIGS.values() if c[1] and os.path.exists(c[0])]:
        active += list(load(f, {}).get(key, {}).keys())
    victims = []
    for name in sorted(set(active)):
        if name in keep: continue  # core selalu hidup
        e = u.get(name)
        if not e:
            e = u[name] = {"count": 0, "last_used": time.time()}  # grace bootstrap
        if e.get("last_used", 0) < cutoff:
            victims.append(name)
    for name in victims:
        deactivate(name); off += 1
    save(USAGE_F, u)
    print(f"[KEEP] core selalu-on: {len(keep)}")
    print(f"[GC] {off} server diparkir (tidak dipakai > {days} hari). Total parkiran: {len(parked())}")

def gc_if_due(days=14, max_files_per_pass=200):
    """Cek murah untuk tiap sesi: GC beneran maks 1x/7 hari, kalau jalan
    proses maks N file per pass supaya ringan. Return True kalau ada aksi."""
    state_f = os.path.join(AGENTS, ".gc-state.json")
    st = load(state_f, {})
    now = time.time()
    if now - st.get("last_gc", 0) < 7 * 86400:
        return False
    # hitung victim dulu (tanpa menulis) — kalau 0, cukup tandai terkunci
    u = usage(); cutoff = now - days * 86400; keep = keep_set()
    active = []
    for f, key in [c for c in CONFIGS.values() if c[1] and os.path.exists(c[0])]:
        active += list(load(f, {}).get(key, {}).keys())
    victims = []
    for name in sorted(set(active)):
        if name in keep: continue
        e = u.get(name)
        if e and 0 < e.get("last_used", 0) < cutoff:
            victims.append(name)
        elif not e:
            u[name] = {"count": 0, "last_used": now}  # grace bootstrap (sekali saja)
    save(USAGE_F, u)
    if not victims:
        st["last_gc"] = now; save(state_f, st); return False
    for name in victims[:max_files_per_pass]:
        deactivate(name)
    st["last_gc"] = now; save(state_f, st)
    print(f"[GC-IF-DUE] {len(victims[:max_files_per_pass])} diparkir "
          f"(sisa {max(0, len(victims)-max_files_per_pass)} untuk pass berikutnya)")
    return True

def status():
    u, p = usage(), parked(); now = time.time()
    tools = {k: v for k, v in u.items() if not k.startswith("_") and isinstance(v, dict)}
    act = []
    for f, key in [c for c in CONFIGS.values() if c[1] and os.path.exists(c[0])]:
        act += list(load(f, {}).get(key, {}).keys())
    print(f"AKTIF (nyala)   : {len(set(act))}")
    print(f"PARKIR (mati)   : {len(p)}")
    hot = sorted(tools.items(), key=lambda x: -x[1].get("count", 0))[:10]
    print("Top dipakai     :", ", ".join(f"{n}({e['count']}x)" for n, e in hot) or "-")
    cold = [n for n, e in tools.items() if e.get("last_used") and now - e["last_used"] > 14*86400]
    if cold: print("Kandidat parkir :", ", ".join(sorted(cold)[:15]), "(>14 hari) -> python3 mcp-lifecycle.py --gc 14")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--record" in a: record(a[a.index("--record")+1])
    elif "--on" in a: activate(a[a.index("--on")+1])
    elif "--off" in a: deactivate(a[a.index("--off")+1])
    elif "--gc" in a: gc(int(a[a.index("--gc")+1]))
    elif "--gc-if-due" in a:
        d = int(a[a.index("--gc-if-due")+1]) if len(a) > a.index("--gc-if-due")+1 else 14
        gc_if_due(d)
    else: status()
