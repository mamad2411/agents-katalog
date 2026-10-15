#!/usr/bin/env python3
"""aggressive-scan.py — bounded aggressive sweep (no giant-file hang).

Merges:
  - scan-code.json findings (already computed)
  - fresh md scan of skills-expanded / skills-store / repo-refs for
    exec-download, prompt-injection, secret-exfil, hidden-unicode

Quarantine (reversible). Skips root-level tooling + files > 512KB.
"""
import os, re, json, shutil, time

BASE = os.path.dirname(os.path.abspath(__file__))
QUAR = os.path.join(BASE, "quarantine")
MANIFEST = os.path.join(QUAR, "manifest.json")
MAX = 512_000
SKIP_DIR = {'.git','node_modules','.dupes','quarantine','.venv','venv','site-packages',
            'dist','build','.next','__pycache__','.cache','vendor','target','.tox'}
SCAN_DIRS = ('skills-expanded', 'skills-store', 'repo-refs', 'cap-store', 'skills')

PATS = [
    ("exec-download", re.compile(r"(curl[^\n|]{0,200}\|\s*(ba)?sh|wget[^\n|]{0,200}\|\s*(ba)?sh|iwr[^\n|]{0,200}\|\s*iex|Invoke-Expression|DownloadString|FromBase64String|/dev/tcp/\d|base64\s+-d\s*\|\s*(ba)?sh)", re.I)),
    ("prompt-injection", re.compile(r"(ignore (all )?(previous|prior|above) instructions|disregard (your|all) (rules|instructions)|you are now|new system prompt|jailbreak)", re.I)),
    ("secret-exfil", re.compile(r"(send|upload|post|exfiltrate|leak)[^\n]{0,40}(api[ _-]?key|token|password|secret|credential|\.env|ssh)", re.I)),
    ("hidden-unicode", re.compile(r"[\u200b\u200c\u200d\u2060\ufeff\u202a-\u202e]")),
]

def walk(root):
    for r, ds, fs in os.walk(root):
        ds[:] = [d for d in ds if d not in SKIP_DIR]
        for f in fs:
            if f.lower().endswith('.md'):
                yield os.path.join(r, f)

def main():
    seen = {}
    # 1) existing code findings
    cp = os.path.join(BASE, "scan-code.json")
    if os.path.exists(cp):
        for f in json.load(open(cp)):
            seen[f["path"]] = f["reasons"]
    # 2) fresh md sweep
    t0 = time.time(); n = 0
    for d in SCAN_DIRS:
        root = os.path.join(BASE, d)
        if not os.path.isdir(root): continue
        for p in walk(root):
            n += 1
            if n % 20000 == 0: print(f"  ...{n} ({time.time()-t0:.0f}s)", flush=True)
            try:
                if os.path.getsize(p) > MAX: continue
                txt = open(p, 'r', errors='ignore').read(131072)
            except Exception:
                continue
            reasons = [name for name, rx in PATS if rx.search(txt)]
            if reasons:
                rel = os.path.relpath(p, BASE)
                seen.setdefault(rel, [])
                seen[rel] = sorted(set(seen[rel]) | set(reasons))
    print(f"md dipindai: {n} ({time.time()-t0:.0f}s)")

    findings = [{"path": k, "tier": 2, "reasons": v,
                 "size": os.path.getsize(os.path.join(BASE, k)) if os.path.exists(os.path.join(BASE, k)) else 0}
                for k, v in seen.items()]
    # jangan buang tooling/infra sendiri (file di root ~/.agents tanpa '/')
    findings = [f for f in findings if "/" in f["path"]]
    findings.sort(key=lambda x: -x["size"])
    json.dump(findings, open(os.path.join(BASE, "scan-aggressive.json"), "w"), indent=1)

    byr = {}
    for f in findings:
        for r in f["reasons"]: byr[r] = byr.get(r, 0) + 1
    print(f"TOTAL kena: {len(findings)}  per alasan: {dict(sorted(byr.items(), key=lambda x:-x[1]))}")

    moved = []
    DRY = "--dry" in os.sys.argv
    for f in findings:
        if DRY: break
        src = os.path.join(BASE, f["path"]); dst = os.path.join(QUAR, f["path"])
        if not os.path.exists(src): continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try: shutil.move(src, dst); moved.append(f)
        except Exception as e: print("  ! ", f["path"], e)
    prev = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else []
    json.dump(prev + moved, open(MANIFEST, "w"), indent=1)
    print(f"QUARANTINE: {len(moved)} file dipindah")

if __name__ == "__main__":
    main()
