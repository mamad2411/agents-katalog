#!/usr/bin/env python3
"""tool-install — jadikan repo yang benar-benar berupa TOOL bisa dipakai semua AI.

Masalahnya: 100k repo di repos.db cuma metadata; 99.9% di repo-refs hanya stub
(LICENSE/TREE.txt) sehingga "install" tidak mungkin. Skrip ini:

  1. clone dangkal repo (kalau belum ada kode nyata),
  2. deteksi cara install: Cargo.toml / go.mod / pyproject scripts / package.json bin,
  3. install ke ~/.agents/tools/<nama> (tidak mengotori global site-packages),
  4. symlink executable ke ~/.agents/bin (PATH bersama semua AI/CLI),
  5. catat ke ~/.agents/tools-installed.json + ~/.agents/TOOLS.md,
  6. kalau `--mcp`, cetak/daftarkan entri MCP (default: disabled).

Pakai:
  python3 ~/.agents/tool-install.py --dry-run <owner/name> [...]
  python3 ~/.agents/tool-install.py <owner/name>
  python3 ~/.agents/tool-install.py --mcp <owner/name>
  python3 ~/.agents/tool-install.py --list
"""
import json
import os
import re
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
BIN = os.path.join(AG, "bin")
TOOLS = os.path.join(AG, "tools")
REG = os.path.join(AG, "tools-installed.json")
CATALOG = os.path.join(AG, "TOOLS.md")


