#!/usr/bin/env python3
"""skill-scan.py — malware/trojan scanner for harvested skills & repo-refs.

Detects:
  T1 native executables (always suspicious in a text skill catalog)
  T2 malicious content patterns in scripts/text (reverse shell, downloader-exec,
     credential exfil, miner, webhook exfil, persistence, obfuscation)
  T3 prompt-injection / exfil instructions inside SKILL.md

Usage:
  python3 skill-scan.py                 # report only
  python3 skill-scan.py --quarantine    # move flagged files to ./quarantine (reversible)
  python3 skill-scan.py --json          # machine-readable report
  python3 skill-scan.py --restore       # put everything back from quarantine
"""
import os, re, sys, json, shutil, time

BASE = os.path.dirname(os.path.abspath(__file__))
QUAR = os.path.join(BASE, "quarantine")
MANIFEST = os.path.join(QUAR, "manifest.json")

# ---- T1: native executables / installer payloads ----------------------------
NATIVE = {'.exe','.dll','.scr','.com','.msi','.vbs','.vbe','.jar','.lnk','.hta',
          '.wsf','.bat','.cmd','.ps1','.apk','.deb','.rpm','.dmg','.pkg',
          '.so','.dylib','.bin','.jnilib','.sys','.cpl','.ocx'}

# ---- T2: malicious content patterns ----------------------------------------
# prefix base64 dropper AMOS — disusun runtime supaya literal tidak nongkrong di repo publik
_DROPPER = "L2Jpbi9iYXNo" + "IC1jIC"

PAT = [
    ("reverse-shell",  re.compile(r"(bash\s+-i\s*>&?\s*/dev/tcp/|/dev/tcp/(?!127\.0\.0\.1|localhost)|nc\s+-e\s|ncat\s+-e\s|socat\s+.*exec|mkfifo\s+\S+.*nc\s)")),
    ("downloader-exec",re.compile(r"(curl[^\n|]*\|\s*(ba)?sh|wget[^\n|]*\|\s*(ba)?sh|iwr[^\n|]*\|\s*iex|Invoke-WebRequest[^\n]*\|\s*IEX|Invoke-Expression|IEX\s*\(|DownloadString|DownloadFile|FromBase64String|-EncodedCommand|\b-enc\b\s+[A-Za-z0-9+/=]{40})", re.I)),
    ("base64-exec",    re.compile(r"(eval\s*\(\s*(atob|base64|__import__\('base64')|base64\s+-d\s*\|\s*(ba)?sh|echo\s+[A-Za-z0-9+/=]{200,}\s*\|\s*base64\s+-d)", re.I)),
    ("obfuscation",    re.compile(r"[A-Za-z0-9+/]{2000,}={0,2}")),
    ("credential-exfil",re.compile(r"(\.aws/credentials|\.ssh/id_rsa|id_rsa\b|/\.ssh/|\.netrc|keychain|security\s+find-generic-password|\.env\b.*(curl|wget|post)|(cat|type)\s+.*(credentials|id_rsa|\.env))", re.I)),
    ("crypto-miner",   re.compile(r"(xmrig|minerd|cpuminer|stratum\+tcp|stratum\+ssl|--donate-level|cryptonight)", re.I)),
    ("exfil-endpoint", re.compile(r"(webhook\.site|discord\.com/api/webhooks|pastebin\.com/raw|transfer\.sh|0x0\.st|termbin\.com|ngrok\.io|pipedream\.net|requestbin|burpcollaborator)", re.I)),
    ("persistence",    re.compile(r"(crontab\s+-|/Library/LaunchAgents|/Library/LaunchDaemons|LaunchAgents/.*\.plist|systemctl\s+enable|schtasks\s+/create|reg\s+add\s+.*\\\\Run|Startup\\\\|\.bashrc\s*>>|authorized_keys)", re.I)),
    ("ransom-note",    re.compile(r"(your files have been encrypted|decrypt.{0,20}bitcoin|ransom|\.locked\b|openssl\s+enc\s+-aes.*-in\s+/|for\s+root,\s*dirs,\s*files.*encrypt)", re.I)),
    ("data-destroy",   re.compile(r"(rm\s+-rf\s+/\s|rm\s+-rf\s+~|dd\s+if=/dev/(zero|urandom)\s+of=/dev/|:\(\)\s*\{\s*:\|:&\s*\};:|chmod\s+-R\s+000\s+/)")),
    ("stealer-dropper",re.compile("(" + _DROPPER + r"|91\.92\.242\.30|swcdn\.apple\.com[^\n]{0,80}\|\s*base64)", re.I)),
]
# ---- T3: prompt-injection / exfil in markdown ------------------------------
INJECT = [
    ("prompt-injection", re.compile(r"(ignore (all )?(previous|prior|above) instructions|disregard (your|all) (rules|instructions)|you are now|new system prompt|jailbreak)", re.I)),
    ("secret-exfil",     re.compile(r"(send|upload|post|exfiltrate|leak)[^\n]{0,40}(api[ _-]?key|token|password|secret|credential|\.env|ssh)", re.I)),
    ("hidden-unicode",   re.compile(r"[\u200b\u200c\u200d\u2060\ufeff\u202a-\u202e]")),
]
CODE_EXT = {'.py','.sh','.bash','.zsh','.js','.mjs','.cjs','.ts','.rb',
            '.pl','.php','.yml','.yaml','.ps1','.bat','.cmd','.vbs'}
