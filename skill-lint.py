#!/usr/bin/env python3
"""skill-lint.py — validasi skill curated (read-only).

Cek per skill di ~/.agents/skills-store/<nama>/SKILL.md:
  1. frontmatter ada (--- ... ---)
  2. name == nama folder (kebab-case)
  3. description ada & >= 20 karakter
  4. body >= 5 baris (bukan stub)
  5. script di scripts/ lolos syntax check (bash -n / py_compile)
  6. referensi file lokal (path ber-backtick) benar-benar ada

Pakai:
  python3 skill-lint.py                 # ringkasan + 20 masalah pertama
  python3 skill-lint.py --json          # semua masalah (JSON)
  python3 skill-lint.py --limit 50      # batasi jumlah skill dicek
Exit: 0 bersih, 1 ada masalah.
"""
import json
import os
import re
import subprocess
import sys

AG = os.path.expanduser("~/.agents")
STORE = f"{AG}/skills-store"
SKIP_DIRS = {".dupes", "skills-expanded", "node_modules", ".git"}


def parse_fm(text):
    """Parser frontmatter minimal: dukung nilai multi-baris (| dan >) + kutip."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    fm = text[3:end]
    body = text[end + 4:]
    data = {}
    key = None
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in ("|", ">", "|-", ">-", "|+", ">+"):
                buf = []
                i += 1
                while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                    buf.append(lines[i].strip())
                    i += 1
                data[key] = " ".join(x for x in buf if x).strip()
                continue
            data[key] = val.strip('"').strip("'")
        i += 1
    return data, body


def check_scripts(sdir):
    bad = []
    for root, _, files in os.walk(sdir):
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(".sh"):
                r = subprocess.run(["bash", "-n", p], capture_output=True, text=True)
                if r.returncode:
                    bad.append(f"{os.path.relpath(p, sdir)}: {r.stderr.strip().splitlines()[:1]}")
            elif f.endswith(".py"):
                r = subprocess.run([sys.executable, "-m", "py_compile", p],
                                   capture_output=True, text=True)
                if r.returncode:
                    bad.append(f"{os.path.relpath(p, sdir)}: {r.stderr.strip().splitlines()[:1]}")
    return bad


LOCAL_PATH = re.compile(r"`(~?[\w./-]+\.(?:sh|py|md|json|ya?ml|ts|js))`")


def check_refs(sdir, body):
    missing = []
    for m in LOCAL_PATH.finditer(body):
        p = os.path.expanduser(m.group(1))
        if p.startswith("~") or "/" not in p:
            continue
        cand = p if os.path.isabs(p) else os.path.join(sdir, p)
        if not os.path.exists(cand):
            missing.append(m.group(1))
    return sorted(set(missing))[:5]


def lint_one(p):
    d = os.path.dirname(p)
    name = os.path.basename(d)
    issues = []
    try:
        text = open(p, encoding="utf-8", errors="replace").read()
    except OSError as e:
        return name, [f"tidak bisa dibaca: {e}"]
    fm, body = parse_fm(text)
    if fm is None:
        issues.append("frontmatter tidak ada / tidak ditutup")
    else:
        if (fm.get("name") or "") != name:
            issues.append(f"name '{fm.get('name')}' != folder '{name}'")
        desc = fm.get("description") or ""
        if len(desc) < 20:
            issues.append(f"description terlalu pendek ({len(desc)} char)")
    if len([l for l in body.splitlines() if l.strip()]) < 5:
        issues.append("body terlalu pendek (<5 baris)")
    sd = os.path.join(d, "scripts")
    if os.path.isdir(sd):
        for b in check_scripts(sd):
            issues.append(f"script rusak: {b}")
    for m in check_refs(d, body):
        issues.append(f"file dirujuk tapi tidak ada: {m}")
    return name, issues


def main():
    fs_json = "--json" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        try:
            limit = int(sys.argv[sys.argv.index("--limit") + 1])
        except (IndexError, ValueError):
            pass
    targets = []
    for name in sorted(os.listdir(STORE)):
        if name in SKIP_DIRS or name.startswith("."):
            continue
        p = os.path.join(STORE, name, "SKILL.md")
        if os.path.isfile(p):
            targets.append(p)
    if limit:
        targets = targets[:limit]

    bad = {}
    warn = {}
    for p in targets:
        name, issues = lint_one(p)
        errs = [i for i in issues if not i.startswith("file dirujuk")]
        wrns = [i for i in issues if i.startswith("file dirujuk")]
        if errs:
            bad[name] = errs
        if wrns:
            warn[name] = wrns

    total = len(targets)
    if fs_json:
        json.dump({"total": total, "error": len(bad), "warning": len(warn),
                   "detail": {"error": bad, "warning": warn}},
                  sys.stdout, indent=1, ensure_ascii=False)
        print()
    else:
        print(f"skill dicek : {total}")
        print(f"ERROR       : {len(bad)} ({len(bad)*100//max(total,1)}%)")
        print(f"WARNING     : {len(warn)} (path template/dibuat-saat-jalan, tidak difailkan)")
        kinds = {}
        for issues in bad.values():
            for i in issues:
                k = i.split(":")[0]
                kinds[k] = kinds.get(k, 0) + 1
        for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
            print(f"  - {k}: {v}")
        for name, issues in list(bad.items())[:20]:
            print(f"\n{name}")
            for i in issues[:4]:
                print(f"  · {i}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