def sh(cmd, cwd=None, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def repo_dir(slug):
    return os.path.join(AG, "repo-refs", slug.replace("/", "_"))


def clone(slug):
    d = repo_dir(slug)
    if os.path.isdir(os.path.join(d, ".git")):
        return d, "sudah ada"
    r = sh([sys.executable, os.path.join(AG, "repo-hub.py"), "get", slug], timeout=900)
    if not os.path.isdir(d):
        return None, (r.stdout + r.stderr)[-300:]
    return d, "clone baru"


def has_code(d):
    """True kalau ada file selain stub metadata."""
    stub = {"license", "license.md", "license.txt", "tree.txt", "readme.md",
            "requirements.txt", "setup.py", ".git"}
    try:
        for e in os.listdir(d):
            if e.lower() not in stub and not e.startswith("."):
                return True
    except Exception:
        return False
    return False


def detect(d):
    """Tentukan metode install dari isi repo."""
    j = lambda f: os.path.join(d, f)
    if os.path.exists(j("Cargo.toml")):
        return "cargo", None
    if os.path.exists(j("go.mod")):
        target = "."
        if not any(f.endswith(".go") for f in os.listdir(d)):
            cand = []
            for root, dirs, files in os.walk(d, topdown=True):
                dirs[:] = [x for x in dirs if x not in (".git", "vendor", "testdata")]
                if "main.go" in files:
                    cand.append(root)
            if cand:
                base = os.path.basename(d).split("_", 1)[-1].lower()
                cand.sort(key=lambda c: (os.path.basename(c).lower() != base,
                                         os.path.basename(c).lower() not in base, len(c)))
                target = "./" + os.path.relpath(cand[0], d)
        return "go", target
    if os.path.exists(j("pyproject.toml")):
        txt = open(j("pyproject.toml"), encoding="utf-8", errors="ignore").read()
        if "[project.scripts]" in txt or "console_scripts" in txt:
            return "uv", None
    if os.path.exists(j("package.json")):
        try:
            pkg = json.load(open(j("package.json"), encoding="utf-8", errors="ignore"))
        except Exception:
            pkg = {}
        if pkg.get("bin"):
            return "npm", pkg
        if "mcp" in (json.dumps(pkg.get("keywords") or []) + (pkg.get("description") or "")).lower():
            return "mcp-node", pkg
    for f in os.listdir(d):
        if f.startswith("mcp") and f.endswith(".json"):
            return "mcp-json", None
    return None, None


def do_install(kind, d, name, pkg):
    os.makedirs(BIN, exist_ok=True)
    os.makedirs(TOOLS, exist_ok=True)
    if kind == "cargo":
        r = sh(["cargo", "install", "--path", d, "--root", os.path.join(TOOLS, name), "--locked"],
               timeout=3600)
        return r, [os.path.join(TOOLS, name, "bin")]
    if kind == "go":
        out = os.path.join(BIN, name)
        r = sh(["go", "build", "-o", out, pkg or "."], cwd=d, timeout=1800)
        return r, [BIN]
    if kind == "uv":
        r = sh(["uv", "tool", "install", d, "--force"], timeout=1800)
        return r, [os.path.join(HOME, ".local", "bin")]
    if kind == "npm":
        prefix = os.path.join(TOOLS, name)
        target = d
        pub = (pkg or {}).get("name")
        if pub and not (pkg or {}).get("private") and (pkg or {}).get("version"):
            target = f"{pub}@latest"   # registry: node_modules ikut, tidak "Cannot find module"
        r = sh(["npm", "install", "-g", "--prefix", prefix, target], timeout=1800)
        return r, [os.path.join(prefix, "bin")]
    return None, []


def link(bindirs, d):
    """Symlink semua executable ke ~/.agents/bin supaya ada di PATH."""
    made = []
    for bd in bindirs:
        if not os.path.isdir(bd):
            continue
        for f in os.listdir(bd):
            src = os.path.join(bd, f)
            if not os.path.isfile(src) or not os.access(src, os.X_OK):
                continue
            dst = os.path.join(BIN, f)
            if os.path.islink(dst) or os.path.exists(dst):
                continue
            os.symlink(src, dst)
            made.append(f)
    return made


def load_reg():
    try:
        return json.load(open(REG))
    except Exception:
        return {}


def save_reg(reg):
    with open(REG, "w") as f:
        json.dump(reg, f, indent=1, ensure_ascii=False, sort_keys=True)


def write_catalog(reg):
    lines = ["# Tool terpasang (bisa dipanggil semua AI lewat PATH)\n"]
    ok = {k: v for k, v in reg.items() if v.get("status") == "installed"}
    lines.append(f"total: {len(ok)}\n")
    for slug, v in sorted(ok.items()):
        lines.append(f"- **{v.get('bin') or slug}** ← `{slug}` ({v.get('kind')}) "
                     f"· perintah: `{v.get('cmd')}`\n")
    if not ok:
        lines.append("_(kosong — jalankan `python3 ~/.agents/tool-install.py <owner/name>`)_\n")
    open(CATALOG, "w").write("".join(lines))


def mcp_snippet(kind, d, name, pkg):
    if kind == "mcp-node":
        return {"command": "npx", "args": ["-y", name]}
    if kind == "mcp-json":
        return {"command": "python3", "args": [os.path.join(d, "server.py")]}
    if pkg and pkg.get("bin"):
        cmd = list(pkg["bin"].values())[0] if isinstance(pkg["bin"], dict) else pkg["bin"]
        return {"command": os.path.join(BIN, os.path.basename(cmd)), "args": []}
    return None


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    if a[0] == "--scan-local":
        # Inventaris: dari 17k repo yang sudah ter-clone, mana yang benar-benar bisa diinstall.
        out = []
        root = os.path.join(AG, "repo-refs")
        for d in sorted(os.listdir(root)):
            p_dir = os.path.join(root, d)
            if not os.path.isdir(p_dir) or "_" not in d:
                continue
            if not has_code(p_dir):
                continue
            kind, _ = detect(p_dir)
            if not kind:
                continue
            out.append({"slug": d.replace("_", "/", 1), "kind": kind})
        path = os.path.join(AG, "tool-candidates.json")
        json.dump(out, open(path, "w"), indent=1)
        import collections
        print(f"[scan-local] {len(out)} repo bisa diinstall -> {path}")
        for k, v in collections.Counter(x["kind"] for x in out).most_common():
            print(f"  {k}: {v}")
        return
    if a[0] == "--list":
        reg = load_reg()
        for slug, v in sorted(reg.items()):
            print(f"- {slug} [{v.get('status')}] bin={v.get('bin')} kind={v.get('kind')}")
        return
    dry = "--dry-run" in a
    want_mcp = "--mcp" in a
    slugs = [x for x in a if not x.startswith("-")]
    reg = load_reg()
    for slug in slugs:
        print(f"\n=== {slug} ===")
        d, note = clone(slug)  # dry-run tetap clone (dangkal) supaya metode bisa dideteksi
        if not d or not os.path.isdir(d):
            print("  GAGAL clone:", note)
            continue
        print("  repo :", d, f"({note})")
        if not has_code(d):
            print("  TOLAK: isinya stub (LICENSE/requirements saja), tidak ada kode nyata.")
            reg[slug] = {"status": "stub", "kind": None, "bin": None}
            save_reg(reg)
            continue
        kind, pkg = detect(d)
        name = slug.split("/")[-1].lower()
        if not kind:
            print("  TOLAK: tidak ada cara install yang dikenal (cargo/go/uv/npm bin/mcp).")
            reg[slug] = {"status": "unknown-install", "kind": None, "bin": None}
            save_reg(reg)
            continue
        print(f"  metode: {kind}")
        if dry:
            continue
        r, bindirs = do_install(kind, d, name, pkg)
        if r is None:
            print(f"  GAGAL: metode {kind} belum didukung untuk install otomatis.")
            reg[slug] = {"status": "manual", "kind": kind, "bin": None}
            save_reg(reg)
            continue
        if r.returncode != 0:
            print("  GAGAL install:", (r.stderr or r.stdout)[-400:])
            reg[slug] = {"status": "failed", "kind": kind, "bin": None}
            save_reg(reg)
            continue
        if kind == "go":
            bins = [name] if os.path.exists(os.path.join(BIN, name)) else []
        else:
            bins = link(bindirs, d)
        slugbin = bins[0] if bins else None
        cmd = slugbin or f"(tidak ada bin) {name}"
        print(f"  OK · bin: {', '.join(bins) or '-'}")
        reg[slug] = {"status": "installed", "kind": kind, "bin": slugbin, "cmd": cmd,
                     "path": d, "mcp": mcp_snippet(kind, d, name, pkg) if want_mcp else None}
        save_reg(reg)
        if want_mcp and reg[slug]["mcp"]:
            print("  MCP:", json.dumps(reg[slug]["mcp"]))
    write_catalog(load_reg())


if __name__ == "__main__":
    main()