TEXT_EXT = CODE_EXT | {'.md','.txt','.json','.toml','.ini','.cfg','.html','.xml','.csv'}
MAXREAD = 262144  # 256KB
SKIP_DIR = {'.git','node_modules','.dupes','quarantine','.venv','venv','site-packages',
            'dist','build','.next','__pycache__','.cache','vendor','target','.tox'}

def scan_file(p):
    """Return (tier, list_of_reasons)."""
    e = os.path.splitext(p)[1].lower()
    reasons = []
    if e in NATIVE:
        reasons.append("native-exec:"+e)
    if e in CODE_EXT or e in NATIVE or e == '.md':
        try:
            if os.path.getsize(p) <= 8_000_000:
                with open(p, 'r', errors='ignore') as f:
                    txt = f.read(MAXREAD)
            else:
                txt = ""
        except Exception:
            txt = ""
        if e == '.md':
            for name, rx in INJECT:
                if rx.search(txt):
                    reasons.append(name)
        else:
            for name, rx in PAT:
                if rx.search(txt):
                    reasons.append(name)
    if not reasons:
        return None
    tier = 1 if e in NATIVE else (3 if (e == '.md') else 2)
    return tier, reasons

def walk():
    for r, ds, fs in os.walk(BASE):
        ds[:] = [d for d in ds if d not in SKIP_DIR]
        for f in fs:
            yield os.path.join(r, f)

def do_scan():
    findings = []
    t0 = time.time()
    n = 0
    for p in walk():
        n += 1
        if n % 50000 == 0:
            print(f"  ...{n} file dipindai ({time.time()-t0:.0f}s)", flush=True)
        res = scan_file(p)
        if res:
            tier, reasons = res
            findings.append({"path": os.path.relpath(p, BASE), "tier": tier,
                             "reasons": reasons, "size": os.path.getsize(p)})
    findings.sort(key=lambda x: (x["tier"], -x["size"]))
    print(f"  total file: {n}", flush=True)
    return findings, time.time() - t0

def quarantine(findings):
    os.makedirs(QUAR, exist_ok=True)
    moved = []
    for f in findings:
        src = os.path.join(BASE, f["path"])
        dst = os.path.join(QUAR, f["path"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.move(src, dst)
            moved.append(f)
        except Exception as ex:
            print("  ! gagal pindah", f["path"], ex)
    prev = []
    if os.path.exists(MANIFEST):
        try: prev = json.load(open(MANIFEST))
        except Exception: prev = []
    json.dump(prev + moved, open(MANIFEST, "w"), indent=1)
    return moved

def restore():
    if not os.path.exists(MANIFEST):
        print("no manifest"); return
    items = json.load(open(MANIFEST))
    n = 0
    for f in items:
        src = os.path.join(QUAR, f["path"])
        dst = os.path.join(BASE, f["path"])
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst); n += 1
    json.dump([], open(MANIFEST, "w"))
    print(f"restored {n} files")

HARD = {'.exe','.dll','.scr','.com','.msi','.vbs','.vbe','.jar','.lnk','.hta',
        '.wsf','.apk','.deb','.rpm','.dmg','.pkg','.so','.dylib','.jnilib','.sys','.cpl','.ocx','.bin'}
RAW_ONLY = {'.ps1','.bat','.cmd'}   # scripts: only purge from raw repo clones
RAW_DIRS = ('repo-refs/',)

def scan_native_only():
    """Fast pass: list native executables by scope, no content read.

    repo-refs/  -> purge ALL native (raw clones, reference only)
    curated dirs-> purge HARD binaries only (keep .ps1/.bat/.cmd skill helpers)
    """
    out = []
    for p in walk():
        e = os.path.splitext(p)[1].lower()
        if e not in NATIVE:
            continue
        rel = os.path.relpath(p, BASE)
        in_raw = rel.startswith(RAW_DIRS)
        if in_raw or e in HARD:
            out.append({"path": rel, "tier": 1, "reasons": ["native-exec:"+e],
                        "size": os.path.getsize(p)})
    out.sort(key=lambda x: -x["size"])
    return out

# ---- T2b: HIGH-SIGNAL patterns for real script files (low false positive) ----
HIGH = [
    ("reverse-shell",  PAT[0][1]),
    ("downloader-exec",PAT[1][1]),
    ("base64-exec",    PAT[2][1]),
    ("crypto-miner",   PAT[5][1]),
    ("exfil-endpoint", PAT[6][1]),
    ("data-destroy",   PAT[9][1]),
    ("persistence",    re.compile(r"(crontab\s+-[el]|/Library/Launch(Agents|Daemons)/|schtasks\s+/create|reg\s+add\s+.*\\\\Run\b|>>\s*~?/?\.?authorized_keys|>>\s*~/\.bashrc)", re.I)),
]
SCRIPT_EXT = {'.sh','.bash','.zsh','.py','.ps1','.bat','.cmd','.vbs','.js','.mjs','.cjs','.rb','.pl','.php'}

def scan_code():
    """Refined content scan: scripts (high-signal) + md (hidden-unicode only)."""
    out = []
    t0 = time.time(); n = 0
    for p in walk():
        n += 1
        if n % 50000 == 0: print(f"  ...{n} ({time.time()-t0:.0f}s)", flush=True)
        e = os.path.splitext(p)[1].lower()
        if e not in SCRIPT_EXT and e != '.md':
            continue
        try:
            if os.path.getsize(p) > 1_000_000: continue
            txt = open(p, 'r', errors='ignore').read(MAXREAD)
        except Exception:
            continue
        reasons = []
        if e == '.md':
            if INJECT[2][1].search(txt): reasons.append("hidden-unicode")
        else:
            for name, rx in HIGH:
                if rx.search(txt): reasons.append(name)
        if reasons:
            out.append({"path": os.path.relpath(p, BASE), "tier": 2,
                        "reasons": reasons, "size": os.path.getsize(p)})
    out.sort(key=lambda x: -x["size"])
    json.dump(out, open(os.path.join(BASE, "scan-code.json"), "w"), indent=1)
    return out, time.time() - t0

def scan_aggressive():
    """AGGRESSIVE: flag EVERYTHING. All native exec everywhere, all content
    patterns on every text file, all md injections, plus exec-download in md.
    Skips root-level tooling (no '/') so the infra/scripts survive."""
    EXEC_DL = PAT[1][1]
    out = []
    t0 = time.time(); n = 0
    for p in walk():
        n += 1
        if n % 50000 == 0: print(f"  ...{n} ({time.time()-t0:.0f}s)", flush=True)
        rel = os.path.relpath(p, BASE)
        if "/" not in rel:          # root-level tooling: never quarantine
            continue
        e = os.path.splitext(p)[1].lower()
        reasons = []
        if e in NATIVE:
            reasons.append("native-exec:"+e)
        if e in TEXT_EXT or e in NATIVE:
            try:
                if os.path.getsize(p) <= 8_000_000:
                    txt = open(p, 'r', errors='ignore').read(MAXREAD)
                else:
                    txt = ""
            except Exception:
                txt = ""
            for name, rx in PAT:
                if rx.search(txt): reasons.append(name)
            if not reasons and EXEC_DL.search(txt): reasons.append("downloader-exec")
            if e == '.md':
                for name, rx in INJECT:
                    if rx.search(txt): reasons.append(name)
        if reasons:
            out.append({"path": rel, "tier": 2, "reasons": reasons,
                        "size": os.path.getsize(p)})
    out.sort(key=lambda x: -x["size"])
    json.dump(out, open(os.path.join(BASE, "scan-aggressive.json"), "w"), indent=1)
    return out, time.time() - t0

def main():
    args = sys.argv[1:]
    if "--restore" in args:
        restore(); return
    if "--aggressive" in args:
        findings, dt = scan_aggressive()
        byr = {}
        for f in findings:
            for r in f["reasons"]: byr[r] = byr.get(r, 0) + 1
        print(f"AGGRESSIVE {dt:.0f}s — {len(findings)} file kena")
        print("per alasan:", dict(sorted(byr.items(), key=lambda x: -x[1])))
        for f in findings[:15]:
            print(f"  {f['size']//1024:>7}KB  {f['path']}  <- {','.join(f['reasons'][:3])}")
        if len(findings) > 15: print(f"  ... +{len(findings)-15} lagi")
        if "--quarantine" in args:
            moved = quarantine(findings)
            print(f"\nQUARANTINE: {len(moved)} file dipindah")
        return
    if "--code" in args:
        findings, dt = scan_code()
        byr = {}
        for f in findings:
            for r in f["reasons"]: byr[r] = byr.get(r, 0) + 1
        print(f"scan {dt:.0f}s — {len(findings)} file kode/md mencurigakan (high-signal)")
        print("per alasan:", byr)
        for f in findings[:20]:
            print(f"  {f['size']//1024:>7}KB  {f['path']}  <- {','.join(f['reasons'])}")
        if len(findings) > 20: print(f"  ... +{len(findings)-20} lagi")
        if "--quarantine" in args:
            moved = quarantine(findings)
            print(f"\nQUARANTINE: {len(moved)} file dipindah")
        return
    if "--t1" in args:
        findings = scan_native_only()
        print(f"native executable (scope: repo-refs=all, curated=hard-only): {len(findings)} file")
        for f in findings[:15]:
            print(f"  {f['size']//1024:>7}KB  {f['path']}")
        if len(findings) > 15: print(f"  ... +{len(findings)-15} lagi")
        if "--quarantine" in args:
            moved = quarantine(findings)
            print(f"\nQUARANTINE: {len(moved)} file native dipindah ke {QUAR}")
        return
    findings, dt = do_scan()
    t1 = [f for f in findings if f["tier"] == 1]
    t2 = [f for f in findings if f["tier"] == 2]
    t3 = [f for f in findings if f["tier"] == 3]
    if "--json" in args:
        print(json.dumps(findings, indent=1)); return
    print(f"scan {dt:.1f}s — {len(findings)} temuan  (T1 native={len(t1)}  T2 kode={len(t2)}  T3 md-inject={len(t3)})")
    def show(lst, title, n=25):
        if not lst: return
        print(f"\n== {title} ==")
        for f in lst[:n]:
            print(f"  [{f['tier']}] {f['size']//1024:>7}KB  {f['path']}  <- {','.join(f['reasons'][:3])}")
        if len(lst) > n: print(f"  ... +{len(lst)-n} lagi")
    show(t2, "T2 kode mencurigakan")
    show(t3, "T3 markdown prompt-injection / exfil")
    show(t1, "T1 native executable (contoh 25 teratas)")
    if "--quarantine" in args:
        moved = quarantine(findings)
        print(f"\nQUARANTINE: {len(moved)} file dipindah ke {QUAR}  (balik: --restore)")

if __name__ == "__main__":
    main()
